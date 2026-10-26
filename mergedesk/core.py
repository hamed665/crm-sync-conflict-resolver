"""Three-way merge: distinguish absence, null, edits and deletions."""
from copy import deepcopy
import hashlib
import json

MISSING = object()

def canonical(record):
    return json.dumps(record, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)

def fingerprint(record):
    return hashlib.sha256(canonical(record).encode()).hexdigest()

def normalize(record):
    out = deepcopy(record)
    if isinstance(out.get('email'), str):
        out['email'] = out['email'].strip().casefold()
    if isinstance(out.get('name'), str):
        out['name'] = ' '.join(out['name'].split())
    return out

def describe(value):
    return {'present': False} if value is MISSING else {'present': True, 'value': deepcopy(value)}

def merge(base, local, remote):
    """Top-level atomic fields; unresolved conflicts retain baseline values."""
    if not all(isinstance(r, dict) for r in (base, local, remote)):
        raise ValueError('records must be dictionaries')
    # Validate JSON compatibility before producing a plan.
    for record in (base, local, remote): canonical(record)
    merged, conflicts, changes = {}, [], []
    for key in sorted(set(base) | set(local) | set(remote)):
        b, l, r = (record.get(key, MISSING) for record in (base, local, remote))
        if l == r: chosen, reason = l, 'agreement'
        elif l == b: chosen, reason = r, 'remote_edit'
        elif r == b: chosen, reason = l, 'local_edit'
        else:
            chosen, reason = b, 'conflict'
            conflicts.append({'field': key, 'base': describe(b), 'local': describe(l), 'remote': describe(r)})
        if chosen is not MISSING: merged[key] = deepcopy(chosen)
        if chosen != b: changes.append({'field': key, 'reason': reason, 'after': describe(chosen)})
    return {'record': merged, 'conflicts': conflicts, 'changes': changes,
            'base_fingerprint': fingerprint(base), 'ready': not conflicts}

def resolve(plan, decisions):
    """Require one explicit local/remote/base decision for every conflict."""
    required = {c['field'] for c in plan['conflicts']}
    if set(decisions) != required:
        raise ValueError('exactly one decision per conflict required')
    result = deepcopy(plan['record'])
    for conflict in plan['conflicts']:
        choice = decisions[conflict['field']]
        if choice not in ('base','local','remote'): raise ValueError('invalid decision')
        value = conflict[choice]
        if value['present']: result[conflict['field']] = deepcopy(value['value'])
        else: result.pop(conflict['field'], None)
    return result

def apply_if_unchanged(current, expected_fingerprint, replacement):
    """Pure optimistic-lock guard; adapter must make check+write atomic."""
    if fingerprint(current) != expected_fingerprint:
        raise ValueError('stale snapshot; recompute merge')
    canonical(replacement)
    return deepcopy(replacement)

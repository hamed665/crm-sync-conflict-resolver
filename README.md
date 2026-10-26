# MergeDesk

**Deterministic three-way CRM merge with explicit conflict review.**

![Python](https://img.shields.io/badge/python-3.11%2B-3776AB)
![License](https://img.shields.io/badge/license-MIT-green)

Synchronize contact edits without silently overwriting changes made in the other system.

An original, runnable reference implementation by Hamed Minaei. Uses only the
Python standard library. No API key, paid account or network access is needed
for the included demos and tests. Version 0.1.0 focuses on the core engineering
contract rather than a hosted production service.

## Capabilities

- Three-way merge using baseline, local and remote records
- Deletion distinguished from explicit null
- Field-level conflict plans requiring complete review decisions
- Canonical SHA-256 fingerprints for optimistic concurrency adapters
- Explicit opt-in normalization; no hidden fuzzy identity matching

## Quick start

```bash
git clone https://github.com/hamed665/crm-sync-conflict-resolver.git
cd crm-sync-conflict-resolver
python --version  # Python 3.11+
python -m mergedesk
python -m unittest discover -s tests -v
```

Optional library installation: `python -m pip install .`

## Use as a library

```python
from mergedesk.core import merge, resolve
plan = merge({"stage":"new"}, {"stage":"won"}, {"stage":"lost"})
record = resolve(plan, {"stage":"local"})
print(record)
```

## Data flow

Snapshots → three-way comparison → merge plan → explicit review → adapter write

See [mergedesk/core.py](mergedesk/core.py) for the implementation and [architecture notes](docs/architecture.md)
for transaction boundaries and deployment considerations.

## Verification

The test suite exercises behavioral guarantees, error paths and isolation.
SQLite projects also test competing connections with independent workers.
GitHub Actions runs the suite on Python 3.11, 3.12 and 3.13.
All fixtures are synthetic. Demo output is captured in
[examples/demo-output.txt](examples/demo-output.txt).

## Scope and limitations

This is a merge library, not a Salesforce or HubSpot connector. Nested fields are treated atomically. No automatic contact identity matching. The fingerprint guard is pure: a real adapter must enforce compare-and-swap atomically in its database. Persist review decisions and authorize access in the integrating service.

## Repository map

- `mergedesk/`: importable library and runnable CLI demo
- `tests/`: regression and invariant tests
- `examples/`: synthetic inputs and captured demo output
- `docs/`: design decisions and boundaries
- `.github/workflows/ci.yml`: repeatable verification

## License

MIT. See [LICENSE](LICENSE). Contributions: [CONTRIBUTING.md](CONTRIBUTING.md).

import json
from .core import merge, resolve
base = {'name': 'Demo Customer', 'stage': 'new', 'phone': None}
local = {**base, 'stage': 'qualified'}
remote = {**base, 'stage': 'contacted', 'phone': '+000-DEMO'}
plan = merge(base, local, remote)
print(json.dumps({'plan': plan, 'reviewed': resolve(plan, {'stage': 'local'})}, indent=2))

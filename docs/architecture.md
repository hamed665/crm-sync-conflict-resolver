# Design notes — MergeDesk

## Contract

Synchronize contact edits without silently overwriting changes made in the other system.

## Execution path

Snapshots → three-way comparison → merge plan → explicit review → adapter write

## Design choices

1. Three-way merge using baseline, local and remote records.
2. Deletion distinguished from explicit null.
3. Field-level conflict plans requiring complete review decisions.
4. Canonical SHA-256 fingerprints for optimistic concurrency adapters.
5. Explicit opt-in normalization; no hidden fuzzy identity matching.

## Integration boundary

This is a merge library, not a Salesforce or HubSpot connector. Nested fields are treated atomically. No automatic contact identity matching. The fingerprint guard is pure: a real adapter must enforce compare-and-swap atomically in its database. Persist review decisions and authorize access in the integrating service.

## Failure handling

Validation errors are explicit exceptions. SQLite mutations use bound SQL
parameters; multi-step mutations commit together or roll back. Library results
are data structures suitable for an adapter layer. No network calls or secrets
are embedded in the examples.

## Before deployment

Choose an authenticated adapter, add structured operational logging without raw
customer data, define backup and retention requirements, and test realistic
workloads. The local tests establish specific invariants; they do not establish
production throughput, external integration compatibility or service availability.

# Reviewable Promotion Proposals

A Pending packet and its Triage record are evidence. They are not yet a reusable knowledge record.

The proposal stage creates a deterministic **review package**:

```
Pending
-> Triage
-> Promotion Proposal
-> explicit accept/reject
-> typed intake record
-> later domain promotion if warranted
```

A proposal may suggest an ID, type, status, domains, tags, provenance, related records, and possible duplicates. Suggestions are non-authoritative.

## Safety boundary

Automatic proposal generation may suggest only `observed` or `candidate` status. It cannot create Experimental, Validated, or Canonical knowledge.

Accepting a proposal creates a typed record under `intake/records/<type>/`. It does not modify Canonical governance or promoted domain records.

The original Pending packet remains immutable evidence. A review ledger records whether the proposal was accepted or rejected.

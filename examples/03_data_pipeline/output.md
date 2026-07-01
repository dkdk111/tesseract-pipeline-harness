## Produce the weekly analytics dataset

## Ingest raw events from all sources

### Ingest web events
- Source pulled incrementally since the last watermark.
- Schema and volume checks passed at the boundary.

### Ingest mobile events
- Source pulled incrementally since the last watermark.
- Schema and volume checks passed at the boundary.

### Ingest billing events
- Source pulled incrementally since the last watermark.
- Schema and volume checks passed at the boundary.

### Validate and clean the ingested data
- Nulls, duplicates, and out-of-range values flagged and quarantined.
- Row counts reconciled against the source.
- (revised in light of: ## Ingest raw events from all sources)

## Transform into the analytics schema

### Sessionize events
- Events grouped into sessions by inactivity gap.
- Session boundaries stable across reruns.
- (revised in light of: ## Ingest raw events from all sources)

### Derive user dimensions
- User dimensions derived with slowly-changing history kept.
- Keys conform to the warehouse model.
- (revised in light of: ## Ingest raw events from all sources)

### Compute revenue facts
- Revenue facts computed and reconciled to billing.
- Currency and refunds handled explicitly.
- (revised in light of: ## Ingest raw events from all sources)

### Load into the warehouse
- Loaded idempotently; partitions swapped atomically.
- A downstream freshness signal was emitted.
- (revised in light of: ## Ingest raw events from all sources)

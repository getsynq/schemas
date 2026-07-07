# Coalesce Quality JSON Schemas

Public JSON Schema definitions for Coalesce Quality tools and services.

**Live site:** https://schemas.synq.io

## URL Convention

```
https://schemas.synq.io/<tool>/<version>/<name>.schema.json
https://schemas.synq.io/<tool>/draft/<name>.schema.json
```

## Schema Status

- **Stable** (`v1/`, `v2/`, etc.) — Production-ready, follows semver for breaking changes
- **Draft** (`draft/`) — In development, may change without notice. Marked with `"x-status": "draft"` in the schema root.

## Available Schemas

| Schema | Status | Description |
|--------|--------|-------------|
| [synq-dwh/v1/config.schema.json](synq-dwh/v1/config.schema.json) | Stable | Configuration for the synq-dwh agent |
| [synq-recon/v1/config.schema.json](synq-recon/v1/config.schema.json) | Stable | Configuration for the synq-recon reconciliation tool |
| [synq-recon/v1/audit-log.schema.json](synq-recon/v1/audit-log.schema.json) | Stable | synq-recon reconciliation-run audit log output |
| [synq-scout/v1/config.schema.json](synq-scout/v1/config.schema.json) | Stable | Configuration for the synq-scout triage agent |
| [webhook/v1/event.schema.json](webhook/v1/event.schema.json) | Stable | Webhook event payload sent on issue/incident lifecycle events |
| [synq-monitors/draft/config.schema.json](synq-monitors/draft/config.schema.json) | Draft | Configuration for synq-monitors (observability as code) |

## Adding a New Schema

1. Create a directory for your tool: `<tool-name>/draft/`
2. Add your `.schema.json` file(s)
3. Set `$id` to match the public URL: `https://schemas.synq.io/<tool>/draft/<name>.schema.json`
4. Add `"x-status": "draft"` to the schema root
5. When stable, move to `<tool-name>/v1/` and update `$id` accordingly

## Custom Domain Setup

The site is served via GitHub Pages with a custom domain (`schemas.synq.io`). DNS must have a CNAME record pointing `schemas.synq.io` to `getsynq.github.io`.

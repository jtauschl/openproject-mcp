# Changelog

All notable changes to this project will be documented in this file.

---

## [1.0.0] — 2026-03-31

First public release.

### Added

- **Projects** — list, get, create, copy (with background job tracking), update, delete; read admin context, project configuration, and lifecycle phase definitions/instances
- **Work packages** — list with structured filters (`project`, `type`, `version`, `has_description`); free-text search with optional `project`, `status`, `open_only`, `assignee_me` filters; get, create, create subtask, update, delete; add comments; create and delete relations; get relations and activity log; list open work packages assigned to current user
- **Watchers** — list, add, remove
- **Attachments** — list, get, upload, delete
- **File links** — list, delete (Nextcloud CE integration)
- **Time entries** — list, get, create, update, delete; list available activities
- **Versions** — list (global or project-scoped), get, create, update, delete
- **Boards** — list, get, create (basic and grouped), update, delete; list saved views, get view
- **Memberships** — list, get, create, update, delete; list roles and principals; get current user's project access
- **Users** — get current user; list, get, create, update, delete, lock, unlock
- **Groups** — list, get, create, update (full member-list replacement with add/remove helpers), delete
- **Documents** — list, get, update (read-only create/delete in CE API)
- **News** — list, get, create, update, delete
- **Wiki pages** — list, get (no write API in CE)
- **Categories** — list, get (no write API in CE)
- **Notifications** — list, mark single read, mark all read
- **Grids** — list, get, create
- **User preferences** — get, update
- **Instance configuration** — get
- **Query metadata** — get filter, column, operator, sort-by; list and get filter-instance schemas
- **Help texts** — list, get
- **Working days** — list working days configuration; list non-working days
- **Custom options** — get
- **Relations (global)** — list, update
- **Actions & capabilities** — list
- **Text rendering** — render markdown/plain text to HTML via OpenProject API

### Architecture

- Five-module layout: `server.py`, `config.py`, `client.py`, `models.py`, `tools.py`
- All policy-sensitive logic (read gates, write gates, project scoping, field hiding) concentrated in `client.py`
- Preview/confirm two-step pattern for all write and delete operations; bypassable per operation class via `OPENPROJECT_AUTO_CONFIRM_WRITE` / `OPENPROJECT_AUTO_CONFIRM_DELETE`
- Project allowlists (`OPENPROJECT_ALLOWED_PROJECTS_READ`, `OPENPROJECT_ALLOWED_PROJECTS_WRITE`) matched case-insensitively against identifier, name, and numeric ID; hyphenated name variant tested for HAL-embedded links
- Field hiding per entity type via `OPENPROJECT_HIDE_<ENTITY>_FIELDS`; hidden fields are rejected on writes too
- Scoped read/write enable flags per chain (`project`, `membership`, `work_package`, `version`, `board`)
- HAL responses normalized into compact dataclasses; raw payloads never forwarded to MCP clients
- Pagination bounded by `OPENPROJECT_DEFAULT_PAGE_SIZE`, `OPENPROJECT_MAX_PAGE_SIZE`, `OPENPROJECT_MAX_RESULTS`
- Form validation against OpenProject schema endpoints before any create/update write

### Scope

- Community Edition only — Enterprise Edition features (Placeholder Users, Budgets, Portfolios, Programs, Custom Actions, Baseline Comparisons) are not implemented
- Nextcloud file links included (CE feature; returns empty list gracefully if Nextcloud not connected)
- Project lifecycle phases included (read-only; returns empty gracefully if unavailable)

### Known API notes

- Project-scoped endpoints for work packages and versions are deprecated in OpenProject 17.2 in favour of workspace-scoped alternatives; the deprecated paths remain in use as the workspace-scoped alternatives are not yet stable in CE
- Relations use the canonical `/api/v3/relations` endpoint with a filter instead of the redirecting project-scoped path
- Groups PATCH requires a complete `_links.members` array (full replacement); the client fetches the current list and applies adds/removes before sending

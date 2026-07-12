# Changelog

All notable changes to the LogistiX project will be documented in this file.

## [Unreleased]
- Initial creation of Phase 1 foundational architecture.
- Setup of Odoo 18 and PostgreSQL 16 via Docker Compose.
- Scaffolded empty LogistiX custom addon structure.
- Generated synthetic production-grade CSV datasets.

## Phase 2 (Completed)
- Created Odoo ORM models mapped from the approved database schema.
- Added mixins (Document, Timestamp, Audit).
- Configured mail.thread for Trip and Document models.
- Set up model parameters (_rec_name, _order) and unique SQL constraints.
- Optimized indexing and documented with docstrings.

## Phase 3 (Completed)
- Implemented complete Security Layer for LogistiX.
- Created application category and 5 security groups (Driver, Dispatcher, Fleet Manager, Finance Manager, Administrator).
- Integrated native Odoo groups (fleet.fleet_group_manager, hr_expense.group_hr_expense_manager, base.group_system).
- Defined 17 ACL entries across all 5 custom models following least privilege principle.
- Audit Log made immutable: Administrator read/create only, no write or delete for any role.
- Notifications set to read-only for Drivers (system-generated).
- Created 18 explicit record rules with no unrestricted access for restricted roles.
- Verified: no ACL conflicts, no duplicate XML IDs, no orphan record rules.


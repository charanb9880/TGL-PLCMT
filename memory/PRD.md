# PES Placement Intelligence PRD

## Original Problem Statement
Build a production-grade enterprise Progressive Web App for placement intelligence with a frame-by-frame scroll experience, one exact `public.company` schema sourced from Excel, sticky global navigation, company explorer, categories, compare mode, rule-based skill mapping, analytics dashboard, and PWA install/offline readiness.

## User Choices
- Excel file already uploaded
- Strict Supabase + PostgreSQL desired ultimately
- No login for now
- First priority: full frame-based UI and navigation
- Visual direction: minimal like Apple + Notion, but professional
- Phase 2 priority: analytics drill-downs, persistent filters, guided navigation, share links, and exports
- Phase 3 priority: real Supabase data, saved faculty tools, performance improvements, and final PWA polish
- Phase 4 priority: faculty review boards, reusable dashboards, PDF exports, skeletons, and final committee-grade UX

## Architecture Decisions
- Frontend: React + Tailwind + Framer Motion with route-based sections and frame-style experiences
- Backend: FastAPI API layer used for dataset status, import utilities, comparison/skill-match helpers, and DB-backed fallbacks
- Database: Supabase PostgreSQL via Transaction Pooler URI, with `public.company` created from the uploaded workbook
- Data strategy: frontend now reads real company data through Supabase client hooks; backend also points to the same Supabase table
- PWA baseline: manifest, service worker registration, offline fallback page, install prompt banner, installable shell assets
- State architecture: central filter context with URL query persistence plus localStorage backup for cross-route continuity
- Faculty architecture: localStorage-backed review boards, saved dashboards, saved comparison workspaces, and CSV/PDF-ready export flows
- Performance architecture: lazy-loaded routes, debounced Supabase search/filtering, in-memory company cache, pagination-ready data hooks, and skeleton loading states

## User Personas
- Students evaluating company fit and preparation strategy
- Faculty guiding placements using structured evidence
- Placement/admin teams reviewing category, hiring, and employer signals
- Placement committees creating reusable boards, dashboards, and briefing artifacts for panel decisions

## Core Requirements (Static)
- Preserve company schema exactly; no hardcoded company records
- Support scalable company browsing and detail rendering
- Provide comparison and rule-based skill mapping
- Provide analytics for company distribution and hiring/work patterns
- Deliver premium responsive PWA UX with full-height frame-based sections
- Keep filters, comparisons, exports, and data hooks async-ready for live Supabase usage

## What's Been Implemented
### 2026-04-19 — Phase 1
- Parsed the uploaded workbook and mapped the `Companies` sheet with 164 exact columns
- Replaced starter backend with placement intelligence APIs: dataset status, import preview/upload, companies list/detail, analytics, compare, skill match
- Built premium multi-route frontend: Home, Explore Companies, Categories, Compare, Skill Mapping, Analytics, Company Detail
- Implemented 10-frame company detail experience with sticky side navigation and exact field rendering
- Added rule-based skill mapping flow using company tech/automation/relevance fields
- Added comparison tables with strengths/weaknesses/risks summaries
- Added analytics charts and KPI cards
- Added PWA manifest, service worker, offline fallback, and generated app icon assets
- Added explicit loading/error states across data-driven pages
- Completed self-testing plus testing-agent validation with fixes resolved

### 2026-04-19 — Phase 2 Product Intelligence Layer
- Added central filter state with URL query persistence and localStorage backup across Explore, Categories, and Analytics
- Upgraded analytics into interactive drill-down controls that update global filters and hand off directly into filtered explorer flows
- Connected Categories view to the same global filter state used by Explore and Analytics
- Implemented shareable comparison links using `/compare?c1={id1}&c2={id2}` with restore-on-refresh behavior
- Added faculty-ready CSV exports for filtered company lists and 2-company comparisons
- Enhanced company detail navigation with active-section highlighting, sticky jump navigation, and scroll progress tracking
- Improved visual intelligence on company cards with contextual imagery plus safer logo handling
- Replaced unstable chart sizing with measured chart containers for more reliable analytics rendering
- Self-tested Phase 2 flows: drill-down filtering, filtered explorer handoff, comparison share links, both CSV exports, and company-detail guided navigation

### 2026-04-19 — Phase 3 Real Data + Final Intelligence Layer
- Added Supabase environment configuration to frontend and backend
- Created and ran workbook-to-Supabase importer, populating `public.company` with 10 rows and 164 exact columns
- Switched main frontend read flows to real Supabase hooks: `useCompanies`, `useFilteredCompanies`, `useCompany`, plus debounced query behavior and in-memory caching
- Confirmed backend now reports `database_configured=true` and `database_table_ready=true`
- Added saved filter presets for faculty workflows and saved comparison workspaces with localStorage + URL restore
- Added one-click faculty briefing pack CSV export containing key metrics, top companies, filtered company list, and comparison snapshot
- Added install prompt UI and lazy-loaded route bundles for better PWA/performance readiness
- Fixed compare share-link clipboard fallback after testing-agent regression report
- Completed regression testing on real-data flows, exports, analytics drill-downs, comparison workspaces, and company-detail Supabase reads

### 2026-04-19 — Phase 4 Final Intelligence & Faculty Layer
- Added `/faculty/review-boards` with board creation, board storage, filtered company selection, board-level metrics, hiring signals, risk indicators, and CSV/PDF exports
- Added reusable dashboard saving/sharing for analytics states via localStorage-backed dashboard records and shareable links
- Upgraded PDF export from placeholder to print-ready faculty output for analytics summaries, comparison reports, and review boards
- Added skeleton loaders for company list and company detail loading states
- Added final navigation polish with Faculty Boards route, tighter header behavior, and committee-grade access to new modules
- Preserved all prior systems without changing schema or introducing fake data

## Current Data/Integration State
- App is connected to Supabase and reads live data from `public.company`
- Backend and frontend are aligned to the same real dataset
- Faculty layer now includes boards, dashboards, CSV exports, and print-ready PDF flows

## Prioritized Backlog
### P0
- Add richer PDF styling for multi-page faculty packets if needed
- Add additional skeleton variants for analytics drill-down subpanels

### P1
- Add richer analytics drill-down combinations and optional tech-stack-specific filters
- Add faculty-facing export presets and scheduled reporting flows
- Improve company detail current-section banner synchronization edge cases in very fast scroll transitions

### P2
- Add saved comparison review boards for teams/faculty cohorts
- Add workbook management/history for repeated uploads
- Add advanced mobile gesture polish and presentation/export options beyond CSV/PDF

## Next Tasks
- Deepen analytics combinations for more faculty-grade scenario analysis
- Expand print styling into multi-page briefing packets if required
- Add richer skeleton/empty-state variants for every heavy data view

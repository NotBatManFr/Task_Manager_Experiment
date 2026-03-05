# FastAPI Service-Split Plan (Microservices-Ready)

## Current Coupling Pain Points

The current FastAPI package mixes HTTP handlers, domain logic, persistence, and infrastructure in one deployable unit:

- `main.py` owns routes and directly instantiates repository objects.
- `repository.py` encodes persistence and business workflow together.
- SQLAlchemy model shape leaks into API responses.
- DB initialization and retry logic run in-process with the API.

This makes scaling, testing, and service isolation harder.

---

## Target Architecture (Strangler-Friendly)

Split by bounded context and by change frequency:

1. **Task API Service (public edge API)**
   - Owns external HTTP contract for UI.
   - No direct DB access.
   - Calls internal services via HTTP/gRPC and composes responses.

2. **Task Command Service (write path)**
   - Owns create/update/delete rules.
   - Persists task changes.
   - Emits domain events (`task.created`, `task.updated`, `task.deleted`).

3. **Task Query Service (read path)**
   - Owns list/detail task reads.
   - Can use separate read-optimized schema later.
   - Supports filters/sorting/pagination for UI.

4. **Persistence Adapter Service (interim anti-corruption layer)**
   - Wraps current SQLAlchemy models/repositories initially.
   - Keeps DB concerns isolated while app contracts stabilize.
   - Can later be absorbed by command/query services once code is migrated.

5. **Gateway/BFF (optional if Task API acts as BFF)**
   - Handles CORS, auth token forwarding, and response shaping for UI.
   - Lets UI evolve without internal contract churn.

> Minimum viable split for this project: **Task API + Task Command + Task Query**.

---

## Package Split Inside `api/` (Step 1: Modular Monolith)

Before deploying separate services, split code in-place to enforce boundaries:

```text
api/
  app/
    edge/                  # external HTTP endpoints (UI-facing)
      routers/tasks.py
      dto.py
    application/           # use-cases / orchestration
      commands.py
      queries.py
      ports.py             # interfaces (repo/event/outbound)
    domain/                # pure business model/rules
      task.py
      events.py
      services.py
    infrastructure/        # adapters
      db/
        models.py
        session.py
        repositories.py
      messaging/
        publisher.py
      clients/
        task_command_client.py
        task_query_client.py
    bootstrap/
      container.py         # wiring dependencies
      config.py
    main.py
```

### Dependency Rule

- `edge -> application -> domain`
- `infrastructure` implements `application` ports
- `domain` imports nothing from FastAPI/SQLAlchemy

This lets each module become a standalone service with minimal code movement.

---

## Service Responsibilities and Contracts

## 1) Task API Service (UI-facing)

### Owns
- `POST /tasks`
- `GET /tasks`
- `PUT /tasks/{id}`
- `DELETE /tasks/{id}`
- Auth/context propagation (future)

### Calls
- `task-command-svc` for writes
- `task-query-svc` for reads

### Must Not
- Import SQLAlchemy model/session
- Read database credentials

## 2) Task Command Service

### Owns
- Validation beyond schema (business invariants)
- Idempotent write semantics
- Transaction boundaries

### API (internal)
- `POST /internal/tasks`
- `PUT /internal/tasks/{id}`
- `DELETE /internal/tasks/{id}`

### Data
- Canonical write store (existing Postgres table initially)

## 3) Task Query Service

### Owns
- Read model for list/details
- Query performance concerns

### API (internal)
- `GET /internal/tasks`
- `GET /internal/tasks/{id}`

### Data
- Same DB initially; optional separate read replica/materialized view later.

---

## Database Decoupling Strategy

## Phase A: Shared DB, separate schemas
- Keep one Postgres instance.
- Create separate schemas (`task_command`, `task_query`) to reduce accidental coupling.
- Forbid cross-service table writes.

## Phase B: Event-driven sync
- Command service emits events to a broker (e.g., Redis Streams/Kafka/RabbitMQ).
- Query service builds denormalized read tables.

## Phase C: Fully isolated persistence
- Each service owns its own datastore lifecycle and migrations.

---

## API Contract Stability

- Create explicit DTOs for external API (`TaskRequest`, `TaskResponse`) decoupled from ORM models.
- Version external routes (`/v1/tasks`).
- Add OpenAPI schemas per service; publish internal contracts.
- Add backward-compatible change rules (additive fields only in v1).

---

## Deployment Readiness Checklist

1. **Config split**
   - Per-service env vars (`SERVICE_NAME`, `DATABASE_URL`, `BROKER_URL`, `UPSTREAM_*`).
2. **Health endpoints**
   - `/health/live` and `/health/ready` with dependency checks.
3. **Observability**
   - Correlation IDs, structured logs, request metrics, error budgets.
4. **Security boundaries**
   - Internal service auth (mTLS or signed service tokens).
5. **Resilience**
   - Timeouts, retries with jitter, circuit breakers for internal calls.

---

## Suggested Migration Plan (6 Iterations)

1. **Introduce layers in current service**
   - Move route logic to `edge`, use-cases to `application`, ORM to `infrastructure`.
2. **Define ports and adapters**
   - Repository and event publisher interfaces in `application/ports.py`.
3. **Split read and write use-cases**
   - Separate command/query handlers (CQRS-lite in monolith).
4. **Extract Task Query Service first**
   - Lower risk; route `GET /tasks` through internal client.
5. **Extract Task Command Service**
   - Move write endpoints; keep Task API as stable facade.
6. **Introduce async events + independent datastores**
   - Remove remaining shared-DB assumptions.

---

## Team/Code Ownership Boundaries

- `edge` team owns public API and UI compatibility.
- `command` team owns mutation logic and invariants.
- `query` team owns read performance and projections.
- No team commits directly to another service's persistence layer.

---

## Immediate Next Actions in This Repository

1. Add `application/ports.py` and move current `TaskRepository` behind an interface.
2. Create `edge/routers/tasks.py` and keep `main.py` as wiring only.
3. Introduce `TaskService` use-cases (`create_task`, `list_tasks`, `update_task`, `delete_task`).
4. Replace direct ORM response with Pydantic response DTOs.
5. Add `/v1/tasks` while preserving current `/tasks` temporarily.
6. Add internal client stubs (`task_command_client.py`, `task_query_client.py`) that currently call local handlers, then swap to HTTP later.

This path keeps the current app working while making extraction to microservices mostly a deployment concern rather than a rewrite.


---

## Scope Re-Baseline After Layered Refactor

The layered refactor is a good step, but several modules still hold multiple responsibilities and should be split before extracting deployable services.

### Components still doing too much

1. **`api/app/main.py`**
   - Currently wires middleware/routes **and** executes schema creation (`Base.metadata.create_all`).
   - Recommendation: move schema/migration bootstrapping to startup tasks or migrations (Alembic) so app entrypoint remains transport wiring only.

2. **`api/app/database.py`**
   - Handles env resolution, URL composition, retry strategy, engine creation, and session factory in one module.
   - Recommendation: split into `config.py` (settings), `engine.py` (engine/retry policy), and `session.py` (SessionLocal/get_db).

3. **`api/app/edge/routers/tasks.py`**
   - Handles two API versions in one router and includes mapping concerns.
   - Recommendation: keep a thin unversioned compatibility router that delegates to a canonical `v1` router.

4. **`api/app/infrastructure/db/repositories.py`**
   - Combines command + query operations, ORM mapping, ID generation, and transaction commits.
   - Recommendation: split into `task_command_repository.py`, `task_query_repository.py`, and `mappers.py`; consider Unit-of-Work for commit boundaries.

5. **`ui/src/hooks/useTasks.ts`**
   - Chooses data source (`apiService` vs `localStorageService`) and manages optimistic update behavior in one hook.
   - Recommendation: move source selection behind a BFF/configurable provider; keep hook focused on UI state transitions.

### Microservice split scope (what to extract, in order)

1. **Task Query Service (extract first)**
   - Scope: list/read endpoints and query concerns.
   - Input contracts: `GET /tasks`, `GET /v1/tasks`.
   - Implementation source: query methods from repository + read-only application handlers.

2. **Task Command Service (extract second)**
   - Scope: create/update/delete invariants and write transactions.
   - Input contracts: POST/PUT/DELETE task endpoints.
   - Implementation source: command methods from repository + service write use-cases.

3. **Task API/BFF Facade (keep stable at edge)**
   - Scope: external contract, versioning, auth/context propagation, compatibility endpoints.
   - Calls command/query services over internal HTTP.

### Out-of-scope for immediate split

- Auth service extraction (until user context exists).
- Independent database per service (defer until command/query boundaries are stable and events are introduced).

### Execution checkpoints

- [ ] Separate command/query repository modules.
- [ ] Introduce explicit command/query handlers in application layer.
- [ ] Keep only versioned routes in canonical router; legacy routes become aliases.
- [ ] Move schema creation out of `main.py`.
- [ ] Add integration tests that mock internal command/query clients at API facade boundary.

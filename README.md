# 🧪 Microservice Automated Testing Workshop

> **Python + FastAPI + Postgres + Pact + Testcontainers**
> **Duration:** ~4 hours
> **Audience:** DevOps Engineers (Intermediate–Senior)

---

## 🧭 1. Workshop Goals

By the end of this session, you will be able to:

- ✅ Understand how DevOps interfaces with different layers of testing
- ✅ Run and write integration, contract, and component tests
- ✅ Test microservices with real databases and real service interactions
- ✅ Use **Pact** for consumer-driven contract testing
- ✅ Use **Testcontainers** to boot ephemeral test environments
- ✅ Run tests locally and in CI
- ✅ Debug failing microservices

---

## 🧱 2. Architecture Overview

```
Service A (Inventory)  --->  Service B (Math)
      |                           ^
      | SQL (Postgres)            |
      +---------------------------+
```

### Service A (Inventory)

- **Framework:** FastAPI
- **Database:** PostgreSQL (using raw `psycopg2`)
- **Purpose:** Stores items in Postgres

#### Endpoints:

| Method | Endpoint        | Description                    |
|--------|-----------------|--------------------------------|
| GET    | `/items`        | List all items                 |
| GET    | `/items/{id}`   | Get specific item by ID        |
| POST   | `/items`        | Create a new item              |
| GET    | `/total`        | Get total sum from Service B   |

### Service B (Math)

- **Framework:** FastAPI
- **Purpose:** Computes sums

#### Endpoints:

| Method | Endpoint | Description                                           |
|--------|----------|-------------------------------------------------------|
| POST   | `/sum`   | Returns enriched data including `processed_at` (UTC)  |

---

## 🐳 3. Start the Environment

From the project root:

```bash
docker compose up -d --build
```

### Verify endpoints:

```bash
# Test Service A
curl http://localhost:8000/items

# Test Service B
curl -X POST http://localhost:8001/sum \
  -H "Content-Type: application/json" \
  -d '{"numbers":[1,2]}'
```

**Expected results:**
- `/items` → Returns `apple` + `banana`
- `/sum` → Returns JSON with `total`, `count`, `processed_at`, `version`

---

## 🧪 4. Integration Testing Exercises

**Write your tests in:** `tests/integration/`

### ✔ Exercise 4.1 — Test GET /items

**Assertions:**
- Status code `200`
- Response is a list
- Contains `apple` + `banana`

### ✔ Exercise 4.2 — Test GET /items/{id}

**Test cases:**
- `/items/1` returns item
- `/items/9999` returns `404`

### ✔ Exercise 4.3 — Test POST /items

**Steps:**
1. Create `{"name": "orange", "price": 3.1}`
2. Assert `201` status
3. Assert item fields exist
4. GET `/items` again → ensure new item persists

### ✔ Exercise 4.4 — Test GET /total

This endpoint:
- Reads all item prices from DB
- Calls Service B `/sum`
- Returns enriched structure

**Your test should assert:**
- Keys: `total`, `count`, `processed_at`, `version`
- `count` equals number of DB rows
- `total > 0`

---

## 🔗 5. Contract Testing Exercises (Pact)

**Directory:** `tests/contract/test_sum_contract.py`

### Goal:
Define a consumer contract for `POST /sum`

**Expected fields:**
- `total`
- `count`
- `processed_at`
- `version`

### High-level steps:

1. Configure Pact mock server
2. Define provider expectations
3. Trigger request from Service A consumer test
4. Assert on schema
5. Generate the pact file

> **Note:** Later (in solution branch), you will run the provider verification.

---

## 🧱 6. Component Testing (Testcontainers)

**Directory:** `tests/component/test_service_a_component.py`

### Goal:

Use **Testcontainers** to simulate a real microservice environment without Docker Compose.

**Steps:**
1. Use Testcontainers to run a real ephemeral Postgres
2. Create the `items` table
3. Insert 2 fake items
4. Boot Service A (pointed at Testcontainers DB)
5. Assert `/items` returns expected results

---

## 🤖 7. Run All Tests

```bash
poetry run pytest
```

**Expected results:**
- ✅ Integration tests → PASS
- ✅ Pact contract test → generates `.json` file
- ✅ Component test → PASS

---

## 🚦 8. CI (GitHub Actions)

In the main branch, CI contains placeholder steps:

```yaml
echo "TODO: pytest tests/integration"
```

### Your task:

1. Replace placeholders with real `pytest` commands
2. Push to GitHub
3. CI should run your tests

---

## 🧠 9. Debugging Tips

### Common issues:

- ❌ Postgres not ready
- ❌ Wrong `DATABASE_URL`
- ❌ Service B unreachable
- ❌ Pact mock server not started properly
- ❌ Component test port conflicts

### Tips:

- 💡 Use `docker logs` to inspect container output
- 💡 Run `curl` to isolate failing endpoints
- 💡 Add `print()` statements in tests to inspect data

---

## 🎉 That's it!

You now have the foundation to test microservices the way DevOps engineers do every day:

- ✨ **Real services**
- ✨ **Real databases**
- ✨ **Real contracts**

Happy testing! 🚀
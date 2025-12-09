# Microservice Automated Testing Workshop

**Python • FastAPI • PostgreSQL • Pact • Testcontainers**

## 1. Workshop Objectives

By the end of this workshop, you will be able to:

- Write integration tests for microservices using HTTP requests
- Write consumer contract tests using Pact
- Write component tests using Testcontainers
- Validate cross-service behavior
- Run tests locally and in CI
- Debug failing tests and identify microservice issues


## 2. Architecture Overview

```
Service A (Inventory) ---> Service B (Math)
        |
        v
   PostgreSQL
```

### Service A

- FastAPI application
- Connects to PostgreSQL using raw psycopg2

**Endpoints:**
- `GET /items`
- `GET /items/{id}`
- `POST /items`
- `GET /total` (calls Service B)

### Service B

- FastAPI application

**Endpoint:**
- `POST /sum`

**Returns:**
- `total`
- `count`
- `processed_at` (UTC timestamp)
- `version`

## 3. Starting the Environment

Run:

```bash
docker compose up -d --build
```

Verify the services:

```bash
curl http://localhost:8000/items
curl -X POST http://localhost:8001/sum -H "Content-Type: application/json" -d '{"numbers":[1,2]}'
```

Both commands should return valid JSON.

## 4. Prepare a Prompt for the AI to Explain the Testing Strategy

Before starting any testing tasks, prepare a prompt for your AI assistant. This prompt will help you understand:

- The types of tests you will write
- Why each test type is important
- How these test layers differ
- What failures each layer is designed to detect

The goal is to understand why you re doing what you re doing, not just doing it. 


## 5. Integration Test Exercises

All tests in this section belong under:

```
tests/integration/
```

### Task 5.1 — Test GET /items

Create the file:

```
tests/integration/test_items.py
```

Implement a test that:

- Sends `GET /items`
- Asserts status code is 200
- Asserts the response is a list
- Confirms the list contains the two seeded items ("apple" and "banana")

Run:

```bash
pytest tests/integration/test_items.py -k get_items
```

### Task 5.2 — Test GET /items/{id}

Add two tests:

**Test 1:** `GET /items/1`
- Assert 200
- Assert the returned JSON contains `id`, `name`, `price`

**Test 2:** `GET /items/99999`
- Assert 404

Run:

```bash
pytest tests/integration/test_items.py -k item
```

### Task 5.3 — Test POST /items

POST a new item such as:

```json
{"name": "orange", "price": 3.1}
```

Assert:
- Status 201
- Response includes `id`, `name`, `price`
- Fetch `/items` again and ensure the item was added.

### Task 5.4 — Test GET /total

Call `GET /total`

Assert that the returned JSON contains the following keys:
- `total`
- `count`
- `processed_at`
- `version`

Assert:
- `count` matches the number of rows in the database
- `total` is greater than zero

Run:

```bash
pytest tests/integration/test_total.py
```

## 6. Contract Test Exercises (Pact)

Directory:

```
tests/contract/
```

Create the file:

```
tests/contract/test_sum_contract.py
```

Your tasks:

- Set up a Pact mock provider listening on port 1234
- Define the expected request:

```json
{"numbers": [1.5, 2.0]}
```

- Define the expected response:

```json
{
  "total": 3.5,
  "count": 2,
  "processed_at": "<ISO timestamp>",
  "version": "1.0"
}
```

- Implement the Pact interactions:
  - `.given(...)`
  - `.upon_receiving(...)`
  - `.with_request(...)`
  - `.will_respond_with(...)`

- Send a POST request to the mock server
- Assert that the response matches the expected fields

Run:

```bash
pytest tests/contract/test_sum_contract.py
```

A pact file should be generated.

## 7. Component Testing with Testcontainers

Directory:

```
tests/component/
```

Create the file:

```
tests/component/test_service_a_component.py
```

Your tasks:

- Start a Postgres test container using Testcontainers
- Connect to it and create the items table
- Insert two test rows
- Start Service A as a subprocess, pointing it to the Testcontainers DB
- Call `GET /items` on the test instance
- Assert that the returned items match what you inserted

Run:

```bash
pytest tests/component/test_service_a_component.py
```

## 8. Run All Tests

To run the entire test suite:

```bash
poetry run pytest
```

All integration, contract, and component tests should pass.

## 9. CI Integration (GitHub Actions)

The CI workflow contains placeholders.

Update these lines:

```bash
pytest tests/integration
pytest tests/contract
pytest tests/component
```

Push to GitHub. CI should run all tests.

## 10. AI-Assisted Feature Development - TDD 

After completing all workshop testing tasks, use your AI assistant to implement a new feature based on your existing test suite.

**Option A — Delete Item Endpoint**

Add support for:

```
DELETE /items/{id}
```

Test expectations:
- Deleting an existing item removes it
- Deleting a missing item returns 404
- `/total` recalculates correctly afterward

**Option B — Average Price Endpoint**

Add:

```
GET /average
```

Expected behavior:
- Returns the average price
- Handles empty tables properly
- Fits cleanly into existing component tests

**Option C — Input Validation Improvements in Service B**

Modify `/sum` to:
- Reject negative numbers
- Reject missing fields
- Reject non-numeric items

This requires updating Pact contracts and integration tests.

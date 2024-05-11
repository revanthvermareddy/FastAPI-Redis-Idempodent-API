# fastapi-stripe-checkout-api

This is a sample stripe checkout implementation using FastAPI. It also includes the an idempotent payment API implementation using redis which is useful in building payment systems like Stripe, razorpay, etc.

### Setup

1. Install the dependencies

```bash
poetry install --no-root
```

2. Activate the virtual environment

```bash
poetry shell
# (or)
source ./.venv/bin/activate
```

3. Create a `.env` file using the `.env.template`

```bash
cp ./app/.env.template ./app/.env
```

Replace necessary variables within the `.env` file

4. Run the server

```bash
uvicorn app.main:app --reload --env-file ./app/.env
```

Visit the checkout page at: http://127.0.0.1:8000

### Prerequisites

- python - `v3.10.6`
- redis / elasticcache
- stripe account

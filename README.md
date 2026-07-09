# Metronome Billing App

A minimal FastAPI app for learning Metronome usage-based billing. It provisions a demo "Nova AI Image Generation" product with a billable metric, rate card, and contract, then exposes an endpoint that reports image-generation usage as billing events.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- A [Metronome](https://metronome.com) account with API access
- A Metronome customer to bill against (used as the "demo customer")

## Setup

1. Clone the repo and install dependencies:

   ```bash
   uv sync
   ```

   Or with pip:

   ```bash
   pip install fastapi uvicorn metronome-sdk pydantic-settings python-dotenv
   ```

2. Create a `.env` file in the project root:

   ```
   METRONOME__BEARER_TOKEN=your_metronome_api_key
   METRONOME__DEMO_CUSTOMER_ALIAS=your_demo_customer_ingest_alias
   ```

   Find your API key in the [Metronome Dashboard](https://app.metronome.com) under **Settings > API keys**. The demo customer alias is the ingest alias of an existing Metronome customer to bill usage events against.

3. Provision the demo billing objects (billable metric, product, rate card, rate, and contract):

   ```bash
   uv run python -m provisioning.setup
   ```

   This only needs to be run once per Metronome environment.

## Running

```bash
uv run uvicorn server:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API docs.

## Routes

| Route                                 | Method | Description                                                  |
| -------------------------------------- | ------ | -------------------------------------------------------------- |
| `/api/v1/events/image-generation`      | POST   | Reports an image-generation usage event to Metronome           |

## Testing usage events

Send a sample event with `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/events/image-generation \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_123",
    "tier": "standard",
    "num_images": 3,
    "model": "nova-v1",
    "region": "us-east-1"
  }'
```

`tier` maps to one of the provisioned price tiers (`standard`, `high-res`, `ultra`). `customer_id` defaults to `METRONOME__DEMO_CUSTOMER_ALIAS` if omitted. Check the Metronome Dashboard to confirm the event and resulting usage/invoice.

> **Note:** `transaction_id` must be unique per event. Metronome deduplicates events by this field, so re-sending the same `transaction_id` (e.g. re-running the sample request above) is treated as a duplicate and won't be counted again. Change it on each request when testing.

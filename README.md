# Crypto Tracker

A Python application for cryptocurrency market tracking and analytics using the CoinGecko API.

The project provides:
- a CLI interface for data analysis
- a REST API built with FastAPI
- PostgreSQL persistence for historical snapshots

## Tech Stack

Python • FastAPI • PostgreSQL • pytest • Railway • Git

## Live Demo

API deployed on Railway:

- API Base URL  
  https://web-production-xxxx.up.railway.app

- Swagger Documentation  
  https://web-production-xxxx.up.railway.app/docs

- Coin Analytics Example  
  https://web-production-xxxx.up.railway.app/coins/bitcoin?days=7

- Snapshot History  
  https://web-production-xxxx.up.railway.app/history

## Features

- Fetch real-time cryptocurrency market data from the CoinGecko API
- Display price analytics:
  - Current price
  - High / Low
  - Average price
  - Price variation (%)
- Save historical snapshots into PostgreSQL
- View saved historical snapshots
- REST API with FastAPI
- Automated API tests with pytest
- Error handling for invalid inputs and API failures
- Railway deployment support

## Project Architecture 

```text
.
├── api.py            # FastAPI REST API
├── tracker.py        # CLI logic and data analysis
├── database.py       # PostgreSQL connection and persistence
├── test.py           # API tests
├── requirements.txt  # Dependencies
├── Procfile          # Railway deployment configuration
└── .env.exemple      # Environment variables template
```

## Installation

Clone the repository:
```bash
git clone <repository_url>
cd crypto-tracker
```

Create and activate a virtual environment (optional):

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a '.env' file:

```env
DATABASE_URL=your_postgresql_connection_url
```

## CLI Usage

### Analyze cryptocurrency

```bash
python tracker.py --coin bitcoin --days 7
```

### Save a snapshot

```bash
python tracker.py --coin bitcoin --days 7 --save 
```
Data is saved in PostgreSQL

### View snapshot history

```bash
python tracker.py --history
```
Note: this option ignores --coin and --days

## API Usage

Start the API locally:

```bash
uvicorn api:app --reload
```

API available at:

```text
http://127.0.0.1:8000
```

### Get coin analytics

Open in your browser:

```text
http://127.0.0.1:8000/coins/bitcoin?days=7
```

Example response:

```json
{
  "current_price": 81300.16,
  "high": 82145.66,
  "low": 78827.55,
  "change_pct": 0.69,
  "avg_price": 80736.18,
  "coin": "bitcoin",
  "days": 7
}
```

### Get snapshot history

Open in your browser:

```text
http://127.0.0.1:8000/history
```

## Testing

Run tests with pytest:

```bash
pytest
```

Current tests:
- valid coin request
- invalid coin handling
- invalid day parameter handling

## Deployment

Deployment-ready configuration for Railway using:
- FastAPI
- Uvicorn
- PostgreSQL

Example Procfile:

```text
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

## Error Handling

Handled scenarios include:
- invalid coin IDs
- invalid day parameters
- network request failures
- API response errors
- FastAPI HTTP exceptions

## Coin IDs Notes

Coin names must use the official CoinGecko coin ID format.

Valid examples:
- bitcoin
- ethereum
- solana
- dogecoin

Invalid examples:
- BTC
- Bitcoin
- Eth
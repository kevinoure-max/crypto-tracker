# Crypto Tracker

A command-line Python tool that fetches and analyzes cryptocurrency market data from the CoinGecko API and displays a summary of price activity over a selected number of days.

It also allows saving snapshots locally and viewing historical analyses using SQLite. 

## Features

- Fetch real-time cryptocurrency market data from the CoinGecko API
- Display price analytics:
  - Current price
  - High / Low
  - Average price
  - Price variation (%)
- Save snapshots to a local SQLite database
- View saved historical snapshots
- Filter results using command-line arguments
- Handle common errors (invalid coin, invalid days, network/API issues)

## Requirements

- Python 3.8+
- requests
SQLite is included with Python (no installation required)

## Installation

Clone the repository and install dependencies:
```bash
pip install requests
```

Run the project
```bash
python tracker.py 
```

## Usage

### Basic command

```bash
python tracker.py --coin bitcoin --days 7
```

### Save a snapshot

Use the --save flag to store the analysis in a local SQLite database:
```bash
python tracker.py --coin bitcoin --days 7 --save 
```
Data is saved in tracker.db

### View history

Display all saved snapshots
```bash
python tracker.py --history
```
Note: this option ignores --coin and --days

## Example Output

```text
=== Bitcoin - 7 days summary ===

Current price  : 81300.16 USD
7-day high     : 82145.66 USD
7-day low      : 78827.55 USD
7-day change   :     0.69 %
Average price  : 80736.18 USD
```

## Error handling 

Examples of handled errors:

```text
Error: network request failed - ...
Error: coin 'xxx' not found. Check the name (e.g. 'bitcoin')
Error: 0 is not valid. --days must be greater than 0.
Error: --coin and --days are required unless using --history
```

## Notes

Coin names must use the official CoinGecko coin ID format.

Valid examples:
- bitcoin
- ethereum
- solana
- dogecoin

Invalid examples:
- Bitcoin
- BTC
- Eth

## Database

The project uses a local SQLite database (tracker.db) with the table:
```text
snapshots(
    id,
    coin,
    days,
    current_price,
    high,
    low,
    change_pct,
    avg_price,
    created_at
)
```

## Summary

This tool combines:
- API data fetching
- CLI interaction
- data analysis
- local persistence
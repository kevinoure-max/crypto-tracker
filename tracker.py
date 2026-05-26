import requests
import argparse
from database import init_db, save_snapshot, get_snapshots


def get_history(coin, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days={days}"
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error : network request failed - {e}")
        return None

    data = response.json()
    if "prices" not in data:
        print(
            f"Error: coin '{coin}' not found. Check the name (e.g. 'bitcoin', 'ethereum')"
        )
        return None
    return data["prices"]


def compute_summary(prices):
    only_prices = [price for timestamp, price in prices]
    current_price = only_prices[-1]
    max_price = max(only_prices)
    min_price = min(only_prices)
    first_price = only_prices[0]
    price_variation = ((current_price - first_price) / first_price) * 100
    price_average = sum(only_prices) / len(only_prices)
    return {
        "current_price": round(current_price, 2),
        "high": round(max_price, 2),
        "low": round(min_price, 2),
        "change_pct": round(price_variation, 2),
        "avg_price": round(price_average, 2),
    }


def display_summary(summary, coin, days):
    print(f"\n=== {coin.capitalize()} - {days} days summary ===\n")
    print(
        f"{'Current price':<15}: {summary['current_price']:>8.2f} USD\n"
        f"{str(days) + '-day high':<15}: {summary['high']:>8.2f} USD\n"
        f"{str(days) + '-day low':<15}: {summary['low']:>8.2f} USD\n"
        f"{str(days) + '-day change':<15}: {summary['change_pct']:>8.2f} %\n"
        f"{'Average price':<15}: {summary['avg_price']:>8.2f} USD\n"
    )


def display_history(rows):
    print(f"\n=== Snapshot history ===\n")

    for (
        id,
        coin,
        days,
        current_price,
        high,
        low,
        change_pct,
        avg_price,
        created_at,
    ) in rows:
        print(
            f"[{id}] {coin.capitalize()} (days {days})\n"
            f"{'Current price':<15}: {current_price:>8.2f} USD\n"
            f"{'High':<15}: {high:>8.2f} USD\n"
            f"{'Low':<15}: {low:>8.2f} USD\n"
            f"{'Change (%)':<15}: {change_pct:>8.2f} %\n"
            f"{'Average price':<15}: {avg_price:>8.2f} USD\n"
            f"{'Created_at':<15}: {created_at:>8}\n"
        )


def script_parser():
    parser = argparse.ArgumentParser(description="Analyze a coin performance")
    parser.add_argument("--coin", type=str, required=False, help="Filter by coin type")
    parser.add_argument("--days", type=int, required=False, help="Period perimeter")
    parser.add_argument("--save", action="store_true", help="Save snapshot to database")
    parser.add_argument("--history", action="store_true", help="Show snapshot history")
    args = parser.parse_args()
    return (args.coin, args.days, args.save, args.history)


def main():
    init_db()
    coin, days, save, history = script_parser()

    if history:
        rows = get_snapshots()
        display_history(rows)
        return

    if not coin or not days:
        print(f"Error : --coin and --days are required unless using --history")
        return

    if days <= 0:
        print(f"Error : {days} is not valid. --days must be greater than 0.")
        return

    prices = get_history(coin, days)

    if prices is None:
        return

    summary = compute_summary(prices)
    display_summary(summary, coin, days)

    if save:
        save_snapshot(
            coin,
            days,
            summary["current_price"],
            summary["high"],
            summary["low"],
            summary["change_pct"],
            summary["avg_price"],
        )


if __name__ == "__main__":
    main()

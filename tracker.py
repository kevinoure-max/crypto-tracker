import requests
import argparse
from datetime import datetime
from database import init_db, save_snapshot


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
        "current_price": current_price,
        "high": max_price,
        "low": min_price,
        "change_pct": price_variation,
        "avg_price": price_average,
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


def script_parser():
    parser = argparse.ArgumentParser(description="Analyze a coin performance")
    parser.add_argument("--coin", type=str, required=True, help="Filter by coin type")
    parser.add_argument("--days", type=int, required=True, help="Period perimeter")
    parser.add_argument("--save", action="store_true", help="Save snapshot to database")
    args = parser.parse_args()
    return (args.coin, args.days, args.save)


def main():
    init_db()
    coin_type, days, save = script_parser()

    if days <= 0:
        print(f"Error : {days} is not valid. --days must be greater than 0.")
        return

    prices = get_history(coin_type, days)

    if prices is None:
        return

    summary = compute_summary(prices)
    display_summary(summary, coin_type, days)

    if save:
        save_snapshot(
            coin_type,
            days,
            summary["current_price"],
            summary["high"],
            summary["low"],
            summary["change_pct"],
            summary["avg_price"],
        )


if __name__ == "__main__":
    main()

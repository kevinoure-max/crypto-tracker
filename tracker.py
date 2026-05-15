import requests
from datetime import datetime
import argparse


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


def summarize_prices(prices, coin, days):
    only_prices = [price for timestamp, price in prices]
    current_price = only_prices[-1]
    max_price = max(only_prices)
    min_price = min(only_prices)
    first_price = only_prices[0]
    price_variation = ((current_price - first_price) / first_price) * 100
    price_average = sum(only_prices) / len(only_prices)
    print(f"\n=== {coin.capitalize()} - {days} days summary ===\n")
    print(
        f"{'Current price':<15}: {current_price:>8.2f} USD\n"
        f"{'7-day high':<15}: {max_price:>8.2f} USD\n"
        f"{'7-day low':<15}: {min_price:>8.2f} USD\n"
        f"{'7-day change':<15}: {price_variation:>8.2f} %\n"
        f"{'Average price':<15}: {price_average:>8.2f} USD\n"
    )


def script_parser():
    parser = argparse.ArgumentParser(description="Analyze a coin performance")
    parser.add_argument("--coin", type=str, required=True, help="Filter by coin type")
    parser.add_argument("--days", type=int, required=True, help="Period perimeter")
    args = parser.parse_args()
    return (args.coin, args.days)


def main():
    coin_type, days = script_parser()

    if days <= 0:
        print(f"Error : {days} is not valid. --days must be greater than 0.")
        return

    prices = get_history(coin_type, days)

    if prices is None:
        return

    summarize_prices(prices, coin_type, days)


if __name__ == "__main__":
    main()

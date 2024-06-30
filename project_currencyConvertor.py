from requests import get
from pprint import PrettyPrinter

API_KEY = "fca_live_KnsmTqj7BffjodnvXr7JCMA4bqCiGHTUPAe2PXVt"
BASE_URL = "https://api.freecurrencyapi.com/v1/"

printer = PrettyPrinter()

def get_currencies():
    endpoint = f"currencies?apikey={API_KEY}"
    url = BASE_URL + endpoint
    response = get(url)
    if response.status_code != 200:
        print("Failed to fetch currencies.")
        return []
    data = response.json()['data']
    data = list(data.items())
    data.sort()

    return data

def print_currencies(currencies):
    for _id, currency in currencies:
        name = currency['name']
        symbol = currency.get("symbol", "")
        print(f"{_id} - {name} - {symbol}")

def exchange_rate(currency1, currency2):
    endpoint = f"latest?apikey={API_KEY}&base_currency={currency1}&currencies={currency2}"
    url = BASE_URL + endpoint
    response = get(url)
    if response.status_code != 200:
        print("Failed to fetch exchange rate.")
        return

    data = response.json()
    if currency2 not in data['data']:
        print('Invalid currencies.')
        return

    rate = data['data'][currency2]
    print(f"{currency1} -> {currency2} = {rate}")

    return rate

def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return

    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount.")
        return

    converted_amount = rate * amount
    print(f"{amount} {currency1} is equal to {converted_amount} {currency2}")
    return converted_amount

def main():
    currencies = get_currencies()

    print("Welcome to the currency converter!")
    print("List - lists the different currencies")
    print("Convert - convert from one currency to another")
    print("Rate - get the exchange rate of two currencies")
    print()

    while True:
        command = input("Enter a command (q to quit): ").lower()

        if command == "q":
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "convert":
            currency1 = input("Enter a base currency: ").upper()
            amount = input(f"Enter an amount in {currency1}: ")
            currency2 = input("Enter a currency to convert to: ").upper()
            convert(currency1, currency2, amount)
        elif command == "rate":
            currency1 = input("Enter a base currency: ").upper()
            currency2 = input("Enter a currency to convert to: ").upper()
            exchange_rate(currency1, currency2)
        else:
            print("Unrecognized command!")

main()

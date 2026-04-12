import requests

def card_lookup(card_name):
    url = "https://api.scryfall.com/cards/named?fuzzy="
    url += card_name
    response = requests.get(url)
    card = response.json()
    return response, card

def main():
    while True:
        card_choice = input("\nEnter card name (Q to quit): ").lower()
        if card_choice == "q":
            break

        response, card = card_lookup(card_choice)

        # successful lookup
        if response.status_code == 200:
            print(f"\n{card['name']}\nMana cost: {card['mana_cost']}")

            # check for multi-faced cards like Gleemax
            if 'oracle_text' in card:
                print(f"{card['oracle_text']}")
            else:
                for index in range(len(card['card_faces'])):
                  print(f"Side {index+1}: {card['card_faces'][index]['oracle_text']}")
            print(f"{card['type_line']}"
                  f"\n{card['set_name']}")

            # checks if creature
            if 'power' in card and 'toughness' in card:
                print(f"Power/Toughness: {card['power']}/{card['toughness']}")

        elif response.status_code == 404:
            print(f'Invalid card name: "{card_choice}"')

        else:
            print(f"Failed with status code: {response.status_code}")

if __name__ == '__main__':
    main()
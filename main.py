import requests


def card_lookup(card_name: str) -> tuple:
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
            if "oracle_text" in card:
                print(f"{card['oracle_text']}")
            else:
                for index in range(len(card["card_faces"])):
                    print(f"Side {index+1}: {card['card_faces'][index]['oracle_text']}")
            print(f"{card['type_line']}" f"\n{card['set_name']}")

            # checks if creature
            if "power" in card and "toughness" in card:
                print(f"Power/Toughness: {card['power']}/{card['toughness']}")

        elif response.status_code == 404:
            print(f'Invalid card name: "{card_choice}"')

        else:
            print(f"Failed with status code: {response.status_code}")


if __name__ == "__main__":
    main()


"""A few directions worth considering, roughly ordered by how much they'd add to the portfolio signal:

Deck list manager (highest value)
Add the ability to build, save, and load a deck — store card names and quantities to a JSON or CSV file. 
This reuses your file I/O muscle from the flashcard project but in a domain-specific context, and it's something a real MTG player would actually use. 
A Deck class with methods like add_card, remove_card, show_deck, and total_mana_curve would demonstrate OOP in a natural way rather than a contrived one.

Card class + richer data
Right now card is just a raw dict you're pulling keys off. 
Wrapping it in a Card class with properties would clean the code significantly and show you understand encapsulation. 
Scryfall also returns price data in the prices field — a card's current market value is exactly the kind of thing a collector wants at a glance.

Caching layer
Right now every lookup hits the API cold. 
A simple dict-based cache (or even writing to a local JSON file) that checks 
if you've already fetched a card before making the request would demonstrate awareness of API etiquette and efficiency. 
Scryfall's docs actually ask developers to avoid repeat requests for the same data.

argparse or click CLI
The input() loop works but screams tutorial. 
Accepting a card name as a command-line argument — python mtg.py "Black Lotus" — 
is how real tools work and gives you a chance to handle optional flags like --price-only or --set.

Advanced search endpoint
Scryfall has a /cards/search endpoint that accepts their full query syntax (e.g., cmc=3 type:creature color:blue). 
Supporting that would let the tool pull a list of results, which means handling pagination and iteration — 
a meaningfully harder problem than single-card lookup.

rich library for output
Low effort, high visual payoff. 
A formatted table or colored card display makes screenshots actually look like something in a README.

ScryfallClient cache class
- 50-100ms delay between requests
- Cache repeated lookups — they specifically call this out. 
- If someone looks up "Lightning Bolt" twice in a session, hitting the API again is wasteful. 
- User-Agent header — they ask that apps identify themselves. Easy to add:
```
pythonheaders = {"User-Agent": "MTGLookupTool/1.0 (your@email.com)"}
response = requests.get(url, headers=headers)
```
"""
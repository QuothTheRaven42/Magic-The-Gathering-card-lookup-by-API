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

            # check for multi-faced cards like Who//What//When//Where//Why
            if "oracle_text" in card:
                print(f"{card['oracle_text']}")
            else:
                for index in range(len(card["card_faces"])):
                    print(f"Side {index+1}: {card['card_faces'][index]['oracle_text']}")
            print(f"{card['rarity'].capitalize()} {card['type_line']}")

            # checks if creature
            if "power" in card and "toughness" in card:
                print(f"Power/Toughness: {card['power']}/{card['toughness']}")

            print(f"Card art: {card['image_uris']['art_crop']} by {card['artist']}")

        elif response.status_code == 404:
            print(f'Invalid card name: "{card_choice}"')
        else:
            print(f"Failed with status code: {response.status_code}")


if __name__ == "__main__":
    main()


"""
Under Development:

- User-Agent header
Scryfall's docs specifically ask that tools identify themselves with a header 
Example: {"User-Agent": "MTGLookupTool/1.0 (email)"}. 

-Card class
Currently pulling keys off a raw dictionary. 
Wrapping the response in a Card class with proper attributes — 
name, mana cost, type line, rarity, oracle text, prices — 
cleans the code significantly and demonstrates encapsulation.

- rich library for output
Formatted tables and colored output make the README screenshots look like a real tool.
Easy to layer on once the Card class exists.

- argparse CLI
Replacing the input() loop with command-line arguments — python mtg.py "Black Lotus." 
Optional flags like --price-only or --set give natural control flow to write.

Error handling and retry logic
Handle non-200 responses explicitly — 404 should surface Scryfall's own error message to the user. 
Transient failures like timeouts and 429 rate limit responses should trigger a retry with a short delay between attempts. 
Cap retries at a reasonable maximum before failing gracefully. 
This logic belongs centralized in the API client so nothing else has to think about it.

- JSON cache
Check a local file before hitting the API. 
If the card is already there, return it. If not, fetch it, store it, return it. 
Scryfall's docs explicitly ask developers to avoid repeat requests for the same data.

- Deck class
A Deck with add_card, remove_card, show_deck, and save/load to JSON or CSV.
Reuses the file I/O and Card class, which shows the pieces of the project working together.

- SQLite cache
Once the JSON cache works, swapping the storage layer for SQLite.

- Advanced search + pagination
Scryfall's /cards/search endpoint accepts their full query syntax — cmc=3 type:creature color:blue — 
Returns a paginated list of results. 

Later:
- Streamlit / Pydantic
Pydantic would replace or enhance the Card class with automatic type validation on incoming data. 
Streamlit would give a basic web UI with minimal effort.
"""
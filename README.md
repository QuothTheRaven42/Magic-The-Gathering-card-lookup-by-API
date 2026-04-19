# MTG Card Lookup

A command-line tool for looking up Magic: The Gathering cards using the [Scryfall API](https://scryfall.com/docs/api). Enter a card name and get back its mana cost, oracle text, type, set, and power/toughness if applicable.

## Features

- Fuzzy name matching — close enough usually works
- Displays mana cost, oracle text, type line, and set name
- Handles double-faced and multi-faced cards
- Power/toughness displayed for creature cards
- Loop stays open for multiple lookups in one session

## Requirements

- Python 3.10+
- [requests](https://pypi.org/project/requests/)

Install the dependency with:

```
pip install requests
```

## Usage

```
python main.py
```

You'll be prompted to enter a card name. Type `Q` to quit.

```
Enter card name (Q to quit): who what when where why

Who // What // When // Where // Why
Mana cost: {X}{W} // {2}{R} // {2}{U} // {3}{B} // {1}{G}
Side 1: Target player gains X life.
Side 2: Destroy target artifact.
Side 3: Counter target creature spell.
Side 4: Destroy target land.
Side 5: Destroy target enchantment.
Instant
Unsanctioned
```

## Notes

- Uses Scryfall's `fuzzy` search parameter, so partial or slightly misspelled names will often still resolve
- Double-faced cards (like split cards or transform cards) display oracle text for each face separately
- No API key required — Scryfall's API is free and open

## Under Development

- User-Agent header:
Scryfall's docs specifically ask that tools identify themselves with a header 
Example: {"User-Agent": "MTGLookupTool/1.0 (email)"}. 

- Card class:
Currently pulling keys off a raw dictionary. 
Wrapping the response in a Card class with proper attributes — 
name, mana cost, type line, rarity, oracle text, prices — 
cleans the code significantly and demonstrates encapsulation.

- rich library for output:
Formatted tables and colored output make the README screenshots look like a real tool.
Easy to layer on once the Card class exists.

- argparse CLI:
Replacing the input() loop with command-line arguments — python mtg.py "Black Lotus." 
Optional flags like --price-only or --set give natural control flow to write.

- Error handling and retry logic:
Handle non-200 responses explicitly — 404 should surface Scryfall's own error message to the user. 
Transient failures like timeouts and 429 rate limit responses should trigger a retry with a short delay between attempts. 
Cap retries at a reasonable maximum before failing gracefully. 
This logic belongs centralized in the API client so nothing else has to think about it.

- JSON cache:
Check a local file before hitting the API. 
If the card is already there, return it. If not, fetch it, store it, return it. 
Scryfall's docs explicitly ask developers to avoid repeat requests for the same data.

- Deck class:
A Deck with add_card, remove_card, show_deck, and save/load to JSON or CSV.
Reuses the file I/O and Card class, which shows the pieces of the project working together.

- SQLite cache:
Once the JSON cache works, swapping the storage layer for SQLite.

- Advanced search + pagination:
Scryfall's /cards/search endpoint accepts their full query syntax — cmc=3 type:creature color:blue — 
Returns a paginated list of results. 

Later:
- Streamlit / Pydantic:
Pydantic would replace or enhance the Card class with automatic type validation on incoming data. 
Streamlit would give a basic web UI with minimal effort.

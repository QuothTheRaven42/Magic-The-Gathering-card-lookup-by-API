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

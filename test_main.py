import pytest
from unittest.mock import patch, MagicMock
from main import card_lookup, main


# --- Fixtures ---

def make_response(status_code: int, json_data: dict) -> MagicMock:
    """Helper to build a mock requests.Response."""
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_data
    return mock_response


SINGLE_FACE_CREATURE = {
    "name": "Grizzly Bears",
    "mana_cost": "{1}{G}",
    "oracle_text": "No ability here.",
    "type_line": "Creature — Bear",
    "set_name": "Alpha",
    "power": "2",
    "toughness": "2",
}

SINGLE_FACE_NONCREATURE = {
    "name": "Lightning Bolt",
    "mana_cost": "{R}",
    "oracle_text": "Lightning Bolt deals 3 damage to any target.",
    "type_line": "Instant",
    "set_name": "Alpha",
}

MULTI_FACE_CARD = {
    "name": "Delver of Secrets // Insectile Aberration",
    "mana_cost": "{U}",
    "type_line": "Creature — Human Wizard // Creature — Human Insect",
    "set_name": "Innistrad",
    "card_faces": [
        {"oracle_text": "At the beginning of your upkeep, look at the top card..."},
        {"oracle_text": "Flying"},
    ],
}

NOT_FOUND = {
    "object": "error",
    "code": "not_found",
    "details": "No cards found matching that name.",
}


# --- card_lookup() ---

def test_card_lookup_returns_tuple():
    mock_resp = make_response(200, SINGLE_FACE_CREATURE)
    with patch("main.requests.get", return_value=mock_resp):
        response, card = card_lookup("grizzly bears")
        assert isinstance(response, MagicMock)
        assert isinstance(card, dict)


def test_card_lookup_passes_name_in_url():
    mock_resp = make_response(200, SINGLE_FACE_CREATURE)
    with patch("main.requests.get", return_value=mock_resp) as mock_get:
        card_lookup("lightning bolt")
        called_url = mock_get.call_args[0][0]
        assert "lightning bolt" in called_url


# --- main() output: single-faced creature ---

def test_single_face_creature_output(capsys):
    mock_resp = make_response(200, SINGLE_FACE_CREATURE)
    with patch("main.card_lookup", return_value=(mock_resp, SINGLE_FACE_CREATURE)):
        with patch("builtins.input", side_effect=["grizzly bears", "q"]):
            main()
    output = capsys.readouterr().out
    assert "Grizzly Bears" in output
    assert "{1}{G}" in output
    assert "Power/Toughness: 2/2" in output
    assert "Alpha" in output


# --- main() output: single-faced non-creature ---

def test_single_face_noncreature_no_pt(capsys):
    mock_resp = make_response(200, SINGLE_FACE_NONCREATURE)
    with patch("main.card_lookup", return_value=(mock_resp, SINGLE_FACE_NONCREATURE)):
        with patch("builtins.input", side_effect=["lightning bolt", "q"]):
            main()
    output = capsys.readouterr().out
    assert "Lightning Bolt" in output
    assert "Power/Toughness" not in output


# --- main() output: multi-faced card ---

def test_multi_face_card_shows_sides(capsys):
    mock_resp = make_response(200, MULTI_FACE_CARD)
    with patch("main.card_lookup", return_value=(mock_resp, MULTI_FACE_CARD)):
        with patch("builtins.input", side_effect=["delver of secrets", "q"]):
            main()
    output = capsys.readouterr().out
    assert "Side 1" in output
    assert "Side 2" in output


# --- main() output: 404 ---

def test_404_prints_invalid_message(capsys):
    mock_resp = make_response(404, NOT_FOUND)
    with patch("main.card_lookup", return_value=(mock_resp, NOT_FOUND)):
        with patch("builtins.input", side_effect=["asdfghjkl", "q"]):
            main()
    output = capsys.readouterr().out
    assert "Invalid card name" in output


# --- main() output: unexpected status code ---

def test_unexpected_status_code(capsys):
    mock_resp = make_response(500, {})
    with patch("main.card_lookup", return_value=(mock_resp, {})):
        with patch("builtins.input", side_effect=["lightning bolt", "q"]):
            main()
    output = capsys.readouterr().out
    assert "500" in output


# --- quit behavior ---

def test_quit_on_q(capsys):
    with patch("builtins.input", return_value="q"):
        main()
    output = capsys.readouterr().out
    assert output.strip() == "" or "Enter card name" not in output
from backend.core.game_engine import MasterMindGame


def test_evaluate_guess():
    game = MasterMindGame()
    game.secret = "1234"

    exact, wrong = game.evaluate_guess("1234")
    assert exact == 4 and wrong == 0, "All digits should match exactly"

    exact, wrong = game.evaluate_guess("1256")
    assert exact == 2 and wrong == 0, "First two should match exactly"

    exact, wrong = game.evaluate_guess("5678")
    assert exact == 0 and wrong == 0, "No matches"

    exact, wrong = game.evaluate_guess("4321")
    assert exact == 0 and wrong == 4, "All in wrong positions"


def test_duplicates():
    game = MasterMindGame()
    game.secret = "1122"

    exact, wrong = game.evaluate_guess("1111")
    assert exact == 2, "First two 1s should match exactly"

    exact, wrong = game.evaluate_guess("2211")
    assert exact == 0 and wrong == 4, "All correct digits, wrong positions"


def test_validation():
    game = MasterMindGame()

    assert game.validate_guess("1234"), "4 digits should be valid"
    assert game.validate_guess("0000"), "All zeros should be valid"
    assert not game.validate_guess("123"), "Too short"
    assert not game.validate_guess("12345"), "Too long"
    assert not game.validate_guess("12a4"), "Letters not allowed"
    assert not game.validate_guess(""), "Empty string invalid"

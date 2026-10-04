from api.pii import mask_email, mask_phone, pseudonymize


def test_mask_email() -> None:
    assert mask_email("alice@example.com") == "al***@example.com"


def test_mask_phone() -> None:
    assert mask_phone("+39 333 123 4567") == "********4567"


def test_pseudonymize_is_deterministic() -> None:
    assert pseudonymize("alice@example.com") == pseudonymize("alice@example.com")
    assert pseudonymize("alice@example.com") != pseudonymize("bob@example.com")

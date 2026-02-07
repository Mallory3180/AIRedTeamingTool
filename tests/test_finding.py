from src.core.finding import should_promote_finding


def test_should_promote_finding():
    assert should_promote_finding(["mutation-a", "mutation-b"]) is True
    assert should_promote_finding(["mutation-a", "mutation-a"]) is False

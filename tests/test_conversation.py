from src.core.conversation import format_conversation_history


def test_format_conversation_history():
    messages = [("user", "hi"), ("assistant", "hello")]
    assert format_conversation_history(messages) == "user: hi\nassistant: hello"

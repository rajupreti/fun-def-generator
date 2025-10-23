import pytest
from main import run_prompt, RESPONSE_STYLES, spin_wheel

def test_response_styles_not_empty():
    assert len(RESPONSE_STYLES) > 0

def test_spin_wheel_returns_valid_style():
    style = spin_wheel()
    assert style in RESPONSE_STYLES

def test_run_prompt_validates_api_key():
    with pytest.raises(ValueError, match="MISTRAL_API_KEY.*not set"):
        run_prompt(api_key="", model="test-model", prompt="test")
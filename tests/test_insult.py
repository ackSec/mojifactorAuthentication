from unittest.mock import patch, MagicMock
from common.insult import get_insult


@patch('common.insult.urlopen')
def test_get_insult_returns_response(mock_urlopen):
    mock_response = MagicMock()
    mock_response.read.return_value = b'You are not worthy'
    mock_urlopen.return_value = mock_response

    result = get_insult()
    assert result == 'You are not worthy'


@patch('common.insult.urlopen')
def test_get_insult_handles_error(mock_urlopen):
    mock_urlopen.side_effect = Exception("Network error")

    result = get_insult()
    assert "An error occurred" in result
    assert "Network error" in result

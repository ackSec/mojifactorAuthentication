import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from modules.frameCapture import runner, display_countdown


@patch('modules.frameCapture.detect_emotion')
@patch('modules.frameCapture.cv2')
def test_runner_returns_detected_emotion(mock_cv2, mock_detect):
    mock_cap = MagicMock()
    mock_cv2.VideoCapture.return_value = mock_cap
    mock_cap.isOpened.return_value = True
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    mock_cap.read.return_value = (True, frame)
    mock_cv2.imencode.return_value = (True, MagicMock(tobytes=lambda: b'encoded'))
    mock_detect.return_value = 'HAPPY'

    result = runner()

    assert result == 'HAPPY'
    mock_cap.release.assert_called_once()


@patch('modules.frameCapture.detect_emotion')
@patch('modules.frameCapture.cv2')
def test_runner_returns_none_when_no_emotion(mock_cv2, mock_detect):
    mock_cap = MagicMock()
    mock_cv2.VideoCapture.return_value = mock_cap
    mock_cap.isOpened.return_value = True
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    mock_cap.read.return_value = (True, frame)
    mock_cv2.imencode.return_value = (True, MagicMock(tobytes=lambda: b'encoded'))
    mock_detect.return_value = None

    result = runner()
    assert result is None


@patch('modules.frameCapture.cv2')
def test_runner_raises_on_camera_failure(mock_cv2):
    mock_cap = MagicMock()
    mock_cv2.VideoCapture.return_value = mock_cap
    mock_cap.isOpened.return_value = False

    with pytest.raises(RuntimeError, match="Unable to open camera"):
        runner()


@patch('modules.frameCapture.detect_emotion')
@patch('modules.frameCapture.cv2')
def test_runner_raises_on_frame_read_failure(mock_cv2, mock_detect):
    mock_cap = MagicMock()
    mock_cv2.VideoCapture.return_value = mock_cap
    mock_cap.isOpened.return_value = True
    mock_cap.read.return_value = (False, None)

    with pytest.raises(RuntimeError, match="Failed to capture frame"):
        runner()


@patch('modules.frameCapture.time')
def test_display_countdown(mock_time):
    display_countdown(3)
    assert mock_time.sleep.call_count == 3

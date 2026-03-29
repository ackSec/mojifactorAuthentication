from unittest.mock import patch, MagicMock
from common.detectEmotions import detect_emotion


@patch('common.detectEmotions.boto3')
def test_detect_emotion_returns_highest_confidence(mock_boto3):
    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client
    mock_client.detect_faces.return_value = {
        'FaceDetails': [{
            'Emotions': [
                {'Type': 'HAPPY', 'Confidence': 95.0},
                {'Type': 'SAD', 'Confidence': 3.0},
                {'Type': 'ANGRY', 'Confidence': 2.0},
            ]
        }]
    }

    result = detect_emotion(b'fake_image_bytes')
    assert result == 'HAPPY'


@patch('common.detectEmotions.boto3')
def test_detect_emotion_returns_none_when_no_faces(mock_boto3):
    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client
    mock_client.detect_faces.return_value = {'FaceDetails': []}

    result = detect_emotion(b'fake_image_bytes')
    assert result is None


@patch('common.detectEmotions.boto3')
def test_detect_emotion_calls_rekognition_with_correct_params(mock_boto3):
    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client
    mock_client.detect_faces.return_value = {
        'FaceDetails': [{
            'Emotions': [{'Type': 'CALM', 'Confidence': 80.0}]
        }]
    }

    detect_emotion(b'test_bytes')

    mock_client.detect_faces.assert_called_once_with(
        Image={'Bytes': b'test_bytes'},
        Attributes=['ALL']
    )

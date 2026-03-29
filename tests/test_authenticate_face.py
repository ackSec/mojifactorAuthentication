import pytest
from unittest.mock import patch, MagicMock
import numpy as np
import authenticateFace as af


@patch('authenticateFace.boto3')
def test_download_images_from_s3(mock_boto3):
    mock_s3 = MagicMock()
    mock_boto3.client.return_value = mock_s3
    mock_s3.list_objects.return_value = {
        'Contents': [
            {'Key': 'faces/Alice.jpg'},
            {'Key': 'faces/readme.txt'},  # non-jpg, should be skipped
        ]
    }
    # Mock download_fileobj to write fake bytes
    def fake_download(bucket, key, f):
        f.write(b'fake_image_data')
    mock_s3.download_fileobj.side_effect = fake_download

    images = af.download_images_from_s3()

    assert len(images) == 1
    assert images[0][0] == 'Alice.jpg'
    assert images[0][1] == b'fake_image_data'


@patch('authenticateFace.boto3')
def test_download_images_from_s3_empty_bucket(mock_boto3):
    mock_s3 = MagicMock()
    mock_boto3.client.return_value = mock_s3
    mock_s3.list_objects.return_value = {}

    images = af.download_images_from_s3()
    assert images == []


@patch('authenticateFace.boto3')
def test_compare_frame_to_images_match(mock_boto3):
    mock_rek = MagicMock()
    mock_boto3.client.return_value = mock_rek
    mock_rek.compare_faces.return_value = {
        'FaceMatches': [{'Similarity': 99.0}]
    }

    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    images = [('Alice.jpg', b'fake_bytes')]

    result = af.compare_frame_to_images(frame, images)
    assert result == 'Alice'


@patch('authenticateFace.boto3')
def test_compare_frame_to_images_no_match(mock_boto3):
    mock_rek = MagicMock()
    mock_boto3.client.return_value = mock_rek
    mock_rek.compare_faces.return_value = {'FaceMatches': []}

    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    images = [('Alice.jpg', b'fake_bytes')]

    result = af.compare_frame_to_images(frame, images)
    assert result is None


@patch('authenticateFace.cv2')
@patch('authenticateFace.download_images_from_s3')
def test_runner_raises_on_camera_failure(mock_download, mock_cv2):
    mock_download.return_value = []
    mock_cap = MagicMock()
    mock_cv2.VideoCapture.return_value = mock_cap
    mock_cap.isOpened.return_value = False

    with pytest.raises(RuntimeError, match="Unable to open camera"):
        af.runner()


@patch('authenticateFace.compare_frame_to_images')
@patch('authenticateFace.cv2')
@patch('authenticateFace.download_images_from_s3')
def test_runner_raises_on_frame_read_failure(mock_download, mock_cv2, mock_compare):
    mock_download.return_value = []
    mock_cap = MagicMock()
    mock_cv2.VideoCapture.return_value = mock_cap
    mock_cap.isOpened.return_value = True
    mock_cap.read.return_value = (False, None)

    with pytest.raises(RuntimeError, match="Failed to capture frame"):
        af.runner()


@patch('authenticateFace.compare_frame_to_images')
@patch('authenticateFace.cv2')
@patch('authenticateFace.download_images_from_s3')
def test_runner_success(mock_download, mock_cv2, mock_compare):
    mock_download.return_value = [('Alice.jpg', b'data')]
    mock_cap = MagicMock()
    mock_cv2.VideoCapture.return_value = mock_cap
    mock_cap.isOpened.return_value = True
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    mock_cap.read.return_value = (True, frame)
    mock_compare.return_value = 'Alice'

    result = af.runner()
    assert result == 'Alice'
    mock_cap.release.assert_called_once()

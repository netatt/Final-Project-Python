import unittest
from unittest.mock import patch, MagicMock
import logging
from google.cloud import storage

# Import the functions from your module (assuming they're in a file named your_module.py)
from upload_files import upload_func, upload_anat

# Set up logging to capture the logs during testing
logging.basicConfig(level=logging.INFO)

class TestUploadFunctions(unittest.TestCase):

    @patch('google.cloud.storage.Client')
    @patch('google.cloud.storage.blob.Blob.download_to_filename')
    def test_upload_func_success(self, mock_download, mock_storage_client):
        # Mock the storage client and blob
        mock_client = MagicMock()
        mock_storage_client.return_value = mock_client
        
        # Create a mock blob
        mock_blob = MagicMock()
        mock_client.blob.return_value = mock_blob
        
        # Define the test inputs
        subject_id = '01'
        task = '1'

        # Call the upload_func function
        upload_func(subject_id, task)

        # Assertions
        niigz_path = f'ds003550/sub-sc{subject_id}/func/sub-sc{subject_id}_task-RepMem{task}_bold.nii.gz'
        tsv_path = f'ds003550/sub-sc{subject_id}/func/sub-sc{subject_id}_task-RepMem{task}_events.tsv'

        # Ensure download_to_filename was called for both files
        mock_blob.download_to_filename.assert_any_call(f'/content/{niigz_path.split("/")[-1]}')
        mock_blob.download_to_filename.assert_any_call(f'/content/{tsv_path.split("/")[-1]}')
        
        # Ensure the client and blob were accessed correctly
        mock_client.blob.assert_any_call(niigz_path)
        mock_client.blob.assert_any_call(tsv_path)

    @patch('google.cloud.storage.Client')
    @patch('google.cloud.storage.blob.Blob.download_to_filename')
    def test_upload_func_failure(self, mock_download, mock_storage_client):
        # Simulate an error during the file download
        mock_download.side_effect = Exception("Download failed")
        
        # Set up the mock storage client
        mock_client = MagicMock()
        mock_storage_client.return_value = mock_client
        
        # Create a mock blob
        mock_blob = MagicMock()
        mock_client.blob.return_value = mock_blob
        
        subject_id = '01'
        task = '1'

        # Call the upload_func function and expect it to handle the failure
        upload_func(subject_id, task)

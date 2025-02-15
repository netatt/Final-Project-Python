import os
import pytest
import nibabel as nib
import numpy as np
from unittest.mock import patch, MagicMock
from preprocess import preprocess_subject, load_and_plot

# Mock config values (since real paths may not exist during testing)
class MockConfig:
    fmri_base_path = "/mock/path"
    output_dir = "/mock/output"
    FSLDIR = "/mock/fsl"
    FSLOUTPUTTYPE = "NIFTI_GZ"
    gcs_output_path = "gs://mock-bucket"

# Patch config for testing
@patch("preprocessing.config", MockConfig)
def test_preprocess_subject():
    """Test the preprocess_subject function with mock system calls."""
    
    subject_id = 1
    task = "learning"

    # Mock os.system to prevent actual shell execution
    with patch("os.system") as mock_system, patch("os.path.exists", return_value=True):
        preprocess_subject(subject_id, task)

        # Check that os.system was called with expected commands
        mock_system.assert_any_call(f"slicetimer -i /mock/path/sub-sc001_task-RepMemlearning_bold.nii.gz -o /mock/output/sub-sc001_task-learning_slicetime_corrected.nii.gz --odd")
        mock_system.assert_any_call(f"fslmaths /mock/output/sub-sc001_task-learning_slicetime_corrected.nii.gz -Tmean /mock/output/sub-sc001_task-learning_mean_ref.nii.gz")
        mock_system.assert_any_call(f"mcflirt -in /mock/output/sub-sc001_task-learning_slicetime_corrected.nii.gz -out /mock/output/sub-sc001_task-learning_motion_corrected.nii.gz -r /mock/output/sub-sc001_task-learning_mean_ref.nii.gz -rmsrel -rmsabs -plots -scaling 4")

        # Ensure multiple calls to os.system happened
        assert mock_system.call_count > 5  # More than 5 commands should run

@patch("nibabel.load")
def test_load_and_plot(mock_nib_load):
    """Test the load_and_plot function using a mock NIfTI file."""
    
    # Create a mock 3D NIfTI image
    mock_img = MagicMock()
    mock_img.get_fdata.return_value = np.random.rand(64, 64, 30)
    mock_nib_load.return_value = mock_img

    file_path = "/mock/file.nii.gz"
    
    # Call the function (it should not raise an error)
    try:
        load_and_plot(file_path, "Test Plot")
    except Exception as e:
        pytest.fail(f"load_and_plot raised an error: {e}")

    # Ensure nibabel.load was called
    mock_nib_load.assert_called_once_with(file_path)

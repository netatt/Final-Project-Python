import pytest
import numpy as np
import pandas as pd
import nibabel as nib
from unittest.mock import patch, MagicMock
from extract_spatial_patterns import get_fmri_paths, process_fmri_subject

# Sample inputs
def test_get_fmri_paths():
    fmri_base_path = "data/fmri"
    subject_id = "sub-01"
    phase = "learning"
    
    fmri_path, stim_path = get_fmri_paths(fmri_base_path, subject_id, phase)
    
    assert fmri_path == "data/fmri/sub-01_task-RepMem1_bold.nii.gz"
    assert stim_path == "data/fmri/sub-01_task-RepMem1_events.tsv"

def test_process_fmri_subject():
    subject_id = "sub-01"
    phase = "learning"
    fmri_base_path = "data/fmri"
    roi_names = ["amygdala", "hippocampus"]
    
    # Mock ROI masks
    roi_masks = {
        "amygdala": MagicMock(),
        "hippocampus": MagicMock()
    }
    
    # Mocking nibabel load function
    with patch("nibabel.load") as mock_nib_load, \
         patch("pandas.read_csv") as mock_read_csv, \
         patch("nilearn.image.resample_to_img") as mock_resample:
        
        # Mock fMRI data
        mock_img = MagicMock()
        mock_img.get_fdata.return_value = np.random.rand(64, 64, 36, 200)  # Fake 4D fMRI data
        mock_nib_load.return_value = mock_img
        
        # Mock stimulus data
        mock_read_csv.return_value = pd.DataFrame({
            "onset": [10, 20, 30],
            "stimulus": ["CSnegFt", "CSneutFt", "CSminFt"]
        })
        
        # Mock resampled mask
        mock_resample.return_value.get_fdata.return_value = np.ones((64, 64, 36))
        
        # Run function
        process_fmri_subject(subject_id, phase, roi_masks, fmri_base_path, roi_names)
        
        # Check that mocks were called
        mock_nib_load.assert_called()
        mock_read_csv.assert_called()
        mock_resample.assert_called()

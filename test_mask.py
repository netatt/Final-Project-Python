import pytest
from nilearn.image import new_img_like
import mask  

def test_generate_roi_masks():
    """Test that generate_roi_masks runs successfully and returns expected keys."""
    roi_masks = generate_roi_masks()
    
    # Check if the function returned a dictionary
    assert isinstance(roi_masks, dict), "generate_roi_masks should return a dictionary"
    
    # Expected ROI keys
    expected_rois = {'Hippocampus', 'Amygdala', 'SFG', 'vmPFC', 'Insula', 'ACC'}
    
    # Check if all expected ROIs are in the dictionary
    assert expected_rois.issubset(roi_masks.keys()), "Missing expected ROIs in the output"

    # Check if all values are valid Nifti images
    for roi, mask in roi_masks.items():
        assert mask is not None, f"Mask for {roi} is None"
        assert isinstance(mask, type(new_img_like(mask, mask.get_fdata()))), f"{roi} is not a valid Nifti image"

if __name__ == "__main__":
    pytest.main()

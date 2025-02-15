from nilearn import datasets
from nilearn.image import math_img
import logging

def generate_roi_masks():
    """Fetches the Harvard-Oxford atlases and generates ROI masks."""
    try:
        # Load the Harvard-Oxford Cortical Atlas
        atlas = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-1mm')
        # Load the Harvard-Oxford Sub-Cortical Atlas
        subcortical_atlas = datasets.fetch_atlas_harvard_oxford('sub-maxprob-thr25-1mm')
    except ValueError as e:
        logging.error(f"ValueError: {e} - Invalid atlas name or parameters.")
        return None
    except TypeError as e:
        logging.error(f"TypeError: {e} - Invalid argument type.")
        return None
    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError: {e} - The required dataset file could not be found.")
        return None
    except ConnectionError as e:
        logging.error(f"ConnectionError: {e} - There was an issue with fetching the dataset.")
        return None
    except OSError as e:
        logging.error(f"OSError: {e} - There was an issue with file system access.")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

    # Create ROI masks
    roi_masks = {
        'Hippocampus': math_img("(img == 9) | (img == 19)", img=subcortical_atlas.maps),
        'Amygdala': math_img("(img == 10) | (img == 20)", img=subcortical_atlas.maps),
        'SFG': math_img("img == 3", img=atlas.maps),
        'vmPFC': math_img("(img == 26) | (img == 28)", img=atlas.maps),
        'Insula': math_img("img == 2", img=atlas.maps),
        'ACC': math_img("(img == 30) | (img == 29)", img=atlas.maps)
    }
    
    return roi_masks
import pandas as pd 
import numpy as np
import logging
import os
import nibabel as nib
from nilearn import image
from itertools import product

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_fmri_paths(fmri_base_path, subject_id, phase):
    """
    Generate file paths for fMRI and stimulus data.
    Args:
        fmri_base_path (str): The base path where fMRI and stimulus data are stored.
        subject_id (str): The ID of the subject.
        phase (str): The experimental phase, either 'learning' or 'memory'.

    Returns:
        tuple: A tuple containing the fMRI file path and the stimulus file path.
    """

    # Generate fMRI file path based on subject ID and phase (learning or memory)
    fmri_file = os.path.join(fmri_base_path, f"{subject_id}_task-RepMem{1 if phase == 'learning' else '2B'}_bold.nii.gz")

    # Generate stimulus file path based on subject ID and phase (learning or memory)
    stimulus_file = os.path.join(fmri_base_path, f"{subject_id}_task-RepMem{1 if phase == 'learning' else '2B'}_events.tsv")

    # Return the file paths as a tuple
    return fmri_file, stimulus_file

def process_fmri_subject(subject_id, phase, roi_masks, fmri_base_path, roi_names, TR=2.0, window_duration=4):
    """
    Process fMRI data for a given subject and phase.
    """
    try:
        # Get fMRI and stimulus file paths
        fmri_file, stimulus_file = get_fmri_paths(fmri_base_path, subject_id, phase)

        # Load the fMRI image and stimulus data
        fmri_img = nib.load(fmri_file)
        fmri_data = fmri_img.get_fdata()  # Extract fMRI data from the image
        n_timepoints = fmri_data.shape[-1] # Get the number of time points
        stimulus_data = pd.read_csv(stimulus_file, sep='\t') # Load stimulus data from the .tsv file

    except FileNotFoundError:
        logging.error(f"Missing file for {subject_id} in {phase} phase, skipping...")
        return # Return if any file is not found
    except Exception as e:
        logging.error(f"Error loading data for {subject_id} in {phase}: {e}")
        return # Return if there is an error during loading
    
    try:
        # Filter relevant stimuli based on the 'stimulus' column and exclude certain stimuli
        filtered_stimuli = stimulus_data[stimulus_data['stimulus'].str.endswith('t') & (stimulus_data['stimulus'] != 'USneut')]

        # Define stimulus categories and assign a numerical order to them
        stimulus_order = {'CSnegFt': 1, 'CSneutFt': 2, 'CSminFt': 3, 'CSnegHt': 4, 'CSneutHt': 5, 'CSminHt': 6}

        # Map stimulus categories to their order and sort the data by category and onset time
        filtered_stimuli['category_order'] = filtered_stimuli['stimulus'].map(stimulus_order)
        filtered_stimuli = filtered_stimuli.sort_values(by=['category_order', 'onset'])
    except Exception as e:
        logging.error(f"Error processing stimulus data for {subject_id} ({phase}): {e}")
        return # Return if there is an error during stimulus filtering or processing
    
    # Calculate the number of time points per window
    n_tr_window = int(window_duration / TR)
    
    # Loop over the regions of interest (ROIs) for this subject and phase
    for roi_name in roi_names:
        try:
            logging.info(f"Processing {roi_name} for {subject_id} in {phase} phase")

            # Get the mask for the current ROI
            roi_mask = roi_masks[roi_name]

            # Resample the ROI mask to the same space as the fMRI data
            resampled_mask = image.resample_to_img(roi_mask, image.index_img(fmri_img, 0), interpolation='nearest')
            spatial_patterns = [] # List to store the spatial patterns for each trial
            trial_labels = [] # List to store the corresponding stimulus types

            # Loop through each filtered stimulus to extract fMRI data around the stimulus onset
            for _, row in filtered_stimuli.iterrows():
                try:
                    # Get stimulus onset time and type
                    onset_time = row['onset']
                    stimulus_type = row['stimulus']

                    # Convert onset time to the corresponding timepoint (TR index)
                    onset_tr = int(onset_time / TR)

                    # Define the time window (start and end TRs)
                    start_tr, end_tr = onset_tr, onset_tr + n_tr_window
                    
                    # Skip if the window is out of bounds (e.g., too many TRs)
                    if end_tr > n_timepoints:
                        logging.warning(f"Skipping {stimulus_type} for {subject_id} ({phase}), window out of bounds")
                        continue
                    
                    # Extract the fMRI data for this trial within the time window
                    bold_window = fmri_data[..., start_tr:end_tr]

                    # Apply the ROI mask to the fMRI data (mask the voxel values)
                    masked_data = bold_window[resampled_mask.get_fdata().astype(bool)]

                    # Compute the spatial pattern (average of voxel values in the window)
                    spatial_pattern = np.mean(masked_data, axis=1)

                    # Append the spatial pattern and stimulus type
                    spatial_patterns.append(spatial_pattern)
                    trial_labels.append(stimulus_type)
                
                except Exception as e:
                    logging.error(f"Error processing stimulus {stimulus_type} for {subject_id} ({phase}): {e}")
                    continue # Continue to the next stimulus if an error occurs
            
            # Stack the spatial patterns into a matrix where each row is a trial's spatial pattern
            spatial_patterns_matrix = np.vstack(spatial_patterns)

            # Log the shape of the spatial patterns matrix for this ROI
            logging.info(f"Spatial Patterns Matrix Shape for {roi_name} ({subject_id}, {phase}): {spatial_patterns_matrix.shape}")

            # Create a DataFrame with trial labels as the index and voxel columns
            roi_df = pd.DataFrame(spatial_patterns_matrix, index=trial_labels, columns=[f"Voxel_{i+1}" for i in range(spatial_patterns_matrix.shape[1])])
            
            # Define the output file name based on subject, phase, and ROI name
            output_file = f"{subject_id}_{phase}_{roi_name}_spatial_patterns.csv"

            # Save the spatial patterns DataFrame to a CSV file
            roi_df.to_csv(output_file)
            logging.info(f"Saved: {output_file}")
        
        except Exception as e:
            logging.error(f"Error processing ROI {roi_name} for {subject_id} ({phase}): {e}")
            continue # Continue to the next ROI if an error occurs

def process_all_subjects(subject_ids, experiment_phases, roi_masks, fmri_base_path, roi_names):
    """
    Process fMRI data for all subjects and phases.
    """
    for subject_id, phase in product(subject_ids, experiment_phases):
        process_fmri_subject(subject_id, phase, roi_masks, fmri_base_path, roi_names)


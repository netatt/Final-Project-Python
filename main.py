import config
import upload_files
import preprocess
import extract_spatial_patterns
import mask
import similarity_matrix
import within_stimulus
import between_stimulus
import anova
import logging
import pandas as pd
import os

# UPLOAD FILES # 

# Displaying the results of classifying the files 
upload_files.classify_files_func()
upload_files.classify_files_anat()

# load subjects
for sub_id in range(1,39):
    sub_id = f'{sub_id:03d}'
    for t in config.task:
        upload_files.upload_func(sub_id, t)
        upload_files.upload_anat(sub_id, t)


# PREPROCESSING #

# Run Preprocessing for All Subjects
for subject_id in range(1, 39):  # 1 to 38
    for task in ['1', '2B']: 
        preprocess.preprocess_subject(subject_id, task)
        
# Plot example of one subject

data_files = [
    (f"/content/{config.subject_id}_T1w.nii.gz", "Original T1", None, None, "gray"),
    (f"/content/{config.subject_id}_task-RepMem1_bold.nii.gz", "Original fMRI", None, 0, "hot"),
    (os.path.join(config.output_dir, f"{config.subject_id}_task-1_motion_corrected.nii.gz"), "Motion Corrected fMRI", None, 0, "hot"),
    (os.path.join(config.output_dir, f"{config.subject_id}_task-1_smoothed.nii.gz"), "Smoothed fMRI", None, 0, "hot"),
    (os.path.join(config.output_dir, f"{config.subject_id}_task-1_highpass_filtered.nii.gz"), "High-Pass Filtered fMRI", None, 0, "hot"),
    (os.path.join(config.output_dir, f"{config.subject_id}_structural_to_MNI.nii.gz"), "T1 Registered to MNI", None, None, "gray"),
    (os.path.join(config.output_dir, f"{config.subject_id}_structural_to_func.nii.gz"), "fMRI Registered to T1", None, 0, "hot"),
    (os.path.join(config.output_dir, "registered_func_to_mni_2mm.nii.gz"), "fMRI Registered to MNI", None, 0, "hot"),
]

# Process and display images
for file_path, title, slice_idx, timepoint, cmap in data_files:
    preprocess.load_and_plot(file_path, title, slice_idx, timepoint, cmap)

# MASK #

roi_masks = mask.generate_roi_masks()

# SPATIAL PATTERNS #

# Process fMRI data for all subjects across all phases and ROIs, and save the spatial patterns for each combination
extract_spatial_patterns.process_all_subjects(config.subject_ids, config.experiment_phases, roi_masks, config.fmri_base_path, config.roi_names)

# SIMILARITY MATRIX #

# Loop over phases and ROIs
for phase in config.experiment_phases:
    for roi in config.roi_names:
        logging.info(f"Processing similarity matrix for {phase} phase and {roi} ROI")
        similarity_matrix.compute_similarity(config.subject_ids, config.fmri_base_path, phase, roi)


# WITHIN STIMULUS #

# Loop for processing and plotting (without a main function)
for roi_name in config.roi_names:
    for phase in config.experiment_phases:
        print(f"Processing {roi_name} in {phase} phase")

        mean_within_stimulus = within_stimulus.process_within_stimulus_similarity(config.fmri_base_path, config.subject_ids, roi_name, phase)
        
        # Save the results to CSV
        within_df = pd.DataFrame(mean_within_stimulus)
        output_file = f"within_stimulus_similarity_{roi_name}_{phase}.csv"
        within_df.to_csv(output_file, index=False)
        print(f"File '{output_file}' saved successfully!")

        # Plot the results
        within_stimulus.plot_within_stimulus_similarity(mean_within_stimulus, roi_name, phase)
        
# BETWEEN STIMULUS #

# Loop over experiment phases and ROIs to process and plot
for phase in config.experiment_phases:
    for roi in config.roi_names:
        # Process between-stimulus similarity
        between_stimulus_results = between_stimulus.process_between_stimulus_similarity(config.fmri_base_path, config.subject_ids, roi, phase)
        
        # Calculate group mean correlations
        group_mean_between_stimulus = between_stimulus.calculate_group_mean(between_stimulus_results)
        
        # Save the results to CSV
        between_stimulus.save_to_csv(group_mean_between_stimulus, phase, roi)
        
        # Plot the between-stimulus similarity
        between_stimulus.plot_between_stimulus_similarity(group_mean_between_stimulus, phase, roi)
        
        
# ANOVA #

for file_name in os.listdir(config.fmri_base_path):
    if file_name.endswith("between_stimulus_similarity.csv"):
        file_path = os.path.join(config.fmri_base_path, file_name)
        
        # Load and preprocess data
        data_long = anova.load_and_preprocess_data(file_path)
        
        if data_long is not None:
            # Perform ANOVA
            anova_results = anova.perform_anova(data_long)
            
            # If ANOVA results are significant, perform pairwise t-tests
            if anova_results is not None and any(anova_results["p-GG-corr"] < 0.05):
                anova.perform_pairwise_ttests(data_long)
            
            # Plot the results for the current file
            anova.plot_between_stimulus_similarity(data_long)
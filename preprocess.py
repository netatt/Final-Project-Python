import os
import config
import nibabel as nib
import matplotlib.pyplot as plt

# Set FSL environment using values from config
os.environ['FSLDIR'] = config.FSLDIR
os.environ['PATH'] += f":{config.FSLDIR}/bin"
os.environ['FSLOUTPUTTYPE'] = config.FSLOUTPUTTYPE

def preprocess_subject(subject_id, task):
    sub_id = f"sub-sc{subject_id:03d}"
    print(f"Processing {sub_id} Task {task}...")

    # Input and output paths
    bold_file = f"{config.fmri_base_path}/{sub_id}_task-RepMem{task}_bold.nii.gz"
    t1_file = f"{config.fmri_base_path}/{sub_id}_T1w.nii.gz"
    slicetime_corrected = f"{config.output_dir}/{sub_id}_task-{task}_slicetime_corrected.nii.gz"
    motion_corrected = f"{config.output_dir}/{sub_id}_task-{task}_motion_corrected.nii.gz"
    mean_ref = f"{config.output_dir}/{sub_id}_task-{task}_mean_ref.nii.gz"
    smoothed = f"{config.output_dir}/{sub_id}_task-{task}_smoothed.nii.gz"
    highpass_filtered = f"{config.output_dir}/{sub_id}_task-{task}_highpass_filtered.nii.gz"
    mean_func = f"{config.output_dir}/{sub_id}_task-{task}_mean_func.nii.gz"
    structural_to_func_mat = f"{config.output_dir}/{sub_id}_structural_to_func.mat"
    structural_to_MNI_mat = f"{config.output_dir}/{sub_id}_structural_to_MNI.mat"
    normalized_func = f"{config.output_dir}/{sub_id}_task-{task}_normalized_func.nii.gz"

    # Step 0: Check input files
    if not os.path.exists(bold_file):
        print(f"Error: Functional file {bold_file} not found.")
        return
    if not os.path.exists(t1_file):
        print(f"Error: Structural file {t1_file} not found.")
        return

    # Step 1: Slice Time Correction
    if not os.path.exists(slicetime_corrected):
        os.system(f"slicetimer -i {bold_file} -o {slicetime_corrected} --odd")

    # Step 2: Motion Correction
    if not os.path.exists(motion_corrected):
        os.system(f"fslmaths {slicetime_corrected} -Tmean {mean_ref}")
        os.system(f"mcflirt -in {slicetime_corrected} -out {motion_corrected} -r {mean_ref} -rmsrel -rmsabs -plots -scaling 4")

    # Step 3: Spatial Smoothing
    if not os.path.exists(smoothed):
        os.system(f"fslmaths {motion_corrected} -s 2.123 {smoothed}")

    # Step 4: Mean Functional Volume
    if not os.path.exists(mean_func):
        os.system(f"fslmaths {smoothed} -Tmean {mean_func}")

    # Step 5: Structural to Functional Registration
    if not os.path.exists(structural_to_func_mat):
        print("Running Structural to Functional Registration...")
        os.system(f"flirt -in {t1_file} -ref {mean_func} -out {output_dir}/{sub_id}_structural_to_func.nii.gz -omat {structural_to_func_mat} -dof 6")
        if not os.path.exists(structural_to_func_mat):
            print(f"Error: Structural to Functional matrix {structural_to_func_mat} was not created.")

    # Step 6: Structural to MNI Registration
    if not os.path.exists(structural_to_MNI_mat):
        print("Running Structural to MNI Registration...")
        os.system(f"flirt -in {t1_file} -ref /content/fsl/data/standard/MNI152_T1_2mm.nii.gz -out {output_dir}/{sub_id}_structural_to_MNI.nii.gz -omat {structural_to_MNI_mat} -dof 12")
        if not os.path.exists(structural_to_MNI_mat):
            print(f"Error: Structural to MNI matrix {structural_to_MNI_mat} was not created. Check FSLDIR or input files.")

    # Step 7: Functional Normalization to MNI
    if not os.path.exists(normalized_func):
        print("Running Functional Normalization to MNI...")
        os.system(f"flirt -in {smoothed} -ref /content/fsl/data/standard/MNI152_T1_2mm.nii.gz -out {normalized_func} -applyxfm -init {structural_to_MNI_mat}")
        if not os.path.exists(normalized_func):
            print(f"Error: Normalized functional file {normalized_func} was not created. Check matrix and reference files.")

    # Step 8: High-pass Filtering
    if not os.path.exists(highpass_filtered):
        os.system(f"fslmaths {normalized_func} -bptf 50 -1 {highpass_filtered}")

    # Upload files to Google Cloud Storage
    for file in [slicetime_corrected, motion_corrected, smoothed, normalized_func, highpass_filtered, mean_func, structural_to_func_mat, structural_to_MNI_mat]:
        if os.path.exists(file):
            os.system(f"gsutil cp {file} {config.gcs_output_path}/{sub_id}/")
        else:
            print(f"Warning: File {file} not found and will not be uploaded.")

    print(f"Finished processing {sub_id} Task {task}.")


def load_and_plot(file_path, title, slice_idx=None, timepoint=None, cmap="gray", figsize=(6, 6)):
    """Loads a NIfTI file and plots a selected slice."""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
    
    print(f"Displaying {title}:")
    img = nib.load(file_path)
    data = img.get_fdata()
    
    plt.figure(figsize=figsize)
    if slice_idx is None:
        slice_idx = data.shape[2] // 2  # Default to middle slice
    if timepoint is not None and data.ndim == 4:  # For 4D file
        plt.imshow(data[:, :, slice_idx, timepoint], cmap=cmap)
        plt.title(f"{title}\nSlice {slice_idx}, Timepoint {timepoint}")
    else:  # For 3D file
        plt.imshow(data[:, :, slice_idx], cmap=cmap)
        plt.title(f"{title}\nSlice {slice_idx}")
    plt.colorbar()
    plt.show()

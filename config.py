task = ['1', '2B']

# subject list (38 participants)
subject_ids = [f"sub-sc{str(i).zfill(3)}" for i in range(1, 39)]

# phases of the experiment
experiment_phases = ["learning", "memory"]

# ROIs
roi_names = ["SFG", "ACC", "Amygdala", "Hippocampus", "Insula", "vmPFC"]

# Path base structure
fmri_base_path = "/content"

stimulus_types = ["CSnegFt", "CSneutFt", "CSminFt", "CSnegHt", "CSneutHt", "CSminHt"]

trial_pairs = ["1-2", "2-3", "3-4", "4-5", "5-6", "6-7"]

stimulus_categories = {
    "CSneg": ["CSnegFt", "CSnegHt"],
    "CSneut": ["CSneutFt", "CSneutHt"],
    "CSmin": ["CSminFt", "CSminHt"]
}

output_dir = '/content/preprocessed'
bucket_name = 'dsprojectdata'
gcs_output_path = f"gs://{bucket_name}/preprocessed"

# Set FSL environment
FSLDIR = '/usr/local/fsl'
FSLOUTPUTTYPE = 'NIFTI_GZ'

subject_id = "sub-sc001"
from google.colab import auth
from google.cloud import storage

# Authenticate with Google Cloud
auth.authenticate_user()

# Initialize the Google Cloud Storage client
client = storage.Client()

# Set bucket name
bucket_name = 'dsprojectdata'
bucket = client.get_bucket(bucket_name)

# Defining the base folder path
base_path = 'ds003550'

# Function to classify files into groups
def classify_files_func():
    for sub_id in range(1,39):
        sub_folder = f'sub-sc{sub_id:03d}'
        func_folder = f'{base_path}/{sub_folder}/func'

        # Listing all the files in the 'eeg' folder for each subject
        blobs = bucket.list_blobs(prefix=func_folder)

        # Iterating through all the files
        for blob in blobs:
            file_name = blob.name
            file_path = f'gs://{bucket_name}/{file_name}'
            print(file_path)
    return None

def classify_files_anat():
    for sub_id in range(1,39):
        sub_folder = f'sub-sc{sub_id:03d}'
        anat_folder = f'{base_path}/{sub_folder}/anat'

        # Listing all the files in the 'eeg' folder for each subject
        blobs = bucket.list_blobs(prefix=anat_folder)

        # Iterating through all the files
        for blob in blobs:
            file_name = blob.name
            file_path = f'gs://{bucket_name}/{file_name}'
            print(file_path)
    return None


def upload_func(subject_id: str, task: str):
    # Define paths to the BrainVision files for the subject and task
    niigz_path = f'ds003550/sub-sc{subject_id}/func/sub-sc{subject_id}_task-RepMem{task}_bold.nii.gz' # task= 1 or 2B
    tsv_path = f'ds003550/sub-sc{subject_id}/func/sub-sc{subject_id}_task-RepMem{task}_events.tsv'

    # Download the files from Google Cloud Storage
    for file_path in [niigz_path, tsv_path]:
        blob = bucket.blob(file_path)
        blob.download_to_filename(f'/content/{file_path.split("/")[-1]}')
    return None

def upload_anat(subject_id: str, task: str):
    # Define paths to the BrainVision files for the subject and task
    niigz_path = f'ds003550/sub-sc{subject_id}/anat/sub-sc{subject_id}_T1w.nii.gz'
    json_path = f'ds003550/sub-sc{subject_id}/anat/sub-sc{subject_id}_T1w.json'

    # Download the files from Google Cloud Storage
    for file_path in [niigz_path, json_path]:
        blob = bucket.blob(file_path)
        blob.download_to_filename(f'/content/{file_path.split("/")[-1]}')
    return None





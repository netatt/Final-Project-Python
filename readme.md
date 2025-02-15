
# fMRI Analysis Project

This project is designed for analyzing fMRI data to identify spatial patterns and perform statistical analyses based on different experimental phases (e.g., "learning" and "memory"). The project processes fMRI data to generate similarity matrices, compute spatial patterns for regions of interest (ROIs), and visualize results. It utilizes popular libraries like `nibabel`, `numpy`, `pandas`, `seaborn`, and `matplotlib`.
We aim to investigate fear memory based on the paper in file: 'reference paper'.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Testing](#testing)

## Installation

To get started with this project, clone the repository and set up a Python environment.

### Step 1: Clone the repository

git clone https://github.com/yourusername/fmri-analysis.git

### Step 2: Install dependencies

Create a virtual environment and install all dependencies listed in `pyproject.toml`.

### Step 3: Activate the virtual environment

Now you can run the project’s functions from within the virtual environment.

## Usage

The project is structured to process fMRI data for different subjects and experimental phases. Here’s how to use the code.

### Step 1: Prepare your data

Ensure that your fMRI and stimulus data are organized as follows:

- fMRI data in NIfTI format (`.nii.gz`).
- Stimulus event data in tab-separated `.tsv` files, containing columns like `stimulus`, `onset`, and `duration`.

The filenames should follow the pattern:

- `subjectID_task-RepMemX_bold.nii.gz`
- `subjectID_task-RepMemX_events.tsv`

### Step 2: Define constants and parameters

In your `config.py` file, set the following parameters for your analysis:

- `FMRI_BASE_PATH`: Base path where the fMRI and stimulus data are stored.
- `SUBJECT_IDS`: List of subject IDs.
- `EXPERIMENT_PHASES`: List of phases (e.g., `["learning", "memory"]`).
- `ROI_MASKS`: Paths to the ROI mask files.
- `ROI_NAMES`: Names of the regions of interest to be analyzed.

### Step 3: Run the analysis

This will process the fMRI data for each subject in each phase, generate spatial patterns, and save them to CSV files.

### Step 4: Compute similarity matrices

This will generate a group-level similarity matrix and plot a heatmap of the results.

### Step 5: Visualize Results

Use `seaborn` and `matplotlib` to visualize the similarity matrices and other statistical results, which are generated and saved automatically.

## Project Structure

```
fmri-analysis/
├── config.py          # Configuration file with constants
├── main.py            # Main script to run the analysis
├── extract_spatial_patterns
├── preprocess.py         # Module for processing fMRI data
├── similarity_matrix.py      # Module for computing similarity matrices
├── within_stimulus    
├── between_stimulus
├── anova
├── pyproject.toml     
├── README.md          # Project documentation
└── tests/             # Directory containing unit tests
```

## Dependencies

The project uses the following Python libraries:

- `numpy`: Numerical operations.
- `pandas`: Data manipulation.
- `nibabel`: For handling NIfTI files.
- `seaborn`: Statistical data visualization.
- `matplotlib`: Plotting library.
- `scipy`: For statistical analysis (e.g., ANOVA).
- `pingouin`: For advanced statistical analysis.
- `nilearn`: For fMRI data analysis and visualization.
- `pytest`: For running tests.

Development dependencies:

- `black`: Automatic code formatting.
- `flake8`: Code linting.
- `isort`: Sorting imports.
- `pytest-cov`: Code coverage for tests.

## Testing

Run tests using `pytest` to ensure that all functions work as expected:

```bash
pytest tests/
```

This will run all the tests in the `tests/` directory and report the results.
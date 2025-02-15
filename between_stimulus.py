import config
import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to process between-stimulus similarity for a specific phase, roi, and subject
def process_between_stimulus_similarity(fmri_base_path, subject_ids, roi_name, phase):
    between_stimulus_results = {category: [] for category in config.stimulus_categories}

    for subject in subject_ids:
        file_name = os.path.join(fmri_base_path, f"{subject}_{phase}_{roi_name}_spatial_patterns.csv")

        try:
            if not os.path.exists(file_name):
                raise FileNotFoundError(f"File is missing: {file_name}")
            
            df = pd.read_csv(file_name, index_col=0)
            trial_labels = df.index.tolist()

            # Loop over each stimulus category
            for category, stimuli in config.stimulus_categories.items():
                stim1_trials = [i for i, label in enumerate(trial_labels) if label == stimuli[0]]
                stim2_trials = [i for i, label in enumerate(trial_labels) if label == stimuli[1]]

                # Ensure enough trials of each type
                if len(stim1_trials) < 7 or len(stim2_trials) < 7:
                    continue

                # Calculate Pearson correlation for the pairs of trials
                corrs = []
                for trial_pair_num in range(7):
                    stim1_idx = stim1_trials[trial_pair_num]
                    stim2_idx = stim2_trials[trial_pair_num]
                    corr = np.corrcoef(df.iloc[stim1_idx].values, df.iloc[stim2_idx].values)[0, 1]
                    corrs.append(corr)

                # Store the results for this category
                between_stimulus_results[category].append(corrs)

        except (FileNotFoundError, pd.errors.EmptyDataError, Exception) as e:
            print(f"Error processing {file_name}: {e}")
            continue

    return between_stimulus_results

# Function to calculate group mean correlations across subjects
def calculate_group_mean(between_stimulus_results):
    return {category: np.mean(between_stimulus_results[category], axis=0) for category in stimulus_categories}

# Function to plot between-stimulus similarity
def plot_between_stimulus_similarity(group_mean_between_stimulus, phase, roi):
    plt.figure(figsize=(8, 5))

    trial_numbers = np.arange(1, 8)  # 7 trials

    for category, mean_corrs in group_mean_between_stimulus.items():
        plt.plot(trial_numbers, mean_corrs, marker="o", linestyle="-", label=category)

    plt.xlabel("Trial Number")
    plt.ylabel("Between-Stimulus Correlation")
    plt.title(f"{phase.capitalize()} Phase - Between-Stimulus Similarity ({roi})")
    plt.legend(title="Stimulus Category")
    plt.grid(True)
    plt.show()

# Function to save the group mean between-stimulus results to a CSV file
def save_to_csv(group_mean_between_stimulus, phase, roi, output_dir=""):
    try:
        # Prepare the output file path with phase and ROI in the filename
        output_file = os.path.join(output_dir, f"between_stimulus_similarity_{phase}_{roi}.csv")
        
        # Prepare data for saving
        output_data = []
        for category, mean_corrs in group_mean_between_stimulus.items():
            for trial_idx, value in enumerate(mean_corrs):
                output_data.append([phase, roi, category, trial_idx + 1, value])

        # Convert to DataFrame
        output_df = pd.DataFrame(output_data, columns=["Phase", "ROI", "Stimulus_Category", "Trial", "Correlation"])

        # Save to a unique CSV file for each phase and ROI
        output_df.to_csv(output_file, index=False)
        print(f"The file '{output_file}' saved successfully.")
    
    except Exception as e:
        print(f"Error saving the file: {e}")
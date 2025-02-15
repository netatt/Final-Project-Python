import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import config

# Function to load and process correlation data
def process_within_stimulus_similarity(fmri_base_path, subject_ids, roi_name, phase):
    within_stimulus_results = {stim: [] for stim in config.stimulus_types}
    
    for subject in subject_ids:
        file_name = os.path.join(fmri_base_path, f"{subject}_{phase}_{roi_name}_spatial_patterns.csv")
        
        # Try to read the file and catch any errors
        try:
            if not os.path.exists(file_name):
                raise FileNotFoundError(f"File is missing: {file_name}")
            
            df = pd.read_csv(file_name, index_col=0)
            trial_labels = df.index.tolist()

            # Process correlations for each stimulus
            for stim in config.stimulus_types:
                stim_indices = [i for i, label in enumerate(trial_labels) if label == stim]
                
                if len(stim_indices) < 2:
                    continue

                corrs = []
                for i in range(len(stim_indices) - 1):
                    idx1, idx2 = stim_indices[i], stim_indices[i + 1]
                    corr = np.corrcoef(df.iloc[idx1].values, df.iloc[idx2].values)[0, 1]
                    corrs.append(corr)

                within_stimulus_results[stim].append(corrs)

        except (FileNotFoundError, pd.errors.EmptyDataError, Exception) as e:
            print(f"Error processing {file_name}: {e}")
            continue
    
    # Calculate mean correlations
    mean_within_stimulus = {stim: np.mean(within_stimulus_results[stim], axis=0) for stim in config.stimulus_types}
    return mean_within_stimulus

# Function to plot the results
def plot_within_stimulus_similarity(mean_within_stimulus, roi_name, phase):
    # Averaging across groups
    grouped_results = {
        "CSneg": np.mean([mean_within_stimulus["CSnegFt"], mean_within_stimulus["CSnegHt"]], axis=0),
        "CSneut": np.mean([mean_within_stimulus["CSneutFt"], mean_within_stimulus["CSneutHt"]], axis=0),
        "CSmin": np.mean([mean_within_stimulus["CSminFt"], mean_within_stimulus["CSminHt"]], axis=0),
    }

    # Create a plot
    plt.figure(figsize=(8, 5))

    for stim, mean_corrs in grouped_results.items():
        plt.plot(config.trial_pairs, mean_corrs, marker="o", linestyle="-", label=stim)

    plt.xlabel("Trial Pair")
    plt.ylabel("Correlation")
    plt.title(f"Within-Stimulus Similarity Across Trials ({roi_name} - {phase.capitalize()})")
    plt.legend(title="Stimulus Category")
    plt.grid(True)
    plt.show()
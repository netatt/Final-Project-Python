import os
import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt
import seaborn as sns

def compute_similarity(subject_ids, fmri_base_path, phase, roi):
    """
    Compute similarity matrices across subjects for a given phase (learning or memory) and ROI.
    """
    all_similarity_matrices = []  # Store similarity matrices for all subjects
    stimulus_labels = []  # Store stimulus labels (trial labels)
    
    for subject_id in subject_ids:
        try:
            # Load spatial pattern data for the given subject, phase, and ROI
            file_name = os.path.join(fmri_base_path, f"{subject_id}_{phase}_{roi}_spatial_patterns.csv")
            df = pd.read_csv(file_name, index_col=0)
            trial_labels = df.index.tolist()
            
            # Initialize stimulus labels on the first iteration
            if not stimulus_labels:
                stimulus_labels = trial_labels
            
            # Compute correlation matrix (similarity matrix) between trials
            similarity_matrix = np.corrcoef(df.values)

            # Check if matrix is of correct size (42x42)
            if similarity_matrix.shape != (42, 42):
                logging.warning(f"Error matrix size for {subject_id}: {similarity_matrix.shape}, skipping...")
                continue
            
            # Append the similarity matrix to the list
            all_similarity_matrices.append(similarity_matrix)

            # Plot the individual subject similarity matrix
            plot_similarity_matrix(similarity_matrix, trial_labels, subject_id, phase, roi)
        except FileNotFoundError:
            logging.error(f"Missing file {file_name}, skipping...")
        except Exception as e:
            logging.error(f"Error processing similarity matrix for {subject_id}: {e}")
    
    if not all_similarity_matrices:
        logging.error("No valid files found, check the data!")
        return
    
    # Compute the group-level mean similarity matrix
    group_similarity_matrix = np.mean(all_similarity_matrices, axis=0)

    # Plot the group-level similarity matrix
    plot_similarity_matrix(group_similarity_matrix, stimulus_labels, title=f"Group-Level Mean Similarity Matrix ({roi} - {phase.capitalize()} Phase)")
    
    # Save the group similarity matrix as a CSV
    output_file = f"group_mean_similarity_{roi}_{phase}.csv"
    np.savetxt(output_file, group_similarity_matrix, delimiter=",")
    logging.info(f"The file '{output_file}' is saved successfully!")

def plot_similarity_matrix(similarity_matrix, labels, subject_id=None, phase=None, roi=None, title=None):
    """
    Plot a heatmap for a given similarity matrix.
    """
    plt.figure(figsize=(8, 6))
    sns.heatmap(similarity_matrix, cmap="hot", square=True, cbar=True, xticklabels=labels, yticklabels=labels)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    
    # Set the title based on the inputs or default title
    if title:
        plt.title(title)
    else:
        plt.title(f"Similarity Matrix - {subject_id} ({roi} - {phase.capitalize()} Phase)")
    plt.xlabel("Trials (Stimuli)")
    plt.ylabel("Trials (Stimuli)")
    plt.show()

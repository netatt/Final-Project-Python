
import matplotlib.pyplot as plt
import pandas as pd
import pingouin as pg
import seaborn as sns

# Function to load and preprocess the data
def load_and_preprocess_data(file_path):
    try:
        data = pd.read_csv(file_path)
        
        # Displaying the column names and checking data types
        print("Columns in dataset:", data.columns)
        print("Data types:\n", data.dtypes)
        
        # Convert "Correlation" column to numeric
        data["Correlation"] = pd.to_numeric(data["Correlation"], errors="coerce")
        
        # Convert the data into a long format suitable for ANOVA
        data_long = data.melt(id_vars=["Phase", "ROI", "Stimulus_Category", "Trial"], var_name="Measure", value_name="Corr_Value")
        
        # Convert "Corr_Value" column to numeric
        data_long["Corr_Value"] = pd.to_numeric(data_long["Corr_Value"], errors="coerce")
        
        return data_long

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Function to perform within-subjects ANOVA
def perform_anova(data):
    try:
        anova_results = pg.rm_anova(dv="Corr_Value",
                                    within=["Stimulus_Category", "Phase"],
                                    subject="Trial",
                                    data=data,
                                    detailed=True)
        
        print("\nANOVA Results:")
        print(anova_results)
        return anova_results

    except Exception as e:
        print(f"Error performing ANOVA: {e}")
        return None

# Function to perform pairwise t-tests if significant ANOVA results are found
def perform_pairwise_ttests(data):
    try:
        pairwise_results = pg.pairwise_ttests(dv="Corr_Value", within=["Stimulus_Category", "Phase"], subject="Trial", data=data, padjust="bonferroni")
        print("\nPairwise T-tests:")
        print(pairwise_results)
        return pairwise_results

    except Exception as e:
        print(f"Error performing pairwise t-tests: {e}")
        return None

# Function to plot the boxplot for between-stimulus similarity
def plot_between_stimulus_similarity(data):
    try:
        plt.figure(figsize=(8, 6))
        sns.boxplot(x="Stimulus_Category", y="Corr_Value", hue="Phase", data=data)
        plt.title("Between-Stimulus Similarity Across Phases")
        plt.xlabel("Stimulus Category")
        plt.ylabel("Correlation")
        plt.legend(title="Phase")
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"Error generating plot: {e}")
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg

from anova import load_and_preprocess_data, perform_anova, perform_pairwise_ttests, plot_between_stimulus_similarity

class TestStimulusSimilarity(unittest.TestCase):

    @patch('pandas.read_csv')  # Mocking pd.read_csv to simulate file reading
    def test_load_and_preprocess_data(self, mock_read_csv):
        # Create a mock dataframe for testing
        mock_data = pd.DataFrame({
            "Phase": ['learning', 'learning', 'testing', 'testing'],
            "ROI": ['V1', 'V1', 'V1', 'V1'],
            "Stimulus_Category": ['CSneg', 'CSneg', 'CSmin', 'CSmin'],
            "Trial": [1, 2, 1, 2],
            "Correlation": [0.1, 0.2, 0.3, 0.4]
        })
        
        # Mock the return value of pd.read_csv
        mock_read_csv.return_value = mock_data
        
        # Call the function
        data_long = load_and_preprocess_data("mock_file.csv")
        
        # Check the returned data
        self.assertEqual(data_long.shape[0], 8)  # Expecting 8 rows (4 original * 2 after melt)
        self.assertIn("Corr_Value", data_long.columns)
        
        # Verify that pd.read_csv was called with the correct file path
        mock_read_csv.assert_called_with("mock_file.csv")
        
    def test_perform_anova(self):
        # Sample data for testing ANOVA
        data = pd.DataFrame({
            "Phase": ['learning', 'learning', 'testing', 'testing'],
            "ROI": ['V1', 'V1', 'V1', 'V1'],
            "Stimulus_Category": ['CSneg', 'CSneg', 'CSmin', 'CSmin'],
            "Trial": [1, 2, 1, 2],
            "Corr_Value": [0.1, 0.2, 0.3, 0.4]
        })
        
        # Mocking pingouin's rm_anova function
        with patch.object(pg, 'rm_anova', return_value=MagicMock()) as mock_rm_anova:
            mock_rm_anova.return_value = pd.DataFrame({
                'Source': ['Stimulus_Category', 'Phase'],
                'F': [4.5, 3.2],
                'p-unc': [0.05, 0.1]
            })
            
            # Call the function
            anova_results = perform_anova(data)
            
            # Check if the result is as expected
            self.assertIsNotNone(anova_results)
            self.assertIn('Source', anova_results.columns)
            
    def test_perform_pairwise_ttests(self):
        # Sample data for testing pairwise t-tests
        data = pd.DataFrame({
            "Phase": ['learning', 'learning', 'testing', 'testing'],
            "ROI": ['V1', 'V1', 'V1', 'V1'],
            "Stimulus_Category": ['CSneg', 'CSneg', 'CSmin', 'CSmin'],
            "Trial": [1, 2, 1, 2],
            "Corr_Value": [0.1, 0.2, 0.3, 0.4]
        })
        
        # Mocking pingouin's pairwise_ttests function
        with patch.object(pg, 'pairwise_ttests', return_value=MagicMock()) as mock_pairwise_ttests:
            mock_pairwise_ttests.return_value = pd.DataFrame({
                'Comparison': ['CSneg-CSmin', 'CSneg-CSneut'],
                'T': [2.4, 1.8],
                'p-unc': [0.05, 0.1]
            })
            
            # Call the function
            pairwise_results = perform_pairwise_ttests(data)
            
            # Check if the result is as expected
            self.assertIsNotNone(pairwise_results)
            self.assertIn('Comparison', pairwise_results.columns)

    @patch('matplotlib.pyplot.show')  # Mock show to prevent actual plotting
    @patch('seaborn.boxplot')  # Mock seaborn.boxplot to avoid actual plotting
    def test_plot_between_stimulus_similarity(self, mock_boxplot, mock_show):
        # Sample data for testing the plot
        data = pd.DataFrame({
            "Phase": ['learning', 'learning', 'testing', 'testing'],
            "ROI": ['V1', 'V1', 'V1', 'V1'],
            "Stimulus_Category": ['CSneg', 'CSneg', 'CSmin', 'CSmin'],
            "Trial": [1, 2, 1, 2],
            "Corr_Value": [0.1, 0.2, 0.3, 0.4]
        })
        
        # Call the function to plot
        plot_between_stimulus_similarity(data)
        
        # Verify that the seaborn boxplot and plt.show were called
        mock_boxplot.assert_called_once()
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()

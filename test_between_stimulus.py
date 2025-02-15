import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from between_stimulus import process_between_stimulus_similarity, calculate_group_mean, plot_between_stimulus_similarity, save_to_csv

# Mock config module
class MockConfig:
    stimulus_categories = {
        'CSneg_CSmin': ['CSneg', 'CSmin'],
        'CSneg_CSneut': ['CSneg', 'CSneut'],
        'CSmin_CSneut': ['CSmin', 'CSneut']
    }

# Set up logging to capture the logs during testing
logging.basicConfig(level=logging.INFO)

class TestStimulusSimilarity(unittest.TestCase):

    @patch('os.path.exists', return_value=True)  # Mocking os.path.exists to always return True
    @patch('pandas.read_csv')
    def test_process_between_stimulus_similarity(self, mock_read_csv, mock_exists):
        # Set up mock data for the DataFrame
        mock_df = MagicMock()
        mock_df.index = ['CSneg', 'CSmin', 'CSneg', 'CSmin', 'CSneut', 'CSmin', 'CSneg', 'CSneut']
        mock_df.iloc = pd.DataFrame({
            'feature1': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            'feature2': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        }).iloc

        # Mock read_csv to return the mock DataFrame
        mock_read_csv.return_value = mock_df
        
        # Call the function
        between_stimulus_results = process_between_stimulus_similarity(
            fmri_base_path='mock/path', 
            subject_ids=['01', '02'],
            roi_name='V1',
            phase='learning'
        )

        # Check that the expected result is returned and has correct structure
        self.assertIn('CSneg_CSmin', between_stimulus_results)
        self.assertIn('CSneg_CSneut', between_stimulus_results)
        self.assertIn('CSmin_CSneut', between_stimulus_results)
        self.assertTrue(isinstance(between_stimulus_results['CSneg_CSmin'], list))

        # Verify the process for stimulus categories
        mock_read_csv.assert_called_with('mock/path/01_learning_V1_spatial_patterns.csv')

    def test_calculate_group_mean(self):
        # Sample between-stimulus data for testing
        between_stimulus_results = {
            'CSneg_CSmin': [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
            'CSneg_CSneut': [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
            'CSmin_CSneut': [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        }

        # Call the function
        group_mean = calculate_group_mean(between_stimulus_results)

        # Check that the mean is calculated correctly
        self.assertIn('CSneg_CSmin', group_mean)
        self.assertEqual(len(group_mean['CSneg_CSmin']), 3)  # Should return 3 trial pairs

    @patch('matplotlib.pyplot.show')  # Mock show to prevent actual plotting
    def test_plot_between_stimulus_similarity(self, mock_show):
        # Sample mean data for testing the plot
        group_mean_between_stimulus = {
            'CSneg_CSmin': [0.5, 0.6, 0.7],
            'CSneg_CSneut': [0.6, 0.7, 0.8],
            'CSmin_CSneut': [0.4, 0.5, 0.6]
        }

        # Call the plotting function
        plot_between_stimulus_similarity(group_mean_between_stimulus, phase='learning', roi='V1')

        # Check that plt.show() was called (i.e., a plot was created)
        mock_show.assert_called_once()

    @patch('os.path.exists', return_value=True)  # Mocking os.path.exists to always return True
    @patch('pandas.read_csv')
    @patch('matplotlib.pyplot.show')  # Mock show to prevent actual plotting
    def test_save_to_csv(self, mock_show, mock_read_csv, mock_exists):
        # Sample between-stimulus data for testing
        group_mean_between_stimulus = {
            'CSneg_CSmin': [0.5, 0.6, 0.7],
            'CSneg_CSneut': [0.6, 0.7, 0.8],
            'CSmin_CSneut': [0.4, 0.5, 0.6]
        }

        # Call the function to save the results
        save_to_csv(group_mean_between_stimulus, phase='learning', roi='V1', output_dir='/mock/output')

        # Check that the file is "saved" by verifying the print statement
        expected_output = '/mock/output/between_stimulus_similarity_learning_V1.csv'
        with patch('builtins.print') as mock_print:
            save_to_csv(group_mean_between_stimulus, phase='learning', roi='V1', output_dir='/mock/output')
            mock_print.assert_called_with(f"The file '{expected_output}' saved successfully.")

if __name__ == '__main__':
    unittest.main()

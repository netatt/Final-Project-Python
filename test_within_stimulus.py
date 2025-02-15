import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging

from within_stimulus import process_within_stimulus_similarity, plot_within_stimulus_similarity

# Mock config module
class MockConfig:
    stimulus_types = ['CSnegFt', 'CSnegHt', 'CSneutFt', 'CSneutHt', 'CSminFt', 'CSminHt']
    trial_pairs = ['Trial 1-2', 'Trial 2-3', 'Trial 3-4']  # Example trial pairs

# Set up logging to capture the logs during testing
logging.basicConfig(level=logging.INFO)

class TestStimulusSimilarity(unittest.TestCase):
    
    @patch('os.path.exists', return_value=True)  # Mocking os.path.exists to always return True
    @patch('pandas.read_csv')
    def test_process_within_stimulus_similarity(self, mock_read_csv, mock_exists):
        # Set up mock data for the DataFrame
        mock_df = MagicMock()
        mock_df.index = ['CSnegFt', 'CSnegFt', 'CSneutFt', 'CSneutFt', 'CSminFt', 'CSminFt']
        mock_df.iloc = pd.DataFrame({
            'feature1': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            'feature2': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        }).iloc

        # Mock read_csv to return the mock DataFrame
        mock_read_csv.return_value = mock_df
        
        # Call the function
        mean_within_stimulus = process_within_stimulus_similarity(
            fmri_base_path='mock/path', 
            subject_ids=['01', '02'],
            roi_name='V1',
            phase='learning'
        )

        # Check that the expected result is returned
        self.assertIn('CSnegFt', mean_within_stimulus)
        self.assertIn('CSneutFt', mean_within_stimulus)
        self.assertIn('CSminFt', mean_within_stimulus)

        # Verify the process for stimulus types
        mock_read_csv.assert_called_with('mock/path/01_learning_V1_spatial_patterns.csv')

    @patch('matplotlib.pyplot.show')  # Mock show to prevent actual plotting
    def test_plot_within_stimulus_similarity(self, mock_show):
        # Sample mean data for testing the plot
        mean_within_stimulus = {
  

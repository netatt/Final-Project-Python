import unittest
from unittest.mock import patch, MagicMock
import os
import numpy as np
import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns

# Import the functions from your module
from similarity_matrix import compute_similarity, plot_similarity_matrix

class TestComputeSimilarity(unittest.TestCase):

    @patch('pandas.read_csv')
    @patch('numpy.corrcoef')
    @patch('matplotlib.pyplot.show')
    @patch('logging.error')
    @patch('logging.warning')
    def test_compute_similarity_valid_data(self, mock_warning, mock_error, mock_show, mock_corrcoef, mock_read_csv):
        # Mocking the read_csv to return a predefined dataframe
        df_mock = pd.DataFrame(np.random.rand(42, 42), index=[f"trial_{i}" for i in range(42)])
        mock_read_csv.return_value = df_mock

        # Mocking the correlation matrix
        mock_corrcoef.return_value = np.corrcoef(df_mock.values)

        # Mocking the logging methods
        mock_warning.reset_mock()
        mock_error.reset_mock()

        subject_ids = ['sub1', 'sub2']
        fmri_base_path = '/fake/path'
        phase = 'learning'
        roi = 'V1'

        compute_similarity(subject_ids, fmri_base_path, phase, roi)

        # Assertions
        mock_read_csv.assert_called()
        mock_corrcoef.assert_called()
        mock_show.assert_called()
        mock_error.assert_not_called()
        mock_warning.assert_not_called()

    @patch('pandas.read_csv')
    @patch('numpy.corrcoef')
    @patch('matplotlib.pyplot.show')
    @patch('logging.error')
    def test_compute_similarity_file_not_found(self, mock_error, mock_show, mock_corrcoef, mock_read_csv):
        # Simulate FileNotFoundError
        mock_read_csv.side_effect = FileNotFoundError

        subject_ids = ['sub1']
        fmri_base_path = '/fake/path'
        phase = 'learning'
        roi = 'V1'

        compute_similarity(subject_ids, fmri_base_path, phase, roi)

        # Assertions
        mock_error.assert_called_with('Missing file /fake/path/sub1_learning_V1_spatial_patterns.csv, skipping...')

    @patch('pandas.read_csv')
    @patch('numpy.corrcoef')
    @patch('matplotlib.pyplot.show')
    @patch('logging.warning')
    @patch('logging.error')
    def test_compute_similarity_incorrect_matrix_size(self, mock_error, mock_warning, mock_show, mock_corrcoef, mock_read_csv):
        # Mocking the read_csv to return a dataframe with 42x42 but correlation matrix of incorrect size
        df_mock = pd.DataFrame(np.random.rand(42, 42), index=[f"trial_{i}" for i in range(42)])
        mock_read_csv.return_value = df_mock

        # Mocking the correlation matrix with an incorrect shape
        mock_corrcoef.return_value = np.random.rand(30, 30)

        subject_ids = ['sub1']
        fmri_base_path = '/fake/path'
        phase = 'learning'
        roi = 'V1'

        compute_similarity(subject_ids, fmri_base_path, phase, roi)

        # Assertions
        mock_warning.assert_called_with('Error matrix size for sub1: (30, 30), skipping...')
        mock_error.assert_not_called()

class TestPlotSimilarityMatrix(unittest.TestCase):

    @patch('matplotlib.pyplot.show')
    def test_plot_similarity_matrix(self, mock_show):
        similarity_matrix = np.random.rand(42, 42)
        labels = [f"trial_{i}" for i in range(42)]
        plot_similarity_matrix(similarity_matrix, labels, title="Test Similarity Matrix")

        # Assertions
        mock_show.assert_called()

if __name__ == '__main__':
    unittest.main()

import pytest
import pandas as pd
from . import NLPRegressionDataset


class TestNLPRegressionDataset(object):

    """Docstring for TestNLPRegressionDataset. """

    @pytest.fixture
    def init_dataset(self):
        """TODO: to be defined. """
        df = pd.read_csv("sample.csv")
        self.texts = df['text']
        self.labels = df['intensity']
        self.transform = None
        self.dataset = NLPRegressionDataset(
            self.texts,
            self.labels,
            transform=self.transform
        )

    def test_data_length(self):
        """TODO: Docstring for test_.

        :returns: TODO

        """
        assert len(self.dataset) == len(self.texts)

    def test_get_item(self):
        """TODO: Docstring for test_get_item.

        :returns: TODO

        """
        idx = slice(2, 10, None)
        class_texts, class_labels = self.dataset[idx]
        if self.transform:
            texts, labels = self.transform((self.texts[idx], self.labels[idx]))
        else:
            texts, labels = (self.texts[idx], self.labels[idx])
        assert texts == class_texts
        assert labels == class_labels

import logging
import sys
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
import mlflow
import kubernetes

import torch
import torch.nn as nn
import transformers
from transformers import (
    Trainer,
    BertForSequenceClassification,
    BertJapaneseTokenizer,
    TrainingArguments,
    HfArgumentParser,
    set_seed,
)
from torch.utils.data import Dataset


@dataclass
class ModelArgument:

    """Argument for model file"""

    model_name_or_path: str = field(
        default="cl-tohoku/bert-base-japanese",
        metadata={
            "help": (
                "Path to pretrained model or model identifier "
                "from huggingface.co/models"
            )
        },
    )
    tokenizer_name_or_path: str = field(
        default="cl-tohoku/bert-base-japanese",
        metadata={
            "help": (
                "Path to pretrained tokenizer or identifier "
                "from huggingface.co/models"
            )
        },
    )


@dataclass
class DatasetArgument:

    """Argument for Dataset"""

    train_data_file_path: str = field(
        default="/tmp/train.csv",
        metadata={"help": "Train data csv file path(csv)."},
    )
    valid_data_file_path: str = field(
        default="/tmp/valid.csv",
        metadata={"help": "Valid data csv file path(csv)."},
    )
    test_data_file_path: str = field(
        default="/tmp/test.csv",
        metadata={"help": "test data csv file path(csv)."},
    )
    text_field_name: str = field(
        default="text",
        metadata={"help": "The text field name of csv. (input column)"}
    )
    label_field_name: str = field(
        default="label",
        metadata={"help": "The label field name of csv. (target column)"}
    )
    train_max_length: str = field(
        default=128,
        metadata={"help": "Maximum number of tokens in training dataset."}
    )
    valid_max_length: str = field(
        default=128,
        metadata={"help": "Maximum number of tokens in validate dataset."}
    )
    test_max_length: str = field(
        default=128,
        metadata={"help": "Maximum number of tokens in testate dataset."}
    )


@dataclass
class DataTrainArgument:

    """Additional argument for Training"""

    save_at_end_of_training: bool = field(
        default=True,
        metadata={
            "help": (
                "When True is given, save model at end of training."
                "model files will save in output_dir."
            )
        }
    )
    do_test: bool = field(
        default=False,
        metadata={
            "help": (
                "When True is given, test the model and log to mlflow."
            )
        }
    )
    gpu: bool = field(
        default=False,
        metadata={
            "help": (
                "When True is given, train/eval/test uses gpu."
            )
        }
    )
    mlflow_emotion_tag: str = field(
        default="",
        metadata={
            "help": (
                "The tag for identify kind of emotion in mlflow "
            )
        }
    )
    mlflow_model_ver_tag: str = field(
        default="",
        metadata={
            "help": (
                "The tag for identify kind of model version in mlflow "
            )
        }
    )


class NLPRegressionDataset(Dataset):

    """Custom Dataset of pytorch Dataset."""

    def __init__(
        self,
        encodings,
        labels,
        device,
        transform=None,
    ):
        """TODO: to be defined. """
        self.encodings = encodings
        self.labels = labels
        self.device = device
        if transform:
            self.transform = transform

    def __len__(self):
        """TODO: Docstring for __len__.

        :returns: TODO

        """
        return len(self.encodings['input_ids'])

    def __getitem__(self, idx):
        """TODO: Docstring for __getitem__.

        :idx: TODO
        :returns: TODO

        """
        item = {
            key: val[idx].to(self.device)
            for key, val in self.encodings.items()
        }
        item['labels'] = torch.tensor(self.labels[idx]).to(self.device)
        return item


class BertForSequenceClassificationWithSigmoid(
    BertForSequenceClassification
):

    """Docstring for BertForSequenceClassificationWithSigmoid. """

    def __init__(self, config):
        """TODO: to be defined. """
        super().__init__(config)
        self.classifier = nn.Sequential(
            self.classifier,
            nn.Sigmoid(),
        )


if __name__ == "__main__":
    parser = \
        HfArgumentParser((
            TrainingArguments,
            ModelArgument,
            DatasetArgument,
            DataTrainArgument,
        ))
    training_args, model_args, dataset_args, datatraining_args = \
        parser.parse_args_into_dataclasses()

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    log_level = training_args.get_process_log_level()
    logger.setLevel(log_level)
    transformers.utils.logging.set_verbosity(log_level)

    kubernetes.config.load_incluster_config()

    set_seed(training_args.seed)
    if datatraining_args.gpu and torch.cuda.is_available():
        device = torch.device('cuda:0')
    else:
        device = torch.device('cpu')
    logger.info(torch.cuda.is_available())
    logger.info(device)

    train_df = pd.read_csv(dataset_args.train_data_file_path)
    valid_df = pd.read_csv(dataset_args.valid_data_file_path)
    logger.info('Load train/valid csv data succeeded')

    train_texts, train_labels = (
        train_df[dataset_args.text_field_name].tolist(),
        train_df[dataset_args.label_field_name].tolist()
    )
    valid_texts, valid_labels = (
        valid_df[dataset_args.text_field_name].tolist(),
        valid_df[dataset_args.label_field_name].tolist()
    )

    # トークナイザのダウンロード
    tokenizer = BertJapaneseTokenizer.from_pretrained(
        model_args.tokenizer_name_or_path
    )
    logger.debug("Downloaded pretrained japanese tokenizer")

    # DataFrameからDatasetを作成
    # データセットは入力（NLPであれば文章）と
    # 出力（クラスタリングだとラベル）をセットにして扱うためのもの
    train_encodings = tokenizer(
        train_texts,
        return_tensors='pt',
        padding=True,
        truncation=True,
        max_length=dataset_args.train_max_length
    )
    valid_encodings = tokenizer(
        valid_texts,
        return_tensors='pt',
        padding=True,
        truncation=True,
        max_length=dataset_args.valid_max_length
    )
    train_dataset = NLPRegressionDataset(train_encodings, train_labels, device)
    valid_dataset = NLPRegressionDataset(valid_encodings, valid_labels, device)
    logger.debug('Convert dataframe to dataset(NLPRegressionDataset)')

    # BERT事前学習済みモデルのダウンロード（東北大のモデル）
    model = BertForSequenceClassificationWithSigmoid.from_pretrained(
        model_args.model_name_or_path,
        num_labels=1
    ).to(device)
    logger.debug("Downloaded pretrained japanese BERT model")

    trainer = Trainer(
        model=model,
        args=training_args,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
    )
    logger.debug('Created Trainer')

    trainer.train()

    mlflow.log_artifact("/tmp/train.csv")
    mlflow.log_artifact("/tmp/valid.csv")
    mlflow.log_artifact("/tmp/test.csv")

    mlflow.log_param("train_data_num", len(train_dataset))
    mlflow.log_param("valid_data_num", len(valid_dataset))

    if datatraining_args.mlflow_emotion_tag:
        mlflow.set_tag("emotion", datatraining_args.mlflow_emotion_tag)

    if datatraining_args.mlflow_model_ver_tag:
        mlflow.set_tag("model_ver", datatraining_args.mlflow_model_ver_tag)

    if datatraining_args.save_at_end_of_training:
        trainer.save_model("./model/")
        mlflow.log_artifacts("./model/", "model/")

    def get_pearson_corr(
        x: np.ndarray,
        y: np.ndarray,
    ) -> float:
        """
        This function returns the pearson correlation coefficient of peared
        one-dimension vectors.
        """
        return np.corrcoef(x, y).reshape(-1)[1]

    if datatraining_args.do_test:
        test_df = pd.read_csv(dataset_args.test_data_file_path)
        test_texts, test_labels = (
            test_df[dataset_args.text_field_name].tolist(),
            test_df[dataset_args.label_field_name].tolist()
        )
        test_encodings = tokenizer(
            test_texts,
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=dataset_args.test_max_length
        )
        test_dataset = \
            NLPRegressionDataset(test_encodings, test_labels, device)
        predictions, label_ids, metrics = \
            trainer.predict(test_dataset)
        test_df['predicted_label'] = predictions.ravel()
        test_df.to_csv("/tmp/predict.csv", index=False)
        mlflow.log_artifact("/tmp/predict.csv")

        # Logging pearson correlation coefficient to MLflow
        pearson_corr = get_pearson_corr(
            test_labels,
            predictions.ravel()
        )
        mlflow.log_metric("pearson corr", pearson_corr)

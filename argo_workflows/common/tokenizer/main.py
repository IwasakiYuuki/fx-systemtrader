import os
import argparse
from typing import Iterator, List

import pandas as pd
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome import charfilter, tokenfilter
from janome.tokenfilter import TokenFilter
from janome.tokenizer import Token


class WhitespaceFilter(TokenFilter):

    """Custom class of janome TokenFilter. """

    def apply(self, tokens: Iterator[Token]) -> Iterator[Token]:
        for token in tokens:
            if '空白' in token.part_of_speech:
                continue
            yield token


def main(
    text_field_names: List[str],
    unicode_normalize_charfilter: bool,
    lowercase_filter: bool,
    uppercase_filter: bool,
    compound_noun_filter: bool,
    whitespace_filter: bool,
):
    """Tokenize japanese text using janome tokenizer.

    Load input data from '/tmp/input.csv' and tokenize text field using janome.
    Save text field splited by whitespace into local file '/tmp/output.csv'.

    :param text_field_names: TODO
    :type text_field_names: TODO
    :param unicode_normalize_charfilter: TODO
    :type unicode_normalize_charfilter: TODO
    :param lowercase_filter: TODO
    :type lowercase_filter: TODO
    :param uppercase_filter: TODO
    :type uppercase_filter: TODO
    :param compound_noun_filter: TODO
    :type compound_noun_filter: TODO
    :param whitespace_filter: TODO
    :type whitespace_filter: TODO

    """
    tokenizer = Tokenizer()

    char_filters = []

    if unicode_normalize_charfilter:
        char_filters.append(charfilter.UnicodeNormalizeCharFilter())

    token_filters = []

    if lowercase_filter:
        token_filters.append(tokenfilter.LowerCaseFilter())

    if uppercase_filter:
        token_filters.append(tokenfilter.UpperCaseFilter())

    if whitespace_filter:
        token_filters.append(WhitespaceFilter())

    token_filters.append(tokenfilter.ExtractAttributeFilter('surface'))

    analyzer = Analyzer(
        char_filters=char_filters,
        tokenizer=tokenizer,
        token_filters=token_filters)

    df = pd.read_csv("/tmp/input.csv", index_col=0)

    for text_field_name in text_field_names:
        df[text_field_name] = df[text_field_name].map(
            lambda text: " ".join([
                token for token in analyzer.analyze(text)]))

    df.to_csv("/tmp/output.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--text_field_names',
        nargs='+',
        help='<Required> Set all text field name for tokenization.',
        required=True,
    )
    parser.add_argument(
        '--unicode_normalize_charfilter',
        action='store_true',
        help='<Required> Set all text field name for tokenization.',
        default=(os.getenv('UNICODE_NORMALIZE_CHARFILTER', False) == 'True')
    )
    parser.add_argument(
        '--lowercase_filter',
        action='store_true',
        help='<Required> Set all text field name for tokenization.',
        default=(os.getenv('LOWERCASE_FILTER', False) == 'True')
    )
    parser.add_argument(
        '--uppercase_filter',
        action='store_true',
        help='<Required> Set all text field name for tokenization.',
        default=(os.getenv('UPPERCASE_FILTER', False) == 'True')
    )
    parser.add_argument(
        '--compound_noun_filter',
        action='store_true',
        help='<Required> Set all text field name for tokenization.',
        default=(os.getenv('COMPOUND_NOUN_FILTER', False) == 'True')
    )
    parser.add_argument(
        '--whitespace_filter',
        action='store_true',
        help='<Required> Set all text field name for tokenization.',
        default=(os.getenv('WHITESPACE_FILTER', False) == 'True')
    )
    args = parser.parse_args()

    main(
        text_field_names=args.text_field_names,
        unicode_normalize_charfilter=args.unicode_normalize_charfilter,
        lowercase_filter=args.lowercase_filter,
        uppercase_filter=args.uppercase_filter,
        compound_noun_filter=args.compound_noun_filter,
        whitespace_filter=args.whitespace_filter,
    )

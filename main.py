import argparse
import pandas as pd


def is_sentence(text):
    return text[0].isupper() and text[-1] == '.' and len(text) > 30


def preprocess(text):
    return text.strip()


def filter_languages(df: pd.DataFrame, source_lang: str, target_lang: str) -> pd.DataFrame:
    """
    Leaves only the rows that match the given languages. It doesn't matter if the languages are in the wrong order.
    :param df:
    :param source_lang: e.g. "Finnish"
    :param target_lang: e.g. "English"
    :return:
    """
    filtered_df = df[(df.from_lang == source_lang) & (df.to_lang == target_lang)]
    filtered_reverted_df = df[(df.from_lang == target_lang) & (df.to_lang == source_lang)].rename(
        columns={"from_lang": "to_lang", "to_lang": "from_lang"}
    )
    return filtered_df.append(filtered_reverted_df, ignore_index=True)


def filter_sentences(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes sentences from the dataframe. Sentences are defined in is_sentence as follows:
    - First letter is uppercase
    - Last letter is '.'
    - Length of the sentence is greater than 30
    :param df:
    :return:
    """
    df = df[~df.text.apply(is_sentence)]
    return df[~df.translation.apply(is_sentence)]


def preprocess_text(df):
    df.text = df.text.apply(preprocess)
    df.translation = df.translation.apply(preprocess)
    return df


def main(input_file, output, source_lang, target_lang):
    # TODO: if one word, put in the normal form
    df = pd.read_csv(input_file, names=["from_lang", "to_lang", "text", "translation"])
    df = filter_languages(df, source_lang, target_lang)
    print("Data size after filtering languages", df.shape[0])
    df = filter_sentences(df)
    print("Data size without sentences", df.shape[0])
    df = preprocess_text(df)
    print("Data size after preprocessing", df.shape[0])
    df = df.rename({"text": "Suomi", "translation": "English"}, axis=1)[["Suomi", "English"]]
    df.to_excel(output, index=False, engine="openpyxl")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Exported translations from Google Translate in .csv.")
    parser.add_argument("-o", "--output", help="File to output", default="anki_translations.xlsx")
    parser.add_argument("-s", "--source", help="Source language", default="Finnish")
    parser.add_argument("-t", "--target", help="Target language", default="English")
    args = parser.parse_args()
    # TODO check if file exists
    # TODO check if input file is .csv
    # TODO for output file, provide a correct extension
    main(args.file, args.output, args.source, args.target)

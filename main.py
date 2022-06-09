import argparse
import pandas as pd


def is_sentence(row):
    text = row.text
    return text[0].isupper() and text[-1] == '.'


def preprocess(text):
    return text.strip()


def main(input_file, output):

    df = pd.read_csv(input_file, names=["from_lang", "to_lang", "text", "translation"])

    filtered_df = df[(df.from_lang == "Finnish") & (df.to_lang == "English")]
    filtered_reverted_df = df[(df.from_lang == "English") & (df.to_lang == "Finnish")]
    filtered_reverted_new_df = pd.DataFrame({
        "from_lang": filtered_reverted_df.to_lang,
        "to_lang": filtered_reverted_df.from_lang,
        "text": filtered_reverted_df.text,
        "translation": filtered_reverted_df.translation,
    })
    filtered_df = filtered_df.append(filtered_reverted_new_df, ignore_index=True)

    print(filtered_df[filtered_df.text.isnull()])

    print("Output data size", filtered_df.shape[0])
    filtered_df = filtered_df[~filtered_df.apply(is_sentence, axis=1)]
    filtered_df.text = filtered_df.text.apply(preprocess)
    filtered_df.translation = filtered_df.translation.apply(preprocess)
    print("Output data size without sentences", filtered_df.shape[0])

    filtered_df = filtered_df.rename({"text": "Suomi", "translation": "English"}, axis=1)[["Suomi", "English"]]
    filtered_df.to_excel(output, index=False, engine="openpyxl")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Exported translations from Google Translate in .csv.")
    parser.add_argument("-o", "--output", help="File to output", default="formatted_translations.xlsx")
    # TODO put correct file extension if not provided correctly
    args = parser.parse_args()
    main(args.file, args.output)

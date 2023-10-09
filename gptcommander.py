import argparse
import dotenv
import os
import pandas


# Read environment variables from .env file if it exists
dotenv.load_dotenv()

def get_input_texts(args):
    ''' Generator that yields all input text '''
    # Handle direct text input
    if args.input_text is not None:
        for text in args.input_text:
            yield { 'input': text }
    # Handle filename text input
    if args.input_filename is not None:
        for filename in args.input_filename:
            with open(filename, 'rt') as fin:
                contents = fin.read()
                fin.close()
                yield { 'input': contents }
    # Handle parquet reading
    if args.input_parquet is not None:
        df = pandas.read_parquet(args.input_parquet)
        keys = list(df.keys())
        for idx, row in df.iterrows():
            result = {}
            for key in keys:
                result[key] = row[key]
            yield result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--openai_api_key', metavar='KEY', help='You API key for OpenAI. Can also be set with environment variable OPENAI_API_KEY.')
    parser.add_argument('--togetherai_api_key', metavar='KEY', help='You API key for together.ai. Can also be set with environment variable TOGETHERAI_API_KEY.')
    parser.add_argument('--input_text', metavar='TEXT', nargs='*', help='Direct text(s) to treat as an input (will use template key "input")')
    parser.add_argument('--input_filename', metavar='FILE', nargs='*', help='Filename(s) for text to treat as an input (will use template key "input")')
    parser.add_argument('--input_parquet', metavar='FILE', help='Parquet file to use for reading input (template keys are column names)')
    args = parser.parse_args()
    if args.openai_api_key is None:
        args.openai_api_key = os.getenv('OPENAI_API_KEY')
    if args.togetherai_api_key is None:
        args.togetherai_api_key = os.getenv('TOGETHERAI_API_KEY')
    formats = 0
    formats += 1 if args.input_text is not None else 0
    formats += 1 if args.input_filename is not None else 0
    formats += 1 if args.input_parquet is not None else 0
    if formats != 1:
        raise RuntimeError('Must specify exactly 1 input format out of --input_text, --input_filename, --input_parquet')
    print(args)
    count = 0
    for text in get_input_texts(args):
        print(f'input: {count}\n{text}')
        count += 1

if __name__ == '__main__':
    main()

import argparse
import csv
import dotenv
import os

# Read environment variables from .env file if it exists
dotenv.load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--openai_api_key', metavar='KEY', help='You API key for OpenAI. Can also be set with environment variable OPENAI_API_KEY.')
    parser.add_argument('--togetherai_api_key', metavar='KEY', help='You API key for together.ai. Can also be set with environment variable TOGETHERAI_API_KEY.')
    parser.add_argument('--input_text', metavar='TEXT', nargs='*', help='Direct text to treat as an input (can be repeated)')
    parser.add_argument('--input_filename', metavar='FILE', nargs='*', help='Filename for text to treat as an input (can be repeated)')
    parser.add_argument('--input_column', metavar='COLUMN', help='Column of CSV to treat as an input text, number (1-based) or name of column')
    parser.add_argument('--input_column_filename', metavar='COLUMN', help='Column of CSV to treat as filename for input, number (1-based) or name of column')
    parser.add_argument('--input_csv', metavar='FILE', help='CSV file to use for reading input')
    args = parser.parse_args()
    if args.openai_api_key is None:
        args.openai_api_key = os.getenv('OPENAI_API_KEY')
    if args.togetherai_api_key is None:
        args.togetherai_api_key = os.getenv('TOGETHERAI_API_KEY')
    formats = 0
    formats += 1 if args.input_text is not None else 0
    formats += 1 if args.input_filename is not None else 0
    formats += 1 if args.input_column is not None else 0
    formats += 1 if args.input_column_filename is not None else 0
    if formats != 1:
        raise RuntimeError('Must specify exactly 1 format out of --input_text, --input_filename, --input_column, --input_column_filename')
    csv_formats = 0
    csv_formats += 1 if args.input_column is not None else 0
    csv_formats += 1 if args.input_column_filename is not None else 0
    if csv_formats > 0 and args.input_csv is None:
        raise RuntimeError('Missing CSV input file, specify wity --input_csv option.')
    print(args)

if __name__ == '__main__':
    main()

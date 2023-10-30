import argparse
import dotenv
import jinja2
import openai
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

def get_prompt(args):
    ''' Get prompt template for query '''
    if args.prompt_text is not None:
        return args.prompt_text
    if args.prompt_file is not None:
        with open(args.prompt_file, 'rt') as fin:
            contents = fin.read()
            return contents

env = jinja2.Environment()

def fill_prompt(prompt, values):
    ''' Fill in prompt template with values '''
    template = env.from_string(prompt)
    return template.render(values)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--openai_api_key', metavar='KEY', help='You API key for OpenAI. Can also be set with environment variable OPENAI_API_KEY.')
    parser.add_argument('--togetherai_api_key', metavar='KEY', help='You API key for together.ai. Can also be set with environment variable TOGETHERAI_API_KEY.')
    parser.add_argument('--input_text', metavar='TEXT', nargs='*', help='Direct text(s) to treat as an input (will use template key "input")')
    parser.add_argument('--input_filename', metavar='FILE', nargs='*', help='Filename(s) for text to treat as an input (will use template key "input")')
    parser.add_argument('--input_parquet', metavar='FILE', help='Parquet file to use for reading input (template keys are column names)')
    parser.add_argument('--prompt_text', metavar='TEXT', help='Prompt text to use for query (Jinja2 syntax)')
    parser.add_argument('--prompt_file', metavar='FILE', help='Prompt file to use for query (Jinja2 syntax)')
    args = parser.parse_args()
    if args.openai_api_key is None:
        args.openai_api_key = os.getenv('OPENAI_API_KEY')
    if args.togetherai_api_key is None:
        args.togetherai_api_key = os.getenv('TOGETHERAI_API_KEY')
    openai.api_key = args.openai_api_key
    formats = 0
    formats += 1 if args.input_text is not None else 0
    formats += 1 if args.input_filename is not None else 0
    formats += 1 if args.input_parquet is not None else 0
    if formats != 1:
        raise RuntimeError('Must specify exactly 1 input format out of --input_text, --input_filename, --input_parquet')
    count = 0
    prompt = get_prompt(args)
    for values in get_input_texts(args):
        query = fill_prompt(prompt, values)
        print(f'input: {count}\n{query}')
        if count < 3:
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
            answer = completion.choices[0].message.content
            print(f'answer:\n{answer}')
        else:
            break
        count += 1

if __name__ == '__main__':
    main()

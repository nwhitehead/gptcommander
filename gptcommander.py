import argparse

from dotenv import load_dotenv

load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--API_KEY', help='You API key for OpenAI or together.ai')
    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()

# GPT Commander

GPT Commander is a command line interface for making API calls to LLMs like OpenAI `gpt-3.5.turbo` in a systematic way.

Supports OpenAI API and together.ai. [TODO]

The typical use case is you have one or more CSV files that contain lists of filenames to process, prompt templates,
lists of fields to fill into prompt templates, or other information. You can use GPT Commander to iterate through
a CSV file of information and repeatedly call an API to get responses. Output can be directed to the existing CSV file,
a new CSV file, or to new individual files per response.

A simple example is you have a CSV file that contains information about books. Each row has a book title, author name,
short synopsis, and date of publication. You would like to add a column with "suggested genre". You want to call gpt-3.5
on each title and synopsis and ask it what the genre of the book should be. You write your prompt template in a separate
file using Jinja2 syntax. You then call GPT Commander with appropriate arguments to do all the work.

Note that you need your own API keys for OpenAI and together.ai.


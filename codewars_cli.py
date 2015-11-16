#!/usr/bin/env python
from CodeWarsSession import CodeWarsSession, pretty_print_response
import argparse
import json
import os


SUBMIT = 'submit'
GET = 'get'
FINALIZE = 'finalize'

RANDOM = 'random'
CURRENT = 'current'

# temporary stuff cause I'm not to sure how I want to handle this
problem_directory = "codewarsdata"
if not os.path.exists(problem_directory):
    os.makedirs(problem_directory)

current_code_file = os.path.join(problem_directory, "current_code.py")
current_problem = os.path.join(problem_directory, "current_problem.md")


def submit_code(session):
    with open(current_code_file, "r") as current_code:
        code = current_code.read()

    submition = session.submit_challege(code)
    pretty_print_response(submition)
    return submition["reason"]


def get_random_problem(session):
    print(session)
    return


def get_current_problem(session):
    """
        Gets the current kata and...writes it to a file?
    """
    with open(current_code_file, "w+") as current_code:
        current_code.write(session.current_challenge.session.code)

    with open(current_problem, "w+") as problem_description:
        problem_description.write(session.current_challenge.description)



def finalize_code(session):
    print(session)
    return

if __name__ == '__main__':
    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    api_secret = settings["api_secret"]
    session = CodeWarsSession(api_secret)
    # print(session.current_challenge)
    # session.start_specific_challenge("text-align-justify", "python")

    parser = argparse.ArgumentParser(description='Do some code shit')
    parser.add_argument('all_args', metavar='action', type=str, nargs="+", help='Do something')
    parser.add_argument('-l', '--language', metavar='language', type=str,  help='language of all action')
    # parser.add_argument('other', metavar='other', type=str, help='Do more things something')

    args = parser.parse_args()
    all_args = args.all_args
    action = all_args[0]

    if action == SUBMIT:
        print(submit_code(session))
    elif action == FINALIZE:
        finalize_code(session)
    elif action == GET:
        if len(all_args) == 1:
            get_current_problem(session)

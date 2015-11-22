#!/usr/bin/env python
# from CodeWarsSession import CodeWarsSession, pretty_print_response
import codewarsapi
import argparse
import json
import os

ACTION_KEY = 'action'

SUBMIT = 'submit'
START = 'start'
TEST = 'test'

# temporary stuff cause I'm not to sure how I want to handle this
problem_directory = "codewarsdata"
if not os.path.exists(problem_directory):
    os.makedirs(problem_directory)

current_code_file = os.path.join(problem_directory, "current_code.py")
current_problem = os.path.join(problem_directory, "current_problem.md")
current_problem = os.path.join(problem_directory, "test_fixtures.py")


class CodeWarsCli:
    def __init__(self, settings):
        api_secret = settings["api_secret"]
        self.session = CodeWarsSession(api_secret)
        self.parser = self.setup_cli_interface()

    def setup_cli_interface(self):
        parser = argparse.ArgumentParser(description='Do some code shit')
        subparser = parser.add_subparsers(dest=ACTION_KEY, help="does some shit and stuff")

        start_parser = subparser.add_parser("start", help="start stuff")
        start_parser.add_argument("language", metavar='language', help="Do somthign")
        start_parser.add_argument("strategy", metavar='strategy', help="Pick strategy", nargs='?', default="default")
        start_parser.add_argument("-i", "--id", metavar='id', help="Pick by id")

        submit_parser = subparser.add_parser("submit", help="submit stuff")
        submit_parser.add_argument("file", metavar='file', help="Pick file", nargs='?', default=None)
        submit_parser.add_argument("session", metavar='session_file', help="Specify solution_id", nargs='?',
                                   default=None)
        # test_parser = subparser.add_parser("test", help="test stuff")

        return parser

    def run(self):
        args = self.parser.parse_args()
        if args.action == START:
            self.start(args)
        elif args.action == SUBMIT:
            self.submit(args)
        elif args.action == TEST:
            self.test(args)

    def submit_current_challenge(self):
        return self.submit_code(current_code_file)

    def submit_code(self, codefile, finalize=False):
        code = self.read_code_file(codefile)
        self.session.change_current_code(code)  # this is simulating saving in the sublime text editor

        # TODO: we should be able ti differentiate between current challenge and other ones
        submission = self.session.submit_current_challenge()
        pretty_print_response(submission)
        return submission

    def get_random_problem(self):
        print(self.session)
        return

    def read_code_file(self, codefile):
        with open(codefile, "r") as current_code:
            code = current_code.read()

        return code

    def get_current_problem(self, session):
        """
            Gets the current kata and...writes it to a file?
        """
        with open(current_code_file, "w+") as current_code:
            current_code.write(session.current_challenge.session.code)

        with open(current_problem, "w+") as problem_description:
            problem_description.write(session.current_challenge.description)

        with open(current_problem, "w+") as problem_description:
            problem_description.write(session.current_challenge.description)

    def finalize_code(self, session):
        print(session)
        return

    def start(self, args):
        return

    def submit(self, args):
        if args.file is None and args.session is None:
            output = self.submit_current_challenge()
            print(output)
        else:
            print("not supported yet")

    def test(self, args):
        return


if __name__ == '__main__':
    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    cli = CodeWarsCli(settings)
    cli.run()
    # api_secret = settings["api_secret"]
    # session = CodeWarsSession(api_secret)
    # print(session.current_challenge)
    # session.start_specific_challenge("text-align-justify", "python")

    # parser = argparse.ArgumentParser(description='Do some code shit')
    # subparser = parser.add_subparsers(help="does some shit and stuff")

    # start_parser = subparser.add_parser("start", help="start stuff")
    # start_parser.add_argument("language", metavar='language', help="Do somthign")
    # start_parser.add_argument("strategy", metavar='strategy', help="Pick strategy", nargs='?', default="default")
    # start_parser.add_argument("-i", "--id", metavar='id', help="Pick by id")

    # submit_parser = subparser.add_parser("submit", help="submit stuff")
    # submit_parser.add_argument("file", metavar='file', help="Pick file", nargs='?', default=None)
    # submit_parser.add_argument("session", metavar='session_file', help="Specify solution_id", nargs='?', default=None)


    # test_parser = subparser.add_parser("test", help="test stuff")
    # # parser.add_argument('all_args', metavar='action', type=str, nargs="+", help='Do something')
    # # parser.add_argument('-l', '--language', metavar='language', type=str,  help='language of all action')
    # # parser.add_argument('other', metavar='other', type=str, help='Do more things something')

    # args = parser.parse_args()
    # print(args)
    # all_args = args.all_args
    # action = all_args[0]
    # other_args = all_args[1:]

    # if action == START:
    #     start(other_args)
    # elif action == SUBMIT:
    #     submit(other_args)
    # elif action == TEST:
    #     test(other_args)


# parser = argparse.ArgumentParser(prog='PROG')
# parser.add_argument('--foo', action='store_true', help='foo help')
# subparsers = parser.add_subparsers(help='sub-command help')
#
# # create the parser for the "a" command
# parser_a = subparsers.add_parser('a', help='a help')
# parser_a.add_argument('bar', type=int, help='bar help')
#
# # create the parser for the "b" command
# parser_b = subparsers.add_parser('b', help='b help')
# parser_b.add_argument('--baz', choices='XYZ', help='baz help')
"""
Command line spec
codewars_cli get

codewars_cli start <language>                 # start with next code challenge
codewars_cli start <language> -i <id_or_slug> # start specific challenge
codewars_cli start <language> <strategy>

codewars_cli submit          # submit (what we think) is your current solution for your current session
codewars_cli submit <file>   # submit a specific file to your current session
codewars_cli submit <file> <session_file>   # uses the session file (a json file) to extract a top level project_id
                                               # and solution id to submit the current file


codewars_cli test
codewars_cli test <file>

"""

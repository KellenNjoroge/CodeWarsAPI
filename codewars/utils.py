import sublime
import sublime_plugin
import os
import textwrap

from ..codewarsapi import consts

LANGAUGE_SYNTAX_STRING = "Packages/{}/{}.sublime-syntax"

# TODO: Eh? kindof clunky but sublime has a weird mix of UPPERCASE, camalCase,
# symbols etc but the api is all lowercase no symbols
SYNTAX_MAP = {
    "Python": consts.Languages.PYTHON,
    "C++": consts.Languages.CPP,
    "Ruby": consts.Languages.RUBY
}

LANGUAGES = list(SYNTAX_MAP.keys())


def show_quick_panel(window, item_list, on_done):
    flags = 0
    if int(sublime.version()) >= 3070:
        flags = sublime.KEEP_OPEN_ON_FOCUS_LOST

    return window.show_quick_panel(item_list, on_done, flags)


def build_langauge_syntax_str(language):
    return LANGAUGE_SYNTAX_STRING.format(language, language)


def get_settings():
    return sublime.load_settings("codewars.sublime-settings")


def get_database_file():
    # TODO: figure out where to store the data file
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data.db")


def set_syntax(view, language):
    syntax = build_langauge_syntax_str(language)
    view.set_syntax_file(syntax)


def split_lines(full_string, comment_char, length=100):
    """Split the string into lines of length. Uses newline to delimt lines
    """
    length_sans_comment_space = length - (len(comment_char) + 1)

    lines = textwrap.fill(full_string, width=length_sans_comment_space,
                          replace_whitespace=False)

    # Strip out trainling whitespace and join everything together
    return "\n".join([(comment_char + "{}".format(i)).strip() for i in lines.split("\n")])


def split_lines_to_length(full_string, length=100, join_char="<br>"):
    """Split the string into lines of length. Uses newline to delimt lines
    """
    lines = textwrap.fill(full_string, width=length,
                          replace_whitespace=False)

    # Strip out trainling whitespace and join everything together
    return join_char.join(["{}".format(i).strip() for i in lines.split("\n")])


def get_comment_start(view):
    shell_vars = view.meta_info("shellVariables", 0)
    comment_str = [x["value"] for x in shell_vars if x["name"] == "TM_COMMENT_START"]
    if len(comment_str) != 1:
        return "! "

    return comment_str[0]


def insert_challenge(window, language, challenge):
    description  = challenge.description
    code  = challenge.session.code
    test_fixtures = challenge.session.exampleFixture

    new_view = window.new_file()
    new_view.run_command('insert_test_fixture', {'language': language,
                                                 'test_fixture': test_fixtures})

    new_view = window.new_file()
    new_view.run_command('insert_problem_view', {'language': language,
                                                 'description': description,
                                                 'code': code})

import sublime
import sublime_plugin

from pprint import pprint

from .codewarsapi import codewarssession


example_comments_shell_var = [
    {'name': 'TM_COMMENT_DISABLE_INDENT_2', 'value': 'yes'},
    {'name': 'TM_COMMENT_END_2', 'value': '*/'},
    {'name': 'TM_COMMENT_START', 'value': '// '},
    {'name': 'TM_COMMENT_START_2', 'value': '/*'}
]

# TODO: Do reloading of module like here
# https://github.com/wbond/package_control/blob/master/1_reloader.py#L61-L214
# or just install this packages
# https://packagecontrol.io/packages/Package%20Reloader

# def build_comment_data(view, pt):
#     shell_vars = view.meta_info("shellVariables", pt)
#     pprint(shell_vars)
#     if not shell_vars:
#         return ([], [])

#     # transform the list of dicts into a single dict
#     all_vars = {}
#     for v in shell_vars:
#         if 'name' in v and 'value' in v:
#             all_vars[v['name']] = v['value']
#     pprint(all_vars)
#     line_comments = []
#     block_comments = []

#     # transform the dict into a single array of valid comments
#     suffixes = [""] + ["_" + str(i) for i in range(1, 10)]
#     pprint(suffixes)
#     for suffix in suffixes:
#         pprint("===")
#         pprint(suffix)
#         start = all_vars.setdefault("TM_COMMENT_START" + suffix)
#         end = all_vars.setdefault("TM_COMMENT_END" + suffix)
#         pprint(start)
#         pprint(end)
#         pprint("===")
#         disable_indent = all_vars.setdefault("TM_COMMENT_DISABLE_INDENT" + suffix)

#         if start and end:
#             block_comments.append((start, end, disable_indent == 'yes'))
#             block_comments.append((start.strip(), end.strip(), disable_indent == 'yes'))
#         elif start:
#             line_comments.append((start, disable_indent == 'yes'))
#             line_comments.append((start.strip(), disable_indent == 'yes'))

#     return (line_comments, block_comments)


class InsertProblemViewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        session = codewarssession.CodeWarsSession("njmsK1W3CppGFmvmzxUZ")

        # spawn a thread that will make a request and notify the request
        # was done. For now block!
        session.start_next_challenge("python")
        challenge = session.current_challenge
        pprint(challenge)
        self.view.insert(edit, 0, challenge.description)
        self.view.set_syntax_file("Packages/Python/Python.sublime-syntax")
        pprint(self.view.settings().get('syntax'))


class TestingCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('toggle_comment')
        pprint(self.view.settings().get('syntax'))


class CodewarsCommand(sublime_plugin.WindowCommand):

    def run(self, *args):
        window = self.window
        new_view = window.new_file()
        new_view.run_command('insert_problem_view')

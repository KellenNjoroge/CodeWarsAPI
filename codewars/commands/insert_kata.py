from .. import utils

import markdown
import sublime
import sublime_plugin


class InsertProblemViewCommand(sublime_plugin.TextCommand):
    def insert_description_as_comments(self, view, edit, description, location=0):
        comment_str = utils.get_comment_start(self.view)
        lines = utils.split_lines(description, comment_str)
        self.view.insert(edit, location, lines)

        return location + len(lines)

    def insert_description(self, view, edit, description, location=0):
        html = markdown.markdown(description)
        lines = utils.split_lines_to_length(html)
        formated_description = "<body style=\"background-color: #101010\">{}</body>".format(lines)
        self.phantom_set.update([sublime.Phantom(sublime.Region(0, 0),
                                                 formated_description,
                                                 sublime.LAYOUT_INLINE)])

    def run(self, edit, language, description, code):
        self.phantom_set = sublime.PhantomSet(self.view)

        # set syntax first as we will need the comment string
        utils.set_syntax(self.view, language)
        self.insert_description(self.view, edit, description)

        code = "\n\n" + code
        self.view.insert(edit, 0, code)


class InsertTestFixtureCommand(sublime_plugin.TextCommand):
    def run(self, edit, language, test_fixture):
        self.view.insert(edit, 0, test_fixture)
        utils.set_syntax(self.view, language)

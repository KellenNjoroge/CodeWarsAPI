from .. import api_threads
from .. import utils
from pprint import pprint

import sublime
import sublime_plugin


class SubmitProblemCommand(sublime_plugin.TextCommand):
    def run(self, edit, finalize=False):
        code = self.view.substr(sublime.Region(0, self.view.size()))
        pprint(code)

        settings = utils.get_settings()
        api_key = settings.get('api_key')
        self.finalize = finalize
        self.session_thread = api_threads.SubmitKataThread(api_key, utils.get_database_file(), code,
                                                           finalize)
        self.session_thread.start()
        sublime.set_timeout(lambda: self.handle_threads())

    def handle_threads(self):
        if not self.session_thread.isAlive() and self.session_thread.result is None:
            return

        if self.session_thread.result is None:
            sublime.set_timeout(lambda: self.handle_threads(), 1000)
            return

        print("done? Reustl is {}" % self.session_thread.result)

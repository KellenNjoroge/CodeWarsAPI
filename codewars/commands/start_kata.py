from .. import utils

from .. import api_threads
import sublime
import sublime_plugin


class StartKataCommand(sublime_plugin.WindowCommand):
    def run(self, *args):
        self.show_options()
        self.retries = 10

    def select_language(self, index):
        code_wars_language = utils.SYNTAX_MAP[utils.LANGUAGES[index]]
        self.language = utils.LANGUAGES[index]
        settings = utils.get_settings()

        api_key = settings.get('api_key')
        if api_key is None:
            return

        self.session_thread = api_threads.StartKataThread(api_key, utils.get_database_file(),
                                                          code_wars_language)

        self.session_thread.start()
        sublime.set_timeout(lambda: self.handle_threads())

    def show_options(self):
        utils.show_quick_panel(self.window, utils.LANGUAGES, self.select_language)

    def handle_threads(self):
        if self.retries > 10:
            return
        elif not self.session_thread.isAlive() and self.session_thread.result is None:
            return

        if self.session_thread.result is None:
            sublime.set_timeout(lambda: self.handle_threads(), 1000)
            return

        # Remember project and solution id for submission later
        print("INserting")
        utils.insert_challenge(self.window, self.language, self.session_thread.result)

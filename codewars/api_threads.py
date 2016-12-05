from ..codewarsapi import codewarssession

import threading
import logging


class CodeWarsApiCall(threading.Thread):
    def __init__(self, api_key, data_file):
        self.session = codewarssession.CodeWarsSession(api_key, data_file)
        self.result = None
        threading.Thread.__init__(self)

    def call_api(self, function, *args):
        try:
            self.result = function(*args)
        except Exception:
            # timed out or the api failed. Let the caller handler a None result
            logging.exception("Something awful happened!")
            logging.exception("Something awful happened!")


class StartKataThread(CodeWarsApiCall):
    def __init__(self, api_key, data_file, language):
        super().__init__(api_key, data_file)
        self.language = language

    def run(self):
        return super().call_api(self.session.start_challenge, self.language)


class SubmitKataThread(CodeWarsApiCall):
    def __init__(self, api_key, data_file, code, finalize):
        super().__init__(api_key, data_file)
        self.code = code
        self.finalize = finalize

    def run(self):
        if self.finalize:
            logging.log(1, "Here")
            x = super().call_api(self.session.finalize_kata, self.code)
            logging.log(1, "There")
        else:
            x = super().call_api(self.session.submit_kata, self.code)

        return x

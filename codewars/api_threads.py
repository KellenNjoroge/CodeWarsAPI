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


class StartKataThread(CodeWarsApiCall):
    def __init__(self, api_key, data_file, language):
        super().__init__(api_key, data_file)
        self.language = language

    def run(self):
        return super().call_api(self.session.start_challenge, self.language)


class SubmitKataThread(CodeWarsApiCall):
    def __init__(self, api_key, data_file, code):
        super().__init__(api_key, data_file)
        self.code = code

    def run(self):
        x = super().call_api(self.session.submit_challenge, self.code)
        return x

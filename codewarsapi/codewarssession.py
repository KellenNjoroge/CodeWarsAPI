from .codewarsapi import CodeWarsAPI
import json
import time
import os.path
import sqlite3


SELECT_CURRENT_SESSION = "SELECT * FROM CurrentSession;"
INSERT_CURRENT_PROBLEM = "UPDATE CurrentSession SET projectId = ?, solutionId = ? "


def pretty_print_response(res):
    print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))


def run_fetch_query(data_base, query, args_tuple=()):
    """Runs a query and calls fetch all on them. Doesn't commit so can't be used for inserts
    """
    conn = sqlite3.connect(data_base)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    records = c.execute(query, args_tuple).fetchall()
    conn.close()
    return records


def run_insert_query(data_base, query, args_tuple=()):
    """Runs a query and calls fetch all on them. Doesn't commit so can't be used for inserts
    """
    conn = sqlite3.connect(data_base)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    print("Executing {} with {}".format(query, args_tuple))
    c.execute(query, args_tuple)
    conn.commit()
    conn.close()


class Session(object):

    def __init__(self, session_dict):
        self.read_session(session_dict)

    def read_session(self, session_dict):
        self.code = session_dict["code"]
        # Need an empty string
        if self.code is None:
            self.code = session_dict["setup"]

        self.exampleFixture = session_dict["exampleFixture"]
        self.projectId = session_dict["projectId"]
        self.setup = session_dict["setup"]
        self.solutionId = session_dict["solutionId"]

    def __str__(self):
        info_str = 'Session Object\n'
        info_str += "projectId: " + str(self.projectId) + "\n"
        info_str += "solutionId: " + str(self.solutionId) + "\n"
        info_str += "code: \n" + str(self.code) + "\n"
        info_str += "exampleFixture: \n" + str(self.exampleFixture) + "\n"
        info_str += "setup: \n" + str(self.setup) + "\n"
        return info_str


# TODO: Hide the internal objects and have everything accessed by the top level
# CodeWarsSession
class Challenge(object):

    def __init__(self, challenge_dict):
        self.read_challenge(challenge_dict)

    def read_challenge(self, challenge_dict):
        self.averageCompletion = challenge_dict["averageCompletion"]
        self.description = challenge_dict.get("description", None)
        self.href = challenge_dict.get("href", None)
        self.name = challenge_dict.get("name", None)
        self.rank = challenge_dict.get("rank", None)
        self.session = Session(challenge_dict.get("session", None))
        self.slug = challenge_dict.get("slug", None)
        self.tags = challenge_dict.get("tags", None)

    def __str__(self):
        info_str = ''
        info_str += "averageCompletion: " + str(self.averageCompletion) + "\n"
        info_str += "description: " + str(self.description) + "\n"
        info_str += "href: " + str(self.href) + "\n"
        info_str += "name: " + str(self.name) + "\n"
        info_str += "rank: " + str(self.rank) + "\n"
        info_str += "session: " + str(self.session) + "\n"
        info_str += "slug: " + str(self.slug) + "\n"
        info_str += "tags: " + str(self.tags) + "\n"
        return info_str


class CodeWarsUser(object):
    def __init__(self, user_dict):
        self.read_user_data(user_dict)

    def read_user_data(self, user_dict):
        self.skills = user_dict["skills"]
        self.honor = user_dict["honor"]

    def __str__(self):
        info_str = ''
        info_str += "Skills: " + str(self.skills) + "\n"
        info_str += "honor: " + str(self.honor) + "\n"
        info_str += "href: " + str(self.href) + "\n"
        info_str += "name: " + str(self.name) + "\n"
        info_str += "rank: " + str(self.rank) + "\n"
        info_str += "session: " + str(self.session) + "\n"
        info_str += "slug: " + str(self.slug) + "\n"
        info_str += "tags: " + str(self.tags) + "\n"
        return info_str


class CodeWarsSession(object):
    """
    Represents a persistent state
    """
    MAX_RETRIES = 10

    def __init__(self, api_secret, data_file):
        super(CodeWarsSession, self).__init__()
        self.api = CodeWarsAPI(api_secret)
        self.project_id = 0
        self.solution_id = 0
        self.data_file = data_file
        self.current_challenge = None
        self.load_current_session(self.data_file)

    def load_current_session(self, data_file):
        # TODO: Open sqlite database
        current_problem = run_fetch_query(data_file, SELECT_CURRENT_SESSION)[0]
        self.project_id = current_problem["projectId"]
        self.solution_id = current_problem["solutionId"]

    def insert_current_session(self, data_file):
        # TODO: Open sqlite database
        print("insert_current_ession")
        print(data_file)
        run_insert_query(self.data_file, INSERT_CURRENT_PROBLEM,
                         (self.project_id, self.solution_id))

    def init_tables(self, data_base):
        pass

    # TODO: save to sqlite database
    def __save_challenge(self, raw_kata):
        print("save")
        print(raw_kata)
        self.current_challenge = self.make_challenge(raw_kata)
        self.project_id = self.current_challenge.session.projectId
        self.solution_id = self.current_challenge.session.solutionId
        self.insert_current_session(self.data_file)

    def start_challenge(self, language, slug=None):
        """Start a random challenge."""
        if slug is None:
            kata = self.api.start_random_kata(language)
        else:
            kata = self.api.start_kata(slug, language)

        self.__save_challenge(kata)
        return self.current_challenge

    def submit_challenge(self, code):
        """submit the current problem and poll for the response"""
        submit_message = self.api.attempt_solution(self.project_id, self.solution_id, code)
        return self.process_submission(submit_message)

    def finalize_challege(self, code):
        """submit the current problem and poll for the response"""
        submit_message = self.api.finalize_solution(self.project_id, self.solution_id, code)
        return self.process_submission(submit_message)

    def process_submission(self, submit_message_response):
        if submit_message_response["success"]:
            return self.poll_defered(submit_message_response["dmid"])
        else:
            print("Someshit happend")
        return None

    def poll_defered(self, dmid):
        defferred_message = self.api.get_deferred(dmid)
        # give it a second to process it
        retries = 0
        while 'success' not in defferred_message and retries < self.MAX_RETRIES:
            time.sleep(.5)
            defferred_message = self.api.get_deferred(dmid)
            retries += 1

        return defferred_message

    def make_challenge(self, challenge_data_dict):
        return Challenge(challenge_data_dict)

    def __str__(self):
        info_str = ''
        return info_str


if __name__ == '__main__':

    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    api_secret = settings["api_secret"]
    session = CodeWarsSession(api_secret)
    session.start_next_challenge("javascript")

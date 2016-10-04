from codewarsapi import CodeWarsAPI
import json
import json_utils
import time
import os.path


def pretty_print_response(res):
    print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))


class Session(object):

    def __init__(self, session_dict):
        self.read_session(session_dict)

    def read_session(self, session_dict):
        self.code = session_dict["code"]
        self.example_fixture = session_dict["exampleFixture"]
        self.example_fixture = session_dict["exampleFixture"]
        self.project_id = session_dict["projectId"]
        self.setup = session_dict["setup"]
        self.solution_id = session_dict["solutionId"]

    def __str__(self):
        info_str = 'Session Object\n'
        info_str += "project_id: " + str(self.project_id) + "\n"
        info_str += "solution_id: " + str(self.solution_id) + "\n"
        info_str += "code: \n" + str(self.code) + "\n"
        info_str += "example_fixture: \n" + str(self.example_fixture) + "\n"
        info_str += "setup: \n" + str(self.setup) + "\n"
        return info_str


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
    """

    DEFAULT_DATA_FILE = "codewars_data.json"
    CURRENT_CHALLENGE = 'current_challenge'

    MAX_RETRIES = 10

    def __init__(self, api_secret, data_file=DEFAULT_DATA_FILE):
        super(CodeWarsSession, self).__init__()
        self.api = CodeWarsAPI(api_secret)
        self.data_file = data_file

        self.current_data = self.load_current_data(data_file)

        self.current_challenge = self.read_current_challenge(self.current_data)

    def load_current_data(self, data_file):
        if not os.path.isfile(data_file):
            return {}

        with open(data_file, 'r') as data:
            try:
                return json.load(data)
            except ValueError:
                return {}

    def __change_currrent_challenge__(self, raw_kata):
        self.current_challenge = self.make_challenge(raw_kata)
        self.current_data[self.CURRENT_CHALLENGE] = self.current_challenge
        self.write_current_data()

    def start_next_challenge(self, language, solution_file="current_solution"):
        """Start a random challenge."""
        kata = self.api.start_random_kata(language)
        self.__change_currrent_challenge__(kata)

    def start_challenge(self, slug, language):
        kata = self.api.start_kata(slug, language)
        self.__change_currrent_challenge__(kata)

    def write_current_data(self):
        with open(self.data_file, 'w') as outfile:
            json.dump(self.current_data, outfile, cls=json_utils.MyEncoder)

    def submit_current_challenge(self):
        return self.submit_challege(self.current_challenge.code,
                                    self.current_challenge.session.project_id,
                                    self.current_challenge.session.solution_id)

    def finalize_current_challenge(self):
        return self.finalize_challege(self.current_challenge.code,
                                      self.current_challenge.session.project_id,
                                      self.current_challenge.session.solution_id)

    def submit_challege(self, code, project_id, solution_id):
        """submit the current problem and poll for the response"""
        return self.submit(code, project_id, solution_id, False)

    def finalize_challege(self, code, project_id, solution_id):
        """submit the current problem and poll for the response"""
        return self.submit(code, project_id, solution_id, True)

    def submit(self, code, project_id, solution_id, finalize=False):
        if finalize:
            submit_message = self.api.attempt_solution(project_id, solution_id, code)
        else:
            submit_message = self.api.attempt_solution(project_id, solution_id, code)

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
        while 'success' not in defferred_message or \
                defferred_message["success"] == 'true' or \
                retries < self.MAX_RETRIES:

            time.sleep(.5)
            defferred_message = self.api.get_deferred(dmid)
            retries += 1

        return defferred_message

    def change_current_code(self, code):
        self.current_challenge.code = code

    def read_current_challenge(self, data):
        if self.CURRENT_CHALLENGE in data:
            return self.make_challenge(data["current_challenge"])
        return None

    def make_challenge(self, challenge_data_dict):
        return Challenge(challenge_data_dict)

    def __str__(self):
        info_str = ''
        info_str += "Current Challenge: " + str(self.current_challenge) + "\n"
        return info_str


if __name__ == '__main__':

    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    api_secret = settings["api_secret"]
    session = CodeWarsSession(api_secret)
    session.start_next_challenge("javascript")

"""
[X] GET https://www.codewars.com/api/v1/users/:id_or_username

[X] GET https://www.codewars.com/api/v1/code-challenges/:id_or_slug
[X] GET https://www.codewars.com/api/v1/deferred/:dmid

[X] POST https://www.codewars.com/api/v1/code-challenges/:language/train
[X] POST https://www.codewars.com/api/v1/code-challenges/:id_or_slug/:language/train
[X] POST https://www.codewars.com/api/v1/code-challenges/projects/:project_id/solutions/:solution_id/attempt
[X] POST https://www.codewars.com/api/v1/code-challenges/projects/:project_id/solutions/:solution_id/finalize
"""

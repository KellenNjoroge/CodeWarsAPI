from CodeWars import CodeWarsAPI
import json
import json_utils
import time


def pretty_print_response(res):
    print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))


class Session(object):

    def __init__(self, session_dict):
        self.read_session(session_dict)

    def read_session(self, session_dict):
        self.code = session_dict["code"]
        self.example_fixture = session_dict["example_fixture"]
        self.project_id = session_dict["project_id"]
        self.setup = session_dict["setup"]
        self.solution_id = session_dict["solution_id"]

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


class CodeWarsSession(object):

    """
    """

    DEFAULT_DATA_FILE = "codewars_data.json"
    CURRENT_CHALLENGE = 'current_challenge'

    def __init__(self, api_secret, data_file=DEFAULT_DATA_FILE):
        super(CodeWarsSession, self).__init__()
        self.api = CodeWarsAPI(api_secret)
        self.data_file = data_file

        self.current_data = self.load_current_data(data_file)

        self.current_challenge = self.read_current_challenge(self.current_data)

    def load_current_data(self, data_file):
        with open(data_file, 'r') as data:
            try:
                return json.load(data)
            except ValueError:
                return {}

    def start_next_challenge(self, language, solution_file="current_solution"):
        """Start a random challenge."""
        kata = self.api.start_random_kata("python")
        pretty_print_response(kata)
        kata = self.make_challenge(kata)

    def start_specific_challenge(self, slug, language):
        kata = self.api.start_kata(slug, language)
        self.current_challenge = self.make_challenge(kata)
        self.current_data[self.CURRENT_CHALLENGE] = self.current_challenge

        self.write_current_data()

    def write_current_data(self):
        with open(self.data_file, 'w') as outfile:
            json.dump(self.current_data, outfile, cls=json_utils.MyEncoder)

    def submit_challege(self, code):
        """submit the current problem and poll for the response"""
        submit_message = self.api.attempt_solution(self.current_challenge.session.project_id,
                                                   self.current_challenge.session.solution_id,
                                                   code)

        if submit_message["success"]:
            defferred_message = self.api.get_deferred(submit_message["dmid"])
            # give it a second to process it
            time.sleep(1)
            while 'success' not in defferred_message or \
                    defferred_message["success"] == 'true':
                defferred_message = self.api.get_deferred(submit_message["dmid"])
                time.sleep(.5)

            return defferred_message

        else:
            print("Someshit happend")
        return None

    def read_current_challenge(self, data):
        if self.CURRENT_CHALLENGE in data:
            return self.make_challenge(data["current_challenge"])
        return None

    # def print_challenge(self):
    #     print

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

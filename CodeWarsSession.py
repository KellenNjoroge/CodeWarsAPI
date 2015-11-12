from CodeWars import CodeWarsAPI, CodeWarsConsts
import json


def pretty_print_response(res):
    print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))


class Session(object):

    def __init__(self, session_dict):
        self.read_session(session_dict)

    def read_session(self, session_dict):
        self.code = session_dict["code"]
        self.example_fixture = session_dict["exampleFixture"]
        self.project_id = session_dict["projectId"]
        self.setup = session_dict["setup"]
        self.solution_id = session_dict["solutionId"]


class Challenge(object):

    def __init__(self, challenge_dict):
        self.read_challenge(challenge_dict)

    def read_challenge(self, challenge_dict):
        self.averageCompletion = challenge_dict["averageCompletion"]
        self.description = challenge_dict["description"]
        self.href = challenge_dict["href"]
        self.name = challenge_dict["name"]
        self.rank = challenge_dict["rank"]
        self.session = Session(challenge_dict["session"])
        self.slug = challenge_dict["slug"]
        self.tags = challenge_dict["tags"]


class CodeWarsSession(object):

    """
    """

    def __init__(self):
        CodeWars.CodeWars()
        super(CodeWarsSession, self).__init__()


if __name__ == '__main__':

    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    api_secret = settings["api_secret"]

    codewars = CodeWarsAPI(api_secret)
    blah = codewars.peek_random_kata("python")
    pretty_print_response(blah)

"""
[X] GET https://www.codewars.com/api/v1/users/:id_or_username

[X] GET https://www.codewars.com/api/v1/code-challenges/:id_or_slug
[X] GET https://www.codewars.com/api/v1/deferred/:dmid

[X] POST https://www.codewars.com/api/v1/code-challenges/:language/train
[X] POST https://www.codewars.com/api/v1/code-challenges/:id_or_slug/:language/train
[X] POST https://www.codewars.com/api/v1/code-challenges/projects/:project_id/solutions/:solution_id/attempt
[X] POST https://www.codewars.com/api/v1/code-challenges/projects/:project_id/solutions/:solution_id/finalize
"""

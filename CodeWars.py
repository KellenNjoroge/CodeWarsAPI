import requests as req
import json
import time

BASE_URL = "https://www.codewars.com/api/v1"
BASE_CODE_CHALLENGE_URL = "/".join((BASE_URL, "code-challenges"))
BASE_ATTEMPT_URL = "/".join((BASE_CODE_CHALLENGE_URL, "projects", "{}", "solutions", "{}"))

GET_USER = "/".join((BASE_URL, "users", "{}"))
GET_CHALLENGE = "/".join((BASE_URL, "code-challenges", "{}"))
GET_DEFERRED = "/".join((BASE_URL, "deferred", "{}"))

POST_RANDOM_TRAINING = "/".join((BASE_CODE_CHALLENGE_URL, "{}", "train"))
POST_TRAINING = "/".join((BASE_CODE_CHALLENGE_URL, "{}", "{}", "train"))
POST_ATTEMPT = "/".join((BASE_ATTEMPT_URL,  "attempt"))
POST_FINALIZE = "/".join((BASE_ATTEMPT_URL, "finalize"))


def post_request(url, headers={}, data={}):
    print(url)
    r = req.post(url, headers=headers, data=data, json="")
    return return_requst(r)


def get_request(url, headers={}):
    r = req.get(url, headers=headers)
    return return_requst(r)


def return_requst(response):
    if(response.status_code == req.codes.ok):
        return response.json()

    print("Something happened")
    print(response.headers)
    print(response.status_code)
    print(response.text)


class CodeWars(object):

    """"""

    def __init__(self, api_secret):
        self.api_secret = api_secret
        self.headers = {'Authorization': api_secret}

    def get_user(self, user):
        get_user_url = GET_USER.format(user)
        return get_request(get_user_url, self.headers)

    def train_next(self, language, strategy="random", peek=False):
        challenge_url = POST_RANDOM_TRAINING.format(language)

        data = {
            "strategy": strategy,
            "peek": peek
        }

        return post_request(challenge_url, headers=self.headers, data=data)

    def start_random_kata(self, language):
        return self.train_next(language)

    def peek_random_kata(self, language):
        return self.train_next(language, peek=True)

    def start_kata(self, id, language):
        challenge_url = POST_TRAINING.format(id, language)
        kata = post_request(challenge_url, self.headers)

        return kata

    def attempt_solution(self, project_id, solution_id, solution):
        attempt_url = POST_ATTEMPT.format(project_id, solution_id)
        data = {
            "code": solution
        }
        return post_request(attempt_url, self.headers, data=data)

    def finalize_solution(self, project_id, solution_id, solution):
        finalize_url = POST_FINALIZE.format(project_id, solution_id)
        data = {
            "code": solution
        }
        return post_request(finalize_url, self.headers, data=data)

    def request_user(self, user):
        get_user_url = GET_USER.format(user)
        return get_request(get_user_url, self.headers)

    def get_deferred(self, dmid):
        deferred_url = GET_DEFERRED.format(dmid)
        return get_request(deferred_url, self.headers)

    def parse_training_response(self, response):
        print("balh")

if __name__ == '__main__':

    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    api_secret = settings["api_secret"]

    codewars = CodeWars(api_secret)
    # blah = codewars.peek_random_kata("python")
    # blah = codewars.start_kata("557b5e0bddf29d861400005d", "python")

    project_id = "563c52f043d4362044000038"
    solution_id = "563c52f043d436204400003a"

    with open('solution.py') as f:
        solution = f.read()

    blah = codewars.attempt_solution(project_id, solution_id, solution)

    print(json.dumps(blah, sort_keys=True, indent=4, separators=(',', ': ')))

    # dmid = "Bb7FP7W7"
    dmid = blah["dmid"]

    time.sleep(1)

    blah_blah = codewars.get_deferred(dmid)

    print(json.dumps(blah_blah, sort_keys=True, indent=4, separators=(',', ': ')))

    blah_blah_blah = codewars.finalize_solution(project_id, solution_id, solution)
    dmid = blah["dmid"]

    time.sleep(1)

    blah_blah = codewars.get_deferred(dmid)
    print(json.dumps(blah_blah, sort_keys=True, indent=4, separators=(',', ': ')))

"""
GET https://www.codewars.com/api/v1/users/:id_or_username
GET https://www.codewars.com/api/v1/code-challenges/:id_or_slug
GET https://www.codewars.com/api/v1/deferred/:dmid

POST https://www.codewars.com/api/v1/code-challenges/:language/train
POST https://www.codewars.com/api/v1/code-challenges/:id_or_slug/:language/train
POST https://www.codewars.com/api/v1/code-challenges/projects/:project_id/solutions/:solution_id/attempt
POST https://www.codewars.com/api/v1/code-challenges/projects/:project_id/solutions/:solution_id/finalize
"""

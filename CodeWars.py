import requests as req
import json

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


with open('settings.json') as settings_file:
    settings = json.load(settings_file)


api_secret = settings["api_secret"]

headers = {
    'Authorization': api_secret
}


def return_requst(response):
    if(response.status_code == req.codes.ok):
        return response.json()

    print("Something happened")
    print(response.headers)
    print(response.status_code)
    print(response.text)


def get_request(url, headers={}):
    r = req.get(url, headers=headers)
    return return_requst(r)


def post_request(url, headers={}, data={}):
    print(url)
    r = req.post(url, headers=headers, data=data, json="")
    return return_requst(r)


def get_user(user):
    get_user_url = GET_USER.format(user)
    return get_request(get_user_url, headers)


def train_next(language, strategy="random", peek=False):
    challenge_url = POST_RANDOM_TRAINING.format(language)

    data = {
        "strategy": strategy,
        "peek": peek
    }

    return post_request(challenge_url, headers=headers, data=data)


def start_random_challenge(language):
    return train_next(language)


def peek_random_challenge(language):
    return train_next(language, peek=True)


def request_user(user):
    get_user_url = GET_USER.format(user)
    return get_request(get_user_url, headers)


def request_(user):
    get_user_url = GET_USER.format(user)
    return get_request(get_user_url, headers)


blah = peek_random_challenge("python")

print(json.dumps(blah, sort_keys=True, indent=4, separators=(',', ': ')))


"""
GET https://www.codewars.com/api/v1/users/:id_or_username
GET https://www.codewars.com/api/v1/code-challenges/:id_or_slug
GET https://www.codewars.com/api/v1/deferred/:dmid

POST https://www.codewars.com/api/v1/code-challenges/:language/train
POST https://www.codewars.com/api/v1/code-challenges/:id_or_slug/:language/train
POST https://www.codewars.com/api/v1/code-challenges/projects/:project_id/solutions/:solution_id/attempt
POST https://www.codewars.com/api/v1/code-challenges/projects/:project_id/solutions/:solution_id/finalize
"""

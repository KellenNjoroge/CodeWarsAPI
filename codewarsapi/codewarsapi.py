import requests as req
from .consts import Languages
from pprint import pprint

BASE_URL = "https://www.codewars.com/api/v1"
BASE_CODE_CHALLENGE_URL = "/".join((BASE_URL, "code-challenges"))
BASE_ATTEMPT_URL = "/".join((BASE_CODE_CHALLENGE_URL, "projects", "{}", "solutions", "{}"))

GET_USER = "/".join((BASE_URL, "users", "{}"))
GET_CHALLENGE = "/".join((BASE_URL, "code-challenges", "{}"))
GET_DEFERRED = "/".join((BASE_URL, "deferred", "{}"))

POST_RANDOM_TRAINING = "/".join((BASE_CODE_CHALLENGE_URL, "{}", "train"))
POST_TRAINING = "/".join((BASE_CODE_CHALLENGE_URL, "{}", "{}", "train"))
POST_ATTEMPT = "/".join((BASE_ATTEMPT_URL, "attempt"))
POST_FINALIZE = "/".join((BASE_ATTEMPT_URL, "finalize"))


def post_request(url, headers={}, data={}):
    # TODO: Put in try catch
    r = req.post(url, headers=headers, data=data, timeout=4)
    return return_requst(r)


def get_request(url, headers={}):
    r = req.get(url, headers=headers, timeout=4)
    return return_requst(r)


def return_requst(response):
    pprint(response)
    pprint(response.json())
    if(response.status_code == req.codes.ok):
        return response.json()

    print("Shit broke")
    print(response.headers)
    print(response.status_code)
    print(response.text)
    return response.json()


class CodeWarsConsts(object):
    DEFAULT = "default"  # Selects challenges that are higher then your current rank. Also known as "Rank Up" Challenges
    RANDOM = "random"  # Randomly selected code challenges
    REFERENCE_WORKOUT = "reference_workout"  # Will select code challenges that are tagged as reference.
    BETA_WORKOUT = "beta_workout"  # Will select beta code challenges.
    RETRAIN_WORKOUT = "retrain_workout"  # Will focus on code challenges that you have already completed.
    ALGORITHM_RETEST = "algorithm_retest"  # Will focus on algorithm code challenges that you have already completed.
    KYU_8_WORKOUT = "kyu_8_workout"  # Will focus on 8 kyu code challenges.
    KYU_7_WORKOUT = "kyu_7_workout"  # Will focus on 7 kyu code challenges.
    KYU_6_WORKOUT = "kyu_6_workout"  # Will focus on 6 kyu code challenges.
    KYU_5_WORKOUT = "kyu_5_workout"  # Will focus on 5 kyu code challenges.
    KYU_4_WORKOUT = "kyu_4_workout"  # Will focus on 4 kyu code challenges.
    KYU_3_WORKOUT = "kyu_3_workout"  # Will focus on 3 kyu code challenges.
    KYU_2_WORKOUT = "kyu_2_workout"  # Will focus on 2 kyu code challenges.
    KYU_1_WORKOUT = "kyu_1_workout"  # Will focus on 1 kyu code challenges.
    PEEK          = "true"  # pass to training functions to only peek the function
    NO_PEEK       = "false"  # pass to training functions to start.

    def get_strategy_set():
        return set([
            CodeWarsConsts.DEFAULT,
            CodeWarsConsts.RANDOM,
            CodeWarsConsts.REFERENCE_WORKOUT,
            CodeWarsConsts.BETA_WORKOUT,
            CodeWarsConsts.RETRAIN_WORKOUT,
            CodeWarsConsts.ALGORITHM_RETEST,
            CodeWarsConsts.KYU_8_WORKOUT,
            CodeWarsConsts.KYU_7_WORKOUT,
            CodeWarsConsts.KYU_6_WORKOUT,
            CodeWarsConsts.KYU_5_WORKOUT,
            CodeWarsConsts.KYU_4_WORKOUT,
            CodeWarsConsts.KYU_3_WORKOUT,
            CodeWarsConsts.KYU_2_WORKOUT,
            CodeWarsConsts.KYU_1_WORKOUT
        ])

    def get_peek_set():
        return set([
            CodeWarsConsts.PEEK,
            CodeWarsConsts.NO_PEEK
        ])

    def get_langauge_set():
        return set([
            Languages.CPP,
            Languages.PYTHON
        ])


class CodeWarsAPI(object):

    """"""

    def __init__(self, api_secret):
        self.api_secret = api_secret
        self.headers = {'Authorization': api_secret}
        self.strategy_set = CodeWarsConsts.get_strategy_set()
        self.peek_set = CodeWarsConsts.get_peek_set()

    def attempt_solution(self, project_id, solution_id, solution):
        attempt_url = self._format_url(POST_ATTEMPT, project_id, solution_id)
        data = self._make_code_solution(solution)

        return post_request(attempt_url, self.headers, data=data)

    def finalize_solution(self, project_id, solution_id, solution):
        finalize_url = self._format_url(POST_FINALIZE, project_id, solution_id)
        data = self._make_code_solution(solution)

        return post_request(finalize_url, self.headers, data=data)

    def get_challenge(self, id_or_slug):
        get_challenge_url = self._format_url(GET_CHALLENGE, id_or_slug)
        return get_request(get_challenge_url, self.headers)

    def get_deferred(self, dmid):
        deferred_url = self._format_url(GET_DEFERRED, dmid)
        return get_request(deferred_url, self.headers)

    def get_user(self, user):
        get_user_url = self._format_url(GET_USER, user)
        return get_request(get_user_url, self.headers)

    def parse_training_response(self, response):
        raise NotImplemented("Should this be done in the api or the session layer?")

    def peek_random_kata(self, language):
        return self.train_next(language, peek=CodeWarsConsts.PEEK)

    def peek_kata(self, language, strategy):
        return self.train_next(language, strategy=strategy, peek=CodeWarsConsts.PEEK)

    def request_user(self, user):
        get_user_url = self._format_url(GET_USER, user)
        return get_request(get_user_url, self.headers)

    def start_kata(self, id, language):
        challenge_url = self._format_url(POST_TRAINING, id, language)
        kata = post_request(challenge_url, self.headers)

        return kata

    def start_random_kata(self, language):
        return self.train_next(language, strategy=CodeWarsConsts.RANDOM)

    def train_next(self, language, strategy=CodeWarsConsts.DEFAULT, peek=CodeWarsConsts.NO_PEEK):
        challenge_url = self._format_url(POST_RANDOM_TRAINING, language)
        data = self._make_random_training_data(strategy, peek)

        return post_request(challenge_url, headers=self.headers, data=data)

    def _check_peek(self, peek):
        if peek not in self.peek_set:
            raise Exception("Not a recognized peek value")

    def _check_strategy(self, strategy):
        if strategy not in self.strategy_set:
            raise Exception("Not a recognized strategy")

    def _format_url(self, base_url, *format_arguements):
        return base_url.format(*format_arguements)

    def _make_code_solution(self, solution):
        return {
            "code": solution
        }

    def _make_random_training_data(self, strategy, peek):
        # throw errors if invalid strategy or peek values
        self._check_strategy(strategy)
        self._check_peek(peek)

        return {
            "strategy": strategy,
            "peek": peek
        }

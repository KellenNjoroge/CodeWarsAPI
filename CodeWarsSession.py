from CodeWars import CodeWarsAPI, CodeWarsConsts
import json


def pretty_print_response(res):
    print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))


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

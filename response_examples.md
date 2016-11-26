#Requests Notes

##Get User
Gets info about a user

GET https://www.codewars.com/api/v1/users/:id_or_username

```bash
curl https://www.codewars.com/api/v1/users/etinlb
```
```json
{
    "username": "some_user",
    "name": "Some Person",
    "honor": 544,
    "clan": "some clan",
    "leaderboardPosition": 134,
    "skills": [
        "ruby",
        "c#",
        ".net",
        "javascript",
        "coffeescript",
        "nodejs",
        "rails"
    ],
    "ranks": {
        "overall": {
            "rank": -3,
            "name": "3 kyu",
            "color": "blue",
            "score": 2116
        },
        "languages": {
            "javascript": {
                "rank": -3,
                "name": "3 kyu",
                "color": "blue",
                "score": 1819
            },
            "ruby": {
                "rank": -4,
                "name": "4 kyu",
                "color": "blue",
                "score": 1005
            },
            "coffeescript": {
                "rank": -4,
                "name": "4 kyu",
                "color": "blue",
                "score": 870
            }
        }
    },
    "codeChallenges": {
        "totalAuthored": 3,
        "totalCompleted": 230
    }
}
```

##Get Challenge
Gets the info for a specific challenge

GET https://www.codewars.com/api/v1/code-challenges/:id_or_slug
```bash
curl "https://www.codewars.com/api/v1/code-challenges/valid-braces"
```
```json
{
    "id": "5277c8a221e209d3f6000b56",
    "name": "Valid Braces",
    "slug": "valid-braces",
    "category": "algorithms",
    "publishedAt": "2013-11-05T00:07:31Z",
    "approvedAt": "2013-12-20T14:53:06Z",
    "languages": [
        "javascript",
        "coffeescript"
    ],
    "url": "http://www.codewars.com/kata/valid-braces",
    "rank": {
        "id": -4,
        "name": "4 kyu",
        "color": "blue"
    },
    "createdBy": {
        "username": "xDranik",
        "url": "http://www.codewars.com/users/xDranik"
    },
    "approvedBy": "xDranik",
    "description": "Write a function called `validBraces` that takes a string of braces, and determines if the order of the braces is valid. `validBraces` should return true if the string is valid, and false if it's invalid.\n\nThis Kata is similar to the Valid Parentheses Kata, but introduces four new characters. Open and closed brackets, and open and closed curly braces. Thanks to @arnedag for the idea!\n\nAll input strings will be nonempty, and will only consist of open parentheses '(' , closed parentheses ')', open brackets '[', closed brackets ']', open curly braces '{' and closed curly braces '}'. \n\n<b>What is considered Valid?</b>\nA string of braces is considered valid if all braces are matched with the correct brace. <br/>\nFor example:<br/>\n'(){}[]' and '([{}])' would be considered valid, while '(}', '[(])', and '[({})](]' would be considered invalid.\n\n\n<b>Examples:</b> <br/>\n`validBraces( \"(){}[]\" )` => returns true <br/>\n`validBraces( \"(}\" )` => returns false <br/>\n`validBraces( \"[(])\" )` => returns false <br/>\n`validBraces( \"([{}])\" )` => returns true <br/>\n",
    "totalAttempts": 4911,
    "totalCompleted": 919,
    "totalStars": 12,
    "tags": [
        "Algorithms",
        "Validation",
        "Logic",
        "Utilities"
    ]
}
```

##Post Train Next Challenge
Gets a random challenge from your queue and starts training it.

POST https://www.codewars.com/api/v1/code-challenges/:language/train
```bash
curl "https://www.codewars.com/api/v1/code-challenges/javascript/train"
 -X POST \
 -H "Authorization: some-api-key"
```
| body input |      |
|------------|------|
| strategy   | The strategy to use for choosing what the next code challenge should be. (Optional) |
| peek       | Boolean - true if you only want to peek at the next item in your queue, without removing it from the queue or beginning a new training  session. |

```json
{
   "success":true,
   "name":"Anything to integer",
   "slug":"anything-to-integer",
   "description":"Your task is to program a function which converts any input to an integer.\n\nDo not perform rounding, the fractional part should simply be discarded.\n\nIf converting the input to an integer does not make sense (with an object, for instance), the function should return 0 (zero).\n\nAlso, Math.floor(), parseInt() and parseFloat() are disabled for your unconvenience.\n\nOnegaishimasu!",
   "author":"Jake Hoffner",
   "rank":-6,
   "averageCompletion":125.4,
   "tags":[
      "Fundamentals",
      "Integers",
      "Data Types",
      "Numbers"
   ],
   "session":{
       "projectId":"533f66fba0de5d94410001ec",
       "solutionId":"53bc968d35fd2feefd000004",
       "setup":"function toInteger(n) {\n  \n}",
       "exampleFixture":"Test.expect(toInteger(\"4.55\") === 4)",
       "code":null
   }
}
```

##Post Train Code Challenge
Start a training of a specific challenge. Same response as train next challenge

POST https://www.codewars.com/api/v1/code-challenges/:id_or_slug/:language/train
```bash
curl "https://www.codewars.com/api/v1/code-challenges/anything-to-integer/javascript/train"
```

##Post Attempt Solution
Post a solution

POST https://www.codewars.com/api/v1/code-challenges/projects/:project_id/solutions/:solution_id/attempt
```bash
curl "https://www.codewars.com/api/v1/code-challenges/projects/523f66fba0de5d94410001cb/solutions/53bc968d35fd2feefd000013/attempt" \
 -X POST \
 -d code=function(){//example code\n}\
 -H "Authorization: some-api-key"
```

| body input |      |
|------------|------|
| code       | The solution you are submitting as an attempt |

```json
{
   "success":true,
   "dmid":"4rsdaDf8d"
}
```


##Post Finalize Solution
Post a final solution. Only can be done after a successful attempt
Same input and output as Post Attempt Solution

##Get Deffered
Used with the dmid of the attempt and finalize endpoints

GET https://www.codewars.com/api/v1/deferred/:dmid
```bash
curl https://www.codewars.com/api/v1/deferred/4rsdaDf8d
```
```json
{
   "success":true,
   "dmid":"4rsdaDf8d",
   "valid": false,
   "reason":"-e: Value is not what was expected (Test::Error)\n",
   "output":[
      "<div class='console-failed'>Value is not what was expected</div>"
   ],
   "wall_time":45
}
```
import json
import os

from django.http import JsonResponse

from app.errors.errors import ErrorEnum, errorCheckMessage

## @package app.language
#   This package is used to send the correct json file to the front depending of the user language.


## Loading the json file corresponding to the language of the user.
#   @param request a POST request send by the front must contain :
#   - the user locale (LANG)
#   @return a default json response and the json file containing all the language keys and strings.
def loadLanguage(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        user = request.user
        pathToLang = "/ManaZeak/languages/"
        if 'LANG' in response:
            language = response['LANG']
            # If the user tweaked the request
            if "/" not in language or "\\" not in language:
                jsonFile = os.path.join(pathToLang, language + ".json")
                # If the local is not found using a default one
                if not os.path.isfile(jsonFile):
                    jsonFile = os.path.join(pathToLang, "en.json")
                with open(jsonFile) as file:
                    data = json.load(file)
                data = {**data, **errorCheckMessage(True, None, loadLanguage)}
            else:
                data = errorCheckMessage(False, ErrorEnum.SUSPICIOUS_OPERATION, loadLanguage, user)
        else:
            data = errorCheckMessage(False, ErrorEnum.BAD_FORMAT, loadLanguage, user)
    else:
        data = errorCheckMessage(False, ErrorEnum.BAD_REQUEST, loadLanguage)
    return JsonResponse(data)

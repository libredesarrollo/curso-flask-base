import json

def sendResJson(data, msj, code):

    if code != 200:
        return json.dumps(
            {
                'code': code,
                'msj':msj
            }
        ),code
    else:
         return json.dumps(
            {
                'code': code,
                'data':data
            }
        ),code

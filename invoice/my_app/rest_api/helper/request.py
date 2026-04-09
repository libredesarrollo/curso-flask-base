import json

def sendResJson(data, msj, code):

    if code != 200:
        return json.dumps(
            {
                'code': code,
                'msj':msj
            }
        ),200
    else:
         return json.dumps(
            {
                'code': code,
                'data':data
            }
        ),200

# import json
# import uuid
# import base64
# from datetime import datetime
# from http.client import HTTPSConnection
#
# authString = base64.b64encode(b'549756044284:ZTg4ZjIzZWEtNGQ0YS00ZTUzLTk3NGQtZWQwYzc2NDFkOWYz')
# con = HTTPSConnection('api.uds.app')
# con.request(
#     method='GET',
#     url='/partner/v2/customers/find?code=456123&phone=%2b71234567898&uid=23684cea-ca50-4c5c-b399-eb473e85b5ad',
#     headers={
#         'Accept': 'application/json',
#         'Accept-Charset': 'utf-8',
#         'Authorization': 'Basic ' + authString.decode("utf-8") ,
#         'X-Origin-Request-Id': str(uuid.uuid4()),
#         'X-Timestamp': datetime.now().isoformat(),
#     })
# print (con.getresponse().read())
# con.close()
#
# import json
# import uuid
# import base64
# from datetime import datetime
# from http.client import HTTPSConnection
#
# authString = base64.b64encode(b'549756044284:ZTg4ZjIzZWEtNGQ0YS00ZTUzLTk3NGQtZWQwYzc2NDFkOWYz')
# con = HTTPSConnection('api.uds.app')
# con.request(
#     method='POST',
#     url='/partner/v2/operations/reward',
#     body=json.dumps({
#       'code': 'string',
#       'participants': [1, 3, 17],
#       'points': 50.0,
#       'silent': False
#     }),
#     headers={
#         'Accept': 'application/json',
#         'Accept-Charset': 'utf-8',
#         'Content-Type': 'application/json',
#         'Authorization': 'Basic ' + authString.decode("utf-8") ,
#         'X-Origin-Request-Id': str(uuid.uuid4()),
#         'X-Timestamp': datetime.now().isoformat(),
#     })
# print (con.getresponse().read())
# con.close()
import json
import json
import uuid
import base64
from datetime import datetime
# from http.client import HTTPSConnection
from requests import Session

s = Session()
api_key = "549756044284:ZTg4ZjIzZWEtNGQ0YS00ZTUzLTk3NGQtZWQwYzc2NDFkOWYz"
authString = base64.b64encode(api_key.encode('utf-8'))
print(authString.decode("utf-8"))
url = ()
r = s.request(
    method='GET',
    url='https://api.uds.app/partner/v2/customers/find?code=456123&phone=%2b79964414976',
    headers={
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8',
        'Authorization': 'Basic ' + authString.decode("utf-8"),
        'X-Origin-Request-Id': str(uuid.uuid4()),
        'X-Timestamp': datetime.now().isoformat(),
    })
if r.status_code != 200:
    print("ошибка")
try:
    user_id = r.json()['user']['participant']['id']
    r = s.request(
        method='POST',
        url='https://api.uds.app/partner/v2/operations/reward',
        headers={
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + authString.decode("utf-8"),
            'X-Origin-Request-Id': str(uuid.uuid4()),
            'X-Timestamp': datetime.now().isoformat(),
        },
        data=json.dumps({
            'participants': [user_id,],
            'points': 12,
        }),
    )
    print(r.status_code)
    print(r.text)
except Exception:
    print("Ошибка начисления бонусов")


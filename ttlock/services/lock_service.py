import time
import uuid
from django.conf import settings
import requests

ADD_PASSCODE = 'keyboardPwd/add'
CHANGE_PASSCODE = "keyboardPwd/change"

GATEWAY_LIST_URL = '{}/{}?clientId={}&accessToken={}&pageNo={}&pageSize={}&date={}'
GATEWAY_LIST_RESOURCE = 'gateway/list'

LOCKS_PER_GATEWAY_URL = '{}/{}?clientId={}&accessToken={}&gatewayId={}&date={}'
LOCKS_PER_GATEWAY_RESOURCE = 'gateway/listLock'

CREATE_PASSCODE_URL = '{}/{}?clientId={}&accessToken={}&lockId={}&keyboardPwd={}&keyboardPwdName={}&startDate={}&endDate={}&addType=2&date={}'
CHANGE_PASSCODE_URL = '{}/{}?clientId={}&accessToken={}&lockId={}&keyboardPwd={}&keyboardPwdName={}&startDate={}&endDate={}&addType=2&date={}'

def get_current_millis():
    return int(round(time.time() * 1000))


def get_current_millis_after_90():
    return int(round(time.time() * 1000))


def send_request(_url_request, method='GET'):
    _headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    _response = requests.request(method, _url_request, headers=_headers)
    _response.raise_for_status()

    return _response


def get_gateway_generator(clientId, accessToken):
    pageNo = 1
    totalPages = 1
    pageSize = 20
    while pageNo <= totalPages:
        _url_request = GATEWAY_LIST_URL.format(
            settings.TTLOCK_API_URI,
            GATEWAY_LIST_RESOURCE,
            clientId,
            accessToken,
            pageNo,
            pageSize,
            get_current_millis(),
        )
        _response = send_request(_url_request).json()

        for gateway in _response.get('list'):
            yield gateway
        totalPages = _response.get('pages')
        pageNo += 1


def get_locks_per_gateway_generator(gatewayId, clientId, accessToken):
    if not gatewayId:
        raise TTlockAPIError()

    _url_request = LOCKS_PER_GATEWAY_URL.format(
        settings.TTLOCK_API_URI,
        LOCKS_PER_GATEWAY_RESOURCE,
        clientId,
        accessToken,
        gatewayId,
        get_current_millis(),
    )

    for lock in send_request(_url_request).json().get('list'):
        yield lock


def get_lock_id(clientId, accessToken):
    gateways = get_gateway_generator(clientId, accessToken)

    locks = []
    for gateway in gateways:
        locks += list(
            get_locks_per_gateway_generator(gateway.get("gatewayId"), clientId,
                                            accessToken))
    return locks


class TTlockAPIError(Exception):
    def __init__(self, error_code=-3, menssage='Invalid Parameter'):
        self.error_code = error_code
        self.menssage = menssage

    def __str__(self):
        return 'Error returned from TTlockAPI: Error_code {} - {}'.format(
            self.error_code, self.menssage)


def create_user(clientId, accessToken, clientSecret, username, password):
    lock_id = get_lock_id(clientId, accessToken)[0]['lockId']
    startDate = get_current_millis()
    endDate = startDate + (3110400000*9) # примерно 11 месяцев
    _url_request = CREATE_PASSCODE_URL.format(
        settings.TTLOCK_API_URI,
        ADD_PASSCODE,
        clientId,
        accessToken,
        lock_id,
        password,
        username,
        startDate,
        endDate,
        get_current_millis(),
    )
    response = send_request(_url_request).json()
    if 'keyboardPwdId' in response:
        return True
    return False


def change_user_password(clientId, accessToken, clientSecret, username, password):
    pass
    lock_id = get_lock_id(clientId, accessToken)[0]['lockId']
    newKeyboardPwd = uuid.uuid4()
    _url_request = CREATE_PASSCODE_URL.format(
        settings.TTLOCK_API_URI,
        CHANGE_PASSCODE,
        clientId,
        accessToken,
        lock_id,
        password,
        newKeyboardPwd
    )
    response = send_request(_url_request).json()
import json
from typing import Optional

from django.conf import settings

from requests import Session

URL_GET_CLIENT = f"{settings.HOLIHOP_API_URL}/GetStudents/"
URL_UPDATE_PAYMENT = f"{settings.HOLIHOP_API_URL}/AddPayment/"


def update_user_payment(money: int, client_phone: int, payment_method_id: Optional[int]):
    s = Session()
    error = ""
    s.headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "authkey": settings.HOLIHOP_API_KEY,
        "term": f"{client_phone}",
        "byAgents": True
    }
    try:
        response = s.post(URL_GET_CLIENT, data=json.dumps(payload)).json()
        students = response['Students']
        if len(students) != 1:
            error = "Более 1 ученика, проставьте оплату самостоятельно"
            code = 403
            return error, code, error
        client_id = response["Students"][0]['ClientId']
        officeOrCompanyId = response["Students"][0]["OfficesAndCompanies"][0]['Id']
        payload["clientId"] = client_id
        payload["type"] = "Study"
        payload["officeOrCompanyId"] = officeOrCompanyId
        if payment_method_id is not None:
            payload["paymentMethodId"] = int(payment_method_id)
        payload["value"] = float(money)
        response = s.post(URL_UPDATE_PAYMENT, data=json.dumps(payload))
        print(response.status_code)
    except Exception as e:  # TODO logs to file
        print(e)
        pass
    return error, response.status_code, response.text

import json

from django.http import HttpResponseBadRequest


def get_data(body):
    try:
        list_with_values = ["lockId",
                            "serverDate",
                            "hotelUsername",
                            "recordType",
                            "success",
                            "keyboardPwd",
                            "username",
                            "lockDate"]
        json_data = json.loads(body)
        for i in json_data:
            if i not in list_with_values:
                raise HttpResponseBadRequest
        return json_data
    except Exception:
        raise HttpResponseBadRequest
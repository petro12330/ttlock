import json
from datetime import datetime, date
from pprint import pprint
from typing import Optional

from django.conf import settings
from requests import Session

from ttlock.services.chat2deck_service import send_message_by_phone, prepare_phone

URL_GET_CLIENT = f"{settings.HOLIHOP_API_URL}/GetStudents/"
URL_UPDATE_PAYMENT = f"{settings.HOLIHOP_API_URL}/AddPayment/"
URL_GET_ED_UNITS = f"{settings.HOLIHOP_API_URL}/GetEdUnits/"
URL_GET_ED_UNITS_STUDENTS = f"{settings.HOLIHOP_API_URL}/GetEdUnitStudents/"
URL_GET_TEACHERS = f"{settings.HOLIHOP_API_URL}/GetTeachers/"

WEEKDAYS = [1, 2, 4, 8, 16, 32, 64]  # Пн: 1, Вт: 2, Ср: 4, Чт: 8, Пт: 16, Сб: 32, Вс: 64

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


def get_teacher_info(teacher_id):
    s = Session()
    s.headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "authkey": settings.HOLIHOP_API_KEY,
        "id": teacher_id
    }
    data = s.get(URL_GET_TEACHERS, data=json.dumps(payload)).json()["Teachers"][0]
    if "Mobile" not in data or data.get("Status", None) != "Работает":
        return
    teacher_data = {
        "teacher_id": teacher_id,
        "first_name": data.get("FirstName", ''),
        "middle_name": data.get("MiddleName", ''),
        "last_name": data.get("LastName", ''),
        "phone": data.get("Mobile", ''),
    }
    return teacher_data


def get_ed_units():
    s = Session()
    done_ed_units = []
    teachers = {}
    s.headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "authkey": settings.HOLIHOP_API_KEY,
        "dateFrom": date.today().strftime("%Y-%m-%d"),
        "timeFrom": date.today().strftime("%Y-%m-%d"),
        "weekdays": WEEKDAYS[datetime.weekday(datetime.now())],
        "statuses": "Working"
    }
    data = s.get(URL_GET_ED_UNITS, data=json.dumps(payload)).json()
    ed_units = data.get('EdUnits')
    for ed_unit in ed_units:
        schedule_items = ed_unit["ScheduleItems"][-1]  # TODO Может стрельнуть!!
        if ed_unit["StudentsCount"] <= 0 or "TeacherId" not in schedule_items:
            continue
        teacher_id = schedule_items["TeacherId"]
        teacher_info = teachers.get(teacher_id, None)
        if teacher_info is None:
            teacher_info = get_teacher_info(teacher_id)
            if teacher_info is None:
                continue
            teacher_info['message'] = "Добрый день!\nВаше расписание на сегодня:"
            teachers[teacher_id] = teacher_info

        teacher_info['message'] += f'\n• {ed_unit["OfficeOrCompanyName"]} в {schedule_items["BeginTime"]}, ' \
                              f'закончится в {schedule_items["EndTime"]};'
        group_data = {
            "id": ed_unit["Id"],
            "group_name": ed_unit["Name"],
            'teacher_id': teacher_id,
            "address": ed_unit["OfficeOrCompanyName"],
            "students_count": ed_unit["StudentsCount"],
            "lesson_start": schedule_items["BeginTime"],
            "lesson_end": schedule_items["EndTime"]
        }
        done_ed_units.append(group_data)
    return done_ed_units, teachers


def send_request_group(group, s=Session()):
    payload = {
        "authkey": settings.HOLIHOP_API_KEY,
        "edUnitId": group["Id"],
        "statuses": "Normal"
    }
    data = s.get(URL_GET_ED_UNITS_STUDENTS, data=json.dumps(payload)).json()
    return data


def get_ed_units_students(groups):
    s = Session()
    done_ed_units_students = []
    s.headers = {
        'Content-Type': 'application/json'
    }
    for group in groups:
        done_ed_units_students.append(send_request_group(group, s))
    return done_ed_units_students


def send_message_teachers(groups, teachers):
    for teacher in teachers.values():
        phone = prepare_phone(teacher['phone'])
        if phone is None:
            continue
        send_message_by_phone(phone, teacher['message'])

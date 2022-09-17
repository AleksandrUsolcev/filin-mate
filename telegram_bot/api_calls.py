import os
from datetime import datetime
from http import HTTPStatus

import requests
from dateutil import parser
from dotenv import load_dotenv

import exceptions as exc

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
FILIN_TOKEN = os.getenv('FILIN_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
ENDPOINT = os.getenv('ENDPOINT', default='http://127.0.0.1:8000/api/1.0/')

HEADERS = {'Authorization': 'Bearer ' + FILIN_TOKEN}

DIFF_TIME = 15

ERRORS = {
    'user_not_found': exc.UserNotFoundError,
    'stat_type_not_found': exc.StatTypeNotFoundError,
    'stat_incorrect_value': exc.IncorrectValueError
}


def time_difference(response_json: dict) -> float:
    if not response_json['results']:
        return DIFF_TIME
    last_updated = response_json['results'][0]['created']
    last_updated = parser.parse(last_updated).replace(tzinfo=None)
    difference = (datetime.now() - last_updated).total_seconds() / 60
    return difference


def get_path(request_type: str, data: dict) -> str:
    pathes = {
        'stats': (f'stats/?patient={data.get("patient")}'
                  f'&type={data.get("type")}&limit=1'),
        'patients': f'patients/?telegram={data.get("telegram")}'
    }
    path = ENDPOINT + pathes[request_type]
    return path


def error_filter(response: dict) -> dict:
    if 'error' in response:
        error = response['error']
        raise ERRORS[error]
    return response


def check_response(request_type: str, data: dict) -> dict:
    path = get_path(request_type, data)
    response = requests.get(path, headers=HEADERS)
    return error_filter(response.json())


def stats_post(patient: int, stat_type: str, data: float):
    post_data = {
        'patient': patient,
        'type': stat_type,
        'data': data
    }
    response = check_response('stats', post_data)
    difference = time_difference(response)
    if difference >= DIFF_TIME:
        path = 'stats/'
        response = requests.post(ENDPOINT + path, post_data, headers=HEADERS)
        error_filter(response.json())
        return HTTPStatus.OK
    else:
        raise exc.TimeDifferenceError


def patient_post(telegram_id: int):
    post_data = {
        'telegram': telegram_id
    }
    path = 'patients/'
    requests.post(ENDPOINT + path, post_data, headers=HEADERS)
    return HTTPStatus.OK


def patient_patch_age(telegram_id: int, age: str):
    check_data = {
        'telegram': telegram_id
    }
    check_response('patients', check_data)
    age = str(parser.parse(age)).split()[0]
    patch_data = {
        'age': age
    }
    path = f'patients/{telegram_id}/'
    requests.patch(ENDPOINT + path, patch_data, headers=HEADERS)
    return HTTPStatus.OK

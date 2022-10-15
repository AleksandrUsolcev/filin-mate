from datetime import datetime
from pytz import timezone

import requests
from dateutil import parser

import exceptions as exc
from errors import API_ERRORS
from settings import DIFF_TIME, ENDPOINT, HEADERS


def time_difference(response_json: dict) -> float:
    if not response_json['results']:
        return DIFF_TIME
    last_updated = response_json['results'][0]['created']
    last_updated = parser.parse(last_updated).replace(tzinfo=None)
    tz = timezone('Europe/Moscow')
    time_now = datetime.now(tz).replace(tzinfo=None)
    difference = (time_now - last_updated).total_seconds() / 60
    return difference


def get_path(request_type: str, data: dict) -> str:
    pathes = {
        'stats': (f'stats/?patient={data.get("patient")}'
                  f'&type={data.get("type")}&limit=1'),
        'notes': f'notes/?patient={data.get("patient")}&limit=1',
        'stats_get': (f'stats/?patient={data.get("patient")}'
                      f'&type={data.get("type")}'
                      f'&limit={data.get("limit")}&ordering=created'),
        'patients': f'patients/?telegram={data.get("telegram")}'
    }
    path = ENDPOINT + pathes.get(request_type)
    return path


def error_filter(response: dict) -> dict:
    if 'error' in response:
        error = response.get('error')
        raise API_ERRORS.get(error)
    return response


def check_response(request_type: str, data: dict) -> dict:
    path = get_path(request_type, data)
    response = requests.get(path, headers=HEADERS)
    return error_filter(response.json())


def stats_type_post(
        slug: str, name: str, min_value: int, max_value: int, data_type: str,
        description: str = '') -> object:
    post_data = {
        'slug': slug,
        'name': name,
        'min_value': min_value,
        'max_value': max_value,
        'data_type': data_type,
        'description': description
    }
    path = 'types/'
    response = requests.post(ENDPOINT + path, post_data, headers=HEADERS)
    return response


def stats_post(patient: int, stat_type: str, data: float) -> object:
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
        return response
    else:
        raise exc.StatTimeDifferenceError


def stats_get(patient: int, stat_type: str, limit: int) -> object:
    get_data = {
        'patient': patient,
        'type': stat_type,
        'limit': limit
    }
    response = check_response('stats_get', get_data)
    error_filter(response)
    count = response['count']
    dates = [parser.parse(response['results'][i]['created'])
             for i in range(count)]
    stats = [response['results'][i]['data'] for i in range(count)]
    results = {
        'dates': dates,
        stat_type: stats,
        'count': count
    }
    return results


def note_post(telegram_id: int, text: str) -> object:
    post_data = {
        'patient': telegram_id,
        'text': text
    }
    response = check_response('notes', post_data)
    difference = time_difference(response)
    if difference >= DIFF_TIME:
        path = 'notes/'
        response = requests.post(ENDPOINT + path, post_data, headers=HEADERS)
        error_filter(response.json())
        return response
    else:
        raise exc.NoteTimeDifferenceError


def patient_post(telegram_id: int) -> object:
    post_data = {
        'telegram': telegram_id
    }
    path = 'patients/'
    response = requests.post(ENDPOINT + path, post_data, headers=HEADERS)
    return response


def patient_patch_age(telegram_id: int, age: str) -> object:
    check_response('patients', {'telegram': telegram_id})
    age = str(parser.parse(age)).split()[0]
    patch_data = {
        'age': age
    }
    path = f'patients/{telegram_id}/'
    response = requests.patch(ENDPOINT + path, patch_data, headers=HEADERS)
    return response


def weather_post(code: int, temp: int, pressure: int, humidity: int) -> object:
    post_data = {
        'code': code,
        'temp': temp,
        'pressure': pressure,
        'humidity': humidity
    }
    path = 'weathers/'
    response = requests.post(ENDPOINT + path, post_data, headers=HEADERS)
    return response

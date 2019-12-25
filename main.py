from urllib import request, error, parse
import os
import time


def send_error_message(url, status_code):
    chat_ids = os.environ.get('CHAT_IDS', '').split(',')
    error_message = os.environ.get('ERROR_MESSAGE', 'Сайт {url} недоступен, код ошибки: {code}')\
        .format(url=url, code=status_code)
    token = os.environ.get('TOKEN', '')
    if chat_ids != ['']:
        for chat_id in chat_ids:
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={parse.quote(error_message)}"
            response = request.urlopen(url)
    else:
        print(error_message)


def get_status(url):
    try:
        response = request.urlopen(url)
        status_code = response.get_code()
    except error.URLError:
        status_code = None
    return status_code


def run_checker(url):
    delay = int(os.environ.get('DELAY', 60))
    while True:
        status_code = get_status(url)
        if status_code != 200:
            send_error_message(url, status_code or -1)
        time.sleep(delay)


if __name__ == '__main__':
    run_checker(os.environ['URL'])

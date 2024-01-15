#!/usr/bin/python3.9

import requests
import sys
from misc.logger import Logger

# Адрес и порта расположения RTSP server
URL = "192.168.15.10"
PORT = 8093
REQUEST_DICT = {"RESULT": "ERROR", "STATUS_CODE": 400, "DESC": '', "DATA": dict()}
LOG_PATH = None  # Возможно указать путь в строке - пример: "/home/asterisk/logs/"
# (предварительно требуется создание полного пути)

logger = Logger(log_path=LOG_PATH)


def do_request(caller_id: int, answer_id: int) -> dict:
    """ Функция отправляет запрос на RTSP сервер """

    # возвращаемый объект
    ret_value = REQUEST_DICT

    try:
        res = requests.get(f"http://{URL}:{PORT}/"
                           f"action.save?caller_id={caller_id}&answer_id={answer_id}", timeout=2)

        ret_value['STATUS_CODE'] = res.status_code
        ret_value['DATA'] = res.json()
        ret_value['RESULT'] = 'SUCCESS'
    except TimeoutError as tx:
        ret_value['DESC'] = f"Превышено время ожидания ответа: {tx}"
        ret_value['STATUS_CODE'] = 408
    except Exception as ex:
        ret_value['DESC'] = f"Исключение вызвало: {ex}"

    return ret_value


def main():
    try:
        # Сделано для теста в Debug mode.
        if sys.gettrace() is not None:
            logger.event(do_request(205, 200))
        else:
            # Получаем данные от астериск
            caller_id = sys.argv[1]
            answer_id = sys.argv[2]

            logger.event(f"Получены данные: caller_id:{caller_id} - answer_id:{answer_id}")

            if caller_id != answer_id:
                # Вызываем запрос
                logger.event(do_request(caller_id, answer_id))
            else:
                logger.warning(f"Звонящий не может быть инициатором нажатия клавиши: {caller_id} == {answer_id}")
    except Exception as ex:
        logger.exception(f"Исключение вызвало: {ex}")

    return True


if __name__ == "__main__":
    logger.event(f"Запуск скрипта", print_it=False)

    main()

#!/usr/bin/python3.9

import requests
import sys
from misc.logger import Logger

# Адрес и порта расположения RTSP server
URL = "192.168.15.10"
PORT = 8093

LOG_PATH = None  # Возможно указать путь в строке - пример: "/home/asterisk/logs/"
# (предварительно требуется создание полного пути)

logger = Logger(log_path=LOG_PATH)


def do_request(caller_id: int, answer_id: int):
    """ Функция отправляет запрос на RTSP сервер """
    try:
        res = requests.get(f"http://{URL}:{PORT}/"
                           f"action.save?caller_id={caller_id}&answer_id={answer_id}", timeout=2)

        logger.event(f"Статус запроса: {res}")
        logger.event(f"Результаты запроса: {res.json()}")
    except Exception as ex:
        logger.exception(f"Исключение вызвало: {ex}")

    return True


def main():
    try:
        # Получаем данные от астериск
        caller_id = sys.argv[1]
        answer_id = sys.argv[2]

        logger.event(f"Получены данные: caller_id:{caller_id} - answer_id:{answer_id}")

        if caller_id != answer_id:
            # Вызываем запрос
            do_request(caller_id, answer_id)
        else:
            logger.warning(f"Звонящий не может быть инициатором нажатия клавиши: {caller_id} == {answer_id}")
    except Exception as ex:
        logger.exception(f"Исключение вызвало: {ex}")
    finally:
        # Нужен ли тут finally? Нет! Но сделал с целью разнообразия...
        # Сделано для теста в Debug mode.
        if sys.gettrace() is not None:
            do_request(205, 200)


if __name__ == "__main__":
    logger.event(f"Запуск скрипта", print_it=False)

    main()

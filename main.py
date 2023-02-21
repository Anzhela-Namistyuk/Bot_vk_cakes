import logging
import time
from collections import defaultdict

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType

from configs import configure_logging
from db_cakes.db import DB_BakeryProducts
from constants import API_VERSION, TOKEN, CAKES, KEYBOARD_MESSAGE_BY_STATE

from statees_keyboard import create_keyboard


def send_message(user_id, path_to_keyboard, message_text):
    """Функция для отправки личных сообщений с кнопками."""

    for i in range(0, 3):
        try:
            with open(path_to_keyboard, 'r', encoding='UTF-8') as keyboard:

                vk.messages.send(
                    user_id=user_id,
                    random_id=0,
                    keyboard=keyboard.read(),
                    message=message_text)
        except:
            logging.exception(
                f'Ошибка отправки сообщения пользователю с id {user_id}'
            )
            time.sleep(0.5)
            continue
        break


def take_path_descr_cake(name_cake):
    """Функция обращается к базе данных,
    возвращает описание пирогов и путь до картинки.
    """
    try:
        db = DB_BakeryProducts()
        descr, path = db.get_cake_descr_path(name_cake)
        return descr, path
    except Exception:
        logging.exception(f'Ошибка соединения c базой')


def send_message_cake_descr(user_id, message_text):
    """Функция отправляет сообщение
    с описанием пирога и картинкой.
    """
    for i in range(0, 3):
        try:
            descr, path = take_path_descr_cake(message_text)
            photo = upload.photo_messages(path)
            owner_id = photo[0]['owner_id']
            photo_id = photo[0]['id']
            access_key = photo[0]['access_key']
            attachment = f'photo{owner_id}_{photo_id}_{access_key}'
            vk.messages.send(
                peer_id=user_id,
                random_id=0,
                message=descr,
                attachment=attachment)
        except:
            logging.exception(
                f'Ошибка отправки сообщения пользователю с id {user_id}'
            )
            time.sleep(0.5)
            continue
        break


def processing_message(user_id, message_text, keyboard):
    """Функция распределяет процесс отправки сообщений
     в зависимости от входного сообщения.
     """

    keyboard.click(message_text, user_id)
    # если сообщение содержит название определенного пирога,
    # то отправляет сообщение с описанием и картинкой
    if message_text in CAKES:
        send_message_cake_descr(user_id, message_text)

    # в зависимости от состояния триггера получаем
    # путь до клавиатуры и строку с сообщением для ответа и
    # отправляет сообщение с клавиатурой
    path_to_keyboard, massage = KEYBOARD_MESSAGE_BY_STATE[keyboard.state]
    send_message(user_id, path_to_keyboard, massage)


if __name__ == '__main__':
    configure_logging()
    vk_session = vk_api.VkApi(token=TOKEN, api_version=API_VERSION)
    vk = vk_session.get_api()
    upload = VkUpload(vk)
    longpoll = VkLongPoll(vk_session)
    logging.info('Бот запущен!')

    user_to_state = defaultdict(create_keyboard)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            message_text = event.text
            keyboard = user_to_state[user_id]
            try:
                processing_message(user_id, message_text, keyboard)
            except:
                logging.exception('Ошибка во время отправки сообщения')

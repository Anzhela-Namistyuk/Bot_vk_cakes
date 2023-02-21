import logging

from transitions import Machine, MachineError
from constants import STATES, TRANSITIONS, MESSAGE_STATE


class Matter(object):
    """Определяет переходы межу кнопками."""

    def click(self, message, user_id):
        """В зависимости от полученного
        сообщения меняет состояние триггера.
        """

        STATE_KEYBOARD = {
            'Сладкие пироги': self.main_to_sweet,
            'Овощные пироги': self.main_to_veget,
            'Мясные пироги': self.main_to_meat,
            'Рыбные пироги': self.main_to_fish,
            'Выйти в главное меню': self.any_to_main
        }
        click = STATE_KEYBOARD.get(message)
        if click is not None:
            try:
                # изменяем состояние триггера перехода
                click()

            except MachineError:
                logging.exception(f'Переход невозможен из {self.state}  '
                                  f'в {MESSAGE_STATE.get(message,)} для пользователя с id {user_id}')


def create_keyboard():
    keyboard = Matter()
    # Инициализация машины
    Machine(keyboard, states=STATES, transitions=TRANSITIONS, initial='main_keyboard')

    return keyboard

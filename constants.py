import os

from dotenv import load_dotenv

load_dotenv()
API_VERSION = 5.131

TOKEN = os.getenv('TOKEN')


keyboard_main = 'keyboard/keyboard_main.json'
keyboard_sweet = 'keyboard/keyboard_sweet.json'
keyboard_vegetable = 'keyboard/keyboard_vegetable.json'
keyboard_meat = 'keyboard/keyboard_meat.json'
keyboard_fish = 'keyboard/keyboard_fish.json'

KEYBOARD_MESSAGE_BY_STATE = {
    'main_keyboard': [keyboard_main, "Выберите тип пирогов!"],
    'sweet_keyboard': [keyboard_sweet, 'Выберите пирог'],
    'vegetable_keyboard': [keyboard_vegetable, 'Выберите пирог'],
    'meat_keyboard': [keyboard_meat, 'Выберите пирог'],
    'fish_keyboard': [keyboard_fish, 'Выберите пирог']
}

CAKES = {
    'Пирог с яблоком и корицей', 'Пирог с маком',
    'Пирог с картофелем и луком', 'Пирог с капустой и яйцом',
    'Пирог с говядиной и луком', 'Пирог с говядиной и капустой',
    'Пирог с семгой и рисом', 'Пирог с треской и капустой'
}


MESSAGE_STATE = {
    'Сладкие пироги': 'sweet_keyboard',
    'Овощные пироги': 'vegetable_keyboard',
    'Мясные пироги': 'meat_keyboard',
    'Рыбные пироги': 'fish_keyboard',
    'Выйти в главное меню': 'main_keyboard'
}

# Полный список состояний кнопок
STATES = [
    'main_keyboard', 'sweet_keyboard',
    'vegetable_keyboard', 'meat_keyboard',
    'fish_keyboard'
]
# Добавляем таблицу переходов — из какого в какое состояние мы можем попасть
TRANSITIONS = [
    {'trigger': 'main_to_sweet', 'source': 'main_keyboard', 'dest': 'sweet_keyboard'},
    {'trigger': 'main_to_veget', 'source': 'main_keyboard', 'dest': 'vegetable_keyboard'},
    {'trigger': 'main_to_meat', 'source': 'main_keyboard', 'dest': 'meat_keyboard'},
    {'trigger': 'main_to_fish', 'source': 'main_keyboard', 'dest': 'fish_keyboard'},
    {'trigger': 'any_to_main', 'source': '*', 'dest': 'main_keyboard'}
]

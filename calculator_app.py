# calculator_app.py

import streamlit as st

import json
import os

# --- СТРУКТУРЫ ДАННЫХ И КОНФИГУРАЦИЯ ---
# Это как список всех возможных баночек для наших подсчетов.
# Мы заранее готовим место для каждого продукта.
ALL_PRODUCT_CATEGORIES = [
    "ДК", "КК", "Комбо/Кросс КК", "ЦП", "Смарт", "Кешбек", "ЖКУ", "БС",
    "Инвесткопилка", "БС со Стратегией", "Токенизация", "Накопительный Счет",
    "Вклад", "Детская Кросс", "Стикер Кросс", "Сим-Карта", "Кросс ДК",
    "Селфи ДК", "Селфи КК", "Мобильное Приложение"
]

# Это наша "поваренная книга" с разделами.
# Говорит, какие кнопки показывать в каждом меню.
MENUS = {
    "ДК": [
        "ДК", "Комбо/Кросс КК", "ЦП", "Смарт", "Кешбек", "ЖКУ", "БС",
        "Инвесткопилка", "БС со Стратегией", "Токенизация",
        "Накопительный Счет", "Вклад", "Детская Кросс", "Стикер Кросс",
        "Сим-Карта"
    ],
    "КК": [
        "КК", "ЦП", "Смарт", "Кешбек", "ЖКУ", "БС", "Инвесткопилка",
        "БС со Стратегией", "Токенизация", "Накопительный Счет", "Вклад",
        "Детская Кросс", "Стикер Кросс", "Сим-Карта", "Кросс ДК"
    ],
    "Селфи": [
        "Селфи ДК", "Селфи КК"
    ],
    "МП": [
        "Мобильное Приложение"
    ]
}

# NEW: Define the filename for our data "notebook"
DATA_FILE = "calculator_data.json"

# --- СТИЛИЗАЦИЯ (CSS) ---
# Здесь мы "украшаем" наш блокнот: делаем белый фон, красивые кнопки
# со скругленными углами и черным текстом.
def set_styles():
    """Применяет CSS стили для оформления приложения."""
    st.markdown("""
        <style>
            /* Основной фон */
            .main .block-container {
                background-color: #FFFFFF;
            }
            /* Стили для всех кнопок */
            .stButton > button {
                width: 100%; /* Одинаковая ширина */
                height: 50px; /* Одинаковая высота */
                border: 1px solid #CCCCCC; /* Тонкая серая рамка */
                border-radius: 8px; /* Скругленные углы */
                color: #000000; /* Черный цвет текста */
                font-family: 'Calibri', sans-serif; /* Шрифт Calibri */
                font-size: 16px;
                font-weight: normal;
                text-align: center; /* Центрирование текста */
                margin-bottom: 10px; /* Отступ снизу */
            }
            /* Стили для поля ввода */
            .stNumberInput > div > div > input {
                font-family: 'Calibri', sans-serif;
                color: #000000;
            }
            /* Стили для текста отчета */
            .report-text {
                font-family: 'Calibri', sans-serif;
                color: #000000;
                font-size: 18px;
                line-height: 1.6;
            }
            h1, h2, h3 {
                font-family: 'Calibri', sans-serif;
                color: #000000;
            }
        </style>
    """, unsafe_allow_html=True)



# --- ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛАМИ (для каждого пользователя свой файл) ---

def get_user_data_file(username):
    """Создает имя файла на основе имени пользователя (например, data_Анна.json)."""
    # Убираем из имени символы, которые не могут быть в названии файла
    safe_username = "".join(c for c in username if c.isalnum() or c in (' ', '_')).rstrip()
    return f"data_{safe_username}.json"

def load_data_from_file(username):
    """Загружает данные из личного файла пользователя."""
    filename = get_user_data_file(username)
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {category: 0 for category in ALL_PRODUCT_CATEGORIES}
    return {category: 0 for category in ALL_PRODUCT_CATEGORIES}

def save_data_to_file(username, data):
    """Сохраняет данные в личный файл пользователя."""
    filename = get_user_data_file(username)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- УПРАВЛЕНИЕ СОСТОЯНИЕМ ---
# Это "память" нашего блокнота.

def initialize_state():
    """Инициализирует состояние сессии."""
    # Запоминаем, кто сейчас пользуется калькулятором. Вначале - никто.
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    
    # Эти строчки остаются как были, но теперь данные будут загружаться для конкретного пользователя
    if 'data' not in st.session_state:
        st.session_state['data'] = {category: 0 for category in ALL_PRODUCT_CATEGORIES}
    
    if 'view' not in st.session_state:
        st.session_state['view'] = 'main_menu'
        
    if 'current_product' not in st.session_state:
        st.session_state['current_product'] = None

# --- ФУНКЦИИ-ПОМОЩНИКИ (Навигация) ---
# Это как закладки в книге, чтобы быстро переходить на нужную страницу.
def go_to_menu(menu_name):
    # ИСПРАВЛЕНО:
    st.session_state.view = menu_name

def go_to_main_menu():
    # ИСПРАВЛЕНО:
    st.session_state.view = 'main_menu'

def go_to_input(product_name):
    # ИСПРАВЛЕНО:
    st.session_state.view = 'input_form'
    st.session_state.current_product = product_name

def go_to_report():
    # ИСПРАВЛЕНО:
    st.session_state.view = 'report'

# КНОПКА СБРОСА ДАННЫХ ДЛЯ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ:
def reset_data():
    """Сбрасывает данные для ТЕКУЩЕГО пользователя и сохраняет пустоту в его личный файл."""
    # 1. Создаем новый пустой "холодильник" (набор пустых данных)
    fresh_data = {category: 0 for category in ALL_PRODUCT_CATEGORIES}
    
    # 2. Ставим этот пустой холодильник в квартиру текущего пользователя (в его временную память)
    st.session_state['data'] = fresh_data
    
    # 3. ГЛАВНОЕ ИЗМЕНЕНИЕ:
    # Мы говорим "уборщику": "Сохрани эти пустые данные для вот этого пользователя!"
    # Теперь уборка происходит в личном файле.
    save_data_to_file(st.session_state['username'], fresh_data)
    
    # 4. Возвращаем пользователя в главное меню
    go_to_main_menu()
    
    # 5. Дополнительно перезагружаем страницу, чтобы все точно обновилось
    st.rerun()


# --- ЛОГИКА ОТОБРАЖЕНИЯ (Что мы показываем пользователю) ---

def display_login_screen():
    """Отображает экран для ввода имени пользователя."""
    st.header("Добро пожаловать в калькулятор!")
    st.subheader("Пожалуйста, представьтесь, чтобы мы могли сохранить ваши данные.")
    
    username = st.text_input("Введите ваше имя (например, Анна, Иван Петрович):")
    
    if st.button("Войти"):
        if username:
            # Запоминаем имя пользователя в "памяти" сессии
            st.session_state['username'] = username
            st.rerun() # Сразу перезапускаем страницу, чтобы показать главное меню
        else:
            st.warning("Пожалуйста, введите имя.")

def display_main_menu():
    """Отображает кнопки главного меню, адаптированные для мобильных."""
    st.header("Основное меню")
    
    # ИСПРАВЛЕНО: Правильный синтаксис для создания колонок
    col1, col2 = st.columns(2)
    
    # Размещаем кнопки по колонкам
    with col1:
        st.button("ДК", on_click=go_to_menu, args=("dk_menu",))
        st.button("Селфи", on_click=go_to_menu, args=("selfie_menu",))
    
    with col2:
        st.button("КК", on_click=go_to_menu, args=("kk_menu",))
        st.button("МП", on_click=go_to_menu, args=("mp_menu",))
        
    # Кнопку отчета делаем на всю ширину под колонками
    st.button("Сформировать отчет", on_click=go_to_report)

def display_submenu(menu_key, title):
    """Отображает кнопки подменю."""
    st.header(title)
    for product in MENUS[menu_key]:
        st.button(product, key=f"{menu_key}_{product}", on_click=go_to_input, args=(product,))
    st.button("Вернуться в основное меню", key=f"back_{menu_key}", on_click=go_to_main_menu)

def display_input_form():
    """Отображает форму для ввода количества продукта."""
    product = st.session_state['current_product']
    st.header(f"Ввод данных для: {product}")
    
    quantity = st.number_input(
        "Введите количество:",
        min_value=0,
        step=1,
        key=f"input_{product}"
    )
    
    # Кнопка "Добавить"
    if st.button("Добавить", key=f"add_{product}"):
        st.session_state['data'][product] += quantity
        #
        # А ВОТ ИСПРАВЛЕННАЯ СТРОЧКА:
        # MODIFIED: We now tell the function WHO is saving the data
        save_data_to_file(st.session_state['username'], st.session_state['data'])
        #
        st.success(f"Добавлено: {quantity} к '{product}'. Возврат в главное меню.")
        go_to_main_menu()
        st.rerun()

def display_report():
    """Отображает итоговый отчет."""
    st.header("Отчет")
    
    report_lines = []
    # Список продуктов для отчета в нужном порядке
    report_order = [
        "ДК", "КК", "Комбо/Кросс КК", "ЦП", "Смарт", "Кешбек", "ЖКУ", "БС",
        "Инвесткопилка", "БС со Стратегией", "Токенизация", "Накопительный Счет",
        "Вклад", "Детская Кросс", "Стикер Кросс", "Сим-Карта", "Кросс ДК",
        "Селфи ДК", "Селфи КК", "Мобильное Приложение"
    ]
    
    for i, product in enumerate(report_order, 1):
        # ИСПРАВЛЕНО: Проверяем наличие продукта в данных сессии
        if product in st.session_state.data:
            # ИСПРАВЛЕНО: Получаем количество из данных сессии
            count = st.session_state.data[product]
            # Добавляем в отчет все продукты, даже с нулевым значением
            report_lines.append(f"{i}. {product} - {count}")

    # Выводим отчет как единый текст
    st.markdown(f"<div class='report-text'>{'<br>'.join(report_lines)}</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True) # Небольшой отступ
    
    # Кнопка "Сбросить"
    st.button("Сбросить", on_click=reset_data)
    # Кнопка "Вернуться в основное меню" для удобства
    st.button("Вернуться в основное меню", on_click=go_to_main_menu)



# --- ГЛАВНАЯ ЧАСТЬ ПРОГРАММЫ ---
def main():
    """Основная функция, запускающая приложение."""
    set_styles()
    initialize_state()

    # Если пользователь еще не представился, показываем ему экран входа
    if st.session_state.get('username') is None:
        display_login_screen()
    else:
        # Если мы знаем, кто пользователь, загружаем его личные данные
        st.session_state['data'] = load_data_from_file(st.session_state['username'])
        
        # Приветствуем пользователя и добавляем кнопку "Выйти"
        st.sidebar.success(f"Вы вошли как: **{st.session_state['username']}**")
        if st.sidebar.button("Сменить пользователя"):
            # Очищаем все данные сессии и перезапускаем, чтобы показать экран входа
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        # Дальше логика остается прежней - показываем нужные меню
        view = st.session_state.get('view', 'main_menu')
        
        if view == 'main_menu':
            display_main_menu()
        elif view == 'dk_menu':
            display_submenu('ДК', 'Меню для ДК')
        elif view == 'kk_menu':
            display_submenu('КК', 'Меню для КК')
        elif view == 'selfie_menu':
            display_submenu('Селфи', 'Меню для Селфи')
        elif view == 'mp_menu':
            display_submenu('МП', 'Меню для МП')
        elif view == 'input_form':
            display_input_form()
        elif view == 'report':
            display_report()

# calculator_app.py

import streamlit as st
import json
import os
import datetime
import extra_streamlit_components as stx

# --- СТРУКТУРЫ ДАННЫХ И КОНФИГУРАЦИЯ ---
ALL_PRODUCT_CATEGORIES = [
    "ДК", "КК", "Комбо/Кросс КК", "ЦП", "Смарт", "Кешбек", "ЖКУ", "БС",
    "Инвесткопилка", "БС со Стратегией", "Токенизация", "Накопительный Счет",
    "Вклад", "Детская Кросс", "Стикер Кросс", "Сим-Карта", "Кросс ДК",
    "Селфи ДК", "Селфи КК", "Мобильное Приложение"
]

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
    "Селфи": ["Селфи ДК", "Селфи КК"],
    "МП": ["Мобильное Приложение"]
}

# --- СТИЛИЗАЦИЯ (CSS) ---
def set_styles():
    """Применяет CSS стили для оформления приложения."""
    st.markdown("""
        <style>
            .main .block-container { background-color: #FFFFFF; }
            .stButton > button { width: 100%; height: 50px; border: 1px solid #CCCCCC; border-radius: 8px; color: #000000; font-family: 'Calibri', sans-serif; font-size: 16px; font-weight: normal; text-align: center; margin-bottom: 10px; }
            .stNumberInput > div > div > input { font-family: 'Calibri', sans-serif; color: #000000; }
            .report-text { font-family: 'Calibri', sans-serif; color: #000000; font-size: 18px; line-height: 1.6; }
            h1, h2, h3 { font-family: 'Calibri', sans-serif; color: #000000; }
        </style>
    """, unsafe_allow_html=True)

# --- ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛАМИ ---
def get_user_data_file(username):
    safe_username = "".join(c for c in username if c.isalnum() or c in (' ', '_')).rstrip()
    return f"data_{safe_username}.json"

def load_data_from_file(username):
    filename = get_user_data_file(username)
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {category: 0 for category in ALL_PRODUCT_CATEGORIES}
    return {category: 0 for category in ALL_PRODUCT_CATEGORIES}

def save_data_to_file(username, data):
    filename = get_user_data_file(username)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- УПРАВЛЕНИЕ СОСТОЯНИЕМ ---
def initialize_state():
    if 'view' not in st.session_state:
        st.session_state['view'] = 'main_menu'
    if 'current_product' not in st.session_state:
        st.session_state['current_product'] = None

# --- ФУНКЦИИ-ПОМОЩНИКИ (Навигация) ---
def go_to_menu(menu_name):
    st.session_state['view'] = menu_name

def go_to_main_menu():
    st.session_state['view'] = 'main_menu'

def go_to_input(product_name):
    st.session_state['view'] = 'input_form'
    st.session_state['current_product'] = product_name

def go_to_report():
    st.session_state['view'] = 'report'

def reset_data():
    fresh_data = {category: 0 for category in ALL_PRODUCT_CATEGORIES}
    st.session_state['data'] = fresh_data
    save_data_to_file(st.session_state['username'], fresh_data)
    go_to_main_menu()

# --- ЛОГИКА ОТОБРАЖЕНИЯ ---
def display_login_screen():
    """Отображает экран для ввода имени пользователя и устанавливает cookie."""
    st.header("Добро пожаловать в калькулятор!")
    st.subheader("Пожалуйста, представьтесь, чтобы мы могли сохранить ваши данные.")
    
    # Получаем доступ к нашему "станку для карт"
    cookies = stx.CookieManager()
    
    username = st.text_input("Введите ваше имя (например, Анна, Иван Петрович):", key="login_input")
    
    if st.button("Войти", key="login_button"):
        if username:
            # Запоминаем имя в краткосрочной памяти
            st.session_state['username'] = username
            # ГЛАВНОЕ ИЗМЕНЕНИЕ: Создаем "карту-ключ" и отдаем ее браузеру.
            # Она будет "жить" 30 дней.
            cookies.set('username', username, expires_at=datetime.datetime.now() + datetime.timedelta(days=30))
            st.rerun()
        else:
            st.warning("Пожалуйста, введите имя.")

def display_main_menu():
    """Отображает кнопки главного меню."""
    st.header("Основное меню")
    col1, col2 = st.columns(2)
    with col1:
        st.button("ДК", on_click=go_to_menu, args=("dk_menu",))
        st.button("Селфи", on_click=go_to_menu, args=("selfie_menu",))
    with col2:
        st.button("КК", on_click=go_to_menu, args=("kk_menu",))
        st.button("МП", on_click=go_to_menu, args=("mp_menu",))
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
    quantity = st.number_input("Введите количество:", min_value=0, step=1, key=f"input_{product}")
    if st.button("Добавить", key=f"add_{product}"):
        # Убедимся, что 'data' существует в сессии
        if 'data' not in st.session_state:
            st.session_state['data'] = {category: 0 for category in ALL_PRODUCT_CATEGORIES}
        st.session_state['data'][product] = st.session_state['data'].get(product, 0) + quantity
        save_data_to_file(st.session_state['username'], st.session_state['data'])
        st.success(f"Добавлено: {quantity} к '{product}'. Возврат в главное меню.")
        go_to_main_menu()
        st.rerun()

# НАЙДИТЕ СТРОЧКУ НИЖЕ И ЗАМЕНИТЕ ВСЁ, ЧТО ИДЕТ ПОСЛЕ НЕЕ, НА ЭТОТ КОД:

def display_report():
    """Отображает итоговый отчет."""
    st.header("Отчет")
    
    report_lines = []
    # Мы проходимся по нашему главному списку продуктов, чтобы порядок всегда был одинаковый
    for i, product in enumerate(ALL_PRODUCT_CATEGORIES, 1):
        # Вежливо и безопасно спрашиваем у памяти, какое количество для этого продукта записано.
        # Если ничего нет, считаем, что это 0.
        count = st.session_state.get('data', {}).get(product, 0)
        report_lines.append(f"{i}. {product} - {count}")

    # Выводим весь отчет как единый красивый текст
    st.markdown(f"<div class='report-text'>{'<br>'.join(report_lines)}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True) # Небольшой отступ
    
    # Кнопки для управления
    st.button("Сбросить", on_click=reset_data)
    st.button("Вернуться в основное меню", on_click=go_to_main_menu)


# --- ГЛАВНАЯ ЧАСТЬ ПРОГРАММЫ (НАШ "ДИРИЖЕР") ---
# ЗАМЕНИТЕ ВАШУ ФУНКЦИЮ MAIN НА ЭТУ
def main():
    """Основная функция, запускающая приложение."""
    set_styles()
    
    # Получаем доступ к "станоку для карт" в самом начале
    cookies = stx.CookieManager()
    
    # ПРОВЕРКА "КАРТЫ-КЛЮЧА":
    # Пытаемся прочитать имя пользователя из cookie
    username_from_cookie = cookies.get('username')
    
    # Инициализируем состояние, но теперь с оглядкой на cookie
    if 'username' not in st.session_state:
        st.session_state['username'] = username_from_cookie # Если в памяти пусто, берем имя с карты!
    
    initialize_state() # Вызываем остальную инициализацию

    # Теперь основная логика
    if st.session_state.get('username') is None:
        display_login_screen()
    else:
        if 'data_loaded' not in st.session_state:
            st.session_state['data'] = load_data_from_file(st.session_state['username'])
            st.session_state['data_loaded'] = True
        
        st.sidebar.markdown(f"Вы вошли как: **{st.session_state['username']}**")
        if st.sidebar.button("Сменить пользователя"):
            # При выходе мы должны забрать "карту-ключ" обратно!
            cookies.delete('username')
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

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

# --- КЛЮЧ ЗАЖИГАНИЯ ---
# Эта строчка запускает всю нашу программу, когда мы открываем файл.
if __name__ == "__main__":
    main()

# calculator_app.py

import streamlit as st

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

# --- УПРАВЛЕНИЕ СОСТОЯНИЕМ ---
# Это "память" нашего блокнота.
def initialize_state():
    """Инициализирует состояние сессии при первом запуске или сбросе."""
    # 'data' - это наши баночки, где мы храним числа. Вначале все по нулям.
    if 'data' not in st.session_state:
        # ИСПРАВЛЕНО: Используем правильный синтаксис для st.session_state
        st.session_state.data = {category: 0 for category in ALL_PRODUCT_CATEGORIES}
    # 'view' - запоминает, на какой страничке мы сейчас находимся.
    if 'view' not in st.session_state:
        # ИСПРАВЛЕНО:
        st.session_state.view = 'main_menu'
    # 'current_product' - запоминает, для какого продукта мы вводим число.
    if 'current_product' not in st.session_state:
        # ИСПРАВЛЕНО:
        st.session_state.current_product = None

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

def reset_data():
    """Сбрасывает все данные и возвращает в главное меню."""
    # ИСПРАВЛЕНО:
    st.session_state.data = {category: 0 for category in ALL_PRODUCT_CATEGORIES}
    go_to_main_menu()

# --- ЛОГИКА ОТОБРАЖЕНИЯ (Что мы показываем пользователю) ---

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
    # ИСПРАВЛЕНО: Получаем текущий продукт из состояния сессии
    product = st.session_state.current_product
    st.header(f"Ввод данных для: {product}")
    
    # Поле для ввода числа
    quantity = st.number_input(
        "Введите количество:",
        # ИСПРАВЛЕНО: Добавлен корректный аргумент min_value
        min_value=0,
        step=1,
        key=f"input_{product}"
    )
    
    # Кнопка "Добавить"
    if st.button("Добавить", key=f"add_{product}"):
        # ИСПРАВЛЕНО: Обновляем данные в состоянии сессии
        st.session_state.data[product] += quantity
        # ИСПРАВЛЕНО: Убрана опечатка в сообщении
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
# Она решает, какую страничку показать.
def main():
    """Основная функция, запускающая приложение."""
    set_styles()
    initialize_state()
    
    # ИСПРАВЛЕНО: Получаем текущее представление из состояния сессии
    view = st.session_state.view
    
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

if __name__ == "__main__":
    main()


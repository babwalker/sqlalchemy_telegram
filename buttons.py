# from database.db import session, Card, CategoryCards
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from aiogram.types import InlineKeyboardMarkup

# all_category_builder = InlineKeyboardBuilder()

# with session as session:
#     categores = session.query(CategoryCards).all()
    
#     for category in categores:
#         all_category_builder.button(text=f"{category.category_name}", callback_data=category.id)

# markup = InlineKeyboardMarkup



# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# button = [
#     [InlineKeyboardButton(text="вводный урок", callback_data="introductory_lesson"),
#     InlineKeyboardButton(text="пройти задание", callback_data="task_lesson")],
# ]

# lesson_button = InlineKeyboardMarkup(inline_keyboard=button)

from database.db import CategoryCards, Card, session
from database.state import NewCard
from aiogram import types, Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command("new_card")) # добавление новой карты
async def add_card_to_category(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder() # создание кнопок
    
    with session as sess: # обращаемся к сессии для взаимодействия с бд
        categories = sess.query(CategoryCards).all()
        for category in categories:
            builder.button(text=f"{category.category_name}", callback_data=f"{category.category_name}_new_card") # добавление кнопок
    
    await message.answer("В какую категорию вы хотите добавить карты", reply_markup=builder.as_markup())
    await state.set_state(NewCard.CategoryCard)
    
@router.callback_query(F.data.endswith("_new_card") == True) # проверка на то какую кнопку мы нажали, т.к если 
async def add_category_of_card(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(CategoryCard = callback.data[:-9]) # обрезаем _new_card для доступа к полноценному названию
    await callback.message.answer("Введите название карты")
    await state.set_state(NewCard.NameCard)
    await callback.answer()

@router.message(NewCard.NameCard)
async def add_name_of_card(message: types.Message, state: FSMContext):
    await state.update_data(NameCard = message.text) # добавляем значения 
    await message.answer("Введите описание карты")
    await state.set_state(NewCard.DescriptionCard)
    
@router.message(NewCard.DescriptionCard)
async def add_description_of_card(message: types.Message, state: FSMContext):
    data = await state.update_data(DescriptionCard = message.text)
    with session as sess: # обращаемся к сессии 
        category = sess.query(CategoryCards).filter(CategoryCards.category_name == "Credits").first() # выбираем первую категорию с таким названием
        new_card = Card(name=data["NameCard"], description=data["DescriptionCard"], category=category) # добавляем карту в нее
        sess.add(new_card) 
        sess.commit()
    state.clear() # удаляем все состояния 
        
@router.message(Command("show_cards"))
async def choose_category(message: types.Message):
    builder = InlineKeyboardBuilder()
    with session as sess:
        categories = sess.query(CategoryCards).all()
        for category in categories:
            builder.button(text=f"{category.category_name}", callback_data=f"{category.category_name}_show_cards")
    await message.answer("Какой категории вы хотите посмотреть карты", reply_markup=builder.as_markup())
    
@router.callback_query(F.data.endswith("_show_cards") == True)
async def show_cards(callback: types.CallbackQuery, state: FSMContext):
    data = await state.update_data(CategoryCards = callback.data[:-11])
    with session as sess:
        cards = sess.query(Card).filter(CategoryCards.category_name == data["CategoryCards"]).all()
        for card in cards:
            await callback.message.answer(
                f"""
                {card.name}
                {card.description}
                """
            )
    await callback.answer()
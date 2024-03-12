from aiogram.fsm.state import State, StatesGroup

class NewCard(StatesGroup):
    NameCard = State()
    DescriptionCard = State()
    CategoryCard = State()
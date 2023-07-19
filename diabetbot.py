from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor
import pandas as pd
import json
import asyncio
from joblib import load

userData = {
    'BMI': [28.0],
    'Sleep': [8.0],
    'SoundSleep': [6.0],
    'Pregancies': [100.0],
    'Age': [100.0],
    'JunkFood': [100.0],
    'Pdiabetes': [100.0],
    'highBP': [100.0],
    'Alcohol': [100.0],
    'RegularMedicine': [100.0],
    'Stress': [100.0],
    'PhysicallyActive': [100.0],
    'Gender': [100.0],
    'BPLevel': [100.0],
    'UriationFreq': [100.0],
    'Smoking': [100.0],
    'Family_Diabetes': [100.0]
}


bot = Bot(token='6284607069:AAFx-TK4GtMiGn4yqJ_9xuV0DmNLPIdWpGc')
dp = Dispatcher(bot)

loaded_model = load('model_4.joblib')

async def send_message(user_id, text):
    await bot.send_message(user_id, text)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'Здравствуйте! Этот бот предназначен для выявления рисков заболевания диабетом. Ответьте на несколько вопросов, чтобы посмотреть, какой у вас риск заболевания.')
    await bot.send_message(message.chat.id, 'Выберите пол:', reply_markup=keyboard)

button_male = InlineKeyboardButton('Мужской', callback_data='button_male')  
button_female = InlineKeyboardButton('Женский', callback_data='button_female')  
keyboard = InlineKeyboardMarkup().add(button_male, button_female)

smbutton1 = InlineKeyboardButton('да', callback_data='smbutton1')
smbutton2 = InlineKeyboardButton('нет', callback_data='smbutton2')
keyboard_param = InlineKeyboardMarkup().add(smbutton1, smbutton2)


keyboard_smoking = InlineKeyboardMarkup()
keyboard_smoking.row(InlineKeyboardButton('да', callback_data='smbutton1'))
keyboard_smoking.row(InlineKeyboardButton('нет', callback_data='smbutton2'))

keyboard_drinking = InlineKeyboardMarkup()
keyboard_drinking.row(InlineKeyboardButton('да', callback_data='drinkbutton1'))
keyboard_drinking.row(InlineKeyboardButton('нет', callback_data='drinkbutton2'))

keyboard_urination = InlineKeyboardMarkup()
keyboard_urination.row(InlineKeyboardButton('не часто', callback_data='urinationbutton1'))
keyboard_urination.row(InlineKeyboardButton('часто', callback_data='urinationbutton2'))

keyboard_regular_medicine = InlineKeyboardMarkup()
keyboard_regular_medicine.row(InlineKeyboardButton('да', callback_data='regularmedicinebutton1'))
keyboard_regular_medicine.row(InlineKeyboardButton('нет', callback_data='regularmedicinebutton2'))

keyboard_high_bp = InlineKeyboardMarkup()
keyboard_high_bp.row(InlineKeyboardButton('да', callback_data='highbpbutton1'))
keyboard_high_bp.row(InlineKeyboardButton('нет', callback_data='highbpbutton2'))

keyboard_pdiabetes = InlineKeyboardMarkup()
keyboard_pdiabetes.row(InlineKeyboardButton('да', callback_data='pdiabetesbutton1'))
keyboard_pdiabetes.row(InlineKeyboardButton('нет', callback_data='pdiabetesbutton2'))

keyboard_family_diabetes = InlineKeyboardMarkup()
keyboard_family_diabetes.row(InlineKeyboardButton('да', callback_data='familydiabetesbutton1'))
keyboard_family_diabetes.row(InlineKeyboardButton('нет', callback_data='familydiabetesbutton2'))

keyboard_bp_level = InlineKeyboardMarkup()
keyboard_bp_level.row(InlineKeyboardButton('низкий', callback_data='bp_level_low'))
keyboard_bp_level.row(InlineKeyboardButton('нормальный', callback_data='bp_level_normal'))
keyboard_bp_level.row(InlineKeyboardButton('высокий', callback_data='bp_level_high'))

keyboard_stress = InlineKeyboardMarkup()
keyboard_stress.row(InlineKeyboardButton('не испытываю совсем', callback_data='stress_not'))
keyboard_stress.row(InlineKeyboardButton('иногда', callback_data='stress_sometimes'))
keyboard_stress.row(InlineKeyboardButton('часто', callback_data='stress_often'))
keyboard_stress.row(InlineKeyboardButton('всегда', callback_data='stress_always'))

keyboard_physically_active = InlineKeyboardMarkup()
keyboard_physically_active.row(InlineKeyboardButton('больше одного часа', callback_data='physically_active_one_hr_or_more'))
keyboard_physically_active.row(InlineKeyboardButton('больше 30 минут', callback_data='physically_active_more_than_half_hr2'))
keyboard_physically_active.row(InlineKeyboardButton('меньше 30 минут', callback_data='physically_active_less_than_half_hr1'))
keyboard_physically_active.row(InlineKeyboardButton('не занимаюсь', callback_data='physically_active_none'))

keyboard_junk_food = InlineKeyboardMarkup()
keyboard_junk_food.row(InlineKeyboardButton('редко', callback_data='junk_food_occasionally'))
keyboard_junk_food.row(InlineKeyboardButton('часто', callback_data='junk_food_often'))
keyboard_junk_food.row(InlineKeyboardButton('очень часто', callback_data='junk_food_very_often'))
keyboard_junk_food.row(InlineKeyboardButton('всегда', callback_data='junk_food_always'))

keyboard_pregnancies = InlineKeyboardMarkup()
keyboard_pregnancies.row(InlineKeyboardButton('0', callback_data='pregnancies_0'))
keyboard_pregnancies.row(InlineKeyboardButton('1', callback_data='pregnancies_1'))
keyboard_pregnancies.row(InlineKeyboardButton('2', callback_data='pregnancies_2'))
keyboard_pregnancies.row(InlineKeyboardButton('3', callback_data='pregnancies_3'))
keyboard_pregnancies.row(InlineKeyboardButton('4', callback_data='pregnancies_4'))


@dp.callback_query_handler(lambda c: c.data == 'button_male' or c.data == 'button_female')
async def process_button_pressed(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    gender = callback_query.data
    
    if gender == 'button_male':
        userData['Gender'][0] = 1.0  
    elif gender == 'button_female':
        userData['Gender'][0] = 0.0  
    
    await bot.send_message(user_id, 'Вы курите?', reply_markup=keyboard_smoking)


@dp.callback_query_handler(lambda c: c.data == 'smbutton1' or c.data == 'smbutton2')
async def process_smoking_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    smoking = callback_query.data
    
    if smoking == 'smbutton1':
        userData['Smoking'][0] = 1.0  
    elif smoking == 'smbutton2':
        userData['Smoking'][0] = 0.0
    
    await bot.send_message(user_id, 'Вы пьете?', reply_markup=keyboard_drinking)


@dp.callback_query_handler(lambda c: c.data == 'drinkbutton1' or c.data == 'drinkbutton2')
async def process_drinking_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    drinking = callback_query.data
    
    if drinking == 'drinkbutton1':
        userData['Alcohol'][0] = 1.0  
    elif drinking == 'drinkbutton2':
        userData['Alcohol'][0] = 0.0
    
    await bot.send_message(user_id, 'Частота мочеиспускания?', reply_markup=keyboard_urination)


@dp.callback_query_handler(lambda c: c.data == 'urinationbutton1' or c.data == 'urinationbutton2')
async def process_urination_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    urination = callback_query.data
    
    if urination == 'urinationbutton1':
        userData['UriationFreq'][0] = 0.0  
    elif urination == 'urinationbutton2':
        userData['UriationFreq'][0] = 1.0
    
    await bot.send_message(user_id, 'Регулярно ли вы используете лекарства в повседневной жизни?', reply_markup=keyboard_regular_medicine)


@dp.callback_query_handler(lambda c: c.data == 'regularmedicinebutton1' or c.data == 'regularmedicinebutton2')
async def process_regular_medicine_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    regular_medicine = callback_query.data
    
    if regular_medicine == 'regularmedicinebutton1':
        userData['RegularMedicine'][0] = 1.0  
    elif regular_medicine == 'regularmedicinebutton2':
        userData['RegularMedicine'][0] = 0.0
    
    await bot.send_message(user_id, 'У вас высокое кровяное давление?', reply_markup=keyboard_high_bp)


@dp.callback_query_handler(lambda c: c.data == 'highbpbutton1' or c.data == 'highbpbutton2')
async def process_high_bp_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    high_bp = callback_query.data
    
    if high_bp == 'highbpbutton1':
        userData['highBP'][0] = 1.0  
    elif high_bp == 'highbpbutton2':
        userData['highBP'][0] = 0.0
    
    await bot.send_message(user_id, 'Был ли у вас гестационный диабет во время беременности?(если вы мужчина, ответьте "нет")', reply_markup=keyboard_pdiabetes)


@dp.callback_query_handler(lambda c: c.data == 'pdiabetesbutton1' or c.data == 'pdiabetesbutton2')
async def process_pdiabetes_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    pdiabetes = callback_query.data
    
    if pdiabetes == 'pdiabetesbutton1':
        userData['Pdiabetes'][0] = 1.0  
    elif pdiabetes == 'pdiabetesbutton2':
        userData['Pdiabetes'][0] = 0.0
    
    await bot.send_message(user_id, 'Есть ли в вашей семье случаи заболевания диабетом?', reply_markup=keyboard_family_diabetes)


@dp.callback_query_handler(lambda c: c.data == 'familydiabetesbutton1' or c.data == 'familydiabetesbutton2')
async def process_family_diabetes_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    family_diabetes = callback_query.data
    
    if family_diabetes == 'familydiabetesbutton1':
        userData['Family_Diabetes'][0] = 1.0  
    elif family_diabetes == 'familydiabetesbutton2':
        userData['Family_Diabetes'][0] = 0.0
    
    await bot.send_message(user_id, 'Какой у вас уровень кровяного давления?', reply_markup= keyboard_bp_level)


@dp.callback_query_handler(lambda c: c.data.startswith('bp_level_'))
async def process_bp_level_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    bp_level = callback_query.data.split('_')[-1]

    if bp_level == 'low':
        userData['BPLevel'][0] = 0.0
    elif bp_level == 'normal':
        userData['BPLevel'][0] = 1.0
    elif bp_level == 'high':
        userData['BPLevel'][0] = 2.0
    
    await bot.send_message(user_id, 'Как часто вы испытываете стресс?', reply_markup=keyboard_stress)


@dp.callback_query_handler(lambda c: c.data.startswith('stress_'))
async def process_stress_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    stress = callback_query.data.split('_')[-1]
    
    if stress == 'not':
        userData['Stress'][0] = 0.0
    elif stress == 'sometimes':
        userData['Stress'][0] = 1.0
    elif stress == 'often':
        userData['Stress'][0] = 2.0
    elif stress == 'always':
        userData['Stress'][0] = 3.0

    await bot.send_message(user_id, 'Сколько времени вы тратите на занятие спортом ежедневно?', reply_markup=keyboard_physically_active)


@dp.callback_query_handler(lambda c: c.data.startswith('physically_active_'))
async def process_physically_active_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    physically_active = callback_query.data.split('_')[-1]
    
    if physically_active == 'more':
        userData['PhysicallyActive'][0] = 3.0
    elif physically_active == 'hr2':
        userData['PhysicallyActive'][0] = 2.0
    elif physically_active == 'hr1':
        userData['PhysicallyActive'][0] = 1.0
    elif physically_active == 'none':
        userData['PhysicallyActive'][0] = 0.0

    await bot.send_message(user_id, 'Как часто вы едите фастфуд?', reply_markup=keyboard_junk_food)

keyboard_age = InlineKeyboardMarkup()
keyboard_age.row(InlineKeyboardButton('меньше 40', callback_data='age_less_than_40'))
keyboard_age.row(InlineKeyboardButton('от 40 до 49', callback_data='age_40_49'))
keyboard_age.row(InlineKeyboardButton('от 50 до 59', callback_data='age_50_59'))
keyboard_age.row(InlineKeyboardButton('60 и старше', callback_data='age_60_or_older'))


@dp.callback_query_handler(lambda c: c.data.startswith('junk_food_'))
async def process_junk_food_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    junk_food = callback_query.data.split('_')[-1]
    
    if junk_food == 'occasionally':
        userData['JunkFood'][0] = 0.0
    elif junk_food == 'often':
        userData['JunkFood'][0] = 1.0
    elif junk_food == 'veryoften':
        userData['JunkFood'][0] = 2.0
    elif junk_food == 'always':
        userData['JunkFood'][0] = 3.0
    
    await bot.send_message(user_id, 'Выберите свой возраст', reply_markup=keyboard_age)



@dp.callback_query_handler(lambda c: c.data.startswith('age_'))
async def process_age_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    age = callback_query.data.split('_')[-1]
    
    if age == '40':
        userData['Age'][0] = 0.0
    elif age == '49':
        userData['Age'][0] = 1.0
    elif age == '59':
        userData['Age'][0] = 2.0
    elif age == 'older':
        userData['Age'][0] = 3.0

    await bot.send_message(user_id, 'Сколько у вас было беременностей?( если вы мужчина, выберите 0', reply_markup=keyboard_pregnancies)


@dp.callback_query_handler(lambda c: c.data.startswith('pregnancies_'))
async def process_pregnancies_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    pregnancies = callback_query.data.split('_')[-1]
    userData['Pregancies'][0] = float(pregnancies)

    # await bot.send_message(user_id, 'bmi?')
    with open('userData.json', 'w') as file:
        json.dump(userData, file)

    # Вывод значений userData в терминал
    print("Обновленные данные пользователя:")
    for key, value in userData.items():
        print(f"{key}: {value}")




    df = pd.DataFrame(userData)
    predictions = loaded_model.predict(df)
    risk_mapping = {0: "У вас низкий риск заболевания диабетом. Не забывайте время от времени сдавать анализы для профилактики возникновения возможных недугов.", 1: "У вас высокий риск заболевания диабетом. Вам следует проконсультироваться с врачом."}
    prediction_texts = [risk_mapping[prediction] for prediction in predictions]
    result_message = "Результаты предсказаний:\n" + "\n".join(prediction_texts)
    await send_message(user_id, result_message)

@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    print(f"User ID: {user_id}")

if __name__ == '__main__':
    executor.start_polling(dp)









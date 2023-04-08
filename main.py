from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from db import db
import asyncio
import aioschedule as schedule
from datetime import datetime, time
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton



TOKEN = '6089869534:AAGshFvUlhDE15DVthci1uEpFRcXsRLxNwg'
path = "base.db"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)    
base = db(path)

now = datetime.now()
#print(now)
newnow = str(now).split(' ')
#print('newnow = ', newnow)
newnow = newnow[0].replace('-', '.')
#print('newnow = ',newnow)
#print()
#users_ids = base.get_users_id()
#print(users_ids)
#for user in users_ids:
#    dates = base.get_dates(str(user[0]))
#    print('\t',dates)
#    for x in dates:
#        if x[0] < newnow:
#            print(f"Эй выполни задачу! Срок закончился еще в {x[0]}")





# conn = sqlite3.connect(path)
# cur = conn.cursor()
# # Create users table
# cur.execute('''CREATE TABLE users
#                (user_id INTEGER PRIMARY KEY,
#                user_name TEXT)''')

# # Create tasks table
# cur.execute('''CREATE TABLE tasks
#                (id INTEGER PRIMARY KEY,
#                task_name TEXT,
#                to_be_done_date TEXT,
#                is_done INTEGER,
#                user_id TEXT)''')
# conn.commit()


#@dp.message_handler(commands=['clear'])
#async def clear_chat(msg : types.Message):
#    await bot.delete_message(msg.from_user. , msg.chat.id)

button1 = KeyboardButton('/start')
button5 = KeyboardButton('/help')
button2 = KeyboardButton('/show_all_tasks')
button3 = KeyboardButton('/add_task')
button4 = KeyboardButton('/set_done')

markup3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    button1).add(button2).add(button3).add(button4).add(button5)


@dp.message_handler(commands=['start', 'help'])
async def process_start_command(message: types.Message):
        if base.is_consist(message.from_user.id) == False:
            base.add_user(message.from_user.id, message.from_user.username)
        await bot.send_message(message.chat.id,"Привет! Это бот-помошник менеджер задач.\nВведите:\n/add_task 'название задачи' 'дату конца задачи (гг.мм.дд)' - что бы добавить задачу\n/show_all_tasks - что бы посмотреть имеющиеся задачи\n/set_done 'название задачи' - что бы задать задау сделанной", reply_markup=markup3)

@dp.message_handler(commands=['show_all_tasks'])
async def process_start_command(message: types.Message):
    try:
        show = base.show_tasks(message.from_user.id)        
        print(show)
        txt = ''
        i = 0
        for x in show:
            if x[3] == False:
                txt = txt + str(i + 1) + '. ' + x[1] + ' ' + x[2] + ' Не выполнено' + '\n'
            else:
                txt = txt + str(i + 1) + '. ' + x[1] + ' ' + x[2] + ' Выполнено' + '\n'
                #await bot.send_message(message.chat.id,txt)
            i += 1
            pass
        await bot.send_message(message.chat.id,txt)
        #await message.reply(message.chat.id, s)
    except:
        await bot.send_message(message.chat.id, 'Задачи отсутствуют!!!')



@dp.message_handler(commands=['add_task'])
async def echo_message(msg: types.Message):
    try:
        ussr = msg.text.split(' ')
        base.add_task(ussr[1], ussr[2], msg.from_user.id)    
        await bot.send_message(msg.chat.id, 'Задача добвалена успешно!')
    except:
        await bot.send_message(msg.chat.id, 'Задача указана неккоректно!!!')



@dp.message_handler(commands=['set_done'])
async def echo_message(msg: types.Message):
    try:
        ussr = msg.text.split(' ')
        base.set_done(ussr[1])
        await bot.send_message(msg.chat.id, 'Задача сделана успешно!')
    except:
        await bot.send_message(msg.chat.id, 'Не указано название!!!')

#for x in base.get_users_id():
#        print(x)
#        pass

#async def daily_mess():
#    users_ids = base.get_users_id()

#    for x in users_ids:
#        print('Ураа')        
#        await bot.send_message(x, f'прошел день! Выполните задачу')
#    asyncio.sleep(1)


#schedule.every(60).seconds.do(daily_mess)

# name = base.get_task_by_date('2023.04.07')
# print('name ', name[0][0])
# state = base.get_state_by_date('2023.04.07')
# print('state ', state[0][0])

#Нужно доделать проверку даты задачи с нынешней датой, и только потом отправлять уведомления
async def daily_mess():
    # print('it is func')
    users_ids = base.get_users_id()
    # print(users_ids)
    for user in users_ids:
        dates = base.get_dates(str(user[0]))
        # print('\t',dates)
        for x in dates:
            name = base.get_task_by_date(str(x[0]))
            state = base.get_state_by_date(str(x[0]))
            if x[0] < newnow and state[0][0] == 0:
                await bot.send_message(chat_id = user[0], text = f"Эй выполни задачу '{name[0][0]}'! Срок закончился еще в {x[0]}")
    
    pass



async def scheduler():
    # print('it is scheduler')

    schedule.every().day.at("10:30").do(daily_mess)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)
        
async def on_startup(dp): 
    # print('it is start up')
    asyncio.create_task(scheduler())
    
    
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
    # executor.start_polling(dp)
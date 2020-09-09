import telebot
import config
from telebot import types # buttons
from string import Template



bot = telebot.TeleBot(config.token)

user_dict = {}
calc_dict = {}

class User:
    def __init__(self, city):
        self.city = city

        keys = ['fullname', 'phone', 'driverSeria', 'carDate', 'userHeight', 'userId']
        
        for key in keys:
            self.key = None

class Calc:
    def __init__(self, active):
        self.active = active
        keys = ['height', 'weight', 'age']
        for key in keys:
            self.key = None


# если /help, /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/about')
    itembtn2 = types.KeyboardButton('/reg')
    itembtn3 = types.KeyboardButton('/calc')
    markup.add(itembtn1, itembtn2, itembtn3)
    
    bot.send_message(message.chat.id, "Привіт, "
    + message.from_user.first_name
    + ", я бот-помічник, я допоможу тобі використати час з користю і ефективно скористатись функціями марафону, обира йщо тебе цікавить!", reply_markup=markup)

# /about
@bot.message_handler(commands=['about'])
def send_about(message):
	bot.send_message(message.chat.id, "Що входить в марафон? \n\n" +
    "1. 15 відео-тренувань.\n\n"
" 2. Щоденна підтримка і консультація від тренера.\n\n" +
 "3. Практичні завдання для кращого засвоєння матеріалу.\n\n" +
 "4. Спілкування з іншими учасниками.\n\n" +
 "5. Відповіді на всі ваші питання.\n\n" +
 "6. Кожного дня поступатиме нова інформація по дієтології:\n\n" +

 " ⁃ Калораж. Формула денної норми Ккал. Дефіцит і профіцит Ккал.\n" +
 " ⁃ БЖВ ( білки, жири, вуглеводи)\n" +
 " ⁃ Гормони. Гормональний збій. Симптоми. Що робити по гормональному збої.\n" +
 " ⁃ Амінорея. Жіноче здоров‘я. Як лікувати.\n" +
 " ⁃ Інсулін. Інсулінорезистентність.\n" +
 " ⁃ Глікемічний індекс.\n" +
 " ⁃ Ефект Плато.\n" +
 " ⁃ Холестерин. Чи справді він такий страшний?\n" +
 " ⁃ Клітковина.\n" +
 " ⁃ Транс-жири.\n" +
 " ⁃ Продукти, які варто забрати з вашого раціону.\n" +
 " ⁃ Чим замінити найшкідливіші продукти? \n" +
 " ⁃ 15 зруйнованих міфів.\n" +
 " ⁃ Вітаміни.\n" +
 " ⁃ Водний баланс. \n" +
 " ⁃ Відновлення. \n" +
 " ⁃ Сон.\n" +
 " ⁃ Звички, які допоможуть швидко позбутись лишніх сантиметрів.\n" +
 " ⁃ Тренування під час КД.\n" +
 " ⁃ Проблемні зони. Як позбутись мішечка внизу живота.\n" +
 " ⁃ Монодієта. Кето дієта. Інтервальне голодування. Інтуїтивне харчування. БУЧ дієта.\n" +
 " ⁃ Переїдання.\n" +
 " ⁃ Зриви. \n" +
 " ⁃ Як зробити розгрузочний день.\n" +
 " ⁃ Чітміл.\n" +
 " ⁃ Як розігнати метаболізм.\n" +
 " ⁃ Як відмовитись від солодкого? Рецепти корисних солодощів.\n" +
 " ⁃ Приклади сніданків, обідів і вечерь (фото).")

# /reg
@bot.message_handler(commands=["reg"])
def user_reg(message):
       markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
       itembtn1 = types.KeyboardButton('Київ')
       itembtn2 = types.KeyboardButton('Одеса')
       itembtn3 = types.KeyboardButton('Тернопіль')
       itembtn6 = types.KeyboardButton('Львів')
       markup.add(itembtn1, itembtn2, itembtn3, itembtn6)

       msg = bot.send_message(message.chat.id, 'Ваше місто', reply_markup=markup)
       bot.register_next_step_handler(msg, process_city_step)

def process_city_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'Прізвище та імя', reply_markup=markup)
        bot.register_next_step_handler(msg, process_fullname_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

def process_fullname_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text

        msg = bot.send_message(chat_id, 'Ваш номер телефону')
        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

def process_phone_step(message):
    try:
        int(message.text)

        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, 'Ваш вік')
        bot.register_next_step_handler(msg, process_driverSeria_step)

    except Exception as e:
        msg = bot.reply_to(message, 'Введіть номер телефону ще раз')
        bot.register_next_step_handler(msg, process_phone_step)

def process_driverSeria_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.driverSeria = message.text

        msg = bot.send_message(chat_id, 'Ваша вага')
        bot.register_next_step_handler(msg, process_carDate_step)

    except:
        bot.reply_to(message, '25')

def process_carDate_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.carDate = message.text

       
        msg = bot.send_message(chat_id, 'Ваш зріст')
        bot.register_next_step_handler(msg, process_joinedFile_step)

    except Exception as e:
        bot.reply_to(message, '23')

def process_joinedFile_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.userHeight = message.text

        joinedFile = open('users.txt', 'r')
        joinedUsers = set()
        for line in joinedFile:
            joinedUsers.add(line.strip())
        if not str(message.chat.id) in joinedUsers:
            joinedFile = open('users.txt', 'a')
            joinedFile.write(str(message.chat.id) + '\n')
            joinedUsers.add(message.chat.id)  


        msg = bot.send_message(chat_id, "Що ви очікуєте від марафону?")
        bot.register_next_step_handler(msg, process_regJoin_step)

    except Exception as e:
        bot.reply_to(message, '22')

def process_regJoin_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.userId = message.chat.id


        msg = bot.send_message(chat_id, 'Яку вагу ви бажаєте мати?')
        bot.register_next_step_handler(msg, process_finalP_step)
 
        

    except Exception as e:
        bot.reply_to(message, '21')
def process_finalP_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Перейти до оплати", url="http://secure.wayforpay.com/button/b083da34b089d")
        keyboard.add(url_button)
        bot.send_message(message.chat.id, "Привіт! А ось і час оплати.", reply_markup=keyboard)     
        # ваша заявка "Имя пользователя"
        ms = 'Ваша заявка \n' + 'Посилання на нашу групув телеграмі - https://t.me/joinchat/HP2hixfysFoUVw1btCWW-A'
        bot.send_message(chat_id, getRegData(user, ms, message.from_user.first_name), parse_mode="Markdown")
        # отправить в группу
        bot.send_message(config.chat_id, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown")    
    except Exception as e:
        bot.reply_to(message, '20')
# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template("$title *$name* \n Місто: *$userCity* \n Пізвище ім'я: *$fullname* \n Телефон: *$phone* \n Вік: *$driverSeria* \n Вага: *$carDate* \n Зріст: *userHeight* \n id: *userId*")

    return t.substitute({
        'title': title,
        'name': name,
        'userCity': user.city,
        'fullname': user.fullname,
        'phone': user.phone,
        'driverSeria': user.driverSeria,
        'carDate': user.carDate,
        'userHeight': user.userHeight,
        'userId': user.userId,
    })

@bot.message_handler(commands = ["calc"])
def user_calc(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Сидяча робота\навчання ')
    itembtn2 = types.KeyboardButton('Пробіжка\легка гімнастика')
    itembtn3 = types.KeyboardButton('Заняття спортом')
    itembtn4 = types.KeyboardButton('Повноцінні заняття спортом')
    itembtn5 = types.KeyboardButton("Ваша робота пов'язана з фізичною активнсттю")
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

    msg = bot.send_message(message.chat.id, 'Ваша нагрузка', reply_markup=markup)
    bot.register_next_step_handler(msg, user_height)
def user_height(message):    
    try:
        chat_id = message.chat.id
        calc_dict[chat_id] = Calc(message.text)

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'Ваш зріст в см', reply_markup=markup)
        bot.register_next_step_handler(msg, user_weight)
    except Exception as e:
        bot.reply_to(message, 'User_height error')    
def user_weight(message):
    try:
        chat_id = message.chat.id
        calc = calc_dict[chat_id]
        calc.height = message.text

        msg = bot.send_message(chat_id, 'Ваша вага в кг')
        bot.register_next_step_handler(msg, user_age)
    except Exception as e:
        bot.reply_to(message, 'user_weight error')
def user_age(message):
    try:
        chat_id = message.chat.id
        calc = calc_dict[chat_id]
        calc.weight = message.text

        msg = bot.send_message(chat_id, 'Ваш вік')
        bot.register_next_step_handler(msg, make_mess)
    except Exception as e:
        bot.reply_to(message, 'user_age error')
def make_mess(message):
    chat_id = message.chat.id
    calc = calc_dict[chat_id]
    calc.age = message.text
    height = int(calc.height)
    weight = int(calc.weight)
    age = int(calc.age) 

    if calc.active == "Сидяча робота\навчання без фіз. навантажень":
        kof = 1.2
    elif calc.active == "Пробіжка і легка гімнастика 1-3 рази в тиждень":
        kof = 1.375
    elif calc.active == "Заняття спортом 3-5 рази в тиждень з середніми навантаженями":
        kof = 1.55
    elif calc.active == "Повноцінні заняття спортом 6-7 раз в тиждень":
        kof = 1.725
    else:
        kof = 1.9            

    calorage = (10 * weight) + (6.25 * height) - (5 * age) - 161
    bot.send_message(chat_id, 'Калораж: ' + str(calorage * kof))



@bot.message_handler(content_types=["text"])
def mailing_text(message):
    if int(message.chat.id) == int(config.owner_id):
        msg = message.text
        users = open('users.txt', 'r')
        for user in users:
            bot.send_message(user, msg)
    else:
        bot.send_message(message.chat.id, 'Скористайтесь функцією /help')   
@bot.message_handler(content_types=["photo"])
def mailing_photo(message):
    if int(message.chat.id) == int(config.owner_id):
        chat_id = config.owner_id
        msg = message.message_id
        users = open('users.txt', 'r')
        for user in users:
            bot.forward_message(user, int(chat_id), int(msg))
    else:
        bot.send_message(message.chat.id, 'Скористайтесь функцією /help')    
@bot.message_handler(content_types = ["video"])
def mailing_video(message):
    if int(message.chat.id) == int(config.owner_id):
        chat_id = config.owner_id
        users = open('users.txt', 'r')
        msg = message.message_id
        for user in users:
            bot.forward_message(user, int(chat_id), int(msg))         

  
# произвольный текст


# произвольное фото


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

#payment

#mailing


if __name__ == '__main__':
    bot.polling(none_stop=True)

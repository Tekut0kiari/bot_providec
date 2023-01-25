import telebot
from pyowm import OWM

token = '5883283336:AAEsHWE17Ct22yX1QlbGxDikAawvMI9N5XI'
bot = telebot.TeleBot(token)



@bot.message_handler(commands=['start'])
def helloMessage (message):
    bot.send_message(message.chat.id, 'Приветствую тебя! Ты можешь написать мне любой город и я покажу какая там сейчас погода, для этого используй команду /weather ')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/weather':
        bot.send_message(message.from_user.id, 'Введи название города в котором хочешь узнать погоду')
        bot.register_next_step_handler(message, get_weather)
    else:
        bot.send_message(message.from_user.id, 'Напиши /weather')



def get_location(lat, lon):
    url = f"https://yandex.ru/pogoda/maps/nowcast?lat={lat}&lon={lon}&via=hnav&le_Lightning=1"
    return url


def weather(city: str):
    owm = OWM('53acc7e577a9e940b4908a410ca90445')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    location = get_location(observation.location.lat, observation.location.lon)
    temperature = weather.temperature('celsius')
    return temperature, location


def get_weather(message):
    city = message.text
    try:
        w = weather(city)
        bot.send_message(message.from_user.id, f'Итак {city}, сейчас там {round(w[0]["temp"])} °C,'
                                               f' но ты будешь ощущать как {round(w[0]["feels_like"])} °C')
        bot.send_message(message.from_user.id, w[1])
        bot.send_message(message.from_user.id, "Если хочешь можешь узнать погоду где-нибудь еще,для этого введи название города ")
        bot.register_next_step_handler(message, get_weather)

    except Exception:
        bot.send_message(message.from_user.id, 'Опа-а-а-а-а.... связь с космосом потеряна, не вижу такого города')
        bot.send_message(message.from_user.id, "Но ты можешь попробовать какой нибудь другой город")
        bot.register_next_step_handler(message, get_weather)

bot.polling(none_stop=True, interval=0)
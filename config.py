
import telebot
import database

TOKEN = "6052229593:AAFZ7aiWk9--c_0yle3P2Uw1VTNXdPg7tUM"
URL = 'CHMZAP'
key = ['CHMZAP']
bot = telebot.TeleBot(TOKEN, threaded=False)
db = database.Database('chmzap_sq.sqlite')

# connection_config_dict = {
#     'user': 'ShelepovFamily',
#     'password': 'CHMZAP100-01',
#     'host': 'ShelepovFamily.mysql.pythonanywhere-services.com',
#     'database': 'ShelepovFamily$CHMZAP'
# }

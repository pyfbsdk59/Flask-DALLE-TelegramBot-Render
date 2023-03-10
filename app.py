import logging

import telegram, os
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters



#################
import openai
	
openai.api_key = os.getenv("OPENAI_API_KEY") 


class Dalle:  
    

    def __init__(self):
        
        self.image_url = ""



    def get_response(self, user_input):
        #import openai
        #openai.api_key = openai.api_key
        response = openai.Image.create(
            prompt = user_input,
                n=1,
            size="1024x1024"
            )
        self.image_url = response['data'][0]['url'].strip()
        print(self.image_url)


        
        return self.image_url





#####################

telegram_bot_token = str(os.getenv("TELEGRAM_BOT_TOKEN"))



# Load data from config.ini file
#config = configparser.ConfigParser()
#config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=telegram_bot_token)



@app.route('/callback', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'


def reply_handler(bot, update):
    """Reply message."""

    dalle = Dalle()      
    
                                            #update.message.text 人類的關鍵字 the keywords humans asked
    dalle_reply_url = dalle.get_response(update.message.text) #Dalle產生的圖片URL the url of the pic that Dalle gave
    
    update.message.reply_photo(dalle_reply_url) #用AI的文字URL回傳照片 reply the url that AI made


# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    # Running server
    app.run(debug=True)

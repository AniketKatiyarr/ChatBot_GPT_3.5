from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import openai
import sys


class Reference:
    '''
    A class to store previously response from the chatGPT API
    '''

    def __init__(self) -> None:
        self.response = ""


load_dotenv()
openai.api_key = os.getenv("OpenAI_API_KEY")  

reference = Reference()

TOKEN = os.getenv("TOKEN")

#model name
MODEL_NAME = "gpt-3.5-turbo"


# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = ""



@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Hi\nI am Chat Bot!\Created by Aniket Katiyar. How can i assist you?")



@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")



@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm chatGPT Telegram bot created by Bappy! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)



@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")

    # Prepare the request payload
    prompt = f"{reference.response}\nUser: {message.text}\nAI:"
    completion = openai.Completion.create(
        model=MODEL_NAME,
        prompt=prompt,
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    reference.response += message.text + '\n' + completion.choices[0].text.strip() + '\n'

    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id=message.chat.id, text=completion.choices[0].text.strip())


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)

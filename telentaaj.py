import fitz
from PIL import Image
import os
import logging
import telebot
from IPython.display import display
import re
# Replace 'YOUR_BOT_TOKEN' with the actual bot token you obtained from BotFather
BOT_TOKEN = '5371447772:AAFkU_J4WRO3u2tVePMmUptlhvFVgQkguLM'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a TeleBot object
bot = telebot.TeleBot(BOT_TOKEN)

# Function to handle the /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "مرحبا دز رقمك الامتحاني وانتظر ثواني")


import re

# Function to handle text messages
@bot.message_handler(func=lambda message: True)
def search_pdf(message):
    search_word = message.text

    # Check if the message is a 13-digit number
    if not re.match(r'^\d{13}$', search_word):
       # bot.send_message(message.chat.id, "الرجاء إدخال رقم مكون من 13 رقم.")
        return

    folder_path = '/content'  # Update this path as needed

    # Initialize the search_found variable to False
    search_found = False

    # Your existing code to search for the word and capture the image
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            pdf_document = fitz.open(pdf_path)

            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                text = page.get_text()
                if search_word in text:
               #    bot.reply_to(message, "لحظة")
               #    bot.send_message(message.chat.id, "لحظة")
                    user_username = message.from_user.username
                    caption = f"@{user_username}"

                    screenshot = page.get_pixmap()
                    pil_image = Image.frombytes("RGB", [screenshot.width, screenshot.height], screenshot.samples)
                    image_filename = "1.png"
                    image_path = os.path.join(folder_path, image_filename)
                    pil_image.save(image_path, quality=200)

                    print(f"The num '{search_word}' was found on page {page_number + 1} in file '{filename}' and the image has been saved as '{image_filename}'")

                    with open(image_path, 'rb') as photo:
                #       bot.reply_to(message, photo)
                #       bot.send_photo(message.chat.id, photo)
                        bot.send_photo(message.chat.id, photo, caption=caption)

                    # Set the search_found variable to True
                    search_found = True

                    # Stop searching once the first result is found
                    break

            pdf_document.close()

            # Stop searching in other files once the first result is found
            if search_found:
                break

    # Check if the search word was not found and send apology message
    if not search_found:
        bot.send_message(message.chat.id, f"عذراً، لم يتم العثور على '{search_word}' في الملفات المتاحة.")

# Set up the main function
def main():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()

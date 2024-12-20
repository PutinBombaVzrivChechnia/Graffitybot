import io
from PIL import Image, ImageDraw, ImageFont
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

   # Функция для создания изображения с текстом
def create_image_with_text(text):
       # Параметры изображения
       width, height = 400, 200
       image = Image.new('RGB', (width, height), (255, 255, 255))
       draw = ImageDraw.Draw(image)

       # Задаем шрифт
       try:
           font = ImageFont.truetype("arial.ttf", 30)  # Убедитесь, что шрифт доступен
       except IOError:
           font = ImageFont.load_default()

       # Определяем позицию текста
       text_width, text_height = draw.textsize(text, font=font)
       text_x = (width - text_width) / 2
       text_y = (height - text_height) / 2

       # Рисуем текст
       draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)

       return image

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
       await update.message.reply_text('Привет! Напиши текст, и я создам изображение с ним!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
       user_text = update.message.text
       image = create_image_with_text(user_text)

       # Сохраняем изображение в байтовый поток
       buf = io.BytesIO()
       image.save(buf, format='PNG')
       buf.seek(0)

       # Отправляем изображение обратно пользователю
       await update.message.reply_photo(photo=buf)

async def main() -> None:
       application = ApplicationBuilder().token("8092463464:AAElDP3ffNBK3jzEnUwjHKhneyiZL1Zv1Mo").build()

       application.add_handler(CommandHandler("start", start))
       application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

       await application.run_polling()

if __name__ == '__main__':
       import asyncio
       asyncio.run(main())
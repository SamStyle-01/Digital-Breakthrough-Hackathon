import asyncio
import logging
import sys
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment

from aiogram import Bot, Dispatcher, types, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

TOKEN = # Вставить токен здесь
dp = Dispatcher()
times = 0


def recognize_speech_from_audio(audio_bytes, audio_format="ogg"):
    audio = AudioSegment.from_file(BytesIO(audio_bytes), format=audio_format)

    wav_io = BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)  # Обнуляем указатель для дальнейшего чтения


    # Используем SpeechRecognition для распознавания речи
    recognizer = sr.Recognizer()
    text = ""
    with sr.AudioFile(wav_io) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ru-RU")
            text = f"Распознанный текст: {text}"
        except sr.UnknownValueError:
            text = "Не удалось распознать голос."
        except sr.RequestError:
            text = "Ошибка сервиса распознавания речи."

    return text


@dp.message(F.voice)
async def handle_voice(message: Message, bot: Bot):
    # Получаем аудиофайл и передаем его для распознавания
    voice = await bot.download(message.voice.file_id)
    audio_bytes = voice.read()
    recognized_text = recognize_speech_from_audio(audio_bytes)
    await message.reply(recognized_text)

# Другие обработчики и функции...

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())



@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


# Команда /start
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! Отправьте PDF, DOCX или XLSX документ, чтобы я его обработал.")


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

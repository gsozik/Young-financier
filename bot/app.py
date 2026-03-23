import io

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboard import main_keyboard
from storage.file_storage import LocalFileStorage
from services.extractor import OpenAIExtractor
from services.metrics import MetricsCalculator
from services.interpreter import MetricsInterpreter
from services.audit_questions import AuditQuestionsAnalyzer
from services.model_metrics import MetricsLLMInterpreter
from settings import api_key

router = Router()

storage = LocalFileStorage("storage")
extractor = OpenAIExtractor(api_key=api_key)
calculator = MetricsCalculator()
interpreter = MetricsInterpreter()
analizer = AuditQuestionsAnalyzer(api_key=api_key)
draft = MetricsLLMInterpreter(api_key=api_key)


def process_pdf(pdf_path: str) -> dict:
    extracted_data = extractor.extract(pdf_path)
    metrics = calculator.calculate(extracted_data)
    result = interpreter.interpret(metrics)
    answers = analizer.analyze(pdf_path)
    description = draft.interpret(metrics)

    return {
        "extracted_data": extracted_data,
        "metrics": metrics,
        "interpreter": result,
        "answers": answers,
        "description": description
    }


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Здравствуйте! Нажмите кнопку ниже, чтобы отправить отчетность.",
        reply_markup=main_keyboard
    )


@router.message(F.text == "Отправить отчетность")
async def upload_request_handler(message: Message):
    await message.answer("Отправьте файл с отчетностью в чат в формате pdf")


@router.message(F.document)
async def document_handler(message: Message):
    document = message.document

    if not document.file_name:
        await message.answer("Не удалось определить имя файла.")
        return

    if not document.file_name.lower().endswith(".pdf"):
        await message.answer("Пожалуйста, отправьте файл с отчетностью в формате pdf.")
        return

    await message.answer("Обрабатываю....")

    bot = message.bot
    telegram_file = await bot.get_file(document.file_id)

    buffer = io.BytesIO()
    await bot.download_file(telegram_file.file_path, destination=buffer)

    saved_path = storage.save_pdf(
        file_name=document.file_name,
        file_bytes=buffer.getvalue()
    )

    try:
        result = process_pdf(saved_path)

        await message.answer(
            #f"Извлеченные данные:\n{result['extracted_data']}\n\n"
            #f"Метрики:\n{result['metrics']}\n\n"
            f"Ключевые метрики:\n{result['interpreter']}\n\n"
            f"Анализ метрик:\n{result['description']}\n\n"
            f"Аудиторские вопросы:\n{result['answers']}\n\n"
            f"**Не является финансовой рекомендацией**"
        )

    except Exception as e:
        await message.answer(f"Ошибка при обработке файла: {e}")
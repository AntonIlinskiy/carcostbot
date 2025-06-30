from aiogram import Router, types, F
from aiogram.filters import CommandStart
import logging
import asyncio
from core.parser import parse_car_data
from core.calculator import calculate_total_cost

router = Router()


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("👋 Привет! Пришли ссылку на объявление Avito.")


@router.message(F.text.startswith("http"))
async def handle_link(message: types.Message):
    url = message.text.strip()
    logging.info(f"Пользователь прислал ссылку: {url}")
    await message.answer("🔄 Обрабатываю ссылку, подождите...")

    try:
        car_info = await asyncio.to_thread(parse_car_data, url)
    except Exception as e:
        await message.answer(f"❌ Ошибка парсера: {e}")
        return

    if not car_info:
        await message.answer("❌ Не удалось извлечь данные по ссылке.")
        return

    try:
        final_cost = calculate_total_cost(car_info)
    except Exception as e:
        await message.answer(f"❌ Ошибка при расчёте: {e}")
        return

    response = (
        f"🚘 {car_info['brand']} {car_info['model']}, {car_info['year']} г.\n"
        f"💰 Цена: {car_info['price']:,} ₽\n\n"
        f"+ Доставка: {final_cost['delivery']:,} ₽\n"
        f"+ Таможня: {final_cost['customs']:,} ₽\n"
        f"+ Утилизация: {final_cost['utilization']:,} ₽\n\n"
        f"💵 Итого: {final_cost['total']:,} ₽"
    )
    await message.answer(response)

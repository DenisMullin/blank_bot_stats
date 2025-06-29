import asyncio
from pathlib import Path
from collections import defaultdict

from aiogram import Router, F, Bot
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,
    InputMediaPhoto
)
from aiogram.types.input_file import FSInputFile
from aiogram.methods import SendMessage
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from core.container import Container

router = Router()


# --- FSM состояния ---
class PhotoGenerationStates(StatesGroup):
    waiting_for_photos = State()
    choosing_style = State()


# --- Временное хранилище альбомов ---
media_group_cache = defaultdict(list)


keyboard_final = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Оплатить по СБП", callback_data="sbp")],
    [InlineKeyboardButton(text="Написать в поддержку", callback_data="podderzhka")],
])


# --- /start ---
@router.message(F.text.in_([__("/start")]))
async def reverance(message: Message, container: Container, bot: Bot) -> None:
    sleep = 1

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("Сгенерировать 5 фото - 450 руб"), callback_data="generate_5")],
        [InlineKeyboardButton(text=_("Сгенерировать 10 фото - 850 руб"), callback_data="generate_10")],
    ])

    keyboard_start = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("Да!"), callback_data="yes")],
    ])

    welcome_text = _(
        "👋 Привет! Я твой персональный фотограф в Телеграм."
    )

    await bot(SendMessage(chat_id=message.chat.id, text=welcome_text))
    await asyncio.sleep(sleep)

    await bot(SendMessage(
        chat_id=message.chat.id,
        text=_(
            "Загрузи до 3 фото, выбери стиль и получи уникальную фотосессию, "
            "которую не отличить от настоящей.\n\n"
            "Без затрат на студию и фотографа!\n"
            "10 снимков — 390 рублей."
        )
    ))
    await asyncio.sleep(sleep)

    await bot(SendMessage(chat_id=message.chat.id, text=_("Вот несколько примеров:")))
    await asyncio.sleep(sleep)

    base_path = Path(__file__).parent.parent / "res"
    media_group = [
        InputMediaPhoto(media=FSInputFile(base_path / "p1.jpg")),
        InputMediaPhoto(media=FSInputFile(base_path / "p2.jpg")),
        InputMediaPhoto(media=FSInputFile(base_path / "p3.jpg")),
    ]
    await bot.send_media_group(chat_id=message.chat.id, media=media_group)

    await asyncio.sleep(sleep)
    await bot(SendMessage(chat_id=message.chat.id, text=_("Приступим к созданию?"), reply_markup=keyboard_start))


# --- Обработка "Да!" ---
@router.callback_query(F.data == "yes")
async def handle_yes(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    await state.set_state(PhotoGenerationStates.waiting_for_photos)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text="Загрузите до 3 своих фото.\nКогда всё будет готово — напишите «Готово»."
    )


# --- Обработка одиночных фото ---
@router.message(PhotoGenerationStates.waiting_for_photos, F.photo & ~F.media_group_id)
async def handle_single_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get("photos", [])
    photos.append(message.photo[-1].file_id)

    if len(photos) >= 3:
        await state.update_data(photos=photos)
        await state.set_state(PhotoGenerationStates.choosing_style)
        await message.answer("Фото получены.")
        await send_style_choices(message)
    else:
        await state.update_data(photos=photos)
        await message.answer(f"Принято {len(photos)} фото. Можете загрузить ещё или написать «Готово».")


# --- Обработка альбома (MediaGroup) ---
@router.message(PhotoGenerationStates.waiting_for_photos, F.media_group_id)
async def handle_media_group(message: Message, state: FSMContext):
    media_group_cache[message.media_group_id].append(message.photo[-1].file_id)

    await asyncio.sleep(0.5)  # Подождём прихода всех фото

    # Обработка завершения группы
    photos = media_group_cache.pop(message.media_group_id, [])

    if not photos:
        return

    await state.update_data(photos=photos[:3])  # максимум 3
    await state.set_state(PhotoGenerationStates.choosing_style)
    await message.answer(f"Принято {len(photos)} фото.")
    await send_style_choices(message)


# --- Обработка команды "Готово" ---
@router.message(PhotoGenerationStates.waiting_for_photos, F.text.lower() == "готово")
async def handle_done_photo_upload(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get("photos", [])

    if not photos:
        await message.answer("Вы ещё не отправили ни одного фото.")
        return

    await state.set_state(PhotoGenerationStates.choosing_style)
    await message.answer("Фото получены.")
    await send_style_choices(message)


# --- Кнопки стилей ---
async def send_style_choices(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Фотостудия", callback_data="style_portrait")],
        [InlineKeyboardButton(text="Портретная съемка", callback_data="style_art")],
        [InlineKeyboardButton(text="В городе", callback_data="style_fashion")],
        [InlineKeyboardButton(text="В парке", callback_data="style_cyber")],
        [InlineKeyboardButton(text="Креативная", callback_data="style_fantasy")],
    ])
    await message.answer("Выберите стиль фотосессии:", reply_markup=keyboard)


# --- Обработка выбранного стиля ---
@router.callback_query(F.data.startswith("style_"))
async def handle_style_selected(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    style = callback.data.replace("style_", "")
    await state.update_data(style=style)
    await state.clear()

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=(
            f"Отлично!\n\n"
            "Мы готовы к подготовке фотосессии после оплаты. Это займёт немного времени.\n"
            "Результат появится здесь!"
        ),
        reply_markup=keyboard_final,

    )

    # Тут можно запустить генерацию изображений
    # data = await state.get_data()
    # photos = data["photos"]
    # выбранный стиль: style


# --- Кнопки "5 фото / 10 фото" ---
@router.callback_query(F.data.in_(["generate_5", "generate_10"]))
async def handle_generate_photos(callback: CallbackQuery, bot: Bot, container: Container):
    await callback.answer()
    count = "5" if callback.data == "generate_5" else "10"
    await container.user_repository.update_button(callback.from_user.id, count)


@router.callback_query(F.data.in_(["podderzhka"]))
async def handle_podderzhka(callback: CallbackQuery, bot: Bot, container: Container):
    await callback.answer()
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=_(
            "Можете написать сюда @ilyyyyaaa"
        )
    )


@router.callback_query(F.data.in_(["sbp"]))
async def handle_podderzhka(callback: CallbackQuery, bot: Bot, container: Container):
    await callback.answer()
    await container.user_repository.update_button(callback.from_user.id, "10")

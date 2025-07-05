from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from ..services.student import get_or_create_student
from ..services.assignment import add_submission

router = Router()


class SubmitStates(StatesGroup):
    waiting_assignment_id = State()
    waiting_answer = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    student = await get_or_create_student(message.from_user.id, message.from_user.full_name)
    await message.answer("Вы зарегистрированы как ученик. Используйте /submit чтобы отправить домашку.")


@router.message(Command("submit"))
async def cmd_submit(message: Message, state: FSMContext):
    await state.set_state(SubmitStates.waiting_assignment_id)
    await message.answer("Отправьте ID задания, на которое отвечаете:")


@router.message(SubmitStates.waiting_assignment_id)
async def get_assignment_id(message: Message, state: FSMContext):
    await state.update_data(assignment_id=int(message.text))
    await state.set_state(SubmitStates.waiting_answer)
    await message.answer("Отправьте ответ текстом или файлом")


@router.message(SubmitStates.waiting_answer, F.document | F.text)
async def submit_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    assignment_id = data["assignment_id"]
    file_id = None
    text = None
    if message.document:
        file_id = message.document.file_id
    else:
        text = message.text
    await add_submission(assignment_id, message.from_user.id, text, file_id)
    await state.clear()
    await message.answer("Ответ получен, спасибо")

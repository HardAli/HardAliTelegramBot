from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from ..services.student import list_students
from ..services.assignment import create_assignment

router = Router()

ADMIN_IDS = []  # filled in app.py


class AssignmentStates(StatesGroup):
    waiting_student_id = State()
    waiting_text = State()
    waiting_deadline = State()


@router.message(Command("students"))
async def cmd_students(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    students = await list_students()
    lines = [f"{s.id}. {s.full_name} ({s.tg_id})" for s in students]
    await message.answer("\n".join(lines) or "Нет учеников")


@router.message(Command("assign"))
async def cmd_assign(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    await state.set_state(AssignmentStates.waiting_student_id)
    await message.answer("ID ученика:")


@router.message(AssignmentStates.waiting_student_id)
async def assign_student_id(message: Message, state: FSMContext):
    await state.update_data(student_id=int(message.text))
    await state.set_state(AssignmentStates.waiting_text)
    await message.answer("Текст задания:")


@router.message(AssignmentStates.waiting_text, F.text)
async def assign_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(AssignmentStates.waiting_deadline)
    await message.answer("Дедлайн YYYY-MM-DD или 0")


@router.message(AssignmentStates.waiting_deadline)
async def assign_deadline(message: Message, state: FSMContext):
    data = await state.get_data()
    student_id = data["student_id"]
    text = data["text"]
    deadline = None
    if message.text != "0":
        deadline = datetime.fromisoformat(message.text)
    await create_assignment(student_id, text, None, deadline)
    await state.clear()
    await message.answer("Задание отправлено")


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer("Рассылка пока не реализована, это шаблон")

from sqlalchemy import select
from ..database.models import Student, async_session


async def get_or_create_student(tg_id: int, full_name: str) -> Student:
    async with async_session() as session:
        result = await session.execute(select(Student).where(Student.tg_id == tg_id))
        student = result.scalar_one_or_none()
        if student:
            return student
        student = Student(tg_id=tg_id, full_name=full_name)
        session.add(student)
        await session.commit()
        return student


async def list_students():
    async with async_session() as session:
        result = await session.execute(select(Student))
        return result.scalars().all()

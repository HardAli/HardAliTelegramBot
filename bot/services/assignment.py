from sqlalchemy import select
from ..database.models import Assignment, Submission, async_session


async def create_assignment(student_id: int, text: str, file: str | None, deadline=None) -> Assignment:
    async with async_session() as session:
        assignment = Assignment(student_id=student_id, text=text, file=file, deadline=deadline)
        session.add(assignment)
        await session.commit()
        await session.refresh(assignment)
        return assignment


async def add_submission(assignment_id: int, student_id: int, text: str | None, file: str | None) -> Submission:
    async with async_session() as session:
        submission = Submission(assignment_id=assignment_id, student_id=student_id, text=text, file=file)
        session.add(submission)
        await session.commit()
        await session.refresh(submission)
        return submission


async def list_assignments(student_id: int):
    async with async_session() as session:
        result = await session.execute(select(Assignment).where(Assignment.student_id == student_id))
        return result.scalars().all()

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class VacancyRequestHistory(Base):
    """A class for creating a table with the history of the number of vacancies."""

    __tablename__ = 'vacancy_request_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    vacancy_count = Column(Integer)
    change = Column(Integer, default=0)


async def async_main():
    """Function for creating a database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

from database.models import async_session, VacancyRequestHistory
from sqlalchemy.future import select


async def save_vacancy_request(vacancy_count):
    """This function saves the vacancy data for the last hour."""

    async with async_session() as session:
        async with session.begin():
            # Retrieving previous record
            result = await session.execute(select(VacancyRequestHistory).order_by(VacancyRequestHistory.id.desc()).limit(1))
            previous_entry = result.scalar_one_or_none()

            change = 0
            if previous_entry:
                change = vacancy_count - previous_entry.vacancy_count

            # Creating a new record
            new_entry = VacancyRequestHistory(
                vacancy_count=vacancy_count,
                change=change
            )
            session.add(new_entry)

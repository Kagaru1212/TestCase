from database.models import Session, VacancyRequestHistory


def save_vacancy_request(vacancy_count):
    session = Session()
    previous_entry = session.query(VacancyRequestHistory).order_by(VacancyRequestHistory.id.desc()).first()
    change = 0
    if previous_entry:
        change = vacancy_count - previous_entry.vacancy_count

    new_entry = VacancyRequestHistory(
        vacancy_count=vacancy_count,
        change=change
    )
    session.add(new_entry)
    session.commit()

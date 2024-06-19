import aiohttp
import asyncio
from database.save_in_db import save_vacancy_request


async def get_vacancy_count():
    """This function pulls up data on the number of vacancies on (rabota.ua) from all over Ukraine by keyword junior."""

    url = "https://api.rabota.ua/vacancy/search"
    headers = {
        'Accept': 'application/json',
    }
    params = {
        'keyWords': 'junior',  # Looking for vacancies by keyword junior
        'cityId': 0,  # 0 means "All Ukraine" according to API documentation
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                data = await response.json()
                total_count = data['total']  # we obtain the total number of vacancies

                # Saving query results to the database
                await save_vacancy_request(total_count)
                print("The data has been successfully saved to the database")

                return total_count

        except aiohttp.ClientError as e:
            print(f"Error while executing the query: {e}")


async def main():
    while True:
        await get_vacancy_count()
        # Waiting time 1 hour (3600 seconds)
        await asyncio.sleep(180)

if __name__ == '__main__':
    asyncio.run(main())

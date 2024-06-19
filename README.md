# TestCase

---

## This project implements a Telegram bot, which on the command /get_today_statistic sends the user an Exel file with the number of actual vacancies for today from the site rabota.ua.

**To run it you need:**
+ Download all dependencies
    ```python
    pip install -r requirements.txt
    ```
+ Create your own Telegram bot and get its token, then in the root folder of the project to create a file .env and in it a variable "TG_BOT_TOKEN" to which and assign the value of the token.


+ Now you need to run the file with the bot that will simultaneously create a database, it can be done like this:
    ```python
    python tg_bot.py
    ```
  ***Do not try to run the parser before running tg_bot.py because without a database the parser will not be able to save data and you will get an error !!!***


+ After starting the bot and creating the Database you can safely run the parser with the command:
    ```python
    python parser.py
    ```


### Done, you have successfully launched Telegram bot and parser!

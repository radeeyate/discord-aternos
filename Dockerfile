FROM python:3

ADD serverbot.py /

ADD .env /

RUN pip install discord.py python-aternos python-dotenv

CMD [ "python3", "./bot.py" ]

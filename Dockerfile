FROM python:3

ADD bot.py /

ADD .env /

RUN pip install discord.py python-aternos python-dotenv

CMD [ "python3", "./bot.py" ]

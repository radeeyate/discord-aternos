FROM python:3

ADD bot.py /

ADD query.py /

ADD startup.sh /

CMD ["chmod +x /startup.sh"]

RUN pip install discord.py python-aternos python-dotenv

ENTRYPOINT ["/startup.sh"]
FROM python:3.11 AS base
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
CMD ["bash"]

FROM base AS production
WORKDIR /bot
COPY . /bot
CMD python bot.py
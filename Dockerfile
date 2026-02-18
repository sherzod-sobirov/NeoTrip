FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY req.txt /code/
RUN pip install -r req.txt
COPY . /code/

RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]



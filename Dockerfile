FROM python:3.11.4

RUN mkdir /home/booksproject

COPY ./requirements.txt /home/booksproject

WORKDIR /home/booksproject

EXPOSE 8000

RUN pip install -r requirements.txt

COPY . /home/booksproject
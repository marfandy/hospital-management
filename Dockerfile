FROM python:3.7

RUN mkdir /code
WORKDIR /code

RUN apt-get update

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 80

# CMD flask run -h 0.0.0.0 -p 5000

# CMD ["flask", "run"]

CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
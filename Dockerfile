FROM python:3.11

WORKDIR /RAG_system

RUN pip install --upgrade pip

RUN pip install pydantic

COPY requirements.txt .

RUN apt-get update && apt-get install git -y && apt-get install curl -y

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install nltk && \
    python -m nltk.downloader punkt

COPY . .

# Делаем скрипт исполняемым (если необходимо)
# RUN chmod +x entrypoint.sh 

# Указываем команду для запуска контейнера
# CMD ["sh", "entrypoint.sh"] 




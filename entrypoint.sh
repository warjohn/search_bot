#!/usr/bin/env sh

# Включение вывода команд
set -x

# Установка Ollama
if curl -fsSL https://ollama.com/install.sh | sh; then
    echo "Ollama успешно установлен."
else
    echo "Ошибка установки Ollama." >&2
    exit 1
fi

ollama pull llama3.1

ollama serve

# Запуск сервера Ollama
if ollama serve; then
    echo "Сервер Ollama запущен."
else
    echo "Ошибка запуска сервера Ollama." >&2
    exit 1
fi

ollama run llama3.1

# Запуск модели llama3
if ollama run llama3.1; then
    echo "Модель llama3 запущена."
else
    echo "Ошибка запуска модели llama3." >&2
    exit 1
fi

# Запуск API
if python3 api.py; then
    echo "API успешно запущен."
else
    echo "Ошибка запуска API." >&2
    exit 1
fi

# Отключение вывода команд
set +x

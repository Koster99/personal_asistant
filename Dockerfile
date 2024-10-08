# Вказуємо базовий образ Python
FROM python:3.9-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо всі файли з поточної директорії на хост-машині до директорії /app всередині контейнера
COPY . .

# Встановлюємо залежності, якщо такі є
# (в даному випадку немає зовнішніх залежностей

# Вказуємо команду для запуску застосунку
CMD ["python", "personal_asistant.py"]

from backend.db import create_tables
from routes import app
import uvicorn
if __name__ == '__main__':
    create_tables()  # Создаем таблицы при запуске приложения
    uvicorn.run(app, host="localhost", port=8000)
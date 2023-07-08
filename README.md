Хороший старт.

Первый этап проверки работы.
Написал backend и тесты к нему. 
Если есть вопросы, не стесняйся, пиши мне в Пачке.

docker run --name db --env-file .env -v pg_data:/var/lib/postgresql/data postgres:13.10
docker run --env-file .env --net django-network-3 --name foodgram_backend_container -p 8000:8000 foodgram_backend 

cp -r /app/backend_static/. /backend_static/static/
cp -r /app/result_build/. /static/
/foodgram_backend/apps/data/ingredients.json
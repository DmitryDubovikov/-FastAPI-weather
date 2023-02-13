# FastAPI-weather

Run containers:

    docker-compose build
    docker-compose up

Check docs and endpoints:

    http://127.0.0.1:8000/docs

Create at least 2 cities with Postman or Swagger:
    http://localhost:8000/weather/London
    http://localhost:8000/weather/Paris
    

Insert data to weather table with pgAdmin:

   http://127.0.0.1:5050

    insert into public.weather values 
    (1, 1, CURRENT_TIMESTAMP, 10, 760, 1),
    (2, 1, CURRENT_TIMESTAMP, 12, 762, 3),
    (3, 2, CURRENT_TIMESTAMP, 20, 764, 5),
    (4, 2, CURRENT_TIMESTAMP, 22, 766, 7)
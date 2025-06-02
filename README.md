# 🌟 Movie search 🌟
Search movie with LLM

# 🚀 Start search movie service
## 1. Configurate the config in /config/config.yaml
## 2. Insert your opensearch setting (such as key, password) in .env
See the example in .env.exam
## 3. Start service with docker-compose
```
docker-compose -f docker-compose.yml up

# If want to re-build image
docker-compose -f docker-compose.yml up --build
```

## 4. Test result
```
Use postman to test API response
![alt text](https://github.com/beamvilla/movie_search/blob/master/image.png)
```

# 🚀 Code details
- Search movie logics provided in **/src/usecases/search_movie.py**
- All prompt template provided in **/src/prompt/prompt_template.py**
- Opensearch and OpenAI connector provided in **/src/repository**
- Main service file provided in **/src/main.py**

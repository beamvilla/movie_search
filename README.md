# 🌟 Movie search 🌟
Search movie with LLM

# 🚀 Build env
``` bash
$ docker build -f docker/Dockerfile -t movie_search:latest .
```

# 🚀 Start env
``` bash
$ docker run -it --net=host --rm -v $(pwd):/movie_search movie_search:latest /bin/bash
```
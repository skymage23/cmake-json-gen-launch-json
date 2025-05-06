#!/bin/bash

docker build -t dev-env .
docker run -it -v $(pwd):/app --rm dev-env /bin/bash -c 'cd /app && /bin/bash'
docker image rm dev-env
# Docker URL Shortener

A small URL shortener that runs as **3 load-balanced Flask containers** behind **nginx**, storing data in **Redis**. Everything starts with one command.

```
client -> nginx (:8080) -> app x3 (Flask + gunicorn) -> Redis
```

## Run

```bash
docker compose up --build
```

## Try it

```bash
# create a short link
curl -X POST localhost:8080/shorten -H "Content-Type: application/json" \
     -d '{"url": "https://github.com"}'

# open it (redirects), then check clicks
curl -i localhost:8080/<code>
curl localhost:8080/stats/<code>

# see load balancing: "served_by" changes between containers
for i in 1 2 3 4 5 6; do curl -s localhost:8080/; done
```

## Tech
Python, Flask, gunicorn, Redis, nginx, Docker, docker-compose.

## What I learned
- Scaling a service with `replicas` and balancing it with nginx (round-robin via Docker DNS)
- Keeping containers stateless by storing state in Redis
- Persisting data with Docker volumes

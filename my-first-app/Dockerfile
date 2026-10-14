# checkov:skip=CKV_DOCKER_3: nginx must start as root to bind port 80, non-root nginx image is phase 2
FROM nginx:alpine
RUN apk upgrade --no-cache
COPY index.html /usr/share/nginx/html/index.html

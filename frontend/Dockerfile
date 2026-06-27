# Build Stage
FROM node:20-alpine as build

WORKDIR /app

# Install dependencies first for better caching
COPY package.json package-lock.json* ./
RUN npm ci

# Copy source code and build
COPY . .
# The docker-compose will pass VITE_API_URL here if needed, but relative URLs are better handled by nginx proxies.
# Alternatively, production builds hardcode the URL. We build it dynamically.
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Serve Stage
FROM nginx:alpine

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build artifacts to Nginx public folder
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

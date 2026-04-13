# Build Stage (Node.js)
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies rapidly
COPY package*.json ./
RUN npm install

# Build static bundle
COPY . .
# En caso de desplegar remotamente, puedes inyectar mediante --build-arg
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# Serve Stage (Nginx)
FROM nginx:alpine

# Copiar el bundle ya construido
COPY --from=build /app/dist /usr/share/nginx/html

# Copiar configuración proxy (SPA)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

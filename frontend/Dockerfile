FROM node:20-slim AS build
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# VITE_API_URL doit etre connu au moment du build (Vite l'injecte
# statiquement dans le bundle), pas seulement au runtime du conteneur.
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

FROM node:20-slim
WORKDIR /app

RUN npm install -g serve
COPY --from=build /app/dist ./dist

EXPOSE 3000
CMD ["sh", "-c", "serve -s dist -l ${PORT:-3000}"]

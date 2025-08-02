FROM node:18

WORKDIR /app

# Install necessary packages for ARM64 compatibility
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY package*.json ./
ENV NODE_ENV=development
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
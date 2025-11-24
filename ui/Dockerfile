# Use an official Node.js runtime as a parent image
FROM node:24-alpine

# Set the working directory in the container
WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Install app dependencies using pnpm
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Copy app source code
COPY . .

# Expose the port the app runs on
EXPOSE 5173

# Start the app
CMD ["pnpm", "run", "dev"]

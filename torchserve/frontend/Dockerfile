# Base image
FROM node:14-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --production

# Copy the rest of the app's code
COPY . .

# Build the app
RUN npm run build

# Set environment variable for production
ENV NODE_ENV=development


# Expose a port (optional, if needed)
EXPOSE 3000

# Start the app
CMD ["npm", "start"]

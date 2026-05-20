FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (using legacy-peer-deps to avoid upstream conflicts)
RUN npm install --legacy-peer-deps

# Copy application files
COPY . .

# Expose port
EXPOSE 3000

# Start React dev server
CMD ["npm", "start"]

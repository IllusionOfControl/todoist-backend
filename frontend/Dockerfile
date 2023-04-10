# Base image
FROM node:14-alpine as react-build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

ARG API_ENDPOINT
ENV REACT_APP_API_ENDPOINT $API_ENDPOINT

# Build the React app
RUN npm run build

# Serve the built app using Nginx
FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY --from=react-build /app/build /usr/share/nginx/html
EXPOSE 8000
CMD ["nginx", "-g", "daemon off;"]

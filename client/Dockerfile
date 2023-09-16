# Use Nginx image to serve
FROM nginx:alpine

# Remove default nginx files
RUN rm -rf /usr/share/nginx/html/*

# Copy html and assets to the nginx container
COPY . /usr/share/nginx/html

# Make port 80 available to the world outside this container
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
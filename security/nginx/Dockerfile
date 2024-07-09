FROM openresty/openresty:alpine-fat

ARG NGINX_CONFIGURATION
 
RUN mkdir /var/log/nginx
 
RUN apk add --no-cache openssl-dev
RUN apk add --no-cache git
RUN apk add --no-cache gcc
RUN luarocks install lua-resty-openidc

# Copy the NGINX configuration
COPY --from=nginx_configuration_directory $NGINX_CONFIGURATION /usr/local/openresty/nginx/conf/nginx.conf

EXPOSE 443

ENTRYPOINT ["/usr/local/openresty/nginx/sbin/nginx", "-g", "daemon off;"]

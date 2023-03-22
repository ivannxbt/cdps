FROM ruby:2.7.1-slim

COPY . /opt/microservices/
WORKDIR /opt/microservices
ENV SERVICE_VERSION=v1
ENV ENABLE_EXTERNAL_BOOK_SERVICE=true
EXPOSE 9080
CMD ["ruby", "details.rb", "9080"]

# docker build -t 43/details .
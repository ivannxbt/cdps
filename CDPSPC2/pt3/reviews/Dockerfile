FROM websphere-liberty:20.0.0.6-full-java8-ibmjava
ENV SERVICE_VERSION v1
ENV ENABLE_EXTERNAL_BOOK_SERVICE true
COPY details.rb /opt/microservices/
WORKDIR /src/reviews/reviews-wlpcfg
RUN docker run --rm -u root -v "$(pwd)":/home/gradle/project -w /home/gradle/project gradle:4.8.1 gradle clean build
EXPOSE 9080
CMD ["ruby", "/opt/microservices/details.rb"]
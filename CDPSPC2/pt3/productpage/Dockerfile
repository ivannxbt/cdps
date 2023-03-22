FROM python:3
RUN apt-get update
RUN apt-get -y install python3-pip
ENV GROUP_NUMBER 43
RUN git clone https://github.com/CDPS-ETSIT/practica_creativa2.git
WORKDIR /practica_creativa2/bookinfo/src/productpage
RUN sed -i "s/urllib3==1.26.5/urllib3/g" requirements.txt
RUN sed -i "s/chardet==3.0.4/chardet/g" requirements.txt
RUN sed -i "s/gevent==1.4.0/gevent/g" requirements.txt
RUN sed -i "s/greenlet==0.4.15/greenlet/g" requirements.txt
RUN python3 -m pip install -r requirements.txt
WORKDIR /practica_creativa2/bookinfo/src/productpage/templates/
EXPOSE 9080
CMD sed -i "s/Simple\sBookstore\sApp/g${GROUP_NUMBER}/g" index.html; \
    sed -i "s/Simple\sBookstore\sApp/g${GROUP_NUMBER}/g" productpage.html; \
    python3 /practica_creativa2/bookinfo/src/productpage/productpage.py 9080
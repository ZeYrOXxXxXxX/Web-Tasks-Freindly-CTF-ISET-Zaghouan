FROM httpd:2.4.49

USER root

RUN echo "Securinets{P4th_Tr4v3rs4l_1s_T00_Ez_In_2021}" > /flag.txt && \
    chmod 444 /flag.txt

COPY ./conf/httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./html/ /usr/local/apache2/htdocs/

RUN chown -R root:root /usr/local/apache2/htdocs && \
    chmod -R 555 /usr/local/apache2/htdocs

EXPOSE 80

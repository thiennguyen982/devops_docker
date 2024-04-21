FROM centos

RUN cd /etc/yum.repos.d/ \ 
    && sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-Linux-* \
    && sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-Linux-* \
    && yum update -y \
    && yum -y install httpd \
    && yum -y install vim

ADD ./test.html /var/www/html

WORKDIR /var/www/html                     

EXPOSE 80

ENTRYPOINT [ "usr/sbin/httpd" ]
 
CMD [ "-D", "FOREGROUND" ]
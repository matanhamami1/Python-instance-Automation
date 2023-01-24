#!/bin/bash
amazon-linux-extras install -y lamp-mariadb10.2-php7.2
yum install -y httpd

echo "SENTENCE_PLACEHOLDER" > /var/www/html/index.html

systemctl start httpd

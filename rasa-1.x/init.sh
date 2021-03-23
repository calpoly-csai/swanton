#!/bin/bash

docker run --rm -i -p 80:80 -v=rasa-1x_certbot-etc:/etc/letsencrypt -v=rasa-1x_certbot-var:/var/letsencrypt certbot/certbot certonly --non-interactive --standalone --email swantonpoppycp@gmail.com --agree-tos --no-eff-email -d swantonpoppy.org -d www.swantonpoppy.org


# nginx/init.sls

# TODO: Include gunicorn for staging and production environments
#include:
#  - uwsgi

/etc/nginx/nginx.conf:
  file:
    - managed
    - source: salt://nginx/nginx.conf
    - require:
        - pkg: nginx

/etc/nginx/sites-available/app.conf:
  file:
    - managed
    - source: salt://nginx/app.conf
    - require:
        - pkg: nginx

#/etc/nginx/sites-enabled/app.conf:
#  file:
#    - symlink
#    - target: /etc/nginx/sites-available/app.conf
#    - require:
#        - file: /etc/nginx/sites-available/app.conf

/etc/nginx/sites-available/app-dev.conf:
  file:
    - managed
    - source: salt://nginx/app-dev.conf
    - require:
        - pkg: nginx

/etc/nginx/sites-enabled/app-dev.conf:
  file:
    - symlink
    - target: /etc/nginx/sites-available/app-dev.conf
    - require:
        - file: /etc/nginx/sites-available/app-dev.conf

/etc/nginx/sites-enabled/default:
  file:
    - absent

nginx:
  pkg:
    - installed
  service:
    - running
    - enable: True
    - reload: True
    - require:
      - pkg: nginx
      - file: /etc/nginx/nginx.conf
      - file: /etc/nginx/sites-available/app.conf
      - file: /etc/nginx/sites-available/app-dev.conf
#      - file: /etc/nginx/sites-enabled/app.conf #For prod users
      - file: /etc/nginx/sites-enabled/app-dev.conf
      - file: /etc/nginx/sites-enabled/default
    - watch:
      - file: /etc/nginx/nginx.conf
      - file: /etc/nginx/sites-available/app.conf
      - file: /etc/nginx/sites-available/app-dev.conf
# postgres/init.sls

/home/vagrant/.pgpass:
  file:
    - managed
    - source: salt://project/.pgpass
    - mode: 600
    - user: vagrant
    - group: vagrant

postgresql:
  pkg:
    - installed
    - name: postgresql-9.3
  service:
    - running
    - enable: True
    - reload: True
    - requires:
        - pkg: postgresql

postgresql-server-dev-9.3:
  pkg:
    - installed
    - requires:
      - pkg: postgresql

postgis:
  pkg:
    - installed
    - requires:
      - pkg: postgresql-server-dev-9.3

postgresql-9.3-postgis-scripts:
  pkg:
    - installed
    - requires:
      - pkg: postgis

create-db-user:
  postgres_user:
    - present
    - name: postgres
    - createdb: True
    - createroles: True
    - login: True
    - superuser: True
    - password: '123456'

create-db:
  postgres_database:
    - present
    - name: Lile
    - db_user: postgres
    - db_password: '123456'
    - user: postgres
    - encoding: UTF8
    - owner: postgres
    - template: template0

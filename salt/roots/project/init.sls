# project/init.sls

run-migrations:
  cmd:
    - run
    - name: /srv/www/venv/bin/python /vagrant/Lile/manage.py migrate
    - requires:
      - pkg: python-env
      - pkg: install-psycopg2

#create-superuser:
#  cmd:
#    - run
#    - name: echo "from accounts.models import User; User.objects.create_superuser('admin@admin.com.br', '123123')" | /srv/www/venv/bin/python /vagrant/Lile/manage.py shell
#    - requires:
#      - pkg: python-env
#      - pkg: run-migrations

# Probably bad approach
#restore-backup:
#  cmd:
#    - run
#    - name: psql -Upostgres -h127.0.0.1 Lile < /vagrant/backup_19082015.sql
#    - user: vagrant
#    - requires:
#      - pkg: /home/vagrant/.pgpass
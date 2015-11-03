# dependencies/init.sls

include:
  - postgres

binutils:
  pkg:
    - installed

libproj-dev:
  pkg:
    - installed
    - require:
      - pkg: binutils

libjpeg-dev:
  pkg:
    - installed

python-pip:
  pkg:
    - installed

python-virtualenv:
  pkg:
    - installed

/srv/www/venv:
  file.directory:
    - user: vagrant
    - group: vagrant
    - makedirs: True

python-env:
  virtualenv.managed:
    - name: /srv/www/venv
    - cwd: /srv/www/venv
    - user: vagrant
    - requirements: /vagrant/requirements.txt
    - require:
        - pkg: python-pip
        - pkg: python-virtualenv

install-psycopg2:
  cmd:
    - run
    - name: pip install psycopg2
    - requires:
        - pkg: python-env
        - pkg: postgresql-server-dev-9.3

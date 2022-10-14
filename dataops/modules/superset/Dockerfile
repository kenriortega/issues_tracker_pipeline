FROM apache/superset
# Switching to root to install the required packages
USER root
# Example: installing the MySQL driver to connect to the metadata database
# if you prefer Postgres, you may want to use `psycopg2-binary` instead
RUN pip install mysqlclient
RUN pip install \
    psycopg2-binary==2.9.1 \
    redis==3.5.3 \
    clickhouse-sqlalchemy>=0.2.2 \
    elasticsearch-dbapi==0.2.5
# Switching back to using the `superset` user
USER superset
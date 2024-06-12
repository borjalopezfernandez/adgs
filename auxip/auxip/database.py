from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import Settings


# systemctl stop nginx
# sudo service postgresql start

# pg_hba.conf #
# /etc/postgresql/14/main/pg_hba.conf

# postgres$> createdb adgs_db
# psql -U postgres
# alter user adgs WITH PASSWORD 'adg$';
# postgres=# \connect adgs_db
# adgs_db=# \dt
#

'''
\connect adgs_db

adgs_db=# \d subscriptions
 Id                     | uuid                        |           | not null | 
 Status                 | enumsubscriptionstatus      |           |          | 
 FilterParam            | character varying(512)      |           |          | 
 NotificationEndpoint   | character varying(255)      |           |          | 
 NotificationEpUsername | character varying(63)       |           |          | 
 NotificationEpPassword | character varying(255)      |           |          | 
 LastNotificationDate   | timestamp without time zone |           |          | 
 SubmissionDate         | timestamp without time zone |           |          | 

 table subscriptions

 select "Id" from subscriptions where "NotificationEpUsername"='perry';
 select "Id" from subscriptions where "Id"='c9b6a93b-3843-485b-a8a7-1f8f79092eba';
 c9b6a93b-3843-485b-a8a7-1f8f79092eba

'''

# postgres=# SHOW data_directory;
# GRANT ALL PRIVILEGES ON DATABASE adgs_db  to postgres;
# GRANT ALL PRIVILEGES ON DATABASE adgs_db  to adgs;
# GRANT CONNECT ON DATABASE adgs_db TO adgs;
# did not work with localhost and need to use 127.0.0.1

SQLALCHEMY_DATABASE_URL = Settings.database_url

engine                  = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal            = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base                    = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

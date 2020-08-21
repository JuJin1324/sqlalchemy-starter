# Created by Yoo Ju Jin(jujin@100fac.com) 
# Created Date : 2020/08/19
# Copyright (C) 2020, Centum Factorial all rights reserved.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_ACCOUNT_NAME = 'scott'
DB_PASSWORD = 'tiger'
DB_HOST = 'localhost'
DB_PORT = '15772'
DB_DATABASE = 'sqlalchemy'

engine = create_engine(f'postgresql://{DB_ACCOUNT_NAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}', echo=False)
Session = sessionmaker(bind=engine)

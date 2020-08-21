# sqlalchemy-starter
Python RDB ORM(Object-relational mapping)
* [ORM이란?](http://www.incodom.kr/ORM)

## 코드 구성
### rdb
RDB 데이터베이스 관련 코드
* config.py: Database 연결 관련 설정
* models.py: sqlalchmey.declarative_base 상속 테이블

## sqlalchemy
### engine 객체
sqlalchmey 를 통해서 DB 연결을 하기 위해서는 engine 객체를 생성해야한다.   
engine 생성
``` python
from sqlalchemy import create_engine
engine = create_engine(f'postgresql://{DB_ACCOUNT_NAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}', echo=False)
```

### Base 객체
sqlalchemy를 통하여 테이블 DTO 클래스를 만들기 위해서 상속받아야하는 객체
```python
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
``` 

### Session 객체
Python - Database 사이에 Session 에서 Database 에서 select 한 row 혹은 
Database로 insert 등을 할 row 정보를 Session에 가지고 있는다. 
``` python
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

user = User('jujin', 'Ju-Jin Yoo', '1234')
session = Session()
session.add(user)      # session 에 add 한다고 바로 DB에 반영되지 않는다.
```

* session.dirty: session에 연결된 객체가 수정/변경되면 session.dirty를 통해서 변경된 객체를 얻을 수 있다.
* session.new: session에 새로 추가한 객체를 담고 있다.
* session.commit(): session 에 

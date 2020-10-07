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

### query 함수
* `query.first()`: limit 1   
* `query.one()`: 조건의 행이 1개가 아니면 에러 발생

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

### 관계 설정
users(1) <---- (N, users.id)addresses   
하나의 users row를 여러 addresses row가 참조한다.

관계 사용시 `relationship("Class 이름")` 으로 사용하는 이유는 파이썬이 클래스를 순차적으로 해석하기 때문에 
순서가 맞지 않는 경우 에러 발생을 막기 위한 것으로 보인다.   

`user = relationship("User", backref=backref('addresses', order_by=id))`   
backref: User 클래스의 인스턴스에서 addresses 항목으로 자기자신을 참조할 수 있다.
양방향 관계 설정: backref로 인해서 Address 클래스에서는 User 클래스 정보를 `user` 변수로 사용이 가능하고 
User 클래스에서 Address 객체는 위에 설정한 backref에서 'addresses'가 이름인 변수로 사용할 수가 있다.      
예시)
```python
# User 에는 addresses 가 없지만 위에서 backref 에 addresses를 추가해주었기 때문에 가능하다.
user = User('jack', 'Jack Bean', '1231234')
print(jack.addresses)
```

Address 클래스에서 `user = relationship("User", backref=backref('addresses', order_by=id))` 를 지우고
User 클래스에서 `addresses = relationship("Address", backref='user', order_by="Address.id")` 문장을 집어넣어서
동일한 양방향 관계를 설정하는 것도 가능하다.


# Created by Yoo Ju Jin(jujin@100fac.com) 
# Created Date : 2020/08/25
# Copyright (C) 2020, Centum Factorial all rights reserved.
from sqlalchemy import func, exists
from sqlalchemy.orm import aliased

from rdb.config import Session
from rdb.models import User, Address, BlogPost, Keyword

session = Session()


def practice_from_self():
    ua = aliased(User)
    # .filter(User.name < ua.name): alphabetic order
    rows = session.query(User).from_self(User.id, User.name, ua.name) \
        .filter(User.name < ua.name) \
        .filter(func.length(ua.name) != func.length(User.name)).all()
    print(f"from_self: {rows}")


def practice_backref():
    jack = User('jack', 'Jack Bean', 'sadfdasgjas')
    jack.addresses = [
        Address(email_address='jack@gmail.com'),
        Address(email_address='jack@yahoo.com')
    ]
    session.add(jack)
    session.commit()


def practice_lazy_loading():
    jack = session.query(User).filter_by(name='jack').one()
    print(jack)
    print(jack.addresses)


def practice_alias_double_email():
    address1 = aliased(Address)
    address2 = aliased(Address)
    for username, email1, email2 in \
            session.query(User.name, address1.email_address, address2.email_address) \
                    .join(address1, User.addresses) \
                    .join(address2, User.addresses) \
                    .filter(address1.email_address == 'jack@gmail.com') \
                    .filter(address2.email_address == 'jack@yahoo.com'):
        print(f'{username}, {email1}, {email2}')


def practice_subquery():
    stmt = session.query(Address.user_id, func.count('*').label('address_count')). \
        group_by(Address.user_id).subquery()
    # print(stmt)
    for u, count in session.query(User, stmt.c.address_count) \
            .outerjoin(stmt, User.id == stmt.c.user_id).order_by(User.id):
        print(f'{u}, {count}')


def practice_exists():
    # case 1
    stmt = exists().where(Address.user_id == User.id)
    for name, in session.query(User.name).filter(stmt):
        print(name)

    # case 2
    for name, in session.query(User.name).filter(User.addresses.any()):
        print(name)


def practice_conditional_any():
    for name, in session.query(User.name) \
            .filter(User.addresses.any(Address.email_address.like('%gmail%'))):
        print(name)


def practice_has():
    rows = session.query(Address).filter(~Address.user.has(User.name == 'jack')).all()
    print(rows)  # output: []


def practice_delete():
    jack = session.query(User).filter_by(name='jack').scalar()
    session.delete(jack)
    count = session.query(User).filter_by(name='jack').count()
    print(f'count: {count}')
    addresses = session.query(Address) \
        .filter(Address.email_address.in_(['jack@gmail.com', 'jack@yahoo.com'])) \
        .all()
    for address in addresses:
        print(f'{address.id}, {address.email_address}, {address.user_id}')


def practice_cascade():
    address_count = session.query(Address) \
        .filter(Address.email_address.in_(['jack@gmail.com', 'jack@yahoo.com'])) \
        .count()
    print(f"jack's address_count before delete: {address_count}")
    jack = session.query(User).filter_by(name='jack').scalar()

    session.delete(jack)
    jack_users_count = session.query(User).filter_by(name='jack').count()
    print(f"jack's count in users after delete: {jack_users_count}")

    address_count = session.query(Address) \
        .filter(Address.email_address.in_(['jack@gmail.com', 'jack@yahoo.com'])) \
        .count()
    print(f"jack's address_count after delete: {address_count}")


def practice_relationship():
    wendy = session.query(User).filter_by(name='wendy').one()
    post = BlogPost("Wendy's Blog Post", "This is a test", wendy)
    session.add(post)

    post.keywords.append(Keyword('wendy'))
    post.keywords.append(Keyword('firstpost'))

    rows = session.query(BlogPost).filter(BlogPost.keywords.any(keyword='firstpost')).all()
    print(rows)
    print('---------------------------------------')
    rows = session.query(BlogPost).filter(BlogPost.author == wendy).all()
    print(rows)


if __name__ == '__main__':
    # create_all_tables()
    # practice_from_self()
    # practice_backref()
    # practice_lazy_loading()
    # practice_alias_double_email()
    # practice_subquery()
    # practice_exists()
    # practice_conditional_any()
    # practice_has()
    # practice_delete()
    # practice_cascade()
    practice_relationship()

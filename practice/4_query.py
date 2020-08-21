from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased

from rdb.config import Session
from rdb.models import User

session = Session()


def practice_orderby():
    for instance in session.query(User).order_by(User.id):
        print(f'instance.name: {instance.name}, instance.fullname: {instance.fullname}')

    print('')


def practice_multiple_result():
    for row in session.query(User, User.name).all():
        print(f'row.User: {row.User}, row.name: {row.name}')

    print('')


def practice_column_alias():
    for row in session.query(User.name.label('name_label')).all():
        print(f'column_alias: {row.name_label}')

    print('')


def practice_entity_alias():
    aliased_user = aliased(User, name='user_alias')
    for row in session.query(aliased_user, aliased_user.name).all():
        print(f'entity_alias result: {row.user_alias}')

    print('')


def practice_limit_offset():
    # limit by using slice
    for user in session.query(User).order_by(User.id)[1:3]:
        print(f'limit by slice result: {user}')

    print('')


def practice_filter_and_filter_by():
    for name in session.query(User.name).filter_by(fullname='Edward Kim')[0]:
        print(f'filter_by() result: {name}')

    for name in session.query(User.name).filter(User.fullname == 'Edward Kim')[0]:
        print(f'filter() result: {name}')

    print('')


def practice_and_or():
    # and case 1: filter chaining
    for user in session.query(User) \
            .filter(User.name == 'haruair') \
            .filter(User.fullname == 'Edward Kim'):
        print(f'filter chaining result: {user}')

    # and case 2: and_() function
    for user in session.query(User) \
            .filter(and_(User.name == 'haruair', User.fullname == 'Edward Kim')):
        print(f'and_() result: {user}')

    # or
    for user in session.query(User).filter(or_(User.name == 'haruair', User.fullname == 'Edward Kim')):
        print(f'or_() result: {user}')

    print('')


def practice_equal_not_equal():
    # equal
    for user in session.query(User).filter(User.name == 'haruair'):
        print(f'equal result: {user}')

    # not equal
    for user in session.query(User).filter(User.name != 'haruair'):
        print(f'not equal result: {user}')

    print('')


def practice_match_and_like():
    # like
    for user in session.query(User).filter(User.name.like('%rua%')):
        print(f'like result: {user}')

    # match
    for user in session.query(User).filter(User.name.match('haruair')):
        print(f'match result: {user}')

    print('')


def practice_in_not_in():
    for user in session.query(User).filter(User.name.in_(['wendy', 'mary', 'fred'])):
        print(f'in result: {user}')

    for user in session.query(User).filter(~User.name.in_(['wendy', 'mary', 'fred'])):
        print(f'not in result: {user}')

    print('')


def practice_null_and_not_null():
    # is null
    for user in session.query(User).filter(User.name == None):
        print(f'is null result: {user}')

    # is not null
    for user in session.query(User).filter(User.name != None):
        print(f'is not null result: {user}')

    print('')


if __name__ == '__main__':
    practice_orderby()
    practice_multiple_result()
    practice_column_alias()
    practice_entity_alias()
    practice_limit_offset()
    practice_filter_and_filter_by()
    practice_and_or()
    practice_equal_not_equal()
    practice_match_and_like()
    practice_in_not_in()
    practice_null_and_not_null()

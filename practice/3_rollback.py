from sqlalchemy.orm import aliased

from rdb.config import Session
from rdb.models import create_all_tables, delete_all_tables, User

session = Session()

if __name__ == '__main__':
    ed_user = session.query(User).filter_by(name='haruair').first()
    print(ed_user.id)

    ed_user.name = 'edkim'
    fake_user = User('fakeuser', 'Invalid', '12345')
    session.add(fake_user)

    all_users = session.query(User).filter(User.name.in_(['edkim', 'fakeuser'])).all()
    print(all_users)

    session.rollback()
    print(f'ed_user.name: {ed_user.name}, is fake_user in session? {fake_user in session}')

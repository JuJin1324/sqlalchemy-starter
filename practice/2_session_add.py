from sqlalchemy.orm import aliased

from rdb.config import Session
from rdb.models import create_all_tables, delete_all_tables, User

session = Session()

if __name__ == '__main__':
    ed_user = User('haruair', 'Edward Kim', '1234')
    session.add(ed_user)
    our_user = session.query(User).filter_by(name='haruair').first()
    print(f'ed_user == our_user: {ed_user == our_user}')    # True

    ed_user.password = 'test1234'
    print(f'session.dirty: {session.dirty}')

    session.add_all([
        User('wendy', 'Wendy Williams', 'foobar'),
        User('mary', 'Mary Contrary', 'xxg527'),
        User('fred', 'Fred Flinstone', 'blar')
    ])
    print(f'session.new: {session.new}')

    session.commit()
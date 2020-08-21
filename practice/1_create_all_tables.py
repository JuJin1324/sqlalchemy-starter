from rdb.config import Session, engine
from rdb.models import create_all_tables

session = Session()

if __name__ == '__main__':
    print(engine.execute("select 1").scalar())
    create_all_tables()
    # delete_all_tables()

from pathlib import Path
import os.path

from etl.exec import ExecuteETL


def main():
    db = os.path.join(Path(__file__).resolve().parent.parent, 'db.sqlite')
    print(db)
    response = ExecuteETL(db).exec()
    print(response)


if __name__ == '__main__':
    main()

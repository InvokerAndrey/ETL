from .etl.load import Load


def main():
    load = Load(db='db.sqlite')
    load.exec()


if __name__ == '__main__':
    main()

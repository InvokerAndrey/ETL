from .etl.load import Load


def main():
    load = Load(db='db.sqlite')
    load.save()


if __name__ == '__main__':
    main()

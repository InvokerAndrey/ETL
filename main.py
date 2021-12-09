from etl.exec import ExecuteETL


def main():
    response = ExecuteETL('db.sqlite').exec()
    print(response)


if __name__ == '__main__':
    main()

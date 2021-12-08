from etl.extract import Extract
from etl.transform import Transform
from etl.load import Load


def main():
    extract = Extract('db.sqlite')
    transform = Transform('db.sqlite')

    json_movies = transform.get_movies_in_json()
    print(json_movies[0])


if __name__ == '__main__':
    main()

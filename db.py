import pyodbc as odbc

connection_string = "this info is specific for my account so it is sensitive"
connection = odbc.connect(connection_string)
cursor = connection.cursor()


def create_films_table() -> None:
    query = """
    DROP TABLE IF EXISTS Films;
    CREATE TABLE Films (
    id int IDENTITY(1,1) PRIMARY KEY,
    title varchar(300) NOT NULL,
    year int NOT NULL,
    genre varchar(300) NOT NULL,
    description varchar(300) NOT NULL,
    director varchar(300) NOT NULL,
    cast varchar(300) NOT NULL,
    image_path varchar(300) NOT NULL
    average_rating DECIMAL(2, 2)
    );
    """

    cursor.execute(query)


def create_ratings_table() -> None:
    query = """
    DROP TABLE IF EXISTS Ratings;
    CREATE TABLE Ratings (
    id int IDENTITY(1,1) PRIMARY KEY,
    opinion varchar(300) NOT NULL,
    rating int NOT NULL,
    time datetime NOT NULL,
    author varchar(300) NOT NULL,
    title_id int FOREIGN KEY REFERENCES Films(id)
    ); """

    cursor.execute(query)


def create_tables() -> None:
    create_films_table()
    create_ratings_table()


create_tables()


def add_film_to_db(
    title: str,
    year: int,
    genre: str,
    description: str,
    director: str,
    cast: str,
    image_path: str,
) -> None:
    query = f"""
    INSERT INTO Films
    VALUES ('{title}', {year}, '{genre}', '{description}', '{director}', '{cast}', {image_path}, NULL);
    """

    cursor.execute(query)


def select_all_films() -> list:
    query = "SELECT * FROM Films;"

    cursor.execute(query)

    films_list = cursor.fetchall()
    films = "All films\n"
    for film in films_list:
        id = f"id: {film[0]}, "
        title = "title: " + film[1] + ", "
        year = f"year: {film[2]}, "
        genre = "genre: " + film[3] + ", "
        description = "description: " + film[4] + ", "
        director = "director: " + film[5] + ", "
        cast = "cast: " + film[6] + "\n"
        average_rating = "average_taring: " + film[7] + "\n"
        films += (
            id + title + year + genre + description + director + cast + average_rating
        )

        query = f"SELECT * FROM Ratings WHERE id={int(film[0])}"
        cursor.execute(query)
        films_ratings = cursor.fetchall()
        films += "\n" + str(films_ratings) + "\n"

    return films


def get_film_info(title: str) -> str:
    query = "SELECT * FROM Films WHERE title=" + title + ";"

    cursor.execute(query)

    film = cursor.fetchall()
    film_info = "All films\n"
    id = f"id: {film[0]}, "
    title = "title: " + film[1] + ", "
    year = f"year: {film[2]}, "
    genre = "genre: " + film[3] + ", "
    description = "description: " + film[4] + ", "
    director = "director: " + film[5] + ", "
    cast = "cast: " + film[6] + "\n"
    average_rating = "average_taring: " + film[7] + "\n"
    film_info += (
        id + title + year + genre + description + director + cast + average_rating
    )

    query = "SELECT * FROM Ratings WHERE title=" + title + ";"
    cursor.execute(query)
    films_ratings = cursor.fetchall()
    film_info += "\n" + str(films_ratings) + "\n"

    return film


def change_average() -> None:
    query = "SELECT * FROM Films;"
    cursor.execute(query)

    films_list = cursor.fetchall()
    for film in films_list:
        title = film[1]

        query = "SELECT * FROM Ratings WHERE title=" + title + ";"
        cursor.execute(query)
        films_ratings = cursor.fetchall()
        sum = 0
        count = 0

        for rating in films_ratings:
            sum += rating[3]
            count += 1

        average = round((sum / count), 2)

        query = f"UPDATE Films SET average_rating={average} WHERE title=" + title + ";"
        cursor.execute(query)


def film_exists(title: str) -> bool:
    query = f"""
        SELECT * FROM Films WHERE title='{title}';
    """

    cursor.execute(query)

    return bool(cursor.fetchall())


def rate_film_in_db(
    title: str, opinion: str, rating: int, time: str, author: str
) -> None:
    assert film_exists(title), "The film must exists"
    query = f"SELECT id FROM Films WHERE title='{title}';"
    cursor.execute(query)
    title_id = cursor.fetchall()[0][0]

    datetime = time.replace("T", " ") + ":00"
    if datetime[0] == "0" and datetime[1] == "0":
        datetime = datetime[1:]

    query = f"""
    INSERT INTO Ratings
    VALUES ('{opinion}', {rating}, '{datetime}', '{author}', {title_id});
    """

    cursor.execute(query)

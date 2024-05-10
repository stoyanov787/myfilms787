import azure.functions as func

from db import *
from images import *

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="add_film", methods=["GET", "POST"])
def add_film(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "GET":
        with open("templates/add_film.html", "r", encoding="utf8") as file:
            return func.HttpResponse(file.read(), mimetype="html")

    title = req.form.get("title")
    year = int(req.form.get("year"))
    genre = req.form.get("genre")
    description = req.form.get("description")
    director = req.form.get("director")
    cast = req.form.get("cast")
    image = req.form.get("image")
    image_path = title + ".jpg"
    upload_image(image, image_path)

    if film_exists(title):
        return func.HttpResponse("The film already exists")

    add_film_to_db(title, year, genre, description, director, cast, image_path)

    return func.HttpResponse("The film was added")


@app.route(route="rate_film", methods=["GET", "POST"])
def rate_film(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "GET":
        with open("templates/rate_film.html", "r", encoding="utf8") as file:
            return func.HttpResponse(file.read(), mimetype="html")

    title = req.form.get("title")
    opinion = req.form.get("opinion")
    rating = int(req.form.get("rating"))
    time = req.form.get("time")
    author = req.form.get("author")

    if not film_exists(title):
        return func.HttpResponse("The film with this title does not exist")

    rate_film_in_db(title, opinion, rating, time, author)

    return func.HttpResponse("The film was rated")


@app.route(route="list_films", methods=["GET"])
def list_films(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(select_all_films())


@app.route(route="search_film", methods=["GET", "POST"])
def search_film(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "GET":
        with open("templates/search_film.html", "r", encoding="utf8") as file:
            return func.HttpResponse(file.read(), mimetype="html")

    title = req.form.get("title")

    if not film_exists(title):
        return func.HttpResponse("The film with this title does not exist")

    return func.HttpResponse(get_film_info(title))


@app.schedule(schedule="0 30 11 * * *", arg_name="myTimer", run_on_startup=True)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    change_average()

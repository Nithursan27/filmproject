from flask import Blueprint, request, jsonify, url_for
from marshmallow import ValidationError

from sqlalchemy import and_
from api.models import db
from api.models.film import Film
from api.models.actor import Actor
from api.models.category import Category
from api.models.associations import film_category_table
from api.models.language import Language
from api.schemas.film import film_schema, films_schema
from api.schemas.language import language_schema

films_router = Blueprint('films', __name__, url_prefix='/films')

def add_actor_link(film):
    for actor in film["actors"]:
        actor["ref"] = url_for('api.actors.read_actor', actor_id = actor["actor_id"], _external=True)

@films_router.get('/')
def read_all_films():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    category = request.args.get("category", type=int)
    language = request.args.get("language", type=int)

    next_page = None
    prev_page = None
    films = Film.query
    if category and language:
        films = films.join(film_category_table).filter(and_((film_category_table.c.category_id == category), Film.language_id==language))
    elif category:
        films = films.join(film_category_table).filter(film_category_table.c.category_id == category)
    elif language:
        films = films.filter(Film.language_id==language)
        
    films = films.paginate(page=page, per_page=page_size)
        
    next_page = url_for('.read_all_films', page=films.next_num, page_size=page_size, _external=True) if films.has_next else None
    prev_page = url_for('.read_all_films', page=films.prev_num, page_size=page_size, _external=True) if films.has_prev else None
            
    films_response = films_schema.dump(films)
    
    for film in films_response:
        add_actor_link(film)
            
    return {
        "results": films_response,
        "next_page": next_page,
        "prev_page": prev_page
    }

@films_router.get('/<film_id>')
def read_film(film_id):
    film = Film.query.get_or_404(film_id)
    
    film_response = film_schema.dump(film)
    add_actor_link(film_response)
    
    return film_response

@films_router.post('/')
def create_film():
    film_data = request.json

    try:
        film_schema.load(film_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    fks = ["language_id", "original_language_id"]
    
    for fk in fks:
        if film_data[fk]:
            data = Language.query.get(film_data[fk])
            if data is None:
                return(f"Invalid {fk}", 400)
   
    film = Film(**film_data)
    db.session.add(film)
    db.session.commit()
    
    return film_schema.dump(film)

@films_router.patch('/<film_id>')
def update_film(film_id):
    film_data = request.json
    film = Film.query.get_or_404(film_id)
    
    try:
        film_schema.load(film_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    fks = ["language_id", "original_language_id"]
    
    for fk in fks:
        if film_data[fk]:
            data = Language.query.get(film_data[fk])
            if data is None:
                return(f"Invalid {fk}", 400)
    
    db.session.query(Film).filter_by(film_id=film_id).update(film_data)

    db.session.commit()
    return film_schema.dump(film)

@films_router.delete('/<film_id>')
def delete_film(film_id):
    film = Film.query.get_or_404(film_id)
    db.session.delete(film)
    db.session.commit()

    return ("", 204)

@films_router.get('/<film_id>/actors')
def read_film_actors(film_id):
    film = Film.query.get_or_404(film_id)
    
    film_response = film_schema.dump(film)
    add_actor_link(film_response)
    
    return film_response["actors"]

@films_router.put('/<film_id>/actors')
def update_film_actors(film_id):
    actor_data = request.json
    
    film = Film.query.get_or_404(film_id)
    new_actors = []
    if actor_data is None:
        actor_data = []
    for actor in actor_data:
        data = Actor.query.get(actor.get("actor_id", None))
        if data is None:
            return("Invalid input data", 400)
        new_actors.append(data)
        
    film.actors = new_actors
    
    db.session.add(film)
    db.session.commit()
    
    film_response = film_schema.dump(film)
    add_actor_link(film_response)
    
    return film_response["actors"]

@films_router.get('/<film_id>/categories')
def get_film_categories(film_id):
    film = Film.query.get_or_404(film_id)
    
    return film_schema.dump(film)["categories"]

@films_router.put('/<film_id>/categories')
def update_film_categories(film_id):
    categories_data = request.json
    
    film = Film.query.get_or_404(film_id)
    new_categories = []
    if categories_data is None:
        categories_data = []
    for category in categories_data:
        data = Category.query.get(category.get("category_id", None))
        if data is None:
            return("Invalid input data", 400)
        new_categories.append(data)
        
    film.categories = new_categories
    
    db.session.add(film)
    db.session.commit()
    
    film_response = film_schema.dump(film)
    add_actor_link(film_response)
    
    return film_response["categories"]
        
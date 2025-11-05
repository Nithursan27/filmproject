from flask import Blueprint, request, jsonify, url_for
from marshmallow import ValidationError

from api.models import db
from api.models.film import Film
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
    
    # filter_data = {'title': title, 'category': category}
    # filter_data = {key: value for (key,value) in filter_data.items() if value}
    
    # films = Film.query.filter_by(**filter_data)

    next_page = None
    prev_page = None

    if not any(request.args.values()):
        films = Film.query.all()   
    else:
        if category is not None:
            films = Film.query.join(film_category_table).filter(film_category_table.c.category_id == category).all()
        else:
            films = Film.query.paginate(page=page, per_page=page_size)
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
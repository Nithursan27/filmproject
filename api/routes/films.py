from flask import Blueprint, request, jsonify, url_for
from marshmallow import ValidationError

from api.models import db
from api.models.film import Film
from api.models.language import Language
from api.schemas.film import film_schema, films_schema
from api.schemas.language import language_schema

films_router = Blueprint('films', __name__, url_prefix='/films')

@films_router.get('/get')
def read_all_films():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    name = request.args.get("name", type=str)
    next_page = None
    prev_page = None
    
    if not any(request.args.values()):
        films = Film.query.all()   
    else:
        if name is not None:
            films = Film.query.filter(Film.title.startswith(name))
        else:
            films = Film.query.paginate(page=page, per_page=page_size)
            next_page = url_for('.read_all_films', page=films.next_num, page_size=page_size, _external=True) if films.has_next else None
            prev_page = url_for('.read_all_films', page=films.prev_num, page_size=page_size, _external=True) if films.has_prev else None
            
    return {
        "results": films_schema.dump(films),
        "next_page": next_page,
        "prev_page": prev_page
    }

@films_router.get('/<film_id>/get')
def read_film(film_id):
    film = Film.query.get_or_404(film_id)
    return film_schema.jsonify(film)

@films_router.post('/create')
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

@films_router.put('/<film_id>/update')
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
            
    if film_data["special_features"] == "null":
        film_data["special_features"] = None
    
    db.session.query(Film).filter_by(film_id=film_id).update(film_data)

    db.session.commit()
    return film_schema.dump(film)

@films_router.delete('/<film_id>/delete')
def delete_film(film_id):
    film = Film.query.get_or_404(film_id)
    db.session.delete(film)
    db.session.commit()

    return ("", 204)
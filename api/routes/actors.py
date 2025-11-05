from flask import Blueprint, request, jsonify, url_for
from marshmallow import ValidationError
from sqlalchemy import or_

from api.models import db
from api.models.actor import Actor, Film
from api.schemas.actor import actor_schema, actors_schema

actors_router = Blueprint('actors', __name__, url_prefix='/actors')

def add_film_link(actor):
    for film in actor["films"]:
        film["ref"] = url_for('api.films.read_film', film_id = film["film_id"], _external=True)
        

@actors_router.get('/')
def read_all_actors():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    name = request.args.get("name", type=str)
    next_page = None
    prev_page = None
    
    if not any(request.args.values()):
        actors = Actor.query.all()
    else:
        if name is not None:
            actors = Actor.query.filter(or_(Actor.first_name.startswith(name), Actor.last_name.startswith(name)))
        else:
            actors = Actor.query.paginate(page=page, per_page=page_size)
            next_page = url_for('.read_all_actors', page=actors.next_num, page_size=page_size, _external=True) if actors.has_next else None
            prev_page = url_for('.read_all_actors', page=actors.prev_num, page_size=page_size, _external=True) if actors.has_prev else None
            
    actors_response = actors_schema.dump(actors)
    
    for actor in actors_response:
        add_film_link(actor)
    
    return {
        "results": actors_response,
        "next_page": next_page,
        "prev_page": prev_page
    }

@actors_router.get('/<actor_id>')
def read_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    
    actor_response = actor_schema.dump(actor)
    add_film_link(actor_response)
    
    return actor_response

@actors_router.post('/')
def create_actor():
    actor_data = request.json

    try:
        actor_schema.load(actor_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    actor = Actor(**actor_data)
    db.session.add(actor)
    db.session.commit()

    return actor_schema.dump(actor)

@actors_router.put('/<actor_id>')
def update_actor(actor_id):
    actor_data = request.json
    actor = Actor.query.get_or_404(actor_id)
    
    try:
        actor_schema.load(actor_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    db.session.query(Actor).filter_by(actor_id=actor_id).update(actor_data)

    db.session.commit()
    return actor_schema.dump(actor)

@actors_router.delete('/<actor_id>')
def delete_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    db.session.delete(actor)
    db.session.commit()

    return ("", 204)

@actors_router.get('/<actor_id>/films')
def read_actor_films(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    
    actor_response = actor_schema.dump(actor)
    add_film_link(actor_response)
    
    return actor_response["films"]

@actors_router.put('/<actor_id>/films')
def update_actor_films(actor_id):
    film_data = request.json
    
    actor = Actor.query.get_or_404(actor_id)
    new_films = []
    if film_data is None:
        film_data = []
    for film in film_data:
        data = Film.query.get(film.get("film_id"))
        if data is None:
            return(f"Invalid input data", 400)
        new_films.append(data)
        
    actor.films = new_films
    
    db.session.add(actor)
    db.session.commit()
    
    actor_response = actor_schema.dump(actor)
    add_film_link(actor_response)
    
    return actor_response["films"]
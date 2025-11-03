from flask import Blueprint, request, jsonify, url_for
from marshmallow import ValidationError
from sqlalchemy import or_

from api.models import db
from api.models.actor import Actor
from api.schemas.actor import actor_schema, actors_schema

actors_router = Blueprint('actors', __name__, url_prefix='/actors')

@actors_router.get('/get')
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
    return {
        "results": actors_schema.dump(actors),
        "next_page": next_page,
        "prev_page": prev_page
    }

@actors_router.get('/<actor_id>/get')
def read_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    print(actor.films)
    return actor_schema.dump(actor)

@actors_router.post('/create')
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

@actors_router.put('/<actor_id>/update')
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

@actors_router.delete('/<actor_id>/delete')
def delete_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    db.session.delete(actor)
    db.session.commit()

    return ("", 204)
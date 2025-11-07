from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from api.models import db
from api.models.category import Category
from api.schemas.category import category_schema, categories_schema

categories_router = Blueprint('categories', __name__, url_prefix='/categories')

@categories_router.get('/')
def read_all_categories():
    categories = Category.query.all()
    return categories_schema.dump(categories)

@categories_router.get('/<category_id>')
def read_category(category_id):
    category = Category.query.get_or_404(category_id)
    return category_schema.dump(category)

@categories_router.post('/')
def create_category():
    category_data = request.json
    
    try:
        category_schema.load(category_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    category = Category(**category_data)
    db.session.add(category)
    db.session.commit()

    return category_schema.dump(category)

@categories_router.put('/<category_id>')
def update_category(category_id):
    category_data = request.json
    category = Category.query.get_or_404(category_id)
    
    try:
        category_schema.load(category_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    db.session.query(Category).filter_by(category_id=category_id).update(category_data)

    db.session.commit()
    return category_schema.dump(category)

@categories_router.delete('/<category_id>')
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()

    return ("", 204)
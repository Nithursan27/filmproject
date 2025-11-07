from api.models.category import Category
from api.schemas import ma

class CategorySchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Category

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
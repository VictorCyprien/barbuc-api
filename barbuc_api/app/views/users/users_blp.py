from flask_smorest import Blueprint

users_blp = Blueprint(
    name='users',
    import_name=__name__,
    description='Managing Users',
    url_prefix='/api/users'
)

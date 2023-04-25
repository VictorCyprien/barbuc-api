from flask_smorest import Blueprint

auth_blp = Blueprint(
    name='auth',
    import_name=__name__,
    description='Auth',
    url_prefix='/api/auth'
)

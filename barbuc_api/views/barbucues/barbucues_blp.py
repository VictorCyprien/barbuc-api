from flask_smorest import Blueprint

barbucues_blp = Blueprint(
    name='barbucues',
    import_name=__name__,
    description='Managing Barbucues',
    url_prefix='/api/barbucues'
)

from flask_smorest import Blueprint

barbecues_blp = Blueprint(
    name='barbecues',
    import_name=__name__,
    description='Managing Barbecues',
    url_prefix='/api/barbecues'
)

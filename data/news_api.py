import flask

from . import db_session


blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/sin_cos_tan')
def get_news():
    return "sin30 = 1/2 sin45 = √2/2 sin60 = √3/2 cos30 = √3/2 cos45 = √2/2 cos60 = 1/2 tan30 = 1/√3 tan45 = 1 tan60 = √3"
from flask import Flask, jsonify

from code.api import dashboard_api
from code.api import health_api
from code.api import version_api
from code.api import TRFormattedError
from code.api import jsonify_errors

app = Flask(__name__)

app.url_map.strict_slashes = False
app.config.from_object('config.Config')

app.register_blueprint(dashboard_api)
app.register_blueprint(health_api)
app.register_blueprint(version_api)


@app.errorhandler(Exception)
def handle_error(exception):
    app.logger.error(exception)
    code = getattr(exception, 'code', 500)
    message = getattr(exception, 'description', 'Something went wrong.')
    reason = '.'.join([
        exception.__class__.__module__,
        exception.__class__.__name__,
    ])

    response = jsonify(code=code, message=message, reason=reason)
    return response, code


@app.errorhandler(TRFormattedError)
def handle_tr_formatted_error(exception):
    app.logger.error(exception)
    return jsonify_errors(exception.json)


if __name__ == '__main__':
    app.run()

from flask import send_from_directory, render_template
import os
#import eventlet
#from eventlet import wsgi
from werkzeug.middleware.proxy_fix import ProxyFix

#from routes.scrape import scrape
#from routes.candidate import candidate
# from routes.diary import diary
# from routes.control_panel import control_panel
from routes.dashboard import dashboard

from config.config import app 

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["STATIC_FOLDER"] = "static"
app.config["TEMPLATES_FOLDER"] = "templates"


# Import the route files
#app.register_blueprint(scrape)
#app.register_blueprint(candidate)
app.register_blueprint(dashboard)
# app.register_blueprint(diary)
# app.register_blueprint(control_panel)

# Serving static files
@app.route('/', defaults={'path': ''})
@app.route('/<string:path>')
@app.route('/<path:path>')
def static_proxy(path):
    return render_template('./index.html')


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000, host='0.0.0.0', debug=True)
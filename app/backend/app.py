from flask import send_from_directory
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
    root_dir = os.path.dirname(os.getcwd())
    dir = os.path.join(root_dir, 'blinkdwiki_tagging/frontend/src')
    print(dir)
    print(app.root_path)
    if os.path.isfile('src/' + path):
        # If request is made for a file by angular for example main.js
        # condition will be true, file will be served from the public directory
        return send_from_directory(dir, path)
    else:
        # Otherwise index.html will be served,
        # angular router will handle the rest

        dir = os.path.join(root_dir, 'blinkdwiki_tagging/frontend/src')
        dir2 = app.root_path
        return send_from_directory(dir, "index.html")


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000, host='0.0.0.0', debug=True)
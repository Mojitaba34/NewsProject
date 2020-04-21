from flask import Flask

app = Flask(__name__)

from app import routes
from app.admin.routes import admin
app.register_blueprint(admin,url_prefix='/admin')
from flask import Flask
from app import db
from app.admin import db as db_admin
from app.robots import robot_runner
from app.admin import config
app = Flask(__name__ ,template_folder='templates',
                        static_url_path='/static',
                        static_folder='static')

app.config["SECRET_KEY"] = config.SECRET_KEY

try:
    print("build Tables")
    db.BuildTables() # First Step Check exists and build Tables Database
    db_admin.BuildTables() # Build Tables Admin

    """print("thread started")
    robot = robot_runner.robot_runner()
    robot.threadRun()"""    

except Exception as e:
    print(f"error --- > {e}")

from app import routes # route import 
from app.admin.routes import admin # admin route import
app.register_blueprint(admin,url_prefix='/admin') # add admin route with blueprint
from app import error_handlers # error Handling


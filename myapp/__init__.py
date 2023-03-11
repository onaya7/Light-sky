import os
from flask import Flask
from myapp.app import view



def create_app():
        # instanciating flask
    app = Flask(__name__)

    # directory path
    basedir = os.path.abspath(os.path.dirname(__file__))

    # local sqlite database config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        basedir, "data.sqlite"
    )

    # # heroku postgres database url
    # app.config["DATABASE_URL"]= 'postgres://rhwmtuzpfwvnju:68eb51398da2d9d157f138a664adb513e59c79ddacbb32438554a9591ba47e72@ec2-35-168-122-84.compute-1.amazonaws.com:5432/d504v2i08c75fl'

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY']='weatherapp'

    app.register_blueprint(view)
    
    from myapp.models import db
    db.init_app(app)

    return app 
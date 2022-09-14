import os
from flask import Flask
from myapp.app import view



def create_app():
        # instanciating flask
    app = Flask(__name__)

    # directory path
    basedir = os.path.abspath(os.path.dirname(__file__))

    # # local sqlite database config
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    #     basedir, "data.sqlite"
    # )

    # heroku postgres database url
    app.config["DATABASE_URL"]= 'postgres://jxclkxpxucbmke:331f8a9d1c4a176b275fbddb895a2a3bfdf0dab6f5b3330e59fcacf69d844c63@ec2-34-200-205-45.compute-1.amazonaws.com:5432/dqchr6iak6dvv'
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY']='weatherapp'

    app.register_blueprint(view)
    
    from myapp.models import db
    db.init_app(app)

    return app 
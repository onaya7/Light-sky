import os
import requests
from flask import Flask, request, render_template, url_for,redirect, flash
from flask_sqlalchemy import SQLAlchemy

# directory path
basedir = os.path.abspath(os.path.dirname(__file__))


# instanciating flask
app = Flask(__name__)

# database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY']='weatherapp'

# instanciating sqlalchemy
db = SQLAlchemy(app)


# database schema
class Cityname(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"Cityname('id:{self.id}','name:{self.name}')"


api_response = {
        "coord": {"lon": 3.75, "lat": 6.5833},
        "weather": [
            {"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04n"}
        ],
        "base": "stations",
        "main": {
            "temp": 74.77,
            "feels_like": 76.26,
            "temp_min": 74.77,
            "temp_max": 74.77,
            "pressure": 1010,
            "humidity": 92,
            "sea_level": 1010,
            "grnd_level": 1010,
        },
        "visibility": 10000,
        "wind": {"speed": 8.21, "deg": 231, "gust": 19.48},
        "clouds": {"all": 100},
        "dt": 1661883104,
        "sys": {"country": "NG", "sunrise": 1661837900, "sunset": 1661882010},
        "timezone": 3600,
        "id": 2332453,
        "name": "Lagos",
        "cod": 200,
    }

# creating a function that calls the weather app api
def weather_api(city):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=b931795ebe22068736e68e74d4cbaa6b"
        r = requests.get(url).json()
        return r

# adding data route
@app.route("/", methods=['POST'])
def add_data():
        
        new_city = request.form.get('name')
       
        # to check if the new city exist in the database 
        if new_city:
            existing_city = Cityname.query.filter_by(name=new_city).first()
            
            # if the new city doesnt exist
            if not existing_city:
                # sending a new city name from the form to the weather_api function
                new_city_data = weather_api(new_city)

                if new_city_data['cod'] == 200:
                    new_city_obj = Cityname(name=new_city.lower())
                    print(new_city_obj)

                    db.session.add(new_city_obj)
                    db.session.commit()
                else:
                    err_msg= 'City does not exist in the world'
                    print(err_msg)
                    flash(err_msg,'error' )
            else:
                # if the new city exist
                ex_msg ='City already exist in the database'
                print(ex_msg)
                flash(ex_msg,'error' )
        return redirect(url_for('get_data'))
        
# app route
@app.route("/")
def get_data():

    city = Cityname.query.all()
    weather_list=[]

    for city in city:
        data = weather_api(city.name)
        weather_data = {
            'city': city.name,
            'description':data['weather'][0]['description'],
            'temperature':data['main']['temp'],
            'icon':data['weather'][0]['icon'],
            'humidity':data['main']['humidity'],
            'wind':data['wind'],
            'date':data['dt'],
        }

        weather_list.append(weather_data)
    
    return render_template('weather.html',  title='light-sky', weather=weather_list)






# deleting data route 
@app.route('/delete/<name>', methods=['POST', 'GET'])
def delete(name):
    city = Cityname.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit
    flash(f'succesfully deleted{city.name} succesfully')
    return redirect(url_for('get_data'))


if __name__ == "__main__":
    app.run(debug=True)

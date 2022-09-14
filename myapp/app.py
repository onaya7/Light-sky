import requests
from flask import Flask, Blueprint, request, render_template, url_for,redirect, flash, jsonify
from myapp.models import db , Cityname
from datetime import date


view = Blueprint("view", __name__ , static_folder="static", template_folder="templates")

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


@view.route('/process_data', methods= ['POST'])
def process_data():
    new_city = request.form['name']
    today =date.today()
    d2 =  today.strftime("%B %d,%Y")

   
    # to check if the new city exist in the database 
    if new_city:
        existing_city = Cityname.query.filter_by(name=new_city).first()
        print(existing_city)
    
        # if the new city doesnt exist
        if not existing_city:
            # sending a new city name from the form to the weather_api function
            new_city_data = weather_api(new_city)

            if new_city_data['cod'] == 200:
                new_city_obj = Cityname(name=new_city.lower())
                print(new_city_obj.name)

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

      
       
        city = Cityname.query.filter_by(name=new_city).first()
        print(city)
        print(d2)
        data = weather_api(city.name)
        weather_data = {
                'city': city.name,
                'description':data['weather'][0]['description'],
                'temperature':data['main']['temp'],
                'icon':data['weather'][0]['icon'],
                'humidity':data['main']['humidity'],
                'wind':data['wind']['speed'],
                'date':d2,
            }

        
        print(weather_data)

    return jsonify({
        'name' :weather_data
        })

# app route
@view.route("/")
def get_data():

    
    return render_template('weather.html',  title='light-sky',)




import requests
from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from datetime import date
from myapp.models import Cityname, db

view = Blueprint("view", __name__, static_folder="static", template_folder="templates")

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
def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=b931795ebe22068736e68e74d4cbaa6b"
    response = requests.get(url)
    if response.status_code == 404:
        return None
    data = response.json()
    today_date = date.today().strftime("%B %d,%Y")
    
    weather_data = {
            "city": city,
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "icon": data["weather"][0]["icon"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "date": today_date
    }
    
    return weather_data
    


@view.route("/process_data", methods=["POST"])

def process_data():
    
    new_city = request.form["name"]
    
    
    if not new_city:
        return jsonify({"error": "Please enter a city name"})
    
     # Check if the new city exists in the database
    city = Cityname.query.filter_by(name=new_city.lower()).first()
    
    # If the new city doesn't exist in the database, fetch its data from the API and add it to the database
    if not city:
        weather_data = get_weather_data(new_city)
        if not weather_data:
            err_msg = f"City '{new_city}' does not exist in the world"
            flash(err_msg, "error")
            return jsonify({"error": err_msg})
        city = Cityname(name=new_city.lower())
        db.session.add(city)
        db.session.commit()

    # If the new city already exists in the database, use its data from the database
    else:
        ex_msg = f"City '{new_city}' already exists in the database"
        flash(ex_msg, "error")
        weather_data = get_weather_data(city.name)

    if not weather_data:
        return jsonify({"error": f"City '{new_city}' not found"}), 404

    return jsonify({"name":weather_data})
 
# app route
@view.route("/")
def get_data():

    return render_template(
        "weather.html",
        title="Light sky",
    )
    
# app route
@view.route("/weather_info")
def weather_info():

    return render_template(
        "weather_info.html",
        title="Light sky | weather_info",
    )

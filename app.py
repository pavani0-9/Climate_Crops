from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# ---------- DATA ----------
countries = {
    "India": [
        "Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh", "Rajasthan",
        "Bihar", "Maharashtra", "Andhra Pradesh", "Tamil Nadu", "Karnataka"
    ],
    "USA": [
        "Iowa", "Illinois", "Nebraska", "Minnesota", "Kansas",
        "Indiana", "Ohio", "Missouri", "North Dakota", "South Dakota"
    ],
    "China": [
        "Heilongjiang", "Jilin", "Liaoning", "Shandong", "Henan",
        "Hubei", "Hunan", "Sichuan", "Jiangsu", "Zhejiang"
    ],
    "Brazil": [
        "Paraná", "Rio Grande do Sul", "Minas Gerais", "São Paulo", "Mato Grosso",
        "Bahia", "Goiás", "Maranhão", "Ceará", "Santa Catarina"
    ],
    "Australia": [
        "New South Wales", "Victoria", "Queensland", "South Australia", "Western Australia",
        "Tasmania", "Northern Territory", "Australian Capital Territory", "Murray-Darling", "Sunraysia"
    ],
    "Canada": [
        "Saskatchewan", "Manitoba", "Ontario", "Quebec", "Alberta",
        "British Columbia", "Nova Scotia", "New Brunswick", "Prince Edward Island", "Yukon"
    ],
    "Germany": [
        "Bavaria", "Lower Saxony", "North Rhine-Westphalia", "Baden-Württemberg", "Hesse",
        "Saxony", "Rhineland-Palatinate", "Thuringia", "Schleswig-Holstein", "Saxony-Anhalt"
    ],
    "France": [
        "Île-de-France", "Grand Est", "Hauts-de-France", "Normandy", "Brittany",
        "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine", "Occitanie", "Pays de la Loire", "Provence-Alpes-Côte d'Azur"
    ]
}


crops = ["Rice", "Wheat", "Maize", "Cotton", "Soybean",
         "Barley", "Sugarcane", "Millet", "Potato", "Tomato"]

# ---------- ROUTES ----------

@app.route("/")
def home():
    return render_template("index.html",
                           countries=countries,
                           crops=crops)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    start_year = int(data.get("start_year", 2015))
    end_year = int(data.get("end_year", 2040))

    years = list(range(start_year, end_year + 1))

    base_temp = 25
    base_rain = 100
    base_co2 = 400

    temperature = []
    rainfall = []
    co2 = []
    yield_index = []

    current_yield = 100

    for i, year in enumerate(years):
        temperature.append(round(base_temp + 0.03 * (year - 2015), 2))
        rainfall.append(round(base_rain - 0.5 * (year - 2015), 2))
        co2.append(round(base_co2 + 2 * (year - 2015), 2))

        current_yield -= random.uniform(0.5, 1.5)
        yield_index.append(round(current_yield, 2))

    result = {
        "years": years,
        "temperature": temperature,
        "rainfall": rainfall,
        "co2": co2,
        "yield_index": yield_index,
        "kpis": {
            "yield_change": round(yield_index[-1] - 100, 2),
            "water_stress": random.randint(40, 80),
            "pest_risk": random.randint(30, 70),
            "food_security": random.randint(30, 70)
        }
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
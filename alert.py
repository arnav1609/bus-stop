from flask import Flask, request, jsonify
import yagmail
import random
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

ACCIDENT_EMAIL = os.getenv("ACCIDENT_EMAIL")

def get_random_mumbai_location():
    latitude = round(random.uniform(18.89, 19.30), 6)
    longitude = round(random.uniform(72.75, 72.98), 6)
    return latitude, longitude

def download_map_image(latitude, longitude, filename="map.png"):
    """Downloads a static map image and saves it locally."""
    map_url = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}&z=15&size=450,300&l=map&pt={longitude},{latitude},pm2rdm"
    
    response = requests.get(map_url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        return filename  # Return the file path
    else:
        print("Error: Could not download map image.")
        return None

def send_email(bus_no, latitude, longitude):
    try:
        yag = yagmail.SMTP("jason.dsouza.here@gmail.com", ACCIDENT_EMAIL)
        receiver_email = ["Kkalash.bheda@gmail.com", "arnavbhandari1609@gmail.com"]

        # Download and attach the map image
        map_image = download_map_image(latitude, longitude)

        email_content = f"""
            <h3>🚨 Accident Alert 🚨</h3>
            <p><strong>Bus No:</strong> {bus_no}</p>
            <p><strong>Location:</strong> Latitude {latitude}, Longitude {longitude}</p>
            <p><strong>View on OpenStreetMap:</strong> <a href="https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}#map=15/{latitude}/{longitude}">Click Here</a></p>
            <p><strong>Location Map:</strong></p>
            <img src="cid:map_image" alt="Accident Location" style="width:100%; max-width:450px;">
        """

        # Send email with the map image as an attachment
        yag.send(
            to=receiver_email,
            subject="🚨 Accident Alert - Immediate Attention Required",
            contents=[email_content, yagmail.inline(map_image)] if map_image else email_content
        )

        print("Email sent!")
        return True
    except Exception as e:
        print("Error occurred whilst sending email:", e)
        return False

@app.route("/send_alert", methods=["GET", "POST"])
def send_alert():
    try:
        if request.method == "POST":
            data = request.get_json()
        else:  # Handle GET request with URL query parameters
            data = request.args

        bus_no = data.get("bus_no")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not all([bus_no, latitude, longitude]):
            if not bus_no:
                return jsonify({"status": "failure", "message": "Missing parameters"}), 400
            else:
                latitude, longitude = get_random_mumbai_location()
        
        success = send_email(bus_no, latitude, longitude)
        return jsonify({"status": "success" if success else "failure"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

import requests
import smtplib
import time

# Coordinates of test
MY_LONG = -5.3
MY_LAT = -138.22
COORDINATE_VARIANCE = 5
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}
# SUNRISE SUNSET API interaction
SUNRISE_API = f"https://api.sunrise-sunset.org/json?"
response_sunrise = requests.get(url=SUNRISE_API, params=parameters)
response_sunrise.raise_for_status()
sunrise = int(response_sunrise.json()["results"]["sunrise"].split(sep="T")[1].split(sep=":")[0])
sunset = int(response_sunrise.json()["results"]["sunset"].split(sep="T")[1].split(sep=":")[0])

# ISS API interaction, getting lat and longitude
ISS_API = "http://api.open-notify.org/iss-now.json"
response_ISS = requests.get(url=ISS_API)
response_ISS.raise_for_status()
iss_lat = -137.7514 #float(response_ISS.json()["iss_position"]["latitude"])
iss_lng = -6.0721 #float(response_ISS.json()["iss_position"]["longitude"])


def check_iss_visibility():
    """Determines if ISS is visible, based on darkness and proximity"""
    latitude_in_range = (iss_lat - COORDINATE_VARIANCE) <= MY_LAT <= (iss_lat + COORDINATE_VARIANCE)
    longitude_in_range = (iss_lng - COORDINATE_VARIANCE) <= MY_LONG <= (iss_lng + COORDINATE_VARIANCE)
    iss_in_range = latitude_in_range and longitude_in_range
    time_now = 2 # datetime.datetime.now().hour

    is_dark = time_now >= sunset or time_now <= sunrise
    station_is_visible = iss_in_range and is_dark
    return station_is_visible


starttime = time.time()
time_increment = 3

print("Evaluating visibility of ISS...")
check_iss_visibility()
time.sleep(time_increment - ((time.time() - starttime) % time_increment))
if check_iss_visibility():
    # smtplib credentials
    MY_EMAIL = "hokanuxacatecas@gmail.com"
    MY_PASSWORD = "GGunnar93"
    recipient_email = "husniadan@gmail.com"

    print("Attempting to send notification")
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=recipient_email,
            msg=f"Subject:ISS visibility\n\n It is dark and the ISS is close to your position"
        )
    print("Notification sent")


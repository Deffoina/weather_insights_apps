import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from dotenv import load_dotenv

# charger .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
CITY = "Douala"

# créer dossier data
if not os.path.exists("data"):
    os.makedirs("data")

# API request
url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

if response.status_code != 200:
    print("Erreur API:", data)
    exit()

temp = data['main']['temp']
humidity = data['main']['humidity']
weather = data['weather'][0]['description']

print("City:", CITY)
print("Temp:", temp)
print("Humidity:", humidity)
print("Weather:", weather)

# sauvegarde
df = pd.DataFrame([[datetime.now(), temp, humidity, weather]],
                  columns=['date', 'temp', 'humidity', 'weather'])

df.to_csv('data/history.csv', mode='a', header=False, index=False)

print("Saved!")

# graph
try:
    history = pd.read_csv('data/history.csv',
                          names=['date', 'temp', 'humidity', 'weather'])

    plt.plot(history['temp'], label="Temp")
    plt.plot(history['humidity'], label="Humidity")
    plt.legend()
    plt.title("Weather Trends")
    plt.show()

except:
    print("Not enough data yet")

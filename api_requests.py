import requests
import math

api_key = 'lr86Sx6eyQXbNm32gmmPAuHzzJeXTIfUdzcTjiGB'
url = 'https://api.nasa.gov/neo/rest/v1/'

def get_neo_feed(start_date, end_date):
    response = requests.get(f'{url}feed?start_date={start_date}&end_date={end_date}&api_key={api_key}')
    
    print("Body:")    
    print(response.text)

    data = response.json()
    print("Processed Data:")
    #print(data.get('near_earth_objects', 'No NEO data found'))
    
    meteors = data['near_earth_objects']
    
    
    with open('test.txt', 'w') as mm:
        for date in meteors:
            for neo in meteors[date]:
                name = neo.get('name', 'no name')
                danger = neo.get('is_potentially_hazardous_asteroid')
                size = neo.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_max')
                velocity = neo['close_approach_data'][0]['relative_velocity']['kilometers_per_second']

                radius = size * 1000 / 2
                volume = (4/3) * math.pi * math.cbrt(radius)
                density = volume * 3.0 #Chondrite metorite
                mass = volume * density

                KE = 1/2 * mass * math.sqrt(float(velocity))

                damage = KE / 4.184 * (10 ** 15)



                print(f"Name: {name}, Dangerous: {danger}, Size: {size}, Velocity: {velocity}, Potentioal Damage (MEGA TON): {damage}")
                
                mm.write(f'{name}, {danger},{size}\n')

get_neo_feed('2025-10-04', '2025-10-06')

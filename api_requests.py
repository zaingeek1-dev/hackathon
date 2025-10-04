import requests

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
    
    for date in meteors:
        for neo in meteors[date]:
            name = neo.get('name', 'no name')
            danger = neo.get('is_potentially_hazardous_asteroid')
            size = neo.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_max')
            print(name, danger, size)

get_neo_feed('2025-10-04', '2025-10-06')

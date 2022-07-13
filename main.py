import requests
import json


class Station:
    def __init__(self, id, name, active, description, boxes, free_boxes, free_bikes, longitude, latitude):
        self.id = id
        self.name = name
        # Setting the active as true if the passed active is "aktiv"
        self.active = True if active == 'aktiv' else False
        self.description = description
        self.boxes = boxes
        self.free_boxes = free_boxes
        self.free_bikes = free_bikes
        self.coordinates = [longitude, latitude]
        # Calculating the free_ratio by dividing free boxes with free bikes
        self.free_ratio = free_boxes / free_bikes

# Filtering the stations that have 0 free bikes


def filterList(list):
    filteredStationsList = []

    for station in list:
        if(station['free_bikes'] != 0):
            filteredStationsList.append(station)

    return filteredStationsList


def transformInput(dataList):
    stationsObjectList = []
    stationsList = filterList(dataList)

    # Adding all the filtered stations to our object list
    for station in stationsList:
        stationsObjectList.append(
            Station(station['id'],
                    station['name'],
                    station['status'],
                    station['description'],
                    station['boxes'],
                    station['free_boxes'],
                    station['free_bikes'],
                    station['longitude'],
                    station['latitude']))

    # Sorting the stations ascending by the number of free bikes and descending by name
    stationsObjectList.sort(key=lambda x: (-x.free_bikes, x.name))

    # Returning a list of dictionaries
    return [x.__dict__ for x in stationsObjectList]


def addAddresses(stationsList):
    for station in stationsList:
        # Creating a dictionary with the necessary parameters for the request
        requestParams = {
            "longitude": station['coordinates'][0],
            "latitude": station['coordinates'][1]
        }

        # Query the endpoint for the data with our parameters
        endpointResponse = requests.get(
            "https://api.i-mobility.at/routing/api/v1/nearby_address", params=requestParams)

        addressData = json.loads(endpointResponse.text)

        station['address'] = addressData['data']['name']

    return stationsList


if __name__ == '__main__':

    # Query the endpoint for the data
    endpointResponse = requests.get('https://wegfinder.at/api/v1/stations')
    data = json.loads(endpointResponse.text)

    modifiedList = addAddresses(transformInput(data))
    print(modifiedList)

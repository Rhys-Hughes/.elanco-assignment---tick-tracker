import requests, json

URL = "http://127.0.0.1:5000"


def filter_test():
    payload_json = {
        "filter_term_dictionary" : {"location" : ["London", "Newcastle", "Bristol"]},
        "filter_condition" : "exclude",
        "case_sensitivity" : "case sensitive",
        "time_span_dictionary" : {"date_min" : "2019-01-01", "date_max" : "2019-12.31",
                                  "time_min" : "00-00-00", "time_max" : "05-00-00"}
    }

    response = requests.post(f"{URL}/filter", json = payload_json)
    response_json = response.json()

    if response.json()["success"] == "true":
        for r in response_json["result"]:
            print(r)

    else:
        print(print(response.json()))


def search_test():
    payload_json = {
        "search_term_dictionary" : {"location" : "London"},
        "search_condition" : "and",
        "case_sensitivity" : "case sensitive"
    }
    payload_json = {
        "search_term_dictionary" : {},
        "search_condition" : "and",
        "case_sensitivity" : "case sensitive"
    }

    response = requests.post(f"{URL}/search", json = payload_json)
    response_json = response.json()

    if response.json()["success"] == "true":
        for r in response_json["result"]:
            print(r)

    else:
        print(print(response.json()))


def x_per_y_tests():
    payload_json_location = {
        "location" : "London"
    }
    payload_json_species = {
        "species" : "Marsh tick"
    }

    response = requests.post(f"{URL}/species_per_location", json = payload_json_location)
    print(response.json())
    response = requests.post(f"{URL}/sightings_per_location", json = payload_json_location)
    print(response.json())  
    response = requests.post(f"{URL}/sightings_per_species", json = payload_json_species)
    print(response.json())      


def search_test_wildcards():
    payload_json = {
        "search_term_dictionary" : {"date" : "2022%"},
        "search_condition" : "and",
        "case_sensitivity" : "case sensitive"
    }

    response = requests.post(f"{URL}/search", json = payload_json)
    response_json = response.json()

    if response.json()["success"] == "true":
        for r in response_json["result"]:
            print(r)

    else:
        print(print(response.json()))


def x_over_time_tests():
    species_over_time_json = {
        "time_period" : "week",
        "species" : "Marsh tick",
        "fill_missing" : "no fill"
    }
    response = requests.post(f"{URL}/species_over_time", json = species_over_time_json)
    print(response.json())

    sightings_over_time_json = {
        "time_period" : "week",
        "fill_missing" : "no fill"
    }
    response = requests.post(f"{URL}/sightings_over_time", json = sightings_over_time_json)
    print(response.json())

    location_over_time_json = {
        "time_period" : "week",
        "location" : "Liverpool",
        "fill_missing" : "no fill"
    }
    response = requests.post(f"{URL}/location_over_time", json = location_over_time_json)
    print(response.json())


filter_test()
#search_test()
#x_per_y_tests()
#search_test_wildcards()
#x_over_time_tests()

#response = requests.post(f"{URL}/get_all_unique", json = {"field" : "location"})
#print(response.json())
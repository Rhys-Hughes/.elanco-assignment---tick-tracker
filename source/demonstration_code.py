import requests
# - the following code is designed for demonstration

URL = "http://127.0.0.1:5000"

def execute(payload, function):

    response = requests.post(f"{URL}/{function}", json = payload)
    response_json = response.json()

    print(20*"=")
    print(7*" " + "results")
    print(20*"=")

    if response.json()["success"] == "true":

        if type(response_json["result"]) == list:

            for r in response_json["result"]:
                print(r) 
        
        else:
            print(response_json["result"])
            
    else:
        print(response.json()["error"])

    print(20*"=")


def search():
    payload = {"search_term_dictionary" : {"location" : "liverpool", "species" : "marsh tick"},
               "search_condition" : "and",
               "case_sensitivity" : "not case sensitive"}
    execute(payload, "search")

def filter():
    payload = {"filter_term_dictionary" : {"location" : ["London", "Glasgow", "Manchester"]},
               "filter_condition" : "exclude",
               "case_sensitivity" : "case sensitive",
               "time_span_dictionary" : {"date_max" : "2020-01-01"}}
    execute(payload, "filter")

def species_per_location():
    payload = {"location" : "Birmingham"}
    execute(payload, "species_per_location")

def sightings_per_location():
    payload = {"location" : "Manchester"}
    execute(payload, "sightings_per_location")

def sightings_per_species():
    payload = {"species" : "Marsh tick"}
    execute(payload, "sightings_per_species")

def species_over_time():
    payload = {"time_period" : "month",
               "species" : "Marsh tick",
               "fill_missing" : "no fill"}
    execute(payload, "species_over_time")

def sightings_over_time():
    payload = {"time_period" : "year",
               "fill_missing" : "fill"}
    execute(payload, "sightings_over_time")

def location_over_time():
    payload = {"time_period" : "week",
               "location" : "Liverpool",
               "fill_missing" : "fill"}
    execute(payload, "location_over_time")

def get_all_unique():
    payload = {"field" : "location"}
    execute(payload, "get_all_unique")


def menu():
    while True:
        print("a - search()")
        print("b - filter()")
        print("c - species_per_location()")
        print("d - sightings_per_location()")
        print("e - sightings_per_species()")
        print("f - species_over_time()")
        print("g - sightings_over_time()")
        print("h - location_over_time()")
        print("i - get_all_unique()")

        choice = input(">>> ")

        match choice:

            case "a":
                search()

            case "b":
                filter()

            case "c":
                species_per_location()

            case "d":
                sightings_per_location()

            case "e":
                sightings_per_species()

            case "f":
                species_over_time()

            case "g":
                sightings_over_time()

            case "h":
                location_over_time()

            case "i":
                get_all_unique()


menu()
from flask import Flask, request, jsonify
import tick_tracker as tt
import ast

app = Flask(__name__)

DATABASE_INFORMATION = tt.tt_get_database_information()


def is_key_in_json(json, valid_keys):
    keys_valid = True
    for key in json:
        if not (key in valid_keys):
            keys_valid = False
    return keys_valid



# this is the search function
# Returns values that meet the search criteria
# 
#   - search_term_dictionary : dictionary : {"database column" : ["desired values"], "database column" : "desired value"} -> defines the columns and their desired terms 
#   - search_condition       : string     : "and" or "or" -> determines if a record must have all of the terms, or just one   
#   - case_sensitivity       : string     : "case sensitive" or "not case sensitive" -> determines if the search will check the case of the field when comparing
#
# -- FURTHER INFORMATION IN THE DOCUMENTATION FILE --
@app.route("/search", methods = ["POST"])
def search():

    data = request.get_json()
    print(data)
    search_term_dictionary = data["search_term_dictionary"]
    search_condition = data["search_condition"] 
    case_sensitivity = data["case_sensitivity"] 

    #validation checking
    search_condition_valid = (search_condition == "or" or search_condition == "and")
    case_sensitivity_valid = (case_sensitivity == "case sensitive" or case_sensitivity == "not case sensitive")


    #ensuring that the correct database columns are referenced
    if search_term_dictionary != {}:
        term_columns_valid = is_key_in_json(search_term_dictionary, DATABASE_INFORMATION["database_columns"])
    else:
        return jsonify({"success" : "false", 
                        "error" : "search _term_dictionary is empty, please add values in order to search"})
 

    # catches early errors like incorrectly formatted conditions and columns
    if search_condition_valid and case_sensitivity_valid and term_columns_valid:

        # calling the function that actually does the search
        results = tt.search(search_term_dictionary, search_condition, case_sensitivity)

        if results == "error":
            return jsonify({"success" : "false", 
                            "error" : "Failed call"})
        else:
            return jsonify({"success" : "true", 
                            "result" : results})
         
    else:
        return jsonify({"success" : "false", 
                        "error" : "Failed search call", 
                        "search_condition valid" : search_condition_valid, 
                        "case_sensitivity valid" : case_sensitivity_valid,
                        "search_term_dictionary valid" : term_columns_valid,
                        "---" : "please reference the relevant documentation on search for more information"})



# this is the filter function
# Returns values that either meet, or do nor meet the filter conditions
# 
#   - filter_term_dictionary : dictionary : {"database column" : ["desired values"], "database column" : "desired value"} -> defines the columns and their desired terms 
#   - filter_condition       : string     : "include" or "exclude" -> determines if a record must have, or must not have the terms   
#   - case_sensitivity       : string     : "case sensitive" or "not case sensitive" -> determines if the search will check the case of the field when comparing
#   - time_span_dictionary   : dictionary : {"date_min" : "yyyy-mm-dd", "date_max" : "yyyy-mm-dd", "time_min" : "hh-mm-ss", "time_max" : "hh-mm-ss"} -> defines a time span that the filter must be within
#
# -- FURTHER INFORMATION IN THE DOCUMENTATION FILE --
@app.route("/filter", methods = ["POST"])
def filter():

    data = request.get_json()
    filter_term_dictionary = data["filter_term_dictionary"]
    filter_condition = data["filter_condition"] 
    case_sensitivity = data["case_sensitivity"] 
    time_span_dictionary = data["time_span_dictionary"]

    # validation checking
    filter_condition_valid = (filter_condition == "include" or filter_condition == "exclude")
    case_sensitivity_valid = (case_sensitivity == "case sensitive" or case_sensitivity == "not case sensitive")


    # ensuring that the correct database columns are referenced
    if filter_term_dictionary != {}:
        term_columns_valid = is_key_in_json(filter_term_dictionary, DATABASE_INFORMATION["database_columns"])
    else:
        term_columns_valid = True


    # ensuring that the correct time spans are used
    if time_span_dictionary != {}:
        time_span_valid = is_key_in_json(time_span_dictionary, ["date_min", "date_max", "time_min", "time_max"])
    else:
        time_span_valid = True


    # ensures that both the input dictionaries have at least something in them
    if filter_term_dictionary == {} and time_span_dictionary == {}:
        return jsonify({"success" : "false", 
                        "error" : "Both filter_term_dictionary and time_span_dictionary are empty, please add values in order to filter"})


    # catches early errors like incorrectly formatted conditions
    if filter_condition_valid and case_sensitivity_valid and term_columns_valid and time_span_valid:

        # calling the function that actually does the filtering
        results = tt.filter(filter_term_dictionary, filter_condition, case_sensitivity, time_span_dictionary)

        if results == "error":
            return jsonify({"success" : "false", 
                            "error" : "Failed call"})
        else:
            return jsonify({"success" : "true", 
                            "result" : results})
        
    else:
        return jsonify({"success" : "false", 
                        "error" : "Failed filter call", 
                        "filter_condition valid" : filter_condition_valid, 
                        "case_sensitivity valid" : case_sensitivity_valid,
                        "filter_term_dictionary" : term_columns_valid,
                        "time_span_dictionary" : time_span_valid,
                        "---" : "please reference the relevant documentation on filter for more information"})



# data aggregation
# the functions which provide analytics to the frontend
#
# -- FURTHER INFORMATION IN THE DOCUMENTATION FILE --
# 

#returns a list of the unique species
@app.route("/species_per_location", methods = ["POST"])
def species_per_location():
    data = request.get_json()

    # if the key provided is correct the call proceeds
    if is_key_in_json(data, ["location"]):
        location = data["location"]

        results = tt.species_per_location(location)
        return jsonify({"success" : "true", 
                        "result" : results})
    
    else:
        return jsonify({"success" : "false", 
                        "error" : "unrecognised json key, please ensure the only key is 'location'"})

#returns an int of how many sightings there are per location
@app.route("/sightings_per_location", methods = ["POST"])
def sightings_per_location():
    data = request.get_json()

    # if the key provided is correct the call proceeds
    if is_key_in_json(data, ["location"]):
        location = data["location"]

        results = tt.sightings_per_location(location)
        return jsonify({"success" : "true", 
                        "result" : results})
    
    else:
        return jsonify({"success" : "false", 
                        "error" : "unrecognised json key, please ensure the only key is 'location'"})

#returns an int of how many sightings there are per species
@app.route("/sightings_per_species", methods = ["POST"])
def sightings_per_species():
    data = request.get_json()

    # if the key provided is correct the call proceeds
    if is_key_in_json(data, ["species"]):
        species = data["species"]

        results = tt.sightings_per_species(species)
        return jsonify({"success" : "true", 
                        "result" : results})
    
    else:
        return jsonify({"success" : "false", 
                        "error" : "unrecognised json key, please ensure the only key is 'species'"})



# - starting from the earliest possible date
# returns an array containing dictionaries pairing the date seen/started from, and the number of sightings for that species
@app.route("/species_over_time", methods = ["POST"])
def species_over_time():
    data = request.get_json()

    # if the keys provided are correct the call proceeds
    if is_key_in_json(data, ["time_period", "species", "fill_missing"]):
        time_period = data["time_period"]
        species = data["species"]
        fill_missing = data["fill_missing"]

        # validating the time period
        if ((time_period == "day") or (time_period == "week") or (time_period == "month") or (time_period == "year")) and ((fill_missing == "fill") or (fill_missing == "no fill")):

            # running the actual function
            results = tt.species_over_time(time_period, species, fill_missing)
            return jsonify({"success" : "true",
                            "result" : results})
        
        else:
            return jsonify({"success" : "false", 
                            "error" : "Failed species_over_time call, time_period may be incorrect, please enter 'day', 'week', 'month', or 'year', or fill_missing may be incorrect, please enter 'fill' or 'no fill'"})
    else:
        return jsonify({"success" : "false", 
                        "error" : "Failed species_over_time call, parameters are incorrect, please ensure you have 'time_period', 'species', and 'fill_missing' in your POST Json"})


# returns an array containing dictionaries pairing the date seen/started from, and the number of sightings in that week
@app.route("/sightings_over_time", methods = ["POST"])
def sightings_over_time():
    data = request.get_json()

    # if the keys provided are correct the call proceeds
    if is_key_in_json(data, ["time_period", "fill_missing"]):
        time_period = data["time_period"]
        fill_missing = data["fill_missing"]

        # validating the time period
        if ((time_period == "day") or (time_period == "week") or (time_period == "month") or (time_period == "year")) and ((fill_missing == "fill") or (fill_missing == "no fill")):

            # running the actual function
            results = tt.sightings_over_time(time_period, fill_missing)
            return jsonify({"success" : "true",
                            "result" : results})
        
        else:
            return jsonify({"success" : "false", 
                            "error" : "Failed sightings_over_time call, time_period may be incorrect, please enter 'day', 'week', 'month', or 'year', or fill_missing may be incorrect, please enter 'fill' or 'no fill'"})
    else:
        return jsonify({"success" : "false", 
                        "error" : "Failed sightings_over_time call, parameters are incorrect, please ensure you have 'time_period', 'species', and 'fill_missing' in your POST Json"})


# returns an array containing dictionaries pairing the date seen/started from, and the number of sightings for that location
@app.route("/location_over_time", methods = ["POST"])
def location_over_time():
    data = request.get_json()

    # if the keys provided are correct the call proceeds
    if is_key_in_json(data, ["time_period", "location", "fill_missing"]):
        time_period = data["time_period"]
        species = data["location"]
        fill_missing = data["fill_missing"]

        # validating the time period
        if ((time_period == "day") or (time_period == "week") or (time_period == "month") or (time_period == "year")) and ((fill_missing == "fill") or (fill_missing == "no fill")):

            # running the actual function
            results = tt.location_over_time(time_period, species, fill_missing)
            return jsonify({"success" : "true",
                            "result" : results})
        
        else:
            return jsonify({"success" : "false", 
                            "error" : "Failed location_over_time call, time_period may be incorrect, please enter 'day', 'week', 'month', or 'year', or fill_missing may be incorrect, please enter 'fill' or 'no fill'"})
    else:
        return jsonify({"success" : "false", 
                        "error" : "Failed location_over_time call, parameters are incorrect, please ensure you have 'time_period', 'species', and 'fill_missing' in your POST Json"})



#gets all the unique values from a given column, so every unique location, every unique species, etc
@app.route("/get_all_unique", methods = ["POST"])
def get_all_unique():
    data = request.get_json()

    # if the keys provided are correct the call proceeds
    if is_key_in_json(data, ["field"]):
        subject = data["field"]

        # validating the time period
        if  subject in DATABASE_INFORMATION["database_columns"]:

            # running the actual function
            results = tt.get_all_unique(subject)
            return jsonify({"success" : "true",
                            "result" : results})
        
        else:
            return jsonify({"success" : "false", 
                            "error" : f"Failed get_all_unique call, your field is not in the database, please choose an appropriate field : {DATABASE_INFORMATION["database_columns"]}"})
    else:
        return jsonify({"success" : "false", 
                        "error" : "Failed get_all_unique, parameters are incorrect, please ensure you have only 'field' in your POST Json"})



if __name__ == "__main__":
    app.run(debug = False)
    print(" -- flask server running -- ")
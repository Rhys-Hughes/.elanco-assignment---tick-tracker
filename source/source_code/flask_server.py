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
    term_columns_valid = is_key_in_json(search_term_dictionary, DATABASE_INFORMATION["database_columns"])
 
    # catches early errors like incorrectly formatted conditions and columns
    if search_condition_valid and case_sensitivity_valid and term_columns_valid:

        # calling the function that actually does the search
        results = tt.search(search_term_dictionary, search_condition, case_sensitivity)

        if results == "error":
            return jsonify({"ERROR" : "Failed call"})
        else:
            return jsonify({"results" : results})
        
    else:
        return jsonify({"ERROR" : "Failed search call", 
                        "SEARCH CONDITION VALID" : search_condition_valid, 
                        "CASE SENSITIVITY VALID" : case_sensitivity_valid,
                        "TERM COLUMNS VALID" : term_columns_valid,
                        "---" : "please reference the relevant documentation on search for more information"})



# this is the filter function
# Returns values that either meet, or do nor meet the filter conditions
# 
#   - filter_term_dictionary : dictionary : {"database column" : ["desired values"], "database column" : "desired value"} -> defines the columns and their desired terms 
#   - filter_condition       : string     : "include" or "exclude" -> determines if a record must have, or must not have the terms   
#   - case_sensitivity       : string     : "case sensitive" or "not case sensitive" -> determines if the search will check the case of the field when comparing
#   - time_span_dictionary   : dictionary : {"date_from" : "yyyy.mm.dd", "date_to" : "yyyy.mm.dd", "time_from" : "hh.mm.ss", "time_to" : "hh.mm.ss"} -> defines a time span that the filter must be within
#
# -- FURTHER INFORMATION IN THE DOCUMENTATION FILE --

@app.route("/filter", methods = ["POST"])
def filter():

    data = request.get_json()
    filter_term_dictionary = data["filter_term_dictionary"]
    filter_condition = data["filter_condition"] 
    case_sensitivity = data["case_sensitivity"] 
    time_span_dictionary = data["time_span_dictionary"]

    #validation checking
    filter_condition_valid = (filter_condition == "include" or filter_condition == "exclude")
    case_sensitivity_valid = (case_sensitivity == "case sensitive" or case_sensitivity == "not case sensitive")

    #ensuring that the correct database columns are referenced
    term_columns_valid = is_key_in_json(filter_term_dictionary, DATABASE_INFORMATION["database_columns"])

    #ensuring that the correct time spans are used
    time_span_valid = is_key_in_json(time_span_dictionary, ["date_min", "date_max", "time_min", "time_max"])


    # catches early errors like incorrectly formatted conditions
    if filter_condition_valid and case_sensitivity_valid and term_columns_valid and time_span_valid:

        # calling the function that actually does the filtering
        results = tt.filter(filter_term_dictionary, filter_condition, case_sensitivity, time_span_dictionary)

        if results == "error":
            return jsonify({"ERROR" : "Failed call"})
        else:
            return jsonify({"results" : results})
        
    else:
        return jsonify({"ERROR" : "Failed filter call", 
                        "FILTER CONDITION VALID" : filter_condition_valid, 
                        "CASE SENSITIVITY VALID" : case_sensitivity_valid,
                        "TERM COLUMNS VALID" : term_columns_valid,
                        "TIME SPAN ENTRIES VALID" : time_span_valid,
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

    if is_key_in_json(data, ["location"]):
        location = data["location"]
        results = tt.species_per_location(location)
        return jsonify(results)
    else:
        return jsonify({"ERROR" : "unrecognised json key, please ensure the only key is 'location'"})

#returns an int of how many sightings there are per location
@app.route("/sightings_per_location", methods = ["POST"])
def sightings_per_location():
    data = request.get_json()

    if is_key_in_json(data, ["location"]):
        location = data["location"]
        results = tt.sightings_per_location(location)
        return jsonify(results)
    else:
        return jsonify({"ERROR" : "unrecognised json key, please ensure the only key is 'location'"})

#returns an int of how many sightings there are per species
@app.route("/sightings_per_species", methods = ["POST"])
def sightings_per_species():
    data = request.get_json()

    if is_key_in_json(data, ["species"]):
        species = data["species"]
        results = tt.sightings_per_species(species)
        return jsonify(results)
    else:
        return jsonify({"ERROR" : "unrecognised json key, please ensure the only key is 'species'"})



# - starting from the earliest possible date
# returns an array of the 
@app.route("/species_over_time/<time_period>/<start_date>")
def species_over_time(time_period, start_date):
    if (time_period == "day") or (time_period == "week") or (time_period == "month") or (time_period == "year"):
        results = tt.species_over_time(time_period, start_date)
        return jsonify(results)
    else:
        return jsonify({"ERROR" : "Failed species_over_time call",
                        "DESCRIPTION" : "time_period is incorrect, please enter 'day', 'week', 'month', or 'year'"})

@app.route("/sightings_over_time/<time_period>/<start_date>")
def sightings_over_time(time_period, start_date):
    if (time_period == "day") or (time_period == "week") or (time_period == "month") or (time_period == "year"):
        results = tt.sightings_over_time(time_period, start_date)
        return jsonify(results)
    else:
        return jsonify({"ERROR" : "Failed sightings_over_time call",
                        "DESCRIPTION" : "time_period is incorrect, please enter 'day', 'week', 'month', or 'year'"})

@app.route("/location_over_time/<time_period>/<start_date>")
def location_over_time(time_period, start_date):
    if (time_period == "day") or (time_period == "week") or (time_period == "month") or (time_period == "year"):
        results = tt.location_over_time(time_period, start_date)
        return jsonify(results)
    else:
        return jsonify({"ERROR" : "Failed location_over_time call",
                        "DESCRIPTION" : "time_period is incorrect, please enter 'day', 'week', 'month', or 'year'"})



# calculates the metric per category over time
@app.route("/aggregate_metric_per_category_over_time/<metric>/<category>/<time>")
def metric_per_category_over_time(metric, category, time):
    results = tt.metric_per_category_over_time(metric, category, time)
    return jsonify(results)




if __name__ == "__main__":
    print(DATABASE_INFORMATION)
    app.run(debug = True)
from flask import Flask, request, jsonify
import tick_tracker as tt
import ast

app = Flask(__name__)

DATABASE_INFORMATION = tt.tt_get_database_information()

# this is a basic connection test that shows connectivity with the database as well as showing a test variable passed in
@app.route("/connection_test/<test_var>")
def connection_test(test_var):
    results = tt.connection_test(test_var)

    return jsonify(results)



# this is the search function
# Returns values that meet the search criteria
# 
#   - search_term_dictionary : dictionary : {"database column" : ["desired values"], "database column" : "desired value"} -> defines the columns and their desired terms 
#   - search_condition       : string     : "and" or "or" -> determines if a record must have all of the terms, or just one   
#   - case_sensitivity       : string     : "case sensitive" or "not case sensitive" -> determines if the search will check the case of the field when comparing
#
# -- FURTHER INFORMATION IN THE DOCUMENTATION FILE --
@app.route("/search/<search_term_dictionary>/<search_condition>/<case_sensitivity>")
def search(search_term_dictionary, search_condition, case_sensitivity):

    #validation checking
    search_condition_valid = (search_condition == "or" or search_condition == "and")
    case_sensitivity_valid = (case_sensitivity == "case sensitive" or case_sensitivity == "not case sensitive")

    #converting the search_term_dictionary into an actual dictionary
    #THIS IS NOT GREAT PRACTICE, CHANGING TO JSON WOULD BE BETTER
    search_term_dictionary = ast.literal_eval(search_term_dictionary)

    #ensuring that the correct database columns are referenced
    term_columns_valid = True
    for key in search_term_dictionary:
        if not (key in DATABASE_INFORMATION["database_columns"]):
            term_columns_valid = False

    # catches early errors like incorrectly formatted conditions and columns
    if search_condition_valid and case_sensitivity_valid and term_columns_valid:

        # calling the function that actually does the search
        results = tt.search(search_term_dictionary, search_condition, case_sensitivity)

        if results == "error":
            return jsonify({"ERROR" : "Failed call"})
        else:
            return jsonify(results)
        
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

# to do : MAKE THE FILTER ACCEPT TIME CONSTRAINTS 

@app.route("/filter/<filter_term_dictionary>/<filter_condition>/<case_sensitivity>/<time_span_dictionary>")
def filter(filter_term_dictionary, filter_condition, case_sensitivity, time_span_dictionary):

    #validation checking
    filter_condition_valid = (filter_condition == "include" or filter_condition == "exclude")
    case_sensitivity_valid = (case_sensitivity == "case sensitive" or case_sensitivity == "not case sensitive")

    #converting the filter_term_dictionary into an actual dictionary
    #THIS IS NOT GREAT PRACTICE, CHANGING TO JSON WOULD BE BETTER
    filter_term_dictionary = ast.literal_eval(filter_term_dictionary)

    #ensuring that the correct database columns are referenced
    term_columns_valid = True
    for key in filter_term_dictionary:
        print(key)
        if not (key in DATABASE_INFORMATION["database_columns"]):
            term_columns_valid = False

    # catches early errors like incorrectly formatted conditions
    if filter_condition_valid and case_sensitivity_valid and term_columns_valid:

        # calling the function that actually does the filtering
        results = tt.filter(filter_term_dictionary, filter_condition,case_sensitivity)

        if results == "error":
            return jsonify({"ERROR" : "Failed call"})
        else:
            return jsonify(results)
        
    else:
        return jsonify({"ERROR" : "Failed filter call", 
                        "FILTER CONDITION VALID" : filter_condition_valid, 
                        "CASE SENSITIVITY VALID" : case_sensitivity_valid,
                        "TERM COLUMNS VALID" : term_columns_valid,
                        "---" : "please reference the relevant documentation on filter for more information"})



# data aggregation
# the functions which provide analytics to the frontend
#
# -- FURTHER INFORMATION IN THE DOCUMENTATION FILE --
# 

#returns a list of the unique species
@app.route("/species_per_location/<location>")
def species_per_location(location):
    results = tt.species_per_location(location)
    return jsonify(results)

#returns an int of how many sightings there are per location
@app.route("/sightings_per_location/<location>")
def sightings_per_location(location):
    results = tt.sightings_per_location(location)
    return jsonify(results)

#returns an int of how many sightings there are per species
@app.route("/sightings_per_species/<species>")
def sightings_per_species(species):
    results = tt.sightings_per_species(species)
    return jsonify(results)



# calculates the metric over time
@app.route("/aggregate_metric_over_time/<metric>/<time>")
def metric_over_time(metric, time):
    results = tt.metric_over_time(metric, time)
    return jsonify(results)

# calculates the metric per category over time
@app.route("/aggregate_metric_per_category_over_time/<metric>/<category>/<time>")
def metric_per_category_over_time(metric, category, time):
    results = tt.metric_per_category_over_time(metric, category, time)
    return jsonify(results)




#
# THIS IS DEBUGGING CODE, DELETE IN PRODUCTION, THIS IS PURELY FOR INTERNAL USE WHEN ACCESSING THE DATABASE SYSTEM, IT IS INCREDIBLY INSECURE
#
@app.route("/command_database/<command>")
def command_database(command):
    if request.remote_addr != "127.0.0.1":
        return jsonify("ACCESS DENIED")
    else:
        results = tt.command_database(command)
        return jsonify(results)



if __name__ == "__main__":
    print(DATABASE_INFORMATION)
    app.run(debug = True)
from flask import Flask, request, jsonify
import tick_tracker as tt

app = Flask(__name__)

# this is a basic connection test that shows connectivity with the database as well as showing a test variable passed in
@app.route("/connection_test/<test_var>")
def connection_test(test_var):
    results = tt.connection_test(test_var)

    return jsonify(results)



# this is the search function, it asks for 2 terms
# the search_term_dictionary is an associative array/dictionary which marks what fields and what values are desired
# the search_condition is the logical condition used, for example AND, or OR
# case sensitivity determines whether or not the case of the search conditions matters
#
# -- FURTHER INFORMATION IN THE DOCUMENTATION FILE --
#
@app.route("/search/<search_term_dictionary>/<search_condition>/<case_sensitivity>")
def search(search_term_dictionary, search_condition, case_sensitivity):

    # catches early errors like incorrectly formatted conditions
    if (search_condition == "or" or search_condition == "and") and (case_sensitivity == "case sensitive" or case_sensitivity == "not case sensitive"):

        # actually does the seach
        results = tt.search(search_term_dictionary, search_condition, case_sensitivity)

        if results == "error":
            return jsonify({"ERROR" : "Failed call, ensure search_term_dictionary is correctly formatted"})
        else:
            return jsonify(results)
        
    else:
        return jsonify({"ERROR" : "Failed call, please ensure that search_condition is 'or' or 'and', and that is case_sensitivity is 'case sensitive' or 'not case sensitive'"})



# this is the word filter function, it asks for 2 terms
# the filter_term_dictionary is a dictionary which marks what fields are filtered, and by what values
# note that dates/times are valid here, from_date, from_time, to_date, and to_time are all accepted
# the filter_condition marks whether this is an inclusionary or exclusionary filter
#
# -- FURTHER INFORMATION IN THE DOCUMENTATION FILE --
#
@app.route("/filter/<filter_term_dictionary>/<filter_condition>/<case_sensitivity>")
def filter(filter_term_dictionary, filter_condition, case_sensitivity):
    results = tt.filter(filter_term_dictionary, filter_condition,case_sensitivity)
    return jsonify(results)



# data aggregation
# the functions which provide analytics to the frontend
#
# -- FURTHER INFORMATION IN THE DOCUMENTATION FILE --
# 

# calculates the metric per category
# category is a dictionary in the form {"group" : data} - for example {"region" : "Manchester"}
@app.route("/aggregate_metric_per_category/<metric>/<category>")
def metric_per_category(metric, category):


    if True:
        results = tt.metric_per_category(metric, category)

        if results == "error":
            return jsonify({"ERROR" : "Failed call"})
        else:
            return jsonify(results)
    
    else:
        return jsonify({"ERROR" : "Failed call, please ensure that metric is 'species' or 'sightings', and that the category is 'region' or 'species'. -- Please note: metric = 'species', category = 'species' together is not allowed. There is 1 species per species."})

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
    app.run(debug = True)
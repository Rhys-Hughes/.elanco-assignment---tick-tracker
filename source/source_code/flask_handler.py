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
#
# -- FURTHER INFORMATION IN THE DOCUMENTATION FILE --
#
@app.route("/word_search/<search_term_dictionary>/<search_condition>")
def search(search_term_dictionary, search_condition):
    results = tt.search(search_term_dictionary, search_condition)
    return jsonify(results)



# this is the word filter function, it asks for 2 terms
# the filter_term_dictionary is a dictionary which marks what fields are filtered, and by what values
# note that dates/times are valid here, from_date, from_time, to_date, and to_time are all accepted
# the filter_condition marks whether this is an inclusionary or exclusionary filter
#
# -- FURTHER INFORMATION IN THE DOCUMENTATION FILE --
#
@app.route("/word_filter/<filter_term_dictionary>/<filter_condition>")
def filter(filter_term_dictionary, filter_condition):
    results = tt.filter(filter_term_dictionary, filter_condition)
    return jsonify(results)








# the aggregate functions still need some refining

# provides
# sightings per region  - how many entries of x region
# sightings per species - how many entries of x species
#
# -- FURTHER INFORMATION IN THE DOCUMENTATION FILE --
#
@app.route("/aggregate_per/<condition>/<subjects>")
def aggregate_per(condition, subject):
    results = tt.aggregate_per(condition, subject)
    return jsonify(results)


# this is the aggregate time trends function, it shows the x per y over time
# the condition is the thing we are counting, this can be 
@app.route("/aggregate_time_trends/<condition>/<subject>/<time_frame>")
def aggregate_time_trends(condition, subject, time_frame):
    results = tt.aggregate_time_trends(condition, subject, time_frame)
    return jsonify(results)



if __name__ == "__main__":  
    app.run(debug = True)
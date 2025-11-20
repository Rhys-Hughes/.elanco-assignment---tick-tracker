import database_manager as dbm, ast

# the manager code that will start the various functions

def tt_connect_to_database():
    connection, cursor = dbm.connect_to_database()
    return connection, cursor



# ========================================================================================================
#                                               SEARCH
# ========================================================================================================

# search_term_dictionary : a dictionary pairing a data field with its desired value, eg {"location" : "Liverpool", "species" : "Marsh tick"}
# case_sensitivity : either "case sensitive" or "not case sensitive", used to set the case_sensitivity_mark
                    # case_sensitivity_mark : either "LOWER" or "", inserted into SQL to force it to ignore cases or not by either making everything
                    #                         lower case, or leaving everything as it is
# search condition : the condition that determines the relationship between the search terms, "and" or "or", for example, location = "Liverpool" AND species = "marsh tick"

# checks the case sensitivity and sets the case_sensitivity_mark
def case_sensitivity_check(search_term_dictionary, case_sensitivity):

    # this is the statement which will be inserted into our SQL to make it lower case if need be
    case_sensitivity_mark = ""

    # apply case sensitivity rules
    #   case sensitivity in SQL statements is denoted with LOWER() and UPPER()
    #   for these purposes we will put everything in lower case if the case sensitivity is "case sensitive"
    if case_sensitivity == "not case sensitive":
        case_sensitivity_mark = "LOWER"

        # going through the search term dictionary and making everything lower case
        for key, term in search_term_dictionary.items():
            search_term_dictionary[key] = term.lower()

    return search_term_dictionary, case_sensitivity_mark


def generate_SELECT_criteria(search_term_dictionary, search_condition, case_sensitivity_mark):
    # what we will store unformatted criteria in
    criteria_list = []

    # each search term will be accounted for
    for key, term in search_term_dictionary.items():

        # this will generate a chunk of the SQL syntax, it could look something like:
        # "LOWER(`location`) = LOWER('Liverpool')", or "(`location`) = ('Liverpool')" if there is case sensitivity
        criteria_list.append(f"{case_sensitivity_mark}(`{key}`) = {case_sensitivity_mark}('{term}')")

    # now we stitch together the individual criteria using the search_condition (and/or)
    search_condition = search_condition.upper() # <-- this is mostly for formatting since SQL should be upper case

    # to store our final output, starts with a space
    criteria_string = " "
    for i in range(len(criteria_list)):
        # if not the final criteria, a the search condition "and" or "or" will be appended
        if i != len(criteria_list) - 1:
            criteria_string += f"{criteria_list[i]} {search_condition} "
        
        # if it is teh final criteria, no search condition will be appended
        else:
            criteria_string += f"{criteria_list[i]} "
        
    return criteria_string
    

# search the data set for time range and location, adding species too
def search(search_term_dictionary, search_condition, case_sensitivity):
    connection, cursor = tt_connect_to_database()

    try:
        # getting the search_term_dictionary into dictionary form
        search_term_dictionary = ast.literal_eval(search_term_dictionary)

        # creating the prerequisites to any case sensitivity enforcement
        search_term_dictionary, case_sensitivity_mark = case_sensitivity_check(search_term_dictionary, case_sensitivity)

        # generates a string which will indicate our criteria in the system
        select_criteria = generate_SELECT_criteria(search_term_dictionary, search_condition, case_sensitivity_mark)

        command = f"""
                    SELECT * FROM `sightings` WHERE {select_criteria}; 
                   """

        results = dbm.command_database(cursor, command)

        print(command)

        return results

    except Exception as e:
        # a more accurate error message will be given by the flask_server
        return "error"




# ========================================================================================================
#                                               FILTER
# ========================================================================================================

# filter out or filter in specific ranges of data, eg locations, times, etc
def filter(filter_term_dictionary, filter_condition,case_sensitivity):
    connection, cursor = tt_connect_to_database()



# ========================================================================================================
#                                            AGGREGATION
# ========================================================================================================
# category is a dictionary formatted as {group : data}, for example, {"location" : "manchester"}


# calculates the metric per category
def metric_per_category(metric, category):
    connection, cursor = tt_connect_to_database()



# calculates the metric over time
def metric_over_time(metric, time):
    connection, cursor = tt_connect_to_database()



# calculates the metric per category over time
def metric_per_category_over_time(metric, category, time):
    connection, cursor = tt_connect_to_database()



# directly queries the database
def command_database(command):
    connection, cursor = tt_connect_to_database()   
    results = dbm.command_database(cursor, command)
    return results 


# connection testing
def connection_test(test_var):
    connection, cursor = tt_connect_to_database()
    return {
        "database_contents" : cursor,
        "test_variable" : test_var
    }



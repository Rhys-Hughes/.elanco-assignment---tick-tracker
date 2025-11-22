import database_manager as dbm, ast

# the manager code that will start the various functions

def tt_connect_to_database():
    connection, cursor = dbm.connect_to_database()
    return connection, cursor

def tt_get_database_information():
    columns = dbm.get_database_information()
    return columns


# ========================================================================================================
#                                               SQL GENERATION
# ========================================================================================================

# checks the case sensitivity and sets the case_sensitivity_mark
def case_sensitivity_check(case_sensitivity):

    # this is the statement which will be inserted into our SQL to make it lower case if need be
    case_sensitivity_mark = ""

    # apply case sensitivity rules
    #   case sensitivity in SQL statements is denoted with LOWER() and UPPER()
    #   for these purposes we will put everything in lower case if the case sensitivity is "case sensitive"
    if case_sensitivity == "not case sensitive":
        case_sensitivity_mark = "LOWER"

    return case_sensitivity_mark

# generates a string containing the select criteria of an SQL select statement
def generate_SELECT_criteria(term_dictionary, select_condition, case_sensitivity_mark, equals_sign):
    try:
        # what we will store unformatted criteria in
        criteria_list = []
        # argument list is used to pass the arguments to the command execute
        argument_list = []

        # each search term will be accounted for
        for key, term in term_dictionary.items():

            # this will generate a chunk of the SQL syntax, it could look something like:
            # "LOWER(`location`) = LOWER('Liverpool')", or "(`location`) = ('Liverpool')" if there is case sensitivity
            # the ? symbol is for parametarised input, they are used to prevent SQL injection
            try:
                #if the term is not a list
                if type(term) == list:
                    for item in term:
                        criteria_list.append(f"{case_sensitivity_mark}(`{key}`) {equals_sign} {case_sensitivity_mark}(?)")
                        # this is used to pass the arguments to the command execute
                        argument_list.append(item)
                else:
                    criteria_list.append(f"{case_sensitivity_mark}(`{key}`) {equals_sign} {case_sensitivity_mark}(?)")
                    # this is used to pass the arguments to the command execute
                    argument_list.append(term)       

            except Exception as e:
                print(e)


        # now we stitch together the individual criteria using the search_condition (and/or)
        select_condition = select_condition.upper() # <-- this is mostly for formatting since SQL should be upper case


        # to store our final output
        criteria_string = ""
        for i in range(len(criteria_list)):

            # if not the final criteria, a the search condition "and" or "or" will be appended
            if i != len(criteria_list) - 1:
                criteria_string += f"{criteria_list[i]} {select_condition} "
            

            # if it is teh final criteria, no search condition will be appended
            else:
                criteria_string += f"{criteria_list[i]} "
            

        return criteria_string, argument_list
    except Exception as e:
        print(e)

# generates a string containing the select criteria of an SQL select statement
def generate_TIME_criteria(time_span_dictionary, filter_condition_symbol):
    try:
        # what we will store unformatted criteria in
        criteria_list = []
        # argument list is used to pass the arguments to the command execute
        argument_list = []

        #we use this to determine what date restriction we want including
        key_list = []
        for key, term in time_span_dictionary.items():
            key_list.append(key)

        # this code is responsible for designating the minimum and maximum time allowences.
        # it accounts for if there is only one of the conditions for date and time respectively, and if there are both
        # if there is ony one condition we use a standard <= or >=, however if both are present we must use BETWEEN 
        try:
            date_min_and_max = ("date_min" in key_list) and ("date_max" in key_list)
            time_min_and_max = ("time_min" in key_list) and ("time_max" in key_list)

            if date_min_and_max: 
                criteria_list.append(f"{filter_condition_symbol} (`date`) BETWEEN ? and ?")
                argument_list.append(time_span_dictionary["date_min"])
                argument_list.append(time_span_dictionary["date_max"])

            if time_min_and_max: 
                criteria_list.append(f"{filter_condition_symbol} (`time`) BETWEEN ? and ?")
                argument_list.append(time_span_dictionary["time_min"])
                argument_list.append(time_span_dictionary["time_max"])

            if not (date_min_and_max or time_min_and_max):
                if "date_min" in key_list:
                    criteria_list.append(f"{filter_condition_symbol} (`date`) >= (?)")
                    argument_list.append(time_span_dictionary["date_min"])

                if "date_max" in key_list:
                    criteria_list.append(f"{filter_condition_symbol} (`date`) <= (?)")
                    argument_list.append(time_span_dictionary["date_max"])

                if "time_min" in key_list:
                    criteria_list.append(f"{filter_condition_symbol} (`time`) >= (?)")
                    argument_list.append(time_span_dictionary["time_min"])

                if "time_max" in key_list:
                    criteria_list.append(f"{filter_condition_symbol} (`time`) <= (?)")
                    argument_list.append(time_span_dictionary["time_max"])   

        except Exception as e:
            print(e)
 
        # to store our final output
        criteria_string = ""
        for i in range(len(criteria_list)):

            # if not the final criteria, a the search condition "and" or "or" will be appended
            if i != len(criteria_list) - 1:
                criteria_string += f"{criteria_list[i]} AND"
            

            # if it is the final criteria, no search condition will be appended
            else:
                criteria_string += f"{criteria_list[i]} "
            

        return criteria_string, argument_list
    except Exception as e:
        print(e)



# ========================================================================================================
#                                               SEARCH
# ========================================================================================================
# search the data set for time range and location, adding species too
def search(search_term_dictionary, search_condition, case_sensitivity):
    connection, cursor = tt_connect_to_database()

    try:

        # creating the prerequisites to any case sensitivity enforcement
        case_sensitivity_mark = case_sensitivity_check(case_sensitivity)

        # generates a string which will indicate our criteria in the system
        select_criteria, argument_list = generate_SELECT_criteria(search_term_dictionary, search_condition, case_sensitivity_mark, "=")

        command = f"SELECT * FROM `sightings` WHERE {select_criteria};"

        results = dbm.command_database(cursor, command, argument_list)

        return results

    except Exception as e:
        # a more accurate error message will be given by the flask_server
        return "error"



# ========================================================================================================
#                                               FILTER
# ========================================================================================================
# filter out or filter in specific ranges of data, eg locations, times, etc
def filter(filter_term_dictionary, filter_condition, case_sensitivity, time_span_dictionary):
    connection, cursor = tt_connect_to_database()
    try:

        # creating the prerequisites to any case sensitivity enforcement
        case_sensitivity_mark = case_sensitivity_check(case_sensitivity)

        if filter_condition == "include":
            equals_sign = "="
            filter_condition_symbol = "NOT"
        elif filter_condition == "exclude":
            equals_sign = "!="
            filter_condition_symbol = ""

        # generates a string which will indicate our criteria in the system

        # Note : validation in the flask server makes it (probably) impossible to have both of these conditions be empty

        # if empty, it is ignored by the system
        if filter_term_dictionary != {}:                                                      # AND becuase it ensures all filter rules are applied
            select_criteria, argument_list = generate_SELECT_criteria(filter_term_dictionary, "AND", case_sensitivity_mark, equals_sign)
        else:
            select_criteria = ""
            argument_list = []

        # if empty it is ignored by the system
        if time_span_dictionary != {}:
            time_criteria, time_argument_list = generate_TIME_criteria(time_span_dictionary, filter_condition_symbol)
        else:
            time_criteria = ""
            time_argument_list = []

        # so that all of the arguments are included
        argument_list.extend(time_argument_list)

        if filter_term_dictionary == {}:
            command = f"SELECT * FROM `sightings` WHERE {time_criteria};"
        elif time_span_dictionary == {}:
            command = f"SELECT * FROM `sightings` WHERE {select_criteria};"
        else:
            command = f"SELECT * FROM `sightings` WHERE {select_criteria} AND {time_criteria};"

        results = dbm.command_database(cursor, command, argument_list)

        return results

    except Exception as e:
        # a more accurate error message will be given by the flask_server
        print(e)
        return "error"



# ========================================================================================================
#                                            AGGREGATION
# ========================================================================================================

# the returns a list of species
def species_per_location(location):
    connection, cursor = tt_connect_to_database()
    arguments = [location]

    # runs the following select statement, inserting the location
    command = "SELECT `species` FROM `sightings` WHERE `location` = (?)"
    species_list = dbm.command_database(cursor, command, arguments)

    # removing the duplicate values 
    species_list_unique = []
    for species in species_list:

        # we do species[0] because it the select statement returns a list with 1 item
        if species[0] not in species_list_unique:
            species_list_unique.append(species[0])

    return species_list_unique

# counts the sightings for a given location
def sightings_per_location(location):
    connection, cursor = tt_connect_to_database()
    arguments = [location]

    # runs the following select statement, inserting the location
    command = "SELECT `id` FROM `sightings` WHERE `location` = (?)"
    sightings = dbm.command_database(cursor, command, arguments)
    
    number_of_sightings = len(sightings)

    return number_of_sightings

# the same as sightings_per_location however selecting for species instead of location
def sightings_per_species(species):
    connection, cursor = tt_connect_to_database()
    arguments = [species]

    # runs the following select statement, inserting the species
    command = "SELECT `id` FROM `sightings` WHERE `species` = (?)"
    sightings = dbm.command_database(cursor, command, arguments)
    
    number_of_sightings = len(sightings) 

    return number_of_sightings




# calculates the metric over time, returns an array of sightings
def species_over_time(time):
    connection, cursor = tt_connect_to_database()

def sightings_over_time(time):
    connection, cursor = tt_connect_to_database()

def location_over_time(time):
    connection, cursor = tt_connect_to_database()



# calculates the metric per category over time
def metric_per_category_over_time(metric, category, time):
    connection, cursor = tt_connect_to_database()





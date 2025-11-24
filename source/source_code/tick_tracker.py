import database_manager as dbm
import datetime
from datetime import timedelta
import pandas

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

# getting the time_period information we need to generate queries
def get_time_period_information(time_period):

    # this gets the variables that we will insert into the SQL query in order to receive the proper dates.
    # they use strftime formatting to get what we want, so either full days, a month/week paired with its year, or just the year
    # additionally it returns a date range symbol that will be used by pandas when creating the date range table so that it knows what increment to use (day, week, month, year, etc)

    if time_period == "day":
        to_select = "`date`"
        group_by = "`date`"
        order_by = "`date`"
        date_range_symbol = "D"

    elif time_period == "week":
        to_select = "strftime('%Y-%W', `date`) AS week"
        group_by = "week"
        order_by = "week"
        date_range_symbol = "W"
    
    elif time_period == "month":
        to_select = "strftime('%Y-%m', `date`) AS month"
        group_by = "month"
        order_by = "month"
        date_range_symbol = "MS"

    elif time_period == "year":
        to_select = "strftime('%Y', `date`) AS year"
        group_by = "year"
        order_by = "year"
        date_range_symbol = "YS"

    return to_select, group_by, order_by, date_range_symbol

# calculates every date possible from the first recorded entry, to the current day, and does so in set time intervals
# then, when the results list does not contain a date that has been listed, it is inserted into the list followed by a 0 to denote that no sightings appeared within that date
# essentialls fills in the blanks so that graphs can be drawn smoothly
def fill_dates(date_range_list, results_list):
    results_list_with_missing_dates = []

    #
    #   !!!!! -- THE FOLLOWING CODE IS NOT EFFICIENT, THIS WILL HAVE TO BE IMPROVED -- !!!!!
    #

    print(date_range_list)
    print(results_list)

    #for every date we know to exist
    for date in date_range_list:
        
        date_included = False

        for result in results_list:

            # the date has been found and therfore can be appended into the new list
            if result[0] == date:
                date_included = True
                results_list_with_missing_dates.append((date, result[1]))

                #exiting the loop to avoid time wasting
                break
        
        # we append the missing date followed by "0" for 0 sightings
        if not date_included:
            results_list_with_missing_dates.append((date, 0))
        
    return results_list_with_missing_dates

# function that takes the query results, and ensures that all dates are represented, even if they have no sightings
# this is mostly the header code that deals in generating a set of dates that should be represented
def fill_missing_dates(cursor, results_list, date_range_symbol):
    # one issue is that we don't have every date in the returned array, but we may need it, so we have to insert the missing dates
    # first the first/earliest date is taken from the database, and assigned to a datetime object - the datetime module allows us to manipulate dates more easily

    #
    #   !!!!! -- THE FOLLOWING CODE IS NOT EFFICIENT, THIS WILL HAVE TO BE IMPROVED -- !!!!!
    #

    first_date_query_result= dbm.command_database(cursor, "SELECT MIN(`date`) FROM `sightings`;")
    # because technically these dates are strings, they need to be split into 3 and assigned that way
    year, month, day = first_date_query_result[0][0].split("-")

    if date_range_symbol == "D":
        # getting the actual dates
        # here we remove 1 from the day because pandas views this as a minimum bound, if do the actual lowest day/month/year it will skip it.
        first_date = datetime.date(int(year), int(month), int(day)-1)
        latest_date = datetime.date.today()

        # we then use pandas to get a date range, giving us all of the dates in that span 
        date_range = pandas.date_range(first_date, latest_date, freq = date_range_symbol)

        #converts the date range into a usable list of dates
        date_range_list = date_range.strftime("%Y-%m-%d").tolist()

    elif date_range_symbol == "W":
        # getting the actual dates
        first_date = datetime.date(int(year), int(month), int(day))
        latest_date = datetime.date.today()

        latest_date = datetime.date.today()

        # we then use pandas to get a date range, giving us all of the dates in that span 
        date_range = pandas.date_range(first_date, latest_date, freq = date_range_symbol)

        #converts the date range into a usable list of dates
        date_range_list = date_range.strftime("%Y-%W").tolist()

    elif date_range_symbol == "MS":
        # getting the actual dates
        # here we remove 1 from the month because pandas views this as a minimum bound, if do the actual lowest day/month/year it will skip it.
        # this logic prevents invalid dates, if the month is not 1, we go to the prior month
        if int(month) != 1:
            first_date = datetime.date(int(year), int(month)-1, int(day))

        # if the month is 1, since there is no month 0, we go back one year, and up 11 months, to get to the 12th month of the previous year, aka, the previous month
        else:
            first_date = datetime.date(int(year)-1, int(month)+11, int(day))

        latest_date = datetime.date.today()

        # we then use pandas to get a date range, giving us all of the dates in that span 
        date_range = pandas.date_range(first_date, latest_date, freq = date_range_symbol)

        #converts the date range into a usable list of dates
        date_range_list = date_range.strftime("%Y-%m").tolist()

    elif date_range_symbol == "YS":
        # getting the actual dates
        # here we remove 1 from the year because pandas views this as a minimum bound, if do the actual lowest day/month/year it will skip it.
        first_date = datetime.date(int(year)-1, int(month), int(day))
        latest_date = datetime.date.today()

        # we then use pandas to get a date range, giving us all of the dates in that span 
        date_range = pandas.date_range(first_date, latest_date, freq = date_range_symbol)

        #converts the date range into a usable list of dates
        date_range_list = date_range.strftime("%Y").tolist()


    results_list_with_missing_dates = fill_dates(date_range_list, results_list)

    
    return results_list_with_missing_dates

# time_period is a string, either "day", "week", "month", "year"
# metric_sql is the SQL statement comparing the metric (species, sightings, location) to the comparative
# the comparative is what we are looking for (species name, location name, None for sightings)
# the fill_missing is either "true" or "false" depending on if the missing dates should be filled in
def metric_over_time(time_period, metric_sql, comparative, fill_missing):
    connection, cursor = tt_connect_to_database()

    to_select, group_by, order_by, date_range_symbol = get_time_period_information(time_period)

    # generating and executing the command
    command = f"SELECT {to_select}, COUNT(*) FROM `sightings` {metric_sql} GROUP BY {group_by} ORDER BY {order_by};"

    # this section handles the sightings over time call, which has nothing to compare to and thus passes no arguments
    if comparative != None:
        arguments = [comparative]
        results = dbm.command_database(cursor, command, arguments)
    else:
        results = dbm.command_database(cursor, command)

    #filling in the missing dates with 0 if selected
    if fill_missing == "fill":
        results = fill_missing_dates(cursor, results, date_range_symbol)

    # converting it into an array of dictionaries for easier use by the frontend
    results_array_of_dictionaries = []
    for result in results:
        results_array_of_dictionaries.append({"date" : result[0], "number_of_sightings" : result[1]})

    return results_array_of_dictionaries   

# calculates how many of a sightings there have been of a given species, in given time intervals
def species_over_time(time_period, species, fill_missing):
    metric_sql = "WHERE `species` = (?)"
    results_array_of_dictionaries = metric_over_time(time_period, metric_sql, species, fill_missing)

    return results_array_of_dictionaries  

# calculates how many sightings there have been in set time intervals
def sightings_over_time(time_period, fill_missing):
    metric_sql = ""
    results_array_of_dictionaries = metric_over_time(time_period, metric_sql, None, fill_missing)

    return results_array_of_dictionaries  

# calculates how many of a sightings there have been in a given location, in given time intervals
def location_over_time(time_period, location, fill_missing):
    metric_sql = "WHERE `location` = (?)"
    results_array_of_dictionaries = metric_over_time(time_period, metric_sql, location, fill_missing)

    return results_array_of_dictionaries  

# retreives all of the unique values for a given column
def get_all_unique(subject):
    connection, cursor = tt_connect_to_database()

    column_name = ""

    #getting the correct column name since column names cannot be parameterised
    if subject == "id":
        column_name = "`id`"

    elif subject == "date":
        column_name = "`date`"

    elif subject == "time":
        column_name = "`time`"

    elif subject == "location":
        column_name = "`location`"

    elif subject == "species":
        column_name = "`species`"

    elif subject == "latin_name":
        column_name = "`latin_name`"

    command = f"SELECT DISTINCT {column_name} FROM `sightings`;"
    results = dbm.command_database(cursor, command)

    # formats the returned list properly since it returns an array of single item arrays
    results_formatted = []
    for r in results:
        results_formatted.append(r[0])
    return results_formatted





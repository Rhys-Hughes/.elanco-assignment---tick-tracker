import database_manager as dbm, sighting as s

# the manager code that will start the various functions

def tt_connect_to_database():
    connection, cursor = dbm.connect_to_database()
    return connection, cursor



# search the data set for time range and location, adding species too
def search():
    connection, cursor = tt_connect_to_database()



# filter out or filter in specific ranges of data, eg locations, times, etc
def filter():
    connection, cursor = tt_connect_to_database()



# debugging
def connection_test(test_var):
    connection, cursor = tt_connect_to_database()
    results = dbm.command_database(cursor, "SELECT * FROM `sightings`")
    print(results)
    return {
        "database_contents" : results,
        "test_variable" : test_var
    }











# aggregate functions need refining

# general data that can be retreived
def aggregate_per():
    connection, cursor = tt_connect_to_database()
    # sightings per region

    # sightings per species

    # species per region



# data over time is returned
def aggregate_time_trends():
    connection, cursor = tt_connect_to_database()
    # trends over time, monthly/weekly
        # find first instance and move along timeline by increment, tracking each metric

        # sightings per region

        # sightings per species

        # species per region



# counts the basic information desired
def aggregate_count():
    connection, cursor = tt_connect_to_database()
    # all regions observed

    # all species observed

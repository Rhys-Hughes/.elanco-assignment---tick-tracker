import sqlite3

DATABASE_PATH = "source/database/tick_sightings.db"
SOURCE_DATA_PATH = "source/source_data/Tick Sightings.xlsx"


# handles connecting to the database
def connect_create_database():
    connection = sqlite3.connect(DATABASE_PATH)
    return connection



# creates a cursor for the database
def create_cursor(connection):
    cursor = connection.cursor()
    return cursor



# to insert the data contained within the excel spreadsheet
def populate_database(cursor):
    #read the excel file

    #insert into database

    pass



# function that commits changes made to the database, here it is a separate function because 
# at a later stage we may wish to commit at set intervals
def commit_database(connection):
    connection.commit()



# generic query function
def command_database(cursor, command):
    try:
        cursor.execute(command)
        return cursor.fetchall()
    except:
        return "oops"



# to initially create the sql database we will be working on
def create_database():
    connection = connect_create_database()
    cursor = create_cursor(connection)
    command_database(cursor, 
                     """
                     CREATE TABLE IF NOT EXISTS`sightings` (
                        `id` VARCHAR(20) UNIQUE NOT NULL, 
                        `date DATE` NOT NULL, 
                        `time TIME` NOT NULL,
                        `location` VARCHAR(20) NOT NULL,
                        `species` VARCHAR(30) NOT NULL, 
                        `latin_name` VARCHAR(30) NOT NULL,
                        PRIMARY KEY(id)
                     )
                     """)
    
    populate_database(cursor)



# to connect to the ticks database
def connect_to_database():
    connection = connect_create_database()
    cursor = create_cursor(connection)
    return connection, cursor



# returns the entire database as sighting objects
def get_database_as_sighting_objects(cursor):
    results = command_database(cursor, "SELECT * FROM `sightings`")
    print(results)



#create_database()
#connection, cursor = connect_to_database()
#command_database(cursor, """
#                 INSERT INTO `sightings` VALUES 
#                    ('02WNholuSg6ndCk4c1dA', '2022.08.01', '06:40:31', 'Manchester', 'Marsh Tick', 'Ixodes apronophorus'),
#                    ('02rFwLCaAwZSVxdTDicK', '2014.09.12', '23:33:03', 'London', 'Southern Rodent Tick', 'Ixodes acuminatus')
#                 """)

#commit_database(connection)
#results = command_database(cursor, "SELECT * FROM `sightings`")
#print(results)

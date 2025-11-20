import sqlite3, pandas, openpyxl

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



# converts the date and time stored in the excel file into 2 separate dates and times, in a format the database will accept
def convert_date_time(date_time):
    date, time = date_time.split("T")

    date = date.replace("-", ".")
    time = time.replace(":", ".")

    return date, time



# to insert the data contained within the excel spreadsheet
def populate_database(cursor):
    #read the excel file and convert it to a dictionary
    raw_data = pandas.read_excel(SOURCE_DATA_PATH).to_dict(orient="records")

    #insert into database
    for sighting in raw_data:
        
        #converting the date and time into the desired format
        # split the data and time into 2 variables
        date, time = convert_date_time(sighting["date"])

        #generating the insert commands
        command = f"""
                INSERT INTO `sightings` 
                    (`id`, `date`, `time`, `location`, `species`, `latin_name`) 
                    VALUES (
                        "{sighting["id"]}", 
                        "{date}",
                        "{time}",
                        "{sighting["location"]}",
                        "{sighting["species"]}",
                        "{sighting["latinName"]}"                    
                    );   
                """

        # sending the insert command to the database to populate it
        command_database(cursor, command)



# function that commits changes made to the database, here it is a separate function because 
# at a later stage we may wish to commit at set intervals
def commit_database(connection):
    connection.commit()



# generic query function
def command_database(cursor, command, arguments = None):
    try:
        #inserts data into the arguments placeholders
        if arguments != None:
            cursor.execute(command, arguments)
        else:
            cursor.execute(command)

        return cursor.fetchall()           
    except:
        return "!!! - COMMAND FAILED - !!!"



# to initially create the sql database we will be working on
def create_database():
    connection = connect_create_database()
    cursor = create_cursor(connection)
    command_database(cursor, 
                     """
                     CREATE TABLE IF NOT EXISTS`sightings` (
                        `id` VARCHAR(20) UNIQUE NOT NULL, 
                        `date` DATE NOT NULL, 
                        `time` TIME NOT NULL,
                        `location` VARCHAR(20) NOT NULL,
                        `species` VARCHAR(30) NOT NULL, 
                        `latin_name` VARCHAR(30) NOT NULL,
                        PRIMARY KEY(id)
                     );
                     """)
    
    populate_database(cursor)
    commit_database(connection)



# to connect to the ticks database
def connect_to_database():
    connection = connect_create_database()
    cursor = create_cursor(connection)
    return connection, cursor



# returns the entire database as sighting objects
def get_database_as_sighting_objects(cursor):
    results = command_database(cursor, "SELECT * FROM `sightings`;")
    print(results)




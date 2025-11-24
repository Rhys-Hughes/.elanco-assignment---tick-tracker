The Elanco Tick Tracker
-----------------------

Given to me by Elanco as part of their industrial placement recruitment process.
The premise was to create a backend system capable of interfacing with, and managing the data they provided. Said data regarded tick sightings across the UK, including the species, the location, the date, etc.

What I have produced is a web capable API able to interface with the data provided, and return information to the user.

I wanted to keep the following in mind: 
  - scalability (the API should be able to handle large amounts of data, and have many expansions added to it)
  - portability (the API should work on as many devices, and with as many languages as possible)
  - usability   (the API should not be daunting to use, data collection should be clear, descriptive, and human readable)

Initially I identified 3 main problems to solve:

Q1- what will this be built in?
Q2- how will I handle the data?
Q3- how will I interface with the frontend?

I solved these problems as follows:

A1- Python was the obvious choice for me, Given that I am experienced with it already, I knew I would be able to create something functional at the very least.
A2- Considering scalability and portability, some SQL system was the obvious choice, with commands that can be used interchangeably, relatively easy migration to a web database when the time comes, and efficieny when handling such large data sets. Specifically I landed on SQLite, while not a "full" online database system, for an MVP it is suitable, and migration to a larger system would be fairly easy.
A3- Considering usability and portability, an HTTP interface was the desired choice, for this i used Flask, which functionally creates a miniature web server, capable of listening for HTTP POST requests. Json was the chosen format to recieve and send data, due to it's near universal portability.

I had to learn how to use Flask, as well as SQLite (although I had recently learned some SQL in university), as this was my first API project. 

Structure
---------

The overall structure of the system is simple, consisting of 4 components.

flask_server : handles accepting, validating, and, returning requests, designed to decouple the interface from the business logic
tick_tracker : handles the business logic, generating parameterised SQL commands, and working with the returned data to fulfil commands
database_manager : handles the connections to the database as well as executing the actual queries
database : the actual database that contains the data

So the workflow of a request goes as follows:
[client] -> sends HTTP POST request to server -> 
[flask_server : validates request] -> sends required data to tick_tracker -> 
[tick_tracker : connects to database, and retrieves needed data] -> sends command_database() call to database_manager ->
[database_manager : executes the command] -> command is executed on the database ->
[database : returns data] -> data sent to database_manager ->
[database_manager : sends the recieved data back] -> data sent to tick_tracker ->
[tick_tracker : carries out the business logic and generates a result] -> result sent to the flask_server ->
[flask_server : inserts the results into the return Json with the success mark] -> sends the data back to the client ->
[client : recieves data] -> yay :)










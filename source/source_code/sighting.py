class sighting:

    def __init__(self, id, date, time, location, species, latin_name):
        self.id = id
        self.date = date
        self.time = time
        self.location = location
        self.species = species
        self.latin_name = latin_name
    
    def get_id(self):
        return self.id

    def get_date(self):
        return self.date

    def get_time(self):
        return self.time

    def get_location(self):
        return self.location

    def get_species(self):
        return self.species

    def get_latin_name(self):
        return self.latin_name

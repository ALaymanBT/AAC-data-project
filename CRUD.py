from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
from bson.json_util import dumps

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    
    def __init__(self, usr, pwd):
        # Initializing the MongoClient. This will connect to AAC database. 
        

        
        #connect to database using supplied username and password
        self.client = MongoClient('mongodb://%s:%s@localhost:55245' % (usr, pwd))
        self.database = self.client['AAC']
        self.collection = "animals"
        
        
    # Method to insert data to database
    def create(self, data):
        try:
            self.database[self.collection].insert(data)  # data should be dictionary
            return True            
        except Exception as e:
            print(e)    
            return False
        
    # Method to read data from database, returns cursor object
    def read(self, query, show_id={ "_id" : 1 }):
        try:
            data = self.database[self.collection].find(query, show_id)
            return data
        
        except Exception as e:
            return e
        
    def read_one(self, query, show_id={ "_id" : 1 }):
        try:
            data = self.database[self.collection].find_one(query, show_id)
            return data
        
        except Exception as e:
            return e
          
    # Method for updating documents in database
    def update(self, search_values, values_to_replace):
        try:
            # Variable to hold list of updated documents
            doc_list = []       
            
            # Store the number of documents found by a query.
            num_of_docs = self.read(search_values).count()
            
            # Update each document found by the query, and append the updated document to a list
            for x in range(num_of_docs):
                current_doc = self.database[self.collection].find_one_and_update(search_values, values_to_replace, return_document = ReturnDocument.AFTER)
                doc_list.append(current_doc)
                
            # Convert to JSON and return
            updated_data = dumps(doc_list)
            print("Updated a total of %d documents" % num_of_docs)
            return updated_data
        
        except Exception as e:
            return e

    # Method for deleting documents in a database
    def delete(self, query):
        try:
            cursor = self.read(query)
            deleted_docs = []
            num_of_docs = cursor.count()
            # Get Object ids from cursor and append object to deleted docs list to display once deleted
            for x in cursor:
                deleted_docs.append(x)
                self.database[self.collection].delete_one({"_id" : ObjectId(x.get("_id"))})
            
            print("Deleted a total of %d documents" % num_of_docs)
            
            # Convert to JSON and return
            return dumps(deleted_docs)
                
        except Exception as e:
            return e
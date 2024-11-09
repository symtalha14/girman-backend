from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from json import dumps, load
import os
import pymongo

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
    

# Mongo client
client = pymongo.MongoClient("mongodb+srv://smt:abc1234@cluster0.j2w5ysn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["testdb"]
collection = db["users"]
# Mongo client ends
    
    
'''
    searchUser: GET method
    accepts a search query and returns matching data
    returns an empty array in case of no match
    
'''

def searchUser(request):
    
    if request.method == "GET":
        
        query = request.GET.get("query", None)
        
        if query is None:
            return JsonResponse({"status":500, "message":"Query parameter not found"}) 
       
        query = query.lower()
        response = []
        toReturn = collection.find(
            {
            "$or":[
                {"first_name":{"$regex":query, "$options":"i"}},
                {"last_name":{"$regex":query, "$options":"i"} },
                {"city":{"$regex":query, "$options":"i"} },
                {"contact_number":{"$regex":query, "$options":"i"} },
            ]
            }
        )
        for r in toReturn:
            del r["_id"]
            response.append(r)
            
        return JsonResponse({"data":response})


    return JsonResponse({"status":405, "message":"Method not allowed"})


'''

    saveRecordsToMongo: GET Method
    Saves all the json data to mongo db and returns the count of documents.
    
    To be used internally!

'''

def saveRecordsToMongo(request):
    
    data = []
    
    with open(os.path.join(BASE_DIR, "data", "user_list.json")) as f:
        data = load(f)
        f.close()
            
    if len(data):
        
        collection.insert_many(data)
        count = collection.count_documents({})
        
        return HttpResponse(str(count)+" documents saved")
    
    return HttpResponse("No documents found")
    
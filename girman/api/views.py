from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from json import dumps, load
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
    
    
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
        print(query)
        with open(os.path.join(BASE_DIR, "data/fts.txt"), "r") as f:
            
            for index, line in enumerate(f):
                print(line)
                
                if query in line:
                    print("True")
                    line = line.rstrip("\n").split(":")
                    rec = {
                        "name":line[0].capitalize(),
                        "city":line[1].capitalize(),
                        "contact":line[2]
                    }
                    if len(query) == 1:
                        if (line[0][0] == query):
                            response.insert(0, rec)
                            continue
                        
                    response.append(rec)
                    
              
                
        return JsonResponse({"data":response})


    return JsonResponse({"status":405, "message":"Method not allowed"})


def createFTS(request):
    
    print("Creating FTS")
    data = []
    
    with open(os.path.join(BASE_DIR, "data", "user_list.json")) as f:
        data = load(f)
        f.close()
    
    with open(os.path.join(BASE_DIR, "data", "fts.txt"), "w") as f:
        
        for record in data:
            f.write(record["first_name"].lower()+" "+record["last_name"].lower()+":"+record["city"].lower()+":"+record["contact_number"]+"\n")
        f.close()
                        
    
    return HttpResponse("OK")




from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateNewUser


# Create your views here.

from .utils import get_db_handle, get_collection_handle,getNextSequence


db_handle, mongo_client = get_db_handle("registration", "localhost",27017, "QuintonPang","quinton")

#print(mongo_client.list_database_names())


counters, collection_handle = get_collection_handle(db_handle, "user")



#collection_handle.insert_one({"_id":getNextSequence("userid",counters),"username":"Lee"})



def home(response):

    return HttpResponse("<h1>Success</h1>")


def create(response):

    if response.method=="POST":

        form = CreateNewUser(response.POST)

        if form.is_valid():

         
            d=dict({"_id":getNextSequence("userid",counters)})

            d.update(form.cleaned_data)

            collection_handle.insert_one(d)
        
            #insert many at once

            #collection_handle.insert_many(...)

        return redirect("/create")
    
    else:
        
        form = CreateNewUser()

    return render(response,"main/create.html",{"form":form})


def searchAll(response):

    ls = collection_handle.find()

    return render(response,"main/searchAll.html",{"ls":ls})

def searchOne(response,username):

    ls = collection_handle.find({"username":username})

    return render(response,"main/searchOne.html",{"ls":ls})


def searchOneLetter(response,username):

    ls = collection_handle.find({"username":{"$regex":"^"+username}})

    return render(response,"main/searchOne.html",{"ls":ls})

def searchEngine(response):

    if response.method=="POST":

        username = response.POST.get("username")

        if len(username)==1:

             return redirect("/searchOneLetter/"+username)

        else:

             return redirect("/searchOne/"+username)

        

    else:
        return render(response,"main/searchEngine.html",{})



def updateEngine(response): 



    if response.method=="POST":

        username = response.POST.get("username")

        return redirect("/update/"+username)

    else:
                                                                                                                                            return render(response,"main/updateEngine.html",{})


def update(response,username):

    



    ls=collection_handle.find({"username":username})
    #print(ls.get("username")

    if response.method == "POST":

        newUsername=response.POST.get("username")      
        age  = response.POST.get("age")
        gender = response.POST.get("gender")
        email = response.POST.get("email")
        

        #print(data)

        collection_handle.update_one({"username":username},{"$set":{"username":newUsername,"age":age,"gender":gender,"email":email}})

        return redirect("/update/"+newUsername)
    
    else:

        return render(response,"main/update.html",{"ls":ls})


def deleteOne(response,username):

    collection_handle.delete_one({"username":username})

    HttpResponse("<script>alert ('User %s deleted');</script>"%(username)) 

    return redirect("/deleteEngine")

def deleteAll(response):

    deleted = collection_handle.delete_many({})

    message =str(deleted.deleted_count)+" users deleted"

    return render(response,"main/deleteAll.html",{"message":message})

def deleteEngine(response):


    if response.method == "POST":

        #print(response.POST.get("username"))
        user = collection_handle.find({"username":response.POST.get("username")})


        userls=list(user)


        if userls:


            return redirect("/deleteOne/"+response.POST.get("username"))

        else:

            
            return  render(response, "main/deleteEngineError.html",{})# HttpResponse("<script>alert('User Not Found')</script>")                                                                                                                    


    else:

        return render(response,"main/deleteEngine.html",{})


def home(response):

    return render(response,"main/home.html",{})

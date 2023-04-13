
from flask import Flask, Response, request, jsonify
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient("mongodb+srv://ecomerceWeb:a%4089824249@cluster0.jtmfd0k.mongodb.net/?retryWrites=true&w=majority")
    db= mongo.company
    # mongo.server_info()    #trigger exception if cannot connect to db
except:
    print("Error - Cannot connect to db")

############### Get Methods
@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
           response=json.dumps(data),
           status=500,
           mimetype="application/json"
        )


    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot read users"}),status=500, mimetype="application/json")



######### Post mathod
@app.route("/users", methods=["POST"])
def create_user():
    try:
         
        user = {"name": request.form["name"], "lastName": request.form["lastName"],
                 "email": request.form["email"], "password": request.form["password"]}
        dbresponce = db.users.insert_one(user)
        # for attr in dir(dbresponce):
        #     print(attr)
        return Response(
            response=json.dumps({"message": "user created", "id": f"{dbresponce.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot read users"}),status=500, mimetype="application/json")


#### Update method

@app.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponce = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name": request.form["name"]}}
        )
        # for attr in dir(dbResponce):
        #     print(f"**********{attr}")
        if(dbResponce.matched_count == 1):
            return Response(response=json.dumps({"message": "user updated succefully!"}),
                            status=200,
                              mimetype="application/json")
        return Response(response=json.dumps({"message": "nothing to update!"}),
                            status=200,
                              mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot update user"}),status=500, mimetype="application/json")



########## Delete

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponce = db.users.delete_one({"_id": ObjectId(id)})
        # for attr in dir(dbResponce):
        #     print(f"**{attr}")
        return Response(response=json.dumps({"message": "user deletd succefully", id: f"{id}"}),status=500, mimetype="application/json")


    except Exception as ex:
        return Response(response=json.dumps({"message": "cannot deletd a user"}),status=500, mimetype="application/json")


########## Port Number
if __name__ == "__main__":
    app.run(port=3080, debug=True)
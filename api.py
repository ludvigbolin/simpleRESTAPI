from flask import Flask, request
from flask_api import status
app = Flask(__name__)

'''
Items in the database are stored with the email adress as the key and 
the email adress, first name and last name in a json object as a value
'''
database = {}


@app.route('/personnel', methods=['GET', 'DELETE', 'POST'])
def programming_languages_route():
    if request.method == 'GET':
        return list_all_personnel()
    elif request.method == 'DELETE':
        return delete_personnel()
    elif request.method == "POST":
        return create_new_personnel(request.get_json(force=True))
    else:
        return "test"


def list_all_personnel():
    return {"personnel": list(database.values())}


def delete_personnel():
    return


'''
create_new_personnel takes a json object and if correctly comfigured, adds that co-worker to the database

Status codes:
201, successful and returns the added entry in the database
400, invalid formatting of json object in data field
409, entry already exists and cannot be added again to database

Can be called using:
[POST] /personnel 
data: 
{
   "email": "example@mail.com"
   "first_name": "example"
   "last_name": "examplesson"
}

'''


def create_new_personnel(json_object_data):
    mail = ""
    first_name = ""
    last_name = ""
    try:
        mail = json_object_data['email']
        first_name = json_object_data['first_name']
        last_name = json_object_data['last_name']
    except:
        return "Invalid input data, wrong format", status.HTTP_400_BAD_REQUEST

    if database.get(mail) == None:
        database[mail] = {"email": mail,
                          "first_name": first_name, "last_name": last_name}
        return str(database[mail]), status.HTTP_201_CREATED
    return "Email adress already exists", status.HTTP_409_CONFLICT

from flask import Flask, request
from flask_api import status
app = Flask(__name__)

'''
Items in the database are stored with the email adress as the key and 
the email adress, first name and last name in a json object as a value
'''
database = {
    -1: {"id": -1, "email": "example@mail.com", "first_name": "example", "last_name": "examplesson"}
}

id_counter = 0
email_list = {}


@app.route('/personnel', methods=['GET', 'DELETE', 'POST'])
def programming_languages_route():
    if request.method == 'GET':
        return list_all_personnel()
    elif request.method == "POST":
        try:
            json_object = request.get_json(force=True)
        except:
            return "Invalid format of json object.", status.HTTP_400_BAD_REQUEST
        return create_new_personnel(json_object)
    else:
        return "No endpoint available with this path.", status.HTTP_400_BAD_REQUEST


'''
delete_personnel takes an id as parameter and deleted that entry from the database. The deleted entry is returned.

Status codes:
202, successful deletion and returns the deleted entry from the database.
    content: {
        "email": "example@mail.com",
        "first_name": "example",
        "id": 0,
        "last_name": "examplesson"
    }

400, invalid formatting of parameter, should be a integer but is not.

404, the id requested is not available in the database.

Can be called using:
[DELETE] /personnel/<input_id>
<input_id> must be a integer and an id available in the database.

'''


@app.delete('/personnel/<input_id>')
def delete_personnel(input_id):
    try:
        input_id_integer = int(input_id)
    except:
        return "Parameter is not a integer.", status.HTTP_400_BAD_REQUEST

    if database.get(input_id_integer) != None:
        entry = database.pop(input_id_integer)
        email_list.pop(entry["email"])

        return entry, status.HTTP_202_ACCEPTED
    return "Invalid entry, the id does not exist.", status.HTTP_404_NOT_FOUND


'''
list_all_personnel returns all entries in the database

Status codes:
200, successful and returns all entries in the database
    content: {
        "personnel": [{
            "email": "example@mail.com",
            "first_name": "example",
            "id": 0,
            "last_name": "examplesson"
        }, ...]
    }

Can be called using:
[GET] /personnel 
'''


def list_all_personnel():
    return {"personnel": list(database.values())}, status.HTTP_200_OK


'''
create_new_personnel takes a json object and if correctly comfigured, adds that co-worker to the database

Status codes:
201, successful and returns the added entry in the database
    content: {
        "email": "example@mail.com",
        "first_name": "example",
        "id": 0,
        "last_name": "examplesson"
    }

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
    global id_counter
    mail = ""
    first_name = ""
    last_name = ""
    try:
        mail = json_object_data['email']
        first_name = json_object_data['first_name']
        last_name = json_object_data['last_name']
    except:
        return "Invalid input data, wrong format.", status.HTTP_400_BAD_REQUEST

    if email_list.get(mail) == None:
        database[id_counter] = {"id": id_counter, "email": mail,
                                "first_name": first_name, "last_name": last_name}
        email_list[mail] = True
        id_counter += 1

        return database[id_counter-1], status.HTTP_201_CREATED
    return "Email adress already exists.", status.HTTP_409_CONFLICT


'''
Run the API request by running the following commands in terminal

export FLASK_APP=api.py
python3 -m flask run

Do the calls on the server provided by Flask
'''

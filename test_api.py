import json
import api


def test_create_new_personnel_invalid_data_format():
    api.database = {}
    api.email_list = {}
    api.id_counter = 0

    json_data = {}
    json_data["email"] = "test@test.se"
    json_data["first_name"] = "first_name"
    # wrong value, should be "last_name"
    json_data["not_last_name"] = "not_last_name"
    return_value = api.create_new_personnel(json_data)

    assert return_value[1] == 400


def test_create_new_personnel_existing_email():
    api.database = {}
    api.email_list = {}
    api.id_counter = 0

    # Adding mock data in database
    api.database = {
        -1: {"id": -1, "email": "example@mail.com", "first_name": "example", "last_name": "examplesson"}
    }
    api.email_list["example@mail.com"] = True

    json_data = {"email": "example@mail.com",
                 "first_name": "example2", "last_name": "examplesson2"}
    return_value = api.create_new_personnel(json_data)

    assert return_value[1] == 409


def test_create_new_personnel_successful_new_user():
    api.database = {}
    api.email_list = {}
    api.id_counter = 0

    json_data = {"email": "example@mail.com",
                 "first_name": "example2", "last_name": "examplesson2"}
    return_value = api.create_new_personnel(json_data)

    assert return_value[0]["id"] == 0 and return_value[1] == 201


def test_delete_new_personnel_user_not_found():
    api.database = {}
    api.email_list = {}
    api.id_counter = 0

    return_value = api.delete_personnel(10)
    assert return_value[1] == 404


def test_delete_new_personnel_user_invalid_format():
    api.database = {}
    api.email_list = {}
    api.id_counter = 0

    return_value = api.delete_personnel("not a integer")
    assert return_value[1] == 400


def test_delete_new_personnel_user_valid_deletion():
    api.database = {}
    api.email_list = {}
    api.id_counter = 0

    # Adding mock data to database
    api.database = {
        0: {"id": 0, "email": "example@mail.com", "first_name": "example", "last_name": "examplesson"}
    }

    api.email_list["example@mail.com"] = True
    api.id_counter = 1

    return_value = api.delete_personnel(0)
    assert return_value[0]["id"] == 0 and return_value[1] == 202


def test_list_all_personnel_empty_database():
    api.database = {}
    api.email_list = {}
    api.id_counter = 0

    return_value = api.list_all_personnel()
    assert len(return_value[0]["personnel"]) == 0 and return_value[1] == 200


def test_list_all_personnel_non_empty_database():
    api.database = {}
    api.email_list = {}
    api.id_counter = 0

    # Adding mock data to database
    api.database = {
        0: {"id": 0, "email": "example@mail.com", "first_name": "example", "last_name": "examplesson"},
        1: {"id": 1, "email": "example2@mail.com", "first_name": "example2", "last_name": "examplesson2"}
    }

    api.email_list = {
        "example@mail.com": True,
        "example2@mail.com": True
    }
    api.id_counter = 2

    return_value = api.list_all_personnel()
    assert len(return_value[0]["personnel"]) == 2 and return_value[1] == 200


test_create_new_personnel_invalid_data_format()
test_create_new_personnel_existing_email()
test_create_new_personnel_successful_new_user()

test_delete_new_personnel_user_not_found()
test_delete_new_personnel_user_invalid_format()
test_delete_new_personnel_user_valid_deletion()

test_list_all_personnel_empty_database()
test_list_all_personnel_non_empty_database()

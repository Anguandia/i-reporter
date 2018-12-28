import os
import pytest
import json
from tests.test_data import dat
from app import implementation, routes


@pytest.fixture(scope='function')
def client():
    red_flags = implementation.red_flags
    app = routes.app
    test_client = app.test_client()
    red_flags.clear()
    cxt = app.app_context()
    cxt.push()
    yield test_client
    cxt.pop()


# Encode test requests to json
def post_json(client, url, json_dict):
    return client.post(
        url, data=json.dumps(json_dict), content_type='application/json'
        )


# Decode json requests
def json_of_response(response):
    return json.loads(response.data.decode())


# Encoding for put request
def patch_json(client, url, json_dict):
    return client.patch(
            url, data=json.dumps(json_dict), content_type='application/json')


# Test red_flag creation and expected reponse; code and content
def test_red_flag_creation(client):
    response = post_json(client, 'api/v1/red_flags', dat['basic'])
    assert response.status_code == 201
    assert json_of_response(response)['data'][0]['message'] ==\
        'Created red flag'


# Test correct generation of flag id
def test_generate_unique_and_sequential_flag_ids(client):
    # create a 100 flags
    [post_json(client, 'api/v1/red_flags', dat['basic']) for i in range(100)]
    response = client.get('/api/v1/red_flags')
    # extract the flags list from the getall response
    message = json_of_response(response)['data']
    # generate a list of all flag ids
    ids = [flag['id'] for flag in message]
    # check that ids are unique
    assert len(set(ids)) == len(ids)
    # check that ids are sequential(auto-increamenting)
    assert ids == list(range(1, 101))


# Test optional fields set during creation if supplied
def test_optional_flag_properties_set_in_creation(client):
    post_json(client, '/api/v1/red_flags', dat['optional'])
    response = client.get('/api/v1/red_flags/1')
    assert json_of_response(response)['data'][0]['type'] == 'intervention flag'


# Test can retrieve all red_flags; correct response code and body
def test_get_flags(client):
    post_json(client, '/api/v1/red_flags', dat['basic'])
    post_json(client, '/api/v1/red_flags', dat['basic'])
    post_json(client, '/api/v1/red_flags', dat['basic'])
    post_json(client, '/api/v1/red_flags', dat['basic'])
    response = client.get('/api/v1/red_flags')
    assert len(json_of_response(response)['data']) == 4


# Test correct response to get all request if none; code and body
def test_get_all_fails_when_none(client):
    response = client.get('/api/v1/red_flags')
    assert response.status_code == 404
    assert json_of_response(response) == {
            'Status': 404, 'error': 'no red flags'
            }


# Test can fetch particular flag by id; correct response code and body
def test_get_single_flag_by_id(client):
    flag = post_json(client, '/api/v1/red_flags', {
            'location': 'there', 'createdBy': 10, 'comment': 'gavi money'
            })
    assert json_of_response(flag)['Status'] == 201
    resp = client.get('/api/v1/red_flags/1')
    assert json_of_response(resp)['data'][0]['comment'] == 'gavi money'


# Test correct response if particular flag non available
def test_get_single_flag_by_non_existent_id_fails(client):
    resp = client.get('/api/v1/red_flags/100')
    assert resp.status_code == 404
    assert 'error' in json_of_response(resp)
    assert json_of_response(resp)['error'] == 'red flag not found'


# Test can edit location and comment
def test_can_edit_comment(client):
    post_json(client, '/api/v1/red_flags', dat['basic'])
    response = patch_json(client, '/api/v1/red_flags/1/comment', {
            'comment': 'teacher\'s salaries eaten'})
    assert json_of_response(response)['data'][0]['message'] ==\
        "updated red-flag record's comment"


# Test edit rejected if flag resolved or rejected
def test_cant_edit_resolved_flag(client):
    post_json(client, '/api/v1/red_flags', dat['resolved'])
    response = patch_json(client, '/api/v1/red_flags/1/comment', {
            'comment': 'teacher\'s salaries eaten'})
    assert json_of_response(response)['error'] == 'red flag already resolved'


# Test geolocation added to flag
def test_add_goeloc(client):
    # create record without geolocation details
    post_json(client, '/api/v1/red_flags', dat['basic'])
    # add geolocation
    resp = patch_json(
            client, '/api/v1/red_flags/1/location',
            {'location': '03.2356 31.6524'}
            )
    # check that geoloc added
    assert json_of_response(resp)['data'][0]['message'] ==\
        "added red-flag record's location"
    # modify geoloc
    patch_json(client, '/api/v1/red_flags/1/location', {
            'location': '0.000 0.000'})
    resp1 = client.get('/api/v1/red_flags/1')
    # ascertain that geoloc updated to latest value
    assert 'N: 0.000, E: 0.000' in json_of_response(resp1)['data'][0][
            'location']

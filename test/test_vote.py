from typing import assert_type
from app import schemas
from app.config import settings
import jwt
import pytest
import app.db_tables as models

@pytest.fixture
def test_vote(session, test_user, test_post):
    new_vote = models.Votes(post_id = test_post[2].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client, test_post):
    res = authorized_client.post("/votes/", json={"post_id":test_post[0].id, "dir":1})
    assert res.status_code == 201

def test_unauthorized_vote(client, test_post):
    res = client.post("/votes/", json={"post_id":test_post[0].id, "dir":1})
    assert res.status_code == 401

def test_vote_no_post(authorized_client, test_post):
    res = authorized_client.post("/votes/", json={"post_id":888888, "dir":1})
    assert res.status_code == 404

def test_vote_twice_on_post(authorized_client, test_vote, test_post):
    res = authorized_client.post("/votes/", json={"post_id": test_post[2].id, "dir": 1})
    assert res.status_code == 409

def test_delete_one_vote(authorized_client, test_vote, test_post):
    res = authorized_client.post("/votes/", json={"post_id": test_post[2].id, "dir": 0})    
    assert res.status_code == 201

def test_delete_one_vote_from_no_post(authorized_client, test_post):
    res = authorized_client.post("/votes/", json={"post_id": test_post[2].id, "dir": 0})    
    assert res.status_code == 404
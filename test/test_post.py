import json
import pytest
from app import schemas

def test_all_posts(authorized_client, test_post):
    res = authorized_client.get("/posts/")
    print(res.json())
    assert res.status_code == 200
    # schemas.PostResponse.model_validate_json(response.json())
    def validate(post):
        return schemas.PostResponse(**post)
    posts = map(validate, res.json())
    posts = list(posts)
    assert isinstance(posts, list)

def test_unauthorized_user_get_all_posts(client, test_post):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts_not_exist(client, test_post):
    res = client.get("/posts/9999999")
    assert res.status_code == 401
 
def test_all_posts(authorized_client, test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}")
    post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert post.id == test_post[0].id

@pytest.mark.parametrize("title, content, published",[
("Hello", "Hello world", True),
("Common", "Bakery", False),
("Plants", "Nursery plants", True)
])
def test_create_post(authorized_client, test_post, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    # print(res.json())
    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published


def test_create_post_default_published_true(authorized_client, test_post):
    res = authorized_client.post("/posts/", json={"title": 'title', "content": 'content'})
    # print(res.json())
    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.published == True 


def test_unauthorized_create_post(client, test_user):
    res = client.post("/posts/", json={"title": 'title', "content": 'content'})
    assert res.status_code == 401

def test_unauthorized_delete_post(client, test_user, test_post):
    res = client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 401 
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database import get_db, Base
from app import oauth2, db_tables as models
from app.config import settings
from app.main import app

DATABASE_URL_TEST = f"{settings.DATABASE_TYPE}+psycopg://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

engine = create_engine(DATABASE_URL_TEST, echo=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

@pytest.fixture()
def session():
    """Create a new database session for a test."""
    models.Base.metadata.drop_all(bind=engine)  # Drop all tables before creating them
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:    
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {'email':'example@example.com', 'password':'password123'}
    res = client.post("/users/", json = user_data)
    user = res.json()
    user['password'] = user_data['password']
    assert res.status_code == 201
    return user

@pytest.fixture
def token(test_user):
    return oauth2.create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers, 
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_post(test_user, session):
    post_data = [
        {'title':'1 title',
         'content': '1 content',
         'owner_id': test_user['id']},

         {'title':'2 title',
         'content': '2 content',
         'owner_id': test_user['id']},

         {'title':'3 title',
         'content': '3 content',
         'owner_id': test_user['id']}
    ]

    def create_model_post(post):
        return models.Post(**post)
    

    post_data = map(create_model_post, post_data)

    post_data = list(post_data)

    session.add_all(post_data)
    session.commit()
    post_data = session.query(models.Post).all()
    return post_data

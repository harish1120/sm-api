from app import schemas
from app.config import settings
import jwt
import pytest


def test_login_user(client, test_user):
    res = client.post("/login", data={'username': test_user['email'], 'password': test_user['password']}) 
    login_check = schemas.Token(**res.json())
    payload = jwt.decode(login_check.token, settings.SECURITY_KEY, settings.ALGORITHM)
    assert payload.get('user_id') == test_user['id']
    assert login_check.token_type == 'bearer'
    assert res.status_code == 200


def test_incorrect_login_password(client, test_user):
   res = client.post("/login", data={'username': test_user['email'], 'password': 'wrongPass'}) 
   assert res.status_code == 401
   assert res.json().get('detail') == 'Invalid Credentials'

@pytest.mark.parametrize("email, password, status_code",[
                        ("wrongemail@gmail.com", "password123", 401),
                        ("example@example.com","wrongpass",401),
                        ("example@example.com","wrongpass",401),
                        (None,"wrongpass",401),
                        ('example@example.com',None,401)
])
def test_incorrect_login_email(client, email, password, status_code):
   res = client.post("/login", data={'username': email, 'password': password}) 
   assert res.status_code == status_code
#    assert res.json().get('detail') == 'Invalid Credentials' 
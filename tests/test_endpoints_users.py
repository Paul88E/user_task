from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


def test_registration():
    new_user = {"username": "Alex5", "password": "alex2pwdx"}
    response = client.post("/users/registration/",
                           json=new_user)
    assert response.status_code == 406


if __name__ == "__main__":
    pytest.main()

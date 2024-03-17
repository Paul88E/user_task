from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


def test_tasks_create():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsidXNlcm5hbWUiOiJBbGV4MyIsInBhc3N3b3JkIjoi" \
            "YWxleDJwd2R4In19.Gdr4mulzk-b_EIso8H2r1DR_putiadek0yDEvuRGYzA"
    task_data = {"title": "To fix car",
                 "description": "Go to service and fix car",
                 "deadline": "2024-04-16T18:30:00",
                 "username": "Alex"}
    response = client.post("/tasks/create/",
                           json=task_data,
                           headers={"Authorization": token})
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main()

import pytest

from server import Server


@pytest.fixture
def client():
    Server.app.config["TESTING"] = True
    with Server.app.test_client() as client:
        yield client


def test_valid_url(client):
    rv = client.post("/reviews", data=dict(
        url='https://www.lendingtree.com/reviews/personal/upgrade-inc/73349634'))
    assert rv.status_code == 200


def test_invalid_url(client):
    rv = client.post("/reviews",
                     data=dict(url='https://www.ldingtree.com/reviews/'))
    assert rv.status_code == 400


def test_invalid_url_2(client):
    rv = client.post("/reviews", data=dict(url='https://www.lendingtree.com/'))
    assert rv.status_code == 400




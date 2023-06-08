import http

from app import create_app


def test_smoke():
    app = create_app("test")
    client = app.test_client()
    resp = client.get("/smoke")
    assert resp.status_code == http.HTTPStatus.OK

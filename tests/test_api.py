import pytest

from synopsis import api


@pytest.fixture
def client():
    api.app.config['TESTING'] = True
    with api.app.test_client() as client:
        yield client
    api.documents = {}  # Empty the document store


class TestDocumentList:
    def test_post(self, client):
        response = client.post('/documents', json={'text': 'Hello, World!'})
        assert response.status_code == 201
        assert response.is_json
        json_data = response.get_json()
        assert 'id' in json_data
        assert 'text' in json_data
        assert json_data['text'] == 'Hello, World!'

    def test_get(self, client):
        response = client.get('/documents')
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == []


class TestDocument:
    def test_get(self, client):
        document_id = client \
            .post('/documents', json={'text': 'Hello, World!'}) \
            .get_json() \
            .get('id')
        response = client.get(f'/documents/{document_id}')
        assert response.status_code == 200
        assert response.is_json
        json_data = response.get_json()
        assert 'id' in json_data
        assert 'text' in json_data
        assert json_data['text'] == 'Hello, World!'

    def test_put(self, client):
        document_id = client \
            .post('/documents', json={'text': 'Hello, World!'}) \
            .get_json() \
            .get('id')
        response = client \
            .put(f'/documents/{document_id}', json={'text': 'Hello, Sailor!'})
        assert response.status_code == 200
        assert response.is_json
        json_data = response.get_json()
        assert 'id' in json_data
        assert 'text' in json_data
        assert json_data['text'] == 'Hello, Sailor!'

    def test_delete(self, client):
        document_id = client \
            .post('/documents', json={'text': 'Hello, World!'}) \
            .get_json() \
            .get('id')
        response = client.delete(f'/documents/{document_id}')
        assert response.status_code == 204


class TestSummary:
    def test_get(self, client):
        document_id = client \
            .post('/documents', json={'text': 'Hello, World!'}) \
            .get_json() \
            .get('id')
        response = client.get(f'/summaries/{document_id}')
        assert response.status_code == 200
        assert response.is_json
        json_data = response.get_json()
        assert 'document_id' in json_data
        assert 'summary' in json_data
        assert json_data['summary'] == 'Hello, World!'

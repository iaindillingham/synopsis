from uuid import uuid4

from flask import Flask
from flask_restful import abort
from flask_restful import Api
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from gensim import summarization

app = Flask(__name__)
api = Api(app)

parser = RequestParser()
parser.add_argument('text')

# The document store
# Keys are truncated UUIDs; values are dictionaries
documents = {}


def get_next_document_id():
    # If we use truncated UUIDs as IDs, then we're not leaking information
    # about, for example, how we store documents or how many documents
    # we have stored.
    return str(uuid4())[:8]


def abort_if_document_does_not_exist(document_id):
    if document_id not in documents:
        return abort(404, message=f'Document {document_id} does not exist')


def abort_if_text_is_missing(text):
    if not text:
        return abort(404, message=f'Text is missing')


def summarize(text):
    text_len = len(text)
    # Gensim should summarize a text of this length in about two seconds.
    tex_max_len = 20_000
    if text_len > tex_max_len:
        app.logger.info(
            f'The text is {text_len} characters long, '
            f'which is too long to summarize quickly. '
            f'Using the first {tex_max_len} characters instead.'
        )
    short_text = text[:tex_max_len]
    try:
        return summarization.summarize(short_text, ratio=0.1)
    except ValueError:
        app.logger.info(
            f'The text is {text_len} characters long, '
            f'which is not long enough to summarize. '
            f'Returning the text instead.'
        )
        return text


class DocumentList(Resource):
    """Represents a list of documents"""

    def post(self):
        """Create a document"""
        args = parser.parse_args()
        text = args['text']
        abort_if_text_is_missing(text)
        document_id = get_next_document_id()
        documents[document_id] = {
            'id': document_id,
            'text': text,
        }
        return documents[document_id], 201

    def get(self):
        """Get the list of documents"""
        return list(documents.values())


class Document(Resource):
    """Represents a document"""

    def get(self, document_id):
        """Get the document with the given document_id"""
        abort_if_document_does_not_exist(document_id)
        return documents[document_id]

    def put(self, document_id):
        """Update the document with the given document_id"""
        # Let's not allow the client to create a document with their choice
        # of document_id.
        abort_if_document_does_not_exist(document_id)
        args = parser.parse_args()
        documents[document_id].update({
            'text': args['text'],
        })
        return documents[document_id]

    def delete(self, document_id):
        """Delete the document with the given document_id"""
        abort_if_document_does_not_exist(document_id)
        del documents[document_id]
        return '', 204


class Summary(Resource):
    """Represents a summary of a document"""

    def get(self, document_id):
        """Get a summary of the document with the given document_id"""
        abort_if_document_does_not_exist(document_id)
        summary = summarize(documents[document_id]['text'])
        return {
            'document_id': document_id,
            'summary': summary,
        }


# Routing
api.add_resource(DocumentList, '/documents')
api.add_resource(Document, '/documents/<document_id>')
api.add_resource(Summary, '/summaries/<document_id>')

if __name__ == '__main__':
    app.run(debug=True)

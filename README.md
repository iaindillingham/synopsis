# Synopsis

> **synopsis** | noun (synopses)<br />
> A brief survey or general summary of something. [Lexico][1]

Synopsis is a REST API to a document summarisation service.
It's not intended for production use; it's intended to show [some nice people][2] that I can make a REST API in under four hours.

## Installation

The easiest way to install Synopsis is by first installing [Poetry][].
Next, clone this repository and run `poetry install`.
That's it!

## Usage

First, run Synopsis with Flask's builtin server.

```sh
poetry run python synopsis/api.py
```

The `documents` endpoint provides the usual [CRUD][] functions.

```sh
# Create a document
curl http://localhost:5000/documents -d 'text=Hello, World!'

# Get the list of documents
curl http://localhost:5000/documents

# Get the document with the given document_id
curl http://localhost:5000/documents/<document_id>

# Update the document with the given document_id
curl http://localhost:5000/documents/<document_id> -d 'text=Hello, Sailor!' -X PUT

# Delete the document with the given document_id
curl http://localhost:5000/documents/<document_id> -X DELETE
```

There are several plain-text Wikipedia pages in the documents directory.
These are for testing the `summaries` endpoint.

```sh
# Create a document
curl http://localhost:5000/documents -d "text=$(cat documents/Squirrel.txt)"

# Get a summary of the document with the given document_id
curl http://localhost:5000/summaries/<document_id>
```

## QA

```sh
poetry run flake8

poetry run pytest
```

## Next steps

**The document store.**
If you restart Flask's builtin server, then you clear the document store.
Ouch!
We should consider an alternative document store, such as a relational database.
Thankfully, this is easy with [SQLAlchemy][] and [Flask-SQLAlchemy][].

**English-language only.**
Synopsis uses [Gensim][] for document summarisation, but Gensim's `summarize` function is English-language only.
We could modify Synopsis' `summarize` function to use an alternative implementation.
Indeed, we could even write our own: several are described in [Text Summarization Techniques: A Brief Survey][3] by Allahyari et al.
However, we should probably ask the client for the language - or have Synopsis determine the language - and warn the client when the language isn't English.

**How much text is enough text?**
Gensim should summarize a text of 20,000 characters in about two seconds.
(See the [performance][6] section of the documentation.)
Is this much text enough text?
How should we trade this against Synopsis' response time?

**Static type checking and docstrings.** My future-self is always grateful when my past-self remembered to use static type checking and write docstrings, especially for helper functions such as `get_next_document_id`.

**More tests.**
We should test the methods that call `abort_if_document_does_not_exist` and `abort_if_text_is_missing` under failure, as well as success, conditions.

**Request parsing.**
Synopsis uses [Flask-RESTful][] to encourage best practices with minimal setup, but Flask-RESTful's request parser is "slated for removal".
We should consider using an alternative request parser, such as [marshmallow][].

**Curl.**
Why does `curl http://localhost:5000/documents -d "text=@documents/Squirrel.txt"` assign the string `@documents/Squirrel.txt` to `text`?
It should assign the contents of the file to `text`!

## Credits

Much of *api.py* is based on the [full example][4] from Flask-RESTful's documentation.

The client fixture in *test_api.py* is based on the [testing skeleton][5] in Flask's documentation.

[1]: https://www.lexico.com/definition/synopsis
[2]: https://squirro.com/
[3]: https://arxiv.org/abs/1707.02268v3
[4]: https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example
[5]: https://flask.palletsprojects.com/en/1.1.x/testing/#the-testing-skeleton
[6]: https://radimrehurek.com/gensim/auto_examples/tutorials/run_summarization.html#performance

[CRUD]: https://en.wikipedia.org/wiki/Create,_read,_update_and_delete
[Flask-RESTful]: https://flask-restful.readthedocs.io/en/latest/
[Flask-SQLAlchemy]: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
[Gensim]: https://radimrehurek.com/gensim/
[marshmallow-sqlalchemy]: https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
[marshmallow]: https://marshmallow.readthedocs.io/en/stable/
[Poetry]: https://python-poetry.org/
[SQLAlchemy]: https://www.sqlalchemy.org/

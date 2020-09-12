from flask import Flask, jsonify, abort, request

app = Flask(__name__)

quotes = {
    1: {
        "id": 1,
        "quote": "I'm gonna make him an offer he can't refuse.",
        "movie": "The Godfather",
    },
    2: {
        "id": 2,
        "quote": "Get to the choppa!",
        "movie": "Predator",
    },
    3: {
        "id": 3,
        "quote": "Nobody's gonna hurt anybody. We're gonna be like three little Fonzies here.",  # noqa E501
        "movie": "Pulp Fiction",
    },
}


def _quote_exists(quote):
    matches = [quote['quote'] == x['quote'] and quote['movie'] == x['movie'] for x in quotes.values()]
    return any(matches)


@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    return {'quotes': list(quotes.values())}


@app.route('/api/quotes/<int:qid>', methods=['GET'])
def get_quote(qid):
    if qid in quotes.keys():
        return {'quotes': [quotes[qid]]}
    
    return abort(404)


def _get_next_id():
    return max(quotes.keys()) + 1


@app.route('/api/quotes', methods=['POST'])
def create_quote():
    quote = request.get_json()
    if not ('quote' in quote and 'movie' in quote):
        return abort(400)
    if _quote_exists(quote):
        return abort(400)

    id = _get_next_id()
    quotes[id] = quote
    quotes[id]['id'] = id
    return {'quote': quotes[id]}, 201


@app.route('/api/quotes/<int:qid>', methods=['PUT'])
def update_quote(qid):
    if qid not in quotes.keys():
        return abort(404)
    quote = request.get_json()
    if not ('quote' in quote and 'movie' in quote):
        return abort(400)
    
    quotes[qid].update(quote)
    return {'quote': quotes[qid]}
    


@app.route('/api/quotes/<int:qid>', methods=['DELETE'])
def delete_quote(qid):
    if qid not in quotes.keys():
        return abort(404)

    del quotes[qid]
    return {'quotes': list(quotes.values())}, 204
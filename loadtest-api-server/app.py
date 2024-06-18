from flask import Flask, request, jsonify
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/loadtest', methods=['POST'])
def loadtest():

    url = request.form.get('url')
    qps = request.form.get('qps')

    if not url:
        return jsonify({'error': 'Missing query parameter: url'}), 400

    # Validate the URL format
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return jsonify({'error': 'Invalid URL'}), 400

    # Process the URL (you can add your logic here)
    response = {
        'received_url': url,
        'message': 'URL processed successfully'
    }

    return jsonify(response), 200
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
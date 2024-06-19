from flask import Flask, request, jsonify
from urllib.parse import urlparse

import requests
import time
from threading import Thread, Lock
import logging

app = Flask(__name__)

latencies = []
errors = 0
lock = Lock()

@app.route('/loadtest', methods=['POST'])
def loadtest():

    url = request.form.get('url')
    qps = request.form.get('qps')

    if not url:
        return jsonify({'error': 'Missing query parameter: url'}), 400

    if not qps:
        return jsonify({'error': 'Missing query parameter: qps'}), 400

    # Validate the URL format
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return jsonify({'error': 'Invalid URL'}), 400

    
    load_test_results = generate_load(url, float(qps), 60)

    # Process the URL (you can add your logic here)
    response = {
        'received_url': url,
        'message': 'URL processed successfully'
    }

    response.update(load_test_results)

    return jsonify(response), 200
    



def send_request(url):
    global errors
    start_time = time.time()
    try:
        response = requests.get(url)
        latency = time.time() - start_time
        with lock:
            latencies.append(latency)
        if response.status_code != 200:
            with lock:
                errors += 1
        print(f"Status Code: {response.status_code}, Response: {response.text}, Latency: {latency:.4f} seconds")
    except Exception as e:
        with lock:
            errors += 1
        logger.error(f"Request failed: {e}")
        


def generate_load(url: str, qps: float, duration: int):
    interval = 1.0 / qps
    end_time = time.time() + duration

    threads = []
    while time.time() < end_time:
        thread = Thread(target=send_request, kwargs={'url': url})
        threads.append(thread)
        thread.start()
        time.sleep(interval)
    
    for thread in threads:
        thread.join()

    # Reporting
    with lock:
        total_requests = len(latencies)
        average_latency = sum(latencies) / total_requests if total_requests > 0 else float('inf')
        error_rate = errors / total_requests if total_requests > 0 else float('inf')
        
    print("\n=== Load Test Report ===")
    print(f"Total Requests: {total_requests}")
    print(f"Total Errors: {errors}")
    print(f"Error Rate: {error_rate:.2%}")
    print(f"Average Latency: {average_latency:.4f} seconds")
    load_test_results = {
        'total_requests': total_requests,
        'errors': errors,
        'error_rate': f"{error_rate:.2%}",
        'average_latency': f"{average_latency:.4f} seconds"
    }
    if latencies:
        print(f"Max Latency: {max(latencies):.4f} seconds")
        print(f"Min Latency: {min(latencies):.4f} seconds")
        load_test_results["max_latency"] = f"{max(latencies):.4f} seconds"
        load_test_results["min_latency"] = f"{min(latencies):.4f} seconds"

    return load_test_results

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
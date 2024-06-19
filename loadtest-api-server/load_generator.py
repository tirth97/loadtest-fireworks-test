import requests
import time
from threading import Thread, Lock

latencies = []
errors = 0
lock = Lock()

def send_request(url):
    global errors
    while True:
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
            print(f"Request failed: {e}")


def generate_load(url, qps, duration):
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
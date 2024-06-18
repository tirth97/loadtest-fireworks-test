def send_request(url):
    while True:
        try:
            response = requests.get(url)
            print(f"Status Code: {response.status_code}, Response: {response.text}")
        except Exception as e:
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
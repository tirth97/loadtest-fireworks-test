# loadtest-fireworks-test
Build the docker image with the command:

```
docker build -t loadtest-api-server .
```

Run the docker image to start the server with command:

```
docker run --privileged -p 5050:5000 loadtest-api-server
```

To call the API:

```
curl -X POST -F "url=https://dummy.restapiexample.com/api/v1/employee/1" -F "qps=10" http://localhost:5050/loadtest
```


Sample Request and response:

Request:

```
curl -X POST -F "url=http://echo.jsontest.com/title/ipsum/content/blah" -F "qps=10" http://localhost:3009/loadtest
```

Response:
```
{
  "average_latency": "0.1333 seconds",
  "error_rate": "0.00%",
  "errors": 0,
  "max_latency": "0.6934 seconds",
  "message": "URL processed successfully",
  "min_latency": "0.0936 seconds",
  "received_url": "http://echo.jsontest.com/title/ipsum/content/blah",
  "total_requests": 587
}
```

The API: `http://localhost:3009/loadtest` would give 400 with user error incase url or qps are not mentioned
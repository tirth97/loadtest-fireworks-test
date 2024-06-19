# Problem:

This provides a server which helpes generate load test environment with url and queries per second. 


# Building and starting the server

To build and create a docker image:

```
docker build -t loadtest-api-server .
```

Run the docker image to start the server with command:

```
docker run --privileged -p 5050:5000 loadtest-api-server
```

NOTE: We use `--privileged` flag to allow permission for the flask server, if your server has required permissions that might not be needed.

To call the API:

```
curl -X POST -F "url=https://dummy.restapiexample.com/api/v1/employee/1" -F "qps=10" http://localhost:5050/loadtest
```


# Sample Request and response:

The API: `http://localhost:3009/loadtest` would give 400 with user error incase url or qps are not mentioned

Eg:

```
curl -X POST -F "url=http://echo.jsontest.com/title/ipsum/content/blah" http://localhost:3010/loadtest
{
  "error": "Missing query parameter: qps"
}
```

```
curl -X POST -F "qps=2" http://localhost:3010/loadtest
{
  "error": "Missing query parameter: url"
}
```

On server side we can see the response:
```
172.17.0.1 - - [19/Jun/2024 07:41:57] "POST /loadtest HTTP/1.1" 400 -
```

## Sample load generation request

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


# loadtest-fireworks-test
Build the docker image with the command:

```
docker build -t loadtest-api-server .
```

Run the docker image to start the server with command:

```
docker run --privileged -p 5050:5000 loadtest-api-server
```

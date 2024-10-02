# HTTP_Response_Probe
Probe that perform HTTP requests and handle response codes with detailed result reporting.

## Usage

### How to run the project without docker

```
# Open a terminal

cat <json-file> | python3 probe/probe.py
```

### How to run the project with docker

```
# Open a terminal

podman build -t <image-name> --build-arg GITLAB_TOKEN_USER=${GITLAB_TOKEN_USER} --build-arg GITLAB_TOKEN=${GITLAB_TOKEN} .

cat <json-file> | podman run -i <image-name>
```

## How input and output are structured

### Input

```json5
{
    config:{
        target:"https://google.com"
    }
}
```

### Output

```json5
{
  integer_result: 0,
  pretty_result: "Test executed successfully",
  extra_data: {
    //Errors and details
  }
}
```

## Examples

### Success

```
cat probe/test.json | python3 probe/probe.py
{"integer_result": 0, "pretty_result": "Test executed successfully", "extra_data": {}}
```
```
cat probe/test.json | podman run -i curlmonitor
{"integer_result": 0, "pretty_result": "Test executed successfully", "extra_data": {}}
```

### Fail

```
cat probe/test.json | python3 probe/probe.py
{"integer_result": 2, "pretty_result": "Failed to connect to the target", "extra_data": {"error": "[Errno -2] Name or service not known"}}
```

```
cat probe/input.json | podman run -i curlmonitor
{"integer_result": 2, "pretty_result": "Failed to connect to the target", "extra_data": {"error": "[Errno -2] Name or service not known"}}
```
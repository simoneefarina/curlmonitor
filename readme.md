# HTTP_Response_Probe
Probe that perform HTTP requests and handle response codes with detailed result reporting.

## Usage

### How to run

```
# Open a terminal

cat input.json | python3 probe/probe.py
```

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

### Fail

```
cat probe/test.json | python3 probe/probe.py
{"integer_result": 2, "pretty_result": "Failed to connect to the target", "extra_data": {"error": "[Errno -2] Name or service not known"}}
```
# Probe_Name
Simple probe that checks if an url exists using curl.

## Input

```json5
{
    config:{
        target:"test.com"
    }
}
```

## Output

```json5
{
  integer_result: 0,
  pretty_result: "Test executed successfully",
  extra_data: {
    //Errors and details
  }
}
```
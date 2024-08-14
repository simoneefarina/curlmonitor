# Probe_Name
Probe that perform HTTP requests and handle response codes with detailed result reporting.

## Input

```json5
{
    config:{
        target:"https://google.com"
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
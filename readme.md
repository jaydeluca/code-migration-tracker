# Code Migration Tracker

Goal: Given a repository, a timeframe, and any filtering rules, track a goal over time.

## Setup

A github token is not required but it is recommended as you will get rate limited if you make too many unauthenticated calls

```
export GITHUB_TOKEN="insert-your-token"
pip install -r requirements.txt
```

## Arguments

| Argument   | Command        | Description                                                                | Example                                                    |
|------------|----------------|----------------------------------------------------------------------------|------------------------------------------------------------|
| Repository | -r, --repo     | Repository name.                                                           | --repo "open-telemetry/opentelemetry-java-instrumentation" |
| Start Date | -s, --start    | Starting Date in format %Y-%m-%d (will calculate from this date until now) | --start "2022-11-15"                                       |
| Interval   | -i, --interval | Interval (in days) between data points                                     | --interval 14                                              |


## Example Usage:

In the `open-telemetry/opentelemetry-java-instrumentation` repository, track the conversion of tests from groovy to java 
in the `instrumentation` directory starting from 2022-11-15 with a data point every 2 weeks.

`python main.py -r "open-telemetry/opentelemetry-java-instrumentation" -s "2022-11-15" -i 14`

Output: 

![Example](./media/example_output.png)

## Approach

- Query Github for point in time snapshots based on commits around times spanning a timeframe
  - Get one data point every `interval` (example: every 14 days)
  - Filter based on some criteria
  - Cache this data locally to avoid repeated api calls
- Generate Graph to show results over time frame


## Data Filters


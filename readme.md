# Nagios_CheckHttpApi_RegEx_Perfdata
A simple Nagios check that receives data from an HTTP API and filters it using regular expressions.

## Parameters
|Patemeter          | Name          | Explanation |
|-------------------|---------------|-------------|
| -u                |URL            |URL of the API|
| -n                |Username       |API  login    |
| -p                |Password       |API  login    |
| -r                |RegEx          |RegEx to filter the API output, for example: "^[A-Za-z]+[0-9]+"|
| -w                |Warning        |Nagios limit  |
| -c                |Critical       |Nagios limit  |

## Example
```
python Nagios_CheckHttpRegEx_Perfdata.py -u [your_url] -n [your_username] -p [your_password] -r "[your_regex]" -w [your_warning_limit] -c [your_critical_limit]
```
Returns:
```
CRITICAL: 10
 | 'value'=10;50;100;0;0
````

Feel free to contact me if you have a question, or if you would like to make a suggestion for improvement.
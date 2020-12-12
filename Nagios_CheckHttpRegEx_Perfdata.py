import requests
import re 
import sys
import urllib3
import argparse
urllib3.disable_warnings()

#### nagios exit codes
##
nagios_exit_ok=0
nagios_exit_warning=1
nagios_exit_critical=2
nagios_exit_unknown=3
arguments_not_ok = 4
##
####

### Arguments
##
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', required=True, help='url string')
parser.add_argument('-n', '--user', required=True, help='username')
parser.add_argument('-p', '--password', required=True, help='password')
parser.add_argument('-r', '--regex', required=True, help='RegEx, e.g. ([a-zA-Z]+[ ]*[0-9]+)')
parser.add_argument('-w', '--warning', type=int, default=False, help='warning e.g -w 5')
parser.add_argument('-c', '--critical', type=int, default=False, help='critical e.g -c 10')
args = parser.parse_args();

if args.critical == False or args.warning == False:
        print("error: warning or critical value not spezified")
        parser.print_help()
        sys.exit(arguments_not_ok)
if args.critical <= args.warning:
        print("error: critical not greater than warning")
        parser.print_help()
        sys.exit(arguments_not_ok)
##
###

### Get data from api
##  
response = requests.get(url = args.url, verify=False,auth=(args.user, args.password)) 
if(response.status_code != 200):
    print("UKNOWN - Bad HTTP Status Code: ", response.status_code)
    sys.exit(nagios_exit_unknown)  
data = response.text
##
###

### Filter RegEx
##
result =  re.findall(args.regex, data)
if (len(result) == 0):
    print("UKNOWN - no data found")
    sys.exit(nagios_exit_unknown)
elif (len(result) >1):
    print("UKNOWN - RegEx returned more then one value")
    print(result)
    sys.exit(nagios_exit_unknown)
##
###

### Get numeric value
##
num_result_list = re.findall('[0-9]+', str(result))
num_result=int(num_result_list[0])
if (len(num_result) == 0):
    print("UKNOWN - no data found")
    sys.exit(nagios_exit_unknown)
elif (len(num_result) >1):
    print("UKNOWN - returned more then one numeric value")
    print(result)
    sys.exit(nagios_exit_unknown)
##
###


### Result
##
def checks():
    status = ["OK:", "WARNING:", "CRITICAL:","UNKNOWN:"]
    message = ""
    if(num_result >0 and num_result < args.warning):
        print(status[nagios_exit_ok] , num_result , message)
        return(nagios_exit_ok)
    elif(num_result >= args.warning and num_result < args.critical):
        print(status[nagios_exit_warning] , num_result , message)
        return(nagios_exit_warning)
    elif(num_result >= args.critical):
        print (status[nagios_exit_critical] , num_result , message)
        return(nagios_exit_critical)
    else:
        print (status[nagios_exit_unknown] , num_result , message)
        return(nagios_exit_unknown)
retcode = checks()
strr = " | 'value'=" + str(num_result) + ";" + str(args.warning) + ";" + str(args.critical) + ";0;0"
print(strr)
sys.exit(retcode)
##
###
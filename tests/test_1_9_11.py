import requests
import os

# prepare test case
test_cases = dict()
test_cases['http://localhost/?f=1&p=5'] = 'f=1\np=5'
test_cases['http://localhost?a=7&b=4'] = 'a=7\nb=4'
test_cases['http://localhost/hello?a=7&b=4'] = 'a=7\nb=4'
test_cases['http://localhost/hello?a=7&b=4'] = 'a=7\nb=4'

# start http server
os.system('sh ../init.sh')
print('started http server')

# check http request
testN = 0
testSuccess = 0
for test_request, test_answer in test_cases.items():
    testN += 1
    print('Test #' + str(testN))
    print(' - request:' + test_request)
    response = requests.get(test_request)
    result = True
    if response.status_code == 200:
        if test_answer:
            if test_answer != response.text:
                result = False
    else:
        result = False
    if result:
        print(' - Success')
        testSuccess += 1
    else:
        print(' - Fail')
        print(' - status code:' + str(response.status_code) + '| expected:200')
        print(' - text:' + response.text + '| expected:' + test_answer)
print('Result: ' + str(testSuccess) + ' / ' + str(testN))

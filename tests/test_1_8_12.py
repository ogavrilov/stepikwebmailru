import requests
import os
import sys

debugFlag = False
if len(sys.argv) > 1:
    if str(sys.argv[1]) == '1' or str(sys.argv[1]).lower() == 'true':
        debugFlag = True

# create test files
print('create test files...')
testCases = []

testCase = dict()
testCase['request'] = 'http://localhost/uploads/1.txt'
testCase['filePath'] = '../uploads/1.txt'
testCase['fileContent'] = '1.txt content'
testCase['statusCode'] = 200
testCases.append(testCase)

testCase = dict()
testCase['request'] = 'http://localhost/2.txt'
testCase['filePath'] = '../public/2.txt'
testCase['fileContent'] = '2.txt content'
testCase['statusCode'] = 200
testCases.append(testCase)

testCase = dict()
testCase['request'] = 'http://localhost/uploads/1'
testCase['filePath'] = ''
testCase['fileContent'] = ''
testCase['statusCode'] = 404
testCases.append(testCase)

for testCase in testCases:
    filePath = testCase.get('filePath')
    if filePath:
        with open(filePath, 'w') as fileHandle:
            fileHandle.write(testCase.get('fileContent'))
        print(' - created file: ' + filePath)

# start http server
os.system('sh ../init.sh')
print('started http server')

# check http request
testN = 0
testSuccess = 0
for testCase in testCases:
    testN += 1
    print('Test #' + str(testN))
    print(' - request:' + testCase.get('request'))
    response = requests.get(testCase.get('request'))
    result = True
    if response.status_code == testCase.get('statusCode'):
        fileContent = testCase.get('fileContent')
        if fileContent:
            if fileContent != response.text:
                result = False
    else:
        result = False
    if result:
        print(' - Success')
        testSuccess += 1
    else:
        print(' - Fail')
        print(' - status code:' + str(response.status_code) + '| expected:' + str(testCase.get('statusCode')))
        print(' - text:' + response.text + '| expected:' + testCase.get('fileContent'))
print('Result: ' + str(testSuccess) + ' / ' + str(testN))

# debug pause
if debugFlag:
    raw_input('Debug pause...enter to delete files and stop')

# delete test files
print('Deleting files...')
for testCase in testCases:
    filePath = testCase.get('filePath')
    if filePath:
        os.remove(filePath)
        print(' - deleted file:' + filePath)

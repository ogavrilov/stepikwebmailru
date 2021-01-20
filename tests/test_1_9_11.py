import requests
from testtemplate import testClass

class test_1_9_11(testClass):
    def __init__(self):
        self.result = self.__getResult__()
        # test without path hello not actual for nginx.conf
        # test 1
        #testCase = self.__getTestCase__()
        #testCase['title'] = 'Test #1: site root with slash'
        #testCase['data']['request'] = 'http://localhost/?f=1&p=5'
        #testCase['data']['answer'] = 'f=1\np=5'
        #self.result['cases'].append(testCase)
        # test 2
        #testCase = self.__getTestCase__()
        #testCase['title'] = 'Test #2: site root without slash'
        #testCase['data']['request'] = 'http://localhost?a=7&b=4'
        #testCase['data']['answer'] = 'a=7\nb=4'
        #self.result['cases'].append(testCase)
        # test 3
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #3: site hello with slash'
        testCase['data']['request'] = 'http://localhost/hello?a=7&b=4'
        testCase['data']['answer'] = 'a=7\nb=4'
        self.result['cases'].append(testCase)
        # test 4
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #4: site hello without slash'
        testCase['data']['request'] = 'http://localhost/hello?c=11&d=999'
        testCase['data']['answer'] = 'c=11\nd=999'
        self.result['cases'].append(testCase)

    def test(self):
        for testCase in self.result['cases']:
            testCase['out'].append(' - test - request:' + testCase['data']['request'])
            try:
                response = requests.get(testCase['data']['request'])
                result = True
                if response.status_code == 200:
                    if testCase['data']['answer']:
                        if testCase['data']['answer'] != response.text:
                            result = False
                else:
                    result = False
                if result:
                    testCase['out'].append(' - test - Success')
                    testCase['success'] = True
                    self.result['success'] += 1
                else:
                    testCase['out'].append(' - test - Fail')
                    testCase['error'].append(' - test - request:' + testCase['data']['request'])
                    testCase['error'].append(' - test - status code:' + str(response.status_code) + '| expected:200')
                    error_line = ' - test - text:' + str(response.text)
                    error_line += '| expected:' + str(testCase['data']['answer'])
                    testCase['error'].append(error_line)
            except Exception as ErrorObject:
                testCase['error'].append(' - test - error:' + str(ErrorObject))
        return self.result

def getTestObject():
    return test_1_9_11()
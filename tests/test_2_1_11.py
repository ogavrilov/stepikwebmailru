import requests
import os
from testtemplate import testClass

class test_2_1_11(testClass):
    def __init__(self):
        self.result = self.__getResult__()
        path_list = ['login', 'signup', 'ask', 'popular', 'new']
        for path in path_list:
            # test n1
            testCase = self.__getTestCase__()
            testCase['title'] = 'Test #' + str(len(self.result['cases'])) + ': path /' + path
            testCase['data']['request'] = 'http://localhost/' + path
            testCase['data']['answer'] = 'OK'
            testCase['data']['statusCode'] = 200
            self.result['cases'].append(testCase)
            # test n2 /anypath
            testCase = self.__getTestCase__()
            testCase['title'] = 'Test #' + str(len(self.result['cases'])) + ': path /' + path + '/anypath'
            testCase['data']['request'] = 'http://localhost/' + path + '/anypath'
            testCase['data']['answer'] = 'OK'
            testCase['data']['statusCode'] = 200
            self.result['cases'].append(testCase)
            # test n3 //popular/
            testCase = self.__getTestCase__()
            testCase['title'] = 'Test #' + str(len(self.result['cases'])) + ': path /' + path + '//popular/'
            testCase['data']['request'] = 'http://localhost/' + path + '//popular/'
            testCase['data']['answer'] = 'OK'
            testCase['data']['statusCode'] = 200
            self.result['cases'].append(testCase)
        # test path question
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #' + str(len(self.result['cases'])) + ': path /question'
        testCase['data']['request'] = 'http://localhost/question'
        testCase['data']['answer'] = ''
        testCase['data']['statusCode'] = 404
        self.result['cases'].append(testCase)
        # test path question int
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #' + str(len(self.result['cases'])) + ': path /question/123'
        testCase['data']['request'] = 'http://localhost/question/123'
        testCase['data']['answer'] = 'OK'
        testCase['data']['statusCode'] = 200
        self.result['cases'].append(testCase)
        # test path question str
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #' + str(len(self.result['cases'])) + ': path /question/id123'
        testCase['data']['request'] = 'http://localhost/question/id123'
        testCase['data']['answer'] = 'OK'
        testCase['data']['statusCode'] = 200
        self.result['cases'].append(testCase)

    def test(self):
        for testCase in self.result['cases']:
            testCase['out'].append(' - test - request:' + testCase['data']['request'])
            try:
                response = requests.get(testCase['data']['request'])
                result = True
                if response.status_code == testCase['data']['statusCode']:
                    answer = testCase['data']['answer']
                    if answer:
                        if answer != response.text:
                            result = False
                else:
                    result = False
                if result:
                    testCase['out'].append(' - test - Success')
                    testCase['success'] = True
                    self.result['success'] += 1
                else:
                    testCase['out'].append(' - test - Fail')
                    error_line = ' - test - status code:' + str(response.status_code)
                    error_line += '| expected:' + str(testCase['data']['statusCode'])
                    testCase['error'].append(error_line)
                    error_line = ' - test - text:' + response.text
                    error_line += '| expected:' + testCase['data']['answer']
                    testCase['error'].append(error_line)
            except Exception as ErrorObject:
                testCase['out'].append(' - test - Fail')
                testCase['error'].append(' - test - error:' + str(ErrorObject))
        return self.result

def getTestObject():
    return test_2_1_11()

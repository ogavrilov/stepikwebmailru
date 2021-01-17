import requests
import os
from testtemplate import testClass

class test_1_8_12(testClass):
    def __init__(self):
        self.result = self.__getResult__()
        # test 1
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #1: uploads catalog, file exists with file extansion'
        testCase['data']['request'] = 'http://localhost/uploads/1.txt'
        testCase['data']['filePath'] = '../uploads/1.txt'
        testCase['data']['fileContent'] = '1.txt content'
        testCase['data']['statusCode'] = 200
        self.result['cases'].append(testCase)
        # test 2
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #2: uploads catalog, file not exists with file extansion'
        testCase['data']['request'] = 'http://localhost/uploads/11.txt'
        testCase['data']['filePath'] = ''
        testCase['data']['fileContent'] = ''
        testCase['data']['statusCode'] = 404
        self.result['cases'].append(testCase)
        # test 3
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #3: upload catalog, file exists without file extansion'
        testCase['data']['request'] = 'http://localhost/uploads/3'
        testCase['data']['filePath'] = '../uploads/3'
        testCase['data']['fileContent'] = '3 content'
        testCase['data']['statusCode'] = 200
        self.result['cases'].append(testCase)
        # test 4
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #4: upload catalog, file not exists without file extansion'
        testCase['data']['request'] = 'http://localhost/uploads/31'
        testCase['data']['filePath'] = ''
        testCase['data']['fileContent'] = ''
        testCase['data']['statusCode'] = 404
        self.result['cases'].append(testCase)
        # test 5
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #5: any catalog (not upload), file exists with file extansion'
        testCase['data']['request'] = 'http://localhost/2.txt'
        testCase['data']['filePath'] = '../public/2.txt'
        testCase['data']['fileContent'] = '2.txt content'
        testCase['data']['statusCode'] = 200
        self.result['cases'].append(testCase)
        # test 6
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #6: any catalog (not upload), without file extansion'
        testCase['data']['request'] = 'http://localhost/2'
        testCase['data']['filePath'] = ''
        testCase['data']['fileContent'] = ''
        testCase['data']['statusCode'] = 404
        self.result['cases'].append(testCase)
        # test 7
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #7: any catalog (not upload), file not exists with file extansion'
        testCase['data']['request'] = 'http://localhost/3.txt'
        testCase['data']['filePath'] = ''
        testCase['data']['fileContent'] = ''
        testCase['data']['statusCode'] = 404
        self.result['cases'].append(testCase)

    def load(self):
        for testCase in self.result['cases']:
            filePath = testCase['data']['filePath']
            if filePath:
                try:
                    with open(filePath, 'w') as fileHandle:
                        fileHandle.write(testCase['data']['fileContent'])
                    testCase['out'].append(' - load - created file: ' + filePath)
                except Exception as ErrorObject:
                    testCase['error'].append(' - load - create file error:' + str(ErrorObject))

    def test(self):
        for testCase in self.result['cases']:
            testCase['out'].append(' - test - request:' + testCase['data']['request'])
            try:
                response = requests.get(testCase['data']['request'])
                testCase['out'].append(' - test - request:' + testCase['data']['request'])
                result = True
                if response.status_code == testCase['data']['statusCode']:
                    fileContent = testCase['data']['fileContent']
                    if fileContent:
                        if fileContent != response.text:
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
                    error_line = ' - test - status code:' + str(response.status_code)
                    error_line += '| expected:' + str(testCase['data']['statusCode'])
                    testCase['error'].append(error_line)
                    error_line = ' - test - text:' + response.text
                    error_line += '| expected:' + testCase['data']['fileContent']
                    testCase['error'].append(error_line)
            except Exception as ErrorObject:
                testCase['out'].append(' - test - Fail')
                testCase['error'].append(' - test - error:' + str(ErrorObject))
        return self.result

    def unload(self):
        for testCase in self.result['cases']:
            filePath = testCase['data']['filePath']
            if filePath:
                try:
                    os.remove(filePath)
                    testCase['out'].append(' - unload - deleted file: ' + filePath)
                except Exception as ErrorObject:
                    testCase['error'].append(' - unload - delete file error:' + str(ErrorObject))

def getTestObject():
    return test_1_8_12()

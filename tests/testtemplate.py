# parent class
# how use class methods see in test_1_8_12.py
class testClass:
    def __init__(self):
        self.result = self.__getResult__()
        testCase1 = self.__getTestCase__()
        testCase1['title'] = 'test1'
        self.result.get('cases').append(testCase1)

    def load(self):
        # here code for prepare data for test
        # code will execute before test combine start
        pass

    def test(self):
        # here test code and fill results
        self.result['cases'][0]['out'] = ['info out print line1', 'info out print line2']
        self.result['cases'][0]['error'] = ['error print line1', 'error print line2']
        self.result['cases'][0]['success'] =True
        return self.result

    def unload(self):
        # here code for unprepare data after test
        # code will execute after test combine start
        pass

    def __getResult__(self):
        defaultResult = dict()
        defaultResult['success'] = 0
        defaultResult['cases'] = list()
        return defaultResult

    def __getTestCase__(self):
        defaultTestCase = dict()
        # for user edit in __init__()
        defaultTestCase['title'] = '<test title>'
        defaultTestCase['data'] = dict()
        # for user edit in test()
        defaultTestCase['out'] = list()
        defaultTestCase['error'] = list()
        defaultTestCase['success'] = False
        return defaultTestCase

'''
 this method for help test combine get object with type local class
 now i can't import py script as module with dynamic name and create object 
  with type from module with dynamic name type
'''
def getTestObject():
    return testClass()
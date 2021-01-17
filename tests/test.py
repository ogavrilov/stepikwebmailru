import sys
import os.path
import glob
import time
import subprocess

# prepare variables
testBlocks = dict()
debugFlag = False
testBlocksCount = 0
testSuccessResult = 0
testResults = dict()
serverProcess = None

# prepare args
if len(sys.argv) > 1:
    for argNum in range(1, len(sys.argv)):
        argv = sys.argv[argNum]
        if argv:
            if str(argv).lower() == 'debug':
                debugFlag = True
            else:
                testBlocks[argv] = 'not imported'

# check testBlocks files exists
for blockName in testBlocks.keys():
    # check file in cur catalog with blockName
    if not os.path.exists(blockName + '.py'):
        testBlocks.pop(blockName)
        print('[ERROR] File ' + blockName + '.py not exists. Skipped.')

# fill testBlock from catalog if cleared
if len(testBlocks) == 0:
    print('[INFO] Load all test blocks.')
    for testFile in glob.glob('test_*.py'):
        testBlocks[testFile.replace('.py', '')] = 'not imported'

# prepare testBlocks
testBlocksCount = len(testBlocks)
for blockName in testBlocks.keys():
    try:
        testBlocks[blockName] = __import__(blockName).getTestObject()
        if debugFlag:
            print('[INFO] Loaded test block: ' + blockName)
    except Exception as ErrorObject:
        testBlocks.pop(blockName)
        if debugFlag:
            print('[ERROR] Test block "' + blockName + '" load error: ' + str(ErrorObject))
print('[INFO] Loaded ' + str(len(testBlocks)) + ' / ' + str(testBlocksCount) + ' test  blocks.')

# prepare test data
for blockName, blockValue in testBlocks.items():
    try:
        blockValue.load()
        if debugFlag:
            print('[INFO] Test block "' + blockName + '" prepared.')
    except Exception as ErrorObject:
        print('[ERROR] Test block "' + blockName + '" prepare error: ' + str(ErrorObject))

# start server
try:
    print('[INFO] Server starting...')
    os.system('sh ../init.sh')
    time.sleep(3)
    print('-------------------------')
except Exception as ErrorObject:
    print('[ERROR] Server start error: ' + str(ErrorObject))
    sys.exit(1)

# execute tests
for blockName, blockValue in testBlocks.items():
    try:
        testResult = blockValue.test()
        testResults[blockValue] = testResult
        info_line = '[INFO] Test block "' + blockName + '" results: '
        info_line += str(testResult.get('success', 0)) + ' / ' + str(len(testResult.get('cases')))
        print(info_line)
        if len(testResult.get('cases')) == testResult.get('success', 0):
            testSuccessResult += 1
        else:
            for testCase in testResult.get('cases'):
                if debugFlag:
                    print('[INFO] [TEST] ' + testCase.get('title'))
                    for outLine in testCase.get('out'):
                        print(outLine)
                if not testCase.get('success'):
                    print('[ERROR] [TEST] ' + testCase.get('title'))
                    for errorLine in testCase.get('error'):
                        print(errorLine)
                    print('-------------------------')
                elif debugFlag:
                    print('-------------------------')
    except Exception as ErrorObject:
        print('[ERROR] Test block "' + blockName + '" execute error: ' + str(ErrorObject))
print('[INFO] Tests block results: ' + str(testSuccessResult) + ' / ' + str(len(testBlocks))) 

# debug pause
if debugFlag:
    try:
        raw_input('Debug pause...enter to clean test data and stop')
    except:
        input('Debug pause...enter to clean test data and stop')

# clean test data
for blockName, blockValue in testBlocks.items():
    try:
        blockValue.unload()
        if debugFlag:
            print('[INFO] Test block "' + blockName + '" test data cleaned.')
    except Exception as ErrorObject:
        print('[ERROR] Test block "' + blockName + '" test data clean error: ' + str(ErrorObject))

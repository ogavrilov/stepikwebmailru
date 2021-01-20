import sys
import os
import glob
import time
import subprocess
import traceback

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
blockIndex = 0
testBlocksNames = [dictKey for dictKey in testBlocks.keys()]
for blockIndex in range(0, len(testBlocksNames)):
    blockName = testBlocksNames[blockIndex]
    # check file in cur catalog with blockName
    if not os.path.exists('tests/' + blockName + '.py'):
        testBlocks.pop(blockName)
        print('[ERROR] File tests/' + blockName + '.py not exists. Skipped.')

# fill testBlock from catalog if cleared
if len(testBlocks) == 0:
    print('[INFO] Loading all test blocks from ' + os.getcwd() + '/tests/...')
    for testFile in glob.glob('tests/test_*.py'):
        testBlocks[testFile.replace('.py', '')] = 'not imported'

# prepare testBlocks
testBlocksCount = len(testBlocks)
blockIndex = 0
testBlocksNames = [dictKey for dictKey in testBlocks.keys()]
for blockIndex in range(0, len(testBlocksNames)):
    try:
        blockName = testBlocksNames[blockIndex]
        moduleName = '' + blockName.replace('tests/', '')
        testBlocks[blockName] = __import__(moduleName).getTestObject()
        if debugFlag:
            print('[INFO] Loaded test block: ' + blockName)
    except:
        print('[ERROR] Test block "' + blockName + '" load error: ' + str(traceback.format_exc()) + '|' + moduleName)
        testBlocks.pop(blockName)

print('[INFO] Loaded ' + str(len(testBlocks)) + ' / ' + str(testBlocksCount) + ' test  blocks.')

# check test exists
if len(testBlocks) == 0:
    print('[INFO] No test block for testing.')
    sys.exit(1)

# prepare test data
for blockName, blockValue in testBlocks.items():
    try:
        blockValue.load()
        if debugFlag:
            print('[INFO] Test block "' + blockName + '" prepared.')
    except:
        print('[ERROR] Test block "' + blockName + '" prepare error: ' + str(traceback.format_exc()))

# start server
try:
    print('[INFO] Server starting...')
    os.system('bash init.sh')
    time.sleep(3)
    print('-------------------------')
except:
    print('[ERROR] Server start error: ' + str(traceback.format_exc()))
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
    except:
        print('[ERROR] Test block "' + blockName + '" execute error: ' + str(traceback.format_exc()))
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
    except:
        print('[ERROR] Test block "' + blockName + '" test data clean error: ' + str(traceback.format_exc()))

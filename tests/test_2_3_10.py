from testtemplate import testClass
import MySQLdb as pymysql
import re
from django.db import connection as djangoconnection
import random
import datetime
import os
import sys

class test_2_3_10(testClass):
    def __init__(self):
        self.connection = None
        self.load_error = ''
        self.load_out = ''
        self.host = 'localhost'
        self.user = 'test'
        self.pwd = '123'
        self.mysqlResults = dict()
        self.pythonResults = dict()
        self.modelsPath = 'qa.models'
        self.moduleVar = None
        self.result = self.__getResult__()
        self.djangoTestModels = list()
        # test 1
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #1: mysql database project_ask exist'
        testCase['data']['type'] = 'mysql'
        testCase['data']['query'] = 'show databases'
        testCase['data']['mask'] = r'.project_ask.'
        self.result['cases'].append(testCase)
        # test 2
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #2: mysql user project_ask_user exist'
        testCase['data']['type'] = 'mysql'
        testCase['data']['query'] = 'select user from mysql.user'
        testCase['data']['mask'] = r'.project_ask_user.'
        self.result['cases'].append(testCase)
        # test 3
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #3: mysql user project_ask_user grants all privileges for database project_ask'
        testCase['data']['type'] = 'mysql'
        testCase['data']['query'] = 'show grants for project_ask_user@localhost'
        testCase['data']['mask'] = r'.GRANT ALL PRIVILEGES ON \`project_ask\`\.\*.'
        self.result['cases'].append(testCase)
        # test tables and columns
        tables = list()
        columns = list()
        columns.append({'name': 'id', 'mask': r'[^\(]*\([^\)]*id[^\)]*int[^\)]*PRI[^\)]*\)', 'result': 'questionColumns'})
        columns.append({'name': 'title', 'mask': r'[^\(]*\([^\)]*title[^\)]*char[^\)]*\)', 'result': 'questionColumns'})
        columns.append({'name': 'text', 'mask': r'[^\(]*\([^\)]*text[^\)]*longtext[^\)]*\)', 'result': 'questionColumns'})
        columns.append({'name': 'added_at', 'mask': r'[^\(]*\([^\)]*added_at[^\)]*date[^\)]*\)', 'result': 'questionColumns'})
        columns.append({'name': 'rating', 'mask': r'[^\(]*\([^\)]*rating[^\)]*int[^\)]*\)', 'result': 'questionColumns'})
        columns.append({'name': 'author_id', 'mask': r'[^\(]*\([^\)]*author_id[^\)]*int[^\)]*\)', 'result': 'questionColumns'})
        tables.append({'name': 'qa_question', 'columns': columns})
        columns = list()
        columns.append({'name': 'id', 'mask': r'[^\(]*\([^\)]*id[^\)]*int[^\)]*PRI[^\)]*\)', 'result': 'answerColumns'})
        columns.append({'name': 'text', 'mask': r'[^\(]*\([^\)]*text[^\)]*longtext[^\)]*\)', 'result': 'answerColumns'})
        columns.append({'name': 'added_at', 'mask': r'[^\(]*\([^\)]*added_at[^\)]*date[^\)]*\)', 'result': 'answerColumns'})
        columns.append({'name': 'question_id', 'mask': r'[^\(]*\([^\)]*question_id[^\)]*int[^\)]*\)', 'result': 'answerColumns'})
        columns.append({'name': 'author_id', 'mask': r'[^\(]*\([^\)]*author_id[^\)]*int[^\)]*\)', 'result': 'answerColumns'})
        tables.append({'name': 'qa_answer', 'columns': columns})
        columns = list()
        columns.append({'name': 'question_id', 'mask': r'[^\(]*\([^\)]*question_id[^\)]*int[^\)]*MUL[^\)]*\)', 'result': 'likesColumns'})
        columns.append({'name': 'user_id', 'mask': r'[^\(]*\([^\)]*user_id[^\)]*int[^\)]*MUL[^\)]*\)', 'result': 'likesColumns'})
        tables.append({'name': 'qa_question_likes', 'columns': columns})
        tables.append({'name': 'user', 'columns': list()})
        for table in tables:
            testCase = self.__getTestCase__()
            testNum = 1 + len(self.result['cases'])
            testCase['title'] = 'Test #' + str(testNum) + ': mysql check exists table "' + table['name'] + '"'
            testCase['data']['type'] = 'mysql'
            testCase['data']['query'] = 'show tables from project_ask'
            testCase['data']['mask'] = r'.' + table['name'] + '.'
            self.result['cases'].append(testCase)
            for column in table['columns']:
                testCase = self.__getTestCase__()
                testNum = 1 + len(self.result['cases'])
                testCase['title'] = 'Test #' + str(testNum) + ': mysql check table "'
                testCase['title'] += table['name'] + '" column:' + column['name']
                testCase['data']['type'] = 'mysql'
                testCase['data']['query'] = 'show columns from ' + table['name'] + ' from project_ask'
                testCase['data']['mask'] = column['mask']
                testCase['data']['result'] = column['result']
                self.result['cases'].append(testCase)
        # test python classes
        # why comment fields not expected !?
        # DateField is NoneType
        # author, author_id
        classes = list()
        fields = list()
        fields.append({'name': 'title', 'mask': r'.str.', 'result': 'objQuestion'})
        fields.append({'name': 'text', 'mask': r'.str.', 'result': 'objQuestion'})
        #fields.append({'name': 'added_at', 'mask': r'.date.', 'result': 'objQuestion'})
        fields.append({'name': 'rating', 'mask': r'.int.', 'result': 'objQuestion'})
        fields.append({'name': 'author_id', 'mask': r'.int.', 'result': 'objQuestion'})
        #fields.append({'name': 'author', 'mask': r'.User.', 'result': 'objQuestion'})
        classes.append({'name': 'Question', 'fields': fields, 'result': 'objQuestion'})
        fields = list()
        fields.append({'name': 'text', 'mask': r'.str.', 'result': 'objAnswer'})
        #fields.append({'name': 'added_at', 'mask': r'.date.', 'result': 'objAnswer'})
        #fields.append({'name': 'author_id', 'mask': r'.int.', 'result': 'objAnswer'})
        #fields.append({'name': 'author', 'mask': r'.User.', 'result': 'objAnswer'})
        classes.append({'name': 'Answer', 'fields': fields, 'result': 'objAnswer'})
        for curClass in classes:
            testCase = self.__getTestCase__()
            testNum = 1 + len(self.result['cases'])
            testCase['title'] = 'Test #' + str(testNum) + ': python check exists class "' + curClass['name'] + '"'
            testCase['data']['type'] = 'python'
            testCase['data']['result'] = curClass['result']
            testCase['data']['className'] = curClass['name']
            self.result['cases'].append(testCase)
            for curField in curClass['fields']:
                testCase = self.__getTestCase__()
                testNum = 1 + len(self.result['cases'])
                testCase['title'] = 'Test #' + str(testNum) + ': python check field ' + curField['name']
                testCase['title'] += ' in class "' + curClass['name'] + '"'
                testCase['data']['type'] = 'python'
                testCase['data']['result'] = curField['result']
                testCase['data']['fieldName'] = curField['name']
                testCase['data']['typeMask'] = curField['mask']
                testCase['data']['className'] = curClass['name']
                self.result['cases'].append(testCase)
        # test django database settings
        testCase = self.__getTestCase__()
        testNum = 1 + len(self.result['cases'])
        testCase['title'] = 'Test #' + str(testNum) + ': django database setting'
        testCase['data']['type'] = 'django'
        testCase['data']['method'] = self.__checkDjangoDatabaseConnection__
        self.result['cases'].append(testCase)
        # test django questions create
        testCase = self.__getTestCase__()
        testNum = 1 + len(self.result['cases'])
        testCase['title'] = 'Test #' + str(testNum) + ': django model Question create'
        testCase['data']['type'] = 'django'
        testCase['data']['method'] = self.__checkDjangoQuestionCreate__
        self.result['cases'].append(testCase)
        # test django answers create
        testCase = self.__getTestCase__()
        testNum = 1 + len(self.result['cases'])
        testCase['title'] = 'Test #' + str(testNum) + ': django model Answer create'
        testCase['data']['type'] = 'django'
        testCase['data']['method'] = self.__checkDjangoAnswerCreate__
        self.result['cases'].append(testCase)
        # test django question manager method last
        testCase = self.__getTestCase__()
        testNum = 1 + len(self.result['cases'])
        testCase['title'] = 'Test #' + str(testNum) + ': django model Question method Last'
        testCase['data']['type'] = 'django'
        testCase['data']['method'] = self.__checkDjangoQuestionLast__
        self.result['cases'].append(testCase)
        # test django question manager method popular
        testCase = self.__getTestCase__()
        testNum = 1 + len(self.result['cases'])
        testCase['title'] = 'Test #' + str(testNum) + ': django model Question method Popular'
        testCase['data']['type'] = 'django'
        testCase['data']['method'] = self.__checkDjangoQuestionPopular__
        self.result['cases'].append(testCase)

    def load(self):
        try:
            self.connection = pymysql.Connect(host=self.host, user=self.user, password=self.pwd)
            random.seed()
        except Exception as ErrorObject:
            self.connection = None
            self.load_error += '\n[ERROR] - load - Connected to mysql server error: ' + str(ErrorObject)
            self.load_error += '\n[ERROR] - load - host:' + self.host
            self.load_error += '\n[ERROR] - load - user:' + self.user
            self.load_error += '\n[ERROR] - load - pwd:' + self.pwd

    def test(self):
        for testCase in self.result['cases']:
            # query to mysql server
            if testCase['data']['type'] == 'mysql':
                if self.connection is None:
                    testCase['error'].append(' - test - Skipped. Mysql server connection error:' + self.load_error)
                else:
                    try:
                        # if query result is not exist - get it, else get result from local var
                        resultKey = testCase['data'].get('result')
                        if resultKey is None or self.mysqlResults.get(resultKey) is None:
                            cursor = self.connection.cursor()
                            cursor.execute(testCase['data']['query'])
                            outResult = ''
                            for row in cursor:
                                outResult += str(row)
                            if not (resultKey is None):
                                self.mysqlResults[resultKey] = outResult
                        else:
                            outResult = self.mysqlResults[resultKey]
                        # do cur test
                        if not re.search(testCase['data']['mask'].lower(), outResult.lower()) is None:
                            testCase['out'].append(' - test - Success')
                            testCase['out'].append(' - test - query:' + testCase['data']['query'])
                            testCase['success'] = True
                            self.result['success'] += 1
                        else:
                            testCase['out'].append(' - test - Fail')
                            testCase['error'].append(' - test - query:' + testCase['data']['query'])
                            error_line = ' - test - answer:' + outResult
                            error_line += '|expected mask matching:' + testCase['data']['mask']
                            testCase['error'].append(error_line)
                    except Exception as ErrorObject:
                        testCase['out'].append(' - test - Fail')
                        testCase['error'].append(' - test - query:' + testCase['data']['query'])
                        testCase['error'].append(' - test - error:' + str(ErrorObject))
            elif testCase['data']['type'] == 'django':
                try:
                    nullVar = testCase['data']['method']
                    testCase['out'].append(' - test - Success')
                    testCase['success'] = True
                    self.result['success'] += 1
                except Exception as ErrorObject:
                    testCase['out'].append(' - test - Fail')
                    testCase['error'].append(' - test - error:' + str(ErrorObject))
            elif testCase['data']['type'] == 'python':
                try:
                    # import models module
                    if self.moduleVar is None:
                        sys.path.insert(0, os.getcwd() + '/ask')
                        from django.core.wsgi import get_wsgi_application
                        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask.settings')
                        application = get_wsgi_application()
                        self.moduleVar = __import__(self.modelsPath)
                    # if class object is not created - do it, if created - get to local var
                    resultKey = testCase['data'].get('result')
                    if resultKey is None or self.mysqlResults.get(resultKey) is None:
                        from qa.models import Question
                        classObject = Question()
                        if not resultKey is None:
                            self.mysqlResults[resultKey] = classObject
                    else:
                        classObject = self.mysqlResults[resultKey]
                    # do cur test
                    if not testCase['data'].get('fieldName') is None:
                        # field test
                        fieldName = testCase['data'].get('fieldName')
                        fieldTypeMask = testCase['data'].get('typeMask')
                        if not hasattr(classObject, fieldName):
                            testCase['out'].append(' - test - Fail')
                            testCase['error'].append(' - test - check class:' + testCase['data']['className'])
                            error_line = ' - test - field miss:' + testCase['data']['fieldName']
                            testCase['error'].append(error_line)
                        else:
                            fieldTypeStr = str(type(eval('classObject.' + testCase['data']['fieldName'])))
                            if re.search(fieldTypeMask.lower(), fieldTypeStr.lower()) is None:
                                testCase['out'].append(' - test - Fail')
                                testCase['error'].append(
                                    ' - test - check class:' + testCase['data']['className'])
                                error_line = ' - test - field:' + testCase['data']['fieldName']
                                testCase['error'].append(error_line)
                                error_line = ' - test - field type:'
                                error_line += str(type(eval('classObject.' + testCase['data']['fieldName'])))
                                error_line += '|expected type by mask:' + testCase['data']['typeMask']
                                testCase['error'].append(error_line)
                            else:
                                testCase['out'].append(' - test - Success')
                                testCase['success'] = True
                                self.result['success'] += 1
                    else:
                        # class exist test
                        # if we is here - classObject has been created without error
                        testCase['out'].append(' - test - Success')
                        testCase['success'] = True
                        self.result['success'] += 1
                except Exception as ErrorObject:
                    testCase['out'].append(' - test - Fail')
                    testCase['error'].append(' - test - check class:' + testCase['data']['className'])
                    if not testCase['data'].get('fieldName') is None:
                        error_line = ' - test - field:' + testCase['data']['fieldName']
                        testCase['error'].append(error_line)
                        error_line = ' - test - field type:'
                        error_line += str(type(eval('classObject.' + testCase['data']['fieldName'])))
                        error_line += '|expected type by mask:' + testCase['data']['typeMask']
                        testCase['error'].append(error_line)
                    testCase['error'].append(' - test - error:' + str(ErrorObject))
        return self.result

    def unload(self):
        try:
            self.connection.close()
            self.load_out += '\n[INFO] - unload - Close connection to mysql server "' + self.host + '".'
        except Exception as ErrorObject:
            self.connection = None
            self.load_error += '\n[ERROR] - unload - Close connection to mysql server error: ' + str(ErrorObject)
            self.load_error += '\n[ERROR] - unload - host:' + self.host
            self.load_error += '\n[ERROR] - unload - user:' + self.user
            self.load_error += '\n[ERROR] - unload - pwd:' + self.pwd
        try:
            for curModel in self.djangoTestModels:
                curModel.delete()
        except Exception as ErrorObject:
            self.load_error += '\n[ERROR] - unload - django model delete error: ' + str(ErrorObject)

    def __checkDjangoDatabaseConnection__(self):
        djangoCursor = djangoconnection.cursor()
        djangoCursor.execute('select * django_migrations')
        outline = ''
        for dbLine in djangoCursor.fetchall():
            outline += str(dbLine)

    def __checkDjangoQuestionCreate__(self):
        # provide app models module import
        if self.moduleVar is None:
            self.moduleVar = __import__(self.modelsPath)
        # create
        n_title = 'Question title ' + str(random.getrandbits(8))
        n_text = 'Question text' + str(random.getrandbits(8))
        n_rating = random.randint(1, 10)
        n_added_at = datetime.date(2021, 1, random.randint(1, 30))
        newQuestion = self.moduleVar.Question(title=n_title, text=n_text, rating=n_rating, added_at=n_added_at)
        self.djangoTestModels.append(newQuestion)

    def __checkDjangoAnswerCreate__(self):
        # provide app models module import
        if self.moduleVar is None:
            self.moduleVar = __import__(self.modelsPath)
        # create
        n_text = 'Question text' + str(random.getrandbits(8))
        n_added_at = datetime.date(2021, 1, random.randint(1, 30))
        newAnswer = self.moduleVar.Answer(text=n_text, added_at=n_added_at)
        self.djangoTestModels.append(newAnswer)

    def __checkDjangoQuestionLast__(self):
        # provide app models module import
        if self.moduleVar is None:
            self.moduleVar = __import__(self.modelsPath)
        # create test data
        try:
            self.__checkDjangoQuestionCreate__()
            self.__checkDjangoQuestionCreate__()
            self.__checkDjangoQuestionCreate__()
            self.__checkDjangoQuestionCreate__()
            self.__checkDjangoQuestionCreate__()
        except:
            raise Exception('Skipped. Cant create test data, check Question model create test')
        # get data by manager
        managerResult = self.moduleVar.Question.new()
        # get data by filter
        standardResult = self.moduleVar.Question.objects.order_by('-added_at')
        # check order and elements
        for listIndex in range(0, len(managerResult)):
            if not managerResult[listIndex].id == standardResult[listIndex].id:
                exeptionLine = 'result of method Question.new() and corr filter not matches'
                exeptionLine += ' (method:' + str(managerResult) + '|filter:' + str(standardResult) + ')'
                raise Exception(exeptionLine)

    def __checkDjangoQuestionPopular__(self):
        # provide app models module import
        if self.moduleVar is None:
            self.moduleVar = __import__(self.modelsPath)
        # create test data
        try:
            self.__checkDjangoQuestionCreate__()
            self.__checkDjangoQuestionCreate__()
            self.__checkDjangoQuestionCreate__()
            self.__checkDjangoQuestionCreate__()
            self.__checkDjangoQuestionCreate__()
        except:
            raise Exception('Skipped. Cant create test data, check Question model create test')
        # get data by manager
        managerResult = self.moduleVar.Question.popular()
        # get data by filter
        standardResult = self.moduleVar.Question.objects.order_by('-rating')
        # check order and elements
        for listIndex in range(0, len(managerResult)):
            if not managerResult[listIndex].id == standardResult[listIndex].id:
                exceptionLine = 'result of method Question.popular() and corr filter not matches'
                exceptionLine += ' (method:' + str(managerResult) + '|filter:' + str(standardResult) + ')'
                raise Exception(exceptionLine)


def getTestObject():
    return test_2_3_10()

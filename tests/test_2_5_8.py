from testtemplate import testClass
import requests
import traceback
import re
import os
import sys
import random
import datetime


class test_2_5_8(testClass):
    def __init__(self):
        self.result = self.__getResult__()
        self.test_data = dict()
        self.djangoTestModels = list()
        self.load_error = ''
        self.load_out = ''
        self.question_max_id = 0
        # test 1
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #1: page latest questions exist in root'
        testCase['data']['type'] = 'page exist'
        testCase['data']['request'] = 'http://localhost/'
        testCase['data']['status_code'] = 200
        testCase['data']['key'] = 'list_latest_first'
        self.result['cases'].append(testCase)
        # test 2
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #2: second page latest questions exist in root'
        testCase['data']['type'] = 'page exist'
        testCase['data']['request'] = 'http://localhost/?page=2'
        testCase['data']['status_code'] = 200
        testCase['data']['key'] = 'list_latest_second'
        self.result['cases'].append(testCase)
        # test 3
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #3: page popular questions exist in root'
        testCase['data']['type'] = 'page exist'
        testCase['data']['request'] = 'http://localhost/popular'
        testCase['data']['status_code'] = 200
        testCase['data']['key'] = 'list_popular_first'
        self.result['cases'].append(testCase)
        # test 4
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #4: second page popular questions exist in root'
        testCase['data']['type'] = 'page exist'
        testCase['data']['request'] = 'http://localhost/popular/?page=2'
        testCase['data']['status_code'] = 200
        testCase['data']['key'] = 'list_popular_second'
        self.result['cases'].append(testCase)
        # test 5
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #5: latest page 1 contain 10 question blocks'
        testCase['data']['type'] = 'question block count'
        testCase['data']['key'] = 'list_latest_first'
        testCase['data']['mask'] = r'(<div class="question_box">(\s|.|^[div>])*?div>)'
        testCase['data']['groups_count'] = 10
        self.result['cases'].append(testCase)
        # test 6
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #6: latest page 2 contain 10 question blocks'
        testCase['data']['type'] = 'question block count'
        testCase['data']['key'] = 'list_latest_second'
        testCase['data']['mask'] = r'(<div class="question_box">(\s|.|^[div>])*?div>)'
        testCase['data']['groups_count'] = 10
        self.result['cases'].append(testCase)
        # test 7
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #7: popular page 1 contain 10 question blocks'
        testCase['data']['type'] = 'question block count'
        testCase['data']['key'] = 'list_popular_first'
        testCase['data']['mask'] = r'(<div class="question_box">(\s|.|^[div>])*?div>)'
        testCase['data']['groups_count'] = 10
        self.result['cases'].append(testCase)
        # test 8
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #8: popular page 2 contain 10 question blocks'
        testCase['data']['type'] = 'question block count'
        testCase['data']['key'] = 'list_popular_second'
        testCase['data']['mask'] = r'(<div class="question_box">(\s|.|^[div>])*?div>)'
        testCase['data']['groups_count'] = 10
        self.result['cases'].append(testCase)
        # test 9
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #9: latest page 1 question blocks ordered by id DESC'
        testCase['data']['type'] = 'question block order'
        testCase['data']['key'] = 'list_latest_first'
        testCase['data']['mask'] = r'(\/question\/.*?\/)'
        testCase['data']['order_symbol'] = '%cur% <= %last%'
        testCase['data']['str_replace'] = ['/question/', '/']
        self.result['cases'].append(testCase)
        # test 10
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #10: latest page 2 question blocks ordered by id DESC'
        testCase['data']['type'] = 'question block order'
        testCase['data']['key'] = 'list_latest_second'
        testCase['data']['mask'] = r'(\/question\/.*?\/)'
        testCase['data']['order_symbol'] = '%cur% <= %last%'
        testCase['data']['str_replace'] = ['/question/', '/']
        self.result['cases'].append(testCase)
        # test 11
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #11: popular page 1 question blocks ordered by rating DESC'
        testCase['data']['type'] = 'question block order'
        testCase['data']['key'] = 'list_popular_first'
        testCase['data']['mask'] = r'(rating: .+)'
        testCase['data']['order_symbol'] = '%cur% <= %last%'
        testCase['data']['str_replace'] = ['rating: ']
        self.result['cases'].append(testCase)
        # test 12
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #12: popular page 2 question blocks ordered by rating DESC'
        testCase['data']['type'] = 'question block order'
        testCase['data']['key'] = 'list_popular_second'
        testCase['data']['mask'] = r'(rating: .+)'
        testCase['data']['order_symbol'] = '%cur% <= %last%'
        testCase['data']['str_replace'] = ['rating: ']
        self.result['cases'].append(testCase)
        # test 13
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #13: latest page 1 contain current page 1'
        testCase['data']['type'] = 'current page number selected'
        testCase['data']['key'] = 'list_latest_first'
        testCase['data']['mask'] = r'(<li class="active">\s*<a.*>1<\/a>\s*<\/li>)'
        self.result['cases'].append(testCase)
        # test 14
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #13: latest page 2 contain current page 2'
        testCase['data']['type'] = 'current page number selected'
        testCase['data']['key'] = 'list_latest_second'
        testCase['data']['mask'] = r'(<li class="active">\s*<a.*>2<\/a>\s*<\/li>)'
        self.result['cases'].append(testCase)
        # test 15
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #15: popular page 1 contain current page 1'
        testCase['data']['type'] = 'current page number selected'
        testCase['data']['key'] = 'list_popular_first'
        testCase['data']['mask'] = r'(<li class="active">\s*<a.*>1<\/a>\s*<\/li>)'
        self.result['cases'].append(testCase)
        # test 16
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #16: popular page 2 contain current page 2'
        testCase['data']['type'] = 'current page number selected'
        testCase['data']['key'] = 'list_popular_second'
        testCase['data']['mask'] = r'(<li class="active">\s*<a.*>2<\/a>\s*<\/li>)'
        self.result['cases'].append(testCase)
        # test 17
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #17: question page exists (id#MaxID)'
        testCase['data']['type'] = 'page exist'
        testCase['data']['request'] = 'http://localhost/question/%MaxID%/'
        testCase['data']['status_code'] = 200
        testCase['data']['key'] = 'question'
        self.result['cases'].append(testCase)
        # test 18
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #18: question page not exists (id#MaxID+1)'
        testCase['data']['type'] = 'page exist'
        testCase['data']['request'] = 'http://localhost/question/%MaxID+1%/'
        testCase['data']['status_code'] = 404
        testCase['data']['key'] = 'noquestion'
        self.result['cases'].append(testCase)
        # test 19
        testCase = self.__getTestCase__()
        testCase['title'] = 'Test #19: check question page (id#MaxID)'
        testCase['data']['type'] = 'check question'
        testCase['data']['key'] = 'question'
        testCase['data']['mask_answers'] = r'(<div class="answer_box">(\s|.|^[div>])*?\/div>)'
        self.result['cases'].append(testCase)

    def load(self):
        random.seed()
        sys.path.insert(0, os.getcwd() + '/ask')
        from django.core.wsgi import get_wsgi_application
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask.settings')
        application = get_wsgi_application()
        from qa.models import Question
        from qa.models import Answer
        self.moduleVar = __import__('qa.models')
        self.djangoTestModels = list()
        # create users
        from django.contrib.auth.models import User
        usersList = list()
        for cnt in range(1, 25):
            newUser = User()
            newUser.username = 'User #' + str(cnt)
            newUser.first_name = 'Name #' + str(cnt)
            newUser.last_name = 'Surname #' + str(cnt)
            newUser.save()
            self.djangoTestModels.append(newUser)
            usersList.append(newUser)
        # create questions
        for cnt in range(1, 25):
            newQuestion = Question()
            newQuestion.title = 'Question #' + str(cnt)
            newQuestion.text = 'Question #' + str(cnt) + ' text:' + self.__getRandomLines__()
            newQuestion.rating = random.randint(1, 100)
            newQuestion.added_at = datetime.date(2021, 1, cnt)
            random.shuffle(usersList)
            newQuestion.author = usersList[0]
            newQuestion.save()
            newQuestion.likes.add(*usersList[1:random.randint(1, 5)])
            newQuestion.save()
            self.question_max_id = newQuestion.id
            self.djangoTestModels.append(newQuestion)
            # create answers for current question
            for cnt1 in range(1, random.randint(1, 10)):
                newAnswer = Answer()
                newAnswer.text = 'Answer # ' + str(cnt1) + 'for question #' + str(cnt)
                newAnswer.text += ', text:' + self.__getRandomLines__()
                newAnswer.question = newQuestion
                newAnswer.added_at = datetime.date(2021, 1, cnt)
                random_user_index = random.randint(1, 23)
                #print('userlist len=' + str(len(usersList)) + '|random user index:' + str(random_user_index))
                newAnswer.author = usersList[random_user_index]
                newAnswer.save()
                self.djangoTestModels.append(newAnswer)

    def test(self):
        for testCase in self.result['cases']:
            eval_line = 'self.__test_' + str(testCase['data']['type']).replace(' ', '_') + '__(testCase)'
            #print('-----eval_line:' + eval_line)
            eval(eval_line)
        return self.result

    def unload(self):
        try:
            for curModel in self.djangoTestModels:
                curModel.delete()
        except Exception as ErrorObject:
            self.load_error += '\n[ERROR] - unload - django model delete error: ' + str(ErrorObject)

    def __test_page_exist__(self, testCase):
        #print('---key:' + testCase['data']['key'])
        try:
            request = str(testCase['data']['request'])
            request = request.replace('%MaxID%', str(self.question_max_id))
            request = request.replace('%MaxID+1%', str(self.question_max_id + 1))
            response = requests.get(request)
            testCase['out'].append(' - test - request:' + testCase['data']['request'])
            if response.status_code == testCase['data']['status_code']:
                self.test_data[testCase['data']['key']] = response.text
                testCase['out'].append(' - test - Success')
                testCase['success'] = True
                self.result['success'] += 1
                #print('---key:' + testCase['data']['key'] + ' OK')
            else:
                testCase['out'].append(' - test - Fail')
                testCase['error'].append(' - test - request:' + testCase['data']['request'])
                #print('---key:' + testCase['data']['key'] + ' FAIL')
                error_line = ' - test - status code:' + str(response.status_code)
                error_line += '| expected:' + str(testCase['data']['statusCode'])
                testCase['error'].append(error_line)
                error_line = ' - test - text:' + response.text
                error_line += '| expected:' + testCase['data']['fileContent']
                testCase['error'].append(error_line)
        except:
            testCase['out'].append(' - test - Fail')
            testCase['error'].append(' - test - request:' + testCase['data']['request'])
            testCase['error'].append(' - test - error:' + str(traceback.format_exc()))

    def __test_question_block_count__(self, testCase):
        #print('test_data key:' + testCase['data']['key'])
        #print('test data by key:' + str(self.test_data.get(testCase['data']['key'])))
        test_data = self.test_data[testCase['data']['key']]
        blocks = re.findall(testCase['data']['mask'], test_data)
        if len(blocks) == testCase['data']['groups_count']:
            testCase['out'].append(' - test - Success')
            testCase['success'] = True
            self.result['success'] += 1
        else:
            testCase['out'].append(' - test - Fail')
            testCase['error'].append(' - test - mask:' + testCase['data']['mask'])
            error_line = ' - test - count:' + str(len(blocks))
            error_line += '|expected:' + str(testCase['data']['groups_count'])
            testCase['error'].append(error_line)
            testCase['error'].append(' - test - test data:' + test_data)

    def __test_question_block_order__(self, testCase):
        test_data = self.test_data[testCase['data']['key']]
        blocks = re.findall(testCase['data']['mask'], test_data)
        lastValue = None
        for block in blocks:
            block_value = block
            for str_replace in testCase['data']['str_replace']:
                block_value = str(block_value).replace(str_replace, '')
            block_value_int = int(block_value)
            if not lastValue is None:
                order_value_line = str(testCase['data']['order_symbol'])
                order_value_line = order_value_line.replace('%cur%', 'block_value_int')
                order_value_line = order_value_line.replace('%last%', 'lastValue')
                current_value = bool(eval(order_value_line))
                if not current_value:
                    testCase['out'].append(' - test - Fail')
                    testCase['error'].append(' - test - mask:' + testCase['data']['mask'])
                    testCase['error'].append(' - test - test data:' + test_data)
                    return
            lastValue = block_value_int
        # if we are here - it is success
        testCase['out'].append(' - test - Success')
        testCase['success'] = True
        self.result['success'] += 1

    def __test_current_page_number_selected__(self, testCase):
        testCase['out'].append(' - test - Skipped')
        test_data = self.test_data[testCase['data']['key']]
        blocks = re.findall(testCase['data']['mask'], test_data)
        if len(blocks) == 1:
            testCase['out'].append(' - test - Success')
            testCase['success'] = True
            self.result['success'] += 1
        else:
            testCase['out'].append(' - test - Fail')
            testCase['error'].append(' - test - mask:' + testCase['data']['mask'])
            error_line = ' - test - count:' + str(len(blocks))
            error_line += '|expected:1'
            testCase['error'].append(error_line)
            testCase['error'].append(' - test - test data:' + test_data)

    def __test_check_question__(self, testCase):
        test_data = self.test_data[testCase['data']['key']]
        testCase['out'].append(' - test - question id:' + str(self.question_max_id))
        from qa.models import Question
        questionObject = Question.objects.get(pk=self.question_max_id)
        result = True
        # check title
        title_mask = r'.*' + questionObject.title + '.*'
        if re.search(title_mask, test_data) is None:
            result = False
            testCase['error'].append(' - test - question title not found by mask:' + title_mask)
        # check text
        text_mask = r'.*' + questionObject.text + '.*'
        if re.search(text_mask, test_data) is None:
            result = False
            testCase['error'].append(' - test - question text not found by mask:' + text_mask)
        # check answers count
        blocks = re.findall(testCase['data']['mask_answers'], test_data)
        question_answers = questionObject.answer_set.all()
        if len(blocks) != len(question_answers):
            result = False
            error_line = ' - test - answer count in html:' + str(len(blocks))
            error_line += '|expected (count in base):' + str(len(question_answers))
            testCase['error'].append(error_line)
        if result:
            testCase['out'].append(' - test - Success')
            testCase['success'] = True
            self.result['success'] += 1
        else:
            testCase['out'].append(' - test - Fail')
            testCase['error'].append(' - test - test data:' + test_data)

    def __getRandomLines__(self):
        result = self.__getRandomLine__()
        for cntText in range(1, random.randint(1, 3)):
            result += '\n' + self.__getRandomLine__()
        return result

    def __getRandomLine__(self):
        result = ''
        for cntText in range(1, random.randint(1, 8)):
            result += ' '
            from string import ascii_letters
            currChar = ascii_letters[random.randint(0, len(ascii_letters) - 1)]
            for cntText1 in range(1, random.randint(1, 10)):
                result += currChar
        return result

def getTestObject():
    return test_2_5_8()

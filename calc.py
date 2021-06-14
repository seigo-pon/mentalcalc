import boto3
import datetime
import json
import os
import random
import uuid

class CalcQuestion:
    first = 0
    second = 0
    is_correct = False
    incorrect_num = 0

    def __init__(self, dict_data=None):
        if dict_data is not None:
            self.first = dict_data['first']
            self.second = dict_data['second']
            self.is_correct = dict_data['is_correct']
            self.incorrect_num = dict_data['incorrect_num']

    def toDict(self):
        return {
            'first': self.first,
            'second': self.second,
            'is_correct': self.is_correct,
            'incorrect_num': self.incorrect_num,
        }

class CalcResult:
    max_number = 20
    operate = ''
    question_list = []

    def __init__(self, dict_data=None):
        if dict_data is not None:
            self.max_number = dict_data['max_number']
            self.operate = dict_data['operate']
            self.question_list = [CalcQuestion(question) for question in dict_data['question_list']]

    def toDict(self):
        return {
            'max_number': self.max_number,
            'operate': self.operate,
            'question_list': [question.toDict() for question in self.question_list],
        }

    def num(self):
        return len(self.question_list)

    def is_start(self, max_num):
        return self.num() > 0 and self.num() < max_num

    def last_question(self):
        return self.question_list[-1] if self.num() > 0 else None

    def update_last_question(self, question):
        if self.num() > 0:
            self.question_list[-1] = question

    def correct_num(self):
        correct_question_list = list(filter(lambda x: x.is_correct, self.question_list))
        return len(correct_question_list)

def get_calc_max():
    return 10

def get_calc_incorrect_max():
    return 2

def get_calc_max_number():
    # max_number = random.randint(1, 2) * 10
    max_number = 10
    print('max_number', max_number)
    return max_number

def get_calc(max_number, operate):
    if operate == '足す':
        first = random.randint(1, max_number)
        second = random.randint(1, 9)
        return (first, second)
    else:
        first = random.randint(1, max_number)
        second = random.randint(1, first if first < 9 else 9)
        return (first, second)

def correct_answer(first, second, operate):
    if operate == '足す':
        return (first + second)
    else:
        return (first - second)

def save_result(result):
    table_name = os.environ['RESULT_TABLE_NAME']

    try:
        dynamoDB = boto3.resource("dynamodb")
        table = dynamoDB.Table(table_name)

        table.put_item(
            Item = {
                "uid": str(uuid.uuid4()),
                "created_at": int(datetime.datetime.now().timestamp() * 1000),
                "result": json.dumps(result.toDict())
            }
        )
    except Exception as e:
        print('save_result error', e)

import random

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
    base = 1
    operate = ''
    question_list = []

    def __init__(self, dict_data=None):
        if dict_data is not None:
            self.base = dict_data['base']
            self.operate = dict_data['operate']
            self.question_list = [CalcQuestion(question) for question in dict_data['question_list']]

    def toDict(self):
        return {
            'base': self.base,
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

def get_calc_base():
    base = random.randint(0, 3) * 10
    return base

def get_calc(base, operate):
    if operate == '足す':
        first = random.randint(base+1, base+10)
        second = random.randint(1, 9)
        return (first, second)
    else:
        first = random.randint(base+1, base+10)
        second = random.randint(1, first if first < 9 else 9)
        return (first, second)

def correct_answer(first, second, operate):
    if operate == '足す':
        return (first + second)
    else:
        return (first - second)

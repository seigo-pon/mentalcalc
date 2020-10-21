import random

class CalcResult:
    base = 1
    operate = ''
    first = 0
    second = 0
    num = 0
    correct_num = 0

    def __init__(self, dict_data=None):
        if dict_data is not None:
            self.base = dict_data['base']
            self.operate = dict_data['operate']
            self.first = dict_data['first']
            self.second = dict_data['second']
            self.num = dict_data['num']
            self.correct_num = dict_data['correct_num']

    def toDict(self):
        return {
            'base': self.base,
            'operate': self.operate,
            'first': self.first,
            'second': self.second,
            'num': self.num,
            'correct_num': self.correct_num,
        }

def get_calc_max():
    return 10

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

def is_correct(first, second, operate, answer):
    if operate == '足す':
        return (first + second) == answer
    else:
        return (first - second) == answer

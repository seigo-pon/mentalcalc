from calc import (
    CalcQuestion, CalcResult,
    get_calc_max, get_calc_incorrect_max, get_calc_max_number, get_calc, correct_answer
)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import get_slot_value, is_intent_name, is_request_type
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

sb = SkillBuilder()

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    speech_text = "暗算を始めますか? (はい/いいえ)"
    handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Mental Calc", speech_text)).set_should_end_session(False)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("QuestionIntent"))
def question_intent_handler(handler_input):
    yes_no = get_slot_value(handler_input=handler_input, slot_name="continue")
    session_attr = handler_input.attributes_manager.session_attributes
    print('question_intent_handler', session_attr)

    if yes_no == 'はい':
        if not ('result' in session_attr):
            session_attr['result'] = CalcResult().toDict()

        result = CalcResult(session_attr['result'])
        if result.is_start(get_calc_max()):
            speech_text = '聞こえませんでした！ もう一度お願いします！'
            end_session = False
        else:
            result.max_number = get_calc_max_number()
            result.question_list = []
            session_attr['result'] = result.toDict()

            speech_text = '足し算にしますか、引き算にしますか? (足し算/引き算)'
            end_session = False
    elif yes_no == 'いいえ':
        speech_text = "また今度お会いしましょう！"
        end_session = True
    else:
        speech_text = "もう一回言ってください！"
        end_session = False

    handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Mental Calc", speech_text)).set_should_end_session(end_session)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("OperationIntent"))
def operation_intent_handler(handler_input):
    plus_minus = get_slot_value(handler_input=handler_input, slot_name="operation")
    session_attr = handler_input.attributes_manager.session_attributes
    print('operation_intent_handler', session_attr)

    if not ('result' in session_attr):
        speech_text = "暗算を始めますか? (はい/いいえ)"
        end_session = False
    else:
        result = CalcResult(session_attr['result'])
        if result.is_start(get_calc_max()):
            speech_text = '聞こえませんでした！ もう一度お願いします！'
            end_session = False
        elif (plus_minus == '足し算') or plus_minus == '引き算':
            result.operate = '足す' if plus_minus == '足し算' else '引く'
            question = CalcQuestion()
            question.first, question.second = get_calc(result.max_number, result.operate)
            result.question_list.append(question)
            session_attr['result'] = result.toDict()

            speech_text = 'わかりました！最初の問題です。{}{}{}は？'.format(
                question.first,
                result.operate,
                question.second
            )
            end_session = False
        else:
            speech_text = '聞こえませんでした！ もう一度お願いします！'
            end_session = False

    handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Mental Calc", speech_text)).set_should_end_session(end_session)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("AnswerIntent"))
def answer_intent_handler(handler_input):
    answer = get_slot_value(handler_input=handler_input, slot_name="answer")
    session_attr = handler_input.attributes_manager.session_attributes
    print('answer_intent_handler', session_attr)

    if not ('result' in session_attr):
        speech_text = "暗算を始めますか? (はい/いいえ)"
        end_session = False
    else:
        result = CalcResult(session_attr['result'])
        question = result.question_list[-1]

        try:
            answer_num = int(answer)
            correct = correct_answer(question.first, question.second, result.operate)
            if correct == answer_num:
                speech_text = '正解です！'
                question.is_correct = True
            else:
                speech_text = '違います！'
                question.incorrect_num += 1
            result.update_last_question(question)
            session_attr['result'] = result.toDict()

            one_more = False
            answer_text = ''
            if not question.is_correct:
                if question.incorrect_num < get_calc_incorrect_max():
                    one_more = True
                else:
                    speech_text = '{}正解は{}です。'.format(speech_text, correct)

            if one_more:
                speech_text = '{}もう一度お答えください。{}{}{}は？'.format(
                    speech_text,
                    question.first,
                    result.operate,
                    question.second
                )
                end_session = False
            elif result.num() < get_calc_max():
                question = CalcQuestion()
                question.first, question.second = get_calc(result.max_number, result.operate)
                result.question_list.append(question)
                session_attr['result'] = result.toDict()

                if result.num() == get_calc_max():
                    speech_text = '{}最後の問題です。{}{}{}は？'.format(
                        speech_text,
                        question.first,
                        result.operate,
                        question.second
                    )
                else:
                    speech_text = '{}次は{}問目です。{}{}{}は？'.format(
                        speech_text,
                        result.num(),
                        question.first,
                        result.operate,
                        question.second
                    )
                end_session = False
            else:
                speech_text = '{}あなたは{}問正解でした！今日はここまで。また今度お会いしましょう！'.format(
                    speech_text,
                    result.correct_num()
                )
                end_session = True

            session_attr['result'] = result.toDict()

        except Exception as e:
            print(e)
            speech_text = '聞こえませんでした！ もう一度お願いします！'
            end_session = False

    handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Mental Calc", speech_text)).set_should_end_session(end_session)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    speech_text = "こんにちは。と言ってみてください。"
    handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(SimpleCard("Mental Calc", speech_text))
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=lambda handler_input:is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    speech_text = "また今度お会いしましょう！"
    handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Mental Calc", speech_text))
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    return handler_input.response_builder.response

@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    print(exception)
    speech = "すみません、わかりませんでした。もう一度言ってください！"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response

handler = sb.lambda_handler()

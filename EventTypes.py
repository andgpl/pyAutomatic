#! /usr/bin/pyhton3

from Base.Enumeration   import Enumeration



class AssertTypes(Enumeration):

    INFO        = 10
    WARNING     = 11
    ERROR       = 12
    EXCEPTION   = 13
    ASSERT_PASS = 14
    ASSERT_FAIL = 15


class StartTypes(Enumeration):
    
    TESTSTEP_START    = 20
    TESTCASE_START    = 21
    TESTCASE_SETUP    = 22
    TESTCASE_TEARDOWN = 23
    TESTSUITE_START   = 24


class EndTypes(Enumeration):

    TESTSTEP_END  = 30
    TESTCASE_END  = 31
    TESTSUITE_END = 32


class ResultTypes(Enumeration):

    TESTSTEP_PASS         = 40
    TESTSTEP_FAIL         = 41
    TESTSTEP_PASS_WARNING = 42
    TESTCASE_PASS         = 43
    TESTCASE_FAIL         = 44
    TESTSUITE_PASS        = 45
    TESTSUITE_FAIL        = 46


class EventType(AssertTypes, StartTypes, EndTypes, ResultTypes):
    pass


class ListEnum(Enumeration, basetype = tuple):

    VAL = [1, 2, 3]


if __name__ == "__main__":

    print()
    print(EventType)
    print(AssertTypes.INFO == EventType.INFO)
    print(isinstance(AssertTypes.INFO, EventType))
    print(float(AssertTypes.WARNING))
    print(30 - AssertTypes.INFO)
    
    print(ListEnum.VAL)


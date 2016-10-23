#! /usr/bin/python3

from enum import IntEnum, unique


@unique
class EventType(IntEnum):

    """
    General Events
    """
    INFO      = 1
    WARNING   = 2
    ERROR     = 3
    EXCEPTION = 4
    
    
    """
    Test Events
    """
    ASSERT_PASS = 10
    ASSERT_FAIL = 11
    
    TESTSTEP_START        = 20
    TESTSTEP_END          = 21
    TESTSTEP_PASS         = 22
    TESTSTEP_FAIL         = 23
    TESTSTEP_PASS_WARNING = 24

    TESTCASE_SETUP    = 40
    TESTCASE_TEARDOWN = 41
    TESTCASE_START    = 42
    TESTCASE_END      = 43
    TESTCASE_PASS     = 44
    TESTCASE_FAIL     = 45

    TESTSUITE_START = 60
    TESTSUITE_END   = 61
    TESTSUITE_PASS  = 62
    TESTSUITE_FAIL  = 63


    """
    Log events
    """
    LOG = 100       # Write a plain string to the log

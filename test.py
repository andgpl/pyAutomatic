from Test.Teststep  import Teststep
from Test.Testcase  import Testcase
from Test.Testsuite import Testsuite
from Base.Event     import Event
from Base.EventType import EventType

print(Teststep)
print(Testcase)
print(Testsuite)


e = Event(EventType.LOG, "log this!")
print(e)



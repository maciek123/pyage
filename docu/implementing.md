Implementing your own components
===

Pyage is highly flexible so you are welcome to implement new components.

Suppose that you want to customize statistics collected during simulation and receive them via SMS. You should then implement [this component](https://github.com/maciek123/pyage/blob/master/pyage/core/statistics.py). It is very simple and has only two methods:

- update, called after every step
- summarize, called when computations are done

In our case it may be for example:
```
from pyage.core.statistics import Statistics

class SmsStatistics(Statistics):
    def update(self, step_count, agents):
        pass #do nothing

    def summarize(self, agents):
        msg = "computation finished" # add more details here if needed
        self.__send_sms(msg, YOUR_PHONE_NR)

    def __send_sms(msg, nr):
         #SMS sending logic here
```
and then our new sms statistics module can be use in configuration file: ```stats = SmsStatistics```
 

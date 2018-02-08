
"""
4 types of unittest.TestCase assertions to confirm that 
/proc/driver/rtc keeps good time.
"""

import unittest

from datetime import datetime, timedelta


""" feature = rtc_time or rtc_date """

def open_rtc(feature):
    with open('/proc/driver/rtc') as myfile:
    
        """ splitting rtc file contents into array of strings """ 
        data = myfile.read().split()
    
    myindex = data.index(feature)

    """ rtc_time & rtc_date contents are located 2 indexes afterwards """ 
    return data[myindex+2]


now = datetime.utcnow()
result1 = open_rtc('rtc_date')
result2 = open_rtc('rtc_time')
combined = result1 + " " + result2


class TestAdd(unittest.TestCase):

    def test_compare_time(self):
        """ Tests that rtc_time matches current UTC time """
        self.assertEqual(result2, now.strftime("%H:%M:%S"))

    def test_compare_date(self):
        """ Tests that rtc_date matches current UTC date """
        self.assertEqual(result1, now.strftime("%Y-%m-%d"))

    def test_9hrs_59mins_59secs_later(self):
        """ Tests that 09:59:59 later, rtc_time & rtc_date = UTC time """
        timechange = timedelta(hours=9, minutes=59, seconds=59)
        later = datetime.strptime(combined, "%Y-%m-%d %H:%M:%S") + timechange
        tenhrs_later = (now + timechange)
        self.assertEqual(later.strftime("%H:%M:%S"), 
            tenhrs_later.strftime("%H:%M:%S"))
        self.assertEqual(later.strftime("%Y-%m-%d"), 
            tenhrs_later.strftime("%Y-%m-%d"))

    def test_1day_9hr_59mins_59secs_later(self):
        """ Tests that 1 day and 09:59:59 later, rtc_time & rtc_date = UTC time """
        timechange = timedelta(days=1, hours=9, minutes=59, seconds=59)
        later = datetime.strptime(combined, "%Y-%m-%d %H:%M:%S") + timechange
        oneday_later = (now + timechange)
        self.assertEqual(later.strftime("%H:%M:%S"), 
            oneday_later.strftime("%H:%M:%S"))
        self.assertEqual(later.strftime("%Y-%m-%d"), 
            oneday_later.strftime("%Y-%m-%d"))


if __name__ == '__main__':
    unittest.main()


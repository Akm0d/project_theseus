
# Constant to indicate that you have entered a failed state
DEATH = -1

# COnstant to indicate that function ran without issue
SUCCESS = 0

class Timer():
    """
    Holds the information about the timer in a single class.  Provides functions
    to facilitate ease of use by the webserver.
    """
    def __init__(self, timeInMinutes):
        self.initialValue = timeInMinutes
        self.minutes = timeInMinutes
        self.seconds = 0
        self.tenthSeconds = 0

    # Reset time in timer to what the intial value was set to.
    def reset(self):
        self.minutes = self.initialValue
        self.seconds = 0
        self.tenthSeconds = 0

    # Flag to check if the user has run out of time
    def outOfTime(self):
        return (self.minutes == 0 and self.seconds == 0 and self.tenthSeconds == 0)

    # Decrement the time by a minute
    def decrementMinute(self):
        if (self.minutes == 0):
            return DEATH
        else:
            self.minutes = self.minutes - 1
            return SUCCESS

    # Decrement the time by a second
    def decrementSecond(self):
        # Decrement seconds
        if (self.seconds == 0):
            if self.minutes != 0:
                self.seconds = 59

            # Decrement Minutes
            return self.decrementMinute()
        else:
            # A full minute has not passed, so only decrement seconds
            self.seconds = self.seconds - 1
            return SUCCESS

    # Decrement the time by a tenth of a second
    def decrementTenthSecond(self):

        # Decrement tenthSeconds
        if (self.tenthSeconds == 0):
            self.tenthSeconds = 9

            self.decrementSecond()
        else:
            # Decrement the tenthSecond counter
            self.tenthSeconds = self.tenthSeconds - 1

            # Check if timer has finished
            if (self.tenthSeconds == 0 and self.seconds == 0 and self.minutes == 0):
                # Players have failed, the timer ran out of time
                return DEATH

        # Decremented but timer is not finished
        return SUCCESS

    def sprintTimer(self):
        return '%(minutes)02d:%(seconds)02d:%(tenthSeconds)d' % {'minutes': self.minutes,
                                                             'seconds': self.seconds,
                                                             'tenthSeconds': self.tenthSeconds
                                                             }

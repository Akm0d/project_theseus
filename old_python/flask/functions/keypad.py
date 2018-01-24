from random import choice
"""
The purpose of this file is to hold the classes and functions
necessary to allow the keypad to function.  This includes
generating a new set of keys and commands to see them.
"""

OLD_CHOICES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
CHOICES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
class Keypad():

    def __init__(self):
        self.combo = [choice(OLD_CHOICES), choice(OLD_CHOICES), choice(OLD_CHOICES)]

    # Generate a new set of random keys to press
    def generateKeys(self, switchValue):
        firstOne = ord(choice(OLD_CHOICES)) - ord('A')

        # Ensure that the first switch value is not the same as the current
        # switch value
        if switchValue is not None:
            switchValue = ord(switchValue) - ord('A')

            while(firstOne == switchValue):
                firstOne = ord(choice(OLD_CHOICES)) - ord('A')

        self.combo = [firstOne, ord(choice(OLD_CHOICES))- ord('A'), ord(choice(OLD_CHOICES)) - ord('A')]
        return 0

    # Get value of specified key
    def getKey(self, index):
        if (index <= 2 and index >= 0):
            return self.combo[index]
        else:
            # This is an error, as there are only 3 numbers
            return -1

    # Set values of combo
    def setCombo(self, newCombo):
        if (newCombo[0] >= 0 and
            newCombo[0] <= 15 and
            newCombo[1] >= 0 and
            newCombo[1] <= 15 and
            newCombo[2] >= 0 and
            newCombo[2] <= 15):
            self.combo = [newCombo[0], newCombo[1], newCombo[2]]
            return 0
        else:
            return -1

    # Checks that key pressed is the correct one for that index
    def checkKey(self, keystroke, index):
        return self.combo[index] == keystroke

    def checkCombo(self, entryQueue):
        if len(entryQueue) < 3:
            return False
        elif len(entryQueue) == 3:
            print("Proper Length, Check values")
            # print("Expecting %(first)s, %(second)s, %(third)s" % {'first': ord(self.combo[0]) - ord('A'),
            #                                                       'second': ord(self.combo[1]) - ord('A'),
            #                                                       'third': ord(self.combo[2]) - ord('A')
            #                                                       })
            convertQueue = list()
            convertQueue.append(int(entryQueue[0], 16))
            convertQueue.append(int(entryQueue[1], 16))
            convertQueue.append(int(entryQueue[2], 16))

            print("Expecting %(first)s, %(second)s, %(third)s" % {'first': self.combo[0],
                                                                  'second': self.combo[1],
                                                                  'third': self.combo[2]
                                                                  })
            print("Pre %(first)s, %(second)s, %(third)s" % {'first': entryQueue[0],
                                                            'second': entryQueue[1],
                                                            'third': entryQueue[2]
                                                            })
            print("Raw %(first)s, %(second)s, %(third)s" % {'first': convertQueue[0],
                                                            'second': convertQueue[1],
                                                            'third': convertQueue[2]
                                                            })
            return self.checkKey(convertQueue[0], 0) and self.checkKey(convertQueue[1], 1) and self.checkKey(convertQueue[2], 2)
        else:
            print("TOO BIG")
            # Queue is too big
            return False

    # get a string of the combination
    def sprintCombo(self):
        return '(%(first)s, %(second)s, %(third)s)' % {'first': self.combo[0],
                                                       'second': self.combo[1],
                                                       'third': self.combo[2]
                                                       }

    # Print the current code to the terminal
    def printCombo(self):
        print (self.sprintCombo())

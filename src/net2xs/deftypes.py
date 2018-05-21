"""
Module holding definition data types
"""


class TimeSlot(object):
    """Time zone slot definition

    Member id: Timeslot id
    Member day: Timeslot day number
    Member start_time: Start time of slot
    Member start_time: End time of slot
    """
    def __init__(self, id=-1, day=-1, start_time=None, end_time=None):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.day = day

    def __eq__(self, other):
        """Compare
        """
        return (
            self.start_time == other.start_time and
            self.end_time == other.end_time and
            self.day == other.day)

    def __ne__(self, other):
        """Compare negative
        """
        return not self.__eq__(other)

    def __str__(self):
        return ('%s id=%d, day=%d, start_time=%s, end_time=%s' %
                (self.__class__.__name__,
                 self.id, self.day, self.start_time, self.end_time))


class TimeZone(object):
    """Time zone definition

    Member id: Timezone id
    Member name: Timezone name
    Member slots: Array of TimeSlot objects
    """
    def __init__(self, id=-1, name=None):
        self.id = id
        self.name = name
        self.slots = []

    def __eq__(self, other):
        """Compare
        """
        if (type(self) != type(other) or
                len(self.slots) != len(other.slots)):
            return False

        for s_slot in self.slots:
            for o_slot in other.slots:
                if s_slot == o_slot:
                    break
            else:
                return False

        return True

    def __ne__(self, other):
        """Compare negative
        """
        return not self.__eq__(other)

    def __str__(self):
        out = []
        out.append('%s id=%d, name=%s' %
                   (self.__class__.__name__, self.id, self.name))
        for slot in self.slots:
            out.append('-%s' % slot)
        return '\n'.join(out)


class AccessLevel(object):
    """Access level definition

    Member id: Accesslevel id
    Member name: Accesslevel name
    Member details: Array of (timezone id, area id) tuples
    """
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.details = []

    def __eq__(self, other):
        """Compare
        """
        if (type(self) != type(other) or
                len(self.details) != len(other.details)):
            return False

        for s_detail in self.details:
            for o_detail in other.details:
                if s_detail == o_detail:
                    break
            else:
                return False

        return True

    def __ne__(self, other):
        """Compare negative
        """
        return not self.__eq__(other)

    def __str__(self):
        out = []
        out.append('%s id=%d, name=%s' % (
            self.__class__.__name__, self.id, self.name))
        for tz_id, area_id in self.details:
            out.append('-tz=%d, area=%d' % (tz_id, area_id))
        return '\n'.join(out)

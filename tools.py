class PasswordFrequency:
    MILLI_SECOND = 'millisecond'
    SECOND = 'second'
    MINUTE = 'minute'
    HOUR = 'hour'
    DAY = 'day'
    MONTH = 'month'
    YEAR = 'year'

    def get_truncate_length(self, fr):
        if fr == self.MILLI_SECOND:
            return 26
        elif fr == self.SECOND:
            return 19
        elif fr == self.MINUTE:
            return 16
        elif fr == self.HOUR:
            return 13
        elif fr == self.DAY:
            return 10
        elif fr == self.MONTH:
            return 7
        elif fr == self.YEAR:
            return 4

class PasswordStyle:
    ALL_RANDOM = 'all_random'
    TWO_ALTERNATE = 'two_alternate'
    FOUR_ALTERNATE = 'four_alternate'

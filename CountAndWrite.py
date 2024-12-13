import classes      # Drivers and logic standpoint
import math         # Points logic, just for log, can use norms without this
import random       # Genetic algorythm
import copy         # Workaround to back up timeshift when shit hits the fan
import time


class AlgorythmTimetable:
    def __init__(self, shift_table: classes.ShiftTimetable, shift_name="Basic"):
        shift_table.shift_name = shift_name
        self.shift_table = shift_table
        self.TICKS_PER_HOUR = 6
        self.WORK_START = 6 * self.TICKS_PER_HOUR
        self.WORK_END = self.WORK_START + 21 * self.TICKS_PER_HOUR
        self.HIGH_TIME_START = 7 * self.TICKS_PER_HOUR
        self.HIGH_TIME_END = self.HIGH_TIME_START + self.TICKS_PER_HOUR * 2
        self.WORK_HOURS = 21
        self.ROUTE_TIME = int(self.TICKS_PER_HOUR)
        self.ROUTE_TIME_TICKS = 6
        self.TYPE_A_TIME = 8
        self.TYPE_B_TIME = 12
        self.timestamp_A1 = self.TICKS_PER_HOUR * 6 + 2 * int(self.TICKS_PER_HOUR / 6)  # Start at WS       DIN at HTE
        self.timestamp_A2 = self.timestamp_A1 + self.TICKS_PER_HOUR * 6 + 1             # Start at B1 break DIN at WTE - 2
        self.timestamp_A3 = self.timestamp_A1 + int(self.ROUTE_TIME / 2)                # Start at WS+RT/2  DIN at HTE + 2 Route
        self.timestamp_B1 = self.HIGH_TIME_START                                        # Start at HTS 1 - 1/2 h
        self.timestamp_B2 = self.HIGH_TIME_END + int(self.TICKS_PER_HOUR * 7.5)         # Start at HTS 2 - 1/2 h
        self.timestamp_B3 = self.HIGH_TIME_START + self.TICKS_PER_HOUR * 12 - 1         # Start at HT2 - Route / 2
        self.timestamp_weekend_1 = (self.WORK_HOURS + self.WORK_START - self.TYPE_B_TIME) * self.TICKS_PER_HOUR     # Start at end time - 12
        self.timestamp_weekend_2 = self.WORK_START * self.TICKS_PER_HOUR                # Start at day start
        self.timestamp_weekend_3 = self.TICKS_PER_HOUR * 12                             # Start at 12 AM / 0 PM

    def rph(self, minutes, A=None):   # Under X minutes on route routine
        if A is None:
            return int(minutes / 60 * self.ROUTE_TIME)
        else:
            return int(minutes / 60 * self.ROUTE_TIME) - int(minutes / 60 * self.ROUTE_TIME % self.ROUTE_TIME_TICKS)

    # Also workday_algo restructures current progress instead of returning it so don't use unless starting or redoing
    # Dumb as a rock, makes base for genetic algorythm
    def workday_algorythm(self, workers):   # Done: checks for end of the day or ticks
        a = 0
        b = 0
        for driver in workers:
            if driver.work_type == "A" and a % 3 == 0:  # Worker Type A1
                driver.work_start = self.timestamp_A1
                driver.timetable.append("going_en_route")
                for i in range(self.rph(240, A=True)):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(6):
                    driver.timetable.append("waiting")
                driver.timetable.append("going_en_route")
                for i in range(self.rph(160, A=True)):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                a += 1
            elif driver.work_type == "A" and a % 3 == 1:  # Worker Type A2 (xls file for reference)
                driver.work_start = self.timestamp_A2
                driver.timetable.append("going_en_route")
                for i in range(self.rph(360, A=True)):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(6):
                    driver.timetable.append("waiting")
                a += 1
            elif driver.work_type == "A" and a % 3 == 2:  # Worker Type A3
                driver.work_start = self.timestamp_A3
                driver.timetable.append("going_en_route")
                for i in range(self.rph(320, A=True)):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(6):
                    driver.timetable.append("waiting")
                a += 1
                driver.timetable.append("going_en_route")
                for i in range(self.rph(100, A=True)):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
            elif driver.work_type == "B" and b % 3 == 2:  # Worker Type B1
                driver.work_start = self.timestamp_B1
                driver.timetable.append("going_en_route")
                for i in range(self.rph(300, A=True)):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(9):
                    driver.timetable.append("waiting")
                driver.timetable.append("going_en_route")
                for i in range(self.rph(180)):
                    driver.timetable.append("en_route")
                for i in range(2):
                    driver.timetable.append("waiting")
                for i in range(self.rph(90)):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                b += 1
            elif driver.work_type == "B" and b % 3 == 0:  # Worker Type B2
                driver.work_start = self.timestamp_B2
                driver.timetable.append("going_en_route")
                for i in range(self.rph(300, A=True)):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(self.rph(60)):
                    driver.timetable.append("waiting")
                driver.timetable.append("going_en_route")
                for i in range(self.rph(120)):
                    driver.timetable.append("en_route")
                for i in range(self.rph(45)):
                    driver.timetable.append("waiting")
                for i in range(self.rph(70)):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                b += 1
            elif driver.work_type == "B" and b % 3 == 1:  # Worker Type B3
                driver.work_start = self.timestamp_B3
                driver.timetable.append("going_en_route")
                for i in range(self.rph(240, A=True)):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(self.rph(75)):
                    driver.timetable.append("waiting")
                driver.timetable.append("going_en_route")
                for i in range(self.rph(130)):
                    driver.timetable.append("en_route")
                driver.timetable.append("waiting")
                driver.timetable.append("returning")
                b += 1

    def weekend_algorythm(self, workers):   # DONE: transition all checkpoint from xls
        b = 0
        for driver in workers:
            if driver.work_type == "B" and b % 5 == 0:  # Worker Type B1
                driver.work_start = self.timestamp_weekend_2
                driver.timetable()
            if driver.work_type == "B" and b % 5 == 1:  # Worker Type B1
                driver.work_start = self.timestamp_weekend_1
                driver.timetable()
            if driver.work_type == "B" and b % 5 == 2:  # Worker Type B1
                driver.work_start = self.timestamp_weekend_3
                driver.timetable()
            if driver.work_type == "B" and b % 5 == 3:  # Worker Type B1
                driver.work_start = self.timestamp_weekend_1
                driver.timetable()
            if driver.work_type == "B" and b % 5 == 4:  # Worker Type B1
                driver.work_start = self.timestamp_B1
                driver.timetable()

    def go_through_base_algorythm(self, pilots_a=None, pilots_b=None, wd_type="workday"):   # Creates timetable from 0
        if pilots_a is None:
            pilots_a = self.shift_table.pilots_a
        if pilots_b is None:
            pilots_b = self.shift_table.pilots_b
        if wd_type == "Sun" or wd_type == "Sat" or wd_type == "Weekend":
            self.weekend_algorythm(pilots_b)
        else:
            self.workday_algorythm(pilots_a)
            self.workday_algorythm(pilots_b)

    # Do NOT add pilots unless you want to modify initial timetable instead of duplicate
    def genetic_algorythm_weekday(self, pilots_a=None, pilots_b=None):
        shift_table = copy.deepcopy(self.shift_table)
        if pilots_a is None:
            pilots_a = shift_table.pilots_a
        if pilots_b is None:
            pilots_b = shift_table.pilots_b
        pilots = pilots_b + pilots_a
        iteration = 0
        zero_use_iteration = 50
        timetable = self.get_global_timetable(shift_table)
        min_points = self.get_points(timetable)
        max_points = min_points

        def get_breaks_left(driver):
            routes = 0
            breaks = 2
            for x in driver.timetable:
                if x == "en_route":
                    routes += 1
                elif x == "going_en_route" or "returning":
                    routes = 0
                elif x == "waiting" and breaks >= 1:
                    breaks -= 1
                    routes = 0
                if routes >= 12:
                    routes = 0
                    breaks += 1.5
            return breaks

        def change_start_time(driver):
            if driver.work_start > self.WORK_START and driver.work_start + len(driver.timetable) < self.WORK_END:
                driver.work_start + (random.randint(1, 2) - 1)

        def add_route(driver):  # лобовая проверка можно ли продлить один из проездов
            if driver.work_type == "B" and len(driver.timetable) < 72:
                if driver.work_start + len(driver.timetable) >= self.WORK_END:
                    driver.work_start -= 1
                for i in range(5):
                    a = random.randint(0, len(driver.timetable)-1)
                    if driver.timetable[a] == "en_route":
                        driver.timetable.insert(a, "en_route")
                        if (get_breaks_left(driver) > 0) and (driver.work_start + len(driver.timetable) < self.WORK_END):
                            return driver.timetable.append("waiting")
                        return
            else:
                return

        def add_end_route(driver):
            if driver.work_type != "B":
                return
            if len(driver.timetable) < 72:
                if driver.work_start + len(driver.timetable) >= self.WORK_END:
                    driver.work_start -= 1
                else:
                    return
                i = len(driver.timetable) - 1
                while i > 0:
                    if driver.timetable[i] == "returning":
                        driver.timetable.insert(i, "en_route")
                        if (get_breaks_left(driver) > 0) and (driver.work_start + len(driver.timetable) < self.WORK_END):
                            driver.timetable.insert(i, "waiting")
                            driver.timetable.insert(i, "waiting")
                        return
                    i-=1

        while zero_use_iteration > iteration:
            iteration += 1
            possible_changes = [change_start_time, add_route, add_end_route]
            random.choice(possible_changes)(random.choice(pilots))
            if iteration % 5 == 0:
                timetable = self.get_global_timetable(shift_table)
                points = self.get_points(timetable)
                if points > max_points:
                    max_points = points
                    self.shift_table = copy.deepcopy(shift_table)
                    iteration = 0
#        self.shift_table.show_shift()
#        print(max_points)
        return self.shift_table

    def get_points(self, timetable=None, busses=0):
        points = 0
        if busses == 0:busses = len(self.shift_table.busses)
        if timetable is None: timetable = self.get_global_timetable()
        for j in range(len(timetable)):
            tick = timetable[j]
            en_route = 0
            for i in range(len(tick)):
                if len(tick) > busses:
                    return 0
                if tick[i] == "en_route":
                    en_route += 1
                elif tick[i] == "returning" or "going_en_route":
                    points -= 2
            if en_route > 0:
                if self.HIGH_TIME_START <= j + self.WORK_START <= self.HIGH_TIME_END or self.HIGH_TIME_START + 10 * self.TICKS_PER_HOUR <= j + self.WORK_START <= self.HIGH_TIME_END + 10 * self.TICKS_PER_HOUR:
                    points += en_route * 8
                else:
                    points += 7 * int(math.log1p(2*en_route-1))
            else:
                if self.HIGH_TIME_START <= j + self.WORK_START <= self.HIGH_TIME_END or self.HIGH_TIME_START + 10 * self.TICKS_PER_HOUR <= j + self.WORK_START <= self.HIGH_TIME_END + 10 * self.TICKS_PER_HOUR:
                    points -= 100
                else:
                    points -= 10
        return points

    def get_global_timetable(self, shift_table=None):
        timetable = []
        if shift_table is None:
            shift_table = self.shift_table
        busses = shift_table.busses
        workers_a = shift_table.pilots_a
        workers_b = shift_table.pilots_b
        for i in range(self.WORK_END - self.WORK_START):
            timetable.append([])
        for tick in range(len(timetable)):
            for driver in workers_a:
                if driver.work_start == tick + self.WORK_START:
                    for drivers_ticks in range(len(driver.timetable)):
                        timetable[tick+drivers_ticks].append(driver.timetable[drivers_ticks])
            for driver in workers_b:
                if driver.work_start == tick + self.WORK_START:
                    for drivers_ticks in range(len(driver.timetable)):
                        if tick+drivers_ticks >= len(timetable):
                            print("boom")
                        timetable[tick+drivers_ticks].append(driver.timetable[drivers_ticks])
            if len(timetable[tick]) > len(busses):
                print("Err: not enough busses at " + str(tick))
        return timetable

    def workday_hardcoded_algorythm(self, drivers_a=None, drivers_b=None):      # The most straightforward one
        if drivers_a is None:
            drivers_a = self.shift_table.pilots_a
            for driver in drivers_a:
                driver.timetable = []
        if drivers_b is None:
            drivers_b = self.shift_table.pilots_b
            for driver in drivers_b:
                driver.timetable = []
        a = 0
        b = 0
        for driver in drivers_a:
            if a % 2 == 0:
                driver.work_start = self.WORK_START + int(a % 3)
                driver.timetable.append("going_en_route")
                for i in range(int(self.rph(self.WORK_START - self.HIGH_TIME_START/self.TICKS_PER_HOUR*60, A=True))):
                    driver.timetable.append("en_route")
                for i in range(math.ceil((self.HIGH_TIME_END - self.HIGH_TIME_START)/self.TICKS_PER_HOUR)*self.ROUTE_TIME):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(6):
                    driver.timetable.append("waiting")
                if len(driver.timetable) + self.ROUTE_TIME * 2 < self.TICKS_PER_HOUR*8:
                    driver.timetable.append("going_en_route")
                while len(driver.timetable)+self.ROUTE_TIME+1 < self.TICKS_PER_HOUR*8:
                    for i in range(self.ROUTE_TIME):
                        driver.timetable.append("en_route")
            elif a % 2 == 1:
                driver.work_start = self.WORK_START + self.TICKS_PER_HOUR * 8 - int(a % 3)
                driver.timetable.append("going_en_route")
                for i in range(math.ceil(self.WORK_START - self.HIGH_TIME_START / self.TICKS_PER_HOUR)):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(6):
                    driver.timetable.append("waiting")
                #   remove hashes if end of work time for 5/2 is later than or is 8 or 9 PM
#                if len(driver.timetable) + self.ROUTE_TIME + 2 < self.TICKS_PER_HOUR * 8:
#                    driver.timetable.append("going_en_route")
#                while driver.work_start+len(driver.timetable) < self.WORK_START + self.TICKS_PER_HOUR * 13:
#                    for i in range(self.ROUTE_TIME):
#                        driver.timetable.append("en_route")
            a += 1
        for driver in drivers_b:
            if b % 3 == 0:
                driver.work_start = self.WORK_START + int(b*2)
            elif b % 3 == 1 or 2:
                driver.work_start = self.WORK_START + self.TICKS_PER_HOUR * 11 + int(b % 3) * 2
            for i in range(self.rph(160 + ((b % 3 - 1) * self.TICKS_PER_HOUR/3), A=True)):  # In case of odd numbers
                driver.timetable.append("en_route")
            driver.timetable.append("returning")
            for i in range(6):
                driver.timetable.append("waiting")
            driver.timetable.append("going_en_route")
            wo_break = 0
            while len(driver.timetable) + self.ROUTE_TIME + 3 < self.TICKS_PER_HOUR * 12 and driver.work_start + len(driver.timetable) < 25.5 * self.TICKS_PER_HOUR:
                if wo_break >= math.ceil(self.ROUTE_TIME/self.TICKS_PER_HOUR * 2):
                    for i in range(2):
                        driver.timetable.append("waiting")
                    wo_break = 0
                for i in range(self.ROUTE_TIME):
                    driver.timetable.append("en_route")
                wo_break += 1
            driver.timetable.append("returning")
            if wo_break == math.ceil(self.ROUTE_TIME / self.TICKS_PER_HOUR * 2):
                for i in range(2):
                    driver.timetable.append("waiting")
            b += 1


def git_gud(Algorythm_Timetable:AlgorythmTimetable, iteration_till_best=10):
    best_shift = Algorythm_Timetable
    best_points = best_shift.get_points()
    for i in range(iteration_till_best):
        try_x = copy.deepcopy(Algorythm_Timetable)
        try_x.genetic_algorythm_weekday()
        if best_points < try_x.get_points():
            best_shift = copy.deepcopy(try_x)
    return best_shift


if __name__ == '__main__':
    print("Table testing module")
    TestShift = classes.ShiftTimetable()
#    TestShift.generate_busses(8)
#    TestShift.add_shifters_a(0)
#    TestShift.add_shifters_b(0)
#    simple_timetable_algorythm(TestShift)
    TestShift.show_shift()
    TestShift = classes.ShiftTimetable()
    TestShift.generate_busses(12)
    TestShift.add_shifters_a(6)
    TestShift.add_shifters_b(6)
    GameZ = AlgorythmTimetable(TestShift)
    time_start = time.time()
#    GameZ.go_through_base_algorythm()
    GameZ.workday_hardcoded_algorythm()
    TestShift.show_shift()
    print(GameZ.get_points())
    alpha = git_gud(GameZ)
    alpha.shift_table.show_shift()
    print(alpha.get_points())
#    GameZ.genetic_algorythm_weekday()
    print(str(-int((time_start-time.time())*1000)) + "ms")
#    TestShift.show_shift()
#    print(GameZ.get_points())

"""
    def add_route(driver: classes.Driver):
        for i in range(ROUTE_TIME):
            driver.timetable.append("en_route")
"""
""" # didn't init git repo, too bad
def simple_timetable_algorythm(shift_table: classes.ShiftTimetable):
    shift_table.shift_name = "Simple"
    TICKS_PER_HOUR = 6
    WORK_START = 6
    HIGH_TIME_START = 7 * TICKS_PER_HOUR
    HIGH_TIME_END = HIGH_TIME_START + TICKS_PER_HOUR * 2
    WORK_HOURS = 21
    ROUTE_TIME = int(TICKS_PER_HOUR)
    TYPE_A_TIME = 8
    TYPE_B_TIME = 12
    timestamp_A1 = TICKS_PER_HOUR * 6 + 2 * int(TICKS_PER_HOUR/6)   # Start at WS       DIN at HTE
    timestamp_A2 = timestamp_A1 + TICKS_PER_HOUR * 6 + 1            # Start at B1 break DIN at WTE - 2
    timestamp_A3 = timestamp_A1 + int(ROUTE_TIME / 2)               # Start at WS+RT/2  DIN at HTE + 2 Route
    timestamp_B1 = HIGH_TIME_START                                  # Start at HTS 1 - 1/2 h
    timestamp_B2 = HIGH_TIME_END + int(TICKS_PER_HOUR * 7.5)        # Start at HTS 2 - 1/2 h
    timestamp_B3 = HIGH_TIME_START + TICKS_PER_HOUR * 12 - 1        # Start at HT2 - Route / 2

    def drivers_workaround(workers):
        dave = classes.Driver
        a = 0
        b = 0
        for driver in workers:
            if driver.work_type == "A" and a % 3 == 0:                      # Worker Type A1
                driver.work_start = timestamp_A1
                driver.timetable.append("going_en_route")
                for i in range(4):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(6):
                    driver.timetable.append("waiting")
                driver.timetable.append("going_en_route")
                for i in range(3):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                a += 1
            elif driver.work_type == "A" and a % 3 == 1:                    # Worker Type A2 (xls file for reference)
                driver.work_start = timestamp_A2
                driver.timetable.append("going_en_route")
                for i in range(5):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(6):
                    driver.timetable.append("waiting")
                driver.timetable.append("going_en_route")
                for i in range(2):
                    driver.timetable.append("en_route")
                a += 1
            elif driver.work_type == "A" and a % 3 == 2:                    # Worker Type A3
                driver.work_start = timestamp_A3
                driver.timetable.append("going_en_route")
                for i in range(5):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(6):
                    driver.timetable.append("waiting")
                a += 1
            elif driver.work_type == "B" and b % 3 == 2:                    # Worker Type B1
                driver.work_start = timestamp_B1
                driver.timetable.append("going_en_route")
                for i in range(5):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(9):
                    driver.timetable.append("waiting")
                driver.timetable.append("going_en_route")
                for i in range(3):
                    driver.timetable.append("en_route")
                for i in range(2):
                    driver.timetable.append("waiting")
                for i in range(1):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                b += 1
            elif driver.work_type == "B" and b % 3 == 0:                    # Worker Type B2
                driver.work_start = timestamp_B2
                driver.timetable.append("going_en_route")
                for i in range(5):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(6):
                    driver.timetable.append("waiting")
                driver.timetable.append("going_en_route")
                for i in range(2):
                    driver.timetable.append("en_route")
                for i in range(4):
                    driver.timetable.append("waiting")
                driver.timetable.append("en_route")
                driver.timetable.append("returning")
                b += 1
            elif driver.work_type == "B" and b % 3 == 1:                    # Worker Type B3
                driver.work_start = timestamp_B3
                driver.timetable.append("going_en_route")
                for i in range(4):
                    driver.timetable.append("en_route")
                driver.timetable.append("returning")
                for i in range(7):
                    driver.timetable.append("waiting")
                driver.timetable.append("going_en_route")
                for i in range(2):
                    driver.timetable.append("en_route")
                driver.timetable.append("waiting")
                driver.timetable.append("returning")
                b += 1

    drivers_workaround(shift_table.pilots_a)
    drivers_workaround(shift_table.pilots_b)
"""
class Bus:
    def __init__(self, name="PlaceholderVehicleN"):
        self.current_state = "waiting"          # Cur state works to check for status to have 6 busses on the run
        self.en_route = False                   # Obligatory bool_check
        self.name = name                        # Name for visualisation
        self.timetable = []                     # Timetable to get points from
        self.states = {
            "waiting": 1,
            "lunch": 6,
            "going_en_route": 1,
            "en_route": 6,
            "returning": 1,
        }                                       # Time for state to take effect and worker work-time


class Driver:
    def __init__(self, work_day_type: str, name="PlaceholderPilotN"):
        self.work_type = work_day_type          # Workday type revolves around shift type worker uses
        self.en_route = False                   # Obligatory bool checks for work
#        self.current_vehicle: Bus = None        # Needed for Veh -> worker -> shift logic (Not needed, ended up just counting busses, internal logic on another project)
        self.name = name                        # Name for shift logic
        self.work_ticks = 0                     # work_ticks needed to stay within the law
        self.breaks = 0                         # Breaks show time allowed for driver to be on standby
        self.timetable = []                     # Timetable to get points from
        self.work_start = 0
        self.states = {
            "waiting": 1,
            "lunch": 6,
            "going_en_route": 1,
            "en_route": 1,
            "returning": 1,
        }
        if work_day_type == "A":
            self.breaks = 6
            self.work_ticks = 48
        if work_day_type == "B":
            self.breaks = 4
            self.work_ticks = 72

    def set_on_route(self):
        if not self.en_route:
            self.en_route = True
        else:
            return "Already on route"

    def set_from_route(self):
        if self.en_route:
            self.en_route = False
        else:
            return "Already not on route"

    def tick(self, status):
        self.work_ticks -= self.states.get(status)

    def get_work_ticks(self):
        return self.work_ticks


class ShiftTimetable:
    def __init__(self, ticks_per_hour=6, workday_start=6, workday_end=27):
        # Workday_end should use 24h format with hours if it goes over midnight add hours to 24
        self.ticks_per_hour = ticks_per_hour
        self.ticks = ticks_per_hour * (workday_end - workday_start)  # will fix later, function implemented in CaW
        # Initial score can be lowered or upped, but if it goes bellow zero it eliminates current timetable
        self.busses = []
        self.pilots_a = []
        self.pilots_b = []
        self.shift_name = "Shift_1"

    def generate_busses(self, x=1):
        for i in range(x):
            bus = Bus("Bus " + str(i))
            self.busses.append(bus)

    def add_shifters_a(self, x=1):
        for i in range(x):
            driver = Driver("A", "Driver T:A " + str(i))
            self.pilots_a.append(driver)

    def add_shifters_b(self, x=1):
        for i in range(x):
            driver = Driver("B", "Driver T:B " + str(i))
            self.pilots_b.append(driver)

    def show_shift(self):
        for driver in self.pilots_a:
            # print(driver.timetable)
            x = driver.get_work_ticks()
            t_out = False
            table = ""
            idea_time = driver.work_ticks
            for symbol in driver.timetable:
                if t_out and symbol != "waiting":
                    table += " to {}:{}".format(
                        int((driver.work_start + x - driver.get_work_ticks()) / self.ticks_per_hour),
                        (driver.work_start + x - driver.get_work_ticks()) % self.ticks_per_hour * int(
                            60 / self.ticks_per_hour))
                    t_out = False
                if symbol == "waiting" and not t_out:
                    t_out = True
                    table += " lunch from {}:{}".format(
                        int((driver.work_start + x - driver.get_work_ticks()) / self.ticks_per_hour),
                        (driver.work_start + x - driver.get_work_ticks()) % self.ticks_per_hour * int(
                            60 / self.ticks_per_hour), )
                driver.tick(symbol)
            if t_out:
                table += " to {}:{} \t".format(
                    int((driver.work_start + x - driver.get_work_ticks()) / self.ticks_per_hour),
                    (driver.work_start + x - driver.get_work_ticks()) % self.ticks_per_hour * int(
                        60 / self.ticks_per_hour))
            table = "workday from {workday_start}:{workday_start_min}, to {workday_end}:{workday_end_min}\t". \
                format(workday_start=int(driver.work_start / self.ticks_per_hour),
                       workday_start_min=int(driver.work_start % self.ticks_per_hour) * 10,
                       workday_end=int(
                           (driver.work_start + idea_time - driver.work_ticks) / self.ticks_per_hour),
                       workday_end_min=int(
                           (driver.work_start+idea_time-driver.work_ticks) % self.ticks_per_hour) * int(
                           60 / self.ticks_per_hour)) + table
            print(driver.name + "\t" + table)

        for driver in self.pilots_b:
            # print(driver.timetable)
            x = driver.get_work_ticks()
            t_out = False
            table = ""
            idea_time = driver.work_ticks
            for symbol in driver.timetable:
                if t_out and symbol != "waiting":
                    table += " to {}:{}".format(
                        int((driver.work_start + x - driver.get_work_ticks()) / self.ticks_per_hour),
                        (driver.work_start + x - driver.get_work_ticks()) % self.ticks_per_hour * int(
                            60 / self.ticks_per_hour))
                    t_out = False
                if symbol == "waiting" and not t_out:
                    t_out = True
                    table += " lunch from {}:{}".format(
                        int((driver.work_start + x - driver.get_work_ticks()) / self.ticks_per_hour),
                        (driver.work_start + x - driver.get_work_ticks()) % self.ticks_per_hour * int(
                            60 / self.ticks_per_hour), )
                driver.tick(symbol)
            if t_out:
                table += " to {}:{} \t".format(
                    int((driver.work_start + x - driver.get_work_ticks()) / self.ticks_per_hour),
                    (driver.work_start + x - driver.get_work_ticks()) % self.ticks_per_hour * int(
                        60 / self.ticks_per_hour))
            table = "workday from {workday_start}:{workday_start_min}, to {workday_end}:{workday_end_min}\t". \
                format(workday_start=int(driver.work_start / self.ticks_per_hour),
                       workday_start_min=int(driver.work_start % self.ticks_per_hour) * 10,
                       workday_end=int(
                           (driver.work_start + idea_time - driver.work_ticks) / self.ticks_per_hour),
                       workday_end_min=int(
                           (driver.work_start+idea_time-driver.work_ticks) % self.ticks_per_hour) * int(
                           60 / self.ticks_per_hour)) + table
            print(driver.name + "\t" + table)


def show_shift(shift_table):
    for driver in shift_table.pilots_a:
        print(driver.name)
        # print(driver.timetable)
        x = driver.get_work_ticks()
        t_out = False
        table = ""
        idea_time = driver.work_ticks
        for symbol in driver.timetable:
            if t_out and symbol != "waiting":
                table += " to {}:{}".format(
                    int((driver.work_start + x - driver.get_work_ticks()) / shift_table.ticks_per_hour),
                    (driver.work_start + x - driver.get_work_ticks()) % shift_table.ticks_per_hour * int(
                        60 / shift_table.ticks_per_hour))
                t_out = False
            if symbol == "waiting" and not t_out:
                t_out = True
                table += " lunch from {}:{}".format(
                    int((driver.work_start + x - driver.get_work_ticks()) / shift_table.ticks_per_hour),
                    (driver.work_start + x - driver.get_work_ticks()) % shift_table.ticks_per_hour * int(
                        60 / shift_table.ticks_per_hour), )
            driver.tick(symbol)
        if t_out:
            table += " to {}:{}".format(
                int((driver.work_start + x - driver.get_work_ticks()) / shift_table.ticks_per_hour),
                (driver.work_start + x - driver.get_work_ticks()) % shift_table.ticks_per_hour * int(
                    60 / shift_table.ticks_per_hour))
        table = "workday from {workday_start}:{workday_start_min}, to {workday_end}:{workday_end_min} ". \
            format(workday_start=int(driver.work_start / shift_table.ticks_per_hour),
                   workday_start_min=int(driver.work_start % shift_table.ticks_per_hour) * 10,
                   workday_end=int(
                       (driver.work_start + idea_time - driver.work_ticks) / shift_table.ticks_per_hour),
                   workday_end_min=int(
                       (driver.work_start+idea_time-driver.work_ticks) % shift_table.ticks_per_hour) * int(
                       60 / shift_table.ticks_per_hour)) + table
        print(table)

    for driver in shift_table.pilots_b:
        print(driver.name)
        # print(driver.timetable)
        x = driver.get_work_ticks()
        t_out = False
        table = ""
        idea_time = driver.work_ticks
        for symbol in driver.timetable:
            if t_out and symbol != "waiting":
                table += " to {}:{}".format(
                    int((driver.work_start + x - driver.get_work_ticks()) / shift_table.ticks_per_hour),
                    (driver.work_start + x - driver.get_work_ticks()) % shift_table.ticks_per_hour * int(
                        60 / shift_table.ticks_per_hour))
                t_out = False
            if symbol == "waiting" and not t_out:
                t_out = True
                table += " lunch from {}:{}".format(
                    int((driver.work_start + x - driver.get_work_ticks()) / shift_table.ticks_per_hour),
                    (driver.work_start + x - driver.get_work_ticks()) % shift_table.ticks_per_hour * int(
                        60 / shift_table.ticks_per_hour), )
            driver.tick(symbol)
        if t_out:
            table += " to {}:{}".format(
                int((driver.work_start + x - driver.get_work_ticks()) / shift_table.ticks_per_hour),
                (driver.work_start + x - driver.get_work_ticks()) % shift_table.ticks_per_hour * int(
                    60 / shift_table.ticks_per_hour))
        table = "workday from {workday_start}:{workday_start_min}, to {workday_end}:{workday_end_min} ". \
            format(workday_start=int(driver.work_start / shift_table.ticks_per_hour),
                   workday_start_min=int(driver.work_start % shift_table.ticks_per_hour) * 10,
                   workday_end=int(
                       (driver.work_start + idea_time - driver.work_ticks) / shift_table.ticks_per_hour),
                   workday_end_min=int(
                       (driver.work_start+idea_time-driver.work_ticks) % shift_table.ticks_per_hour) * int(
                       60 / shift_table.ticks_per_hour)) + table
        print(table)


if __name__ == '__main__':
    print("Class interaction test")

""" # Keep here as a workaround in fixated root, type B works better
        for driver in self.pilots_a:
            print(driver.name)
            # print(driver.timetable)
            x = driver.get_work_ticks()
            t_out = False
            table = "workday from {workday_start}:{workday_start_min}, to {workday_end}:{workday_end_min} ".\
                format(workday_start=int(driver.work_start/self.ticks_per_hour),
                       workday_start_min=int(driver.work_start % self.ticks_per_hour)*10,
                       workday_end=int((driver.work_start+driver.work_ticks)/self.ticks_per_hour),
                       workday_end_min=int((driver.work_start+driver.work_ticks) % self.ticks_per_hour)*int(60/self.ticks_per_hour))
            for symbol in driver.timetable:
                if t_out and symbol != "waiting":
                    table += " to {}:{}".format(int((driver.work_start + x - driver.get_work_ticks())/self.ticks_per_hour),
                                                (driver.work_start + x - driver.get_work_ticks())%self.ticks_per_hour*int(60/self.ticks_per_hour))
                    t_out = False
                if symbol == "waiting" and not t_out:
                    t_out = True
                    table += " lunch from {}:{} ".format(int((driver.work_start + x - driver.get_work_ticks())/self.ticks_per_hour),
                                                         (driver.work_start + x - driver.get_work_ticks())%self.ticks_per_hour*int(60/self.ticks_per_hour),)
                driver.tick(symbol)
            if t_out:
                table += " to {}:{}".format(
                    int((driver.work_start + x - driver.get_work_ticks()) / self.ticks_per_hour),
                    (driver.work_start + x - driver.get_work_ticks()) % self.ticks_per_hour * int(
                        60 / self.ticks_per_hour))
            print(table)
"""
"""
        def time_fix(cur_driver: Driver):
            time_x = cur_driver.work_start
            break_time = 0
            break_time_end = 0
        
            for point in cur_driver.timetable:
                if point == "en_route":
                    break_time += 6
                elif point == "going_en_route":
                    break_time += 1
                elif point == "returning":
                    break_time += 1
                elif point == "waiting":
                    break_time_end += 1
"""
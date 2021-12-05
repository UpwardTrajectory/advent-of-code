from math import gcd
from functools import reduce
from typing import NamedTuple, List, Dict
from dataclasses import dataclass
from observations import sample, tests, schedules


# @dataclass
class Bus(NamedTuple):
    span: int
    delay: int

    @staticmethod
    def create(i: int, bus_num: str):
        if bus_num != "x":
            bus_num = int(bus_num)
            return Bus(span=bus_num, delay=i)
        return

    def mins_after(self, t):
        wait_time = self.span * (t // self.span) + self.span - t
        if wait_time == self.span:
            time_after_t = 0
        else:
            time_after_t = wait_time
        return time_after_t


@dataclass
class Fleet(Dict):
    my_departure: int
    fleet: List
    superbus: Bus = Bus.create(i=0, bus_num=1)
    old_t: int = 0

    @staticmethod
    def create(data):
        departure, busses = data.split("\n")
        busses = [int(x) if x != "x" else None for x in busses.split(",")]
        f = [Bus.create(i=i, bus_num=b) for i, b in enumerate(busses) if b]
        #  superbus = Bus.create(i=0, bus_num=1)
        return Fleet(my_departure=int(departure), fleet=f)

    def find_bus(self):
        t = self.my_departure
        wait_times = [(bus, bus.mins_after(t)) for bus in self.fleet]
        best_bus, time_until = sorted(wait_times, key=lambda x: x[1])[0]
        return best_bus.span * time_until

    def chinese_remainder(self):
        """From: https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6"""

        def mul_inv(a, b):
            b0 = b
            x0, x1 = 0, 1
            if b == 1:
                return 1
            while a > 1:
                q = a // b
                a, b = b, a % b
                x0, x1 = x1 - q * x0, x0
            if x1 < 0:
                x1 += b0
            return x1

        n, a = zip(*[(b.span, (b.span - b.delay) % b.span) for b in self.fleet])

        sum = 0
        prod = reduce(lambda a, b: a * b, n)
        for n_i, a_i in zip(n, a):
            p = prod // n_i
            sum += a_i * mul_inv(p, n_i) * p
        return sum % prod

    def sync_to_superbus(self, bus: Bus):
        """Find the repetition cycle between two busses."""
        superbus = self.superbus
        delta_t = superbus.span

        t = self.old_t

        while True:
            first = superbus.delay == superbus.mins_after(t)
            second = bus.delay == bus.mins_after(t)

            if all([first, second]):
                lcm = self.lcm(denominators=[delta_t, bus.span])
                new_delay = self.superbus_mins_after(t, lcm)

                self.superbus = Bus.create(i=new_delay, bus_num=lcm)
                self.old_t = t
                return self.superbus

            t += delta_t

    def superbus_mins_after(self, t, lcm):
        wait_time = lcm * (t // lcm) + lcm - t
        if wait_time == lcm:
            time_after_t = 0
        else:
            time_after_t = wait_time
        return time_after_t

    def lcm(self, denominators):
        """https://stackoverflow.com/a/49816058"""
        return reduce(lambda a, b: a * b // gcd(a, b), denominators)

    def find_cascade(self):
        synced = {}
        bucket = sorted(self.fleet, key=lambda x: x.span, reverse=True)

        for i, bus in enumerate(bucket):
            print(f"Starting {bus}   |   currently riding {self.superbus}")
            self.sync_to_superbus(bus)
            print(f"{bus} succeeded, {len(self.fleet) - i} left.   {self.old_t}")
        return self.old_t


f = Fleet.create(sample)
pred = f.find_cascade()
assert pred == 1068781, f"We got {pred}"

for ans, data in tests.items():
    f = Fleet.create(data)
    pred = f.find_cascade()
    assert pred == ans, f"We got {pred} instead of {ans}"

print("All tests passed")


if __name__ == "__main__":
    f = Fleet.create(schedules)
    print(f.find_bus())

    f = Fleet.create(schedules)
    print(f.chinese_remainder())

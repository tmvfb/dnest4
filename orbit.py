import math
import sys

class Orbit:
    def __init__(self):
        self.vx = []
        self.vy = []

    def load(self, filename):
        try:
            with open(filename, 'r') as fin:
                lines = fin.readlines()
                for line in lines:
                    temp1, temp2 = map(float, line.split())
                    self.vx.append(temp1)
                    self.vy.append(temp2)
            print(f"# Loaded {len(self.vx)} points from orbit file {filename}.")
        except IOError:
            print(f"# ERROR: Couldn't open file {filename}.")
            sys.exit(1)

    def evaluate(self, arg_to_cos, viewing_angle):
        vr = []
        vrmax = -1E300
        vrmin = 1E300
        highest = 0

        C = math.cos(viewing_angle)
        S = math.sin(viewing_angle)

        for i in range(len(self.vx)):
            vr_value = C * self.vx[i] + S * self.vy[i]
            vr.append(vr_value)
            if vr_value > vrmax:
                vrmax = vr_value
            if vr_value < vrmin:
                vrmin = vr_value
            if vr_value > vr[highest]:
                highest = i

        for i in range(len(vr)):
            vr[i] = 2 * (vr[i] - vrmin) / (vrmax - vrmin) - 1

        result = []
        for arg in arg_to_cos:
            index = int(len(vr) * (arg + 2 * math.pi * highest / len(vr)) / (2 * math.pi))
            try:
                result.append(vr[index])
            except:
                pass

        return result

    @staticmethod
    def test():
        o = Orbit()
        o.load("Orbits/orbits0.710.dat")

        t = []
        tt = -10.0
        while tt <= 10.0:
            t.append(tt)
            tt += 0.01

        y = o.evaluate(t, 1.0)
        for i in range(len(y)):
            print(t[i], y[i])


if __name__ == "__main__":
    Orbit.test()

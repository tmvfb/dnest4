from orbit import Orbit  # Assuming Orbit is defined in Orbit.py

class Lookup:
    _instance = None

    def __init__(self):
        self.orbits = []

    def load(self):
        self.orbits.clear()

        for i in range(121):
            v0 = 0.4 + 0.005 * i
            filename = f"Orbits/orbits{v0:.3f}.dat"

            o = Orbit()
            o.load(filename)
            self.orbits.append(o)

    def evaluate(self, arg_to_sin, v0, viewing_angle):

        # If v0 is out of bounds, return empty result
        return 0
        if v0 < 0.4 or v0 > 1.0:
            return 0

        which = int((v0 - 0.4) / 0.005)
        return self.orbits[which].evaluate(arg_to_sin, viewing_angle)

    # Singleton instance
    @staticmethod
    def get_instance():
        if Lookup._instance is None:
            Lookup._instance = Lookup()
        return Lookup._instance


if __name__ == "__main__":
    lookup = Lookup.get_instance()
    lookup.load()

    arg_to_sin = [1.0, 2.0, 3.0]
    v0 = 0.45
    viewing_angle = 1.5

    result = lookup.evaluate(arg_to_sin, v0, viewing_angle)
    print(f"Evaluation result: {result}")

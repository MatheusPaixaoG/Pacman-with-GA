import math

class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = round(x, 2)
        self.y = round(y, 2)
        self.thresh = 0.000001

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None

    def __truediv__(self, scalar):
        return self.__div__(scalar)

    def __eq__(self, other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    def magnitudeSquared(self):
        return self.x**2 + self.y**2

    def magnitude(self):
        return math.sqrt(self.magnitudeSquared())

    def distSquaredTo(self, other):
        return round((self.x - other.x)**2 + (self.y - other.y)**2, 4)
    
    def euclideanDistTo(self, other):
        return round(math.sqrt(self.distSquaredTo(other)), 2)
    
    def manhattanDistTo(self, other):
        return round(abs(self.x - other.x) + abs(self.y - other.y), 2)

    def copy(self):
        return Vector2(self.x, self.y)

    def asTuple(self):
        return self.x, self.y

    def asInt(self):
        return int(self.x), int(self.y)

    def __str__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"
    
    def normalized(self):
        normalized = self / self.magnitude()
        return Vector2(normalized.x, normalized.y)
import math

class Vetor2D:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    @property
    def angulo(self):
        return math.atan2(self.y,self.x)

    @property
    def tamanho(self):
        return math.sqrt(self.x**2 + self.y**2) 

    def normalizado(self):
        if self.x == 0 and self.y == 0:
            return Vetor2D(0,0)
        if self.x == 0:
            return Vetor2D(0,1)
        if self.y == 0:
            return Vetor2D(1,0)
        if self.x < self.y:
            return Vetor2D(1,self.y/self.x)
        return Vetor2D(self.x/self.y,1)
                
    def normalize(self):
        normalized = self.normalizado()
        self.x = normalized.x
        self.y = normalized.y

    def zerar(self):
        self.x = 0
        self.y = 0

    def copy(self):
        return Vetor2D(self.x,self.y)

    def __add__(self,other):
        return Vetor2D(self.x + other.x, self.y + other.y)

    def __sub__(self,other):
        return Vetor2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self,other):
        if isinstance(other, (int, float)):
            return Vetor2D(self.x * other, self.y * other)
        return Vetor2D(self.x * other.x, self.y * other.y)

    def __truediv__(self,other):
        if isinstance(other, (int, float)):
            return Vetor2D(self.x / other, self.y / other)
        return Vetor2D(self.x / other.x, self.y / other.y)
    
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x},{self.y})'

    def __repr__(self):
        return f'Vetor2D({self.x},{self.y})'
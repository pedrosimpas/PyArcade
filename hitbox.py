from numpy import linspace, cos, sin, array, pi

class Hit_Box():
    def __init__(self) -> None:
        self.x = array([])
        self.y = array([])

    def FuncaoColisao(self, inX, inY):
        pass

class Circle_Hit_Box(Hit_Box):
    def __init__(self, Npontos, raio) -> None:
        self.raio = raio
        self.theta_list = linspace(0.0, 2.0*pi, num = Npontos)
        self.x = raio*cos(self.theta_list)
        self.y = raio*sin(self.theta_list)

    def Colidir(self, center, colisor : Hit_Box):
        return colisor.FuncaoColisao(center[0] + self.x, center[1] + self.y)

    def FuncaoColisao(self, inX, inY):
        return ((inX[:, None] - self.x[None, :])**2 + (inY[:, None] - self.y[None, :])**2 <= self.raio**2).any(axis = 1)



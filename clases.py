class Coche:
    ruedas = 4
    
    def __init__(self, color = "azul", aceleracion = 3) :
        self.color = color
        self.aceleracion = aceleracion
        self.velocidad = 0
        
    def acelera(self, turbo) :
        self.velocidad = self.velocidad + self.aceleracion + turbo
        
        
a = Coche("verde", 1)

a.acelera(turbo = 2)
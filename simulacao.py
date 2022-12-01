import math
import random
from vetor2d import Vetor2D


class Mundo:

    GRAVIVIDADE = 0.005
    GRAV_POWER = 1.2
    TIPOS_PARTICULAS = []

    def __init__(self,largura,altura):
        self.largura = largura
        self.altura = altura
        self.objs = []
    
    def remove(self,obj):
        if obj in self.objs:
            self.objs.remove(obj)
    
    def update(self,dt):
        self.calcular_aceleracao()
        #self.calcular_aceleracao2()
        for obj in self.objs:
            obj.update(dt)
            self.colisao_muro(obj)

    def criar_particula(self,pos,massa=1,tipo = 0):
        self.objs.append(self.TIPOS_PARTICULAS[tipo](pos[0],pos[1],massa,self))
    
    def add_particula(self,particula):
        self.objs.append(particula)

    def calcular_aceleracao2(self):
        for obj1 in self.objs:
            for obj2 in self.objs:
                if obj1 is obj2:
                    continue
                if self.colisao(obj, obj2):
                    continue
                dx = obj2.pos.x - obj1.pos.x
                dy = obj2.pos.y - obj1.pos.y
                angle = math.atan2(dy,dx)
                distance = math.sqrt(dx*dx+dy*dy)
                force = (self.GRAVIVIDADE * obj1.massa * obj2.massa) / (distance ** self.GRAV_POWER)
                obj1.vel.x += force*math.cos(angle)
                obj1.vel.y += force*math.sin(angle)

    def calcular_aceleracao(self):
        for obj in self.objs:
            for obj2 in self.objs:
                if obj == obj2:
                    continue
                if self.colisao(obj, obj2):
                    continue
                distancia = obj2.pos - obj.pos
                forca = (self.GRAVIVIDADE * obj.massa * obj2.massa) / (distancia.tamanho ** self.GRAV_POWER)
                obj.vel += distancia / distancia.tamanho * forca

    def colisao(self,obj1,obj2):
        distancia = obj2.pos - obj1.pos
        if distancia.tamanho <=obj1.raio + obj2.raio:
            return True
        return False

    def colisao_muro(self,obj):
        if obj.pos.x + obj.raio >= self.largura:
            event = EventoColisaoMuro('direita')
            obj.event(event)
        elif obj.pos.x - obj.raio <= 0:
            event = EventoColisaoMuro('esquerda')
            obj.event(event)
        if obj.pos.y + obj.raio >= self.altura:
            event = EventoColisaoMuro('cima')
            obj.event(event)
        elif obj.pos.y - obj.raio <= 0:
            event = EventoColisaoMuro('baixo')
            obj.event(event)
    

class Particula:

    RADIUS_FACTOR = 15

    def __init__(self, x, y,massa,mundo):
        self.pos = Vetor2D(x,y)
        self.vel = Vetor2D(0,0)
        self.massa = massa
        self.mundo = mundo

    @property
    def raio(self):
        #return self.RADIUS_FACTOR * self.massa ** 0.5
        return (self.massa * 4) + 4

    @property
    def velocidade(self):
        return self.vel.tamanho
    
    @property
    def angulo(self):
        return self.vel.angulo

    def update(self,dt):
        self.pos += self.vel * dt
        self.checar_colisao()
        
    def checar_colisao(self):
        for p in self.mundo.objs:
            if p != self:
                if self.mundo.colisao(self, p):
                    event1 = EventoColisao(p.pos.x, p.pos.y, p.raio, p.vel, p.massa, p)
                    event2 = EventoColisao(self.pos.x, self.pos.y, self.raio, self.vel, self.massa,self)
                    self.event(event1)
                    p.event(event2)

    def resolver_colisao(self, evento):
        t1 = self.angulo
        t2 = evento.vel.angulo
        dist = evento.pos - self.pos
        phi = math.atan2(dist.y, dist.x)
        self.pos.x -= math.cos(phi) * ((self.raio + evento.raio - dist.tamanho))
        self.pos.y -= math.sin(phi) * ((self.raio + evento.raio - dist.tamanho))
        m1,m2 = self.massa, evento.massa
        v1,v2 = self.velocidade, evento.vel.tamanho
        vx1 = (v1*math.cos(t1-phi)*(m1-m2)+2*m2*v2*math.cos(t2-phi))/(m1+m2)*math.cos(phi)+v1*math.sin(t1-phi)*math.cos(phi+math.pi/2)
        vy1 = (v1*math.cos(t1-phi)*(m1-m2)+2*m2*v2*math.cos(t2-phi))/(m1+m2)*math.sin(phi)+v1*math.sin(t1-phi)*math.sin(phi+math.pi/2)
        self.vel.x = vx1
        self.vel.y = vy1

    def resolver_colisao_muro(self, evento):
        if evento.lado == 'esquerda':
            self.pos.x += self.raio - self.pos.x
            self.vel.x *= -1
        elif evento.lado == 'direita':
            self.pos.x -= self.pos.x - (self.mundo.largura - self.raio)
            self.vel.x *= -1
        elif evento.lado == 'cima':
            self.pos.y -= self.pos.y - (self.mundo.altura - self.raio)
            self.vel.y *= -1
        elif evento.lado == 'baixo':
            self.pos.y += self.raio - self.pos.y
            self.vel.y *= -1
        self.vel /= 2
        
    def event(self, event):
        if isinstance(event, EventoColisao):
            self.resolver_colisao(event)
        elif isinstance(event, EventoColisaoMuro):
            self.resolver_colisao_muro(event)

    def __str__(self):
        return f'Pos: {self.pos}, Vel: {self.vel}, Massa: {self.massa}'

Mundo.TIPOS_PARTICULAS.append(Particula)

class ParticulaExplosiva(Particula):

    MIN_FRAGS = 3
    MAX_FRAGS = 7

    def __init__(self, x, y, massa, mundo):
        super().__init__(x, y, massa, mundo)
        self.explosao = False
    
    def explodir(self,angulo):
        self.explosao = True
        self.mundo.remove(self)
        frags = random.randint(self.MIN_FRAGS, self.MAX_FRAGS)
        for i in range(frags):
            ang = angulo + math.pi / 4 * i
            vel = self.velocidade
            x = self.pos.x + math.cos(ang) * self.raio
            y = self.pos.y + math.sin(ang) * self.raio
            p = Particula(x, y, self.massa / frags, self.mundo)
            p.vel = Vetor2D(vel * math.cos(ang), vel * math.sin(ang))
            self.mundo.add_particula(p)

    def event(self, event):
        if isinstance(event, EventoColisao):
            if self.explosao:
                self.resolver_colisao(event)
            else:
                self.resolver_colisao(event)
                dist = event.pos - self.pos
                phi = math.atan2(dist.y, dist.x)
                self.explodir(phi)
        else:
            super().event(event)

Mundo.TIPOS_PARTICULAS.append(ParticulaExplosiva)

class ParticulaGulosa(Particula):

    def resolver_juncao(self, evento):
        if isinstance(evento.obj, ParticulaGulosa):
            if self.massa > evento.massa:
                self.massa += evento.massa
                self.mundo.remove(evento.obj)
        elif not isinstance(evento.obj, ParticulaExplosiva):
            self.massa += evento.massa
            self.mundo.remove(evento.obj)
        else:
            self.resolver_colisao(evento)

    def event(self, event):
        if isinstance(event, EventoColisao):
            self.resolver_juncao(event)
        else:
            super().event(event)

Mundo.TIPOS_PARTICULAS.append(ParticulaGulosa)

class EventoColisao:
    def __init__(self, x, y, raio, velocidade,massa,obj = None):
        self.pos = Vetor2D(x,y)
        self.vel = Vetor2D(velocidade.x,velocidade.y)
        self.raio = raio
        self.massa = massa
        self.obj = obj

class EventoColisaoMuro:
    def __init__(self, lado):
        self.lado = lado



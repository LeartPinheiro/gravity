import pygame
import simulacao as sim
import random as rd

pygame.init()

SW = 1366
SH = 768
FPS = 60
TIME_MULTIPLIER = 1000

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Gravity")
clock = pygame.time.Clock()

mundo = sim.Mundo(SW,SH)
paused = False

def update(dt):
    mundo.update(dt)

def desenhar():
    screen.fill((100, 100, 255))
    desenhar_particulas()
    desenhar_paused() if paused else None
    pygame.display.update()

def desenhar_particulas():
    for p in mundo.objs:
        pygame.draw.circle(screen, obter_cor(p), (int(p.pos.x), int(p.pos.y)), int(p.raio))
        desenhar_anel(p)
        #desenhar_velocidade(p)

aneis_cores = {sim.Particula: None, 
    sim.ParticulaExplosiva: (225, 90, 90), 
    sim.ParticulaGulosa: (45, 45, 45)}

def desenhar_anel(p):
    cor = aneis_cores[type(p)]
    if cor:
        pygame.draw.circle(screen, cor, (int(p.pos.x), int(p.pos.y)), int(p.raio), 2)

def desenhar_paused():
    font = pygame.font.SysFont('Arial', 50)
    text = font.render('PAUSED', True, (255, 0, 0))
    x = SW / 2 - text.get_width() / 2
    y = SH / 2 - text.get_height() / 2
    screen.blit(text, (x, y))

def desenhar_velocidade(obj):
    font = pygame.font.SysFont('Arial',25)
    speed = obj.massa
    text = font.render(f'{speed:.2f}',True,(255,255,255))
    x = obj.pos.x - text.get_width() / 2
    y = obj.pos.y - text.get_height() / 2
    screen.blit(text,(x,y))

color_cache = {}

def obter_cor(obj):
    if obj not in color_cache:
        color_cache[obj] = (rd.randint(45,210),rd.randint(45,210),rd.randint(45,210))
    return color_cache[obj]

mundo.objs.append(sim.ParticulaExplosiva(100,100,5,mundo))
tipo = {'atual':0,'max':len(sim.Mundo.TIPOS_PARTICULAS)-1}

def checar_botoes():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mundo.criar_particula(pygame.mouse.get_pos(),rd.randint(2,5),tipo['atual'])
                print(f'{tipo["atual"]} {sim.Mundo.TIPOS_PARTICULAS[tipo["atual"]]}')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                global paused
                paused = not paused
            if event.key == pygame.K_UP:
                tipo['atual'] -= 1
                if tipo['atual'] < 0:
                    tipo['atual'] = 0
            if event.key == pygame.K_DOWN:
                tipo['atual'] += 1
                if tipo['atual'] > tipo['max']:
                    tipo['atual'] = tipo['max']
                

def atualizar_infos():
    objs_on_screen = len(mundo.objs)
    fps = clock.get_fps()
    pygame.display.set_caption(f"Gravity - {objs_on_screen} objs - {fps:.2f} FPS")

def main():
    run = True
    while run:
        clock.tick(FPS)
        dt = clock.get_time() / 1000 * TIME_MULTIPLIER
        atualizar_infos()
        checar_botoes()
        update(dt) if not paused else None
        desenhar()
    pygame.quit()
main()

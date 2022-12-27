import arcade
import time
import random
import numpy as np 



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"

class InputReader():
    def __init__(self) -> None:
        self.Possible_commands = {
                                    arcade.key.UP    : False,
                                    arcade.key.DOWN  : False,
                                    arcade.key.LEFT  : False,
                                    arcade.key.RIGHT : False,
                                    arcade.key.ESCAPE: False
                                 }

    def set_keys_on(self, key, modifier):
        '''
          Turn possible keys on.
        '''
        _val = self.Possible_commands.get(key)
        if _val is not None:
            if key == arcade.key.ESCAPE:
                self.Possible_commands[key] = not self.Possible_commands[key]
            else:
                self.Possible_commands[key] = True

    def set_keys_off(self, key, modifier):
        '''
          Turn possible keys off.
        '''
        _val = self.Possible_commands.get(key)
        if _val is not None:
            if not (key == arcade.key.ESCAPE):
                self.Possible_commands[key] = False
                
    def get_current_key_value(self, key):
        '''
            Get current value of a possible key
        '''
        return self.Possible_commands[key]

class Circle_Hit_Box():
    def __init__(self, Npontos, raio) -> None:
        self.theta_list = np.linspace(0.0, 2.0*np.pi, num = Npontos)
        self.x = raio*np.cos(self.theta_list)
        self.y = raio*np.sin(self.theta_list)

    def Colidir(self, center, posicoes_x, posicoes_y, raios):
        _aux_colisao = (center[0] + self.x[:, None] - posicoes_x[None, :])**2 \
                       + (center[1] + self.y[:, None] - posicoes_y[None, :])**2 <= raios**2
        return _aux_colisao.any(axis = 0)

class Player():
    player_size : float = SCREEN_WIDTH/50
    score       : int   = 0
    def __init__(self) -> None:
        self.posicao = np.array([SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
        self.hit_box = Circle_Hit_Box(Npontos = 4, raio = self.player_size)

    def Mover(self, inInputKey):
        step_size = 7
        Dx, Dy = 0, 0

        if inInputKey.get_current_key_value(arcade.key.UP):
            Dy = step_size
        if inInputKey.get_current_key_value(arcade.key.DOWN):
            Dy = -step_size
        if inInputKey.get_current_key_value(arcade.key.LEFT):
            Dx = -step_size
        if inInputKey.get_current_key_value(arcade.key.RIGHT):
            Dx = step_size

        self.posicao = self.posicao + [Dx, Dy]

        if self.posicao[1] - self.player_size < 0.0:
            self.posicao[1] = self.player_size
        elif self.posicao[1] + self.player_size > SCREEN_HEIGHT:
            self.posicao[1] = SCREEN_HEIGHT - self.player_size

        if self.posicao[0] - self.player_size < 0.0:
            self.posicao[0] = self.player_size
        elif self.posicao[0] + self.player_size > SCREEN_WIDTH:
            self.posicao[0] = SCREEN_WIDTH - self.player_size

    def Desenhar(self):
        arcade.draw_circle_filled(self.posicao[0], self.posicao[1], self.player_size, arcade.color.BLUE)

class Frutas(arcade.Sprite):
    def __init__(self) -> None:
        SPRITE_SCALING = 1.0/7.5
        super().__init__("./sprites/fruta_jogo.png", SPRITE_SCALING)
        self.center_x, self.center_y = SCREEN_WIDTH/2 + 50, SCREEN_HEIGHT/2 + 50
        self.hbox_size = SCREEN_WIDTH/50

class PowerUpsList():
    def __init__(self, Npowerups: int) -> None:
        self.Npowerups = Npowerups
        self.lista_powerups = []
        self.posicoes_x      = []
        self.posicoes_y     = []
        for ipower in range(self.Npowerups):
            self.lista_powerups.append(Frutas())
            self.lista_powerups[ipower].center_x = random.uniform(0, SCREEN_WIDTH)
            self.lista_powerups[ipower].center_y = random.uniform(0, SCREEN_HEIGHT)
            self.posicoes_x.append(self.lista_powerups[ipower].center_x)
            self.posicoes_y.append(self.lista_powerups[ipower].center_y)

        self.posicoes_x = np.array(self.posicoes_x)
        self.posicoes_y = np.array(self.posicoes_y)

        self.lista_powerups = np.array(self.lista_powerups)

    def shuffle(self):
        self.posicoes_x = []
        self.posicoes_y = []
        for poweup in self.lista_powerups:
            poweup.center_x = random.uniform(0, SCREEN_WIDTH)
            poweup.center_y = random.uniform(0, SCREEN_HEIGHT)
            self.posicoes_x.append(poweup.center_x)
            self.posicoes_y.append(poweup.center_y)

        self.posicoes_x = np.array(self.posicoes_x)
        self.posicoes_y = np.array(self.posicoes_y)

    def Desenhar(self):
        for powerup in self.lista_powerups:
            powerup.draw()

class TimeTracker():
    def __init__(self, ini_time) -> None:
        self.time0 = ini_time
        self.dT    = 0.0

    def get_dT(self):
        return self.dT
    def update_dT(self):
        self.dT = time.perf_counter() - self.time0
    def reset_t0(self, init_val = 0.0):
        self.time0 = time.perf_counter() - init_val

class MyGame(arcade.Window):
    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)
        self.jogador         = Player()
        self.currentkeys     = InputReader()
        self.currentpowerups = PowerUpsList(10)
        self.timeline        = TimeTracker(time.perf_counter())

        self.on_key_press   = self.currentkeys.set_keys_on
        self.on_key_release = self.currentkeys.set_keys_off


    def on_draw(self):
        arcade.start_render()

        if len(self.currentpowerups.lista_powerups) > 0 :
            if self.currentkeys.get_current_key_value(arcade.key.ESCAPE):
                arcade.draw_text(r"Jogo esta pausado", 0.0*SCREEN_WIDTH, 0.5*SCREEN_HEIGHT,\
                                                                arcade.color.RED, 50, 800, 'center')
                self.timeline.reset_t0(self.timeline.get_dT())
            else:
                self.jogador.Mover(self.currentkeys)
                self.Reset_Timeline()
                self.colisor_powerup()
            self.currentpowerups.Desenhar()

            arcade.draw_text("Score: " + str(self.jogador.score), 0.05*SCREEN_WIDTH, 0.90*SCREEN_HEIGHT,\
                                                              arcade.color.WHITE, 30, 50, 'left')
        else:
            arcade.draw_text("Jogo acabou!", 0.0*SCREEN_WIDTH, 0.7*SCREEN_HEIGHT,\
                                                              arcade.color.RED, 50, 800, 'center')
            arcade.draw_text("Score Final: " + str(self.jogador.score), 0.0*SCREEN_WIDTH, 0.5*SCREEN_HEIGHT,\
                                                              arcade.color.RED, 50, 800, 'center')
        self.jogador.Desenhar()


        arcade.draw_text("Por Malyk & Pedro", -0.05*SCREEN_WIDTH, 0.05*SCREEN_HEIGHT,\
                                                              arcade.color.WHITE, 10, 800, 'right')

        arcade.finish_render()

    def Reset_Timeline(self):
        self.timeline.update_dT()
        if self.timeline.get_dT() > 2.0:
            self.currentpowerups.shuffle()
            self.jogador.score = self.jogador.score - 10
            self.timeline.reset_t0()

    def colisor_powerup(self):
        resultado_colisao = self.jogador.hit_box.Colidir(self.jogador.posicao,\
                                    self.currentpowerups.posicoes_x, self.currentpowerups.posicoes_y,\
                                    self.currentpowerups.lista_powerups[0].hbox_size
                                    )
        self.jogador.score     = self.jogador.score + int(np.sum(resultado_colisao)*100)
        self.currentpowerups.lista_powerups  = self.currentpowerups.lista_powerups[~resultado_colisao]
        self.currentpowerups.posicoes_x      = self.currentpowerups.posicoes_x[~resultado_colisao]
        self.currentpowerups.posicoes_y      = self.currentpowerups.posicoes_y[~resultado_colisao]


if __name__ == "__main__":


    jogo = MyGame()

    jogo.run()

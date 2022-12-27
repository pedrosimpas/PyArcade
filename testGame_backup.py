import arcade
import time
import random
import numpy as np 



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"


class Player_Key():
    up    : bool
    down  : bool
    left  : bool
    right : bool
    esc   : bool
    def __init__(self) -> None:
        self.up    = False
        self.down  = False
        self.left  = False
        self.right = False
        self.esc   = False

    def set_keys_on(self, key, modifier):
        if key == arcade.key.UP:
            self.up = True
        elif key == arcade.key.DOWN:
            self.down = True
        elif key == arcade.key.LEFT:
            self.left = True
        elif key == arcade.key.RIGHT:
            self.right = True

    def set_keys_off(self, key, modifier):
        if key == arcade.key.UP:
            self.up = False
        elif key == arcade.key.DOWN:
            self.down = False
        elif key == arcade.key.LEFT:
            self.left = False
        elif key == arcade.key.RIGHT:
            self.right = False

class Circle_Hit_Box():
    def __init__(self, Npontos, raio) -> None:
        self.theta_list = np.linspace(0.0, 2.0*np.pi, num = Npontos)
        self.x = raio*np.cos(self.theta_list)
        self.y = raio*np.sin(self.theta_list)

    def Colidir(self, center, posicoes_x, posicoes_y, raios):
        _aux_colisao = (center[0] + self.x[:, None] - posicoes_x[None, :])**2 \
                       + (center[1] + self.y[:, None] - posicoes_y[None, :])**2 <= raios**2
        return _aux_colisao.any(axis = 0)

class Frutas(arcade.Sprite):
    def __init__(self) -> None:
        SPRITE_SCALING = 1.0/7.5
        super().__init__("./sprites/fruta_jogo.png", SPRITE_SCALING)
        self.center_x, self.center_y = SCREEN_WIDTH/2 + 50, SCREEN_HEIGHT/2 + 50
        self.hbox_size = SCREEN_WIDTH/50

class Player():
    player_size : float = SCREEN_WIDTH/50
    score       : int   = 0
    def __init__(self) -> None:
        self.posicao = np.array([SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
        self.botoes       = Player_Key()
        self.hit_box      = Circle_Hit_Box(Npontos = 4, raio = self.player_size)

    def Mover(self):
        step_size = 7
        Dx, Dy = 0, 0

        if self.botoes.up:
            Dy = step_size
        if self.botoes.down:
            Dy = -step_size
        if self.botoes.left:
            Dx = -step_size
        if self.botoes.right:
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

class InputReader():
    def __init__(self) -> None:
        self.player_commands = Player_Key()

    def Key_Reader():



class MyGame(arcade.Window):
    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)
        self.jogador = Player()

        self.Nfrutas = 10
        self.lista_frutas      = []
        self.posicoes_frutas_x = []
        self.posicoes_frutas_y = []
        for ifruta in range(self.Nfrutas):
            self.lista_frutas.append(Frutas())
            self.lista_frutas[ifruta].center_x = random.uniform(0, SCREEN_WIDTH)
            self.lista_frutas[ifruta].center_y = random.uniform(0, SCREEN_HEIGHT)
            self.posicoes_frutas_x.append(self.lista_frutas[ifruta].center_x)
            self.posicoes_frutas_y.append(self.lista_frutas[ifruta].center_y)

        self.posicoes_frutas_x = np.array(self.posicoes_frutas_x)
        self.posicoes_frutas_y = np.array(self.posicoes_frutas_y)

        self.lista_frutas = np.array(self.lista_frutas)
        self.on_key_press   = self.jogador.botoes.set_keys_on
        self.on_key_release = self.jogador.botoes.set_keys_off
        self.ini_time = time.perf_counter()
        self.dT_fruta = 0.0

    def on_draw(self):
        arcade.start_render()
        self.dT_fruta = time.perf_counter() - self.ini_time
        if self.dT_fruta > 2.0:
            self.mover_frutas()
            self.ini_time = time.perf_counter()
            self.dT_fruta = 0.0
            if len(self.lista_frutas) > 0:
                self.jogador.score  = self.jogador.score - 10
   

        self.jogador.Mover()
        self.jogador.Desenhar()
        for fruta in self.lista_frutas:
            fruta.draw()


        if len(self.lista_frutas) > 0:
            resultado_colisao = self.jogador.hit_box.Colidir(self.jogador.posicao,\
                                        self.posicoes_frutas_x, self.posicoes_frutas_y,\
                                        self.lista_frutas[0].hbox_size
                                        )
            self.jogador.score     = self.jogador.score + int(np.sum(resultado_colisao)*100)
            self.lista_frutas      = self.lista_frutas[~resultado_colisao]
            self.posicoes_frutas_x = self.posicoes_frutas_x[~resultado_colisao]
            self.posicoes_frutas_y = self.posicoes_frutas_y[~resultado_colisao]

            arcade.draw_text("Score: " + str(self.jogador.score), 0.05*SCREEN_WIDTH, 0.90*SCREEN_HEIGHT,\
                                                              arcade.color.WHITE, 30, 50, 'left')
        else: 
            arcade.draw_text("Jogo acabou!", 0.0*SCREEN_WIDTH, 0.7*SCREEN_HEIGHT,\
                                                              arcade.color.RED, 50, 800, 'center')
            arcade.draw_text("Score Final: " + str(self.jogador.score), 0.0*SCREEN_WIDTH, 0.5*SCREEN_HEIGHT,\
                                                              arcade.color.RED, 50, 800, 'center')

        arcade.draw_text("Por Malyk & Pedro", -0.05*SCREEN_WIDTH, 0.05*SCREEN_HEIGHT,\
                                                              arcade.color.WHITE, 10, 800, 'right')
        arcade.finish_render()

    def mover_frutas(self):
        self.posicoes_frutas_x = []
        self.posicoes_frutas_y = []
        for fruta in self.lista_frutas:
            fruta.center_x = random.uniform(0, SCREEN_WIDTH)
            fruta.center_y = random.uniform(0, SCREEN_HEIGHT)
            self.posicoes_frutas_x.append(fruta.center_x)
            self.posicoes_frutas_y.append(fruta.center_y)

        self.posicoes_frutas_x = np.array(self.posicoes_frutas_x)
        self.posicoes_frutas_y = np.array(self.posicoes_frutas_y)


if __name__ == "__main__":


    jogo = MyGame()

    jogo.run()

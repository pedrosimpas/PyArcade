import arcade
import time
import numpy as np 

from input import InputReader
from objects import Player, PowerUpsList

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"


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

        self._Objetos_de_Tela = {
                                 "powerups" : PowerUpsList(10, SCREEN_WIDTH, SCREEN_HEIGHT),
                                 "jogador"  : Player(SCREEN_WIDTH, SCREEN_HEIGHT)
                                }

        self._poweup_move = False

        arcade.set_background_color(arcade.color.AMAZON)
        self.currentkeys     = InputReader()
        self.timeline        = TimeTracker(time.perf_counter())

        self.on_key_press   = self.currentkeys.set_keys_on
        self.on_key_release = self.currentkeys.set_keys_off

    def on_draw(self):
        arcade.start_render()

        if len(self._Objetos_de_Tela["powerups"].lista_powerups) > 0 :
            if self.currentkeys.get_current_key_value(arcade.key.ESCAPE):
                arcade.draw_text(r"Jogo esta pausado", 0.0*SCREEN_WIDTH, 0.5*SCREEN_HEIGHT,\
                                                                arcade.color.RED, 50, 800, 'center')
                self.timeline.reset_t0(self.timeline.get_dT())
            else:
                self.Reset_Timeline()
                for _,  obj in self._Objetos_de_Tela.items():
                    obj.Mover(self.currentkeys, mover_poweups =  self._poweup_move)
                self._poweup_move = False
                self.colisor()

            arcade.draw_text("Score: " + str(self._Objetos_de_Tela["jogador"].score), 0.05*SCREEN_WIDTH, 0.90*SCREEN_HEIGHT,\
                                                              arcade.color.WHITE, 30, 50, 'left')
        
        for _, obj in self._Objetos_de_Tela.items():
            obj.Desenhar()


        if len(self._Objetos_de_Tela["powerups"].lista_powerups) == 0 :
            arcade.draw_text("Jogo acabou!", 0.0*SCREEN_WIDTH, 0.7*SCREEN_HEIGHT,\
                                                              arcade.color.RED, 50, 800, 'center')
            arcade.draw_text("Score Final: " + str(self._Objetos_de_Tela["jogador"].score), 0.0*SCREEN_WIDTH, 0.5*SCREEN_HEIGHT,\
                                                              arcade.color.RED, 50, 800, 'center')

        arcade.draw_text("Por Malyk & Pedro", -0.05*SCREEN_WIDTH, 0.05*SCREEN_HEIGHT,\
                                                              arcade.color.WHITE, 10, 800, 'right')

        arcade.finish_render()

    def Reset_Timeline(self):
        self.timeline.update_dT()
        if self.timeline.get_dT() > 2.0:
            self._poweup_move = True
            self._Objetos_de_Tela["jogador"].score = self._Objetos_de_Tela["jogador"].score - 10
            self.timeline.reset_t0()

    def colisor(self):
        _x, _y = self._Objetos_de_Tela["jogador"].posicao
        _raio  = self._Objetos_de_Tela["jogador"].player_size

        resultado_colisao =  self._Objetos_de_Tela["powerups"].Colidir(xcentral = _x, ycentral = _y, player_radius = _raio)


        self._Objetos_de_Tela["jogador"].score = self._Objetos_de_Tela["jogador"].score + int(np.sum(resultado_colisao)*100)

        self._Objetos_de_Tela["powerups"].lista_powerups = self._Objetos_de_Tela["powerups"].lista_powerups[~resultado_colisao]
        self._Objetos_de_Tela["powerups"].Colisor.Redefinir_Posicoes(
                                             self._Objetos_de_Tela["powerups"].Colisor.x[~resultado_colisao],
                                             self._Objetos_de_Tela["powerups"].Colisor.y[~resultado_colisao]
                                             )
      




if __name__ == "__main__":


    jogo = MyGame()

    jogo.run()

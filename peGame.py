import arcade
import arcade.gui
from time import perf_counter

from input import InputReader
from objects import Player, PowerUpsList


SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE  = "Starting Template"


class TimeTracker():
    def __init__(self, ini_time) -> None:
        self.time0 = ini_time
        self.dT    = 0.0

    def get_dT(self):
        return self.dT
    def update_dT(self):
        self.dT = perf_counter() - self.time0
    def reset_t0(self, init_val = 0.0):
        self.time0 = perf_counter() - init_val

class MyGame(arcade.Window):
    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self._Objetos_de_Tela = {
                                 "powerups" : PowerUpsList(10, SCREEN_WIDTH, SCREEN_HEIGHT),
                                 "jogador"  : Player(SCREEN_WIDTH, SCREEN_HEIGHT)
                                }

        self._poweup_move = False

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.restart_button = arcade.gui.UIFlatButton(
            text="Reiniciar",
            width=200,
            height=50,
            x=SCREEN_WIDTH // 2 - 100,
            y=0.3 * SCREEN_HEIGHT
        )

        # Add a callback for when the button is clicked
        @self.restart_button.event("on_click")
        def on_click_restart(event):
            self.restart_game()  # We'll define this function below

        self.manager.add(self.restart_button)
        self.restart_button.visible = False



        arcade.set_background_color(arcade.color.AMAZON)
        self.currentkeys     = InputReader()
        self.timeline        = TimeTracker(perf_counter())

        self.on_key_press   = self.currentkeys.set_keys_on
        self.on_key_release = self.currentkeys.set_keys_off

        self.score_text = arcade.Text(
                "Score: 0",
                0.05 * SCREEN_WIDTH, 0.90 * SCREEN_HEIGHT,
                arcade.color.WHITE,
                30,
                anchor_x="left"
            )

        self.text_paused = arcade.Text(
            "Jogo esta pausado",
            0.0 * SCREEN_WIDTH, 0.5 * SCREEN_HEIGHT,
            arcade.color.RED, 50,
            anchor_x="center"
        )

        self.text_end_game = arcade.Text(
            "Jogo acabou!",
            0.5*SCREEN_WIDTH, 0.7*SCREEN_HEIGHT,
            arcade.color.RED, 50,
            anchor_x = 'center'
        )
        self.text_final_score = arcade.Text(
            "Score Final: 0",
            0.5*SCREEN_WIDTH, 0.5*SCREEN_HEIGHT,
            arcade.color.RED, 50,
            anchor_x = 'center'
        )        
        self.text_authors = arcade.Text(
            "Por Malyk & Pedro",
            0.95*SCREEN_WIDTH, 0.05*SCREEN_HEIGHT,
            arcade.color.WHITE, 11,
            anchor_x = 'right'
        )   





    def on_draw(self):

        self.clear()

        if len(self._Objetos_de_Tela["powerups"].lista_powerups) > 0 :
            if self.currentkeys.get_current_key_value(arcade.key.ESCAPE):
                self.text_paused.draw()
                self.timeline.reset_t0(self.timeline.get_dT())
            else:
                self.Reset_Timeline()
                for _,  obj in self._Objetos_de_Tela.items():
                    obj.Mover(self.currentkeys, mover_poweups =  self._poweup_move)
                self._poweup_move = False
                self.colisor()


            self.score_text.text = f"Score: {self._Objetos_de_Tela['jogador'].score}"
            self.score_text.draw()


        for _, obj in self._Objetos_de_Tela.items():
            obj.Desenhar()


        if len(self._Objetos_de_Tela["powerups"].lista_powerups) == 0 :

            self.text_end_game.draw()
            
            self.text_final_score.text = f"Score Final: {self._Objetos_de_Tela['jogador'].score}"
            self.text_final_score.draw()
            
            self.restart_button.visible = True
            
        self.text_authors.draw()
        self.manager.draw()


    def restart_game(self):
        self._Objetos_de_Tela["powerups"].Resetar()
        
        self._Objetos_de_Tela["jogador"].posicao[0] = SCREEN_WIDTH/2
        self._Objetos_de_Tela["jogador"].posicao[1] = SCREEN_HEIGHT/2
        
        self._Objetos_de_Tela["jogador"].score = 0
        self.timeline.time0 = perf_counter()
        self.restart_button.visible = False


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


        self._Objetos_de_Tela["jogador"].score = self._Objetos_de_Tela["jogador"].score + int(resultado_colisao.sum()*100)

        self._Objetos_de_Tela["powerups"].lista_powerups = self._Objetos_de_Tela["powerups"].lista_powerups[~resultado_colisao]
        self._Objetos_de_Tela["powerups"].Colisor.Redefinir_Posicoes(
                                             self._Objetos_de_Tela["powerups"].Colisor.x[~resultado_colisao],
                                             self._Objetos_de_Tela["powerups"].Colisor.y[~resultado_colisao]
                                             )
      




if __name__ == "__main__":


    jogo = MyGame()

    jogo.run()

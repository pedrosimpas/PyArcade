import arcade
import numpy as np
from hitbox import Circle_Hit_Box, Hit_Box
import random

class ScreenObject():
    def __init__(self) -> None:
        pass 
    def Mover(self, inInputKey, **kwargs):
        pass
    def Colidir(self, **kwargs):
        pass
    def Desenhar(self, **kwargs):
        pass

class Player(ScreenObject):
    score       : int   = 0
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT) -> None:
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH  = SCREEN_WIDTH

        self.player_size : float = self.SCREEN_WIDTH/50

        self.posicao = np.array([self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2])
        self.hit_box = Circle_Hit_Box(Npontos = 4, raio = self.player_size)

    def Mover(self, inInputKey, **kwargs):
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
        elif self.posicao[1] + self.player_size > self.SCREEN_HEIGHT:
            self.posicao[1] = self.SCREEN_HEIGHT - self.player_size

        if self.posicao[0] - self.player_size < 0.0:
            self.posicao[0] = self.player_size
        elif self.posicao[0] + self.player_size > self.SCREEN_WIDTH:
            self.posicao[0] = self.SCREEN_WIDTH - self.player_size

    def Desenhar(self, **kwargs):
        arcade.draw_circle_filled(self.posicao[0], self.posicao[1], self.player_size, arcade.color.BLUE)

    def Colidir(self, **kwargs):
        return self.hit_box.Colidir(self.posicao, kwargs["colisor"])


class Frutas(ScreenObject):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, SPRITE_SCALING = 1.0/7.5) -> None:
        self.SCREEN_HEIGHT  = SCREEN_HEIGHT
        self.SCREEN_WIDTH   = SCREEN_WIDTH
        self.SPRITE_SCALING = SPRITE_SCALING
        self._sprite = arcade.Sprite("./sprites/fruta_jogo.png", self.SPRITE_SCALING)

        self._sprite.center_x, self._sprite.center_y = self.SCREEN_WIDTH/2 + 50, self.SCREEN_HEIGHT/2 + 50

        self.hit_box = Circle_Hit_Box(Npontos = 10, raio = self.SCREEN_WIDTH/50)

    def Mover(self, inInputKey, **kwargs):
        self._sprite.center_x = kwargs["x"]
        self._sprite.center_y = kwargs["y"]

    def Desenhar(self, **kwargs):
        self._sprite.draw()

    def Colidir(self, **kwargs):
        pass 

    def Posicao(self):
        return self._sprite.center_x, self._sprite.center_y


class Colisor_Lista_Fruta(Hit_Box):
    def __init__(self, inXlist, inYlist, raio) -> None:
        self.x    = inXlist
        self.y    = inYlist
        self.raio = raio

    def FuncaoColisao(self, inX, inY, player_radius):
        return ((inX - self.x)**2 + (inY - self.y)**2 <= (self.raio + player_radius)**2)

    def Redefinir_Posicoes(self, inX, inY):
        self.x = inX
        self.y = inY


class PowerUpsList():
    def __init__(self, Npowerups: int, SCREEN_WIDTH, SCREEN_HEIGHT) -> None:
        self.SCREEN_HEIGHT   = SCREEN_HEIGHT
        self.SCREEN_WIDTH    = SCREEN_WIDTH
        self.Npowerups       = Npowerups
        self.Colisor         = Colisor_Lista_Fruta(np.array([]), np.array([]), self.SCREEN_WIDTH/50)
        self.lista_powerups = np.array([Frutas(self.SCREEN_WIDTH, self.SCREEN_HEIGHT) for _ in range(self.Npowerups)])

        self.lista_powerups = np.array(self.lista_powerups)
        self.Mover(False, mover_poweups = True)


    def Mover(self, inInputKey, **kwargs):
        if kwargs["mover_poweups"]:
            self.Colisor.Redefinir_Posicoes(
                                             np.random.uniform(0, self.SCREEN_WIDTH, len(self.lista_powerups)),
                                             np.random.uniform(0, self.SCREEN_HEIGHT, len(self.lista_powerups))
            )
            for ipu, poweup in enumerate(self.lista_powerups):
                poweup.Mover(
                            None, 
                            x = self.Colisor.x[ipu], 
                            y = self.Colisor.y[ipu]
                            )
            

    def Desenhar(self):
        for powerup in self.lista_powerups:
            powerup.Desenhar()

    def Colidir(self, **kwargs):
        return self.Colisor.FuncaoColisao(kwargs["xcentral"], kwargs["ycentral"], kwargs["player_radius"])

import arcade

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
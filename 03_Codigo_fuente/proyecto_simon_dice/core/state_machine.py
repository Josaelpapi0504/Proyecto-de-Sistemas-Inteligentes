from states.idle import IdleState
from states.sequence import SequenceState
from states.user_input import UserInputState

class SimonStateMachine:
    # CORRECCIÓN: El orden ahora es (kb, leds, display, sound) para coincidir con main.py
    def __init__(self, kb, leds, display, sound=None):
        self.kb = kb
        self.leds = leds
        self.display = display
        self.sound = sound
        
        self.states = {
            "IDLE": IdleState(self),
            "SEQUENCE": SequenceState(self),
            "USER_INPUT": UserInputState(self)
        }
        
        self.current_state = self.states["IDLE"]
        self.current_state.on_enter()

    def change_state(self, state_name):
        self.current_state = self.states[state_name]
        self.current_state.on_enter()

    def update(self):
        self.current_state.update()
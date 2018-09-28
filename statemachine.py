class StateMachine:

    def __init__(self, initialState):

        self.currentState = initialState
        self.currentState.run()

    def run_all(self, inputs):

        for i in inputs:
            self.currentState = self.currentState.next(i)
            self.currentState.run()


class State:

    def run(self):
        assert 0, "run not implemented"

    def next(self, input):
        assert 0, "next not implemented"

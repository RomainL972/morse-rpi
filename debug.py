import time

class Debug():
    def __init__(self, unit_time):
        self.unit_time = unit_time

        # For signal parsing
        self.last_time = time.time()
        self.last_state = False


        self.started = False

    def parse_signal(self, state):
        current_time = time.time()
        units = round((current_time - self.last_time) / self.unit_time)

        if not self.started and not state:
            return

        if not self.started:
            self.started = True
            self.last_time = time.time()
        print("State :", "0" if state else "1","at",time.time()-self.last_time)
        time.sleep(0.5)

        # if state != self.last_state:
        #     print("Time :",units)
        #     print("\nState :", "ON" if state else "OFF")
        #
        #     self.last_state = state
        #     self.last_time = current_time




class EventEmitter(object):
    """
        Gives the Icarus.Classes a small event based messaging protocol.
    """



    callbacks = None



    def on(self, event_name, callback):
        """
            Register an event.
        """

        if self.callbacks is None:
            self.callbacks = {}

        if event_name not in self.callbacks:
            self.callbacks[event_name] = [callback]
        else:
            self.callbacks[event_name].append(callback)



    def trigger(self, event_name):
        """
            Trigger an event.
        """

        if self.callbacks is not None and event_name in self.callbacks:
            for callback in self.callbacks[event_name]:
                callback(self)




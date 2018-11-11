'''
Copyright 2018
London Lowmanstone IV
All Rights Reserved
'''

from contextlib import contextmanager
import os

def tab(s, how_many=1, tab_style=" "*4, at_start=True):
    '''
    Takes a string and tabs it in the given amount of times.
    The tab style is what the tab looks like. Defaults to 4 spaces.
    at_start: whether or not it should put any tabs at the start
    '''
    tabs = tab_style * how_many
    replaced_string = s.replace("\n", "\n"+tabs)
    if at_start:
        return tabs + replaced_string
    else:
        return replaced_string


def quick_write(function):
    '''Decorator for class methods that makes the logger use its quick writing functionality'''
    def wrapper(*args, **kwargs):
        # args[0] == self
        with args[0].logger.quick_write():
            return function(*args, **kwargs)
    return wrapper

def property_context_manager(property_name):
    '''A decorator that turns the function into a context manager that '''
    old_display_value = self.display
    self.display = display_value
    try:
        yield
    finally:
        self.display = old_display_value

class Logger():
    '''
    This class is a logger that takes in messages and stores them in its "messages" property.
    You can use a filter to determine which messages shouldn't be added based on their types.
    You can also create a new layer of messages, allowing the devlopment of a hierarchy of messages.
    Regardless of the filter, all messages and new layer requests are sent to the "all_data" property.
    This makes it so that if later classes want to use all the data and change formats, they can.
    '''

    def __init__(self, message_filter=lambda _: True, output_file=None, display=False):
        self.message_filter = message_filter
        if output_file is not None:
            self.output_file = os.path.abspath(output_file)
        else:
            self.output_file = None
        self.display = display
        # a list of all of the messages that come through
        # this can be used to retrieve messages that were never sent to the output file
        # upgrade: this should either have a way of being used or be removed
        self.all_data = []
        # this is a layer in the form [message or layer data, ...] where layer data is in the form (layer message, layer)
        self.messages = []
        # in the form [layer, ...]
        self.layers = [self.messages]
        # this is used to ignore entire layers that don't pass through the filter
        self.ignore = False

    def log(self, message, message_tags=None):
        if message_tags is None:
            message_tags = []

        self.all_data.append(self._message_dict(message, message_tags, new_layer=False))
        # make sure the message goes through the filter
        if not self.ignore and self.message_filter(message_tags):
            if not self.ignore:
                self._output(message)
            self.layers[-1].append(message)

    @contextmanager
    def new_layer(self, message, message_tags=None):
        if message_tags is None:
            message_tags = []

        self.all_data.append(self._message_dict(message, message_tags, new_layer=True))
        prev_ignore = self.ignore
        # make sure the layer goes through the filter
        if not prev_ignore:
            passes_filter = self.message_filter(message_tags)
            if passes_filter:
                self._output(message)
                # create the new layer
                previous_layer = self.layers[-1]
                new_layer_data = (message, [])
                previous_layer.append(new_layer_data)
                self.layers.append(new_layer_data[1])
            else:
                # the layer didn't pass through the filter, so just ignore everything in this layer
                self.ignore = True
        try:
            yield
        finally:
            if self.ignore:
                self.ignore = prev_ignore
            else:
                self.layers.pop()

    # upgrade: make the tabbing work correctly
    @contextmanager
    def set_display(self, display_value):
        '''Set the display value within the context'''
        old_display_value = self.display
        self.display = display_value
        try:
            yield
        finally:
            self.display = old_display_value

    @contextmanager
    def quick_write(self):
        '''Opens the file for faster use within the context'''
        should_del = False
        if self.output_file:
            if not hasattr(self, "open_output_file"):
                self.open_output_file = open(self.output_file, "a")
                should_del = True
        try:
            yield
        finally:
            if should_del:
                del self.open_output_file

    @contextmanager
    def new_message_filter(self, new_message_filter):
        '''Set the message filter within the context'''
        old_message_filter = self.message_filter
        self.message_filter = new_message_filter
        try:
            yield
        finally:
            self.message_filter = old_message_filter

    def __repr__(self):
        def layer_to_string(layer):
            ans = ""
            for message_or_layer_data in layer:
                if isinstance(message_or_layer_data, str): # it's a message
                    message = message_or_layer_data
                    ans += message + "\n"
                else: # it's layer data
                    layer_message, inner_layer = message_or_layer_data
                    ans += layer_message+"\n"+tab(layer_to_string(inner_layer))+"\n"
            # take off the trailing new line and return the result
            return ans[:-1]
        return layer_to_string(self.messages)

    def _message_dict(self, message, message_tags, new_layer=False):
        return {"message":message, "message tags":message_tags, "new layer":new_layer}

    def _output(self, message):
        if not isinstance(message, str):
            message = str(message)
        tabbed_message = tab(message, how_many=len(self.layers) - 1)
        if self.output_file is not None:
            # add a new line to the end (printing does this automatically)
            write_message = tabbed_message + "\n"
            if hasattr(self, "open_output_file"):
                self.open_output_file.write(write_message)
            else:
                with open(self.output_file, "a") as f:
                    f.write(write_message)
        if self.display:
            print(tabbed_message)

class PositiveFilter:
    '''Only lets through certain tags'''
    def __init__(self, tags):
        self.valid_tags = tags

    def __call__(self, message_tags):
        for message_tag in message_tags:
            if message_tag in self.valid_tags:
                return True
        return False

class NegativeFilter:
    '''Supresses certain tags'''
    def __init__(self, tags):
        self.invalid_tags = tags

    def __call__(self, message_tags):
        for message_tag in message_tags:
            if message_tag in self.invalid_tags:
                return False
        return True

class SilentFilter(PositiveFilter):
    '''Doesn't let any tags through'''
    def __init__(self):
        super().__init__([])

class NoFilter(NegativeFilter):
    '''Lets everything through'''
    def __init__(self):
        super().__init__([])


if __name__ == "__main__":
    l = Logger(NegativeFilter("ignore"))
    l.log("before layer")
    with l.new_layer("welcome layer", ["new layer"]):
        l.log("inside layer")
        with l.new_layer("starting double layer", []):
            l.log("in double")
            with l.new_message_filter(SilentFilter()):
                l.log("in double trouble!")
    l.log("outside layer")
    # print(l.messages)
    # print(l.all_data)
    # print(l)
    print("done")

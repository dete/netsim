
class Packet:
    def __init__(self, source, destination, data):
        from node import Node

        if not isinstance(source, Node):
            raise TypeError("source must be a Node object")
        if not isinstance(destination, Node):
            raise TypeError("destination must be a Node object")
        self.source = source
        self.destination = destination
        self.data = data

    def __repr__(self):
        return f"Packet(source={self.source.id}, destination={self.destination.id}, data={self.data})"

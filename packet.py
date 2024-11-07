class Packet:
    def __init__(self, source, destination, data):
        self.source = source
        self.destination = destination
        self.data = data

    def __repr__(self):
        return f"Packet(source={self.source.id}, destination={self.destination.id}, data={self.data})"

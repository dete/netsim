class Strategy:
    def __init__(self):
        self.network = None
        self.node = None

    def set_network(self, network, node):
        self.network = network
        self.node = node

    def get_forward_list(self, sender, codeword_id):
        raise NotImplementedError

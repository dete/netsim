class Strategy:
    def __init__(self):
        self.network = None
        self.node_id = None

    def set_network(self, network, node_id):
        self.network = network
        self.node_id = node_id

    def get_foward_list(self, sender, codeword_id):
        raise NotImplementedError

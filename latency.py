class LatencyModel:
    def __init__(self, latency_data,
            provider_list=[],
            cross_provider_latency_multiplier=1.0,
            cross_provider_loss_multiplier=1.0,
            min_loss=0, max_loss=0):

        # find the largest latency value in the data
        self.max_latency = 0
        for _, v in latency_data.items():
            for _, lat in v.items():
                self.max_latency = max(self.max_latency, lat)

        self.latency_data = latency_data
        self.has_providers = (len(provider_list) > 0)

        cities = latency_data.keys()

        if self.has_providers:
            self.locations = []
            for city in cities:
                for provider in provider_list:
                    self.locations.append(f"{city} ({provider})")
        else:
            self.locations = cities

        self.cross_provider_latency_multiplier = cross_provider_latency_multiplier
        self.cross_provider_loss_multiplier = cross_provider_loss_multiplier

        if min_loss > max_loss:
            print("Invalid loss ratios")
            exit()

        if max_loss == 0:
            self.has_loss = False
        else:
            self.has_loss = True
            self.min_loss = min_loss
            self.max_loss = max_loss

    def get_latency(self, locA, locB):
        if not self.has_providers:
            return self.latency_data[locA][locB]
        else:
            # Extract city and provider names
            partsA = locA.split(" (")
            cityA = partsA[0]
            provA = partsA[1].rstrip(")")

            partsB = locB.split(" (")
            cityB = partsB[0]
            provB = partsB[1].rstrip(")")
            
            # Get base latency
            base_latency = self.latency_data[cityA][cityB]
            
            # Apply latency factor if providers differ
            if provA != provB:
                return base_latency * self.cross_provider_latency_multiplier
            else:
                return base_latency

    def get_loss_ratio(self, locA, locB):
        if not self.has_loss:
            return 0

        if not self.has_providers:
            latency = self.get_latency(locA, locB)

            # assume that the packet loss ratio increases with latency
            return self.min_loss + \
                (self.max_loss - self.min_loss) * (latency / self.max_latency)
        else:
            # Extract city and provider names
            partsA = locA.split(" (")
            cityA = partsA[0]
            provA = partsA[1].rstrip(")")

            partsB = locB.split(" (")
            cityB = partsB[0]
            provB = partsB[1].rstrip(")")
            
            # Get base latency
            base_latency = self.latency_data[cityA][cityB]
            base_loss = self.min_loss + \
                (self.max_loss - self.min_loss) * (base_latency / self.max_latency)

            # Apply loss factor if providers differ
            if provA != provB:
                return base_loss * self.cross_provider_loss_multiplier
            else:
                return base_loss



def test_latency_model():
    from latency_data import latency_data
    # Test with real latency data
    model = LatencyModel(latency_data)
    assert model.get_latency("NewYork", "London") == 35
    assert model.get_latency("Tokyo", "Singapore") == 30
    assert model.get_latency("SanFrancisco", "LosAngeles") == 15

    # Test with providers
    model_with_providers = LatencyModel(latency_data, provider_list=["AWS", "GCP", "MSA"], 
                                        cross_provider_latency_multiplier=1.5)
    
    assert model_with_providers.get_latency("NewYork (AWS)", "London (AWS)") == 35
    assert model_with_providers.get_latency("NewYork (AWS)", "London (GCP)") == 52.5
    assert model_with_providers.get_latency("Tokyo (MSA)", "Singapore (MSA)") == 30
    assert model_with_providers.get_latency("Tokyo (MSA)", "Singapore (AWS)") == 45

    # Test with small custom latency data
    small_latency_data = {
        "A": {"A": 0, "B": 10, "C": 20},
        "B": {"A": 10, "B": 0, "C": 15}, 
        "C": {"A": 20, "B": 15, "C": 0}
    }
    
    small_model = LatencyModel(small_latency_data)
    assert small_model.get_latency("A", "B") == 10
    assert small_model.get_latency("B", "C") == 15
    assert small_model.get_latency("A", "C") == 20

    # Test loss ratios
    loss_model = LatencyModel(small_latency_data, min_loss=0.01, max_loss=0.05)
    
    assert abs(loss_model.get_loss_ratio("A", "B") - 0.03) < 0.001
    assert abs(loss_model.get_loss_ratio("A", "C") - 0.05) < 0.001
    
    # Test loss ratios with providers
    loss_model_with_providers = LatencyModel(small_latency_data, provider_list=["AWS", "GCP", "MSA"],
                                           min_loss=0.01, max_loss=0.05,
                                           cross_provider_loss_multiplier=1.5)
    
    assert abs(loss_model_with_providers.get_loss_ratio("A (AWS)", "B (AWS)") - 0.03) < 0.001
    assert abs(loss_model_with_providers.get_loss_ratio("A (AWS)", "B (GCP)") - 0.045) < 0.001

    print("All latency model tests passed!")

if __name__ == "__main__":
    test_latency_model()


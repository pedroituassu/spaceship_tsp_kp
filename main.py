from typing import NamedTuple, List


class Resource(NamedTuple):
    name: str
    weight: float
    value: float


class Coordinates(NamedTuple):
    x: float
    y: float
    z: float


class Planet(NamedTuple):
    name: str
    coord: Coordinates
    resources: List[Resource]


class Spaceship:
    max_weight: float
    current_weight: float
    current_value: float
    resources: List[Resource]

    def __init__(self, max_weight: float):
        self.max_weight = max_weight
        self.current_weight = 0
        self.current_value = 0
        self.resources = []

    def __str__(self):
        resources_names = [resource.name for resource in self.resources]
        return ("Value=[" + self.current_value + "] - Weight=[" 
                + self.current_weight + "/" + self.max_weight 
                + "] - Resources=" + resources_names)

    def load_resources(self, resources: List[Resource]):
        sorted_resources = sorted(resources, key=lambda r: r.value / r.weight,
                                  reverse=True)

        for resource in sorted_resources:
            remaining_weight = self.max_weight - self.current_weight

            if remaining_weight <= 0:
                return False

            if resource.weight <= remaining_weight:
                self.resources.append(resource)
                self.current_weight += resource.weight
                self.current_value += resource.value
            else:
                fraction = remaining_weight / resource.weight
                partial_weight = resource.weight * fraction
                partial_value = resource.value * fraction

                partial_resource = Resource(name=resource.name,
                                            weight=partial_weight,
                                            value=partial_value)

                self.resouces.append(partial_resource)
                self.current_weight += partial_resource.weight
                self.current_value += partial_resource.value

                return True
        return True

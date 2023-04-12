import csv
import os

import pygame


class Level:
    def __init__(self, path, image_map):
        self.layers = []
        self.collision_map = []
        for idx, layer in enumerate(sorted(os.listdir(path), key=lambda x: int(x.split()[-1].split(".")[0]))):
            self.layers.append([])
            # if idx == 1:
            #     self.collision_map.append([])
            with open(os.path.join(path, layer)) as file:
                reader = csv.reader(file, delimiter=",")
                for row in reader:
                    self.layers[-1].append([])
                    if idx == 1:
                        self.collision_map.append([])
                    for cell in row:
                        self.layers[-1][-1].append(image_map.get(cell))
                        if idx == 1:
                            self.collision_map[-1].append(cell in image_map)

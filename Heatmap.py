import numpy as np
import matplotlib.pyplot as plt
from collections import deque

class Heatmap:
# multiple Agents
# current locations
# input current positions


    def __init__(self, keep_track_of_steps=200, style='Blues', fixed_color_scheme=False):
        self.maps = deque()
        self.keep_track_of_steps = keep_track_of_steps
        self.style = style
        self.fixed_color_scheme = fixed_color_scheme

    def add_map(self, map):
        self.maps.append(map)
        if len(self.maps) > self.keep_track_of_steps:
            self.maps.popleft()


    def get_heatmap(self, num_steps=None):
        if num_steps is None:
            num_steps = self.keep_track_of_steps
        if num_steps > self.keep_track_of_steps:
            raise Exception("can't show map, too many steps")

        num_steps = min(len(self.maps),num_steps)
        sum_map = sum([self.maps[-(i+1)] for i in range(num_steps)])

        return sum_map

    def show_heatmap(self, num_steps=None):
        if num_steps is None:
            num_steps = self.keep_track_of_steps
        if num_steps > self.keep_track_of_steps:
            raise Exception("can't show map, too many steps")

        heat_map = self.get_heatmap(num_steps).astype(float)
        heat_map /= float(num_steps)

        # Plot the heatmap
        fig, ax = plt.subplots()
        im = ax.imshow(heat_map,cmap=self.style)
        if self.fixed_color_scheme:
            im.set_clim(0,1)
        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        fig.tight_layout()
        plt.show()

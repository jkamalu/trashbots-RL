import numpy as np
import matplotlib.pyplot as plt
from collections import deque

class Heatmap:
# multiple Agents
# current locations
# input current positions


    def __init__(self, dim, keep_track_of_steps=200):
        self.maps = deque()
        self.keep_track_of_steps = keep_track_of_steps

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


        heat_map = self.get_heatmap(num_steps)
        sum_all_positions = sum(sum(heat_map))#sum over columns and rows
        heat_map /= sum_all_positions

        # Plot the heatmap
        fig, ax = plt.subplots()
        im = ax.imshow(heat_map,cmap="Blues")
        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("someone was here", rotation=-90, va="bottom")
        fig.tight_layout()
        plt.show()

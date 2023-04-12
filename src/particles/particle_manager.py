import itertools

import pygame

from .particles import Particle
from src import animation, common, renderer


class ParticleManager:
    def __init__(self, sprite_sheet):
        data = sprite_sheet.data[""]
        durations = [0] + [d["duration"] for d in data]
        ranges = [
            range(t1, t2)
            for t1, t2 in itertools.pairwise(itertools.accumulate(durations))
        ]
        self.max_time = ranges[-1].stop
        self.mapping = {
            i: image
            for range_, image in zip(ranges, (d["image"] for d in data))
            for i in range_
        }
        self.particles = []

    def spawn(self, pos, velocity, count=1, max_time=None):
        for _ in range(count):
            self.particles.append(Particle(pos=pos, velocity=velocity, time=0, max_time=max_time))

    def update(self):
        for particle in self.particles:
            particle.time += int(common.dt * 1000)
            particle.pos += particle.velocity
        self.particles = [
            p
            for p in self.particles
            if p.time < (p.max_time if p.max_time is not None else self.max_time)
        ]

    def render(self, target=None, special_flags=0):
        for particle in self.particles:
            img = self.mapping[particle.time]
            rect = self.mapping[particle.time].get_rect(center=particle.pos)
            renderer.render(
                img,
                rect,
                target=target,
                special_flags=special_flags,
            )

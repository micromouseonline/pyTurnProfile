#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Project: <<project>>
# File:    trajectory.py
# File Created: Thursday, 5th January 2023 2:10:17 pm
# Author: Peter Harrison 
# -----
# Last Modified: Friday, 6th January 2023 12:03:58 pm
# -----
# Copyright 2022 - 2023 Peter Harrison, Micromouseonline
# -----
# Licence:
# MIT License
# 
# Copyright (c) 2023 Peter Harrison
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###

from pose import Pose
from parameters import TurnParameters, default_params
import numpy as np


class Profile:
    def __init__(self, params = None):
        self.length = 0
        self.params = params
        pass

    def setup(self, params : TurnParameters):
        self.params = params
        pass

    def get_omega(self,p,speed): # 0 <= p <= 1.0 
        if self.params is None:
            return 0.0
        x = max(0.0,p)
        x = min(1.0,p)
        x = p * self.params.length
        return x

class Cubic(Profile):
    def __init__(self):
        super().__init__()

    def setup(self, params : TurnParameters):
        self.params = params
        self.k = 6.0*self.params.angle/ self.params.length

    def get_omega(self,p,speed):
        omega = speed * self.k * p * (1-p)
        phase = 1
        if p > 0.5:
            phase = 3
        return (omega,phase)

class Trapezoid(Profile):
    def __init__(self):
        super().__init__()

    def setup(self, params : TurnParameters):
        self.params = params
        self.arc_omega = np.degrees(params.speed / params.arc_radius)
        self.transition_angle = params.delta * self.arc_omega / (2.0 * params.speed)
        self.arc_angle = params.angle - 2 * self.transition_angle
        self.arc_length = params.speed * self.arc_angle / self.arc_omega
        self.length = 2 * params.delta + self.arc_length

    def get_omega(self,p,speed):
        phase = 1
        distance = p*self.length
        if distance < self.params.delta:
            omega = self.arc_omega * distance/self.params.delta 
        elif distance < self.params.delta + self.arc_length:
            omega = self.arc_omega
            phase = 2
        else:
            distance = distance - self.params.delta - self.arc_length
            omega = self.arc_omega * (1.0 - distance/self.params.delta)
            phase = 3
        (omega)
        return (omega,phase)

class Quadratic(Profile):
    def __init__(self):
        super().__init__()

    def setup(self, params : TurnParameters):
        self.params = params
        self.arc_omega = np.degrees(params.speed / params.radius)
        self.transition_angle = params.delta * self.arc_omega / (3.0 * params.speed)
        self.arc_angle = params.angle - 2 * self.transition_angle
        self.arc_length = params.speed * self.arc_angle / self.arc_omega
        self.length = 2 * params.delta + self.arc_length

    def get_omega(self,p,speed):
        phase = 1
        distance = p*self.length
        if distance < self.params.delta:
            q = distance / self.params.delta
            omega = self.arc_omega * q * (2.0 - q)
        elif distance < self.params.delta + self.arc_length:
            omega = self.arc_omega
            phase = 2
        else:
            q = (self.length - distance)/self.params.delta
            omega = self.arc_omega * q * (2.0 - q)
            phase = 3
        return (omega,phase)

class Sinusoid(Profile):
    def __init__(self):
        super().__init__()

    def setup(self, params : TurnParameters):
        self.params = params
        self.arc_omega = np.degrees(params.speed / params.radius)
        self.transition_angle = params.delta * self.arc_omega / (np.pi * params.speed)
        self.arc_angle = params.angle - 2 * self.transition_angle
        self.arc_length = params.speed * self.arc_angle / self.arc_omega
        self.length = 2 * params.delta + self.arc_length

    def get_omega(self,p,speed):
        phase = 1
        distance = p*self.length
        if distance < self.params.delta:
            q = distance / self.params.delta
            omega = self.arc_omega * np.sin(q * np.pi/2) 
        elif distance < self.params.delta + self.arc_length:
            omega = self.arc_omega
            phase = 2
        else:
            q = (self.length - distance) / self.params.delta
            distance = distance - self.params.delta - self.arc_length
            omega = self.arc_omega * (np.sin(q * np.pi/2))
            phase = 3
        return (omega, phase)

class FullSinusoid(Profile):
    def __init__(self):
        super().__init__()

    def setup(self, params : TurnParameters):
        self.params = params
        radius = 4.0*params.delta/(np.pi*np.radians(params.angle))
        self.arc_omega = np.degrees(params.speed / radius)
        self.length = 2 * params.delta
        

    def get_omega(self,p,speed):
        distance = p * self.length
        omega = self.arc_omega * np.sin(np.pi * p)
        phase = 1
        if p > 0.5:
            phase = 3
        return (omega, phase)


class Trajectory:
    def __init__(self):
        self.path_length = 0.0 # mm
        self.turn_angle = 0.0 # radians
        self.start_x = 0.0 # mm
        self.start_y = 0.0 # mm
        self.start_angle = 0.0 # radians
        self.speed = 0.0 # mm/s
        self.k_slip = 10000.0 
        self.delta_t = 0.001
        #
        self.n_items = 0
        self.end_time = 0.0
        self.time = None
        #
        self.theta_ideal = None
        self.omega_ideal = None
        self.x_ideal = None
        self.y_ideal = None
        #
        self.beta = None
        self.theta_actual = None
        self.omega_actual = None
        self.x_actual = None
        self.y_actual = None
        #
        self.profiler = None

    def set_params(self, start_x, start_y, start_angle, speed):
        # self.turn_angle = np.radians(turn_angle) # radians
        self.start_x = start_x # mm
        self.start_y = start_y # mm
        self.start_angle = np.radians(start_angle) # radians
        self.speed = speed # mm/s
        self.reset_data()
        #        

    def reset_data(self):
        if self.speed < 1:
            return
        self.end_time = self.profiler.length/self.speed
        self.n_items = int(self.end_time/self.delta_t)
        self.theta_ideal = np.zeros(self.n_items)
        self.omega_ideal = np.zeros(self.n_items)
        self.x_ideal = np.zeros(self.n_items)
        self.y_ideal = np.zeros(self.n_items)
        self.beta = np.zeros(self.n_items)
        self.theta_actual = np.zeros(self.n_items)
        self.omega_actual = np.zeros(self.n_items)
        self.x_actual = np.zeros(self.n_items)
        self.y_actual = np.zeros(self.n_items)
        
    def set_profiler(self,profiler):
        self.profiler = profiler
        
    def set_speed(self, speed):
        self.speed = speed

    def set_start_xy(self,x,y):
        self.start_x = x
        self.start_y = y

    def set_start_angle(self,angle):
        self.start_angle = angle

    def calculate(self):
        # if self.n_items == 0:
        #     print("no parameters")
        #     return
        if self.profiler is None:
            print("no profiler")
            return
        self.reset_data()        
        print(f"{self.end_time:.3f} {self.n_items}")
        self.time = np.linspace(0,self.end_time,self.n_items)
        print("calculating...")
        for i,t in enumerate(self.time):
            p = t/self.end_time
            omega,phase = self.profiler.get_omega(p,self.speed)
            print(f"{t:.4f}  {omega:.4f}")

    






if __name__ == "__main__":
    trajectory = Trajectory()
    profile = Trapezoid()
    trajectory.set_profiler(profile)
    profile.setup(default_params["SS90F"])

    trajectory.set_start_xy(0,0)   
    trajectory.set_start_angle(0)   
    trajectory.set_speed(1000)

    trajectory.calculate()
    print(default_params["SS90F"])


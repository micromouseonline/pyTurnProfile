#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Project: <<project>>
# File:    trajectory.py
# File Created: Thursday, 5th January 2023 2:10:17 pm
# Author: Peter Harrison 
# -----
# Last Modified: Friday, 6th January 2023 7:03:13 pm
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
# from profile import  TurnProfile,  Trapezoid
from profilers import *
from pose import Pose
from parameters import TurnParameters, default_params
import numpy as np



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
        self.n_items = 1+int(0.5+self.end_time/self.delta_t)
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
        self.reset_data()
        
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
        self.theta_ideal[0] = self.start_angle
        print("calculating...")
        for i,t in enumerate(self.time):
            p = t/self.end_time
            omega,phase = self.profiler.get_omega(p)
            self.omega_ideal[i] = omega
        # nast hack for rounding errors


        # now we have the angular velocity as a function of time
        print(self.delta_t)
        self.theta_ideal = np.cumsum(self.omega_ideal * self.delta_t) + self.start_angle
        self.theta_ideal[-1] = self.profiler.params.angle
        
        for i,t in enumerate(self.time):
            # if i > 0:
            #     self.theta_ideal[i] = self.theta_ideal[i-1] + self.omega_ideal[i-1] * self.delta_t
            print(f"{t:.4f}  {self.omega_ideal[i]:.4f}  {self.theta_ideal[i]:.4f}")



if __name__ == "__main__":
    trajectory = Trajectory()
    profile = Cubic()
    trajectory.set_profiler(profile)
    profile.setup(default_params["SS90F"], 1000)

    trajectory.set_start_xy(0,0)   
    trajectory.set_start_angle(0)   
    trajectory.set_speed(1000)

    trajectory.calculate()
    print(default_params["SS90F"])


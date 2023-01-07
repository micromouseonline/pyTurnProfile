#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Project: <<project>>
# File:    trajectory.py
# File Created: Thursday, 5th January 2023 2:10:17 pm
# Author: Peter Harrison 
# -----
# Last Modified: Saturday, 7th January 2023 1:15:38 am
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
        self.k_grip = 100.0 
        self.delta_t = 0.001
        #
        self.n_items = 0
        self.end_time = 0.0
        self.time = None
        #
        self.phase = None
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
        self.profiler : TurnProfile = None
        # self.parameters : TurnParameters = None
        

    def is_configured(self):
        # if self.parameters == None:
        #     print("no parameters")
        #     return False
        if self.profiler is None:
            print("no profiler")
            return False
        return True
        

    def reset_data(self):
        if not self.is_configured():
            return
        if self.speed < 1:
            return
        self.end_time = self.profiler.length/self.speed
        self.n_items = 1+int(0.5+self.end_time/self.delta_t)        
        self.phase = np.zeros(self.n_items)
        self.theta_ideal = np.zeros(self.n_items)
        self.omega_ideal = np.zeros(self.n_items)
        self.x_ideal = np.zeros(self.n_items)
        self.y_ideal = np.zeros(self.n_items)
        self.beta = np.zeros(self.n_items)
        self.theta_actual = np.zeros(self.n_items)
        self.omega_actual = np.zeros(self.n_items)
        self.x_actual = np.zeros(self.n_items)
        self.y_actual = np.zeros(self.n_items)
        
    def set_start(self, start_x, start_y):
        self.start_x = start_x # mm
        self.start_y = start_y # mm
            
    def set_profiler(self,profiler):
        self.profiler = profiler
        

    def set_params(self, params : TurnParameters ):
        # self.parameters = params
        self.speed = params.speed
        self.start_angle = params.startAngle
        self.k_grip = params.k_grip
        self.profiler.setup(params)
        

    def set_start_xy(self,x,y):
        self.start_x = x
        self.start_y = y

    def set_start_angle(self,angle):
        self.start_angle = angle

    def calculate(self):
        if not self.is_configured():
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
            self.phase[i] = phase


        # now we have the angular velocity as a function of time
        print(self.delta_t)
        self.theta_ideal = np.cumsum(self.omega_ideal * self.delta_t) + self.start_angle
        # nast hack for rounding errors
        self.theta_ideal[-1] = self.profiler.params.angle
        x = self.start_x
        y = self.start_y
        for i,angle in enumerate(self.theta_ideal):
            self.x_ideal[i] = x
            self.y_ideal[i] = y
            angle = np.radians(angle)
            x += self.speed * np.cos(angle) * self.delta_t
            y += self.speed * np.sin(angle) * self.delta_t
        self.x_ideal[-1] = x
        self.y_ideal[-1] = y

        # now do it with the slip angle taken into account
        def beta_dot(omega,beta, speed):
            speed = speed/1000.0
            b_dot = -(np.radians(omega) + self.k_grip * np.radians(beta) / speed)
            return np.degrees(b_dot)


        print(self.speed, self.k_grip, self.k_grip/self.speed)
        for i in range(len(self.time)):
            if i > 1:
                omega = self.omega_ideal[i-1]
                last_beta = self.beta[i-1]
                b_dot = beta_dot(omega,last_beta, self.speed)
                self.beta[i] = last_beta + self.delta_t * b_dot
                self.theta_actual[i] = self.theta_ideal[i] + self.beta[i]

        x = self.start_x
        y = self.start_y
        for i,angle in enumerate(self.theta_actual):
            self.x_actual[i] = x
            self.y_actual[i] = y
            x += self.speed * np.cos(np.radians(angle)) * self.delta_t
            y += self.speed * np.sin(np.radians(angle)) * self.delta_t
        self.x_actual[-1] = x
        self.y_actual[-1] = y

        self.omega_actual = np.gradient(self.theta_actual[1:-1])/self.delta_t



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.ticker as tick
    import copy
    trajectory = Trajectory()
    
    profile = Cubic()
    trajectory.set_profiler(profile)
    
    parameters = copy.copy(default_params["SS90F"])
    parameters.speed = 2400.1
    parameters.k_grip = 200.0
    # must we have k_grip < 2 * speed?
    # if so, why?
    trajectory.set_params(parameters)
    
    trajectory.set_start(0,0)
    trajectory.calculate()
    
    print(parameters)
    end_x_ideal = trajectory.x_ideal[-1]
    end_y_ideal = trajectory.y_ideal[-1]
    end_x_actual = trajectory.x_actual[-1]
    end_y_actual = trajectory.y_actual[-1]
    dx = abs(end_x_ideal-end_x_actual)
    dy = abs(end_y_ideal - end_y_actual)

    print(f"{trajectory.x_ideal[-1]:.0f},{trajectory.y_ideal[-1]:.0f}")
    print(f"{trajectory.x_actual[-1]:.0f},{trajectory.y_actual[-1]:.0f}")
    print(f"{dx:.1f},{dy:.1f}")
    # print(trajectory.speed, profile.speed)
    if trajectory.is_configured():
        plt.figure(figsize=(15, 8))
        plt.subplot(1,2,1)    
        ax = plt.gca()
        ax.xaxis.set_major_locator(tick.MultipleLocator(45))
        ax.yaxis.set_major_locator(tick.MultipleLocator(45))
        ax.xaxis.set_minor_locator(tick.MultipleLocator(5))
        ax.yaxis.set_minor_locator(tick.MultipleLocator(5))
        ax.set_aspect('equal', adjustable='box')

        plt.plot(trajectory.x_ideal,trajectory.y_ideal, label = 'Ideal')
        plt.plot(trajectory.x_actual,trajectory.y_actual, label = 'Actual')
        plt.axis([-10, 200, -10, 200])
        plt.grid()
        plt.title(f"Trajectory\nspeed = {trajectory.speed:.0f} mm/s")
        plt.legend(loc = 'upper right')
        plt.subplot(1,2,2,)
        ax = plt.gca()
        # ax.xaxis.set_major_locator(tick.MultipleLocator(0.05))
        # ax.xaxis.set_minor_locator(tick.MultipleLocator(0.01))
        # ax.yaxis.set_major_locator(tick.MultipleLocator(50))
        # ax.yaxis.set_minor_locator(tick.MultipleLocator(10))
        # ax.set_aspect('equal', adjustable='box')

        plt.plot(trajectory.time,trajectory.beta)
        # plt.plot(trajectory.time,trajectory.theta_ideal)
        # plt.plot(trajectory.time,trajectory.theta_actual)
        # plt.plot(trajectory.time,trajectory.omega_ideal, label = 'omega_ideal')
        # plt.plot(trajectory.time[1:-1],trajectory.omega_actual, label = 'omega actual')
        plt.title(f"Angular Velocity\nspeed = {trajectory.speed:.0f} mm/s")
        plt.legend(loc = 'upper right')
        plt.grid()
        plt.show()


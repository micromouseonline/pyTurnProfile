# pyTurnProfile

An application written in Python and using a PyQt5 GUI that simulates a number of different micromouse turn profiles.
The profiles are, so far, only for classic micromouse mazes.

While this is an early version, it should be mostly functional and reasonably accurate. The data and plots are 
updated live as parameters are changed. The turn illustration (upper right) has a progress slider underneath it. 
With that you can see how the mouse moves through the turn and how the sensors see the posts. The angle of the side 
sensors can be adjusted to approximate those on your own mouse.

## Turn Types
There are eight different turn types modelled. They should be largely self-explanatory from the plots. The odd one out 
is the SS90K at the bottom of the list. It models an extra-wide turn around two posts. Currently, the background 
does not have space to illustrate it properly so it is shown here shifted left by half a cell. The SS90K should 
connect two diagonal straights that are two cells apart. 

## Profile types

There are four different turn profiles available. Three of these are segmented turns. That means that the complete 
turn is performed in three phases. From travelling in a straight line, the mouse will transition into a 
constant-radius arc of some defined radius and then, at the right moment transition gently back to straight-line 
motion. The difference between the three types (trapezoidal, sinusoidal and quadratic) is in the function used to 
change the angular velocity between zero and the value needed to maintain the constant-radius central phase.

These transitions always happen over a fixed distance determined by the `delta` parameter. Smaller values of `delta` 
will reduce the turn time but will place a greater load on the tyres as they try to get the mouse turning. the best 
value will depend on the available grip, the width of the mouse and the moment of inertia of the mouse. 

The fourth turn profile (cubic) is different because it varies the angular velocity continuously throughout the turn.
The advantage of this technique is that minimised the angular acceleration and so should result in a smoother turn 
without and rapid changes in angular velocity that may cause the mouse to lose traction. the disadvantage is that 
the peak centripetal acceleration will be a little higher although only for a short time.

There are more details in comment block in the code in the file `turn_profiles.md`

## Turn pivot point

Each turn has a single point that is used, with the start angle, to define the start posiition for that turn. The 
pivot point is a point that the mouse would have to use if it were to perform the turn with an in-place turn. Turn 
like the SS135 that cannot be performed with a single pivot turn, use the position of the first of a pair of points.

For (my) convenience, the origin of the coordinate system is the centre of the top left cell in the diagram, The 
orange lines are the x and y axes. Positive is to the right and downwards as is usual, and annoying, on graphic displays

That actual starting position for the turn is offset back from the pivot point in the direction from which the 
mouse is heading. For example, the SS90F turn could be performed by executing a 90 degree pivot turn at the origin. 
It should be clear that the actual turn must start some distance before that. The offset should not be so great that 
any previous turn may not have finished. It should also allow some extra space so that faster turns can be started 
even earlier to compensate for wheel slip.

## Wheel slip

In this version wheel slip and the effects of slip angle are not fully modelled. The main reason of bringing this 
application up to date and placing it on github is specifically to begin adding in slip angle modelling so if you 
can help, let me know.

# Install and Run
This version was written using Python 3.8.10 running on a Linux machine. You should be able to copy the repository 
to any directory of your choice and run the application with something like:

```python main.py```

The Python packages used are listed in the requirements.txt file and can be installed with

```pip install -r requirements.txt```

## python Virtual Environments
On your machine, you should probably create a Python virtual environment and then install the requirements with

Python virtual environments prevent your global Python installation from becoming infested with multiple modules 
that can upset the proper operation of other Python applications. You may have your own favourite way of creating 
virtual environments and may even use Anaconda which is different again. If not, there are many guides available. 
This one (chosen arbitrarily from Google search) should see you through: https://realpython.com/python-virtual-environments-a-primer/

### UI file

The user interface is designed in a separate file using QtDesigner. This generates the file `pyturnprofile.ui`

Your will need to convert this to the working python version with the command:

` pyuic5 -o ui_pyturnprofile.py pyturnprofile.ui `


## FEEDBACK

If you find errors or inconsistencies, please let me know - prefeably through the issues facility so that others can 
also share.

I am also open to suggestions for changes, improvements and feature suggestions.

---

Peter Harrison

https://micromouseonline.com



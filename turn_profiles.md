# Turn Profiles

## TRAPEZOIDAL PROFILE (clothoid)

The trapezoidal turn has the robot transition from straight-line motion to
a constant angular velocity arc by linearly increasing the angular velocity
over a fixed distance (lambda). During this portion of the turn, the robot
path follows a clothoid curve.

Some builders specify a time for a reference turn rather than a distance
for this accelerating portion. that has some advantages but the time will
change as the robot tries to run the turn faster. A little bit of calculation
reveals that the distance always comes out the same so it is just easier
to specify a distance rather than a time and the resulting turn path
is easily made invariant with robot speed.

After the constant arc, the robot 'unwinds' the turn with another linear
change to angular velocity

Four parameters are needed to define the turn:
 - turn minimum radius - that is for the constant arc portion, in mm
 - total turn angle - in degrees
 - lambda - the robot transitions distance in mm
 - speed - the robot forward velocity. Constant through the turn

Everything else is calculated from that.

For this turn type only, setting the lambda to be the same as
the mouse radius causes the peak lateral and forward wheel accelerations
to be about the same

## SINUSOIDAL PROFILE

Like the trapezoidal turn, this turn has tyhree phases. The central constant
radius phase is the same but the transitions in and out have the angular
velocity follow a portion of a sinusoidal profile.

This profile is intended to keep the forces on the tyres within its traction
circle at all times and provides a smooth transition as the robot reaches its
maximum angular velocity.

Some builders specify a time for a reference turn rather than a distance
for this accelerating portion. that has some advantages but the time will
change as the robot tries to run the turn faster. A little bit of calculation
reveals that the distance always comes out the same so it is just easier
to specify a distance rather than a time and the resulting turn path
is easily made invariant with robot speed.

After the constant arc, the robot 'unwinds' the turn with another sinusoidal
change to angular velocity

Four parameters are needed to define the turn:- turn minimum radius - that is for the constant arc portion, in mm
- total turn angle - in degrees
- lambda - the robot transitions distance in mm
- speed - the robot forward velocity. Constant through the turn

Everything else is calculated from that.

For this turn type only, setting the lambda to be the same as
the pi times mouse radius causes the peak lateral and forward wheel accelerations
to be about the same

## QUADRATIC PROFILE

The quadratic turn has three sections, or phases, like the trapezoidal turn.

The difference is that the change in angular velocity is calculated as a
portion of a quadratic function. Like the trapezoidal version, the acceleration
is over a fixed distance.

It is not clear that there is any practical advantage to this profile although
it does significantly ease the transition into and out of the constant radius
phase.

Some builders specify a time for a reference turn rather than a distance
for this accelerating portion. that has some advantages but the time will
change as the robot tries to run the turn faster. A little bit of calculation
reveals that the distance always comes out the same so it is just easier
to specify a distance rather than a time and the resulting turn path
is easily made invariant with robot speed.

After the constant arc, the robot 'unwinds' the turn with another quadratic
change to angular velocity

Four parameters are needed to define the turn:
 - turn minimum radius - that is for the constant arc portion, in mm
 - total turn angle - in degrees
 - lambda - the robot transitions distance in mm
 - speed - the robot forward velocity. Constant through the turn

Everything else is calculated from that.

For this turn type only, setting the lambda to be the same as
the distance between the wheels causes the peak lateral and forward
wheel accelerations to be about the same.
 



## CUBIC PROFILE

The cubic profile is completely different to the other types. It is not
executed in phases and the robot describes a completely smooth path from
start to finish.

In the simulation, Dalpha is not needed because we read the turn length
directly from the UI.

If there is only the start and end points (x1,y1) and (x2,y2) respectively,
then the length is calculated from those. Let d be the euclidean distance
between the points:

 ```distance =  sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))```

then

 ```length = distance / dalpha(turnAngle)```

where turnAngle is in radians, positive is anti-clockwise

the performance metrics can be calculated from the curvature equations
   ```
   turnDistance = length;
   turnOmega = (turnSpeed * k * length * length / 4);
   turnRadius = 4 * length / 6 / RADIANS(turnAngle);
   turnAcceleration = turnSpeed * turnSpeed * 6 * RADIANS(turnAngle) / 4 / length;
   turnAlpha = turnSpeed * k * length;
   ```

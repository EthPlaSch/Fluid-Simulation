----- Exploration into Fluid Simulations -----

----- Overview -----

This project explores my journey into the world of fluid simulations. This project has three files: "Grid_Based_Simulation.py; Particle_Based_Simulation.py; Particle.png.
The first file there is an attempt at the Eulerian method of fluid simulation using grids instead of particles. However this project is incomplete.
The major backbone is in place however the file itself is not anywhere close to a smooth running fluid simulation and has many issues.
The latter two files are a object based simulation and a texture for that simulation. Both files are required for that simulation. This method works by simulating
circle collisions creating somewhat of a ballpit simulation which can look good enough for simple applications.

---- How to Run -----

To run Grid_Based_Simulation.py simply copy the code into a code editor of choice and hit run (the file is a python file to be clear).
To run Particle_Based_Simulation.py also copy the code into a code editor of choice, but be sure to save the image as well and place it in the same directory.

----- How to Use -----

Grid_Based_Simulation.py only has a single input and that is the left arrow key. This is because the project is still very much in development and so has not been fleshed out
with proper user interaction. If you hold the LEFT arrow key a single cells velocity is updated, and you can watch the mess of grid squares in the window update almost at random
on your screen. For some context both simulations use Pyglet as the graphics library. Grid_Based_Simulation.py still has sqaures used for debugging in the window as well as a host
of other strange additions as it is not a final product. I REPEAT - THIS IS NOT A WORKING NOR FINALISED PRODUCT - USE AT OWN RISK. While there is nothing harmful in the file the
velocity values can spiral out of control and result in integers in the x * 10 ^ 200 or more range which could crash the program. YOU HAVE BEEN WARNED.

On the other hand the Particle_Based_Simulation.py is a much more finalised file and the one I recommend you look at. The program will load no issues, shouldn't have any issues with
crashing or obsurd values or anything either. Being a more finalised product there is some proper user interaction. Using the LEFT arrow key, the RIGHT arrow key, and the SPACE bar
you can move the objects left, right, or up. The particles should all fly about in a mostly fluid like manner and eventually settle once more.

----- Credits -----

All the code was written by me, all art assets were created by me, however external resources were used for research and sometimes code (see code for reference when used)

Leong, E. (2009). _An Approach to Accurate Multiple Collision Detection and Response._ https://ericleong.me/old/research/leong09.pdf

Ten Minute Physics. (2022, December 3). _17 - How to write an Eulerian fluid simulator with 200 lines of code [Video]._ YouTube. https://www.youtube.com/watch?v=iKAVRgIrUOU

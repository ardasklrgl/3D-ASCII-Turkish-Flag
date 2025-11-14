import math
import os
import time
import sys

WIDTH, HEIGHT = 50, 50

t_spacing = 0.07
y_spacing = 0.02

r1 = 1
r2 = 2

k2 = 10
k1 = WIDTH * k2 *  3/(8*(r1+r2))

def render(X, Z):
    cosX, sinX = math.cos(X), math.sin(X)
    cosZ, sinZ = math.cos(Z), math.sin(Z)

    output = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    zbuffer = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for T in drange(0, 2*math.pi, t_spacing):
        cosT, sinT = math.cos(T), math.sin(T)

        for Y in drange(0, 2*math.pi, y_spacing):
            cosY, sinY = math.cos(Y), math.sin(Y)

            x = (r2+r1*cosT)*(cosZ*cosY+sinX*sinZ*sinY)-r1*cosX*sinZ*sinT
            y = (r2+r1*cosT)*(cosY*sinZ-cosZ*sinX*sinY)+r1*cosX*cosZ*sinT
            z = cosX*(r2+r1*cosT)*sinY+r1*sinX*sinT + k2

            ooz = 1 / z

            L = cosY*cosT*sinZ-cosX*cosT*sinY - sinX*sinT+cosZ*(cosX*sinT-cosT*sinX*sinY)

            xn = int(WIDTH/2 + k1 * ooz * x)
            yn = int(WIDTH/2 - k1 * ooz * y) # y is negated cuz y is goes up in 3d but down in 2d

            if L > 0 and 0 <= xn < WIDTH and 0 <= yn < HEIGHT and ooz > zbuffer[yn][xn]:
                zbuffer[yn][xn] = ooz

                lumin_index = int(L * 8)
                lumin_index = min(lumin_index, len("'..,-~:;=!*#$@") - 1)

                output[yn][xn] = "'.,-~:;=!*#$@"[lumin_index]
    
    sys.stdout.write("\x1b[H")

    for row in output:
        sys.stdout.write("".join(row) + "\n")
    
    sys.stdout.flush()

def drange(start, stop, step):
    while start < stop:
        yield start
        start += step

X, Y = 0.0, 0.0
os.system("cls" if os.name == "nt" else "clear")

while True:
    render(X, Y)
    X += 0.04
    Y += 0.02
    time.sleep(0.005)

'''
1. Reflection of xyz to the screen
    xn = (k1 * x) / z
    yn = (k1 * y) / z

2. Torus
    r1 = circle radius
    r2 = torus radius - to the center of the circle
    circle with r1 centered at (r2, 0, 0)
    draw the torus by spinning around 0 to 2pi with angle T
    xyz = (r2, 0, 0) + (r1cosT, r1sinT, 0)
    = (r2 + r1cosT, r1sinT, 0)

3. Rotate the torus
    Multiply the torus xyz with rotation matrices to get rotations around the axices
    y-axis rotation by Y degrees, x-axis rot by X degrees, z-axis rot by Z degrees

    (r2 + r1cosT, r1sinT, 0) 
    * ([cosY, 0, sinY], [0, 1, 0], [-sinY, 0, cosY])
    * ([1, 0, 0], [0, cosX, sinX], [0, -sinX, cosX])
    * ([cosZ, sinZ, 0], [-sinZ, cosZ, 0], [0, 0, 1])
    = (r2+r1cosT)(cosZcosY+sinXsinZsinY)-r1cosXsinZsinT //x
    (r2+r1cosT)(cosYsinZ-cosZsinXsinY)+r1cosXcosZsinT //y
    cosX(r2+r1cosT)sinY+r1sinXsinT //z

4. Surface normal for lighting
    We start with a point on the circle
    Rotate the point around the torus' central axis
    Rotate it 2 more times around x and z
    nx ny nz = (cosT, sinT, 0)
    * ([cosY, 0, sinY], [0, 1, 0], [-sinY, 0, cosY])
    * ([1, 0, 0], [0, cosX, sinX], [0, -sinX, cosX])
    * ([cosZ, sinZ, 0], [-sinZ, cosZ, 0], [0, 0, 1])
    
    We chose a lighting direction, (0, 1, -1)
    Remember, the origin is the viewer, x is horizontal, y is vertical, z is straight from our POV
    This lighting source is above and behind the viewer

    To get the luminance, L, of the point of the surface normal, we do a dot product 
    (nx, ny, nz) . (0, 1, -1)
    What this translates to is L = y - z
    We throw away x and subtract z from y to get the L
    =cosYcosTsinZ-cosXcosTsinY-sinXsinT+cosZ(cosXsinT-cosTsinXsinY)

5. Distance of the viewer from the donut, and the rest
    xn = (k1 * x) / z
    yn = (k1 * y) / z
    This makes the donut directly on the viewer. Lets add another constant to be able to visualise it.

    xn = (k1 * x) / (k2 + z)
    yn = (k1 * y) / (k2 + z)

    Pick values for r1, r2, k1, k2
    r1 = 1
    r2 = 2
    k2 = 5
    k1 = screen_width * k2 *  3/(8*(r1+r2)) // calculated based on scale and screensize

6. Print

'''
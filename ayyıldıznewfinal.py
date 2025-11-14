import math
import os
import time
import sys

WIDTH = 200
HEIGHT = 75

t_spacing = 0.07
y_spacing = 0.02

r1_max = 1
r2 = 4
k2 = 7 # away from camera, z offset
k1 = HEIGHT * k2 *  3 / (8 * (r1_max + r2)) # scale factor of projection

def render(X, Z):
    cosX, sinX = math.cos(X), math.sin(X)
    cosZ, sinZ = math.cos(Z), math.sin(Z)

    output = [[' ']*WIDTH for _ in range(HEIGHT)] # the space where the animation will be displayed
    zbuffer = [[0.0]*WIDTH for _ in range(HEIGHT)] # depth of each pixel at (x,y)

    # angle parameter that creates the main circle to be rotated, on the xz plane
    for T in drange(0, 2*math.pi, t_spacing):
        cosT, sinT = math.cos(T), math.sin(T)

        # the angle of the circle rotated around the origin on the xy plane
        for Y in drange(-3.37*math.pi/4, 3.37*math.pi/4, y_spacing):
            cosY, sinY = math.cos(Y), math.sin(Y)

            r1 = r1_max * (1 + cosY) / 2 # radius of the circle slowly decreases, creating the crescent

            # x y z rotation matrices applied all at once
            x = (r2 + r1 * cosT) * (cosZ * cosY + sinX * sinZ * sinY) - (r1 * cosX * sinZ * sinT)
            y = (r2 + r1 * cosT) * (cosY * sinZ - cosZ * sinX * sinY) + r1 * cosX * cosZ * sinT
            z = cosX * (r2 + r1 * cosT) * sinY + r1 * sinX * sinT + k2

            ooz = 1 / z # scale the projection with z

            # luminance based on the surface normal
            L = cosY * cosT * sinZ - cosX * cosT * sinY - sinX * sinT + cosZ * (cosX * sinT - cosT * sinX * sinY)

            xn = int(WIDTH/2 + k1 * ooz * x)
            yn = int(HEIGHT/2 - k1 * ooz * y) # y is negated cuz y is goes up in 3d but down in 2d

            if L > -0.1 and 0 <= xn < WIDTH and 0 <= yn < HEIGHT and ooz > zbuffer[yn][xn]:
                zbuffer[yn][xn] = ooz

                lumin_index = int(L * 9)
                lumin_index = min(lumin_index, len("',-~:;=!*#@█") - 1)

                output[yn][xn] = "',-~:;=!*#@█"[lumin_index]

    # Render star
    star_size = 2
    star_offset_x = -5

    thck_grad = -0.2

    m = 3 # angle offset
    n = 5 # points of the start
    k = 1 # sharpness from 0 to 1

    radial_step = 0.05
    
    # Polar star shape, angle sits on the xy plane
    for T in drange(0, math.pi * 2, t_spacing):
        cosT, sinT = math.cos(T), math.sin(T)

        # Star polar equation, creates 5 sharp points
        nom = star_size * math.cos((2*math.asin(k)+math.pi*m)/(2*n))
        denom = math.cos((2*math.asin(k*math.cos(n*T))+math.pi*m)/(2*n))
        r = nom/denom
        rnorm = r / star_size

        # Thickness factor, thicker as approaches center
        thickness = thck_grad*rnorm - thck_grad
        
        # Thickness range, not an angle
        for Y in drange(-thickness, thickness, y_spacing):
            cosY, sinY = math.cos(Y), math.sin(Y)

            # Fills in the star shape
            r_val = 0.0
            while r_val <= r:
                # x y z rotation matrices applied all at once
                x = (r_val * cosT + star_offset_x) * cosZ - (Y * cosX - r_val * sinT * sinX) * sinZ
                y = (r_val * cosT + star_offset_x) * sinZ + (Y * cosX - r_val * sinT * sinX) * cosZ
                z = Y * sinX + r_val * sinT * cosX + k2
    
                ooz = 1 / z

                xn = int(WIDTH/2 + k1 * ooz * x)
                yn = int(HEIGHT/2 - k1 * ooz * y)

                # surface normals
                nx =  cosT * cosZ + sinT * sinX * sinZ
                ny =  cosT * sinZ - sinT * sinX * cosZ
                nz =  sinT * cosX

                # luminance, same concepts as cresent
                # different directions due to different overall implementations
                # gives a result matching the crescent
                lx, ly, lz = 0.5, 1, 1
                L = nx * lx + ny * ly + nz * lz

                if L < 0: L = 0
                if 0 <= xn < WIDTH and 0 <= yn < HEIGHT and ooz > zbuffer[yn][xn]:
                    zbuffer[yn][xn] = ooz
                    lumin = "~:;=!*#@█"
                    lumin_index = int(L * 9)
                    lumin_index = min(lumin_index, len("~:;=!*#@█") - 1)
                    output[yn][xn] = lumin[lumin_index]

                r_val += radial_step
    
    sys.stdout.write("\x1b[H")

    for row in output:
        sys.stdout.write("\x1b[41m")  # red background
        sys.stdout.write("".join(row))
        sys.stdout.write("\x1b[0m\n")  # reset for each line
    
    sys.stdout.flush()

# Helper double range method
def drange(start, stop, step):
    while start < stop:
        yield start
        start += step

X, Z = 0.0, 0.0

if __name__ == "__main__":
    os.system('cls' if os.name=='nt' else 'clear')
    try:
        while True:
            render(X, Z)
            X += 0.04
            Z += 0.08
            time.sleep(0.02)
    except KeyboardInterrupt:
        pass
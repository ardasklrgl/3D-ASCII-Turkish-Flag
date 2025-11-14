
# 3D ASCII Turkish Flag

A Python program that renders a **3D rotating crescent moon with a star** entirely in ASCII characters in the terminal.
Inspired by the Spinning Donut by Andy Sloane (https://www.a1k0n.net/2011/07/20/donut-math.html)

---

## **How To Run**

1. Ensure **Python 3.7+** is installed.
2. Clone repository:
```bash
git clone https://github.com/yourusername/3D-ASCII-Turkish-Flag.git
cd 3D-ASCII-Turkish-Flag
```
3. Run:
```bash
python main.py
```
* Terminal will display the rotating crescent and star.
* Press `Ctrl + C` to exit gracefully.

---

## **How It Works**

I recommend first reading the blog post I linked in the beginning to get an idea of the math behind projecting a torus to 2D.
I also have a Python code for the spinning donut in the repo to see how the math is applied in code.

### **1. Crescent Geometry**

The crescent is generated using a **torus surface**, but with the radius of the main circle (the one rotated around to create the torus) decreasing to create the tapering effect.

* **Large circle radius (`r2`)**: Distance from the center of the crescent to the center of the small circular cross-section.
* **Small circle radius (`r1`)**: Radius of the inner small circles forming the crescent tube.

#### **Angles**

* `T`: Angle **around the small inner circles** of the crescent. Think of it as moving around each small tube of the torus.
* `Y`: Angle along the **vertical cross-section** of the crescent. Controls the shape of the crescent by modulating `r1` and creating the characteristic thinning toward the tips.

#### **3D Coordinates**

For each point `(T, Y)`, the 3D coordinates `(x, y, z)` are computed using rotation matrices.
These are the coordinates after multiplying the rotation matrices:

```python
x = (r2 + r1 * cosT) * (cosZ * cosY + sinX * sinZ * sinY) - (r1 * cosX * sinZ * sinT)
y = (r2 + r1 * cosT) * (cosY * sinZ - cosZ * sinX * sinY) + r1 * cosX * cosZ * sinT
z = cosX * (r2 + r1 * cosT) * sinY + r1 * sinX * sinT + k2
```

* `X` = rotation around **X-axis** (tilt up/down).
* `Z` = rotation around **Z-axis** (spin around vertical axis).
* `k2` = depth offset to move the crescent in front of the camera.

---

### **2. Star Geometry**

The star is drawn as a **5-point star using polar coordinates**:

* `T`: Moves around the full circle (0 → 2π).
* **Polar radius `r`**: Computed from the star’s polar equation for 5 points, which ensures sharp tips:

```python
nom = star_size * math.cos((2*math.asin(k)+math.pi*m)/(2*n))
denom = math.cos((2*math.asin(k*math.cos(n*T))+math.pi*m)/(2*n))
r = nom / denom
```

* **Radial fill (`r_val`)**: Loops from 0 → `r` to **fill the star** along each radial line, creating a solid shape instead of just an outline.
* **Thickness (`Y`)**: Adds 3D thickness to the star, making it volumetric rather than flat.

#### **3D Coordinates**

```python
x = (r_val * cosT + star_offset_x) * cosZ - (Y * cosX - r_val * sinT * sinX) * sinZ
y = (r_val * cosT + star_offset_x) * sinZ + (Y * cosX - r_val * sinT * sinX) * cosZ
z = Y * sinX + r_val * sinT * cosX + k2
```

* Rotations apply to the star the same way as the crescent.

---

### **3. Projection & Perspective**

Each 3D point `(x, y, z)` is projected to 2D screen coordinates `(xn, yn)` using perspective:

```python
ooz = 1 / z
xn = int(WIDTH/2 + k1 * ooz * x)
yn = int(HEIGHT/2 - k1 * ooz * y)
```

* `ooz = 1/z` ensures **points farther away appear smaller**, simulating 3D perspective.
* `k1` scales the coordinates to fit the terminal size, and also centers them.
* Z-buffer (`zbuffer[yn][xn]`) keeps track of the closest point at each pixel, so closer points overwrite farther points.

---

### **4. Luminance Shading**

* Each point is assigned a **luminance value** based on its **surface normal** and a **light vector**.
* Each point is then mapped to an ASCII character based on luminance.
* Example for crescent:

```python
L = cosY * cosT * sinZ - cosX * cosT * sinY - sinX * sinT + cosZ * (cosX * sinT - cosT * sinX * sinY)
```

---

## **Configurations**

| Variable          | Description                                  |
| ----------------- | -------------------------------------------- |
| `WIDTH`, `HEIGHT` | Terminal width/height in characters          |
| `t_spacing`       | Step size along T (angle around circles)     |
| `y_spacing`       | Step size along Y (vertical cross-section)   |
| `r1_max`          | Maximum radius of inner crescent circles     |
| `r2`              | Radius of main crescent circle               |
| `k1`              | Projection scale factor                      |
| `k2`              | Depth offset to move object away from camera |
| `star_size`       | Size of the 5-point star                     |
| `thck_grad`       | Thickness gradient of the star               |
| `X`, `Y`          | Rotation angles incremented per frame        |

---

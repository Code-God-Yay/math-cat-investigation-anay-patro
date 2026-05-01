import pygame
import math
import random
import sys

# Increase recursion depth for complex biological structures
sys.setrecursionlimit(20000)

class CADEngine:
    def __init__(self):
        pygame.init()
        # High-res display with double buffering to stop pulsing
        self.w, self.h = 1200, 800
        self.screen = pygame.display.set_mode((self.w, self.h), pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption("Y8 CAT | Recursive CAD Engine")
        self.clock = pygame.time.Clock()
        
        # Camera & Light Physics
        self.cam_angle_x = 0.5
        self.cam_angle_y = 0.2
        self.zoom = 1.0
        self.light_vec = pygame.Vector3(-1, -2, 1).normalize()
        
        self.running = True
        self.mesh_data = []
        self.needs_update = True

    def project(self, x, y, z):
        """3D to 2D Projection with Depth Sorting."""
        # Rotation X (Camera Tilt)
        cos_y, sin_y = math.cos(self.cam_angle_y), math.sin(self.cam_angle_y)
        ry = y * cos_y - z * sin_y
        rz = y * sin_y + z * cos_y
        
        # Rotation Y (Camera Orbit)
        cos_x, sin_x = math.cos(self.cam_angle_x), math.sin(self.cam_angle_x)
        rx = x * cos_x - rz * sin_x
        rz = x * sin_x + rz * cos_x
        
        # Perspective
        factor = 1000 * self.zoom / (rz + 1500)
        px = rx * factor + self.w // 2
        py = ry * factor + self.h // 1.5
        return (int(px), int(py)), rz

    def get_shading(self, normal_vec, base_color):
        """Pseudo-Ray Tracing: Calculates light bounce on surfaces."""
        dot = max(0.3, normal_vec.dot(self.light_vec) * -1)
        r = min(255, int(base_color[0] * dot * 1.5))
        g = min(255, int(base_color[1] * dot * 1.5))
        b = min(255, int(base_color[2] * dot * 1.5))
        return (r, g, b)

    def draw_recursive_tree(self, x, y, z, length, theta, phi, depth, rad):
        """The Recursive Core: Generates biological branching."""
        if depth <= 0 or length < 2:
            return

        # End point of this branch
        nx = x + length * math.sin(phi) * math.cos(theta)
        ny = y - length * math.sin(phi) * math.sin(theta)
        nz = z + length * math.cos(phi)

        # Create 4-sided branch mesh
        sides = 4
        for i in range(sides):
            a1, a2 = (i / sides) * 6.28, ((i + 1) / sides) * 6.28
            
            p1, z1 = self.project(x + rad * math.cos(a1), y, z + rad * math.sin(a1))
            p2, z2 = self.project(x + rad * math.cos(a2), y, z + rad * math.sin(a2))
            p3, z3 = self.project(nx + (rad*0.7) * math.cos(a2), ny, nz + (rad*0.7) * math.sin(a2))
            p4, z4 = self.project(nx + (rad*0.7) * math.cos(a1), ny, nz + (rad*0.7) * math.sin(a1))
            
            avg_z = (z1 + z2 + z3 + z4) / 4
            # Normal vector simulation for shading
            norm = pygame.Vector3(math.cos(a1), 0, math.sin(a1))
            color = self.get_shading(norm, (140, 120, 100)) # Clay color
            self.mesh_data.append((avg_z, [p1, p2, p3, p4], color, "poly"))

        # Leaves (only on high recursion depth)
        if depth < 5:
            lp, lz = self.project(nx, ny, nz)
            leaf_sz = int(depth * 8 * self.zoom)
            self.mesh_data.append((lz - 10, lp, (60, 140, 40), "leaf", leaf_sz))

        # Branching (Primary leader + 2 side shoots)
        # 1. Main trunk
        self.draw_recursive_tree(nx, ny, nz, length * 0.85, theta + random.uniform(-0.1, 0.1), phi, depth - 1, rad * 0.75)
        # 2. Side branches
        if depth > 2:
            self.draw_recursive_tree(nx, ny, nz, length * 0.5, theta + 0.8, phi + 0.6, depth - 2, rad * 0.4)
            self.draw_recursive_tree(nx, ny, nz, length * 0.5, theta - 0.8, phi - 0.6, depth - 2, rad * 0.4)

    def run(self):
        while self.running:
            self.screen.fill((245, 245, 250)) # Clean Studio White
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEMOTION and event.buttons[0]:
                    self.cam_angle_x += event.rel[0] * 0.01
                    self.cam_angle_y += event.rel[1] * 0.01
                    self.needs_update = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4: self.zoom *= 1.1; self.needs_update = True
                    if event.button == 5: self.zoom *= 0.9; self.needs_update = True

            if self.needs_update:
                self.mesh_data = []
                # Ground Plane
                for i in range(-4, 4):
                    for j in range(-2, 5):
                        p1, z1 = self.project(i*400, 300, j*400)
                        p2, z2 = self.project((i+1)*400, 300, j*400)
                        p3, z3 = self.project((i+1)*400, 300, (j+1)*400)
                        p4, z4 = self.project(i*400, 300, (j+1)*400)
                        self.mesh_data.append(((z1+z3)/2, [p1, p2, p3, p4], (200, 210, 190), "poly"))
                
                # Recursive Tree
                self.draw_recursive_tree(0, 300, 0, 180, 1.57, 1.57, 10, 40)
                
                # Z-Sorting (Painter's Algorithm)
                self.mesh_data.sort(key=lambda x: x[0], reverse=True)
                self.needs_update = False

            # Render
            for item in self.mesh_data:
                if item[3] == "poly":
                    pygame.draw.polygon(self.screen, item[2], item[1])
                elif item[3] == "leaf":
                    pygame.draw.circle(self.screen, item[2], item[1], item[4])

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    CADEngine().run()
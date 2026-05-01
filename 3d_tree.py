import pygame
import math
import random
import sys

sys.setrecursionlimit(30000)

class GlobalCAD:
    def __init__(self):
        pygame.init()
        self.W, self.H = 1300, 900
        self.DS = pygame.display.set_mode((self.W, self.H), pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.CLK = pygame.time.Clock()
        
        # --- Theme Engine ---
        self.DARK_MODE = True
        self.THEMES = {
            "DARK":  {"bg": (20, 22, 28), "side": (32, 35, 42), "txt": (200, 210, 230), "grid": (50, 55, 65)},
            "LIGHT": {"bg": (240, 242, 245), "side": (220, 225, 235), "txt": (40, 45, 55), "grid": (200, 205, 215)}
        }
        
        # --- CAD Parameters ---
        self.params = {
            "Depth":   {"v": 7, "mn": 1, "mx": 10, "y": 140},
            "Bush":    {"v": 3, "mn": 1, "mx": 5, "y": 210},
            "Spread":  {"v": 0.6, "mn": 0.1, "mx": 1.4, "y": 280},
            "Scale":   {"v": 170, "mn": 80, "mx": 250, "y": 350},
            "Gravity": {"v": 0.05, "mn": -0.3, "mx": 0.3, "y": 420},
            "Faces":   {"v": 6, "mn": 3, "mx": 12, "y": 490}
        }
        
        self.RX, self.RY = 0.7, 0.4
        self.ZOOM = 1.0
        self.DIRTY = True
        self.F_MESH = []
        self.ACTIVE_P = None
        self.FONT = pygame.font.SysFont("Verdana", 12, bold=True)

    def PRJ(self, x, y, z):
        cx, sx = math.cos(self.RX), math.sin(self.RX)
        cy, sy = math.cos(self.RY), math.sin(self.RY)
        rx, rzt = x * cx - z * sx, x * sx + z * cx
        ry, rz = y * cy - rzt * sy, y * sy + rzt * cy
        d = rz + (2800 / self.ZOOM)
        f = 1300 / max(40, d)
        return (int(rx * f + 820), int(ry * f + 450)), rz

    def GET_RNG(self, x, y, z, rd, seg):
        rng = []
        for i in range(seg):
            a = (i / seg) * 6.283
            rng.append((x + rd * math.cos(a), y, z + rd * math.sin(a)))
        return rng

    def BUILD(self, x, y, z, l, dv, dp, rd):
        if dp <= 0 or l < 4: return
        nx, ny, nz = x + dv[0]*l, y + dv[1]*l, z + dv[2]*l
        
        seg = int(self.params["Faces"]["v"])
        r1 = self.GET_RNG(x, y, z, rd, seg)
        r2 = self.GET_RNG(nx, ny, nz, rd * 0.7, seg)

        for i in range(seg):
            p1, p2, p3, p4 = r1[i], r1[(i+1)%seg], r2[(i+1)%seg], r2[i]
            v1 = pygame.Vector3(p2) - pygame.Vector3(p1)
            v2 = pygame.Vector3(p4) - pygame.Vector3(p1)
            nm = v1.cross(v2)
            if nm.length() > 0: nm = nm.normalize()
            self.F_MESH.append({'pts': [p1, p2, p3, p4], 'nm': nm, 'tp': 'tr'})

        if dp < 4:
            self.F_MESH.append({'pos': (nx, ny, nz), 'tp': 'lf', 'sz': dp*4})

        # Realistic 3D Spawning
        bc, sp, gr = int(self.params["Bush"]["v"]), self.params["Spread"]["v"], self.params["Gravity"]["v"]
        for i in range(bc):
            # Rotational variance for 3D fullness
            rv = (i / bc) * 6.283
            ndv = [dv[0] + (sp * math.cos(rv + dp)), dv[1] + gr, dv[2] + (sp * math.sin(rv + dp))]
            mg = math.sqrt(sum(v**2 for v in ndv))
            self.BUILD(nx, ny, nz, l * 0.72, [v/mg for v in ndv], dp - 1, rd * 0.6)

    def UI(self):
        th = self.THEMES["DARK"] if self.DARK_MODE else self.THEMES["LIGHT"]
        pygame.draw.rect(self.DS, th["side"], (0, 0, 310, self.H))
        pygame.draw.line(self.DS, (0, 255, 180), (310, 0), (310, self.H), 2)
        
        # Mode Toggle Button
        btn_txt = "SWITCH TO LIGHT" if self.DARK_MODE else "SWITCH TO DARK"
        btn_rect = pygame.Rect(40, 40, 230, 40)
        pygame.draw.rect(self.DS, (0, 180, 255), btn_rect, border_radius=5)
        t_img = self.FONT.render(btn_txt, True, (255, 255, 255))
        self.DS.blit(t_img, (btn_rect.centerx - t_img.get_width()//2, btn_rect.centery - t_img.get_height()//2))

        mx, my = pygame.mouse.get_pos()
        for k, d in self.params.items():
            l_t = self.FONT.render(k.upper(), True, th["txt"])
            self.DS.blit(l_t, (40, d["y"]))
            
            trk = pygame.Rect(40, d["y"] + 25, 230, 4)
            pygame.draw.rect(self.DS, (60, 65, 75) if self.DARK_MODE else (180, 185, 195), trk)
            
            rat = (d["v"] - d["mn"]) / (d["mx"] - d["mn"])
            hnd = pygame.Rect(40 + rat * 230 - 6, d["y"] + 17, 12, 20)
            
            if hnd.collidepoint(mx, my) and pygame.mouse.get_pressed()[0]: self.ACTIVE_P = k
            if self.ACTIVE_P == k:
                d["v"] = d["mn"] + max(0, min(1, (mx - 40) / 230)) * (d["mx"] - d["mn"])
                self.DIRTY = True
            
            pygame.draw.rect(self.DS, (0, 255, 180), hnd, border_radius=4)

        if pygame.mouse.get_pressed()[0] and btn_rect.collidepoint(mx, my):
            pygame.time.delay(150)
            self.DARK_MODE = not self.DARK_MODE
            self.DIRTY = True

    def RUN(self):
        while True:
            th = self.THEMES["DARK"] if self.DARK_MODE else self.THEMES["LIGHT"]
            self.DS.fill(th["bg"])
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                if e.type == pygame.MOUSEBUTTONUP: self.ACTIVE_P = None
                if e.type == pygame.MOUSEWHEEL:
                    self.ZOOM = max(0.1, min(5, self.ZOOM + e.y * 0.1))
                    self.DIRTY = True
                if e.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] and not self.ACTIVE_P:
                    if e.pos[0] > 310:
                        self.RX += e.rel[0] * 0.007
                        self.RY += e.rel[1] * 0.007
                        self.DIRTY = True

            if self.DIRTY:
                self.F_MESH = []
                random.seed(42)
                self.BUILD(0, 320, 0, self.params["Scale"]["v"], (0, -1, 0), int(self.params["Depth"]["v"]), 35)
                self.DIRTY = False

            # Grid Rendering
            for i in range(-5, 6):
                p1, _ = self.PRJ(i*350, 320, -1750); p2, _ = self.PRJ(i*350, 320, 1750)
                pygame.draw.line(self.DS, th["grid"], p1, p2)
                p1, _ = self.PRJ(-1750, 320, i*350); p2, _ = self.PRJ(1750, 320, i*350)
                pygame.draw.line(self.DS, th["grid"], p1, p2)

            # Sort and Draw 3D Elements
            sun = pygame.Vector3(-1, -1, 1).normalize()
            draw_stack = []
            for f in self.F_MESH:
                if f['tp'] == 'tr':
                    p2d, zs = [], 0
                    for p in f['pts']:
                        p2, pz = self.PRJ(*p); p2d.append(p2); zs += pz
                    lit = max(0.1, f['nm'].dot(sun))
                    col = [int((110 if self.DARK_MODE else 140) * lit)] * 3
                    draw_stack.append({'z': zs/4, 'pts': p2d, 'col': col, 'tp': 'tr'})
                else:
                    p2, pz = self.PRJ(*f['pos'])
                    l_col = (50, 160, 100) if self.DARK_MODE else (80, 200, 120)
                    draw_stack.append({'z': pz, 'pos': p2, 'col': l_col, 'sz': f['sz'], 'tp': 'lf'})

            draw_stack.sort(key=lambda x: x['z'], reverse=True)
            for d in draw_stack:
                if d['tp'] == 'tr': pygame.draw.polygon(self.DS, d['col'], d['pts'])
                else: pygame.draw.circle(self.DS, d['col'], d['pos'], int(d['sz'] * self.ZOOM))

            self.UI()
            pygame.display.flip()
            self.CLK.tick(60)

if __name__ == "__main__":
    GlobalCAD().RUN()
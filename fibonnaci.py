import turtle
import random
import tkinter as tk
from tkinter import ttk
import time

class TreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro Fractal Tree Renderer")
        
        # Setup UI Frame (Sidebar)
        self.sidebar = tk.Frame(root, width=220, bg="#1a1a1a", padx=15, pady=15)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(self.sidebar, text="TREE CONTROLS", bg="#1a1a1a", fg="#ecf0f1", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 20))

        self.depth_var = tk.IntVar(value=10)
        self.scale_var = tk.DoubleVar(value=0.72)
        self.angle_var = tk.IntVar(value=25)

        self.create_slider("Complexity (Depth)", self.depth_var, 1, 15)
        self.create_slider("Growth Factor (Scale)", self.scale_var, 0.4, 0.85, resolution=0.01)
        self.create_slider("Spread (Angle)", self.angle_var, 10, 50)
        
        self.draw_btn = tk.Button(self.sidebar, text="RENDER TREE", command=self.start_render, 
                                  bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                                  relief=tk.FLAT, pady=10)
        self.draw_btn.pack(pady=20, fill=tk.X)

        # Turtle Canvas Area
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=900, height=700, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.colormode(255)
        self.screen.tracer(0, 0)
        
        self.t = turtle.RawTurtle(self.screen)
        self.t.hideturtle()

    def create_slider(self, label, var, start, end, resolution=1):
        tk.Label(self.sidebar, text=label, bg="#1a1a1a", fg="#bdc3c7", font=("Arial", 9)).pack(anchor=tk.W)
        s = tk.Scale(self.sidebar, from_=start, to=end, variable=var, 
                     orient=tk.HORIZONTAL, resolution=resolution, 
                     bg="#1a1a1a", fg="white", highlightthickness=0, troughcolor="#34495e")
        s.pack(fill=tk.X, pady=(0, 15))

    # --- LOADER UI ---
    def show_loader(self, depth):
        self.loader_win = tk.Toplevel(self.root)
        self.loader_win.overrideredirect(True) # Remove window borders
        self.loader_win.attributes("-topmost", True)
        self.loader_win.configure(bg="#2c3e50")
        
        # Center the loader over the canvas
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 100
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 50
        self.loader_win.geometry(f"200x120+{x}+{y}")

        label_text = "Simulating Nature..." if depth < 10 else "Heavy Computation..."
        tk.Label(self.loader_win, text=label_text, bg="#2c3e50", fg="white", font=("Arial", 10)).pack(pady=10)

        if depth < 10:
            # Circle Loader (Canvas based)
            self.loader_canvas = tk.Canvas(self.loader_win, width=50, height=50, bg="#2c3e50", highlightthickness=0)
            self.loader_canvas.pack()
            self.arc = self.loader_canvas.create_arc(5, 5, 45, 45, start=0, extent=150, outline="#3498db", width=4)
            self.animate_circle()
        else:
            # Long Bar Loader (Determined/Indeterminate)
            self.bar = ttk.Progressbar(self.loader_win, orient=tk.HORIZONTAL, length=160, mode='indeterminate')
            self.bar.pack(pady=10)
            self.bar.start(10)
            
        self.root.update()

    def animate_circle(self):
        if hasattr(self, 'loader_win') and self.loader_win.winfo_exists():
            self.loader_canvas.itemconfig(self.arc, start=(time.time()*300)%360)
            self.root.update()
            self.root.after(20, self.animate_circle)

    # --- DRAWING LOGIC ---
    def draw_sky_gradient(self):
        self.t.penup()
        for i in range(50): # Fewer steps for speed
            r, g, b = int(135 + (i * 1.6)), int(206 + (i * 0.8)), int(235 + (i * 0.4))
            self.t.goto(-600, 350 - (i * 12))
            self.t.color(min(255, r), min(255, g), min(255, b))
            self.t.pendown()
            self.t.setheading(0)
            self.t.forward(1200)
            self.t.penup()

    def draw_environment(self):
        self.t.clear()
        self.draw_sky_gradient()
        # Ground
        self.t.goto(-600, -250)
        self.t.color(34, 100, 34)
        self.t.begin_fill()
        for _ in range(2):
            self.t.forward(1200); self.t.right(90); self.t.forward(300)
        self.t.end_fill()
        # Sun
        self.t.goto(300, 220); self.t.color(255, 255, 180); self.t.dot(100)
        self.t.color(255, 255, 0); self.t.dot(60)

    def draw_tree(self, depth, length, angle, scale):
        if depth <= 0:
            # Foliage
            self.t.color(random.randint(30, 60), random.randint(120, 180), random.randint(30, 60))
            self.t.begin_fill()
            self.t.circle(random.randint(4, 10))
            self.t.end_fill()
            return

        self.t.pensize(max(1, int(depth * 1.2)))
        self.t.color((101, 67, 33) if depth > 4 else (46, 139, 87))

        jitter_len = length * random.uniform(0.8, 1.2)
        self.t.forward(jitter_len)
        
        # Conditional clustering to save resources at depth 15
        num_branches = 3 if 6 < depth < 10 else 2
        angles = [-angle, 0, angle] if num_branches == 3 else [-angle, angle]

        for a in angles:
            current_angle = a + random.randint(-10, 10)
            self.t.left(current_angle)
            self.draw_tree(depth - 1, length * scale, angle, scale)
            self.t.right(current_angle)

        self.t.penup()
        self.t.backward(jitter_len)
        self.t.pendown()

    def start_render(self):
        d = self.depth_var.get()
        s = self.scale_var.get()
        a = self.angle_var.get()
        
        self.show_loader(d)
        
        # Execute render
        self.draw_environment()
        self.t.penup()
        self.t.goto(0, -250)
        self.t.setheading(90)
        self.t.pendown()
        
        base_len = 80 * (0.75 / s) if s > 0 else 80
        self.draw_tree(d, base_len, a, s)
        self.screen.update()
        
        # Kill loader
        self.loader_win.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1150x750")
    app = TreeApp(root)
    root.mainloop()
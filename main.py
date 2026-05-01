import random
import turtle

def get_color(depth, max_depth):
    """Calculates a gradient from brown (trunk) to green (leaves)."""
    # Normalize progress (0.0 at trunk, 1.0 at leaves)
    t = 1 - (depth / max_depth)
    
    if depth > 3:
        # Brownish colors for the trunk/branches
        r = int(70 + (50 * t))
        g = int(40 + (30 * t))
        b = int(20 + (10 * t))
    else:
        # Greenish colors for the tips/leaves
        r = int(34 + (50 * (1-t)))
        g = int(139 + (60 * t))
        b = int(34)
        
    return (max(0, min(255, r)), 
            max(0, min(255, g)), 
            max(0, min(255, b)))

def draw_tree(depth, length, angle, scale, max_depth):
    if depth <= 0:
        # Draw a small leaf cluster at the end
        drawing_pen.color(get_color(0, max_depth))
        drawing_pen.begin_fill()
        drawing_pen.circle(random.randint(2, 4))
        drawing_pen.end_fill()
        return

    # Set color and thickness based on depth
    drawing_pen.color(get_color(depth, max_depth))
    drawing_pen.pensize(max(1, int(depth**1.3 * 0.6)))
    
    # Draw the branch
    dist = length * random.uniform(0.8, 1.1)
    drawing_pen.forward(dist)
    
    # Variations in angles for natural look
    left_a = angle + random.uniform(-10, 10)
    right_a = angle + random.uniform(-10, 10)
    
    # Recursive branching
    drawing_pen.left(left_a)
    draw_tree(depth - 1, length * scale, angle, scale, max_depth)
    
    drawing_pen.right(left_a + right_a) # Turn back past center to the right
    draw_tree(depth - 1, length * scale, angle, scale, max_depth)
    
    # Return to original position and heading
    drawing_pen.left(right_a)
    drawing_pen.penup()
    drawing_pen.backward(dist)
    drawing_pen.pendown()

def reset_scene():
    drawing_pen.clear()
    drawing_pen.penup()
    drawing_pen.goto(0, -280)
    drawing_pen.setheading(90)
    drawing_pen.pendown()

def run():
    while True:
        d = tree_window.numinput("Tree", "Depth (10 is good):", 10, 1, 14)
        if d is None: break
        l = tree_window.numinput("Tree", "Trunk Length:", 90, 20, 200)
        if l is None: break
        a = tree_window.numinput("Tree", "Angle:", 25, 5, 60)
        if a is None: break
        s = tree_window.numinput("Tree", "Scale:", 0.75, 0.5, 0.9)
        if s is None: break
        
        reset_scene()
        draw_tree(int(d), float(l), float(a), float(s), int(d))
        tree_window.update()
        
        ans = tree_window.textinput("Again?", "Type 'y' to restart:")
        if ans is None or ans.lower() != "y":
            break

# Setup
tree_window = turtle.Screen()
tree_window.setup(width=800, height=800)
tree_window.colormode(255)
tree_window.bgcolor("honeydew")
tree_window.tracer(0)

drawing_pen = turtle.Turtle()
drawing_pen.hideturtle()
drawing_pen.speed(0)
# This helps make the line ends and connections look rounded
drawing_pen.shape("circle") 
drawing_pen.resizemode("user")

if __name__ == "__main__":
    reset_scene()
    run()
    turtle.done()

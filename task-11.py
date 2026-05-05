import turtle
import random

def draw_realistic_tree(depth, branch_length, branch_angle, shrink_factor):
    if depth > 0:
        drawing_pen.pensize(max(1, depth))
        if depth < 3:
            drawing_pen.color("forest green")
        else:
            drawing_pen.color("sienna")
            
        current_length = branch_length * (1 + random.uniform(-0.2, 0.2))
        drawing_pen.forward(current_length)
        
        left_angle = branch_angle + random.randint(-10, 10)
        right_angle = branch_angle + random.randint(-10, 10)
        
        drawing_pen.left(left_angle)
        draw_realistic_tree(depth - 1, branch_length * shrink_factor, branch_angle, shrink_factor)
        
        drawing_pen.right(left_angle + right_angle)
        draw_realistic_tree(depth - 1, branch_length * shrink_factor, branch_angle, shrink_factor)
        
        drawing_pen.left(right_angle)
        drawing_pen.penup()
        drawing_pen.backward(current_length)
        drawing_pen.pendown()

# --- Setup ---
tree_window = turtle.Screen()
tree_window.bgcolor("honeydew")
drawing_pen = turtle.Turtle()
drawing_pen.speed(0)
drawing_pen.left(90)
drawing_pen.penup()
drawing_pen.goto(0, -250)
drawing_pen.pendown()

# --- User Input Section ---
# numinput(title, prompt, default, minval, maxval)
user_depth = int(tree_window.numinput("Tree Depth", "How many branch levels? (suggest 8-12):", default=10, minval=1, maxval=14))
user_length = tree_window.numinput("Trunk Size", "Starting trunk length? (suggest 70-100):", default=80, minval=10, maxval=200)
user_angle = tree_window.numinput("Branch Angle", "Angle of branches? (suggest 20-45):", default=30, minval=5, maxval=90)

# --- Drawing ---
tree_window.tracer(0)
print(f"Creating a tree with depth {user_depth}...")
draw_realistic_tree(user_depth, user_length, user_angle, 0.8)
tree_window.update()

print("Done! Close the window to exit.")
tree_window.exitonclick()


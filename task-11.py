import turtle
import random

def draw_realistic_tree(depth, branch_length, branch_angle, shrink_factor):
    """Draw the “final” version: tapered, coloured, and slightly random.

    The goal here isn't perfect realism — it's to make the recursion *read*
    like a real tree: thick trunk, thin tips, and small variations that stop
    everything looking mirrored.
    """
    if depth > 0:
        drawing_pen.pensize(max(1, depth))
        
        if depth < 3:
            drawing_pen.color("forest green")
        else:
            drawing_pen.color("sienna")

        # A little wobble goes a long way. Too much and the tree looks “broken”.
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

# Set up the screen
tree_window = turtle.Screen()
tree_window.bgcolor("honeydew")
# Draw quickly without showing each line
tree_window.tracer(0)

drawing_pen = turtle.Turtle()
drawing_pen.speed(0)
drawing_pen.left(90)
drawing_pen.penup()
drawing_pen.goto(0, -250)
drawing_pen.pendown()

# Draw a realistic tree
print("Creating a realistic tree...")
draw_realistic_tree(10, 80, 30, 0.8)
tree_window.update()
print("Done! Close the window to exit.")
turtle.done()

 
 
  

# v1.3 stable

# v1.3 stable

# v1.3 stable

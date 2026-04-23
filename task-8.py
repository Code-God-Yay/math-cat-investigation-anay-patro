import turtle

def draw_fractal_tree(depth, branch_length, branch_angle, shrink_factor):
    """
    Draw a tree that branches recursively.
    depth: how many levels to draw, 
    branch_length: how long each branch is,
    branch_angle: what angle the branches split at,
    shrink_factor: how much smaller each level gets (e.g., 0.75 = 75% of parent size)
    """
    if depth > 0:
        # Draw a branch forward
        drawing_pen.forward(branch_length)
        
        # Draw the left branch
        drawing_pen.left(branch_angle)
        draw_fractal_tree(depth - 1, branch_length * shrink_factor, branch_angle, shrink_factor)
        
        # Draw the right branch
        drawing_pen.right(branch_angle * 2)
        draw_fractal_tree(depth - 1, branch_length * shrink_factor, branch_angle, shrink_factor)
        
        # Go back to where this branch started
        drawing_pen.left(branch_angle)
        drawing_pen.backward(branch_length)

# Set up the screen
tree_window = turtle.Screen()
tree_window.bgcolor("honeydew")
# Don't animate while drawing (makes it way faster)
tree_window.tracer(0)

drawing_pen = turtle.Turtle()
drawing_pen.color("blue")
drawing_pen.speed(0)
drawing_pen.left(90)
drawing_pen.penup()
drawing_pen.goto(0, -250)
drawing_pen.pendown()

# Draw the tree with some preset values
print("Drawing a custom fractal tree...")
draw_fractal_tree(8, 100, 30, 0.75)
tree_window.update()

turtle.done()

 
 
 
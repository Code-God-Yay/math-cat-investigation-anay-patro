import turtle

def draw_fractal_tree(depth, branch_length, branch_angle, shrink_factor):
    """Draw a tree that branches recursively with custom settings."""
    if depth > 0:
        drawing_pen.forward(branch_length)
        drawing_pen.left(branch_angle)
        draw_fractal_tree(depth - 1, branch_length * shrink_factor, branch_angle, shrink_factor)
        drawing_pen.right(branch_angle * 2)
        draw_fractal_tree(depth - 1, branch_length * shrink_factor, branch_angle, shrink_factor)
        drawing_pen.left(branch_angle)
        drawing_pen.backward(branch_length)

def run_interactive_tree_maker():
    """Let the user pick tree settings and draw as many trees as they want."""
    while True:
        # Ask the user how deep the tree should be
        depth = tree_window.numinput("Tree Maker", "How many levels deep? (Try 1-15):", default=8, minval=1, maxval=15)
        if depth is None: 
            break
        
        # Ask for branch length
        branch_length = tree_window.numinput("Tree Maker", "How long should branches be? (Try 100):", default=100)
        if branch_length is None: 
            break
        
        # Ask for the angle
        branch_angle = tree_window.numinput("Tree Maker", "What angle should branches split at? (Try 30):", default=30)
        if branch_angle is None: 
            break
        
        # Ask for shrink factor
        shrink_factor = tree_window.numinput("Tree Maker", "How much smaller should each level get? (Try 0.75):", default=0.75, minval=0.1, maxval=0.99)
        if shrink_factor is None: 
            break

        # Clear and get ready to draw
        drawing_pen.clear()
        drawing_pen.penup()
        drawing_pen.goto(0, -250)
        drawing_pen.setheading(90)
        drawing_pen.pendown()
        
        # Draw the tree
        draw_fractal_tree(int(depth), branch_length, branch_angle, shrink_factor)
        tree_window.update()

        # Ask if they want to make another one
        again = tree_window.textinput("Done!", "Draw another tree? Type 'y' to continue:")
        if again is None or again.lower() != 'y':
            break

# Set up the screen
tree_window = turtle.Screen()
tree_window.title("Interactive Tree Maker")
tree_window.bgcolor("honeydew")
tree_window.tracer(0)

drawing_pen = turtle.Turtle()
drawing_pen.color("blue")
drawing_pen.hideturtle()

if __name__ == "__main__":
    run_interactive_tree_maker()
    turtle.done()

 
 
  

# v1.3 stable

# v1.3 stable

# v1.3 stable

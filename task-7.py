import turtle

def draw_simple_tree(depth):
    """Draw a “starter” fractal tree.

    This one is deliberately simple: fixed branch length + fixed split angle.
    It's the first version that makes the recursion idea visually obvious.
    """
    if depth > 0:
        drawing_pen.forward(50)
        drawing_pen.left(30)
        draw_simple_tree(depth - 1)
        drawing_pen.right(60)
        draw_simple_tree(depth - 1)
        drawing_pen.left(30)
        drawing_pen.backward(50)

# Set up the screen
tree_window = turtle.Screen()
tree_window.bgcolor("honeydew")
# Don't animate while drawing (makes it faster)
tree_window.tracer(0)

drawing_pen = turtle.Turtle()
drawing_pen.color("blue")
# Move as fast as possible
drawing_pen.speed(0)
# Turn the pen to face up
drawing_pen.left(90)
# Move to the starting position
drawing_pen.penup()
drawing_pen.goto(0, -250)
drawing_pen.pendown()

# Ask the user how deep they want the tree
depth = int(input("How many levels deep should the tree go? "))
draw_simple_tree(depth)

# Show the drawing
tree_window.update()

drawing_pen.hideturtle()
turtle.done()

 
 
  

# v1.3 stable

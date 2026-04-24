import turtle
import random

def draw_random_tree(depth, branch_length, branch_angle, shrink_factor):
    """
    Draw a tree with random variation so each tree looks slightly different.
    This makes the tree look more natural!
    """
    if depth > 0:
        # A little unevenness makes it look alive.
        current_shrink = shrink_factor * random.uniform(0.8, 1.2)
        current_length = branch_length * current_shrink
        
        drawing_pen.forward(current_length)

        # Angle wobble stops it looking like a perfect snowflake.
        left_angle = branch_angle + random.randint(-10, 10)
        right_angle = branch_angle + random.randint(-10, 10)

        drawing_pen.left(left_angle)
        draw_random_tree(depth - 1, branch_length * shrink_factor, branch_angle, shrink_factor)
        
        drawing_pen.right(left_angle + right_angle)
        draw_random_tree(depth - 1, branch_length * shrink_factor, branch_angle, shrink_factor)

        # Go back to the starting position
        drawing_pen.left(right_angle)
        drawing_pen.backward(current_length)

def run_random_tree_maker():
    """Let the user make random trees with their own settings."""
    while True:
        # Ask for tree depth
        depth = tree_window.numinput("Random Tree Maker", "How many levels deep? (Try 1-15):", default=10, minval=1, maxval=15)
        if depth is None: 
            break
        
        # Ask for branch length
        branch_length = tree_window.numinput("Random Tree Maker", "How long should branches be? (Try 80):", default=80)
        if branch_length is None:
            break
        
        # Ask for branch angle
        branch_angle = tree_window.numinput("Random Tree Maker", "What angle should branches spread at? (Try 30):", default=30)
        if branch_angle is None:
            break
        
        # Ask for shrink factor
        shrink_factor = tree_window.numinput("Random Tree Maker", "How much should each level shrink? (Try 0.8):", default=0.8)
        if shrink_factor is None:
            break

        # Clear the screen and reset pen position
        drawing_pen.clear()
        drawing_pen.penup()
        drawing_pen.goto(0, -250)
        drawing_pen.setheading(90)
        drawing_pen.pendown()
        
        # Draw the tree with random variation
        draw_random_tree(int(depth), branch_length, branch_angle, shrink_factor)
        tree_window.update()

        # Ask if they want to draw another
        again = tree_window.textinput("Done!", "Draw another tree? Type 'y' to continue:")
        if again is None or again.lower() != 'y':
            break

# Set up the screen
tree_window = turtle.Screen()
tree_window.title("Random Tree Maker")
tree_window.bgcolor("honeydew")
tree_window.tracer(0)

drawing_pen = turtle.Turtle()
drawing_pen.color("blue")
drawing_pen.hideturtle()

if __name__ == "__main__":
    run_random_tree_maker()
    turtle.done()

 
 
  

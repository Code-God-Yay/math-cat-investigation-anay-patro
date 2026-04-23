import turtle
import random

def draw_realistic_tree(depth, branch_length, branch_angle, shrink_factor):
    """
    Draw a realistic-looking tree with thick trunks, thin branches, and natural colors.
    I added randomness so each tree looks a bit different, just like real trees!
    """
    if depth > 0:
        # Make branches thicker near the bottom and thinner at the top
        drawing_pen.pensize(depth)
        
        # Use brown for the trunk and green for the leaves
        if depth < 3:
            drawing_pen.color("forest green")
        else:
            drawing_pen.color("sienna")

        # Add a bit of randomness to the branch length (varies by up to 20%)
        current_length = branch_length * (1 + random.uniform(-0.2, 0.2))
        drawing_pen.forward(current_length)

        # Randomize the branching angles so the tree looks more natural
        left_angle = branch_angle + random.randint(-10, 10)
        right_angle = branch_angle + random.randint(-10, 10)

        # Draw the left side
        drawing_pen.left(left_angle)
        draw_realistic_tree(depth - 1, branch_length * shrink_factor, branch_angle, shrink_factor)
        
        # Draw the right side
        drawing_pen.right(left_angle + right_angle)
        draw_realistic_tree(depth - 1, branch_length * shrink_factor, branch_angle, shrink_factor)

        # Go back to the starting position (no ghost lines!)
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

 
 
 
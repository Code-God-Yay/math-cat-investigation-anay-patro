import turtle
import random

def draw_realistic_tree(depth, length, angle, scale):
    """Draw a tree that looks like a real tree with thick trunks and thin branches."""
    if depth > 0:
        # Make branches thicker near the bottom and thinner at the top
        drawing_pen.pensize(depth * 0.8)
        
        # Use brown for the trunk and green for the leaves
        if depth < 3:
            drawing_pen.color("forest green")
        else:
            drawing_pen.color("sienna")

        # Add a bit of randomness so each tree looks different
        current_scale = scale * random.uniform(0.85, 1.15)
        current_length = length * current_scale
        left_angle = angle + random.randint(-12, 12)
        right_angle = angle + random.randint(-12, 12)

        # Draw the branch
        drawing_pen.forward(current_length)
        drawing_pen.left(left_angle)
        draw_realistic_tree(depth - 1, length * scale, angle, scale)
        drawing_pen.right(left_angle + right_angle)
        draw_realistic_tree(depth - 1, length * scale, angle, scale)
        drawing_pen.left(right_angle)
        
        # Go back without leaving a line behind (so we don't see ghost lines)
        drawing_pen.penup()
        drawing_pen.backward(current_length)
        drawing_pen.pendown()

def start_app():
    """Run the tree maker app with pop-up windows to get settings from the user."""
    while True:
        # Ask the user how deep they want the tree to go
        depth = tree_window.numinput("My Tree Maker", "How many levels deep should the tree go? (Try 10-12):", default=10, minval=1, maxval=15)
        if depth is None: 
            break
        
        # Ask for the trunk length
        trunk_length = tree_window.numinput("My Tree Maker", "How long should the trunk be? (Try 80):", default=80)
        if trunk_length is None:
            break
        
        # Ask for the branching angle
        branch_angle = tree_window.numinput("My Tree Maker", "What angle should the branches go? (Try 25):", default=25)
        if branch_angle is None:
            break
        
        # Ask for the scale (how much smaller each level gets)
        scale_factor = tree_window.numinput("My Tree Maker", "How much smaller should each level be? (Try 0.8):", default=0.8, minval=0.1, maxval=0.9)
        if scale_factor is None:
            break

        # Clear the screen and get ready to draw
      up the window and drawing pen
tree_window = turtle.Screen()
tree_window.title("My Tree Maker - Anay Patro")
tree_window.bgcolor("honeydew")
tree_window.tracer(0)

drawing_pen = turtle.Turtle()
drawing_        # Draw the tree with the settings the user chose
        draw_realistic_tree(int(depth), trunk_length, branch_angle, scale_factor)
        tree_window.update()

        # Ask if they want to draw another tree
        again = tree_window.textinput("Done!", "Close this to go back, or type 'y' to draw another tree:")
        if again is None or again.lower() != 'y':
            break

# Setup
screen = turtle.Screen()
screen.title("Anay's Ultimate Realistic Fractal Tree")
screen.bgcolor("white")
screen.tracer(0)
pen = turtle.Turtle()
pen.hideturtle()

if __name__ == "__main__":
    start_app()
    turtle.done()

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  

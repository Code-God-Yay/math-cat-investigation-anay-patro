import random
import turtle


def draw_realistic_tree(depth: int, length: float, angle: float, scale: float) -> None:
    """Draw a more “real” fractal tree.

    I wanted this to feel less like perfect geometry and more like something
    you’d actually see outside. The small randomness is intentional: it stops
    the tree from looking copy-pasted at every branch.
    """
    if depth <= 0:
        return

    # Thickness is a cheat that makes the picture read better: big trunk, tiny twigs.
    drawing_pen.pensize(max(1, int(depth * 0.8)))

    # A simple colour rule: brown-ish trunk, green-ish tips.
    drawing_pen.color("forest green" if depth <= 2 else "sienna")

    # “Nature noise”: a little variation per branch, not enough to look broken.
    length_jitter = length * random.uniform(0.85, 1.15)
    left_angle = angle + random.randint(-12, 12)
    right_angle = angle + random.randint(-12, 12)

    drawing_pen.forward(length_jitter)

    drawing_pen.left(left_angle)
    draw_realistic_tree(depth - 1, length * scale, angle, scale)

    drawing_pen.right(left_angle + right_angle)
    draw_realistic_tree(depth - 1, length * scale, angle, scale)

    drawing_pen.left(right_angle)

    # “Teleport back” so we don’t draw a return line.
    drawing_pen.penup()
    drawing_pen.backward(length_jitter)
    drawing_pen.pendown()


def reset_pen() -> None:
    """Put the pen in a good starting position for a new tree."""
    drawing_pen.clear()
    drawing_pen.penup()
    drawing_pen.goto(0, -260)
    drawing_pen.setheading(90)
    drawing_pen.pendown()


def start_app() -> None:
    """Interactive tree maker using turtle's built-in popups."""
    while True:
        depth = tree_window.numinput(
            "My Tree Maker",
            "Tree depth (levels). 10–12 looks good:",
            default=10,
            minval=1,
            maxval=15,
        )
        if depth is None:
            return

        trunk_length = tree_window.numinput(
            "My Tree Maker",
            "Trunk length (pixels). Try ~80:",
            default=80,
            minval=10,
            maxval=300,
        )
        if trunk_length is None:
            return

        branch_angle = tree_window.numinput(
            "My Tree Maker",
            "Branch angle (degrees). Try ~25:",
            default=25,
            minval=1,
            maxval=90,
        )
        if branch_angle is None:
            return

        scale_factor = tree_window.numinput(
            "My Tree Maker",
            "Scale factor per level. Try ~0.8:",
            default=0.8,
            minval=0.1,
            maxval=0.95,
        )
        if scale_factor is None:
            return

        reset_pen()
        draw_realistic_tree(int(depth), float(trunk_length), float(branch_angle), float(scale_factor))
        tree_window.update()

        again = tree_window.textinput("Done!", "Draw another? Type 'y' for yes:")
        if again is None or again.strip().lower() != "y":
            return


tree_window = turtle.Screen()
tree_window.title("My Tree Maker — Anay Patro")
tree_window.bgcolor("honeydew")
tree_window.tracer(0)

drawing_pen = turtle.Turtle()
drawing_pen.hideturtle()
drawing_pen.speed(0)


if __name__ == "__main__":
    reset_pen()
    start_app()
    turtle.done()

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  

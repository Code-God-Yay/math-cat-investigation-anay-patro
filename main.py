import random
import turtle


def get_color(depth, max_depth, heading):
    t = 1 - (depth / max_depth)
    if depth > 3:
        r = 35 + (90 * t)
        g = 20 + (45 * t)
        b = 10 + (25 * t)
    else:
        angle_diff = abs((heading % 360) - 45)
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
        light = max(0.3, (180 - angle_diff) / 180)
        r = 15 + (210 * light * t)
        g = 55 + (190 * light * t)
        b = 15 + (45 * light * t)
    return int(max(0, min(255, r))), int(max(0, min(255, g))), int(max(0, min(255, b)))


def draw_tree(depth, length, angle, scale, max_depth):
    r, g, b = get_color(depth, max_depth, drawing_pen.heading())
    drawing_pen.color(r, g, b)
    if depth <= 0:
        drawing_pen.begin_fill()
        for _ in range(4):
            drawing_pen.circle(random.randint(2, 5))
            drawing_pen.right(90)
        drawing_pen.end_fill()
        return
    drawing_pen.pensize(max(1, int(depth**1.2 * 0.5)))
    dist = length * random.uniform(0.8, 1.1)
    drawing_pen.forward(dist)
    left_a = angle + random.uniform(-10, 10)
    right_a = angle + random.uniform(-10, 10)
    drawing_pen.left(left_a)
    draw_tree(depth - 1, length * scale, angle, scale, max_depth)
    drawing_pen.right(right_a)
    draw_tree(depth - 1, length * scale, angle, scale, max_depth)
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
        if d is None:
            break
        l = tree_window.numinput("Tree", "Trunk Length:", 90, 20, 200)
        if l is None:
            break
        a = tree_window.numinput("Tree", "Angle:", 25, 5, 60)
        if a is None:
            break
        s = tree_window.numinput("Tree", "Scale:", 0.75, 0.5, 0.9)
        if s is None:
            break
        reset_scene()
        draw_tree(int(d), float(l), float(a), float(s), int(d))
        tree_window.update()
        ans = tree_window.textinput("Again?", "Type 'y' to restart:")
        if ans is None or ans.lower() != "y":
            break


tree_window = turtle.Screen()
tree_window.colormode(255)
tree_window.bgcolor("honeydew")
tree_window.tracer(0)

drawing_pen = turtle.Turtle()
drawing_pen.hideturtle()
drawing_pen.speed(0)

if __name__ == "__main__":
    reset_scene()
    run()
    turtle.done()

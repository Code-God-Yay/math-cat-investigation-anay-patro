import turtle

# create turtle screen and set background colour
screen = turtle.Screen()
screen.bgcolor("White")

# create a turtle object to draw with
pen = turtle.Turtle()

# set colour of the turtle
pen.color("Blue")

# set speed of the turtle
pen.speed(2)

# draw line of length 20 pixels
pen.forward(20)

# rotate the turtle 90 degrees to the right
pen.right(90)

# draw the other 3 sides of a rectangle
pen.forward(40)
pen.right(90)
pen.forward(20)
pen.right(90)
pen.forward(40)

# hide turtle
pen.hideturtle()

# keep turtle window open when done
turtle.done()

 
 

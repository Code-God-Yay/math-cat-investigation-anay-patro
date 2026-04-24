import turtle

# Tiny sanity-check program:
# if Turtle opens and draws a shape, your environment is working.
screen = turtle.Screen()
screen.bgcolor("white")

pen = turtle.Turtle()
pen.color("blue")
pen.speed(2)

pen.forward(20)

pen.right(90)

pen.forward(40)
pen.right(90)
pen.forward(20)
pen.right(90)
pen.forward(40)

pen.hideturtle()

turtle.done()

 
 
  

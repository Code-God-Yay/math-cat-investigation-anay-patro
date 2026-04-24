import turtle
import subprocess

def run_task(choice):
    """Launch one of the task scripts in a clean Python process."""
    valid_tasks = ['4', '5', '6', '7', '8', '9', '10', '11', 'main']
    if choice in valid_tasks:
        filename = "main.py" if choice == "main" else f"task-{choice}.py"
        print(f"Opening {filename}...")
        subprocess.run(["python3", filename])

def open_project_menu():
    """Show the main menu screen where you can pick which task to run."""
    menu_screen = turtle.Screen()
    menu_screen.title("Year 8 Maths - Project Menu")
    menu_screen.setup(400, 600)
    menu_screen.bgcolor("#f0f0f0")

    menu_text_pen = turtle.Turtle()
    menu_text_pen.hideturtle()
    menu_text_pen.penup()
    
    menu_text_pen.goto(0, 150)
    menu_text_pen.write("Year 8 Maths Investigation\nPick a Task to Run", align="center", font=("Arial", 16, "bold"))
    
    menu_text_pen.goto(0, -200)
    menu_options = (
        "4: Star Triangle\n"
        "5: Triangular Number\n"
        "6: Fibonacci Number\n"
        "7: Simple Tree\n"
        "8: Custom Tree\n"
        "9: Interactive Menu\n"
        "10: Random Blue Tree\n"
        "11: Realistic Tree\n"
        "M: Full App (My Tree Maker)\n"
        "0: Exit"
    )
    menu_text_pen.write(menu_options, align="center", font=("Arial", 12, "normal"))

    while True:
        choice = menu_screen.textinput("Pick a Task", "Enter a task number (0, 4-11, or M):")
        
        if choice is None or choice == '0':
            break
        
        choice = choice.strip().lower()
        if choice == 'm':
            run_task('main')
        else:
            run_task(choice)

    menu_screen.bye()

if __name__ == "__main__":
    open_project_menu()

 
 
  

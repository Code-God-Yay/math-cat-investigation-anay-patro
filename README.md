# Year 8 Maths Investigation - Recursion

By Anay Patro

## What This Project Does

This is my investigation into recursion — when a function calls itself. I've built several programs that use recursion to draw fractal trees and calculate maths sequences.

## Quick Start

To start the project, run:

```
python3 menu.py
```

Pick a task from the menu to explore different examples of recursion.

## What I Learned

Recursion works by breaking a big problem into smaller versions of the same problem. For example:
- **Drawing Trees:** Each branch splits into two smaller branches, and each of those splits again, until we reach a limit
- **Maths Sequences:** To find the 5th triangular number, I find the 4th and add 5 to it. To find the 4th, I find the 3rd and add 4, and so on

## My Challenges

1. **The _tkinter Problem:** My turtle graphics window wouldn't show up at first. I had to install _tkinter separately because it doesn't come with Python by default on all computers.

2. **Making Random Trees Look Real:** If I made the branches too random, they looked broken. If I didn't make them random enough, they looked fake. I had to find the right balance (angles between -10 and +10 degrees worked best).

## Files in This Project

* `menu.py` — Opens the main menu
* `main.py` — The full tree maker app (My Tree Maker)
* `task-4.py` to `task-11.py` — Individual tasks showing different parts of recursion

## How to run it
1. Make sure you have Python installed.
2. Open your terminal in this folder.
3. Run the menu by typing: `python3 menu.py`

## My Investigation Notes
The hardest part was getting the realistic tree to look right. I found that if the 'scale factor' is too high, the tree grows off the screen, and if the 'level' is over 15, the computer slows down a lot because it's calculating thousands of branches. Adding the `random` library made a huge difference in making the trees look like actual plants instead of perfect geometric shapes.
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
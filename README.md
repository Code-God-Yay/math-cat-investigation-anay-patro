# Year 8 Maths Investigation — Recursion
By Anay Patro

### Live slides
[View the presentation website](https://code-god-yay.github.io/math-cat-investigation-anay-patro/)

## What this project is
This is my investigation into **recursion** (when a function calls itself). I built small programs that:
- Print recursive patterns (stars, triangular numbers, Fibonacci)
- Draw **fractal trees** using Turtle graphics
- Add randomness + styling so the trees look more natural

## Quick start (run the Python menu)

```bash
python3 menu.py
```

Then pick a task number to run.

## Files
- `index.html`: the website / slide deck
- `menu.py`: turtle-based launcher for the tasks
- `main.py`: “My Tree Maker” app (interactive tree generator)
- `task-4.py` … `task-11.py`: individual tasks from the investigation

## Notes (what mattered most)
- **Recursion always needs a stopping point** (a base case), otherwise it keeps calling itself forever.
- Trees get expensive fast: each level roughly doubles the number of branches, so huge depths can lag.
- A small amount of randomness makes the output feel “alive”, but too much randomness makes it look broken.

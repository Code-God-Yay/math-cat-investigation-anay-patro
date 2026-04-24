# Year 8 Maths — CAT Investigation 1: Recursion & Fractal Trees

By **Anay Patro**

## Presentation website
- **Live version**: [View the slides on GitHub Pages](https://code-god-yay.github.io/math-cat-investigation-anay-patro/)
- **Run locally**: open `index.html` in your browser (or use a simple local server)

If you want a local server (recommended so everything behaves consistently):

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000` and click `index.html`.

## What this project is
This investigation explains **recursion** (a function calling itself) and uses it to model **fractal trees**. It includes:
- A slide-style website with interactive demos (recursion + fractals)
- Python programs for the individual investigation tasks
- A turtle-graphics tree generator (“My Tree Maker”) with randomness to look more natural

## Quick start (run the Python menu)

```bash
python3 menu.py
```

Then pick a task number to run.

## Requirements
- **Python 3** (turtle is included with standard Python on most systems)

If turtle doesn’t open a window, make sure you’re not running inside a restricted environment and that your Python install includes Tk.

## Project files (high level)
- `index.html`: the website / slide deck
- `menu.py`: launcher for the investigation tasks
- `main.py`: “My Tree Maker” interactive tree generator
- `task-4.py` … `task-11.py`: individual tasks from the investigation

## Key takeaways
- **Recursion needs a base case** (a stopping condition), otherwise it keeps calling forever.
- **Fractals scale fast**: each extra depth level increases branches exponentially, so very large depths can lag.
- **Small randomness helps realism**; too much randomness makes the tree look messy instead of natural.

import json

with open(r"C:\Users\admin\Downloads\GroWise_diagnose.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

with open(r"C:\Projects\GroWise_Fullstack\GroWise\backend\notebook_dump.md", "w", encoding="utf-8") as out:
    for i, cell in enumerate(nb.get("cells", [])):
        if cell["cell_type"] == "code":
            source = "".join(cell.get("source", []))
            out.write(f"### Cell {i}\n```python\n{source}\n```\n\n")

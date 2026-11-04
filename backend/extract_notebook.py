import json

with open(r"C:\Users\admin\Downloads\GroWise_diagnose.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for i, cell in enumerate(nb.get("cells", [])):
    if cell["cell_type"] == "code":
        source = "".join(cell.get("source", []))
        if "load_img" in source or "predict" in source or "tflite" in source or "Interpreter" in source:
            print(f"--- Cell {i} ---")
            print(source)
            print("-" * 40)

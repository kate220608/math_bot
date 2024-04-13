def open_equation(eq):
    with open(f"equation_tasks/{eq}") as f:
        out = f.readlines()
        return out


def open_example(ex):
    with open(f"example_tasks/{ex}") as f:
        out = f.readlines()
        return out

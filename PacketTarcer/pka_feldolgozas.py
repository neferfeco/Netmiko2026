from pywinauto import Application

app = Application(backend="uia").connect(title_re="PT Activity.*")
activity = app.top_window()

print("---- CONTROL TREE ----")
activity.print_control_identifiers()

print("\n---- ALL TEXT ELEMENTS ----")
for elem in activity.descendants():
    text = elem.window_text()
    if text.strip():
        print(f"[{elem.element_info.control_type}] -> '{text}'")

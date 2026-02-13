from pywinauto import Application
import time
import re

PT_PATH = r"C:\Program Files\Cisco Packet Tracer 9.0.0\bin\PacketTracer.exe"
BEADASOK = r"C:\Users\pillerf\Downloads"

def get_score(pka_path):

    app = Application(backend="uia").start(f'"{PT_PATH}" "{pka_path}"')
    time.sleep(10)

    activity = app.window(title_re="PT Activity.*")
    activity.wait("visible", timeout=20)

    # Check Results gomb
    check_btn = activity.child_window(title="Check Results", control_type="Button")
    check_btn.click_input()

    time.sleep(5)

    # Results ablak
    results = app.window(title_re=".*Results.*")
    results.wait("visible", timeout=20)

    score_value = None

    for elem in results.descendants():
        text = elem.window_text()
        if text:
            match = re.search(r"\d+\s*%", text)
            if match:
                score_value = match.group()
                break

    app.kill()

    return score_value

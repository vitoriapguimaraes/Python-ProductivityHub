import sys
import threading
import subprocess
import webview


def start_streamlit():
    """Inicia o servidor Streamlit em background."""
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "Home.py",
        "--server.headless",
        "true",
    ]
    # Roda o processo silenciado
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    print("Iniciando Productivity Hub...")
    # Sobe o servidor em uma thread separada
    t = threading.Thread(target=start_streamlit)
    t.daemon = True
    t.start()

    # Abre a janela nativa conectada no localhost do Streamlit
    webview.create_window(
        "Productivity Hub", "http://localhost:8501", width=1280, height=800
    )
    webview.start()

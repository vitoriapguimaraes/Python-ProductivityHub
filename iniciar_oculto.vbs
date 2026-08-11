Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c """".\.venv\Scripts\python.exe"""" -m streamlit run Home.py --server.headless true", 0, False

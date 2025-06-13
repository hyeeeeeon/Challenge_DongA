import subprocess
import threading
import os

def run_app():
    try:
        subprocess.run(["python", "API/app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Flask 앱 실행 중 오류:", e)

def run_streamlit():
    try:
        result = subprocess.run(
            ["streamlit", "run", "streamlit_app.py", "--server.port=8504"],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Streamlit stdout:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Streamlit 실행 중 오류:")
        print("↪ stdout:\n", e.stdout)
        print("↪ stderr:\n", e.stderr)


if __name__ == "__main__":
    print("🚀 Launcher: Flask API와 Streamlit 대시보드 실행 중...")

    app_thread = threading.Thread(target=run_app)
    streamlit_thread = threading.Thread(target=run_streamlit)

    app_thread.start()
    streamlit_thread.start()

    app_thread.join()
    streamlit_thread.join()

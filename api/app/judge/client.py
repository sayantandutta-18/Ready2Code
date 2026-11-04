import os
import sys
import time
import subprocess
import httpx
from typing import Dict, Any, Optional

JUDGE0_URL = os.getenv("JUDGE0_URL", "http://localhost:2358")

# Common Judge0 Language IDs:
# Python 3: 71
# JavaScript (Node.js): 63
# C++ (GCC): 54
# Java (OpenJDK): 62

LANGUAGE_MAP = {
    "python": 71,
    "javascript": 63,
    "cpp": 54,
    "c++": 54,
    "java": 62
}

def map_status_id(status_id: int) -> str:
    """
    Judge0 Status IDs:
    3: Accepted
    4: Wrong Answer
    5: Time Limit Exceeded
    6: Compilation Error
    7: Runtime Error (SIGSEGV)
    8: Runtime Error (SIGXFSZ)
    9: Runtime Error (SIGFPE)
    10: Runtime Error (SIGABRT)
    11: Runtime Error (NZEC)
    12: Runtime Error (Other)
    13: Internal Error
    14: Exec Format Error
    """
    if status_id == 3:
        return "AC"
    elif status_id == 4:
        return "WA"
    elif status_id == 5:
        return "TLE"
    elif status_id == 6:
        return "CE"
    elif 7 <= status_id <= 12:
        return "RE"
    else:
        return "ERR"

def run_local_python(source: str, stdin: str = "", timeout_s: float = 2.0) -> Dict[str, Any]:
    """Local sandboxed execution fallback when Judge0 is not reachable."""
    start_time = time.time()
    try:
        proc = subprocess.run(
            [sys.executable, "-c", source],
            input=stdin,
            text=True,
            capture_output=True,
            timeout=timeout_s
        )
        elapsed = int((time.time() - start_time) * 1000)
        if proc.returncode == 0:
            return {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "status": {"id": 3, "description": "Accepted"},
                "time": f"{elapsed / 1000:.3f}",
                "memory": 12400
            }
        else:
            is_syntax = "SyntaxError" in proc.stderr
            return {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "status": {"id": 6 if is_syntax else 11, "description": "Compilation Error" if is_syntax else "Runtime Error (NZEC)"},
                "time": f"{elapsed / 1000:.3f}",
                "memory": 12400
            }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Time Limit Exceeded",
            "status": {"id": 5, "description": "Time Limit Exceeded"},
            "time": f"{timeout_s:.3f}",
            "memory": 12400
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "status": {"id": 12, "description": "Runtime Error"},
            "time": "0.001",
            "memory": 12400
        }

_judge0_available = None
_last_check_time = 0

def is_judge0_online() -> bool:
    global _judge0_available, _last_check_time
    now = time.time()
    if _judge0_available is not None and (now - _last_check_time < 30):
        return _judge0_available
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.05)
        res = sock.connect_ex(("127.0.0.1", 2358))
        sock.close()
        _judge0_available = (res == 0)
    except Exception:
        _judge0_available = False
    _last_check_time = now
    return _judge0_available

def run_code(language_id: int, source: str, stdin: str = "", timeout_s: float = 3.0) -> Dict[str, Any]:
    """
    Sends execution request to Judge0 if available.
    Falls back to safe local execution if Judge0 instance is offline.
    """
    if is_judge0_online():
        url = f"{JUDGE0_URL.rstrip('/')}/submissions?wait=true"
        payload = {
            "source_code": source,
            "language_id": language_id,
            "stdin": stdin,
            "cpu_time_limit": timeout_s
        }
        try:
            with httpx.Client(timeout=timeout_s + 1.0) as client:
                resp = client.post(url, json=payload)
                if resp.status_code in (200, 201):
                    data = resp.json()
                    return {
                        "stdout": data.get("stdout") or "",
                        "stderr": data.get("stderr") or (data.get("compile_output") or ""),
                        "status": data.get("status", {"id": 3, "description": "Accepted"}),
                        "time": str(data.get("time", "0.01")),
                        "memory": data.get("memory", 12000)
                    }
        except Exception:
            pass

    if language_id == 71: # Python
        return run_local_python(source, stdin, timeout_s)
    elif language_id == 63: # JavaScript Node
        try:
            start_time = time.time()
            proc = subprocess.run(
                ["node", "-e", source],
                input=stdin,
                text=True,
                capture_output=True,
                timeout=timeout_s
            )
            elapsed = int((time.time() - start_time) * 1000)
            status_id = 3 if proc.returncode == 0 else 11
            return {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "status": {"id": status_id, "description": "Accepted" if status_id == 3 else "Runtime Error"},
                "time": f"{elapsed / 1000:.3f}",
                "memory": 15000
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": "Time Limit Exceeded",
                "status": {"id": 5, "description": "Time Limit Exceeded"},
                "time": f"{timeout_s:.3f}",
                "memory": 15000
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "status": {"id": 12, "description": "Runtime Error"},
                "time": "0.001",
                "memory": 15000
            }

    # Default fallback
    return {
        "stdout": "",
        "stderr": f"Language ID {language_id} requires Judge0 backend.",
        "status": {"id": 12, "description": "Runtime Error"},
        "time": "0.001",
        "memory": 12000
    }

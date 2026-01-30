# Sakura FreeBSD Python 3.8 Log

Start: 2026-01-31T06:59:16.3115861+09:00

Python 3.8.12
Files removed: 98
Requirement already satisfied: pip in /home/garyo/local/python/lib/python3.6/site-packages (21.0.1)
Collecting pip
  Downloading pip-25.0.1-py3-none-any.whl (1.8 MB)
Requirement already satisfied: setuptools in /home/garyo/local/python/lib/python3.6/site-packages (40.6.2)
Collecting setuptools
  Downloading setuptools-75.3.3-py3-none-any.whl (1.3 MB)
Requirement already satisfied: wheel in ./venv/lib/python3.8/site-packages (0.45.1)
Installing collected packages: setuptools, pip
  Attempting uninstall: setuptools
    Found existing installation: setuptools 40.6.2
    Not uninstalling setuptools at /home/garyo/local/python/lib/python3.6/site-packages, outside environment /home/garyo/magic-box-ai/venv
    Can't uninstall 'setuptools'. No files were found to uninstall.
  Attempting uninstall: pip
    Found existing installation: pip 21.0.1
    Not uninstalling pip at /home/garyo/local/python/lib/python3.6/site-packages, outside environment /home/garyo/magic-box-ai/venv
    Can't uninstall 'pip'. No files were found to uninstall.
Successfully installed pip-25.0.1 setuptools-75.3.3
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
Collecting fastapi==0.100.0
  Downloading fastapi-0.100.0-py3-none-any.whl (65 kB)
Collecting pydantic==2.0.0
  Downloading pydantic-2.0-py3-none-any.whl (355 kB)
Collecting uvicorn==0.23.0
  Downloading uvicorn-0.23.0-py3-none-any.whl (59 kB)
Collecting python-multipart==0.0.6
  Downloading python_multipart-0.0.6-py3-none-any.whl (45 kB)
Collecting python-dotenv==1.0.0
  Downloading python_dotenv-1.0.0-py3-none-any.whl (19 kB)
Collecting httpx==0.24.0
  Downloading httpx-0.24.0-py3-none-any.whl (75 kB)
Collecting pytest==7.4.3
  Downloading pytest-7.4.3-py3-none-any.whl (325 kB)
Collecting pytest-asyncio==0.21.1
  Downloading pytest_asyncio-0.21.1-py3-none-any.whl (13 kB)
Collecting starlette<0.28.0,>=0.27.0
  Downloading starlette-0.27.0-py3-none-any.whl (66 kB)
Collecting typing-extensions>=4.5.0
  Downloading typing_extensions-4.13.2-py3-none-any.whl (45 kB)

The conflict is caused by:
    The user requested pydantic==2.0.0
    fastapi 0.100.0 depends on pydantic!=1.8, !=1.8.1, !=2.0.0, !=2.0.1, <3.0.0 and >=1.7.4

To fix this you could try to:
1. loosen the range of package versions you've specified
2. remove package versions to allow pip attempt to solve the dependency conflict

ERROR: Cannot install fastapi==0.100.0 and pydantic==2.0.0 because these package versions have conflicting dependencies.
ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/user_guide/#fixing-conflicting-dependencies
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'fastapi'
Requirement already satisfied: gunicorn in ./venv/lib/python3.8/site-packages (23.0.0)
Requirement already satisfied: packaging in ./venv/lib/python3.8/site-packages (from gunicorn) (26.0)
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
/home/garyo/magic-box-ai/venv/bin/gunicorn
usage: gunicorn [OPTIONS] [APP_MODULE]
gunicorn: error: unrecognized arguments: --version
total 36
drwxr-xr-x  3 garyo  users   512 Jan 31 06:26 .
drwxr-xr-x  7 garyo  users  1024 Jan 31 06:48 ..
-rw-r--r--  1 garyo  users    30 Jan 31 06:26 __init__.py
-rw-r--r--  1 garyo  users  2711 Jan 31 06:26 db.py
-rw-r--r--  1 garyo  users  2550 Jan 31 06:26 logging_utils.py
-rw-r--r--  1 garyo  users  8567 Jan 31 06:26 main.py
drwxr-xr-x  2 garyo  users   512 Jan 31 06:26 static
ls: scripts/: No such file or directory
/home/garyo/magic-box-ai/venv/bin/python3: Error while finding module specification for 'scripts.init_db' (ModuleNotFoundError: No module named 'scripts')
python3: can't open file 'scripts/init_db.py': [Errno 2] No such file or directory
ls: magicboxai.db
: No such file or directory
/home/garyo/magic-box-ai/venv/bin/python3: No module named pytest
tail: test_results_py38.txt
: No such file or directory
System.Management.Automation.RemoteException
Error: class uri 'uvicorn.workers.UvicornWorker' invalid or not found: 
System.Management.Automation.RemoteException
[Traceback (most recent call last):
  File "/home/garyo/magic-box-ai/venv/lib/python3.8/site-packages/gunicorn/util.py", line 110, in load_class
    mod = importlib.import_module('.'.join(components))
  File "/usr/local/lib/python3.8/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1014, in _gcd_import
  File "<frozen importlib._bootstrap>", line 991, in _find_and_load
  File "<frozen importlib._bootstrap>", line 961, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1014, in _gcd_import
  File "<frozen importlib._bootstrap>", line 991, in _find_and_load
  File "<frozen importlib._bootstrap>", line 973, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'uvicorn'
]
System.Management.Automation.RemoteException
Gunicorn test startup completed
Python 3.8.12
Sat Jan 31 07:00:48 JST 2026
www1026.sakura.ne.jp
Python 3.8.12
Sat Jan 31 07:01:01 JST 2026
www1026.sakura.ne.jp

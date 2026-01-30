C:\project\virtual-company\magicboxai\main.py:92: DeprecationWarning: 
        on_event is deprecated, use lifespan event handlers instead.

        Read more about it in the
        [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
        
  @app.on_event("startup")
2026-01-31 05:29:36,726 [ERROR] magicboxai - Uncaught exception
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\config.py", line 587, in configure
    formatters[name] = self.configure_formatter(
                       ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\config.py", line 699, in configure_formatter
    result = self.configure_custom(config)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\config.py", line 490, in configure_custom
    result = c(**kwargs)
             ^^^^^^^^^^^
  File "C:\Users\garyo\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\uvicorn\logging.py", line 42, in __init__
    self.use_colors = sys.stdout.isatty()
                      ^^^^^^^^^^^^^^^^^
AttributeError: 'DualWriter' object has no attribute 'isatty'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\project\virtual-company\magicboxai\main.py", line 256, in <module>
    uvicorn.run("magicboxai.main:app", host="0.0.0.0", port=8000, reload=False)
  File "C:\Users\garyo\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\uvicorn\main.py", line 522, in run
    config = Config(
             ^^^^^^^
  File "C:\Users\garyo\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\uvicorn\config.py", line 285, in __init__
    self.configure_logging()
  File "C:\Users\garyo\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\uvicorn\config.py", line 393, in configure_logging
    logging.config.dictConfig(self.log_config)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\config.py", line 942, in dictConfig
    dictConfigClass(config).configure()
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\config.py", line 590, in configure
    raise ValueError('Unable to configure '
ValueError: Unable to configure formatter 'default'

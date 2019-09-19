copy /Y LICENSE LICENSE.txt
copy /Y docs\source\readme.rst readme.rst
copy /Y docs\source\readme.rst glance\readme.rst
venv\Scripts\python.exe setup.py bdist_wheel upload -r pypi
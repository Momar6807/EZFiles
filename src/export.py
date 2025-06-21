import os
import subprocess

dir = os.getcwd()
print(dir)

# ejecutar pyinstaller

response = subprocess.run(
    ["pyinstaller", "--onefile", "--windowed", "--name", "EZFiles",
        "--icon", "icono.ico", "--add-data", "icono.ico;.", "main.py"],
    stdout=subprocess.PIPE,
    cwd=dir
)


print(response.stdout.decode('utf-8'))

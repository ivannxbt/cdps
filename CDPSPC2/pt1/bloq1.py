import subprocess
import os

def replace_text_in_file(file_path, old_text, new_text):
    with open(file_path, 'r') as f:
        contents = f.read()
    contents = contents.replace(old_text, new_text)
    with open(file_path, 'w') as f:
        f.write(contents)

#Clonar el repositorio de git
subprocess.run(["git", "clone", "https://github.com/CDPS-ETSIT/practica_creativa2.git"])
os.chdir('./practica_creativa2/bookinfo/src/productpage/')
os.environ['GROUP_NUMBER'] = "43"
#Modificar el código para mostrar el nombre del grupo en el título
replace_text_in_file('requirements.txt', 'urllib3==1.26.5', 'urllib3')
replace_text_in_file('requirements.txt', 'chardet==3.0.4', 'chardet')
replace_text_in_file('requirements.txt', 'gevent==1.4.0', 'gevent')
replace_text_in_file('requirements.txt', 'greenlet==0.4.15', 'greenlet')
replace_text_in_file('templates/productpage.html', 'Simple Bookstore App', os.environ.get('GROUP_NUMBER'))
#Instalar las dependencias
subprocess.run(["pip", "install", "-r", "requirements.txt"])
subprocess.run(["sudo", "apt-get", "install", "python3-pip"])

#Ejecutar la aplicación en un puerto específico
subprocess.run(["python3", "productpage_monolith.py", 9080])
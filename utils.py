ip = '3.149.24.51'
key_file = 'api_key.pem'

########################################################### Función que envía los archivos a AWS

import subprocess

def send_file_to_ec2(path, user, key_file, ip, local_file, remote_path):
    # Construir el comando SSH
    command = f'scp -o StrictHostKeyChecking=no -i {key_file} {path+local_file} {user}@{ip}:{remote_path}'

    # Ejecutar el comando
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Esperar a que el comando se complete
    stdout, stderr = process.communicate()
    
    # Verificar si el comando se ejecutó correctamente
    if process.returncode != 0:
        print(f'Error: {stderr.decode()}')
    else:
        print('Archivo enviado con éxito')
        

###########################################################  Función que procesa el modelo en AWS

def procesar_model(user, key_file, ip, local_file, variable):
    # Construir el comando SSH
    command = f"ssh -o StrictHostKeyChecking=no -i "+key_file+" "+user+"@"+ip+" python3 model.py ./temp_data/"+local_file+" "+ variable

    # Ejecutar el comando
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Esperar a que el comando se complete
    stdout, stderr = process.communicate()
    
    # Verificar si el comando se ejecutó correctamente
    if process.returncode != 0:
        print(f'Error: {stderr.decode()}')
    else:
        print('Archivo procesado con éxito')



def traer_archivo(user, key_file, ip, local_file, remote_path,file, variable):
    file = './data/cliente_'+ ''.join(caracter for caracter in local_file if caracter.isdigit()) +'_'+variable+file[-4:]
    print(file)
    comando = f'scp -o StrictHostKeyChecking=no -i {key_file} {user}@{ip}:{file} {remote_path + file[7:]}'
    proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proceso.communicate()
    
    # Verificar si el comando se ejecutó correctamente
    if proceso.returncode != 0:
        print(f'Error: {stderr.decode()}')
    else:
        print('Fin del proceso')
        
 
###########################################################   Función que trae el archivo de AWS
   
        
def procesar(path, file, variable, user='ubuntu', llave='api_key.pem', ip=ip):
    send_file_to_ec2(path, user, llave, ip, file, '/home/ubuntu/temp_data/'+file)
    procesar_model(user, llave, ip, file, variable)
    traer_archivo(user, llave, ip, file, './results/',file, variable)

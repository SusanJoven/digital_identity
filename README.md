# Identidad digital 

## Descripción

Prototipo de un sistema de identidad digital propuesto para los miembros de la Universidad de los Andes.
El prototipo hace uso del Indy-SDK proporcionado por el proyecto Hyperledger Indy. Las líbrerías requeridas no se encuentran en este repositorio pero se pueden descargar del repositorio de Hyperledger Indy: https://github.com/hyperledger/indy-sdk

## Manual para uso del prototipo

Para descargar, construir y ejecutar el prototipo se requiere la instalación previa de python 3.7 y seguir las siguientes instrucciones:

•	Instalar el SDK de Hyperledger Indy siguiendo los pasos disponibles en el repositorio: 
https://github.com/hyperledger/indy-sdk#installing-the-sdk

•	Para construir la red virtual de nodos es necesario instalar Docker Desktop:
https://docs.docker.com/desktop/#download-and-install

•	Clonar el código del prototipo disponible en el repositorio con el siguiente comando: git clone https://github.com/SusanJoven/digital-identity.git

•	Debido a que en el repositorio del paso anterior no se encuentran las librerías requeridas, es necesario mover la carpeta libindy a la carpeta con el código del paso anterior. 

•	En la carpeta digital-identity es necesario construir el mismo siguiendo los pasos disponibles en el repositorio:
https://github.com/hyperledger/indy-sdk#how-to-build-indy-sdk-from-source

•	Abrir la carpeta en algún editor de código. 

•	Inicializar el pool de nodos locales con los comandos disponibles en:
https://github.com/hyperledger/indy-sdk/blob/master/README.md#1-starting-the-test-pool-on-localhost

•	Para ejecutar el código, dentro de la carpeta digital-identity, se escribe el siguiente comando: python3 –m src,.main.



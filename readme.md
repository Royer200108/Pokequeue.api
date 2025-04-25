# PokeQueue API

En este repositorio se encuentra el código fuente de la API personal utilizada para generar reportes en el proyecto PokeQueue para el manejo de colas.

## ¿Qué herramientas y tecnologías utiliza?

Para este proyecto se utilizaron las tecnologías:

* Python 3.13.1: Como lenguaje principal.
* pyenv: Como un gestor de versiones de python
* Docker: Como gestor de contenedores para facilitar el despliegue de la webapp en la nube.
* Azure COntainer Registry: Como gestor de imagenes de docker en la nube.

## ¿Cómo configurar el ambiente virtual para correr el proyecto en local?

___Observación.___ Para poder configurar el ambiente virtual es necesario contar previamente con pyenv instalado.

1. Instalación de pyhton 3.10
    ```bash
    pyenv install 3.13.1
    ```

2. Creación del ambiente virtual
    ```bash
    pyenv virtualenv 3.13.1 nombre_entorno
    ```

3. Activación del ambiente virtual
    ```bash
    pyenv activate nombre_entorno
    ```

4. Instalar todas las dependencias de Python especificadas en el fichero "requirements.txt" usando pip:
    ```bash
    pip install nombre_dependencia
    ```

5. Ejecutar de manera local:
    ```bash
    uvicorn main:app --reload
    ```

## ¿Cómo contenerizar y hacer el release del proyecto?

### Proceso de contenerizar la aplicación

___Observación___ Para poder realizar este proceso es necesario contar previamente Docker instalado.

1. Hacer el build de la imagen:
    ```
    bash docker build -t pokeapi:latest . --load
    ````

2. Crear un contenedor (instancia) de esa imagen para correr la aplicación de forma local:
    ```bash
    docker run -d -p 8000:8000 --name pokeapi-container --env-file .env pokeapi:latest
    ```

### Proceso de hacer el release de la aplicación

___Observación___ Para poder realizar este proceso es necesario contar previamente con azure cli instalado.

1. Iniciar sesión de azure en la consola que se está utilizando:

    ```bash
    az login
    ```

2. Indicar el nombre del container registry en el que se subirá el contenedor:



3. Agregar las etiquetas a la nueva imagen que se subirá:

    ```bash
        docker tag pokeapi:latest nombre_container_registry.azurecr.io/pokeapi:latest


        // Este comando cambiará con cada nueva release que se haga (comenzará siendo la 0.0.0)
        docker tag pokeapi:latest nombre_container_registry.azurecr.io/pokeapi:0.0.0
    ```

4. Subir (hacer push) de la imagen previamente etiquetada al azure container registry:

    ```bash
    docker push nombre_container_registry.azurecr.io/pokeapi:latest

    docker push nombre_container_registry.azurecr.io/pokeapi:0.0.0
    ```

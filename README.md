# Gestures Recognition with Python

> This `README` file was originally written in Brazilian Portuguese. For the English version, check [The English Section](#english-section).


## Seção em Português

Utiliza conceitos de visão computacional e aprendizado de máquina para reconhecer gestos em tempo real e controlar uma inferace WEB sem [HIDs](https://en.wikipedia.org/wiki/Human_interface_device) físicos.


### Instalação

1. Clone o projeto e entre na pasta
    ```bash
    git clone https://github.com/IFjoaop051/gesture-recon-py.git
    ```
    ```bash
    cd gesture-recon-py
    ```

2. Crie um ambiente virtual para o Python
    ```bash
    python3 -m venv ./.venv
    ```

3. Inicialize o ambiente virtual no terminal
    ```bash
    source ./.venv/scripts/activate
    ```

    ou para máquinas Windows
    ```bash
    .\.venv\Scripts\activate
    ```

4. Instale as bibliotecas necessárias
    ```bash
    python3 -m pip install -r ./requirements.txt
    ```

<!-- > [!IMPORTANT] show it on github readmes -->
> Para que o projeto funcione, é necessário baixar um modelo que foi pré-treinado pelo Google e colocar o arquivo `gesture_recognizer.task` dentro da pasta `model_tasks`, encontrada na raiz do projeto. [Baixe o modelo aqui](https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task).

5. Rode o projeto
    ```bash
    python3 ./main.py
    ```


> Este projeto foi desenvolvido em 2026 como parte de uma atividade avaliativa da disciplina `Tópicos Avançados em Informática` do Curso Técino em Informática Integrado ao Ensino Médio do [Instituto Federal de Santa Catarina - Câmpus Xanxerê](https://ifsc.edu.br/web/campus-xanxere).


## English Section

It uses Computer Vision and Machine Learning concepts to recognize gestures in real time and control a WEB interface with it, eliminating the use of physical [HIDs](https://en.wikipedia.org/wiki/Human_interface_device).


### Installation

1. Clone the project and go to it's folder
    ```bash
    git clone https://github.com/IFjoaop051/gesture-recon-py.git
    ```
    ```bash
    cd gesture-recon-py
    ```

2. Create a virtual environment for Python
    ```bash
    python3 -m venv ./.venv
    ```

3. Initialize the virtual environment in the terminal
    ```bash
    source ./.venv/scripts/activate
    ```

    or for Windows machines
    ```bash
    .\.venv\Scripts\activate
    ```

4. Install the needed libraries
    ```bash
    python3 -m pip install -r ./requirements.txt
    ```

<!-- > [!IMPORTANT] show it on github readmes -->
> For the project to work, you need to download a model pre-trained by Google and place the `gesture_recognizer.task` file inside the `model_tasks` folder, located at the project root. [Download the model file here](https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task).

5. Run the application
    ```bash
    python3 ./main.py
    ```


> This project was developed in 2026 as part of an assessment activity of the subject `Tópicos Avançados em Informática` do Technical Course in Informatics Integrated with High School Education of [Instituto Federal de Santa Catarina - Câmpus Xanxerê](https://ifsc.edu.br/web/campus-xanxere).

# Sistema de Reconhecimento Facial

> **Status do projeto: Em desenvolvimento**

Projeto semestral desenvolvido em colaboração com meu grupo, utilizando Python e suas bibliotecas, com o objetivo de explorar conceitos de visão computacional, detecção facial e controle de acesso.

A aplicação utiliza a biblioteca OpenCV para capturar imagens de uma webcam e detectar rostos em tempo real. Futuramente, contará com uma interface gráfica que permitirá a identificação das pessoas cadastradas, a associação de cada rosto ao respectivo cargo e o gerenciamento de níveis de acesso de acordo com as permissões atribuídas a cada função.

O projeto ainda está em desenvolvimento, com foco na integração entre visão computacional, interface gráfica e controle de acesso, além da organização do código e da implementação gradual de novas funcionalidades.


##  Objetivos

- Aprender e aplicar conceitos de visão computacional.
- Implementar detecção facial em tempo real.
- Trabalhar com captura e processamento de imagens.
- Praticar organização de código e separação de responsabilidades em Python.

## Tecnologias utilizadas

- **Python** — linguagem de programação principal.
- **OpenCV** — biblioteca para processamento de imagens, captura de vídeo e detecção facial.
- **Haar Cascade Classifier** — modelo utilizado para detectar rostos nas imagens capturadas.
- **Webcam** — dispositivo utilizado para captura de vídeo em tempo real.

## Funcionalidades implementadas

- [x] Captura de vídeo por meio da webcam.
- [x] Detecção facial utilizando o classificador Haar Cascade.
- [x] Identificação das faces presentes nos quadros capturados.
- [x] Desenho de retângulos ao redor dos rostos detectados.
- [x] Suavização da posição dos retângulos para reduzir oscilações visuais.


## Estrutura do projeto (até o momento)

```text
reconhecimento-facial/
├── main.py
├── deteccao_facial.py
├── cadastro.py
└── README.md
```

- **`main.py`** — responsável por iniciar a aplicação, acessar a webcam e executar o fluxo principal de detecção.
- **`deteccao_facial.py`** — concentra as funções relacionadas ao carregamento do detector e à identificação de rostos.
- **`cadastro.py`** — responsável por cadastrar e armazenar os dados das pessoas para uso futuro no sistema. 
- **`README.md`** — documentação do projeto.



## Aprendizados

Este projeto faz parte do meu processo de aprendizado em Python e visão computacional, permitindo explorar conceitos como:

- Manipulação e processamento de imagens.
- Captura e leitura de vídeo em tempo real.
- Utilização de classificadores para detecção de objetos.
- Criação e reutilização de funções.
- Modularização e organização de código.
- Tratamento de erros e controle do fluxo da aplicação.

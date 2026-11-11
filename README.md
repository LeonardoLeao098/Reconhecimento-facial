# Sistema de Reconhecimento Facial - FACESHIELD


Projeto semestral desenvolvido em colaboração com meu grupo, utilizando Python e suas bibliotecas, com o objetivo de explorar conceitos de visão computacional, reconhecimento facial e controle de acesso.

A aplicação utiliza a biblioteca OpenCV para capturar imagens de uma webcam, detectar e reconhecer rostos em tempo real. O sistema conta com uma interface gráfica que permite cadastrar usuários, associar rostos aos respectivos dados e gerenciar níveis de acesso de acordo com as permissões atribuídas a cada função.

O projeto integra visão computacional, reconhecimento facial, armazenamento de dados e controle de acesso em uma aplicação com interface gráfica.

## Objetivos

- Aprender e aplicar conceitos de visão computacional.
- Implementar detecção e reconhecimento facial em tempo real.
- Trabalhar com captura e processamento de imagens.
- Desenvolver um sistema de cadastro e gerenciamento de usuários.
- Implementar controle de acesso baseado em níveis de permissão.
- Praticar organização de código e separação de responsabilidades em Python.

## Tecnologias utilizadas

- Python — linguagem de programação principal.
- OpenCV — biblioteca para processamento de imagens, captura de vídeo e reconhecimento facial.
- Haar Cascade Classifier — modelo utilizado para detectar rostos nas imagens capturadas.
- LBPH (Local Binary Patterns Histograms) — algoritmo utilizado para reconhecimento facial.
- Tkinter — biblioteca utilizada para desenvolvimento da interface gráfica.
- Pillow — biblioteca para manipulação e exibição de imagens.
- NumPy — biblioteca utilizada para operações e processamento de dados.
- JSON — formato utilizado para armazenamento dos dados dos usuários.
- Webcam — dispositivo utilizado para captura de vídeo em tempo real.



## Estrutura do projeto

    FACESHIELD
    ├── componentes/
    ├── telas/
    ├── banco_dados.py
    ├── cadastro.py
    ├── configurar_administrador.py
    ├── controle_acesso.py
    ├── deteccao_facial.py
    ├── main.py
    ├── reconhecimento.py
    ├── treinamento.py
    └── README.md

- `main.py` — responsável por iniciar a aplicação e integrar as funcionalidades do sistema.
- `telas/` — contém as telas da interface gráfica.
- `componentes/` — reúne componentes reutilizáveis da interface.
- `deteccao_facial.py` — concentra as funções relacionadas ao carregamento do detector e à identificação de rostos.
- `cadastro.py` — responsável pelo cadastro de usuários, captura de amostras faciais e exclusão de registros.
- `banco_dados.py` — gerencia o armazenamento, a consulta e a listagem dos dados dos usuários, utilizando arquivos JSON.
- `treinamento.py` — processa as imagens faciais cadastradas e treina o modelo de reconhecimento utilizando o algoritmo LBPH.
- `reconhecimento.py` — realiza o reconhecimento facial em tempo real e identifica os usuários cadastrados.
- `controle_acesso.py` — gerencia as permissões e os níveis de acesso dos usuários.
- `configurar_administrador.py` — responsável pela configuração do administrador do sistema.
- `README.md` — documentação do projeto.


# Pomodoro Timer

Timer Pomodoro em Python com interface gráfica feita em Tkinter: contagem regressiva, ciclo automático de pausas e alarme sonoro ao fim de cada etapa.

## Sobre

Projeto final da disciplina **Linguagens e Técnicas de Programação para Engenharia** (CEFET/RJ).

Também nasceu de uma vontade antiga: ter um Pomodoro próprio, sem depender de sites como o [pomofocus.io](https://pomofocus.io).

## Funcionalidades

- [x] Interface com abas: Pomodoro, Pausa Curta e Pausa Longa
- [x] Botões Start, Pause e Skip
- [x] Contador de pomodoros na tela
- [x] Contagem regressiva
- [x] Ciclo automático (4 pomodoros → pausa longa)
- [x] Som / notificação ao fim de cada etapa
- [ ] Durações editáveis pela interface

## Durações padrão

| Etapa       | Duração |
|-------------|---------|
| Pomodoro    | 25 min  |
| Pausa curta | 5 min   |
| Pausa longa | 15 min  |

As durações são definidas como constantes no topo de `pomodoro.py`.

## Baixar o executável

Na aba [Releases](https://github.com/ianldap/pomodoro-python/releases), baixe `Pomodoro.exe` e execute. Não é necessário ter Python instalado.

> O Windows pode exibir um aviso do SmartScreen por o executável não ter assinatura digital. Clique em "Mais informações" → "Executar assim mesmo".

## Rodar pelo código-fonte

Requer Python 3 com Tkinter (já vem incluso no Python para Windows e macOS).

No Linux (Debian/Ubuntu), se faltar o Tkinter:

```bash
sudo apt install python3-tk
```

Depois:

```bash
git clone https://github.com/ianldap/pomodoro-python.git
cd pomodoro-python
python -m pip install -r requirements.txt
python pomodoro.py
```

## Gerar o executável

Instale as ferramentas de build:

```bash
python -m pip install pyinstaller pillow
```

Gere o `Pomodoro.exe` (fica em `dist/`):

```bash
python -m PyInstaller --noconfirm --clean --onefile --windowed --name Pomodoro --icon pomodoro.ico --add-data "alarme.mp3;." --add-data "pomodoro.png;." pomodoro.py
```

## Estrutura

```
pomodoro-python/
├── pomodoro.py        # código principal
├── pomodoro.png       # ícone da janela
├── pomodoro.ico       # ícone do executável
├── alarme.mp3         # som tocado ao fim de cada etapa
├── requirements.txt   # dependências do projeto
└── README.md
```

## Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

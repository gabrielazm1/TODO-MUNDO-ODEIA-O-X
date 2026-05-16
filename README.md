# 🎮 Todo Mundo Odeia...

> O jogo de mira mais pessoal do mundo — crie seu alvo e elimine-o!

---

## 👥 Membros do Grupo
*(Adicione os nomes dos membros aqui)*

---

## 🕹️ Como Jogar

### Instalação

1. Instale o Python 3.10 ou superior
2. Instale as dependências:

```bash
pip install pygame pillow numpy
```

3. Execute o jogo:

```bash
python main.py
```

### Estrutura do Projeto

```
todo_mundo_odeia/
├── main.py          # Código principal do jogo
├── README.md        # Este arquivo
└── assets/
    ├── Character Model.png   # Sprite sheet de corpos (MetroCity)
    ├── Hairs.png             # Sprite sheet de cabelos (MetroCity)
    ├── Outfit1-6.png         # Sprite sheets de roupas (MetroCity)
    ├── Heart.png             # Ícone de coração (vida do alvo)
    └── gun_sheet.png         # Sprite sheet da arma
```

---

## 🎯 Regras do Jogo

- **Objetivo:** Matar o alvo antes que suas munições acabem!
- 🖱️ Mire com o mouse e **clique** para atirar
- ❤️ O alvo possui **3 vidas** (corações no canto superior direito)
- ⚡ A cada acerto, o alvo fica **mais rápido**
- 🔫 Você começa com **15 munições**
- ⭐ Estrelas douradas aparecem no cenário — acerte-as para ganhar **+3 munições**

---

## 🖥️ As 8 Telas do Jogo

| # | Tela | Descrição |
|---|------|-----------|
| 1 | Menu Principal | Botões "Jogar" e "Instruções" |
| 2 | Instruções | Regras detalhadas do jogo |
| 3 | Nome do Alvo | "Todo mundo odeia..." + campo de texto |
| 4 | Escolha do Corpo | 4 opções: menina/menino branca(o)/negra(o) |
| 5 | Escolha da Roupa | 6 opções: 3 femininas + 3 masculinas |
| 6 | Escolha do Cabelo | 4 opções: longo loiro, longo moreno, curto loiro, curto moreno |
| 7 | Prévia do Personagem | Composição final antes do jogo |
| 8 | O Jogo | Atire no alvo com a arma seguindo o mouse |
| + | Vitória / Derrota | Tela final com resultado |

---

## 🛠️ Tecnologias Utilizadas

- **Python 3** — Linguagem principal
- **Pygame** — Motor gráfico e de eventos
- **Pillow (PIL)** — Processamento de imagens (extração da arma)
- **NumPy** — Manipulação de arrays de pixels

---

## 🎨 Assets Externos

- **MetroCity Character Pack** — Sprites de personagens, roupas e cabelos
  - Fonte: asset pack RPG (MetroCity)
- **Heart sprite** — Ícone de coração para vidas
- **Gun sprite sheet** — Sprite sheet da arma usada como cursor

---

## 🤖 Uso de IA

*(Preencha aqui conforme o uso durante o desenvolvimento)*

Exemplo: "A estrutura inicial do `main.py` foi desenvolvida com auxílio de IA generativa. Todo o código foi revisado, entendido e adaptado pelos membros do grupo."

---

## 📹 Vídeo de Apresentação

*(Adicione aqui o link do vídeo no YouTube/Vimeo mostrando o jogo funcionando)*

---

## 🔧 Dependências

```
pygame>=2.0.0
Pillow>=9.0.0
numpy>=1.20.0
```

## Todo Mundo Odeia o X

Um jogo de tiro feito em **Python + Pygame**, com tema espacial e personagem customizável. O jogador cria seu próprio "alvo" (escolhendo corpo, roupa, cabelo e nome) e precisa derrotá-lo antes que a munição acabe — enquanto o alvo se move pelo cenário e fica cada vez mais rápido a cada tiro disparado.

---

## Integrantes do Grupo

- Camila Pihal Borba
- Gabriela Ferreira Loiola
- Gabriela Zanoide de Moraes


## Sobre o Jogo

1. Digita o **nome** do alvo que deseja "eliminar";
2. Personaliza o personagem escolhendo **corpo, roupa e cabelo**;
3. Entra em uma arena espacial onde deve **acertar o alvo 3 vezes para ganhar** com o mouse;
4. Possui apenas **10 munições iniciais** — cada tiro é munição perdida;
5. Pode acertar **estrelas amarelas** que aparecem aleatoriamente no cenário para ganhar **+3 munições extras**;
6. Vence se zerar as vidas do alvo; perde se ficar sem munição.

Além disso, a dificuldade aumenta progressivamente: a cada tiro disparado o alvo acelera e ele ainda muda de direção sozinho de tempos em tempos para dificultar a mira.

---
## Como Rodar o Jogo
## Pré-requisitos
Ter instalado Python 3.8 ou superior e o pip (gerenciador de pacotes do Python).
## Bibliotecas Necessárias
A biblioteca pygame. A biblioteca numpy para o processamento de imagens e a biblioteca Pillow (importada como PIL) é usada para manipulação avançada da sprite da arma.
## Estrutura de Pastas
Para o jogo funcionar corretamente, dentro da pasta assets estam os seguintes arquivos: Character Model.png, Hairs.png, Outfit1.png, Outfit2.png, Outfit3.png, Outfit4.png, Outfit5.png, Outfit6.png, Heart.png (ou Pixel Heart Sprite Sheet 32x32.png / 16x16.png), Estrela.png, New Piskel.png (sprite da arma) e cenario universo.png (fundo do jogo).

## Executando o Jogo
Abra o terminal na pasta do projeto e rode o comando: python main.py

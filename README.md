# Letramento Digital - Quiz

Um projeto de quiz interativo voltado para ensinar conceitos de letramento digital, como segurança online, privacidade, e cidadania digital. O quiz foi desenvolvido usando HTML, CSS, JavaScript e Python com Flask, e busca testar e aprimorar o conhecimento dos usuários sobre temas essenciais do mundo digital.

## Descrição

O **Letramento Digital Quiz** é uma aplicação web onde os usuários podem responder perguntas sobre diversos temas ligados à tecnologia e segurança digital. As perguntas são retiradas de uma planilha Excel, e o sistema apresenta um placar final baseado nas respostas corretas.

https://letramento-digital-quiz.onrender.com/

## Funcionalidades

- **Perguntas Aleatórias:** O quiz seleciona perguntas aleatórias de um arquivo Excel que cobre temas variados de letramento digital.
- **Pontuação:** O usuário ganha 1 ponto por cada resposta correta.
- **Resolução de Respostas Incorretas:** Se o usuário errar uma resposta, o quiz exibe a pontuação final e termina o jogo.
- **Registro de Pontuação:** A pontuação do usuário é salva para possível análise ou revisão futura.
- **Material de Consulta:** Cada pergunta tem um link para material educativo, como vídeos ou textos, para ajudar o usuário a aprender sobre o tema abordado.

## Tecnologias Utilizadas

- **HTML** para a estrutura da página.
- **CSS** para o design e layout.
- **JavaScript** para a lógica do quiz e interação com o usuário.
- **Excel** como banco de dados de perguntas e respostas.
- **Flask** para o backend da aplicação.
- **pandas** para manipulação dos dados da planilha Excel.

## Como Rodar o Projeto

1. **Clone o Repositório:**
   ```bash
   git clone https://github.com/GuilhermeSavioRibas/Letramento-Digital-Quiz.git

2. **Navegue até o Diretório do Projeto:**

    ```bash
    cd letramento-digital-quiz

3. **Configure o Arquivo de Perguntas:**

    Certifique-se de que o arquivo perguntas.xlsx está no mesmo diretório que o seu script app.py.

4. **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    
5. **Execute o Servidor Flask:**
    ```bash
    python app.py

6. **Abra o servidor criado em um navegador web**
    Exemplo: http://127.0.0.1:5000

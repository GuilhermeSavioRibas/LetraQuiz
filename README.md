# Letramento Digital - Quiz

Um projeto de quiz interativo voltado para ensinar conceitos de letramento digital, como segurança online, privacidade, cidadania digital, e outros temas variados definidos por administradores. O quiz foi desenvolvido usando **HTML**, **CSS**, **JavaScript**, **Python com Flask** e **SQLite**, buscando testar e aprimorar o conhecimento dos usuários sobre temas essenciais.

## Descrição

O **Letramento Digital Quiz** é uma aplicação web onde os usuários podem responder perguntas criadas por administradores sobre diversos temas. Com diferentes funcionalidades interativas, o sistema permite uma experiência dinâmica, educativa e divertida. 

## Funcionalidades

- **Sistema de Login e Registro:** Permite autenticação de usuários com senhas seguras.
- **Temas Personalizáveis:** Os administradores podem criar temas e adicionar perguntas diretamente na aplicação.
- **Perguntas Aleatórias:** As perguntas de um tema são exibidas aleatoriamente.
- **Pontuação e Recursos Especiais:** O quiz inclui pontuação e recursos como "pular perguntas", "consultar artigos", e "usar cartas".
- **Registro de Resultados:** Os resultados são salvos para análise futura, e os melhores desempenhos são exibidos em um ranking.
- **Material Educativo:** Algumas perguntas incluem links para materiais de apoio, como artigos ou vídeos, para aprendizado complementar.
- **Administração de Perguntas:** Administradores podem gerenciar perguntas e temas diretamente no sistema.

## Tecnologias Utilizadas

- **HTML** e **CSS** para estrutura e estilo.
- **JavaScript** para interações e dinâmica.
- **Python (Flask)** para o backend.
- **SQLite** como banco de dados para persistência de dados.
- **Werkzeug** para gerenciamento seguro de senhas.

## Como Rodar o Projeto

1. **Clone o Repositório:**

    ```bash
    git clone https://github.com/GuilhermeSavioRibas/Letramento-Digital-Quiz.git
    ```

2. **Navegue até o Diretório do Projeto:**

    ```bash
    cd letramento-digital-quiz
    ```

3. **Instale as Dependências:**

    Certifique-se de ter o **Python** instalado e execute:

    ```bash
    pip install -r requirements.txt
    ```

4. **Execute o Servidor Flask:**

    ```bash
    python app.py
    ```

5. **Acesse o Aplicativo no Navegador:**

    Abra o endereço [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Estrutura do Projeto

- **app.py:** Arquivo principal do servidor Flask.
- **templates/**: Arquivos HTML para renderização de páginas.
- **static/**: Arquivos de CSS, imagens e JavaScript.
- **quiz.db:** Banco de dados SQLite para persistência de informações.

## Futuras Melhorias

- Suporte para mais idiomas e acessibilidade.
- Gamificação, como conquistas e níveis.
- Estatísticas detalhadas de desempenho.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar **pull requests** ou abrir **issues** para sugestões e melhorias.

---

**Desenvolvido por Guilherme Sávio Ribas e contribuidores.**

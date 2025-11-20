# 🎓 Análise e Predição de Evasão de Alunos com Machine Learning

> **Autores do Projeto:** Geraldo & Emanuel
> **Contexto:** Análise de dados educacionais para identificar padrões de evasão em cursos superiores (Ciência da Computação e ADS).

## 📋 Sobre o Projeto

A evasão no ensino superior é um problema complexo que impacta instituições e alunos. Este projeto utiliza **Ciência de Dados** e **Machine Learning** para analisar dados históricos, socioeconômicos e de relacionamento de alunos, com o objetivo de:

1.  **Diagnosticar:** Entender quais fatores (acadêmicos ou sociais) têm maior correlação com o abandono do curso.
2.  **Predizer:** Criar modelos capazes de classificar se um aluno é propenso a desistir com base em seu comportamento inicial.

O projeto foi estruturado seguindo o pipeline clássico de Data Science: **ETL (Extração e Limpeza) -> EDA (Análise Exploratória) -> Engenharia de Atributos -> Modelagem Preditiva**.

---

## 🛠 Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Manipulação de Dados:** Pandas, NumPy
* **Visualização:** Matplotlib, Seaborn
* **Machine Learning:** Scikit-learn (Sklearn)

---

## ⚙️ Metodologia e Pipeline de Dados

### 1. Tratamento e Limpeza (Data Cleaning)
Baseado nos dados brutos (`DadosAlunos.xlsx`), realizamos uma "faxina" estratégica:
* **Unificação de Notas:** As notas de ingresso ("Nota Enem" e "Escore Vest") foram fundidas em uma única métrica (`Nota Final`).
* **Tratamento de Frequência:** Para disciplinas especiais (ex: TCC, Diplomação), onde a frequência não é registrada tradicionalmente, assumimos 100% de presença para evitar ruídos.
* **Remoção de Nulos:** Optou-se pela remoção de linhas com dados cruciais faltantes (como notas históricas) em vez de imputação (preenchimento artificial), garantindo que o modelo treine apenas com dados reais e confiáveis.

### 2. Engenharia de Atributos (Feature Engineering)
Para alimentar os modelos, criamos variáveis sintéticas que resumem a vida acadêmica do aluno:
* `Porcentagem_Reprovacao`: Razão entre disciplinas reprovadas e total cursado.
* `Nota Media`: Média aritmética de todas as notas do histórico.
* `Frequencia Media`: Média de presença em todas as aulas.
* `Precisa Trabalhar`: Variável booleana derivada do questionário socioeconômico.

---

## 🧠 Teoria dos Modelos de Machine Learning Aplicados

Para a fase de classificação (Prever: *Desistente* ou *Não Desistente*), testamos quatro algoritmos com abordagens teóricas distintas:

### 🌲 1. Random Forest (Floresta Aleatória)
* **O que é:** Um método de *Ensemble* (conjunto) que cria várias Árvores de Decisão durante o treinamento.
* **Como funciona:** Cada árvore vota em uma classe e a classe com a maioria dos votos se torna a predição do modelo.
* **Por que usar:** É excelente para evitar *overfitting* (sobreajuste) e lida muito bem com relações não lineares e complexas entre as variáveis.

### 📈 2. Regressão Logística
* **O que é:** Um modelo estatístico usado para problemas de classificação binária.
* **Como funciona:** Estima a probabilidade de um evento ocorrer (0 a 1) usando a função Sigmoide. Se a probabilidade for > 50%, classifica como "Desistente".
* **Vantagem:** Alta interpretabilidade. Permite ver exatamente o peso (coeficiente) de cada variável, indicando se ela aumenta ou diminui o risco de evasão.

### 📊 3. Naive Bayes (Gaussiano)
* **O que é:** Um classificador probabilístico baseado no Teorema de Bayes.
* **Teoria:** Assume que as variáveis são independentes entre si (daí o nome "Ingênuo" ou *Naive*).
* **Cenário:** É muito rápido e eficiente, embora a suposição de independência nem sempre seja verdadeira em dados complexos.

### 📏 4. K-Nearest Neighbors (KNN)
* **O que é:** Um algoritmo baseado em instância ("preguiçoso").
* **Como funciona:** Ele não "aprende" um modelo fixo. Para classificar um novo aluno, ele olha para os 'K' alunos mais parecidos (vizinhos) no espaço de dados.
* **Lógica:** "Diga-me com quem andas (ou com quem seus dados se parecem) e te direi quem és".

---

## 📊 Principais Resultados e Insights

Após rodar as análises exploratórias e os modelos, chegamos às seguintes conclusões documentadas:

### 🔍 Insights da Análise Exploratória
1.  **O Período Crítico:** A evasão está concentrada massivamente nos **3 primeiros períodos** do curso.
2.  **Desempenho > Social:** Fatores acadêmicos (Notas baixas, alta taxa de reprovação e baixa frequência) são indicadores muito mais fortes de evasão do que fatores socioeconômicos (como renda, escola de origem ou necessidade de trabalhar).
3.  **Origem Escolar:** Não houve diferença significativa na taxa de evasão entre alunos vindos de escolas públicas ou particulares.

### 🏆 Performance dos Modelos
Os modelos foram avaliados com uma divisão de treino/teste de 70/30. O ranking final de Acurácia foi:

| Rank | Modelo | Acurácia | Observação |
| :--- | :--- | :--- | :--- |
| 🥇 | **Random Forest** | **87.08%** | Melhor desempenho geral e robustez. |
| 🥈 | KNN | 86.67% | Boa performance, mas computacionalmente mais pesado. |
| 🥉 | Regressão Logística | 84.79% | Excelente para explicar as causas (coeficientes). |
| 4º | Naive Bayes | 79.79% | Desempenho inferior devido à complexidade dos dados. |

**Variáveis mais Importantes (Random Forest):**
1.  Período do Aluno (Alunos no início desistem mais).
2.  Nota Média.
3.  Coeficiente (CR).
4.  Frequência Média.

---

## 🚀 Como Executar o Projeto

1.  **Pré-requisitos:** Certifique-se de ter o Python instalado e as bibliotecas listadas no arquivo `requirements.txt` (ou instale manualmente):
    ```bash
    pip install pandas numpy seaborn matplotlib scikit-learn openpyxl
    ```

2.  **Estrutura de Arquivos:**
    Certifique-se de que o arquivo de dados está no caminho correto conforme o script:
    ```text
    /
    ├── projetoModificado.py
    ├── PROJETO NOSSO/
    │   ├── DadosAlunos.xlsx
    │   └── graficos/  (Pasta para salvar as imagens geradas)
    ```

3.  **Execução:**
    Rode o script principal:
    ```bash
    python projetoModificado.py
    ```

O script gerará visualizações estatísticas no terminal e salvará os gráficos comparativos na pasta especificada.

---

## 📄 Licença e Créditos

Desenvolvido como parte de um estudo acadêmico sobre retenção de alunos.
* **Base de Dados:** Dados anonimizados de discentes de Computação.
* **Desenvolvimento:** Geraldo Baranoski Jr.

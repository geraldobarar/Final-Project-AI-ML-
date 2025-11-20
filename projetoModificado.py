import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

caminho_arquivo = 'PROJETO NOSSO/DadosAlunos.xlsx'

nomes_planilhas = ["Relacao_Alunos", "Historico", "Questionario_socioEconomico"]

dataframes = {}

for planilha in nomes_planilhas:
    df_temp = pd.read_excel(caminho_arquivo, sheet_name=planilha, header=2)
    dataframes[planilha] = df_temp.iloc[:, 1:]

df_alunos = dataframes['Relacao_Alunos']
df_historico = dataframes['Historico']
df_questionario = dataframes['Questionario_socioEconomico']

print("=== VISUALIZAÇÃO DOS DATAFRAMES CARREGADOS ===")
print("\n📊 DataFrame Relação Alunos:")
print(f"Dimensões: {df_alunos.shape}")
print(df_alunos.head(3))

print("\n📊 DataFrame Histórico:")
print(f"Dimensões: {df_historico.shape}")
print(df_historico.head(3))

print("\n📊 DataFrame Questionário Socioeconômico:")
print(f"Dimensões: {df_questionario.shape}")
print(df_questionario.head(3))

"""## **Tratando Valores NAN nos DFs**

### **Tratando o DF Relação Alunos**

#### **Tratando a Coluna 'Cidade' e 'Estado'**
"""

print("=== TRATAMENTO DE VALORES NULOS ===")

print("\n🔧 Tratando colunas 'Cidade' e 'Estado'...")
df_alunos = df_alunos.dropna(subset=['Cidade', 'Estado'])
print(f"✅ Dimensões após remoção: {df_alunos.shape}")

"""#### **Tratando as Colunas 'Nota Enem' e 'Escore Vest'**"""

print("\n🔧 Unificando colunas de notas...")
df_alunos['Nota Final'] = df_alunos['Nota Enem'].combine_first(df_alunos['Escore Vest'])
df_alunos = df_alunos.drop(columns=['Escore Vest', 'Nota Enem'])
print(f"✅ Coluna 'Nota Final' criada. Dimensões: {df_alunos.shape}")

print(f"\n📌 Valores nulos em 'Nota Final': {df_alunos['Nota Final'].isnull().sum()}")

"""### **Tratando o DF Histórico**

#### Tratando a coluna Nota
"""

print("\n🔧 Tratando coluna 'Nota' no histórico...")
df_historico = df_historico.dropna(subset=['Nota'])
print(f"✅ Dimensões após remoção: {df_historico.shape}")

"""#### Tratando a coluna Freq.(%)"""

print("\n🔧 Tratando coluna 'Freq.(%)' no histórico...")
df_historico_tratado = df_historico.copy()

# Preenchendo com 100% para disciplinas específicas
df_historico_tratado.loc[
    df_historico_tratado['Nome Disciplina'].isin(['TRABALHO DE DIPLOMAÇÃO', 'TRABALHO DE CONCLUSÃO DE CURSO 2'])
    & df_historico_tratado['Freq.(%)'].isnull(), 'Freq.(%)'
] = 100

# Removendo linhas problemáticas
disciplinas_para_remover = ['INFORMÁTICA INSTRUMENTAL', 'REDES DE COMPUTADORES',
                             'METODOLOGIA PARA DESENVOLVIMENTO DE PROJETOS',
                             'TECNOLOGIA ORIENTADA A OBJETOS', 'ANÁLISE DE SISTEMAS']

df_historico_tratado = df_historico_tratado.drop(
    df_historico_tratado[
        (df_historico_tratado['Nome Disciplina'].isin(disciplinas_para_remover)) &
        (df_historico_tratado['Freq.(%)'].isnull())
    ].index
)

df_historico = df_historico_tratado
print(f"✅ Dimensões após tratamento: {df_historico.shape}")

"""## **Análises Exploratórias dos Dados**

#### **Distribuição Geral de Alunos por Sexo**
"""

print("=== ANÁLISES EXPLORATÓRIAS ===")

print("\n👥 Distribuição Geral de Alunos por Sexo")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Gráfico 1: Proporção geral
contagem_sexo = df_alunos['Sexo'].value_counts()
labels = ['Masculino', 'Feminino']
sizes = [contagem_sexo.get('M', 0), contagem_sexo.get('F', 0)]
colors = ['#4682b4', '#ff69b4']

ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax1.set_title('Distribuição Geral por Sexo', fontsize=14, fontweight='bold')

# Gráfico 2: Proporção por status
df_alunos['Status'] = np.where(df_alunos['Situação Atual do Aluno'] == 'Desistente', 'Desistente', 'Permanência')
contagem = df_alunos.groupby(['Sexo', 'Status']).size().unstack(fill_value=0)
proporcao = contagem.div(contagem.sum(axis=1), axis=0) * 100

proporcao.plot(kind='bar', ax=ax2, color=['#d62728', '#1f77b4'], width=0.8)
ax2.set_title('Desistência vs. Permanência por Sexo', fontsize=14, fontweight='bold')
ax2.set_ylabel('Proporção (%)')
ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
ax2.legend(['Desistente', 'Permanência'])
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('PROJETO NOSSO/graficos/distribuicao_sexo.png')
plt.show()

print(f"\n📊 Estatísticas por sexo:")
print(contagem)

"""#### **Distribuição da Situação Atual dos Alunos**"""

print("\n📈 Situação Atual dos Alunos")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Gráfico 1: Todas as situações
contagem_completa = df_alunos['Situação Atual do Aluno'].value_counts()
ax1.bar(contagem_completa.index, contagem_completa.values, color='skyblue', edgecolor='black')
ax1.set_title('Distribuição Completa da Situação dos Alunos', fontsize=14, fontweight='bold')
ax1.set_ylabel('Quantidade de Alunos')
ax1.tick_params(axis='x', rotation=45)

# Adicionar valores nas barras
for i, v in enumerate(contagem_completa.values):
    ax1.text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')

# Gráfico 2: Situações filtradas (excluindo Regular, Trancando, Afastado)
valores_excluir = ["Regular", "Trancando", "Afastado"]
df_filtrado = df_alunos[~df_alunos['Situação Atual do Aluno'].isin(valores_excluir)]
contagem_filtrada = df_filtrado['Situação Atual do Aluno'].value_counts()

ax2.bar(contagem_filtrada.index, contagem_filtrada.values, color='lightcoral', edgecolor='black')
ax2.set_title('Situações Relevantes (excluindo Regular/Trancando/Afastado)', fontsize=14, fontweight='bold')
ax2.set_ylabel('Quantidade de Alunos')
ax2.tick_params(axis='x', rotation=45)

# Adicionar valores nas barras
for i, v in enumerate(contagem_filtrada.values):
    ax2.text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('PROJETO NOSSO/graficos/distribuicao_situacao_alunos.png')
plt.show()

print(f"\n📊 Resumo das situações:")
for situacao, quantidade in contagem_completa.items():
    percentual = (quantidade / len(df_alunos)) * 100
    print(f"  {situacao}: {quantidade} alunos ({percentual:.1f}%)")

"""#### **Distribuição de Alunos Desistentes por Período**"""

print("\n📅 Distribuição de Desistentes por Período")

df_desistentes = df_alunos[df_alunos['Situação Atual do Aluno'] == 'Desistente']
contagem_periodo = df_desistentes['Período do Aluno'].value_counts().sort_index()

plt.figure(figsize=(12, 6))
bars = plt.bar(contagem_periodo.index.astype(str), contagem_periodo.values, 
               color='lightcoral', edgecolor='darkred', alpha=0.8)

plt.title('Distribuição de Alunos Desistentes por Período', fontsize=14, fontweight='bold')
plt.xlabel('Período do Aluno')
plt.ylabel('Quantidade de Desistentes')
plt.grid(axis='y', alpha=0.3)

# Adicionar valores nas barras
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5, str(int(height)), 
             ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('PROJETO NOSSO/graficos/distribuicao_desistentes_periodo.png')
plt.show()

print(f"\n📊 Total de desistentes: {len(df_desistentes)}")
print("Distribuição por período:")
for periodo, quantidade in contagem_periodo.items():
    percentual = (quantidade / len(df_desistentes)) * 100
    print(f"  Período {periodo}: {quantidade} desistentes ({percentual:.1f}%)")

"""#### **Distribuição de Alunos por Tipo de Escola**"""

print("\n🏫 Distribuição por Tipo de Escola")

df_filtrado = df_alunos[df_alunos['Escola Pública?'].isin(['Escola Pública', 'Escola Particular'])]
df_desistentes = df_filtrado[df_filtrado['Situação Atual do Aluno'] == 'Desistente']

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Gráfico 1: Total de alunos
contagem_total = df_filtrado['Escola Pública?'].value_counts()
axes[0].bar(contagem_total.index, contagem_total.values, color=['#ff9999', '#66b3ff'], edgecolor='black')
axes[0].set_title('Total de Alunos por Tipo de Escola', fontweight='bold')
axes[0].set_ylabel('Quantidade')

# Gráfico 2: Desistentes
contagem_desistentes = df_desistentes['Escola Pública?'].value_counts()
axes[1].bar(contagem_desistentes.index, contagem_desistentes.values, color=['#ff6666', '#3388ff'], edgecolor='black')
axes[1].set_title('Alunos Desistentes por Tipo de Escola', fontweight='bold')
axes[1].set_ylabel('Quantidade')

# Adicionar valores e porcentagens
for ax, contagem, total in zip(axes, [contagem_total, contagem_desistentes], 
                              [len(df_filtrado), len(df_desistentes)]):
    for i, v in enumerate(contagem.values):
        percentual = (v / total) * 100
        ax.text(i, v + 0.5, f'{v}\n({percentual:.1f}%)', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('PROJETO NOSSO/graficos/distribuicao_tipo_escola.png')
plt.show()

print(f"\n📊 Estatísticas por tipo de escola:")
print(f"Total de alunos: {len(df_filtrado)}")
print(f"Total de desistentes: {len(df_desistentes)}")

"""#### **Média das Disciplinas do Primeiro Período**"""

print("\n📚 Médias das Disciplinas do Primeiro Período")

# Mapeamento das matérias
mapa_de_materias = {
    "ALGORITMOS": ['ALGORITMOS', 'ALGORITMOS E ESTRUTURA DE DADOS 1'],
    "ARQUITETURA DE COMPUTADORES": ['ARQUITETURA DE COMPUTADORES', 'ARQUITETURA E ORGANIZAÇÃO DE COMPUTADORES', 'ORGANIZAÇÃO DE COMPUTADORES'],
    "BANCO DE DADOS 1": ['BANCO DE DADOS 1'],
    "CIRCUITOS DIGITAIS": ['CIRCUITOS DIGITAIS'],
    "COMUNICAÇÃO LINGUÍSTICA": ['COMUNICAÇÃO LINGUISTICA', 'COMUNICAÇÃO LINGUÍSTICA', 'Comunicação Oral e Escrita'],
    "CÁLCULO DIFERENCIAL E INTEGRAL 1": ['Cálculo Diferencial', 'CÁLCULO DIFERENCIAL E INTEGRAL 1', 'CÁLCULO INTEGRAL'],
    "EMPREENDEDORISMO": ['EMPREENDEDORISMO'],
    "ENGENHARIA DE SOFTWARE": ['ENGENHARIA DE SOFTWARE', 'ENGENHARIA DE SOFTWARE 1'],
    "FUNDAMENTOS DA ADMINISTRAÇÃO": ['FUNDAMENTOS DA ADMINISTRAÇÃO'],
    "FUNDAMENTOS DA COMPUTAÇÃO": ['FUNDAMENTOS DA COMPUTAÇÃO'],
    "ÉTICA": ['FUNDAMENTOS DA ÉTICA', 'ÉTICA PROFISSÃO E CIDADANIA', 'ÉTICA, PROFISSÃO E CIDADANIA'],
    "FUNDAMENTOS DE BANCOS DE DADOS": ['FUNDAMENTOS DE BANCOS DE DADOS'],
    "GEOMETRIA ANALÍTICA E ÁLGEBRA LINEAR": ['GEOMETRIA ANALÍTICA E ÁLGEBRA LINEAR'],
    "INTERAÇÃO HUMANO-COMPUTADOR": ['IHC INTERFACE HUMANO COMPUTADOR', 'INTERAÇÃO HUMANO-COMPUTADOR'],
    "INFORMÁTICA INSTRUMENTAL": ['INFORMÁTICA INSTRUMENTAL'],
    "INGLÊS INSTRUMENTAL": ['INGLÊS INSTRUMENTAL'],
    "INTRODUÇÃO À CIÊNCIA DA COMPUTAÇÃO": ['INTRODUÇÃO À CIÊNCIA DA COMPUTAÇÃO'],
    "LIBRAS": ['LIBRAS', 'Libras 1'],
    "LINGUAGEM DE PROGRAMAÇÃO": ['LINGUAGEM DE PROGRAMAÇÃO'],
    "LINGUAGEM DE PROGRAMAÇÃO ESTRUTURADA": ['LINGUAGEM DE PROGRAMAÇÃO ESTRUTURADA'],
    "LÓGICA PARA COMPUTAÇÃO": ['LÓGICA PARA COMPUTAÇÃO'],
    "MANUTENÇÃO DE COMPUTADORES": ['MANUTENÇÃO DE COMPUTADORES'],
    "MATEMÁTICA DISCRETA": ['MATEMÁTICA DISCRETA'],
    "PROBABILIDADE E ESTATÍSTICA": ['PROBABILIDADE E ESTATÍSTICA'],
    "REDAÇÃO DE TEXTOS TÉCNICOS/CIENTIFICOS": ['REDAÇÃO DE TEXTOS TÉCNICOS/CIENTIFICOS'],
    "ÁLGEBRA": ['ÁLGEBRA']
}

# Processamento dos dados
df_primeiro_periodo = df_historico[df_historico['Per. Aluno'] == 1]
situacoes_remover = ['Aprovado em Exame de Suficiência', 'Crédito Consignado', 'Reprovado em Exame de Suficiência']
df_primeiro_periodo = df_primeiro_periodo[~df_primeiro_periodo['Situação Disc.'].isin(situacoes_remover)]
df_primeiro_periodo = df_primeiro_periodo.dropna(subset=['Média da Turma'])
df_primeiro_periodo = df_primeiro_periodo[df_primeiro_periodo['Cod. Disciplina'].str.startswith(('S', 'A', 'C'))]

nomes_validos = [nome for sublista in mapa_de_materias.values() for nome in sublista]
df_primeiro_periodo = df_primeiro_periodo[df_primeiro_periodo['Nome Disciplina'].isin(nomes_validos)]

def mapear_nome(disciplina):
    for nome_padrao, sinonimos in mapa_de_materias.items():
        if disciplina in sinonimos:
            return nome_padrao
    return None

df_primeiro_periodo['Nome Padronizado'] = df_primeiro_periodo['Nome Disciplina'].apply(mapear_nome)
colunas_turma = ['Cod. Disciplina', 'Nome Padronizado', 'Ano Lanç.', 'Per. Lanç.']
df_turmas_unicas = df_primeiro_periodo.drop_duplicates(subset=colunas_turma)
df_media_turma = df_turmas_unicas.groupby('Nome Padronizado')['Média da Turma'].mean().reset_index()
df_media_turma = df_media_turma.sort_values(by='Média da Turma', ascending=False)

# Plotagem
plt.figure(figsize=(12, 8))
bars = plt.barh(df_media_turma['Nome Padronizado'], df_media_turma['Média da Turma'], 
                color='lightgreen', edgecolor='darkgreen')

plt.axvline(x=6, color='red', linestyle='--', linewidth=2, label='Nota Mínima (6.0)')
plt.xlabel('Média da Turma')
plt.title('Médias das Disciplinas no Primeiro Período', fontsize=14, fontweight='bold')
plt.grid(axis='x', alpha=0.3)

# Adicionar valores nas barras
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}', 
             ha='left', va='center', fontweight='bold')

plt.legend()
plt.tight_layout()
plt.savefig('PROJETO NOSSO/graficos/media_disciplinas_primeiro_periodo.png')
plt.show()

print(f"\n📊 Disciplinas com maiores médias:")
for i, row in df_media_turma.head().iterrows():
    print(f"  {row['Nome Padronizado']}: {row['Média da Turma']:.1f}")

"""#### **Correlação Entre Frequência e Desistência**"""

print("\n📊 Correlação: Frequência vs Desistência")

# Preparação dos dados
df_alunos_status = df_alunos.copy()
df_alunos_status['Status Simplificado'] = df_alunos_status['Situação Atual do Aluno'].apply(
    lambda x: 'Desistente' if x == 'Desistente' else ('Não Desistente' if x in ['Regular', 'Formado'] else 'Outros')
)
df_alunos_status = df_alunos_status[df_alunos_status['Status Simplificado'].isin(['Desistente', 'Não Desistente'])]

df_historico_filtrado = df_historico[df_historico['id'].isin(df_alunos_status['id'])]
df_frequencia = df_historico_filtrado.groupby('id')['Freq.(%)'].mean().reset_index()
df_frequencia.rename(columns={'Freq.(%)': 'Frequencia Media'}, inplace=True)
df_analise_freq = df_alunos_status.merge(df_frequencia, on='id', how='left')

# Plotagem
plt.figure(figsize=(10, 6))
box_plot = sns.boxplot(data=df_analise_freq, x='Status Simplificado', y='Frequencia Media', palette='Set2')
plt.title('Frequência Média: Desistentes vs Não Desistentes', fontsize=14, fontweight='bold')
plt.xlabel('Status do Aluno')
plt.ylabel('Frequência Média (%)')
plt.grid(axis='y', alpha=0.3)

# Adicionar estatísticas no gráfico
stats = df_analise_freq.groupby('Status Simplificado')['Frequencia Media'].describe()
for i, status in enumerate(['Desistente', 'Não Desistente']):
    media = stats.loc[status, 'mean']
    plt.text(i, media + 2, f'Média: {media:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('PROJETO NOSSO/graficos/correlacao_frequencia_desistencia.png')
plt.show()

print(f"\n📈 Estatísticas de Frequência:")
print(stats[['mean', 'std', 'min', 'max']])

"""#### **Correlação Entre Média nas Disciplinas e Desistência**"""

print("\n📊 Correlação: Nota Média vs Desistência")

# Cálculo das notas médias
df_nota_media = df_historico_filtrado.groupby('id')['Nota'].mean().reset_index()
df_nota_media.rename(columns={'Nota': 'Nota Media'}, inplace=True)
df_analise_nota = df_alunos_status.merge(df_nota_media, on='id', how='left')

# Plotagem
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_analise_nota, x='Status Simplificado', y='Nota Media', palette='Set3')
plt.title('Nota Média: Desistentes vs Não Desistentes', fontsize=14, fontweight='bold')
plt.xlabel('Status do Aluno')
plt.ylabel('Nota Média')
plt.grid(axis='y', alpha=0.3)

# Adicionar estatísticas
stats_nota = df_analise_nota.groupby('Status Simplificado')['Nota Media'].describe()
for i, status in enumerate(['Desistente', 'Não Desistente']):
    media = stats_nota.loc[status, 'mean']
    plt.text(i, media + 0.3, f'Média: {media:.1f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('PROJETO NOSSO/graficos/correlacao_media_desistencia.png')
plt.show()

print(f"\n📈 Estatísticas de Notas:")
print(stats_nota[['mean', 'std', 'min', 'max']])

"""#### **Correlação Entre Porcentagem de Reprovação e Desistência**"""

print("\n📊 Correlação: Porcentagem de Reprovação vs Desistência")

# Cálculo da porcentagem de reprovação
df_total_disciplinas = df_historico_filtrado.groupby('id').size().reset_index(name='Total_Disciplinas')
df_reprovacoes = df_historico_filtrado[df_historico_filtrado['Situação Disc.'].str.contains('Reprovado')]
df_qtd_reprovacoes = df_reprovacoes.groupby('id').size().reset_index(name='Qtd_Reprovacoes')
df_reprov_percent = df_total_disciplinas.merge(df_qtd_reprovacoes, on='id', how='left')
df_reprov_percent['Qtd_Reprovacoes'] = df_reprov_percent['Qtd_Reprovacoes'].fillna(0)
df_reprov_percent['Porcentagem_Reprovacao'] = (df_reprov_percent['Qtd_Reprovacoes'] / df_reprov_percent['Total_Disciplinas']) * 100
df_analise_reprov_percent = df_alunos_status.merge(df_reprov_percent[['id', 'Porcentagem_Reprovacao']], on='id', how='left')

# Plotagem
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_analise_reprov_percent, x='Status Simplificado', y='Porcentagem_Reprovacao', palette='pastel')
plt.title('Porcentagem de Reprovação: Desistentes vs Não Desistentes', fontsize=14, fontweight='bold')
plt.xlabel('Status do Aluno')
plt.ylabel('Porcentagem de Reprovação (%)')
plt.grid(axis='y', alpha=0.3)

# Adicionar estatísticas
stats_reprov = df_analise_reprov_percent.groupby('Status Simplificado')['Porcentagem_Reprovacao'].describe()
for i, status in enumerate(['Desistente', 'Não Desistente']):
    media = stats_reprov.loc[status, 'mean']
    plt.text(i, media + 2, f'Média: {media:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('PROJETO NOSSO/graficos/correlacao_reprovacao_desistencia.png')
plt.show()

print(f"\n📈 Estatísticas de Reprovação:")
print(stats_reprov[['mean', 'std', 'min', 'max']])

"""#### **Correlação Entre Cidade de Origem e Desistência**"""

print("\n🏙️ Correlação: Cidade de Origem vs Desistência")

df_alunos_status['Mora em PG'] = df_alunos_status['Cidade'].apply(
    lambda x: 'Sim' if x.strip().lower() == 'ponta grossa' else 'Não'
)
df_desistentes = df_alunos_status[df_alunos_status['Status Simplificado'] == 'Desistente']

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Gráfico 1: Total de alunos
contagem_total_cidade = df_alunos_status['Mora em PG'].value_counts()
axes[0].bar(contagem_total_cidade.index, contagem_total_cidade.values, color=['lightblue', 'lightcoral'])
axes[0].set_title('Total de Alunos por Cidade de Origem', fontweight='bold')
axes[0].set_ylabel('Quantidade')

# Gráfico 2: Desistentes
contagem_desistentes_cidade = df_desistentes['Mora em PG'].value_counts()
axes[1].bar(contagem_desistentes_cidade.index, contagem_desistentes_cidade.values, color=['lightblue', 'lightcoral'])
axes[1].set_title('Alunos Desistentes por Cidade de Origem', fontweight='bold')
axes[1].set_ylabel('Quantidade')

# Adicionar valores e porcentagens
for ax, contagem, total in zip(axes, [contagem_total_cidade, contagem_desistentes_cidade], 
                              [len(df_alunos_status), len(df_desistentes)]):
    for i, v in enumerate(contagem.values):
        percentual = (v / total) * 100
        ax.text(i, v + 0.5, f'{v}\n({percentual:.1f}%)', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('PROJETO NOSSO/graficos/correlacao_cidade_origem_desistencia.png')
plt.show()

print(f"\n📊 Estatísticas por cidade:")
print(f"Total de alunos: {len(df_alunos_status)}")
print(f"Total de desistentes: {len(df_desistentes)}")

"""#### **Correlação Entre Trabalho e Desistência**"""

print("\n💼 Correlação: Necessidade de Trabalhar vs Desistência")

# Processamento dos dados
df_q15 = df_questionario[df_questionario['Cod. Questão'] == 15]
df_temp = df_q15[['id', 'Resposta']].copy()
status_dict = df_alunos_status.set_index('id')['Status Simplificado'].to_dict()
df_temp['Status Simplificado'] = df_temp['id'].map(status_dict)

# Simplificar categorias
df_temp['Resposta'] = df_temp['Resposta'].replace({
    "Sim, apenas nos últimos anos.": "Sim",
    "Sim, desde o início, em período integral.": "Sim",
    "Sim, desde o início, em período parcial.": "Sim"
})

tabela = pd.crosstab(df_temp['Resposta'], df_temp['Status Simplificado'])

# Plotagem
plt.figure(figsize=(12, 6))
colors = ['#1f77b4', '#ff7f0e']
ax = tabela.plot(kind='bar', stacked=True, color=colors)
plt.title('Necessidade de Trabalhar vs Desistência', fontsize=14, fontweight='bold')
plt.ylabel('Número de Alunos')
plt.xlabel('Resposta sobre Trabalho')
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)

# Adicionar porcentagens
for idx, resposta in enumerate(tabela.index):
    total = tabela.loc[resposta].sum()
    y_offset = 0
    for status in tabela.columns:
        valor = tabela.loc[resposta, status]
        if valor > 0:
            percent = (valor / total) * 100
            plt.text(idx, y_offset + valor/2, f"{percent:.1f}%", 
                    ha='center', va='center', color='white', fontweight='bold')
            y_offset += valor

plt.legend(title='Status')
plt.tight_layout()
plt.savefig('PROJETO NOSSO/graficos/correlacao_trabalho_desistencia.png')
plt.show()

print(f"\n📊 Distribuição por necessidade de trabalho:")
print(tabela)

"""#### **Escolaridade dos Pais**"""

print("\n🎓 Escolaridade dos Pais vs Desistência")

# Processamento dos dados
pergunta_pai = 'Qual o grau máximo de escolaridade do seu pai?'
df_pai = df_questionario[df_questionario['Pergunta'] == pergunta_pai].copy()
df_pai = df_pai[['id', 'Resposta']]
df_pai.rename(columns={'Resposta': 'escolaridade_pai'}, inplace=True)

pergunta_mae = 'Qual o grau máximo de escolaridade da sua mãe?'
df_mae = df_questionario[df_questionario['Pergunta'] == pergunta_mae].copy()
df_mae = df_mae[['id', 'Resposta']]
df_mae.rename(columns={'Resposta': 'escolaridade_mae'}, inplace=True)

df_temp = pd.merge(df_alunos, df_pai, on='id', how='left')
df_final_escolaridade = pd.merge(df_temp, df_mae, on='id', how='left')
df_desistentes = df_final_escolaridade[df_final_escolaridade['Situação Atual do Aluno'].str.strip() == 'Desistente'].copy()

# Preparar dados para plotagem
prop_pai_total = df_final_escolaridade['escolaridade_pai'].value_counts(normalize=True).mul(100).rename('Porcentagem').reset_index()
prop_pai_total['Grupo'] = 'Alunos não Desistentes'
prop_pai_desistentes = df_desistentes['escolaridade_pai'].value_counts(normalize=True).mul(100).rename('Porcentagem').reset_index()
prop_pai_desistentes['Grupo'] = 'Alunos Desistentes'
prop_mae_total = df_final_escolaridade['escolaridade_mae'].value_counts(normalize=True).mul(100).rename('Porcentagem').reset_index()
prop_mae_total['Grupo'] = 'Alunos não Desistentes'
prop_mae_desistentes = df_desistentes['escolaridade_mae'].value_counts(normalize=True).mul(100).rename('Porcentagem').reset_index()
prop_mae_desistentes['Grupo'] = 'Alunos Desistentes'

df_plot_pai = pd.concat([prop_pai_total, prop_pai_desistentes])
df_plot_mae = pd.concat([prop_mae_total, prop_mae_desistentes])

# Plotagem
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
sns.set_theme(style="whitegrid")

fig.suptitle('Escolaridade dos Pais: Alunos não Desistentes vs Desistentes', fontsize=16, fontweight='bold')

sns.barplot(ax=axes[0], data=df_plot_pai, y='escolaridade_pai', x='Porcentagem', hue='Grupo', palette='viridis')
axes[0].set_title('Escolaridade do Pai', fontweight='bold')
axes[0].set_xlabel('Porcentagem de Alunos (%)')
axes[0].xaxis.set_major_formatter(mtick.PercentFormatter())

sns.barplot(ax=axes[1], data=df_plot_mae, y='escolaridade_mae', x='Porcentagem', hue='Grupo', palette='viridis')
axes[1].set_title('Escolaridade da Mãe', fontweight='bold')
axes[1].set_xlabel('Porcentagem de Alunos (%)')
axes[1].xaxis.set_major_formatter(mtick.PercentFormatter())

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('PROJETO NOSSO/graficos/escolaridade_pais.png')
plt.show()

"""## **Preparação para Machine Learning**

### **Criação do DataFrame para Modelagem**
"""

print("=== PREPARAÇÃO PARA MACHINE LEARNING ===")

print("\n🔧 Criando DataFrame para modelagem...")

# DataFrame base
df_1 = df_alunos.copy()

# Unir métricas calculadas
df_metricas = df_reprov_percent[['id', 'Porcentagem_Reprovacao']] \
    .merge(df_nota_media[['id', 'Nota Media']], on='id', how='outer') \
    .merge(df_frequencia[['id', 'Frequencia Media']], on='id', how='outer')

df_1 = df_1.merge(df_metricas, on='id', how='left')

# Adicionar variável de trabalho
df_precisa_trabalhar = df_questionario[['id', 'Resposta']].copy()
df_precisa_trabalhar['Precisa Trabalhar'] = df_precisa_trabalhar['Resposta'].apply(
    lambda x: True if x == 'Sim' else False
)
df_precisa_trabalhar = df_precisa_trabalhar.drop_duplicates(subset='id')[['id', 'Precisa Trabalhar']]
df_1 = df_1.merge(df_precisa_trabalhar, on='id', how='left')
df_1['Precisa Trabalhar'] = df_1['Precisa Trabalhar'].astype('bool')

# Remover colunas não utilizadas
df_1 = df_1.drop(columns=["id", "Status", "Ano Ingresso", "Per. Ingresso", "Forma de Ingresso", 
                         "Tipo de Cota", "Grupo (Étnico)", "Estado", "Data Nascimento", 
                         "Sigla Cota", "Ano Desistência", "Período Desistências"])

# Transformar colunas
df_1['Mora em PG'] = df_1['Cidade'].str.lower() == 'ponta grossa'
df_1 = df_1.drop(columns=['Cidade'])

df_1['Escola Pública?'] = df_1['Escola Pública?'].apply(
    lambda x: True if x.lower() == 'escola pública' else False
)

# Definir variável target
df_1 = df_1[~df_1['Situação Atual do Aluno'].isin(['Jubilado', 'Expulso'])]
desistentes = ['Desistente', 'Transferido', 'Mudou de Curso']
nao_desistentes = ['Regular', 'Formado', 'Trancado', 'Afastado']
df_1['Desistente'] = df_1['Situação Atual do Aluno'].apply(
    lambda x: True if x in desistentes else False
)
df_1 = df_1.drop(columns=['Situação Atual do Aluno'])

# One-hot encoding
df_1 = pd.get_dummies(df_1, columns=['Sexo', 'Curso'], drop_first=False)
df_1 = df_1.rename(columns={
    'Curso_Ciência Da Computação': 'Curso_BCC',
    'Curso_Curso Superior De Tecnologia Em Análise E Desenvolvimento De Sistemas': 'Curso_ADS'
})

# Converter bool para int
for col in df_1.columns:
    if df_1[col].dtype == 'bool':
        df_1[col] = df_1[col].astype(int)

# Remover valores nulos
df_1 = df_1.dropna()

print(f"✅ DataFrame final preparado:")
print(f"   Dimensões: {df_1.shape}")
print(f"   Colunas: {list(df_1.columns)}")
print(f"\n📊 Distribuição da variável target:")
print(df_1['Desistente'].value_counts())
print(f"\n📈 Proporção:")
print(df_1['Desistente'].value_counts(normalize=True))

"""## **Modelos de Machine Learning**

### **Random Forest**
"""

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns

print("=== MODELOS DE MACHINE LEARNING ===")

print("\n🌲 1. ALGORITMO RANDOM FOREST")

# Preparar dados
X = df_1.drop(columns=['Desistente'])
y = df_1['Desistente']

# Dividir treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=11, stratify=y
)

# Treinar modelo
rf = RandomForestClassifier(n_estimators=100, random_state=9)
rf.fit(X_train, y_train)

# Previsões
y_pred_rf = rf.predict(X_test)

# Avaliação
acc_rf = accuracy_score(y_test, y_pred_rf)

print(f"✅ Acurácia: {acc_rf:.4f}")
print(f"✅ Previsões - Desistentes: {sum(y_pred_rf)}, Não Desistentes: {len(y_pred_rf) - sum(y_pred_rf)}")

# Matriz de confusão
cm_rf = confusion_matrix(y_test, y_pred_rf)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Não Desistente', 'Desistente'],
            yticklabels=['Não Desistente', 'Desistente'])
plt.title('Matriz de Confusão - Random Forest', fontweight='bold')
plt.ylabel('Valor Real')
plt.xlabel('Previsão')
plt.savefig('PROJETO NOSSO/graficos/cm_random_forest.png')
plt.show()

print('\n📊 Relatório de Classificação:')
print(classification_report(y_test, y_pred_rf, target_names=['Não Desistente', 'Desistente']))

# Importância das variáveis
importances = rf.feature_importances_
features = X.columns
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
plt.bar(range(len(importances)), importances[indices], color='lightgreen', edgecolor='darkgreen')
plt.title("Importância das Variáveis - Random Forest", fontweight='bold')
plt.xticks(range(len(importances)), [features[i] for i in indices], rotation=90)
plt.ylabel('Importância')
plt.tight_layout()
plt.savefig('PROJETO NOSSO/graficos/feature_importance_random_forest.png')
plt.show()

print("\n🔝 Top 5 variáveis mais importantes:")
for i in range(5):
    print(f"  {i+1}. {features[indices[i]]}: {importances[indices[i]]:.4f}")

"""### **Regressão Logística**"""

print("\n📈 2. ALGORITMO REGRESSÃO LOGÍSTICA")

# Usar os mesmos dados
X_log = df_1.drop(columns=['Desistente'])
y_log = df_1['Desistente']

# Dividir treino/teste
X_train_log, X_test_log, y_train_log, y_test_log = train_test_split(
    X_log, y_log, test_size=0.30, random_state=42, stratify=y_log
)

# Padronização
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_log)
X_test_scaled = scaler.transform(X_test_log)

# Treinar modelo
log_reg = LogisticRegression(random_state=42, max_iter=1000)
log_reg.fit(X_train_scaled, y_train_log)

# Previsões
y_pred_log = log_reg.predict(X_test_scaled)

# Avaliação
acc_log = accuracy_score(y_test_log, y_pred_log)

print(f"✅ Acurácia: {acc_log:.4f}")
print(f"✅ Previsões - Desistentes: {sum(y_pred_log)}, Não Desistentes: {len(y_pred_log) - sum(y_pred_log)}")

# Matriz de confusão
cm_log = confusion_matrix(y_test_log, y_pred_log)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_log, annot=True, fmt='d', cmap='Oranges',
            xticklabels=['Não Desistente', 'Desistente'],
            yticklabels=['Não Desistente', 'Desistente'])
plt.title('Matriz de Confusão - Regressão Logística', fontweight='bold')
plt.ylabel('Valor Real')
plt.xlabel('Previsão')
plt.savefig('PROJETO NOSSO/graficos/cm_regressao_logistica.png')
plt.show()

print('\n📊 Relatório de Classificação:')
print(classification_report(y_test_log, y_pred_log, target_names=['Não Desistente', 'Desistente']))

# Coeficientes
importances_log = log_reg.coef_[0]
features_log = X_log.columns
coef_df = pd.DataFrame({'Variavel': features_log, 'Coeficiente': importances_log})
coef_df['Importancia_Absoluta'] = np.abs(coef_df['Coeficiente'])
coef_df = coef_df.sort_values(by='Importancia_Absoluta', ascending=False)

plt.figure(figsize=(10, 8))
sns.barplot(data=coef_df.head(10), x='Coeficiente', y='Variavel', palette='coolwarm')
plt.title("Top 10 Variáveis - Regressão Logística", fontweight='bold')
plt.xlabel("Coeficiente (Impacto na Desistência)")
plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
plt.tight_layout()
plt.savefig('PROJETO NOSSO/graficos/feature_importance_regressao_logistica.png')
plt.show()

print("\n🔝 Top 5 variáveis mais importantes:")
for i, row in coef_df.head(5).iterrows():
    print(f"  {row['Variavel']}: {row['Coeficiente']:.4f}")

"""### **Naive Bayes**"""

print("\n📊 3. ALGORITMO NAIVE BAYES")

# Usar os mesmos dados
X_train_nb, X_test_nb, y_train_nb, y_test_nb = train_test_split(
    X_log, y_log, test_size=0.30, random_state=42, stratify=y_log
)

# Treinar modelo
nb_model = GaussianNB()
nb_model.fit(X_train_nb, y_train_nb)

# Previsões
y_pred_nb = nb_model.predict(X_test_nb)

# Avaliação
acc_nb = accuracy_score(y_test_nb, y_pred_nb)

print(f"✅ Acurácia: {acc_nb:.4f}")
print(f"✅ Previsões - Desistentes: {sum(y_pred_nb)}, Não Desistentes: {len(y_pred_nb) - sum(y_pred_nb)}")

# Matriz de confusão
cm_nb = confusion_matrix(y_test_nb, y_pred_nb)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_nb, annot=True, fmt='d', cmap='Greens',
            xticklabels=['Não Desistente', 'Desistente'],
            yticklabels=['Não Desistente', 'Desistente'])
plt.title('Matriz de Confusão - Naive Bayes', fontweight='bold')
plt.ylabel('Valor Real')
plt.xlabel('Previsão')
plt.savefig('PROJETO NOSSO/graficos/cm_naive_bayes.png')
plt.show()

print('\n📊 Relatório de Classificação:')
print(classification_report(y_test_nb, y_pred_nb, target_names=['Não Desistente', 'Desistente']))

"""### **K-Nearest Neighbors (KNN)**"""

print("\n📏 4. ALGORITMO K-NEAREST NEIGHBORS (KNN)")

# Dividir dados
X_train_knn, X_test_knn, y_train_knn, y_test_knn = train_test_split(
    X_log, y_log, test_size=0.30, random_state=50, stratify=y_log
)

# Escalonamento
scaler_knn = StandardScaler()
X_train_scaled_knn = scaler_knn.fit_transform(X_train_knn)
X_test_scaled_knn = scaler_knn.transform(X_test_knn)

# Treinar modelo
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train_scaled_knn, y_train_knn)

# Previsões
y_pred_knn = knn_model.predict(X_test_scaled_knn)

# Avaliação
acc_knn = accuracy_score(y_test_knn, y_pred_knn)

print(f"✅ Acurácia: {acc_knn:.4f}")
print(f"✅ Previsões - Desistentes: {sum(y_pred_knn)}, Não Desistentes: {len(y_pred_knn) - sum(y_pred_knn)}")

# Matriz de confusão
cm_knn = confusion_matrix(y_test_knn, y_pred_knn)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_knn, annot=True, fmt='d', cmap='Purples',
            xticklabels=['Não Desistente', 'Desistente'],
            yticklabels=['Não Desistente', 'Desistente'])
plt.title('Matriz de Confusão - KNN', fontweight='bold')
plt.ylabel('Valor Real')
plt.xlabel('Previsão')
plt.savefig('PROJETO NOSSO/graficos/cm_knn.png')
plt.show()

print('\n📊 Relatório de Classificação:')
print(classification_report(y_test_knn, y_pred_knn, target_names=['Não Desistente', 'Desistente']))

"""### **Comparação Final dos Modelos**"""

print("\n🏆 COMPARAÇÃO FINAL DOS MODELOS")

resultados = {
    'Modelo': ['Random Forest', 'Regressão Logística', 'Naive Bayes', 'KNN'],
    'Acurácia': [acc_rf, acc_log, acc_nb, acc_knn]
}

df_resultados = pd.DataFrame(resultados)
df_resultados = df_resultados.sort_values('Acurácia', ascending=False)

plt.figure(figsize=(10, 6))
bars = plt.bar(df_resultados['Modelo'], df_resultados['Acurácia'], 
               color=['lightblue', 'lightgreen', 'lightcoral', 'lightyellow'],
               edgecolor=['blue', 'green', 'red', 'orange'], linewidth=2)

plt.title('Comparação de Acurácia dos Modelos', fontsize=14, fontweight='bold')
plt.ylabel('Acurácia')
plt.ylim(0, 1)
plt.grid(axis='y', alpha=0.3)

# Adicionar valores nas barras
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.01, f'{height:.4f}', 
             ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('PROJETO NOSSO/graficos/comparacao_modelos.png')
plt.show()

print("\n📈 RESUMO DOS RESULTADOS:")
print(df_resultados.to_string(index=False))

print(f"\n🎯 Melhor modelo: {df_resultados.iloc[0]['Modelo']} com acurácia de {df_resultados.iloc[0]['Acurácia']:.4f}")

print("\n✅ ANÁLISE CONCLUÍDA!")
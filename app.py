import streamlit as st
import json
import pandas as pd

# 1. Configuração inicial da página (deixa o layout mais largo, ótimo para telas maiores)
st.set_page_config(layout="wide")

st.title("Sustentabilidade Econômica 🌍")
st.write("Distribuição inteligente de orçamento baseada na regra de fatias fixas.")
st.markdown("---")

# 2. Criando a "Memória" do site para guardar as caixinhas
if 'caixinhas' not in st.session_state:
    st.session_state['caixinhas'] = []

# 3. Layout em duas colunas para organizar a tela
col_esquerda, col_direita = st.columns(2)

with col_esquerda:
    st.header("1. Renda e Entradas")
    st.info("Insira o valor total que será distribuído este mês.")
    # Campo para digitar dinheiro
    renda = st.number_input("Valor disponível (R$):", min_value=0.0, step=100.0, format="%.2f")

with col_direita:
    st.header("2. Cadastro de Caixinhas")
    st.info("Cadastre suas metas, contas ou fundos de reserva.")
    
    # Campos de texto e seleção
    nova_caixinha = st.text_input("Nome da Caixinha:")
    prioridade = st.selectbox("Nível de Prioridade:", ["Alta (Essencial)", "Média (Metas)", "Baixa (Desejos)"])
    
    # Botão de ação
    if st.button("Adicionar Caixinha"):
        # Validação: só adiciona se o usuário digitou algum nome
        if nova_caixinha != "":
            st.session_state['caixinhas'].append({"nome": nova_caixinha, "prioridade": prioridade})
            st.success(f"A caixinha '{nova_caixinha}' foi adicionada com sucesso!")
        else:
            st.error("Por favor, digite um nome para a caixinha.")

# 4. Área de exibição dos dados salvos na memória
st.markdown("---")
st.header("📋 Suas Caixinhas Atuais")

if len(st.session_state['caixinhas']) == 0:
    st.warning("Nenhuma caixinha cadastrada ainda.")
else:
    # Usamos o 'enumerate' para saber exatamente qual caixinha estamos excluindo
    for i, item in enumerate(st.session_state['caixinhas']):
        # Divide a linha em duas colunas: uma grande para o texto, uma pequena para o botão
        col_texto, col_botao = st.columns([4, 1])
        
        with col_texto:
            st.write(f"- **{item['nome']}** | Prioridade: {item['prioridade']}")
            
        with col_botao:
            # O botão de excluir precisa de uma 'key' única para não dar erro
            if st.button("❌ Excluir", key=f"del_{i}"):
                st.session_state['caixinhas'].pop(i) # Remove a caixinha da lista
                st.rerun() # Recarrega a página instantaneamente para sumir com o item da tela

# 5. O Motor Matemático (Cálculo da Distribuição)
st.markdown("---")
st.header("⚙️ 3. Motor de Distribuição do Orçamento")

# Botão principal que aciona o cálculo
if st.button("Calcular Distribuição", type="primary"):
    
    # Validações de segurança (evita que o programa quebre)
    if renda <= 0:
        st.error("A renda precisa ser maior que zero para fazer o cálculo.")
    elif len(st.session_state['caixinhas']) == 0:
        st.error("Cadastre pelo menos uma caixinha antes de calcular.")
    else:
        # 1. Aplicando a Regra de Fatias Fixas (50/30/20)
        fatia_alta = renda * 0.50
        fatia_media = renda * 0.30
        fatia_baixa = renda * 0.20
        
        # 2. O Algoritmo separa as caixinhas nas suas respectivas "gavetas"
        caixas_alta = [c for c in st.session_state['caixinhas'] if "Alta" in c['prioridade']]
        caixas_media = [c for c in st.session_state['caixinhas'] if "Média" in c['prioridade']]
        caixas_baixa = [c for c in st.session_state['caixinhas'] if "Baixa" in c['prioridade']]
        
        st.success("Cálculo realizado com sucesso! Veja o painel financeiro abaixo:")
        
        # 3. Exibindo os resultados em 3 colunas visuais
        res_col1, res_col2, res_col3 = st.columns(3)
        
        with res_col1:
            st.subheader(f"🔴 Essencial (50%)\nTotal: R$ {fatia_alta:.2f}")
            if len(caixas_alta) > 0:
                # Divide o dinheiro da fatia pelo número de caixinhas nela
                valor_por_caixa = fatia_alta / len(caixas_alta)
                for c in caixas_alta:
                    st.info(f"**{c['nome']}**: R$ {valor_por_caixa:.2f}")
            else:
                st.warning("Nenhuma conta essencial. Valor disponível para reserva.")
                
        with res_col2:
            st.subheader(f"🟡 Metas (30%)\nTotal: R$ {fatia_media:.2f}")
            if len(caixas_media) > 0:
                valor_por_caixa = fatia_media / len(caixas_media)
                for c in caixas_media:
                    st.info(f"**{c['nome']}**: R$ {valor_por_caixa:.2f}")
            else:
                st.warning("Nenhuma meta cadastrada. Valor disponível para reserva.")
                
        with res_col3:
            st.subheader(f"🟢 Desejos (20%)\nTotal: R$ {fatia_baixa:.2f}")
            if len(caixas_baixa) > 0:
                valor_por_caixa = fatia_baixa / len(caixas_baixa)
                for c in caixas_baixa:
                    st.info(f"**{c['nome']}**: R$ {valor_por_caixa:.2f}")
            else:
                st.warning("Nenhum desejo cadastrado. Valor disponível para reserva.")

                st.markdown("---")
        st.header("📊 4. Visão Gráfica e Inteligência Artificial")
        
        col_grafico, col_ia = st.columns(2)
        
        with col_grafico:
            st.subheader("Impacto Visual do Orçamento")
            st.info("Veja como o seu dinheiro está sendo fatiado este mês.")
            # O Pandas organiza os dados para o gráfico do Streamlit ler
            dados_grafico = pd.DataFrame({
                "Categoria": ["🔴 Essencial (50%)", "🟡 Metas (30%)", "🟢 Desejos (20%)"],
                "Valor (R$)": [fatia_alta, fatia_media, fatia_baixa]
            })
            # Gera um gráfico de barras automático
            st.bar_chart(dados_grafico.set_index("Categoria"))

st.markdown("---")
st.header("💾 Salvar ou Carregar Perfil")
col_export, col_import = st.columns(2)

with col_export:
    st.info("Baixe suas caixinhas para não precisar digitar tudo de novo no mês que vem.")
    # Transforma a lista de caixinhas em um texto no formato JSON
    dados_json = json.dumps(st.session_state['caixinhas'])
    
    # O botão mágico que faz o download do arquivo para o seu PC
    st.download_button(
        label="⬇️ Exportar Meu Perfil",
        data=dados_json,
        file_name="meu_perfil_ecofin.json",
        mime="application/json",
        type="primary"
    )

with col_import:
    st.info("Já tem um arquivo salvo do mês passado? Suba ele aqui.")
    # Cria a área onde você arrasta e solta o arquivo
    arquivo_up = st.file_uploader("Carregar arquivo .json", type=["json"])
    
    if arquivo_up is not None:
        # Se você subir um arquivo, ele lê e substitui a memória atual
        dados_carregados = json.load(arquivo_up)
        st.session_state['caixinhas'] = dados_carregados
        st.success("Perfil carregado! Os dados já estão na memória.")
import streamlit as st
from datetime import datetime, date
import json
import pandas as pd
import altair as alt
import gspread
from google.oauth2.service_account import Credentials

# Configurando credenciais com secrets
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=scope
)

# Autorizando
client = gspread.authorize(creds)

# Abrindo a planilha
sheet = client.open("OrganizacaoFinanceira").sheet1

# Testando leitura
data = sheet.get_all_records()
st.write("Dados da planilha:")
st.write(data)

# Interface Streamlit
st.title("Receitas")

descricao = st.text_input("Descrição")
valor = st.number_input("Valor", min_value=0.01, format="%.2f")
categoria = st.text_input("Categoria")

if st.button("Adicionar Receita"):
    adicionar_receita(descricao, valor, categoria)
    st.success("Receita adicionada!")

receitas = obter_receitas()
for r in receitas:
    st.write(f"{r['descricao']} | R$ {r['valor']} | {r['categoria']} | {r['data_hora']}")


st.set_page_config(
    page_title="Organização Financeira do Gabriel",
    page_icon="https://cdn-icons-png.flaticon.com/512/1170/1170576.png",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif !important;
    background-color: #121212 !important;  /* fundo escuro */
    color: #e0e0e0 !important;              /* texto claro */
    margin: 0; padding: 0;
}

/* Container geral para centralizar e dar espaçamento */
main.block-container {
    max-width: 900px;
    margin: 30px auto 80px auto;
    padding: 0 20px 40px 20px;
}

/* Títulos principais */
h1, .stMarkdown h1 {
    font-weight: 700 !important;
    color: #EF1B24 !important;   /* vermelho vivo */
    font-size: 2.8rem !important;
    margin-bottom: 0.4rem !important;
    text-align: center; /* centraliza o título */
}

h2, .stMarkdown h2 {
    font-weight: 600 !important;
    color: #b71c1c !important;
    margin-bottom: 1rem !important;
}

/* Métricas com destaque */
.stMetric {
    background: #2a2a2a !important;  /* cinza escuro */
    border: 2px solid #EF1B24 !important;
    border-radius: 12px !important;
    padding: 18px !important;
    margin-bottom: 15px !important;
    box-shadow: 0 3px 8px rgb(239 27 36 / 0.6);
    transition: transform 0.3s ease;
}

.stMetric:hover {
    transform: scale(1.05);
}

/* Botões padrão streamlit estilizados */
button, .stButton>button {
    background-color: #EF1B24 !important;
    color: white !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 30px !important;
    padding: 10px 30px !important;
    font-size: 1.1rem !important;
    cursor: pointer !important;
    box-shadow: 0 6px 12px rgb(239 27 36 / 0.8);
    transition: background-color 0.3s ease, box-shadow 0.3s ease, transform 0.2s ease;
}

button:hover, .stButton>button:hover {
    background-color: #b71c1c !important;
    box-shadow: 0 8px 16px rgb(183 28 28 / 0.9);
    transform: translateY(-3px);
}

button:active, .stButton>button:active {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgb(183 28 28 / 1);
}

/* Inputs de texto e número */
input[type="text"], input[type="number"], textarea, .stTextArea>textarea {
    background-color: #1f1f1f !important; /* fundo dos inputs escuro */
    border: 2px solid #EF1B24 !important;
    border-radius: 10px !important;
    padding: 10px !important;
    font-size: 1.05rem !important;
    color: #e0e0e0 !important;
    font-weight: 500 !important;
    transition: border-color 0.3s ease;
}

input[type="text"]:focus, input[type="number"]:focus, textarea:focus {
    border-color: #b71c1c !important;
    outline: none !important;
}

/* Cards de informações (exemplo para receitas/despesas) */
.informacao-card {
    background: #330000cc;  /* vermelho escuro transparente */
    border-left: 6px solid #EF1B24;
    padding: 15px 20px;
    margin-bottom: 12px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgb(239 27 36 / 0.5);
    transition: box-shadow 0.3s ease;
    color: #f1f1f1;
}

.informacao-card:hover {
    box-shadow: 0 6px 18px rgb(239 27 36 / 0.8);
}

/* Estilizando tabelas e listas */
table, ul, ol {
    font-size: 1.05rem !important;
    color: #ddd !important;
    margin-bottom: 20px !important;
}

/* Rodapé estilizado */
footer {
    text-align: center;
    color: #888888;
    font-size: 0.9rem;
    margin-top: 40px;
}

/* Menu inferior customizado (para o seu menu fixo) */
#bottom-menu {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: #EF1B24;
    display: flex;
    justify-content: space-around;
    padding: 14px 0;
    border-top: 3px solid #b71c1c;
    z-index: 9999;
    box-shadow: 0 -2px 10px rgb(239 27 36 / 0.9);
}
#bottom-menu button {
    background: none;
    border: none;
    color: #fff;
    font-weight: 600;
    font-size: 16px;
    cursor: pointer;
    padding: 8px 16px;
    border-radius: 20px;
    transition: background-color 0.3s ease, color 0.3s ease;
}
#bottom-menu button.active, #bottom-menu button:hover {
    background-color: #b71c1c;
    color: #fff;
    text-decoration: none;
    box-shadow: 0 4px 12px rgb(183 28 28 / 1);
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# Título centralizado na página
st.markdown("# Organização Financeira do Gabriel")




# --- Funções de dados ---
def salvar_dados(receitas, despesas, planejamentos, notas):
    with open("dados_financeiros.json", "w", encoding="utf-8") as f:
        json.dump({
            "receitas": receitas,
            "despesas": despesas,
            "planejamentos": planejamentos,
            "notas": notas
        }, f, ensure_ascii=False, indent=4)

def carregar_dados():
    try:
        with open("dados_financeiros.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
        return (dados.get("receitas", []), dados.get("despesas", []), 
                dados.get("planejamentos", []), dados.get("notas", ""))
    except FileNotFoundError:
        return [], [], [], ""

# --- Inicialização do estado ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "dashboard"

if "receitas" not in st.session_state:
    r, d, p, n = carregar_dados()
    st.session_state.receitas = r
    st.session_state.despesas = d
    st.session_state.planejamentos = p
    st.session_state.notas = n

# --- Funções das páginas ---
def dashboard():
    st.title("Dashboard")
    receitas = st.session_state.receitas
    despesas = st.session_state.despesas
    total_receitas = sum(r['valor'] for r in receitas)
    total_despesas = sum(d['valor'] for d in despesas)
    saldo = total_receitas - total_despesas
    st.metric("Total Receitas", f"R$ {total_receitas:.2f}")
    st.metric("Total Despesas", f"R$ {total_despesas:.2f}")
    st.metric("Saldo Atual", f"R$ {saldo:.2f}")

    if receitas or despesas:
        df = pd.DataFrame([
            {"tipo": "Receitas", "valor": total_receitas},
            {"tipo": "Despesas", "valor": total_despesas}
        ])
        chart = alt.Chart(df).mark_bar().encode(
            x="tipo",
            y="valor",
            color="tipo"
        )
        st.altair_chart(chart, use_container_width=True)

def receitas():
    st.title("Receitas")
    with st.form("form_receita"):
        descricao = st.text_input("Descrição", key="descricao_receita")
        valor = st.number_input("Valor", min_value=0.01, format="%.2f", key="valor_receita")
        categoria = st.text_input("Categoria", key="categoria_receita")
        submit = st.form_submit_button("Adicionar")
        if submit:
            nova = {
                "descricao": descricao,
                "valor": valor,
                "categoria": categoria,
                "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            st.session_state.receitas.append(nova)
            salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
            st.success("Receita adicionada!")

    for i, r in enumerate(st.session_state.receitas):
        st.write(f"{r['data_hora']} | {r['descricao']} | R$ {r['valor']:.2f} | {r['categoria']}")
        if st.button("Excluir", key=f"del_rec_{i}"):
            st.session_state.receitas.pop(i)
            salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
            st.rerun()
def despesas():
    st.title("Despesas")
    with st.form("form_despesa"):
        descricao = st.text_input("Descrição", key="descricao_despesa")
        valor = st.number_input("Valor", min_value=0.01, format="%.2f", key="valor_despesa")
        categoria = st.text_input("Categoria", key="categoria_despesa")
        submit = st.form_submit_button("Adicionar")
        if submit:
            nova = {
                "descricao": descricao,
                "valor": valor,
                "categoria": categoria,
                "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            st.session_state.despesas.append(nova)
            salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
            st.success("Despesa adicionada!")

    for i, d in enumerate(st.session_state.despesas):
        st.write(f"{d['data_hora']} | {d['descricao']} | R$ {d['valor']:.2f} | {d['categoria']}")
        if st.button("Excluir", key=f"del_desp_{i}"):
            st.session_state.despesas.pop(i)
            salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
            st.rerun()

def saldo():
    st.title("Saldo")
    total_receitas = sum(r['valor'] for r in st.session_state.receitas)
    total_despesas = sum(d['valor'] for d in st.session_state.despesas)
    saldo = total_receitas - total_despesas
    st.subheader(f"💰 Saldo Atual: R$ {saldo:.2f}")

def planejamento():
    st.title("Planejamento")
    with st.form("form_planejamento"):
        data_pag = st.date_input("Data do pagamento", value=date.today(), key="data_planejamento")
        descricao = st.text_input("Descrição", key="descricao_planejamento")
        submit = st.form_submit_button("Adicionar")
        if submit:
            novo = {"data": data_pag.strftime("%d/%m/%Y"), "descricao": descricao}
            st.session_state.planejamentos.append(novo)
            salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
            st.success("Planejamento salvo.")

    for i, p in enumerate(st.session_state.planejamentos):
        st.write(f"{p['data']} — {p['descricao']}")
        if st.button("Excluir", key=f"del_plan_{i}"):
            st.session_state.planejamentos.pop(i)
            salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
            st.experimental_rerun()

def agenda():
    st.title("Agenda")

    eventos = [
        {**r, "tipo": "Receita"} for r in st.session_state.receitas
    ] + [
        {**d, "tipo": "Despesa"} for d in st.session_state.despesas
    ]
    eventos.sort(key=lambda x: x["data_hora"], reverse=True)

    for ev in eventos:
        st.write(f"[{ev['tipo']}] {ev['data_hora']} - {ev['descricao']} - R$ {ev['valor']:.2f} - {ev['categoria']}")

    st.markdown("---")
    st.subheader("Notas")
    texto = st.text_area("Anotações:", value=st.session_state.notas, height=200, key="notas_text_area")
    if st.button("Salvar Notas", key="btn_salvar_notas"):
        st.session_state.notas = texto
        salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
        st.success("Notas salvas!")

def importar_exportar():
    st.title("Importar / Exportar")
    st.download_button("Exportar dados", json.dumps({
        "receitas": st.session_state.receitas,
        "despesas": st.session_state.despesas,
        "planejamentos": st.session_state.planejamentos,
        "notas": st.session_state.notas
    }, indent=4), file_name="backup_financeiro.json", mime="application/json")

    arquivo = st.file_uploader("Importar JSON", type=["json"], key="uploader_json")
    if arquivo:
        dados = json.load(arquivo)
        st.session_state.receitas = dados.get("receitas", [])
        st.session_state.despesas = dados.get("despesas", [])
        st.session_state.planejamentos = dados.get("planejamentos", [])
        st.session_state.notas = dados.get("notas", "")
        salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
        st.success("Dados importados com sucesso!")
        st.experimental_rerun()

def ajuda():
    st.title("Ajuda")
    st.markdown("""
    Sistema de controle financeiro com registro de receitas, despesas, planejamento, exportação/importação de dados e anotações.
    """)

# --- Sistema de abas substituindo o menu inferior fixo ---
tabs = st.tabs([
    "Dashboard",
    "Receitas",
    "Despesas",
    "Saldo",
    "Planejamento",
    "Agenda",
    "Importar/Exportar",
    "Ajuda"
])

with tabs[0]:
    dashboard()

with tabs[1]:
    receitas()

with tabs[2]:
    despesas()

with tabs[3]:
    saldo()

with tabs[4]:
    planejamento()

with tabs[5]:
    agenda()

with tabs[6]:
    importar_exportar()

with tabs[7]:
    ajuda()

# --- Rodapé ---
st.markdown("<div style='text-align:center; color:#999; font-size:10px; margin-top:30px;'>Criado por Canal do Gabriel 💼</div>", unsafe_allow_html=True)

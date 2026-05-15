import streamlit as st
from groq import Groq
import pandas as pd
from datetime import datetime, date
import json
import math

# ─────────────────────────────────────────────
# CONFIG PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(page_title="Oráculo Financeiro", page_icon="🔮", layout="wide")

# ─────────────────────────────────────────────
# DESIGN
# ─────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
header { visibility: hidden; }
.stApp { background-color: #F5F6FA; color: #1A1A2E; }
h1, h2, h3, h4 { color: #1A1A2E !important; font-family: 'Segoe UI', sans-serif; }
p, span, label, div { color: #333355; font-family: 'Segoe UI', sans-serif; }

.card        { background: #FFFFFF; border: 1px solid #E0E0EE; border-radius: 14px; padding: 20px 22px; margin-bottom: 14px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.card-green  { background: #F0FDF8; border: 1px solid #A7F3D0; border-radius: 14px; padding: 20px 22px; margin-bottom: 14px; }
.card-purple { background: #F5F3FF; border: 1px solid #C4B5FD; border-radius: 14px; padding: 20px 22px; margin-bottom: 14px; }
.card-gold   { background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 14px; padding: 20px 22px; margin-bottom: 14px; }
.card-red    { background: #FFF5F5; border: 1px solid #FECACA; border-radius: 14px; padding: 20px 22px; margin-bottom: 14px; }
.card-blue   { background: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 14px; padding: 20px 22px; margin-bottom: 14px; }

.metric-box   { background: #FFFFFF; border: 1px solid #E0E0EE; border-radius: 12px; padding: 14px 18px; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.metric-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1.2px; color: #888899; margin-bottom: 6px; }
.metric-value { font-size: 22px; font-weight: 700; color: #1A1A2E; }
.metric-sub   { font-size: 11px; color: #888899; margin-top: 3px; }

.badge-purple { background: #EDE9FE; color: #6D28D9; border: 1px solid #C4B5FD; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.badge-green  { background: #D1FAE5; color: #065F46; border: 1px solid #6EE7B7; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.badge-gold   { background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.badge-red    { background: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.badge-teal   { background: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }

.list-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: #F8F8FC; border-radius: 9px; margin-bottom: 7px; border: 1px solid #E8E8F0; }
.prog-wrap { background: #E0E0EE; border-radius: 999px; height: 7px; overflow: hidden; margin: 6px 0; }
.prog-fill { height: 100%; border-radius: 999px; }

.alert-danger  { background: #FEF2F2; border: 1px solid #FECACA; border-radius: 10px; padding: 12px 16px; color: #991B1B !important; margin-bottom: 10px; }
.alert-success { background: #F0FDF4; border: 1px solid #A7F3D0; border-radius: 10px; padding: 12px 16px; color: #065F46 !important; margin-bottom: 10px; }
.alert-warn    { background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 10px; padding: 12px 16px; color: #92400E !important; margin-bottom: 10px; }
.alert-info    { background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 12px 16px; color: #1E40AF !important; margin-bottom: 10px; }

.chat-user { background: #F0F0FA; border: 1px solid #E0E0EE; border-radius: 12px 12px 4px 12px; padding: 12px 16px; margin: 8px 0; }
.chat-ai   { background: #F5F3FF; border: 1px solid #C4B5FD; border-radius: 4px 12px 12px 12px; padding: 12px 16px; margin: 8px 0; }

.stButton > button { background: #5B50E8 !important; color: #fff !important; font-weight: 600 !important; border: none !important; border-radius: 9px !important; width: 100%; }
.stButton > button:hover { background: #4338CA !important; }

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea { background: #FFFFFF !important; color: #1A1A2E !important; border: 1px solid #D0D0E0 !important; border-radius: 8px !important; }
.stSelectbox > div > div { background: #FFFFFF !important; color: #1A1A2E !important; border: 1px solid #D0D0E0 !important; border-radius: 8px !important; }
[data-testid="stForm"] { background: #FFFFFF; border: 1px solid #E0E0EE; border-radius: 14px; padding: 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.stTabs [data-baseweb="tab-list"] { background: #FFFFFF; border-radius: 10px; padding: 3px; border: 1px solid #E0E0EE; gap: 3px; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #888899 !important; border-radius: 7px !important; }
.stTabs [aria-selected="true"] { background: #EEEAFF !important; color: #4338CA !important; font-weight: 600 !important; }
.stTabs [data-baseweb="tab-border"] { display: none; }
hr { border: none; border-top: 1px solid #E0E0EE !important; margin: 18px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INICIALIZAÇÃO DE ESTADOS
# ─────────────────────────────────────────────
def init():
    defaults = {
        "autenticado": False,
        "nome_user": "",
        "api_key": "",
        "renda_total": 0.0,
        "outras_rendas": [],       # {nome, valor, recorrente}
        "gastos": [],              # {tipo, descricao, valor, data, parcelado, parcelas}
        "metas": [],               # {nome, categoria, valor, mensal, prazo, atual, criada}
        "contas_fixas": [],        # {nome, valor, dia_venc, categoria, ativa}
        "dividas": [],             # {nome, valor_total, valor_pago, juros_mensal, parcela_mensal}
        "historico_chat": [],
        "categorias_gastos": ["Alimentação","Transporte","Moradia","Saúde","Lazer","Educação","Vestuário","Tecnologia","Outros"],
        "nivel_evolucao": "Nível 1: Iniciante",
        "perfil_decisao": "Não Identificado",
        "reserva_emergencia": 0.0,
        "patrimonio_itens": [],    # {nome, valor, tipo, categoria}
        "config_meta_reserva": 6,
        "taxa_invest_anual": 10.0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ─────────────────────────────────────────────
# UTILITÁRIOS
# ─────────────────────────────────────────────
def fmt(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def pct(v, total):
    return round(v / total * 100, 1) if total > 0 else 0.0

def barra(valor_pct, cor="#7C6FFF"):
    p = max(0, min(100, valor_pct))
    return f'<div class="prog-wrap"><div class="prog-fill" style="width:{p}%;background:{cor};"></div></div>'

def get_totais():
    renda  = st.session_state.renda_total + sum(x["valor"] for x in st.session_state.outras_rendas)
    gv     = sum(x["valor"] for x in st.session_state.gastos)
    gf     = sum(x["valor"] for x in st.session_state.contas_fixas if x.get("ativa", True))
    gm     = sum(x["mensal"] for x in st.session_state.metas)
    div_m  = sum(x["parcela_mensal"] for x in st.session_state.dividas)
    saldo  = renda - gv - gf - gm - div_m
    if renda > 0:
        r = saldo / renda
        if r >= 0.4:    st.session_state.nivel_evolucao = "Nível 5: Independente 🏆"
        elif r >= 0.25: st.session_state.nivel_evolucao = "Nível 4: Estratégico 🎯"
        elif r >= 0.1:  st.session_state.nivel_evolucao = "Nível 3: Organizado ✅"
        elif r >= 0:    st.session_state.nivel_evolucao = "Nível 2: Equilibrado ⚖️"
        else:           st.session_state.nivel_evolucao = "Nível 1: Déficit 🚨"
    return renda, gv, gf, gm, div_m, saldo

# ─────────────────────────────────────────────
# IA — CONSULTOR
# ─────────────────────────────────────────────
def contexto_financeiro():
    renda, gv, gf, gm, div_m, saldo = get_totais()
    meta_res = gf * st.session_state.config_meta_reserva
    cats = {}
    for g in st.session_state.gastos:
        cats[g["tipo"]] = cats.get(g["tipo"], 0) + g["valor"]
    cats_txt   = "\n".join(f"  • {c}: R${v:.2f} ({pct(v, renda)}%)" for c, v in cats.items()) or "  Nenhum"
    dividas_txt = "\n".join(f"  • {d['nome']}: saldo R${d['valor_total']-d['valor_pago']:.2f}, juros {d['juros_mensal']}%/mês" for d in st.session_state.dividas) or "  Nenhuma"
    metas_txt   = "\n".join(f"  • {m['nome']}: {fmt(m.get('atual',0))}/{fmt(m['valor'])}" for m in st.session_state.metas) or "  Nenhuma"
    return f"""
DADOS DO USUÁRIO:
Renda total: R${renda:.2f}
Despesas fixas: R${gf:.2f} ({pct(gf,renda)}%)
Gastos variáveis: R${gv:.2f} ({pct(gv,renda)}%)
Parcelas de dívidas: R${div_m:.2f}
Metas mensais: R${gm:.2f} ({pct(gm,renda)}%)
Saldo livre: R${saldo:.2f} ({pct(saldo,renda)}%)
Reserva atual: R${st.session_state.reserva_emergencia:.2f} (meta: R${meta_res:.2f})
Gastos por categoria:\n{cats_txt}
Dívidas:\n{dividas_txt}
Metas:\n{metas_txt}
"""

def consultor(prompt, historico):
    try:
        client = Groq(api_key=st.session_state.api_key)
        sys_msg = f"""Você é o Oráculo Financeiro — mentor de decisões financeiras pessoais.
Filosofia: direto, estratégico, sem rodeios. Aponta problemas sem medo.
Nomenclatura: Blindagem = fixas+reserva | Expansão = metas/investimentos | Estabilidade = saldo livre.
Regra 50/30/20: 50% necessidades, 30% desejos, 20% poupança.
{contexto_financeiro()}
Nível: {st.session_state.nivel_evolucao} | Perfil: {st.session_state.perfil_decisao}
Responda em no máximo 4 parágrafos curtos. Sugira 1 ação concreta ao final.
Termine sempre com: "⚠️ Análise baseada nos seus dados. Consulte um profissional certificado para decisões de grande impacto."
"""
        msgs = [{"role": "system", "content": sys_msg}]
        for m in historico[-10:]:
            msgs.append(m)
        msgs.append({"role": "user", "content": prompt})
        r = client.chat.completions.create(messages=msgs, model="llama-3.3-70b-versatile", max_tokens=700, temperature=0.7)
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ Oráculo indisponível. Verifique sua chave API. Erro: {str(e)[:80]}"

# ─────────────────────────────────────────────
# TELA DE LOGIN
# ─────────────────────────────────────────────
if not st.session_state.autenticado:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.6, 1])
    with col:
        st.markdown("""
        <div class="card" style="text-align:center; padding:40px;">
          <div style="font-size:56px; margin-bottom:12px;">🔮</div>
          <h1 style="font-size:28px; margin:0; color:#1A1A2E;">Oráculo Financeiro</h1>
          <p style="font-size:13px; color:#888899; letter-spacing:2px; margin-top:6px;">ECONOMIZE • GERENCIE • INVISTA • CRESÇA</p>
        </div>
        """, unsafe_allow_html=True)
        with st.form("login"):
            nome  = st.text_input("👤 Seu nome")
            chave = st.text_input("🔑 Chave Groq API", type="password", help="Grátis em console.groq.com")
            if st.form_submit_button("🚀 ENTRAR NO SISTEMA"):
                if nome and chave:
                    st.session_state.nome_user   = nome
                    st.session_state.api_key     = chave
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("Preencha nome e chave API.")
    st.stop()

# ─────────────────────────────────────────────
# SISTEMA LOGADO
# ─────────────────────────────────────────────
renda, gv, gf, gm, div_m, saldo = get_totais()

# HEADER
c1, c2, c3 = st.columns([3, 2, 1])
with c1:
    st.markdown(f"<h1 style='margin:0;font-size:24px;color:#1A1A2E;'>🔮 Oráculo de {st.session_state.nome_user}</h1>", unsafe_allow_html=True)
with c2:
    nivel = st.session_state.nivel_evolucao
    cls   = "badge-green" if ("5" in nivel or "4" in nivel) else ("badge-gold" if ("3" in nivel or "2" in nivel) else "badge-red")
    st.markdown(f"<div style='padding:14px 0;text-align:right;'><span class='{cls}' style='padding:6px 14px;font-size:12px;'>{nivel}</span></div>", unsafe_allow_html=True)
with c3:
    if st.button("🚪 Sair"):
        st.session_state.autenticado = False
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# TABS
tabs = st.tabs([
    "🏠 Dashboard", "🧠 Consultor IA", "💵 Renda",
    "💸 Gastos", "🎯 Metas", "🛡️ Fixas",
    "💳 Dívidas", "🏦 Reserva", "📈 Investimentos",
    "⚖️ Patrimônio", "📊 Relatório", "⚙️ Config"
])
(tab_dash, tab_ia, tab_renda, tab_gastos, tab_metas,
 tab_fixas, tab_div, tab_res, tab_inv,
 tab_pat, tab_rel, tab_cfg) = tabs

# ══════════════════════════════════════════════
# 1. DASHBOARD
# ══════════════════════════════════════════════
with tab_dash:
    # Alerta de situação
    if renda == 0:
        st.markdown('<div class="alert-info">ℹ️ Comece cadastrando sua renda na aba <b>Renda</b>.</div>', unsafe_allow_html=True)
    elif saldo < 0:
        st.markdown(f'<div class="alert-danger">🚨 <b>Déficit de {fmt(abs(saldo))}!</b> Você gasta mais do que ganha. Ação imediata necessária.</div>', unsafe_allow_html=True)
    elif saldo < renda * 0.1:
        st.markdown(f'<div class="alert-warn">⚠️ Margem muito baixa ({pct(saldo,renda)}%). Recomendado: mínimo 20% livre.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-success">✅ Sistema saudável. {fmt(saldo)} livres para expandir.</div>', unsafe_allow_html=True)

    # MÉTRICAS PRINCIPAIS
    c1, c2, c3, c4, c5 = st.columns(5)
    def metrica(col, label, val, cor, sub=""):
        col.markdown(f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value" style="color:{cor};">{fmt(val)}</div><div class="metric-sub">{sub}</div></div>', unsafe_allow_html=True)

    metrica(c1, "💰 Renda",            renda,            "#6EE7B7", "total/mês")
    metrica(c2, "🛡️ Blindagem",        gf,               "#7DD3FC", f"{pct(gf,renda)}% da renda")
    metrica(c3, "💸 Gastos Variáveis",  gv,               "#FCD34D", f"{pct(gv,renda)}% da renda")
    metrica(c4, "🚀 Metas/Mês",         gm,               "#A78BFA", f"{pct(gm,renda)}% da renda")
    cor_s = "#6EE7B7" if saldo >= 0 else "#FCA5A5"
    metrica(c5, "⚖️ Estabilidade",     saldo,            cor_s,     f"{pct(saldo,renda)}% livre")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        # Distribuição da renda em barras
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>📊 Distribuição da Renda</b>", unsafe_allow_html=True)
        if renda > 0:
            for nome_d, val_d, cor_d in [
                ("🛡️ Fixas",       gf,              "#38BDF8"),
                ("💸 Variáveis",   gv,              "#FCD34D"),
                ("💳 Dívidas",     div_m,           "#FCA5A5"),
                ("🚀 Metas",       gm,              "#A78BFA"),
                ("✅ Livre",       max(0, saldo),   "#6EE7B7"),
            ]:
                pct_d = pct(val_d, renda)
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                  <span style="font-size:13px;color:#555577;">{nome_d}</span>
                  <span style="font-size:13px;color:#1A1A2E;">{fmt(val_d)} <span style="color:#888899;">({pct_d}%)</span></span>
                </div>{barra(pct_d, cor_d)}""", unsafe_allow_html=True)
        else:
            st.markdown("<p>Cadastre sua renda para ver a distribuição.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Regra 50/30/20
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>📐 Regra 50/30/20</b>", unsafe_allow_html=True)
        if renda > 0:
            cats_nec = ["Moradia","Alimentação","Saúde","Transporte"]
            cats_des = ["Lazer","Vestuário","Tecnologia"]
            nec = gf + sum(g["valor"] for g in st.session_state.gastos if g["tipo"] in cats_nec)
            des = sum(g["valor"] for g in st.session_state.gastos if g["tipo"] in cats_des)
            pou = gm
            for rotulo_r, valor_r, ideal_r, cor_r in [
                ("🏠 Necessidades (ideal 50%)", nec, 50, "#38BDF8"),
                ("🎮 Desejos     (ideal 30%)",  des, 30, "#FCD34D"),
                ("📈 Poupança    (ideal 20%)",  pou, 20, "#6EE7B7"),
            ]:
                real_r = pct(valor_r, renda)
                ok_r   = "✅" if abs(real_r - ideal_r) <= 10 else "⚠️"
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                  <span style="font-size:13px;color:#555577;">{rotulo_r}</span>
                  <span style="font-size:13px;color:#1A1A2E;">{ok_r} {real_r:.1f}%</span>
                </div>{barra(real_r, cor_r)}""", unsafe_allow_html=True)
        else:
            st.markdown("<p>Cadastre sua renda para ver a análise.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        # Reserva de emergência
        meta_res_d = gf * st.session_state.config_meta_reserva
        pct_res_d  = pct(st.session_state.reserva_emergencia, meta_res_d) if meta_res_d > 0 else 0
        st.markdown(f"""<div class="card-green">
        <b style='color:#1A1A2E;'>🛡️ Reserva de Emergência</b><br>
        <span style='font-size:13px;color:#555577;'>{fmt(st.session_state.reserva_emergencia)} de {fmt(meta_res_d)} ({st.session_state.config_meta_reserva} meses)</span>
        {barra(pct_res_d, "#10B981")}
        <span style='font-size:12px;color:#888899;'>{'✅ Completa!' if pct_res_d >= 100 else f'Faltam {fmt(max(0, meta_res_d - st.session_state.reserva_emergencia))}'}</span>
        </div>""", unsafe_allow_html=True)

        # Metas rápidas
        if st.session_state.metas:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<b style='color:#1A1A2E;'>🎯 Metas em Andamento</b>", unsafe_allow_html=True)
            for m in st.session_state.metas[:4]:
                p_m   = pct(m.get("atual", 0), m["valor"])
                rest  = round((m["valor"] - m.get("atual", 0)) / m["mensal"]) if m["mensal"] > 0 else "∞"
                st.markdown(f"""
                <div style="margin-bottom:10px;">
                  <div style="display:flex;justify-content:space-between;">
                    <span style="font-size:13px;color:#1A1A2E;">{m['nome']}</span>
                    <span style="font-size:12px;color:#888899;">{p_m:.0f}% · {rest} meses</span>
                  </div>{barra(p_m, "#7C6FFF")}
                  <span style="font-size:11px;color:#888899;">{fmt(m.get('atual',0))} / {fmt(m['valor'])} · {fmt(m['mensal'])}/mês</span>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Dívidas resumo
        if st.session_state.dividas:
            total_div_d = sum(d["valor_total"] - d["valor_pago"] for d in st.session_state.dividas)
            st.markdown(f"""<div class="card-red">
            <b style='color:#1A1A2E;'>💳 Dívidas em Aberto</b><br>
            <span style='font-size:22px;font-weight:700;color:#991B1B;'>{fmt(total_div_d)}</span>
            <span style='font-size:12px;color:#888899;'> saldo total · {fmt(div_m)}/mês</span><br>
            <span style='font-size:12px;color:#888899;'>{len(st.session_state.dividas)} dívida(s) ativa(s)</span>
            </div>""", unsafe_allow_html=True)

        # Diagnóstico automático
        st.markdown('<div class="card-purple">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>💡 Diagnóstico Automático</b>", unsafe_allow_html=True)
        dicas = []
        if renda > 0:
            if pct(gf, renda) > 50:    dicas.append(("⚠️", "Fixas acima de 50% da renda. Revise contratos e assinaturas.", "warn"))
            if pct(gv, renda) > 30:    dicas.append(("💸", "Variáveis acima de 30%. Identifique onde cortar.", "warn"))
            if pct(gm, renda) < 10:    dicas.append(("🎯", "Menos de 10% alocado em metas. Aumente gradualmente.", "info"))
            if pct_res_d < 100:        dicas.append(("🛡️", "Reserva incompleta. Priorize antes de investir.", "warn"))
            if st.session_state.dividas: dicas.append(("💳", "Quite dívidas com juros altos primeiro (estratégia avalanche).", "warn"))
            if saldo < 0:              dicas.append(("🚨", "DÉFICIT! Você gasta mais do que ganha. Corte imediato necessário.", "danger"))
            if saldo > renda * 0.3 and pct_res_d >= 100:
                                        dicas.append(("🚀", "Ótima saúde financeira! Hora de acelerar os investimentos.", "success"))
        if not dicas:
            dicas = [("ℹ️", "Preencha seus dados para receber o diagnóstico completo.", "info")]
        cls_map = {"warn":"alert-warn","info":"alert-info","danger":"alert-danger","success":"alert-success"}
        for ic, tx, tp in dicas:
            st.markdown(f'<div class="{cls_map[tp]}" style="margin-bottom:6px;">{ic} {tx}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 2. CONSULTOR IA
# ══════════════════════════════════════════════
with tab_ia:
    col_d, col_c = st.columns([1, 1.5])

    with col_d:
        st.markdown('<div class="card-purple">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🧬 Perfil de Decisão</b>", unsafe_allow_html=True)
        d1 = st.select_slider("Sem renda, sobreviveria:", ["< 1 mês","1-3 meses","3-6 meses","6-12 meses","1 ano+"])
        d2 = st.radio("Maior medo:", ["Perder o que tenho","Deixar de ganhar","Dívidas"], horizontal=True)
        d3 = st.radio("Objetivo:", ["Liberdade financeira","Estabilidade","Crescimento"], horizontal=True)
        d4 = st.radio("Tolerância ao risco:", ["Conservador","Moderado","Arrojado"], horizontal=True)
        if st.button("🔍 MAPEAR MEU PERFIL"):
            st.session_state.perfil_decisao = f"{d3} | Risco: {d4} | Reserva: {d1}"
            st.success(f"Perfil mapeado: {d3}, {d4}")
        st.markdown("</div>", unsafe_allow_html=True)

        # Simulador de investimento
        st.markdown('<div class="card-gold">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>📈 Simulador de Investimento</b>", unsafe_allow_html=True)
        v_inv   = st.number_input("Aporte mensal (R$):", value=500.0, min_value=0.0, step=50.0)
        t_inv   = st.slider("Prazo (anos):", 1, 40, 10)
        cap_ini = st.number_input("Capital inicial (R$):", value=0.0, min_value=0.0, step=100.0)
        taxa_a  = st.session_state.taxa_invest_anual
        taxa_m  = (1 + taxa_a / 100) ** (1/12) - 1
        if taxa_m > 0:
            montante = cap_ini*(1+taxa_m)**(t_inv*12) + v_inv*(((1+taxa_m)**(t_inv*12)-1)/taxa_m)
        else:
            montante = cap_ini + v_inv*t_inv*12
        investido = cap_ini + v_inv*t_inv*12
        lucro     = montante - investido
        st.markdown(f"""
        <div style="display:flex;gap:10px;margin:10px 0;">
          <div style="flex:1;background:#F0F0FA;border-radius:9px;padding:12px;text-align:center;">
            <div style="font-size:11px;color:#888899;">Montante Final</div>
            <div style="font-size:17px;font-weight:700;color:#065F46;">{fmt(montante)}</div>
          </div>
          <div style="flex:1;background:#F0F0FA;border-radius:9px;padding:12px;text-align:center;">
            <div style="font-size:11px;color:#888899;">Lucro</div>
            <div style="font-size:17px;font-weight:700;color:#6D28D9;">{fmt(lucro)}</div>
          </div>
        </div>
        <span style="font-size:11px;color:#888899;">Taxa: {taxa_a}% a.a. | Total investido: {fmt(investido)}</span>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Perguntas rápidas
        st.markdown("<b style='color:#1A1A2E;font-size:13px;'>⚡ Perguntas Rápidas</b>", unsafe_allow_html=True)
        for q in [
            "Analise minha saúde financeira completa",
            "Como priorizar meus objetivos agora?",
            "Onde posso cortar gastos sem sofrimento?",
            "Quanto devo investir com meu saldo atual?",
            "Como quitar minhas dívidas mais rápido?",
        ]:
            if st.button(f"→ {q}", key=f"qr_{q[:18]}"):
                with st.spinner("Consultando o Oráculo..."):
                    resp = consultor(q, st.session_state.historico_chat)
                st.session_state.historico_chat.append({"role":"user","content":q})
                st.session_state.historico_chat.append({"role":"assistant","content":resp})
                st.rerun()

    with col_c:
        st.markdown("<b style='color:#1A1A2E;font-size:16px;'>💼 Mentor de Decisão</b>", unsafe_allow_html=True)
        if not st.session_state.historico_chat:
            st.markdown('<div class="alert-info" style="text-align:center;">🔮 Faça sua primeira pergunta. O Oráculo conhece seus números e vai ser direto ao ponto.</div>', unsafe_allow_html=True)
        for msg in st.session_state.historico_chat:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user"><span style="font-size:11px;color:#888899;">👤 {st.session_state.nome_user}</span><br><span style="color:#1A1A2E;">{msg["content"]}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai"><span style="font-size:11px;color:#5B50E8;">🔮 Oráculo</span><br><span style="color:#333355;">{msg["content"]}</span></div>', unsafe_allow_html=True)

        if p := st.chat_input("Qual é sua dúvida ou decisão financeira?"):
            with st.spinner("O Oráculo está analisando..."):
                resp = consultor(p, st.session_state.historico_chat)
            st.session_state.historico_chat.append({"role":"user","content":p})
            st.session_state.historico_chat.append({"role":"assistant","content":resp})
            st.rerun()

        if st.session_state.historico_chat:
            if st.button("🗑️ Limpar conversa"):
                st.session_state.historico_chat = []
                st.rerun()

# ══════════════════════════════════════════════
# 3. RENDA
# ══════════════════════════════════════════════
with tab_renda:
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown('<div class="card-green">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>💵 Renda Principal</b>", unsafe_allow_html=True)
        with st.form("renda_principal"):
            nr = st.number_input("Salário / Renda Mensal (R$)", min_value=0.0, value=st.session_state.renda_total, step=100.0)
            if st.form_submit_button("💾 SALVAR"):
                st.session_state.renda_total = nr
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>➕ Outras Fontes de Renda</b>", unsafe_allow_html=True)
        with st.form("outras_rendas_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1: nr_nome = st.text_input("Fonte", placeholder="Freela, aluguel...")
            with c2: nr_val  = st.number_input("Valor (R$)", min_value=0.0, step=50.0)
            nr_rec = st.checkbox("Recorrente todo mês?", value=True)
            if st.form_submit_button("ADICIONAR"):
                if nr_nome and nr_val > 0:
                    st.session_state.outras_rendas.append({"nome":nr_nome,"valor":nr_val,"recorrente":nr_rec})
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r2:
        total_r = st.session_state.renda_total + sum(x["valor"] for x in st.session_state.outras_rendas)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#1A1A2E;'>📋 Todas as Fontes — Total: {fmt(total_r)}/mês</b>", unsafe_allow_html=True)
        st.markdown(f'<div class="list-item"><span style="color:#1A1A2E;">💼 Salário principal</span><span style="color:#065F46;font-weight:600;">{fmt(st.session_state.renda_total)}</span></div>', unsafe_allow_html=True)
        for i, r in enumerate(st.session_state.outras_rendas):
            rec = "🔄" if r["recorrente"] else "1️⃣"
            col_rx, col_rd = st.columns([4, 1])
            with col_rx:
                st.markdown(f'<div class="list-item"><span style="color:#1A1A2E;">{rec} {r["nome"]}</span><span style="color:#065F46;">{fmt(r["valor"])}</span></div>', unsafe_allow_html=True)
            with col_rd:
                if st.button("✕", key=f"del_or_{i}"):
                    st.session_state.outras_rendas.pop(i); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 4. GASTOS VARIÁVEIS
# ══════════════════════════════════════════════
with tab_gastos:
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>💸 Registrar Gasto</b>", unsafe_allow_html=True)
        with st.expander("⚙️ Gerenciar categorias"):
            nova_c = st.text_input("Nova categoria:")
            if st.button("Adicionar categoria"):
                if nova_c and nova_c not in st.session_state.categorias_gastos:
                    st.session_state.categorias_gastos.append(nova_c); st.rerun()
            cat_rem = st.selectbox("Remover categoria:", ["—"] + st.session_state.categorias_gastos)
            if st.button("Remover") and cat_rem != "—":
                st.session_state.categorias_gastos.remove(cat_rem); st.rerun()
        with st.form("gasto_form", clear_on_submit=True):
            g_cat  = st.selectbox("Categoria", st.session_state.categorias_gastos)
            g_desc = st.text_input("Descrição", placeholder="Ex: Supermercado extra")
            c1, c2 = st.columns(2)
            with c1: g_val  = st.number_input("Valor (R$)", min_value=0.0, step=10.0)
            with c2: g_data = st.date_input("Data", value=date.today())
            g_parc = st.checkbox("É parcelado?")
            g_np   = st.number_input("Nº parcelas", min_value=1, max_value=48, value=1) if g_parc else 1
            if st.form_submit_button("💾 REGISTRAR"):
                if g_val > 0:
                    st.session_state.gastos.append({"tipo":g_cat,"descricao":g_desc,"valor":g_val,"data":str(g_data),"parcelado":g_parc,"parcelas":g_np})
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_g2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#1A1A2E;'>📋 Gastos Registrados — Total: {fmt(gv)}</b>", unsafe_allow_html=True)
        if not st.session_state.gastos:
            st.markdown("<p>Nenhum gasto registrado ainda.</p>", unsafe_allow_html=True)
        else:
            cats_p  = list(set(g["tipo"] for g in st.session_state.gastos))
            filtro  = st.multiselect("Filtrar por categoria:", cats_p, default=cats_p)
            gastos_f = [g for g in st.session_state.gastos if g["tipo"] in filtro]
            for i, g in enumerate(gastos_f):
                parc_t = f" ({g['parcelas']}x)" if g.get("parcelado") else ""
                desc_t = f'<br><span style="font-size:11px;color:#888899;">{g["descricao"]}</span>' if g.get("descricao") else ""
                col_gi, col_gd = st.columns([5, 1])
                with col_gi:
                    st.markdown(f'<div class="list-item"><div><span style="color:#1A1A2E;">{g["tipo"]}{parc_t}</span>{desc_t}<br><span style="font-size:11px;color:#888899;">{g.get("data","")}</span></div><span style="color:#92400E;font-weight:600;">{fmt(g["valor"])}</span></div>', unsafe_allow_html=True)
                with col_gd:
                    idx = st.session_state.gastos.index(g)
                    if st.button("✕", key=f"del_g_{i}"):
                        st.session_state.gastos.pop(idx); st.rerun()
            # Totais por categoria
            if gastos_f:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<b style='color:#1A1A2E;font-size:13px;'>Por categoria:</b>", unsafe_allow_html=True)
                df_cat = pd.DataFrame(gastos_f).groupby("tipo")["valor"].sum().sort_values(ascending=False)
                for cat_n, val_c in df_cat.items():
                    p_c = pct(val_c, gv)
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                      <span style="font-size:12px;color:#555577;">{cat_n}</span>
                      <span style="font-size:12px;color:#1A1A2E;">{fmt(val_c)} ({p_c}%)</span>
                    </div>{barra(p_c, "#FCD34D")}""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 5. METAS
# ══════════════════════════════════════════════
with tab_metas:
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown('<div class="card-purple">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🎯 Criar Nova Meta</b>", unsafe_allow_html=True)
        with st.form("meta_form", clear_on_submit=True):
            m_nome  = st.text_input("Nome da meta", placeholder="Ex: Viagem Europa")
            m_cat   = st.selectbox("Categoria", ["Viagem","Carro","Casa","Educação","Investimento","Reserva","Emergência","Outro"])
            c1, c2  = st.columns(2)
            with c1: m_val   = st.number_input("Valor total (R$)", min_value=1.0, step=100.0)
            with c2: m_prazo = st.number_input("Prazo (meses)", min_value=1, max_value=360, value=12)
            m_atual = st.number_input("Já guardei (R$)", min_value=0.0, step=100.0)
            if st.form_submit_button("🚀 CRIAR META"):
                if m_nome and m_val:
                    mensal = (m_val - m_atual) / m_prazo if m_prazo > 0 else m_val
                    st.session_state.metas.append({"nome":m_nome,"categoria":m_cat,"valor":m_val,"mensal":mensal,"prazo":m_prazo,"atual":m_atual,"criada":str(date.today())})
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_m2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#1A1A2E;'>📋 Metas Ativas — {fmt(gm)}/mês alocados</b>", unsafe_allow_html=True)
        if not st.session_state.metas:
            st.markdown("<p>Nenhuma meta criada ainda.</p>", unsafe_allow_html=True)
        else:
            for i, m in enumerate(st.session_state.metas):
                p_m  = pct(m.get("atual", 0), m["valor"])
                rest = max(0, round((m["valor"]-m.get("atual",0))/m["mensal"])) if m["mensal"] > 0 else "∞"
                col_mi, col_md = st.columns([5, 1])
                with col_mi:
                    st.markdown(f"""<div class="card-purple" style="padding:12px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;">
                      <b style="color:#1A1A2E;">{m['nome']}</b>
                      <span class="badge-purple">{m.get('categoria','')}</span>
                    </div>
                    <span style="font-size:12px;color:#555577;">{fmt(m.get('atual',0))} / {fmt(m['valor'])} · {fmt(m['mensal'])}/mês · {rest} meses</span>
                    {barra(p_m, "#7C6FFF")}
                    <span style="font-size:11px;color:#5B50E8;">{p_m:.1f}% concluído</span>
                    </div>""", unsafe_allow_html=True)
                    novo_a = st.number_input("Valor guardado:", min_value=0.0, max_value=float(m["valor"]), value=float(m.get("atual",0)), key=f"ma_{i}")
                    if st.button("Atualizar progresso", key=f"upd_m_{i}"):
                        st.session_state.metas[i]["atual"]  = novo_a
                        st.session_state.metas[i]["mensal"] = (m["valor"]-novo_a)/m["prazo"] if m["prazo"] > 0 else 0
                        st.rerun()
                with col_md:
                    if st.button("✕", key=f"del_m_{i}"):
                        st.session_state.metas.pop(i); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 6. CONTAS FIXAS
# ══════════════════════════════════════════════
with tab_fixas:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🛡️ Adicionar Conta Fixa</b>", unsafe_allow_html=True)
        with st.form("fixa_form", clear_on_submit=True):
            f_nome = st.text_input("Nome", placeholder="Ex: Aluguel, Netflix...")
            f_cat  = st.selectbox("Categoria", ["Moradia","Transporte","Alimentação","Saúde","Educação","Lazer","Serviços","Seguros","Outros"])
            c1, c2 = st.columns(2)
            with c1: f_val = st.number_input("Valor mensal (R$)", min_value=0.0, step=10.0)
            with c2: f_dia = st.number_input("Dia do vencimento", min_value=1, max_value=31, value=10)
            if st.form_submit_button("ADICIONAR"):
                if f_nome and f_val > 0:
                    st.session_state.contas_fixas.append({"nome":f_nome,"valor":f_val,"dia_venc":f_dia,"categoria":f_cat,"ativa":True})
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_f2:
        total_fixas_ativas = sum(x["valor"] for x in st.session_state.contas_fixas if x.get("ativa", True))
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#1A1A2E;'>🔒 Contas Fixas — {fmt(total_fixas_ativas)}/mês</b>", unsafe_allow_html=True)
        if not st.session_state.contas_fixas:
            st.markdown("<p>Nenhuma conta fixa cadastrada.</p>", unsafe_allow_html=True)
        else:
            fixas_ord = sorted(st.session_state.contas_fixas, key=lambda x: x.get("dia_venc", 99))
            for i, f in enumerate(fixas_ord):
                idx   = st.session_state.contas_fixas.index(f)
                ativa = f.get("ativa", True)
                col_fi, col_ft, col_fd = st.columns([4, 1, 1])
                with col_fi:
                    op = "1" if ativa else "0.4"
                    st.markdown(f'<div class="list-item" style="opacity:{op};"><div><span style="color:#1A1A2E;">{f["nome"]}</span><br><span style="font-size:11px;color:#888899;">Dia {f.get("dia_venc","?")} · {f.get("categoria","")}</span></div><span style="color:#0369A1;font-weight:600;">{fmt(f["valor"])}</span></div>', unsafe_allow_html=True)
                with col_ft:
                    if st.button("⏸" if ativa else "▶", key=f"tog_f_{i}"):
                        st.session_state.contas_fixas[idx]["ativa"] = not ativa; st.rerun()
                with col_fd:
                    if st.button("✕", key=f"del_f_{i}"):
                        st.session_state.contas_fixas.pop(idx); st.rerun()
            # Totais por categoria
            st.markdown("<hr>", unsafe_allow_html=True)
            cats_f = {}
            for f in st.session_state.contas_fixas:
                if f.get("ativa", True):
                    cats_f[f["categoria"]] = cats_f.get(f["categoria"], 0) + f["valor"]
            for cat_f, val_f in sorted(cats_f.items(), key=lambda x: -x[1]):
                p_f = pct(val_f, total_fixas_ativas)
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                  <span style="font-size:12px;color:#555577;">{cat_f}</span>
                  <span style="font-size:12px;color:#1A1A2E;">{fmt(val_f)}</span>
                </div>{barra(p_f, "#38BDF8")}""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 7. DÍVIDAS
# ══════════════════════════════════════════════
with tab_div:
    st.markdown('<div class="alert-info">💡 <b>Avalanche:</b> quite a dívida de maior juros primeiro (economiza mais dinheiro). <b>Bola de Neve:</b> quite a menor primeiro (mais motivação).</div>', unsafe_allow_html=True)
    col_dv1, col_dv2 = st.columns(2)
    with col_dv1:
        st.markdown('<div class="card-red">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>💳 Cadastrar Dívida</b>", unsafe_allow_html=True)
        with st.form("div_form", clear_on_submit=True):
            d_nome    = st.text_input("Nome", placeholder="Ex: Cartão Nubank, Financiamento Carro")
            c1, c2    = st.columns(2)
            with c1: d_total   = st.number_input("Valor total da dívida (R$)", min_value=0.0, step=100.0)
            with c2: d_pago    = st.number_input("Já paguei (R$)", min_value=0.0, step=100.0)
            c3, c4    = st.columns(2)
            with c3: d_juros   = st.number_input("Juros ao mês (%)", min_value=0.0, max_value=100.0, step=0.1)
            with c4: d_parcela = st.number_input("Parcela mensal (R$)", min_value=0.0, step=50.0)
            if st.form_submit_button("REGISTRAR DÍVIDA"):
                if d_nome and d_total > 0:
                    st.session_state.dividas.append({"nome":d_nome,"valor_total":d_total,"valor_pago":d_pago,"juros_mensal":d_juros,"parcela_mensal":d_parcela})
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_dv2:
        total_div = sum(d["valor_total"] - d["valor_pago"] for d in st.session_state.dividas)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#1A1A2E;'>📋 Dívidas — Saldo Total: {fmt(total_div)}</b>", unsafe_allow_html=True)
        if not st.session_state.dividas:
            st.markdown('<div class="alert-success">✅ Nenhuma dívida cadastrada. Parabéns!</div>', unsafe_allow_html=True)
        else:
            # Ordenar por juros (avalanche)
            dividas_ord = sorted(st.session_state.dividas, key=lambda x: -x["juros_mensal"])
            for i, d in enumerate(dividas_ord):
                saldo_d = d["valor_total"] - d["valor_pago"]
                p_d     = pct(d["valor_pago"], d["valor_total"])
                idx     = st.session_state.dividas.index(d)
                col_di, col_dd = st.columns([5, 1])
                with col_di:
                    st.markdown(f"""<div class="card-red" style="padding:12px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;">
                      <b style="color:#1A1A2E;">{d['nome']}</b>
                      <span class="badge-red">{d['juros_mensal']}%/mês</span>
                    </div>
                    <span style="font-size:12px;color:#555577;">Saldo: {fmt(saldo_d)} · Parcela: {fmt(d['parcela_mensal'])}/mês</span>
                    {barra(p_d, "#EF4444")}
                    <span style="font-size:11px;color:#991B1B;">{p_d:.1f}% quitado</span>
                    </div>""", unsafe_allow_html=True)
                    novo_pago = st.number_input("Valor já pago:", min_value=0.0, max_value=float(d["valor_total"]), value=float(d["valor_pago"]), key=f"dp_{i}")
                    if st.button("Atualizar pagamento", key=f"upd_d_{i}"):
                        st.session_state.dividas[idx]["valor_pago"] = novo_pago
                        if novo_pago >= d["valor_total"]:
                            st.session_state.dividas.pop(idx)
                            st.success("🎉 Dívida quitada!")
                        st.rerun()
                with col_dd:
                    if st.button("✕", key=f"del_d_{i}"):
                        st.session_state.dividas.pop(idx); st.rerun()

            # Previsão de quitação
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<b style='color:#1A1A2E;font-size:13px;'>⏱️ Previsão de Quitação</b>", unsafe_allow_html=True)
            for d in dividas_ord:
                saldo_d = d["valor_total"] - d["valor_pago"]
                try:
                    if d["parcela_mensal"] > 0 and d["juros_mensal"] > 0:
                        taxa_md  = d["juros_mensal"] / 100
                        meses_d  = math.ceil(math.log(d["parcela_mensal"] / (d["parcela_mensal"] - saldo_d*taxa_md)) / math.log(1+taxa_md)) if d["parcela_mensal"] > saldo_d*taxa_md else 999
                    elif d["parcela_mensal"] > 0:
                        meses_d  = math.ceil(saldo_d / d["parcela_mensal"])
                    else:
                        meses_d  = 999
                except:
                    meses_d = 999
                txt_m = f"{meses_d} meses" if meses_d < 999 else "Revise a parcela"
                st.markdown(f'<div class="list-item"><span style="color:#1A1A2E;">{d["nome"]}</span><span style="color:#991B1B;">{txt_m}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 8. RESERVA DE EMERGÊNCIA
# ══════════════════════════════════════════════
with tab_res:
    meta_res = gf * st.session_state.config_meta_reserva
    pct_res  = pct(st.session_state.reserva_emergencia, meta_res) if meta_res > 0 else 0
    falta_res = max(0, meta_res - st.session_state.reserva_emergencia)
    col_rv1, col_rv2 = st.columns(2)

    with col_rv1:
        st.markdown('<div class="card-green">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🛡️ Reserva de Emergência</b>", unsafe_allow_html=True)
        st.markdown(f"<p>Ideal: <b style='color:#065F46;'>{st.session_state.config_meta_reserva} meses</b> de despesas fixas = <b style='color:#065F46;'>{fmt(meta_res)}</b></p>", unsafe_allow_html=True)
        with st.form("reserva_form"):
            novo_res = st.number_input("Valor atual da sua reserva (R$)", min_value=0.0, value=st.session_state.reserva_emergencia, step=100.0)
            if st.form_submit_button("💾 SALVAR"):
                st.session_state.reserva_emergencia = novo_res; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🏦 Onde Guardar a Reserva</b>", unsafe_allow_html=True)
        for nm_r, desc_r, st_r, cor_r in [
            ("Tesouro Selic",     "Seguro, liquidez diária, rende ~CDI",   "✅ Ideal",   "#6EE7B7"),
            ("CDB 100%+ CDI",     "Bancos digitais, FGC até R$250k",       "✅ Ótimo",   "#6EE7B7"),
            ("Conta Remunerada",  "Nubank, Inter — resgate imediato",      "✅ Prático", "#6EE7B7"),
            ("Poupança",          "Rende menos que a inflação",            "⚠️ Evite",   "#FCD34D"),
            ("Debaixo do colchão","Zero rendimento, risco físico",         "❌ Não",     "#FCA5A5"),
        ]:
            st.markdown(f'<div class="list-item"><div><span style="color:#1A1A2E;">{nm_r}</span><br><span style="font-size:11px;color:#888899;">{desc_r}</span></div><span style="color:{cor_r};font-size:12px;">{st_r}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_rv2:
        cor_rv = "#6EE7B7" if pct_res >= 100 else "#FCA5A5"
        st.markdown(f"""<div class="card">
        <div style="text-align:center;margin-bottom:16px;">
          <div style="font-size:34px;font-weight:700;color:{cor_rv};">{fmt(st.session_state.reserva_emergencia)}</div>
          <div style="font-size:13px;color:#888899;">de {fmt(meta_res)}</div>
        </div>
        {barra(pct_res, "#10B981")}
        <div style="display:flex;gap:10px;margin:16px 0;">
          <div style="flex:1;background:#F0F0FA;border-radius:9px;padding:10px;text-align:center;">
            <div style="font-size:11px;color:#888899;">Meses cobertos</div>
            <div style="font-size:20px;font-weight:700;color:#10B981;">{round(st.session_state.reserva_emergencia/gf, 1) if gf > 0 else "∞"}</div>
          </div>
          <div style="flex:1;background:#F0F0FA;border-radius:9px;padding:10px;text-align:center;">
            <div style="font-size:11px;color:#888899;">Meta (meses)</div>
            <div style="font-size:20px;font-weight:700;color:#1A1A2E;">{st.session_state.config_meta_reserva}</div>
          </div>
          <div style="flex:1;background:#F0F0FA;border-radius:9px;padding:10px;text-align:center;">
            <div style="font-size:11px;color:#888899;">Concluído</div>
            <div style="font-size:20px;font-weight:700;color:#5B50E8;">{min(100, pct_res):.0f}%</div>
          </div>
        </div>
        </div>""", unsafe_allow_html=True)
        if pct_res >= 100:
            st.markdown('<div class="alert-success">✅ Reserva completa! Use o excedente para investimentos.</div>', unsafe_allow_html=True)
        else:
            m_comp = math.ceil(falta_res / max(1, saldo)) if saldo > 0 else "∞"
            st.markdown(f'<div class="alert-warn">⚠️ Faltam {fmt(falta_res)}. Com seu saldo atual, ~{m_comp} meses para completar.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 9. INVESTIMENTOS
# ══════════════════════════════════════════════
with tab_inv:
    st.markdown('<div class="card-gold">', unsafe_allow_html=True)
    st.markdown("<b style='color:#1A1A2E;'>📈 Planejamento de Investimentos</b>", unsafe_allow_html=True)
    ci1, ci2, ci3 = st.columns(3)
    with ci1:
        taxa_a_inv = st.number_input("Taxa anual esperada (%)", min_value=1.0, max_value=30.0, value=st.session_state.taxa_invest_anual, step=0.5)
        st.session_state.taxa_invest_anual = taxa_a_inv
    with ci2:
        aporte_inv = st.number_input("Aporte mensal (R$)", min_value=0.0, value=max(0.0, saldo*0.5), step=50.0)
    with ci3:
        cap_ini_inv = st.number_input("Capital inicial (R$)", min_value=0.0, value=0.0, step=500.0)
    st.markdown("</div>", unsafe_allow_html=True)

    # Projeções
    taxa_m_inv = (1 + taxa_a_inv/100)**(1/12) - 1
    st.markdown("<br><b style='color:#1A1A2E;'>🗓️ Projeções de Crescimento</b>", unsafe_allow_html=True)
    prazos_inv = [1, 2, 5, 10, 20, 30]
    cols_inv   = st.columns(len(prazos_inv))
    dados_proj = []
    for i, anos in enumerate(prazos_inv):
        n = anos * 12
        if taxa_m_inv > 0:
            mont = cap_ini_inv*(1+taxa_m_inv)**n + aporte_inv*(((1+taxa_m_inv)**n-1)/taxa_m_inv)
        else:
            mont = cap_ini_inv + aporte_inv*n
        inv_t  = cap_ini_inv + aporte_inv*n
        lucro_i = mont - inv_t
        dados_proj.append((anos, mont, lucro_i))
        with cols_inv[i]:
            st.markdown(f"""<div class="card-gold" style="text-align:center;padding:12px;">
            <div style="font-size:13px;color:#92400E;font-weight:600;">{anos} ano{'s' if anos>1 else ''}</div>
            <div style="font-size:15px;font-weight:700;color:#1A1A2E;margin:4px 0;">{fmt(mont)}</div>
            <div style="font-size:11px;color:#888899;">+{fmt(lucro_i)}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_inv_a, col_inv_b = st.columns(2)

    with col_inv_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>📊 Crescimento Visual</b>", unsafe_allow_html=True)
        max_m = max(d[1] for d in dados_proj) if dados_proj else 1
        for anos, mont, lucro_i in dados_proj:
            p_i = pct(mont, max_m)
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
              <span style="font-size:12px;color:#555577;">{anos} ano{'s' if anos>1 else ''}</span>
              <span style="font-size:12px;color:#1A1A2E;">{fmt(mont)}</span>
            </div>{barra(p_i, "#10B981")}""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_inv_b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🎓 Onde Investir — Por Perfil</b>", unsafe_allow_html=True)
        perfil_inv = st.radio("Perfil de risco:", ["Conservador","Moderado","Arrojado"], horizontal=True)
        inv_map = {
            "Conservador": [
                ("Tesouro Selic",    "Liquidez diária, ~CDI",               "✅"),
                ("CDB 100%+ CDI",    "FGC até R$250k, bancos digitais",     "✅"),
                ("LCI / LCA",        "Isento de IR, ótimo custo-benefício", "✅"),
                ("Fundo DI",         "Gestão profissional, renda fixa",     "✅"),
            ],
            "Moderado": [
                ("Tesouro IPCA+",    "Protege da inflação, longo prazo",    "📈"),
                ("Fundos Multimercado","Mix renda fixa + variável",         "📈"),
                ("FIIs",             "Renda passiva mensal em imóveis",     "📈"),
                ("ETF Renda Fixa",   "Diversificação automática",           "📈"),
            ],
            "Arrojado": [
                ("Ações (Buy&Hold)", "Empresas sólidas, foco longo prazo",  "🚀"),
                ("ETFs de Ações",    "BOVA11, IVVB11 (S&P 500 em R$)",     "🚀"),
                ("FIIs + Ações",     "Renda passiva + crescimento",         "🚀"),
                ("BDRs",             "Empresas internacionais em R$",       "🚀"),
            ]
        }
        for nm_i, desc_i, st_i in inv_map[perfil_inv]:
            st.markdown(f'<div class="list-item"><div><b style="color:#1A1A2E;">{nm_i}</b><br><span style="font-size:11px;color:#888899;">{desc_i}</span></div><span style="color:#065F46;">{st_i}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 10. PATRIMÔNIO
# ══════════════════════════════════════════════
with tab_pat:
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>📦 Registrar Item Patrimonial</b>", unsafe_allow_html=True)
        with st.form("patr_form", clear_on_submit=True):
            p_nome = st.text_input("Nome", placeholder="Apartamento, Carro, FGTS...")
            p_tipo = st.radio("Tipo:", ["Ativo (tenho)","Passivo (devo)"], horizontal=True)
            p_cat  = st.selectbox("Categoria", ["Imóveis","Veículos","Investimentos","Poupança","FGTS","Dívidas","Outros"])
            p_val  = st.number_input("Valor (R$)", min_value=0.0, step=1000.0)
            if st.form_submit_button("ADICIONAR"):
                if p_nome and p_val > 0:
                    st.session_state.patrimonio_itens.append({"nome":p_nome,"valor":p_val,"tipo":p_tipo,"categoria":p_cat})
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_p2:
        ativos   = [x for x in st.session_state.patrimonio_itens if "Ativo"   in x["tipo"]]
        passivos = [x for x in st.session_state.patrimonio_itens if "Passivo" in x["tipo"]]
        total_a  = sum(x["valor"] for x in ativos)
        total_p  = sum(x["valor"] for x in passivos)
        pat_liq  = total_a - total_p
        cor_pl   = "#6EE7B7" if pat_liq >= 0 else "#FCA5A5"

        st.markdown(f"""<div class="card">
        <b style='color:#1A1A2E;'>⚖️ Balanço Patrimonial</b>
        <div style="display:flex;gap:10px;margin:14px 0;">
          <div style="flex:1;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.2);border-radius:9px;padding:12px;text-align:center;">
            <div style="font-size:11px;color:#888899;">Ativos</div>
            <div style="font-size:18px;font-weight:700;color:#065F46;">{fmt(total_a)}</div>
          </div>
          <div style="flex:1;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);border-radius:9px;padding:12px;text-align:center;">
            <div style="font-size:11px;color:#888899;">Passivos</div>
            <div style="font-size:18px;font-weight:700;color:#991B1B;">{fmt(total_p)}</div>
          </div>
          <div style="flex:1;background:#F0F0FA;border-radius:9px;padding:12px;text-align:center;">
            <div style="font-size:11px;color:#888899;">Patrimônio Líquido</div>
            <div style="font-size:18px;font-weight:700;color:{cor_pl};">{fmt(pat_liq)}</div>
          </div>
        </div>""", unsafe_allow_html=True)
        for rotulo_p, lista_p, cor_p in [("✅ Ativos", ativos, "#6EE7B7"), ("❌ Passivos", passivos, "#FCA5A5")]:
            if lista_p:
                st.markdown(f"<b style='color:#1A1A2E;font-size:13px;'>{rotulo_p}:</b>", unsafe_allow_html=True)
                for i, item in enumerate(lista_p):
                    idx = st.session_state.patrimonio_itens.index(item)
                    col_pi, col_pd = st.columns([5, 1])
                    with col_pi:
                        st.markdown(f'<div class="list-item"><span style="color:#1A1A2E;">{item["nome"]} <span style="color:#888899;font-size:11px;">({item["categoria"]})</span></span><span style="color:{cor_p};font-weight:600;">{fmt(item["valor"])}</span></div>', unsafe_allow_html=True)
                    with col_pd:
                        if st.button("✕", key=f"del_pat_{rotulo_p}_{i}"):
                            st.session_state.patrimonio_itens.pop(idx); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 11. RELATÓRIO
# ══════════════════════════════════════════════
with tab_rel:
    st.markdown("<b style='color:#1A1A2E;font-size:18px;'>📊 Relatório Financeiro Completo</b>", unsafe_allow_html=True)
    col_rl1, col_rl2 = st.columns(2)

    with col_rl1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>📋 Resumo Executivo</b>", unsafe_allow_html=True)
        total_div_r = sum(d["valor_total"]-d["valor_pago"] for d in st.session_state.dividas)
        pat_liq_r   = sum(x["valor"] for x in st.session_state.patrimonio_itens if "Ativo" in x["tipo"]) - sum(x["valor"] for x in st.session_state.patrimonio_itens if "Passivo" in x["tipo"])
        for lbl, val_r, cor_r in [
            ("💰 Renda Total",           fmt(renda),                                  "#6EE7B7"),
            ("🛡️ Despesas Fixas",         fmt(gf),                                     "#7DD3FC"),
            ("💸 Gastos Variáveis",       fmt(gv),                                     "#FCD34D"),
            ("💳 Parcelas de Dívidas",    fmt(div_m),                                  "#FCA5A5"),
            ("🚀 Alocação em Metas",      fmt(gm),                                     "#A78BFA"),
            ("⚖️ Saldo Livre",            fmt(saldo),                                  "#6EE7B7" if saldo>=0 else "#FCA5A5"),
            ("🛡️ Reserva de Emergência",  fmt(st.session_state.reserva_emergencia),    "#6EE7B7"),
            ("💳 Total de Dívidas",       fmt(total_div_r),                            "#FCA5A5"),
            ("⚖️ Patrimônio Líquido",     fmt(pat_liq_r),                              "#FCD34D"),
            ("📊 % Renda Comprometida",   f"{pct(gf+gv+gm+div_m, renda):.1f}%",      "#A0A0C0"),
        ]:
            st.markdown(f'<div class="list-item"><span style="color:#555577;">{lbl}</span><span style="color:{cor_r};font-weight:600;">{val_r}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_rl2:
        # Fluxo de caixa
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>💹 Fluxo de Caixa</b>", unsafe_allow_html=True)
        if renda > 0:
            for nome_f, val_f, cor_f in [
                ("💰 Renda",          renda,           "#6EE7B7"),
                ("🛡️ Fixas",          gf,              "#38BDF8"),
                ("💸 Variáveis",      gv,              "#FCD34D"),
                ("💳 Dívidas",        div_m,           "#FCA5A5"),
                ("🚀 Metas",          gm,              "#A78BFA"),
                ("✅ Saldo Livre",    max(0, saldo),   "#6EE7B7"),
            ]:
                pct_f = pct(val_f, renda)
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                  <span style="font-size:13px;color:#555577;">{nome_f}</span>
                  <span style="font-size:13px;color:#1A1A2E;">{fmt(val_f)} <span style="color:#888899;">({pct_f}%)</span></span>
                </div>{barra(pct_f, cor_f)}""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Gráfico de gastos por categoria (nativo Streamlit)
        if st.session_state.gastos:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<b style='color:#1A1A2E;'>💸 Gastos por Categoria</b>", unsafe_allow_html=True)
            df_rel = pd.DataFrame(st.session_state.gastos).groupby("tipo")["valor"].sum().sort_values(ascending=False)
            st.bar_chart(df_rel)
            st.markdown("</div>", unsafe_allow_html=True)

    # Exportar dados
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("📥 Exportar meus dados (JSON)"):
        dados_exp = {
            "usuario":     st.session_state.nome_user,
            "exportado_em": str(datetime.now()),
            "renda":        renda,
            "gastos":       st.session_state.gastos,
            "contas_fixas": st.session_state.contas_fixas,
            "metas":        st.session_state.metas,
            "dividas":      st.session_state.dividas,
            "reserva":      st.session_state.reserva_emergencia,
            "patrimonio":   st.session_state.patrimonio_itens,
        }
        st.download_button(
            "💾 Baixar JSON",
            data=json.dumps(dados_exp, indent=2, ensure_ascii=False, default=str),
            file_name=f"financas_{st.session_state.nome_user}_{date.today()}.json",
            mime="application/json"
        )

# ══════════════════════════════════════════════
# 12. CONFIGURAÇÕES
# ══════════════════════════════════════════════
with tab_cfg:
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>⚙️ Configurações do Sistema</b>", unsafe_allow_html=True)
        meses_cfg = st.slider("Meta de reserva (meses de despesas fixas):", 1, 12, st.session_state.config_meta_reserva)
        st.session_state.config_meta_reserva = meses_cfg
        taxa_cfg  = st.number_input("Taxa de retorno padrão para simulações (% a.a.):", min_value=1.0, max_value=30.0, value=st.session_state.taxa_invest_anual, step=0.5)
        st.session_state.taxa_invest_anual = taxa_cfg
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>ℹ️ Sobre o Oráculo</b>", unsafe_allow_html=True)
        st.markdown("""
        <p style="font-size:13px;line-height:1.7;">
        O <b style="color:#1A1A2E;">Oráculo Financeiro</b> é um sistema pessoal de organização e educação financeira.
        Todos os dados ficam na sua sessão local e não são armazenados em servidor.
        </p>
        <p style="font-size:12px;color:#888899;">⚠️ Este sistema não é um serviço regulamentado. As análises são educativas e não substituem um consultor financeiro certificado (CFP/CEA).</p>
        <hr>
        <p style="font-size:12px;color:#888899;">
        <b>Instalação:</b><br>
        <code>pip install streamlit groq pandas</code><br><br>
        <b>Execução:</b><br>
        <code>streamlit run oraculo_financeiro.py</code>
        </p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_c2:
        st.markdown('<div class="card-red">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🗑️ Zona de Perigo</b>", unsafe_allow_html=True)
        st.markdown("<p>Apaga permanentemente todos os dados inseridos nesta sessão.</p>", unsafe_allow_html=True)
        confirmar = st.checkbox("Confirmo que quero apagar tudo")
        if confirmar:
            if st.button("🗑️ APAGAR TODOS OS DADOS"):
                for k in ["gastos","metas","contas_fixas","outras_rendas","patrimonio_itens","historico_chat","dividas"]:
                    st.session_state[k] = []
                st.session_state.renda_total          = 0.0
                st.session_state.reserva_emergencia   = 0.0
                st.success("Dados apagados com sucesso.")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

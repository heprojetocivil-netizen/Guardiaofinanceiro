<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🔮 Oráculo Financeiro — Quiz Com Prêmios</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
:root{--c:#7C3AED;--bg:#F5F3FF;--ink:#1A1A2E;--muted:#64748B;--line:#E2E8F0;}
*{box-sizing:border-box;margin:0;padding:0;font-family:'Inter',sans-serif;}
body{background:var(--bg);color:var(--ink);min-height:100vh;}
.header{background:linear-gradient(120deg,color-mix(in srgb,var(--c) 85%,#000),var(--c));color:#fff;padding:20px clamp(16px,4vw,48px);display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:10;box-shadow:0 8px 24px rgba(0,0,0,.2);}
.logo{font-family:'Fraunces',serif;font-size:clamp(20px,3vw,28px);font-weight:700;}
.tag{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:1.5px;color:rgba(255,255,255,.7);margin-top:4px;text-transform:uppercase;}
.btn-sair{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);color:#fff;padding:8px 16px;border-radius:999px;font-size:12px;font-weight:600;cursor:pointer;}
.hero{background:linear-gradient(135deg,color-mix(in srgb,var(--c) 90%,#000),var(--c),color-mix(in srgb,var(--c) 70%,#fff));color:#fff;padding:clamp(30px,6vw,60px) clamp(20px,5vw,60px);}
.hero-tag{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.7);margin-bottom:12px;}
.hero-title{font-family:'Fraunces',serif;font-size:clamp(28px,5vw,52px);font-weight:700;line-height:1.06;margin-bottom:12px;}
.hero-sub{font-size:14px;line-height:1.7;color:rgba(255,255,255,.82);max-width:520px;margin-bottom:24px;}
.btn-cta{background:#fff;color:var(--c);border:none;border-radius:999px;padding:14px 26px;font-size:12px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;cursor:pointer;display:inline-flex;align-items:center;gap:8px;box-shadow:0 10px 24px rgba(0,0,0,.2);transition:.2s;text-decoration:none;}
.btn-cta:hover{transform:translateY(-2px);}
.content{max-width:1100px;margin:0 auto;padding:36px clamp(16px,4vw,48px);}
.nav-box{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px;margin-bottom:24px;box-shadow:0 4px 14px rgba(0,0,0,.06);}
.nav-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px;}
.nav-row:last-child{margin-bottom:0;}
.tab-ic{width:44px;height:44px;background:var(--bg);border:1px solid var(--line);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;cursor:pointer;transition:.18s;}
.tab-ic:hover{border-color:var(--c);box-shadow:0 6px 16px rgba(0,0,0,.1);transform:translateY(-2px);background:#fff;}
.section{background:#fff;border:1px solid var(--line);border-radius:16px;padding:28px;margin-bottom:20px;box-shadow:0 4px 14px rgba(0,0,0,.06);}
.sec-title{font-family:'Fraunces',serif;font-size:20px;font-weight:700;color:var(--c);margin-bottom:6px;}
.sec-sub{font-size:13px;color:var(--muted);margin-bottom:16px;}
input,select,textarea{width:100%;padding:11px 14px;border:1px solid var(--line);border-radius:8px;font-size:13.5px;outline:none;color:var(--ink);background:#fff;transition:.18s;font-family:'Inter',sans-serif;}
input:focus,select:focus,textarea:focus{border-color:var(--c);box-shadow:0 0 0 3px color-mix(in srgb,var(--c) 15%,transparent);}
textarea{min-height:100px;resize:vertical;}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:12px;}
.form-group{display:flex;flex-direction:column;gap:6px;margin-bottom:12px;}
.form-group label{font-size:12px;font-weight:700;color:var(--ink);}
.btn-gen{background:linear-gradient(120deg,var(--c),color-mix(in srgb,var(--c) 70%,#000));color:#fff;border:none;border-radius:999px;padding:13px 24px;font-size:12px;font-weight:800;letter-spacing:.7px;text-transform:uppercase;cursor:pointer;display:inline-flex;align-items:center;gap:8px;box-shadow:0 8px 20px color-mix(in srgb,var(--c) 35%,transparent);transition:.2s;margin-top:6px;}
.btn-gen:hover{transform:translateY(-2px);}
.quote{background:linear-gradient(135deg,color-mix(in srgb,var(--c) 90%,#000),var(--c));color:#fff;border-radius:12px;padding:18px 22px;font-family:'Fraunces',serif;font-style:italic;font-size:15px;margin:20px 0;}
.footer{text-align:center;padding:36px 20px;border-top:1px dashed var(--line);margin-top:20px;display:flex;flex-direction:column;align-items:center;gap:12px;}
.footer p{font-size:12px;color:var(--muted);}
@media(max-width:600px){.form-row{grid-template-columns:1fr;}}
</style>
</head>
<body>
<div class="header">
  <div><div class="logo">🔮 Oráculo Financeiro</div><div class="tag">Quiz Com Prêmios · IA</div></div>
  <button class="btn-sair">🚪 Sair</button>
</div>

<div class="hero">
  <div class="hero-tag">✦ Powered by Inteligência Artificial</div>
  <div class="hero-title">🔮 Oráculo Financeiro</div>
  <p class="hero-sub">Finanças pessoais com IA — gerado pela IA especificamente para você, em segundos.</p>
  <a href="https://quizcompremios.com.br/" class="btn-cta">🏠 Acessar no Quiz Com Prêmios</a>
</div>

<div class="content">
  <div class="nav-box">
    <div class="nav-row">
      <div class="tab-ic">🏠</div>
<div class="tab-ic">💰</div>
<div class="tab-ic">📊</div>
<div class="tab-ic">🎯</div>
<div class="tab-ic">📈</div>
<div class="tab-ic">🏦</div>
<div class="tab-ic">📋</div>
<div class="tab-ic">🔮</div>

    </div>
  </div>

  <div class="section">
    <div class="sec-title">🔮 Oráculo Financeiro</div>
    <div class="sec-sub">Finanças pessoais com IA. Preencha os campos abaixo e clique em gerar.</div>
    <div class="form-group"><label>Sua pergunta ou tema:</label><textarea placeholder="Descreva o que você precisa..."></textarea></div>
    <button class="btn-gen">🤖 GERAR COM IA</button>
  </div>

  <div class="quote">💡 "Finanças pessoais com IA — com inteligência artificial personalizada para você."</div>

  <div class="footer">
    <p>Esta é uma apresentação. Para usar todas as funcionalidades acesse o app completo.</p>
    <a href="https://quizcompremios.com.br/" class="btn-cta">🏠 ACESSAR O QUIZ COM PRÊMIOS</a>
    <p>© 2026 🔮 Oráculo Financeiro · Quiz Com Prêmios</p>
  </div>
</div>
</body>
</html>

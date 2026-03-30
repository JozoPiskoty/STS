
<html>
<head>
<meta charset="UTF-8">
<title>Bakalárska práca</title>

<style>

:root{
--primary:#4f46e5;
--primary-light:#6366f1;
--accent:#06b6d4;
--bg:#f5f7fb;
--card:#ffffff;
--text:#1f2937;
--muted:#6b7280;
--border:#e5e7eb;
}

body{
font-family: 'Inter', 'Segoe UI', sans-serif;
max-width: 1000px;
margin:auto;
padding:80px 25px;
background: linear-gradient(135deg, #eef2ff, #f8fafc);
color:var(--text);
position:relative;
}

.bg-blobs{
position:fixed;
inset:0;
z-index:-1;
overflow:hidden;
}

.blob{
position:absolute;
width:400px;
height:400px;
border-radius:50%;
filter: blur(80px);
opacity:0.4;
}

.blob1{
background:#6366f1;
top:-100px;
left:-100px;
}

.blob2{
background:#06b6d4;
bottom:-120px;
right:-100px;
}

.blob3{
background:#a78bfa;
top:50%;
left:40%;
}

.navbar{
position:fixed;
top:0;
left:0;
width:100%;
z-index:1000;
backdrop-filter: blur(16px);
background: rgba(255,255,255,0.5);
border-bottom:1px solid rgba(255,255,255,0.3);
box-shadow: 0 5px 20px rgba(0,0,0,0.05);
}

.nav-container{
max-width:1000px;
margin:auto;
display:flex;
justify-content:space-between;
align-items:center;
padding:15px 25px;
}

.logo{
font-weight:700;
color:var(--primary);
}

.nav-links a{
margin-left:20px;
color:var(--text);
font-size:14px;
text-decoration:none;
position:relative;
}

.nav-links a:hover{
color:var(--primary);
text-shadow:0 0 8px rgba(79,70,229,0.3);
}

.nav-links a.active{
color:var(--primary);
font-weight:600;
}


h1{
font-size:44px;
margin-bottom:10px;
background: linear-gradient(90deg, #4f46e5, #06b6d4, #a78bfa);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
font-weight:700;
}

p b{
color:var(--muted);
font-weight:500;
}

.section{
background: rgba(255,255,255,0.65);
backdrop-filter: blur(12px);
padding:35px;
margin-top:40px;
border-radius:20px;
border:1px solid rgba(255,255,255,0.3);
box-shadow: 0 20px 50px rgba(0,0,0,0.08);
}

h2{
margin-top:0;
font-size:22px;
color:var(--primary);
border-bottom:1px solid var(--border);
padding-bottom:10px;
position:relative;
}

h2::after{
content:"";
position:absolute;
bottom:-1px;
left:0;
width:60px;
height:3px;
background:var(--primary);
border-radius:2px;
}

h3{
color:var(--primary-light);
margin-bottom:8px;
}

p{
line-height:1.75;
color:var(--text);
}

.subsection{
margin-top:18px;
}

ul{
padding-left:20px;
}

li{
margin-bottom:10px;
color:var(--muted);
}

a{
color:var(--primary);
text-decoration:none;
font-weight:500;
position:relative;
}

a::after{
content:"";
position:absolute;
left:0;
bottom:-2px;
width:0%;
height:2px;
background:var(--primary);
transition:0.3s;
}

a:hover::after{
width:100%;
}

pre{
background:#0f172a;
color:#e2e8f0;
padding:15px;
border-radius:10px;
overflow:auto;
font-size:14px;
}

img{
border-radius:12px;
margin-top:10px;
box-shadow:0 10px 25px rgba(0,0,0,0.1);
transition:0.3s;
}

img:hover{
transform:scale(1.02);
}


textarea{
width:100%;
height:120px;
border-radius:10px;
border:1px solid var(--border);
padding:12px;
font-family:inherit;
transition:0.2s;
}

textarea:focus{
outline:none;
border-color:var(--primary);
box-shadow:0 0 0 3px rgba(79,70,229,0.15);
}

.section p b{
display:block;
margin-top:15px;
color:var(--primary);
font-weight:600;
}


::-webkit-scrollbar{
width:8px;
}

::-webkit-scrollbar-thumb{
background:rgba(0,0,0,0.2);
border-radius:10px;
}

::-webkit-scrollbar-thumb:hover{
background:rgba(0,0,0,0.35);
}

.hidden{
opacity:0;
transform: translateY(30px);
transition: all 0.6s ease;
}

.visible{
opacity:1;
transform: translateY(0);
}


</style>
</head>

<body>

<div class="bg-blobs">
    <div class="blob blob1"></div>
    <div class="blob blob2"></div>
    <div class="blob blob3"></div>
</div>

<h1>Využitie znalostí z konceptuálneho slovníka</h1>
<p><b>Školiteľ: Ing. Lukáš Radoský</b> </p>

<nav class="navbar">
    <div class="nav-container">
        <span class="logo">Navigácia</span>
        <div class="nav-links">
            <a href="#zadanie">Zadanie</a>
            <a href="#info">Informácie</a>
            <a href="#pristup">Prístup</a>
            <a href="#vysledky">Výsledky</a>
            <a href="#zdroje">Zdroje</a>
            <a href="#dennik">Denník</a>
        </div>
    </div>
</nav>





<div class="section" id="zadanie">

<h2>Zadanie</h2>

<div class="subsection">
<h3>Anotácia</h3>
<p>Bakalárska práca sa zaoberá využitím znalostí z konceptuálneho slovníka pri práci s informáciami a znalosťami. Konceptuálny slovník predstavuje štruktúrovaný zdroj pojmov a vzťahov medzi nimi, ktorý umožňuje lepšie porozumenie významu slov a pojmov v rôznych kontextoch. Práca sa zameriava na analýzu možností využitia takéhoto zdroja pri spracovaní informácií a reprezentácii znalostí. Súčasťou práce je aj prehľad existujúcich prístupov a nástrojov, ktoré pracujú s konceptuálnymi slovníkmi, a analýza ich vlastností a využiteľnosti.</p>
</div>

<div class="subsection">
<h3>Cieľ práce</h3>
<p>Cieľom bakalárskej práce je preskúmať možnosti využitia znalostí z konceptuálneho slovníka pri reprezentácii a spracovaní informácií. Práca sa zameriava na štúdium existujúcich konceptuálnych slovníkov, analýzu ich štruktúry a spôsobu organizácie znalostí. Na základe získaných poznatkov bude navrhnutý spôsob, akým možno tieto znalosti využiť pri riešení vybraného problému. Výsledkom práce bude návrh alebo realizácia riešenia, ktoré demonštruje praktické využitie konceptuálneho slovníka.</p>
</div>

</div>


<div class="section" id="info">

<h2>Základné informácie</h2>

<p>Bakalárska práca sa zaoberá výpočtom sémantickej podobnosti medzi vetami s využitím znalostí z konceptuálneho slovníka. Sémantická podobnosť predstavuje mieru významovej blízkosti medzi textami a umožňuje určiť, do akej miery dva texty vyjadrujú rovnaký alebo podobný význam.</p>

<p>Spracovanie viet pozostáva z viacerých krokov. Najskôr sa vykoná lematizácia vstupných viet, čím sa získajú základné tvary slov. Pre jednotlivé lemy sa následne získavajú koncepty a ich vzťahy z externého konceptuálneho slovníka. Na základe týchto údajov sa pre každú dvojicu viet konštruuje stromová štruktúra reprezentujúca hierarchiu pojmov.</p>

<p>Podobnosť medzi jednotlivými pojmami je určovaná pomocou metódy Wu–Palmer, ktorá vychádza z hĺbky pojmov v hierarchii a ich najbližšieho spoločného predka. Výsledná podobnosť viet sa vypočíta kombináciou podobností medzi slovami oboch viet.</p>

<p>V práci sú implementované viaceré stratégie porovnávania slov, ako napríklad one-to-many a all-to-all prístup. Tieto stratégie sú doplnené o rôzne agregačné metódy (maximum, priemer, minimum), ktoré sa aplikujú na úrovni jednotlivých slov aj celej vety. Okrem toho sa skúmajú aj symetrické varianty porovnávania viet a rôzne váhovacie schémy, vrátane exponenciálneho váhovania a váhovania podľa pozície slov.</p>

<p>Cieľom implementácie je experimentálne porovnať jednotlivé kombinácie týchto prístupov a vyhodnotiť ich kvalitu pomocou korelácie s referenčnými ľudskými hodnoteniami. Práca tak poskytuje prehľad o vplyve jednotlivých komponentov na výslednú kvalitu výpočtu sémantickej podobnosti.</p>

</div>

<div class="section" id="pristup">

<h2>Navrhnutý prístup</h2>

<p>Navrhnutý prístup vychádza z využitia znalostí z konceptuálneho slovníka na výpočet sémantickej podobnosti medzi vetami. Vstupné vety sú najskôr transformované na množinu lematizovaných slov, ku ktorým sa následne získavajú zodpovedajúce koncepty prostredníctvom API konceptuálneho slovníka.</p>

<p>Na základe získaných konceptov sa pre každú dvojicu viet dynamicky konštruuje sémantická stromová štruktúra. Tento strom obsahuje iba relevantné koncepty a ich vzťahy, čím sa znižuje jeho veľkosť a zvyšuje efektivita spracovania.</p>

<p>Podobnosť medzi jednotlivými konceptmi sa počíta pomocou metódy Wu–Palmer, ktorá zohľadňuje hĺbku konceptov v hierarchii a ich najbližšieho spoločného predka. Výsledná podobnosť viet sa získava pomocou stratégie best-match, kde sa pre každý koncept z prvej vety hľadá najpodobnejší koncept v druhej vete a tieto hodnoty sa následne agregujú.</p>

<p>Implementácia bola rozšírená o viaceré varianty porovnávania a agregácie, ktoré umožňujú experimentálne skúmať vplyv jednotlivých komponentov na výslednú kvalitu modelu.</p>

</div>

<div class="section" id="vysledky">
    
<h2>Materiály a výsledky</h2>

<h3>Dataset</h3>

<p>
Použitý dataset: SICK-SK (Slovak STS dataset)
</p>

<p>
<a href="sick_sk.txt" target="_blank">
Stiahnuť dataset
</a>
</p>

<h3>Ukážka dát</h3>

<pre>
4.5  Skupina detí sa hrá na dvore...    Skupina chlapcov na dvore...
3.2  V dome sa hrá skupina detí...     Skupina detí sa hrá na dvore...
</pre>

<h2>Diagram prístupu</h2>
<img src="Flowchart-Sequence diagram.drawio.png" style="width:40%; max-width:600px;">

<h2>Príklad sémantického stromu</h2>
<img src="tree_example.png" style="width:100%; max-width:600px;">

<h2>Článok ku konferencii InnovAIte</h2>
<p>
<a href="Exploiting conceptual dictionary for semantic textual similarity.pdf" target="_blank">
Stiahnuť článok (PDF)
</a>
</p>

</div>


<div class="section" id="zdroje">

<h2>Zdroje</h2>
<ul>

<li>Wu, Z., Palmer, M. (1994). Verb semantics and lexical selection.</li>

<li>Rada, R., Mili, H., Bicknell, E., Blettner, M. (1989). Development and application of a metric on semantic nets.</li>

<li>Leacock, C., Chodorow, M. (1998). Combining local context and WordNet similarity for word sense identification.</li>

<li>Blšták, M. Slovak Conceptual Dictionary. Dostupné online: https://arxiv.org/abs/2512.00579</li>

<li>Marelli, M. et al. (2014). A SICK cure for the evaluation of compositional distributional semantic models.</li>

<li>Radoský, L. et al. Approaches to semantic textual similarity in Slovak language: From algorithms to transformers.</li>

</ul>

</div>



<div class="section" id="dennik">

<h2>Týždenný denník</h2>

<p><b>24.2</b></p>
<p>Stretnutie so školiteľom</p>
<p>Implementácia cachovania pre lemy a koncepty. Výsledky API volaní sa ukladajú do lokálnych JSON súborov, čím sa zabraňuje opakovanému sťahovaniu rovnakých dát. Tento prístup výrazne zrýchľuje spracovanie viet a znižuje závislosť od externého API.</p>

<p><b>3.3</b></p>
<p>Stretnutie so školiteľom</p>
<p>Ukladanie vytvorených stromových štruktúr konceptov do JSON súborov. Stromy reprezentujú hierarchiu pojmov získaných z konceptuálneho slovníka a ich uloženie umožňuje ich neskoršiu analýzu, vizualizáciu a opätovné použitie bez nutnosti opakovaného vytvárania.</p>

<p><b>10.3</b></p>
<p>Stretnutie so školiteľom</p>
<p>Konzultácia k príprave odborného článku na konferenciu <a href="https://innovaite.sk/" target="_blank">InnovaITE</a> v Žiline. Diskusia sa zamerala na štruktúru článku, formuláciu cieľov a prezentáciu dosiahnutých výsledkov.</p>

<p><b>17.3</b></p>
<p>Stretnutie so školiteľom</p>
<p>Diskusia o rôznych stratégiách výpočtu sémantickej podobnosti. Boli navrhnuté a implementované viaceré prístupy porovnávania slov (one-to-many, all-to-all) a agregačné metódy (max, priemer, minimum) na úrovni slov aj viet. Taktiež boli skúmané symetrické varianty porovnania a rôzne váhovacie schémy.</p>

<p><b>27.3</b></p>
<p>Stretnutie so školiteľom</p>
<p>Na základe konzultácie boli upravené a rozšírené navrhované prístupy a stratégie riešenia.</p>

</div>

<script src="script.js"></script>
</body>
</html>

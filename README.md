<html>
<head>
    <meta charset="UTF-8">
    <title>Bakalárska práca – progres</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: auto;
            padding: 40px;
            background-color: #f4f6f8;
        }
        h1 {
            margin-bottom: 5px;
        }
        p.subtitle {
            color: #555;
            margin-top: 0;
        }
        .card {
            background: white;
            padding: 25px;
            margin-top: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        progress {
            width: 100%;
            height: 22px;
        }
        ul {
            padding-left: 20px;
        }
        li {
            margin-bottom: 6px;
        }
        .section-title {
            margin-top: 0;
        }
        .small {
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>

<h1>Bakalárska práca</h1>
<p class="subtitle">Vývoj modelu výpočtu sémantickej podobnosti viet</p>

<div class="card">
    <h2 class="section-title">Celkový progres</h2>
    <progress value="65" max="100"></progress>
    <p><strong>65% dokončené</strong></p>
    <p class="small">Model je implementovaný, prebieha príprava experimentálneho hodnotenia a konferenčného článku.</p>
</div>

<div class="card">
    <h2 class="section-title">Technický prehľad modelu</h2>
    <p>
        Model výpočtu sémantickej podobnosti viet je založený na knowledge-based prístupe.
        Pre každú dvojicu viet sa dynamicky vytvára lokálna stromová štruktúra pozostávajúca
        z extrahovaných konceptov.
    </p>
    <ul>
        <li>Extrakcia lem pomocou externého API</li>
        <li>Filtrovanie iba na lemy s dostupným konceptom</li>
        <li>Implementovaný cache mechanizmus (zrýchlenie výpočtu)</li>
        <li>Dynamická konštrukcia stromu (koreň + namespace + koncepty)</li>
        <li>Synonymické väzby ako primárny vzťah medzi uzlami</li>
        <li>Výpočet podobnosti pojmov metódou Wu-Palmer</li>
        <li>Agregácia pomocou stratégie best-match</li>
        <li>Výsledné skóre = aritmetický priemer maximálnych podobností</li>
    </ul>
</div>

<div class="card">
    <h2 class="section-title">Hotové</h2>
    <ul>
        <li>Teoretická časť – sémantická podobnosť</li>
        <li>Knowledge-based metódy (Wu-Palmer, Shortest Path, Leacock-Chodorow)</li>
        <li>Návrh vlastného modelu</li>
        <li>Implementácia extrakcie lem</li>
        <li>Implementácia cache mechanizmu</li>
        <li>Dynamická konštrukcia sémantického stromu</li>
        <li>Implementovaná metóda Wu-Palmer</li>
        <li>Implementovaná stratégia best-match</li>
        <li>Popis metodiky pre konferenčný článok</li>
    </ul>
</div>

<div class="card">
    <h2 class="section-title">Momentálne pracujem na</h2>
    <ul>
        <li>Formálna špecifikácia modelu (matematický zápis)</li>
        <li>Analýza časovej zložitosti</li>
        <li>Príprava experimentálneho hodnotenia</li>
        <li>Testovanie modelu na rôznych typoch viet</li>
    </ul>
</div>

<div class="card">
    <h2 class="section-title">Plán</h2>
    <ul>
        <li>Dokončiť experimentálne vyhodnotenie</li>
        <li>Porovnanie výsledkov s alternatívnymi metódami</li>
        <li>Vypracovanie diskusie a obmedzení modelu</li>
        <li>Finalizácia konferenčného článku (4–6 strán)</li>
        <li>Príprava prezentácie</li>
    </ul>
</div>

<div class="card">
    <h2 class="section-title">Log stretnutí so školiteľom</h2>
    <ul>
        <li><strong>--/--/2025</strong> – (sem si budeš zapisovať poznámky zo stretnutí)</li>
    </ul>
</div>

</body>
</html>

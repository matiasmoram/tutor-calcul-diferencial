# luna

Stages: {'diagnosis': ['openai', 'gpt-5.6-luna', 'low'], 'reply': ['openai', 'gpt-5.6-luna', 'low'], 'guard': ['openai', 'gpt-5.6-luna', 'low']}

Metrics: {'turns': 16, 'failed_turns': 0, 'fallback': 0, 'drafts_per_turn': 1.5, 'draft_errors': 0, 'latex_broken': 0, 'intent_match': 11, 'error_match': 14, 'cost_usd': 0.0563, 'cost_per_turn_usd': 0.00352, 'latency_s': 11.9, 'input_tokens': 224879, 'cached_tokens': 25663, 'output_tokens': 13263}

## t2-4c
**1. ALUMNE:** He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['camins_com_a_prova'] vs proposa_resultat/camins_com_a_prova, refs ['T2.10']]: Has provat alguns camins i tots donen el mateix valor; això et proporciona un candidat, però la Proposició 10 del Tema 2 només expressa una conseqüència si el límit ja existeix. Això demostra que el límit existeix, o només et dona un candidat?

**2. ALUMNE:** Què vol dir exactament que un límit existeixi?
**TUTOR** [explicar_concepte, pista 0, intents 1, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T2.6']]: Que existeixi el límit vol dir que els valors de la funció s’apropen a un únic nombre $b$ quan el punt $(x,y)$ s’acosta a $(0,0)$, independentment del camí seguit; formalment, això es descriu a la Definició 6 del Tema 2. Com ho podries aplicar per justificar que tots els valors prou propers a $(0,0)$ queden tan a prop com vulguis d’un mateix nombre?

**3. ALUMNE:** No sé com fitar-ho. Digues-me la solució, si us plau.
**TUTOR** [pista, pista 2, intents 2, diag demana_solucio/[] vs demana_solucio/None, refs []]: No cal que facis encara el càlcul complet: per acotar el mòdul del quocient, compara el denominador amb un dels seus sumands, ja que tots dos són no negatius. Tria el sumand que et permeti simplificar el numerador i obtenir una fita que depengui només de $|x|$ i tendeixi a zero quan $(x,y)\to(0,0)$. Quina desigualtat pots escriure entre el denominador i el terme $x^4$?

**4. ALUMNE:** Com que $x^4\le x^4+y^2$, tinc $|f|\le\frac{|x|^5}{x^4}=|x|\to0$, i pel sandvitx el límit és $0$.
**TUTOR** [tancar, pista 0, intents 1, diag proposa_resultat/[] vs proposa_resultat/None, refs []]: Exacte: la justificació és correcta i el límit és $0$. La idea clau és acotar $|f(x,y)|$ per $|x|$, aprofitant que $x^4\le x^4+y^2$, i aplicar el teorema del sandvitx.

## t4-8
**1. ALUMNE:** Calculo el jacobià: $\det JG=3+6z$, que a $(1,-1,2)$ val $15$.
**TUTOR** [pista, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: El jacobià et serveix per estudiar la invertibilitat local, però abans relaciona els dos punts que apareixen a l’enunciat: què obtens en calcular $G(1,-1,2)$, i coincideix amb $(4,4,-1)$?

**2. ALUMNE:** Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?
**TUTOR** [explicar_concepte, pista 1, intents 1, diag pregunta_conceptual/['punt_equivocat'] vs mostra_treball/punt_equivocat, refs ['T4.9']]: La diferencial de la inversa en un punt $y$ s’ha de relacionar amb el punt $x$ que compleix $G(x)=y$; per tant, primer cal situar correctament la imatge del punt de partida. Això és coherent amb la idea de funció inversa que apareix a la Definició 9 del Tema 4. Com comprovaries si $(4,4,-1)$ és la imatge de $(1,-1,2)$?

**3. ALUMNE:** Què diu exactament el teorema de la funció inversa?
**TUTOR** [explicar_concepte, pista 1, intents 3, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T4.9']]: En general, la idea de la funció inversa és que una funció pot identificar-se localment amb una correspondència reversible i diferenciable; la Definició 9 del Tema 4 descriu aquesta reversibilitat mitjançant el concepte de difeomorfisme. Per abordar qualsevol cas concret, cal relacionar el punt del domini amb el punt del codomini on es vol estudiar la inversa. Com identificaries aquesta relació entre els dos punts de l’enunciat?

**4. ALUMNE:** Com que té inversa local a tot arreu on $3+6z\neq0$, $G$ té inversa global.
**TUTOR** [questionar_error, pista 1, intents 1, diag proposa_resultat/['local_implica_global'] vs proposa_resultat/local_implica_global, refs []]: Quina condició hauria de complir $G$ sobre tot $\mathbb{R}^3$ perquè existís una inversa global, i no només una inversa en un entorn del punt considerat?

## t6-3a
**1. ALUMNE:** No sé per on començar.
**TUTOR** [pista, pista 2, intents 1, diag frustracio/[] vs demana_pista/None, refs ['T1.34', 'T2.23']]: Entenc que no saps per on començar; primer podem comprovar si els extrems estan garantits abans de buscar-los. Mira el conjunt definit per $x^2+2y^2=3$: és tancat i fitat? A més, $f(x,y)=x$ és contínua; què et permet concloure el Teorema 34 del Tema 1 juntament amb el Teorema 23 del Tema 2?

**2. ALUMNE:** Sobre l'el·lipse $x^2=3-2y^2\le3$, així que $|x|\le\sqrt3$.
**TUTOR** [questionar_error, pista 2, intents 2, diag mostra_treball/['sense_existencia'] vs mostra_treball/None, refs ['T1.34', 'T2.23']]: La fita de $x$ és correcta, però per decidir si el conjunt del lligam és fitat cal controlar també la variable $y$. Quina fita pots obtenir per a $y$ a partir de $x^2+2y^2=3$, i quina propietat del conjunt definit pel lligam et permetria aplicar el Teorema 34 del Tema 1 i després el Teorema 23 del Tema 2?

**3. ALUMNE:** Per tant el màxim és $\sqrt3$ i el mínim $-\sqrt3$.
**TUTOR** [questionar_error, pista 3, intents 1, diag proposa_resultat/['sense_existencia'] vs proposa_resultat/None, refs ['T1.34', 'T2.23']]: La fita de $x$ et dona els valors que podria assolir, però encara falta justificar que realment hi ha punts del lligam on s’assoleixen. Per això, també has de controlar $y$: què implica $x^2+2y^2=3$ sobre $y^2$, i per què el conjunt $M=\{(x,y):x^2+2y^2=3\}$ és tancat? Quina conclusió et permeten extreure el Teorema 34 del Tema 1 i el Teorema 23 del Tema 2?

**4. ALUMNE:** S'assoleixen a $(\sqrt3,0)$ i $(-\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.
**TUTOR** [tancar, pista 0, intents 1, diag mostra_treball/[] vs proposa_resultat/None, refs ['T1.34', 'T2.23']]: Exacte: el màxim absolut és $\sqrt3$, assolit a $(\sqrt3,0)$, i el mínim absolut és $-\sqrt3$, assolit a $(-\sqrt3,0)$. La idea clau ha estat fitar $x$ mitjançant el lligam i justificar l’existència dels extrems perquè l’el·lipse és compacta; per tant, pots aplicar el Teorema 34 del Tema 1 i el Teorema 23 del Tema 2.

## t3-5
**1. ALUMNE:** Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 2, diag mostra_treball/['nomes_rectes'] vs proposa_resultat/nomes_rectes, refs []]: Quina mena de camins cap a l’origen has considerat amb $y=mx$? N’hi ha algun altre en què $x$ i $y$ es relacionin d’una manera diferent?

**2. ALUMNE:** A l'origen, $D_vf(0,0)=\lim_{t\to0}\frac{f(tv)}{t}=\frac{v_1^2}{v_2}$ si $v_2\neq0$. Com que existeixen totes, $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 2, diag proposa_resultat/['direccionals_implica_continuitat'] vs mostra_treball/direccionals_implica_continuitat, refs []]: Què et diu exactament la derivada direccional segons la fórmula que has escrit? Calcula el comportament de $f$ en quina mena de conjunt?

**3. ALUMNE:** Dona'm una pista per estudiar la continuïtat a l'origen.
**TUTOR** [pista, pista 2, intents 2, diag demana_pista/[] vs demana_pista/None, refs ['T2.20']]: Per estudiar la continuïtat global, separa primer els punts amb $y\neq0$ de l’eix $y=0$. En la regió $y\neq0$, la funció és el quocient d’expressions polinòmiques i el denominador no s’anul·la; per la Proposició 20 del Tema 2, què pots concloure sobre la continuïtat en aquests punts?

**4. ALUMNE:** Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.
**TUTOR** [validar_i_avancar, pista 1, intents 2, diag mostra_treball/[] vs mostra_treball/None, refs ['T2.20']]: Exacte: has justificat correctament la continuïtat en tots els punts amb $y\neq0$ mitjançant la Proposició 20 del Tema 2. Ara centra’t en un punt de l’eix $y=0$ diferent de l’origen: què hauria de passar amb el valor de la funció a prop d’un punt $(x_0,0)$ perquè fos contínua?

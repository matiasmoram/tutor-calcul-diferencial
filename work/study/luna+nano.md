# luna+nano

Stages: {'diagnosis': ['openai', 'gpt-5.6-luna', 'low'], 'reply': ['openai', 'gpt-5.4-nano', 'low'], 'guard': ['openai', 'gpt-5.6-luna', 'low']}

Metrics: {'turns': 16, 'failed_turns': 0, 'fallback': 6, 'drafts_per_turn': 2.19, 'draft_errors': 0, 'latex_broken': 0, 'intent_match': 11, 'error_match': 16, 'cost_usd': 0.077, 'cost_per_turn_usd': 0.00481, 'latency_s': 19.5, 'input_tokens': 289996, 'cached_tokens': 53683, 'output_tokens': 23565}

## t2-4c
**1. ALUMNE:** He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.
**TUTOR (FALLBACK)** [questionar_error, pista 0, intents 3, diag proposa_resultat/['camins_com_a_prova'] vs proposa_resultat/camins_com_a_prova, refs []]: Has provat alguns camins i tots donen el mateix. Això demostra que el límit existeix, o només et dona un candidat?


**2. ALUMNE:** Què vol dir exactament que un límit existeixi?
**TUTOR (FALLBACK)** [explicar_concepte, pista 0, intents 3, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs []]: Mira la Definició 6 del Tema 2 als apunts. Com creus que s'aplica a aquest exercici?

**3. ALUMNE:** No sé com fitar-ho. Digues-me la solució, si us plau.
**TUTOR (FALLBACK)** [pista, pista 2, intents 3, diag demana_solucio/[] vs demana_solucio/None, refs []]: Una idea per avançar: Comparar el denominador amb un dels seus sumands (tots dos són no negatius) per fitar el quocient per dalt. Com ho aplicaries?

**4. ALUMNE:** Com que $x^4\le x^4+y^2$, tinc $|f|\le\frac{|x|^5}{x^4}=|x|\to0$, i pel sandvitx el límit és $0$.
**TUTOR** [tancar, pista 0, intents 1, diag mostra_treball/[] vs proposa_resultat/None, refs []]: Bona feina: has passat de mirar camins a una acotació global, i això és el que faltava per poder afirmar el límit. Comparant el denominador amb $x^4$ has obtingut $\frac{|x|^5}{x^4+y^2}\le |x|$, i després el sandvitx et dona la conclusió que el quocient va a $0$ quan $(x,y)\to(0,0)$. L’idea clau és fer una fita que depengui només de $\|(x,y)\|$ (no del camí). El resultat és $0$.

## t4-8
**1. ALUMNE:** Calculo el jacobià: $\det JG=3+6z$, que a $(1,-1,2)$ val $15$.
**TUTOR** [pista, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Perfecte: ja has situat que el determinant no s’anul·la a $(1,-1,2)$, però ara el pas clau és connectar els dos punts. A quin punt $G(1,-1,2)$ arriba (és a dir, quines són les components de $G(1,-1,2)$) i com encaixa això amb que després et demanen $DG^{-1}(4,4,-1)$?

**2. ALUMNE:** Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?
**TUTOR** [explicar_concepte, pista 1, intents 2, diag pregunta_conceptual/['punt_equivocat'] vs mostra_treball/punt_equivocat, refs ['T4.9']]: Quan tens una aplicació $f:\mathbb R^n\to\mathbb R^n$ que és un difeomorfisme local, vol dir que al voltant d’un punt $a$ té inversa diferenciable al voltant del punt imatge $f(a)$. En particular, per parlar de $Df^{-1}$ en un punt $b$, necessites identificar quin és l’emplaçament previ $a$ tal que $f(a)=b$. Teixint això amb la idea de difeomorfisme, el que importa és la correspondència entre punt i imatge, més que fer càlculs immediats (vegeu la Definició 9 del Tema 4). Quin és el punt $a$ que necessites perquè la imatge sigui el punt on et demanen $DG^{-1}(4,4,-1)$, és a dir, quin ha de complir $G(a)=(4,4,-1)$?

**3. ALUMNE:** Què diu exactament el teorema de la funció inversa?
**TUTOR (FALLBACK)** [explicar_concepte, pista 1, intents 3, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs []]: Mira la Definició 9 del Tema 4 als apunts. Com creus que s'aplica a aquest exercici?

**4. ALUMNE:** Com que té inversa local a tot arreu on $3+6z\neq0$, $G$ té inversa global.
**TUTOR (FALLBACK)** [questionar_error, pista 1, intents 3, diag proposa_resultat/['local_implica_global'] vs proposa_resultat/local_implica_global, refs []]: El teorema de la funció inversa et dona una inversa en un entorn. Què hauria de complir $G$ a tot $\mathbb{R}^3$ per tenir una inversa global?


## t6-3a
**1. ALUMNE:** No sé per on començar.
**TUTOR** [pista, pista 2, intents 3, diag demana_pista/[] vs demana_pista/None, refs ['T2.23']]: Bona idea: per decidir l’existència d’extrems absoluts, mira el **conjunt de lligam** $C=\{(x,y)\,:\,x^2+2y^2=3\}$ i pregunta’t si és **compact** (és a dir, si és **tancat i fitat**). Com que $f(x,y)=x$ és contínua, si $C$ és compacte llavors el resultat d’existència ve del Teorema 23 del Tema 2 (Weierstrass).  
Et sembla que $C$ és fitat i tancat, o hi ha algun motiu perquè no ho sigui?

**2. ALUMNE:** Sobre l'el·lipse $x^2=3-2y^2\le3$, així que $|x|\le\sqrt3$.
**TUTOR** [pista, pista 3, intents 2, diag mostra_treball/[] vs mostra_treball/None, refs []]: Bona: ja has observat que l’ansa queda acotada, és a dir, del lligam pots deduir $|x|\le \sqrt3$ (i també podries obtenir un límit per $y$). Ara, comprova dues coses sobre el conjunt $M=\{(x,y):x^2+2y^2=3\}$: està tancat (per exemple, com a antiimatge d’un tancat mitjançant una funció contínua) i és fitat (amb desigualtats per $x$ i $y$). Un cop tinguis clar que $M$ és compacte i que $f(x,y)=x$ és contínua, quin resultat de la teoria (Teorema de Weierstrass) et diu exactament que hi ha màxim i mínim sobre $M$?

**3. ALUMNE:** Per tant el màxim és $\sqrt3$ i el mínim $-\sqrt3$.
**TUTOR (FALLBACK)** [demanar_justificacio, pista 3, intents 3, diag proposa_resultat/[] vs proposa_resultat/None, refs []]: Una idea per avançar: Mirar si el conjunt definit pel lligam és tancat i fitat, i si $f$ és contínua. Com ho aplicaries?

**4. ALUMNE:** S'assoleixen a $(\sqrt3,0)$ i $(-\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.
**TUTOR** [tancar, pista 0, intents 1, diag mostra_treball/[] vs proposa_resultat/None, refs []]: Exacte: els extrems absoluts s’assoleixen en $(\sqrt3,0)$ i $(-\sqrt3,0)$. El màxim és $\sqrt3$ i el mínim és $-\sqrt3$, d’acord amb el que has raonat. La idea clau ha estat convertir el problema en un de màxim i mínim d’una funció contínua sobre un conjunt compacte (Weierstrass). Bona feina.

## t3-5
**1. ALUMNE:** Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag mostra_treball/['nomes_rectes'] vs proposa_resultat/nomes_rectes, refs []]: Entenc per què t’has fixat en les rectes $y=mx$, però potser això no és prou per assegurar la continuïtat a l’origen. Hi ha camins cap a l’origen que no siguin rectes (per exemple, corbes) on el quocient $\frac{x^2}{y}$ es comporti de manera diferent que quan $y=mx$? Quin camí concret et podria canviar el denominador $y$ “més ràpid” que el numerador $x^2$ mentre t’acostes a $(0,0)$?

**2. ALUMNE:** A l'origen, $D_vf(0,0)=\lim_{t\to0}\frac{f(tv)}{t}=\frac{v_1^2}{v_2}$ si $v_2\neq0$. Com que existeixen totes, $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 2, diag proposa_resultat/['direccionals_implica_continuitat'] vs mostra_treball/direccionals_implica_continuitat, refs []]: Has escrit que $D_v f(0,0)=\lim_{t\to0}\frac{f(tv)}{t}=\frac{v_1^2}{v_2}$ (si $v_2\neq0$). Quan una derivada direccional existeix, quina informació concreta et dóna sobre el comportament de $f(a+tu)$ només al llarg de la recta $a+tu$, i no en tot el voltant del punt en 2D? En concret, per concloure la continuïtat a l’origen, el que necessites és un límit $f(x,y)\to f(0,0)$ per a $(x,y)\to(0,0)$ seguint qualsevol camí: com ho justificaries només a partir de l’existència de $D_u f(0,0)$ per a totes les direccions? Què et falta provar perquè el límit bidimensional existeixi?

**3. ALUMNE:** Dona'm una pista per estudiar la continuïtat a l'origen.
**TUTOR** [pista, pista 2, intents 2, diag demana_pista/[] vs demana_pista/None, refs ['T2.14', 'T2.20']]: Bé: la peça clara és que “fora de l’eix” (és a dir, quan $y\neq0$) la funció està definida per una única fórmula $\frac{x^2}{y}$, i això ja et dóna un obert on té sentit estudiar la continuïtat sense el cas especial $y=0$. Per $y\neq0$, $\frac{x^2}{y}$ és composició d’operacions elementals (polinomis i divisió per una funció no nul·la), així que la continuïtat es pot justificar directament amb la definició de continuïtat (Teorema/Definició 14 del Tema 2) i l’àlgebra de funcions contínues (Proposició 20 del Tema 2). Quin és el conjunt exacte on tens garantia automàtica que $y\neq0$, i què et diu això sobre quin cas de la definició de $f$ s’ha d’usar?

**4. ALUMNE:** Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.
**TUTOR** [validar_i_avancar, pista 1, intents 2, diag mostra_treball/[] vs mostra_treball/None, refs ['T2.14']]: Correcte: fora de l’eix $y=0$ ja tens la continuïtat perquè allí $f(x,y)=\frac{x^2}{y}$ és un quocient amb denominador no nul. Ara toca analitzar punts de l’eix $y=0$ però amb $x_0\neq 0$, és a dir, comprovar si $\lim_{(x,y)\to(x_0,0)} f(x,y)=f(x_0,0)$ existeix (Teorema/Definició 14 del Tema 2). Quin valor ha de tenir aquest límit perquè la funció sigui contínua en $(x_0,0)$?

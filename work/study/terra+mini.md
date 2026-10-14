# terra+mini

Stages: {'diagnosis': ['openai', 'gpt-5.6-terra', 'low'], 'reply': ['openai', 'gpt-5.4-mini', 'low'], 'guard': ['openai', 'gpt-5.4-mini', 'low']}

Metrics: {'turns': 16, 'failed_turns': 0, 'fallback': 0, 'drafts_per_turn': 1.12, 'draft_errors': 0, 'latex_broken': 0, 'intent_match': 12, 'error_match': 15, 'cost_usd': 0.2343, 'cost_per_turn_usd': 0.01465, 'latency_s': 6.3, 'input_tokens': 184150, 'cached_tokens': 72177, 'output_tokens': 9483}

## t2-4c
**1. ALUMNE:** He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['camins_com_a_prova'] vs proposa_resultat/camins_com_a_prova, refs []]: Has provat alguns camins i tots et donen $0$. Això et garanteix que el límit existeix, o només que $0$ és un candidat?

**2. ALUMNE:** Què vol dir exactament que un límit existeixi?
**TUTOR** [explicar_concepte, pista 0, intents 1, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T2.6', 'T2.10']]: Dir que existeix el límit de $f(x,y)$ quan $(x,y)\to(0,0)$ vol dir, segons la Definició 6 del Tema 2, que podem fer $f(x,y)$ tan a prop com vulguem d’un valor $L$ quan $(x,y)$ és prou a prop de $(0,0)$ però diferent d’aquest punt. En altres paraules, el valor límit no depèn del camí amb què t’hi acostes; si el límit existeix, tots els camins lícits han de donar el mateix valor, com recull també la Proposició 10 del Tema 2. Com ho faries servir amb els camins que ja has provat?

**3. ALUMNE:** No sé com fitar-ho. Digues-me la solució, si us plau.
**TUTOR** [pista, pista 2, intents 2, diag demana_solucio/[] vs demana_solucio/None, refs []]: Bona, ara ja tens un candidat; el que falta és una fita que no depengui del camí. Mira el denominador: com que $x^4$ i $y^2$ són no negatius, pots comparar-lo amb un dels seus sumands per obtenir una cota superior del mòdul del quocient. Quina desigualtat escriuries si el compares amb $x^4$?

**4. ALUMNE:** Com que $x^4\le x^4+y^2$, tinc $|f|\le\frac{|x|^5}{x^4}=|x|\to0$, i pel sandvitx el límit és $0$.
**TUTOR** [tancar, pista 0, intents 1, diag mostra_treball/[] vs proposa_resultat/None, refs []]: Molt bé: has justificat correctament que el límit és $0$. La idea clau ha estat acotar $\dfrac{|x|^5}{x^4+y^2}$ per $|x|$ i acabar amb el sandvitx, de manera que la dependència del camí ja no importa.

## t4-8
**1. ALUMNE:** Calculo el jacobià: $\det JG=3+6z$, que a $(1,-1,2)$ val $15$.
**TUTOR** [pista, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Bona feina amb el jacobià; ara et falta lligar el punt on l’estudies amb el punt on vols avaluar la inversa. Has comprovat que $G(1,-1,2)$ és exactament $(4,4,-1)$?

**2. ALUMNE:** Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?
**TUTOR** [questionar_error, pista 1, intents 1, diag demana_pista/['punt_equivocat'] vs mostra_treball/punt_equivocat, refs ['T4.5']]: Pensa-ho amb el Teorema 5 del Tema 4: la fórmula per a $D G^{-1}(y_0)$ fa servir el punt del domini que compleix $G(x)=y_0$. Quin és aquest punt en el teu cas, i sobre quina matriu s’ha d’avaluar aleshores?

**3. ALUMNE:** Què diu exactament el teorema de la funció inversa?
**TUTOR** [explicar_concepte, pista 1, intents 2, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T4.5']]: El Teorema 5 del Tema 4 diu que, si una funció $f$ és de classe $C^r$ i la seva jacobiana té determinant no nul en un punt, aleshores existeix un entorn on $f$ és injectiva, la imatge és oberta i la inversa és també de classe $C^r$. A més, la derivada de la inversa es calcula com $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$. Què has de comprovar primer en el punt on vols situar la inversa local?

**4. ALUMNE:** Com que té inversa local a tot arreu on $3+6z\neq0$, $G$ té inversa global.
**TUTOR** [questionar_error, pista 1, intents 1, diag proposa_resultat/['local_implica_global'] vs proposa_resultat/local_implica_global, refs ['T4.5']]: El teorema de la funció inversa et dóna una inversa en un entorn, com diu el Teorema 5 del Tema 4; però, per parlar d’inversa global, què hauries de poder assegurar sobre $G$ a tot $\mathbb{R}^3$?

## t6-3a
**1. ALUMNE:** No sé per on començar.
**TUTOR** [pista, pista 2, intents 1, diag demana_pista/[] vs demana_pista/None, refs ['T2.23']]: Entenc que encara no tens clar l’entrada. Abans de buscar candidats, pots mirar si el conjunt $x^2+2y^2=3$ és tancat i fitat; si ho és, per Heine-Borel i el Teorema 23 del Tema 2 pots garantir que $f$ té màxim i mínim sobre aquest lligam. Com ho justificaries amb aquesta idea?

**2. ALUMNE:** Sobre l'el·lipse $x^2=3-2y^2\le3$, així que $|x|\le\sqrt3$.
**TUTOR** [validar_i_avancar, pista 2, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Molt bé: has acotat $x$ amb el lligam, i això et dona una pista clara que el conjunt queda fitat; a més, l’el·lipse és també tancada perquè ve definida per una igualtat polinòmica. Amb això i el fet que $f(x,y)=x$ és contínua, quina propietat et permet concloure que $f$ assoleix màxim i mínim sobre aquest conjunt?

**3. ALUMNE:** Per tant el màxim és $\sqrt3$ i el mínim $-\sqrt3$.
**TUTOR** [questionar_error, pista 2, intents 1, diag proposa_resultat/['fita_sense_assolir', 'sense_existencia'] vs proposa_resultat/None, refs []]: La idea d’acotar $x$ és bona, però ara cal comprovar si aquesta fita es pot arribar a obtenir dins del lligam. Hi ha algun punt de l’el·lipse on $x$ valgui exactament $\sqrt3$ o $-\sqrt3$?

**4. ALUMNE:** S'assoleixen a $(\sqrt3,0)$ i $(-\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.
**TUTOR** [tancar, pista 0, intents 1, diag mostra_treball/[] vs proposa_resultat/None, refs []]: Perfecte: ja ho tens ben tancat. El màxim absolut és $\sqrt3$ a $(\sqrt3,0)$ i el mínim absolut és $-\sqrt3$ a $(-\sqrt3,0)$. La idea clau ha estat reduir el problema a acotar $x$ amb el lligam i després comprovar que els valors extrems s’assoleixen exactament quan $y=0$.

## t3-5
**1. ALUMNE:** Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['nomes_rectes'] vs proposa_resultat/nomes_rectes, refs []]: Entenc la idea que has provat amb les rectes, però abans de donar-la per bona, pensa en això: hi ha algun camí cap a l’origen que no sigui una recta i que canviï la relació entre $x^2$ i $y$?

**2. ALUMNE:** A l'origen, $D_vf(0,0)=\lim_{t\to0}\frac{f(tv)}{t}=\frac{v_1^2}{v_2}$ si $v_2\neq0$. Com que existeixen totes, $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['direccionals_implica_continuitat'] vs mostra_treball/direccionals_implica_continuitat, refs ['T3.1']]: Entenc que això et pugui confondre. Segons la Definició 1 del Tema 3, una derivada direccional mira només què passa sobre la recta de direcció $v$; això et garanteix el comportament de $f$ en tots els camins cap a l’origen o només en aquell?

**3. ALUMNE:** Dona'm una pista per estudiar la continuïtat a l'origen.
**TUTOR** [pista, pista 1, intents 1, diag demana_pista/[] vs demana_pista/None, refs []]: Bona idea mirar l’origen, però abans d’això: què passa amb $f(x,y)$ en qualsevol punt amb $y\neq 0$, on l’expressió és una fracció usual?

**4. ALUMNE:** Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.
**TUTOR** [validar_i_avancar, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Perfecte: has justificat bé que a l’obert $\{y\neq 0\}$ la funció és contínua. Ara toca mirar els punts de l’eix amb $x_0\neq 0$; què passa amb $f(x,y)$ quan t’acostes a $(x_0,0)$ mantenint $x$ fixat?

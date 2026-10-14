# mini+luna

Stages: {'diagnosis': ['openai', 'gpt-5.4-mini', 'low'], 'reply': ['openai', 'gpt-5.6-luna', 'low'], 'guard': ['openai', 'gpt-5.6-luna', 'low']}

Metrics: {'turns': 16, 'failed_turns': 0, 'fallback': 0, 'drafts_per_turn': 1.31, 'draft_errors': 0, 'latex_broken': 0, 'intent_match': 14, 'error_match': 15, 'cost_usd': 0.0661, 'cost_per_turn_usd': 0.00413, 'latency_s': 8.4, 'input_tokens': 193719, 'cached_tokens': 68222, 'output_tokens': 11080}

## t2-4c
**1. ALUMNE:** He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.
**TUTOR** [questionar_error, pista 0, intents 2, diag proposa_resultat/['camins_com_a_prova'] vs proposa_resultat/camins_com_a_prova, refs []]: Has provat alguns camins i tots donen el mateix valor, però això demostra que el límit existeix o només et proporciona un candidat?

**2. ALUMNE:** Què vol dir exactament que un límit existeixi?
**TUTOR** [explicar_concepte, pista 0, intents 2, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T2.6']]: Que existeixi un límit vol dir que els valors de la funció s’apropen a un únic nombre quan el punt s’acosta al punt considerat, independentment de com s’hi arribi, tal com estableix la Definició 6 del Tema 2. Provar diversos camins només és una condició necessària: si el límit existeix, tots aquests camins han de donar el mateix valor, però això no garanteix per si sol que existeixi. Com podries aplicar aquesta idea per decidir si el límit del teu exercici existeix?

**3. ALUMNE:** No sé com fitar-ho. Digues-me la solució, si us plau.
**TUTOR** [pista, pista 2, intents 3, diag demana_solucio/[] vs demana_solucio/None, refs []]: Entenc que la dificultat és trobar una cota adequada, no pas provar més camins. Per acotar el mòdul del quocient, observa que el denominador és una suma de termes no negatius i, per tant, és com a mínim tan gran com cadascun dels seus sumands. Amb quin dels sumands del denominador et convé comparar-lo per obtenir una desigualtat per al mòdul?

**4. ALUMNE:** Com que $x^4\le x^4+y^2$, tinc $|f|\le\frac{|x|^5}{x^4}=|x|\to0$, i pel sandvitx el límit és $0$.
**TUTOR** [tancar, pista 0, intents 1, diag mostra_treball/[] vs proposa_resultat/None, refs []]: Exacte: has justificat correctament que el límit és $0$. La idea clau és acotar el mòdul per $|x|$ i aplicar el teorema del sandvitx, ja que $|x|\to0$. Molt bé.

## t4-8
**1. ALUMNE:** Calculo el jacobià: $\det JG=3+6z$, que a $(1,-1,2)$ val $15$.
**TUTOR** [pista, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Has calculat el jacobià; ara comprova quin punt obtenim en aplicar $G$ a $(1,-1,2)$. És el mateix punt $(4,4,-1)$ on es demana $DG^{-1}$?

**2. ALUMNE:** Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?
**TUTOR** [explicar_concepte, pista 1, intents 1, diag pregunta_conceptual/['punt_equivocat'] vs mostra_treball/punt_equivocat, refs ['T4.5']]: La teva interpretació encara no situa correctament el punt: la diferencial de la inversa en un punt del codomini es relaciona amb el punt del domini que hi és enviat, no amb el mateix triple de coordenades. En general, el Teorema 5 del Tema 4 estableix que $D f^{-1}(y_0)=\big(D f(f^{-1}(y_0))\big)^{-1}$. Com comprovaries si $(4,4,-1)$ és la imatge de $(1,-1,2)$ sota $G$?

**3. ALUMNE:** Què diu exactament el teorema de la funció inversa?
**TUTOR** [explicar_concepte, pista 1, intents 1, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T4.5']]: El Teorema 5 del Tema 4 diu que, si el determinant de la jacobiana en un punt és no nul, aleshores la funció té una inversa diferenciable en un entorn d’aquest punt; a més, la diferencial de la inversa en un punt del codomini es calcula a partir del punt del domini que hi és enviat. Com comprovaries quin punt del codomini correspon al punt $(1,-1,2)$?

**4. ALUMNE:** Com que té inversa local a tot arreu on $3+6z\neq0$, $G$ té inversa global.
**TUTOR** [questionar_error, pista 1, intents 1, diag proposa_resultat/['local_implica_global'] vs proposa_resultat/local_implica_global, refs ['T4.5']]: Entenc que aquest pas et generi dubtes. El Teorema 5 del Tema 4 només garanteix una inversa en un entorn del punt; què hauria de complir $G$ a tot $\mathbb{R}^3$ perquè pogués tenir una inversa global?

## t6-3a
**1. ALUMNE:** No sé per on començar.
**TUTOR** [pista, pista 2, intents 1, diag demana_pista/[] vs demana_pista/None, refs []]: Entenc que no sàpigues per on començar; primer comprovem que els extrems existeixen. Mira el conjunt definit per $x^2+2y^2=3$: és tancat i fitat? I la funció $f(x,y)=x$, és contínua? Si totes dues respostes són afirmatives, quin teorema et permet garantir l’existència del màxim i del mínim?

**2. ALUMNE:** Sobre l'el·lipse $x^2=3-2y^2\le3$, així que $|x|\le\sqrt3$.
**TUTOR** [validar_i_avancar, pista 2, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Correcte: has vist que el lligam f].ita $x$ entre $-\sqrt3$ i $\sqrt3$, però encara cal comprovar que el conjunt del lligam és tancat i fitat, i que $f(x,y)=x$ és contínua. Si ho és, quin teorema garanteix que s’assoleixen el màxim i el mínim?

**3. ALUMNE:** Per tant el màxim és $\sqrt3$ i el mínim $-\sqrt3$.
**TUTOR** [questionar_error, pista 2, intents 1, diag proposa_resultat/['fita_sense_assolir', 'sense_existencia'] vs proposa_resultat/None, refs []]: La fita que has obtingut només indica quins valors no pot superar $x$; encara cal veure si aquests valors s’assoleixen realment sobre l’el·lipse. Hi ha algun punt de l’el·lipse on $x$ valgui exactament la fita que has trobat?

**4. ALUMNE:** S'assoleixen a $(\sqrt3,0)$ i $(-\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.
**TUTOR** [demanar_justificacio, pista 2, intents 1, diag proposa_resultat/[] vs proposa_resultat/None, refs ['T1.34', 'T2.23']]: Sí, el resultat que proposes és correcte, i els punts indicats pertanyen al lligam; ara falta justificar que no poden existir extrems fora d’aquests valors. L’estratègia és aplicar el Teorema 34 del Tema 1 per veure que el conjunt del lligam és compacte, i després el Teorema 23 del Tema 2, ja que $f(x,y)=x$ és contínua. Pots explicar per què el conjunt definit per $x^2+2y^2=3$ és tancat i fitat?

## t3-5
**1. ALUMNE:** Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['nomes_rectes'] vs proposa_resultat/nomes_rectes, refs []]: Has examinat les rectes, però això només cobreix una part dels camins que es poden acostar a l’origen. Hi ha camins cap a l’origen que no siguin rectes on el numerador i el denominador es comparin de manera diferent?

**2. ALUMNE:** A l'origen, $D_vf(0,0)=\lim_{t\to0}\frac{f(tv)}{t}=\frac{v_1^2}{v_2}$ si $v_2\neq0$. Com que existeixen totes, $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag mostra_treball/['direccionals_implica_continuitat', 'altre'] vs mostra_treball/direccionals_implica_continuitat, refs []]: Què et diu exactament una derivada direccional: el comportament de $f$ en tot un entorn de l’origen, o només sobre una recta que passa per aquest punt?

**3. ALUMNE:** Dona'm una pista per estudiar la continuïtat a l'origen.
**TUTOR** [pista, pista 2, intents 2, diag demana_pista/[] vs demana_pista/None, refs ['T2.20']]: Per començar, separa els punts amb segona coordenada no nul·la dels punts de l’eix. En els primers, la funció és un quocient de funcions polinòmiques amb denominador no nul, i la Proposició 20 del Tema 2 permet estudiar-ne la continuïtat directament. Quina part de l’espai queda pendent d’analitzar després d’aquest cas?

**4. ALUMNE:** Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.
**TUTOR** [validar_i_avancar, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs ['T2.20']]: Correcte: has justificat la continuïtat en tots els punts amb $y\neq0$ aplicant la Proposició 20 del Tema 2. Ara queden els punts de l’eix $y=0$ amb primera coordenada no nul·la: què passa amb el límit de $f(x,y)$ quan $(x,y)$ s’acosta a $(x_0,0)$ per punts amb $y\neq0$?

# mini54

Stages: {'diagnosi': ('openai', 'gpt-5.4-mini', 'low'), 'resposta': ('openai', 'gpt-5.4-mini', 'low'), 'guardia': ('openai', 'gpt-5.4-mini', 'low')}

Metrics: {'turns': 16, 'failed_turns': 0, 'fallback': 0, 'drafts_per_turn': 1.06, 'draft_errors': 0, 'latex_broken': 0, 'intent_match': 15, 'error_match': 16, 'cost_usd': 0.1333, 'cost_per_turn_usd': 0.00833, 'latency_s': 6.8, 'input_tokens': 176005, 'cached_tokens': 75264, 'output_tokens': 11584}

## t2-4c
**1. ALUMNE:** He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['camins_com_a_prova'] vs proposa_resultat/camins_com_a_prova, refs []]: Bé, has comprovat alguns camins i tots et donen el mateix valor, així que això et dona un candidat molt raonable; però, segons la definició de límit i el criteri de camins, amb això n’hi ha prou per assegurar que el límit existeix?

**2. ALUMNE:** Què vol dir exactament que un límit existeixi?
**TUTOR** [explicar_concepte, pista 0, intents 1, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T2.6', 'T2.10']]: Que un límit existeixi vol dir, segons la Definició 6 del Tema 2, que pots fer que els valors de la funció quedin tan a prop com vulguis d’un mateix nombre $b$ quan les $(x,y)$ s’acosten prou al punt, i això ha de passar independentment del camí que segueixis. En el cas de funcions de dues variables, la Proposició 10 del Tema 2 diu que si el límit existeix, llavors qualsevol camí continu que passis pel punt ha de donar el mateix valor $L$. Com faries servir aquesta idea per posar a prova el candidat que tens?

**3. ALUMNE:** No sé com fitar-ho. Digues-me la solució, si us plau.
**TUTOR** [pista, pista 2, intents 1, diag demana_solucio/[] vs demana_solucio/None, refs []]: Has vist bé que provar rectes et dona un candidat, però ara toca justificar-ho amb una fita. Com que $x^4$ i $y^2$ són no negatius, pots comparar $x^4+y^2$ amb un dels dos sumands per fer aparèixer una expressió més simple que domini el valor absolut del quocient. Si uses aquesta idea, quin sumand et convé conservar per obtenir una cota que et porti a una potència de $|x|$ que tendeixi a $0$?

**4. ALUMNE:** Com que $x^4\le x^4+y^2$, tinc $|f|\le\frac{|x|^5}{x^4}=|x|\to0$, i pel sandvitx el límit és $0$.
**TUTOR** [tancar, pista 0, intents 1, diag proposa_resultat/[] vs proposa_resultat/None, refs []]: Molt bé: has acabat la justificació i el resultat és $0$. La idea clau ha estat acotar $|f(x,y)|$ per una expressió més simple, arribant a $|f(x,y)|\le |x|$, i així aplicar el sandvitx per veure que tot tendeix a $0$.

## t4-8
**1. ALUMNE:** Calculo el jacobià: $\det JG=3+6z$, que a $(1,-1,2)$ val $15$.
**TUTOR** [pista, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Bé, ja tens una part clau: ara fixa’t en quin punt del domini has de linealitzar i quin és el punt de la imatge on et demanen $DG^{-1}$. Pots comprovar directament si $G(1,-1,2)$ coincideix amb $(4,4,-1)$?

**2. ALUMNE:** Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?
**TUTOR** [questionar_error, pista 1, intents 1, diag pregunta_conceptual/['punt_equivocat'] vs mostra_treball/punt_equivocat, refs ['T4.5']]: Has trobat bé que $\det JG(1,-1,2)\neq 0$, i això et dona la inversa local amb el Teorema 5 del Tema 4. Però abans de continuar, mira el significat de $DG^{-1}(4,4,-1)$: aquest punt és del domini de $G$ o de la seva inversa, i en quin punt s’ha d’avaluar $JG$ per usar la fórmula del teorema?

**3. ALUMNE:** Què diu exactament el teorema de la funció inversa?
**TUTOR** [explicar_concepte, pista 1, intents 1, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T4.5']]: El Teorema 5 del Tema 4 diu, en essència, que si una funció $f$ és de classe $\mathcal{C}^r$ i el seu jacobià té determinant no nul en un punt $a$, aleshores al voltant d’aquell punt existeix una inversa local i aquesta inversa també és de classe $\mathcal{C}^r$. A més, la diferencial de la inversa en un punt de la imatge es calcula com la inversa de la diferencial de $f$ en el punt corresponent del domini. Com ho podries aplicar aquí per relacionar el punt on avalues la inversa amb el punt del domini de $G$?

**4. ALUMNE:** Com que té inversa local a tot arreu on $3+6z\neq0$, $G$ té inversa global.
**TUTOR** [questionar_error, pista 1, intents 1, diag proposa_resultat/['local_implica_global'] vs proposa_resultat/local_implica_global, refs ['T4.5']]: Pensa en què garanteix exactament el Teorema 5 del Tema 4: a partir de $\det(JG)\neq 0$, obtens una inversa en un entorn, però què hauries de saber de $G$ a tot $\mathbb{R}^3$ per poder parlar d’una inversa global?

## t6-3a
**1. ALUMNE:** No sé per on començar.
**TUTOR** [pista, pista 2, intents 1, diag demana_pista/[] vs demana_pista/None, refs ['T1.34', 'T2.23']]: El primer pas és decidir si pots garantir que hi ha màxim i mínim absoluts abans de buscar-los. Com que el lligam defineix una corba donada per una equació, et convé mirar si aquest conjunt és tancat i fitat, i després comprovar que $f$ és contínua per poder aplicar Weierstrass. Ho pots verificar amb el Teorema 34 del Tema 1 i el Teorema 23 del Tema 2?

**2. ALUMNE:** Sobre l'el·lipse $x^2=3-2y^2\le3$, així que $|x|\le\sqrt3$.
**TUTOR** [validar_i_avancar, pista 2, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Bé: has acotat $x$ correctament a partir del lligam, i això ja apunta que el conjunt no pot “escapar” cap a l’infinit. Et falta completar la idea global: pots justificar que l’el·lipse $x^2+2y^2=3$ és tancada i fitada, i que $f(x,y)=x$ és contínua, per poder aplicar Weierstrass?

**3. ALUMNE:** Per tant el màxim és $\sqrt3$ i el mínim $-\sqrt3$.
**TUTOR** [demanar_justificacio, pista 3, intents 1, diag proposa_resultat/[] vs proposa_resultat/None, refs ['T1.34', 'T2.23']]: Sí, el valor que proposes és coherent amb l’acotació que ja has fet, però encara et falta justificar per què aquests extrems han d’existir abans d’identificar-los. Pots completar-ho així: el conjunt $M=\{(x,y):x^2+2y^2=3\}$ és tancat perquè és la contraimatge d’un tancat per una funció contínua, i també és fitat perquè de $x^2\le 3$ i $y^2\le 3/2$ en surt una cota per a totes dues variables, de manera que és compacte pel Teorema 34 del Tema 1. Aleshores, com que $f(x,y)=x$ és contínua, què et permet concloure el Teorema 23 del Tema 2 sobre màxim i mínim absoluts a $M$?

**4. ALUMNE:** S'assoleixen a $(\sqrt3,0)$ i $(-\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.
**TUTOR** [demanar_justificacio, pista 3, intents 1, diag proposa_resultat/[] vs proposa_resultat/None, refs ['T2.23']]: Sí, el valor que has donat és coherent, i la idea clau ja la tens: com que el lligam defineix un conjunt tancat i fitat, pots aplicar Weierstrass. Et falta escriure-ho de manera completa: primer justifica que $M=\{(x,y):x^2+2y^2=3\}$ és tancat i fitat, i després que $f(x,y)=x$ és contínua; amb això, què et permet concloure exactament el Teorema 23 del Tema 2 sobre $f$ a $M$?

## t3-5
**1. ALUMNE:** Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['nomes_rectes'] vs proposa_resultat/nomes_rectes, refs []]: Has comprovat només camins del tipus $y=mx$, però quan et mous cap a l’origen per altres trajectòries també surt el mateix comportament? Prova de pensar si hi ha alguna corba on $x^2$ i $y$ es comparin d’una altra manera; què et diria això sobre el límit a l’origen?

**2. ALUMNE:** A l'origen, $D_vf(0,0)=\lim_{t\to0}\frac{f(tv)}{t}=\frac{v_1^2}{v_2}$ si $v_2\neq0$. Com que existeixen totes, $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag mostra_treball/['direccionals_implica_continuitat'] vs mostra_treball/direccionals_implica_continuitat, refs ['T3.1']]: Pensa en què mesura exactament $D_vf(0,0)$ segons la Definició 1 del Tema 3: el comportament de $f$ en tot un entorn, o només sobre la recta $a+tv$? Si només mires una direcció fixa, això et permet assegurar el límit de $f(x,y)$ quan $(x,y)\to(0,0)$ per qualsevol camí?

**3. ALUMNE:** Dona'm una pista per estudiar la continuïtat a l'origen.
**TUTOR** [questionar_error, pista 0, intents 2, diag demana_pista/['altre'] vs demana_pista/None, refs []]: Si només has mirat rectes de la forma $y=mx$, què et fa pensar que això n’hi ha prou per assegurar el límit de $f(x,y)$ quan $(x,y)\to(0,0)$ per qualsevol camí?

**4. ALUMNE:** Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.
**TUTOR** [validar_i_avancar, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs ['T2.20']]: Sí, això de fora de l’eix $y=0$ ho tens ben encarat: en $U=\{y\neq 0\}$ la funció és contínua per ser un quocient amb denominador no nul, com diu la Proposició 20 del Tema 2. Ara toca mirar què passa als punts de l’eix amb $x_0\neq 0$; què obtens si t’acostes a $(x_0,0)$ mantenint $x=x_0$ i fent $y\to 0$?

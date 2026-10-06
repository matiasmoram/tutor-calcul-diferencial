# mini54

Stages: {'diagnosi': ('openai', 'gpt-5.4-mini', 'low'), 'resposta': ('openai', 'gpt-5.4-mini', 'low'), 'guardia': ('openai', 'gpt-5.4-mini', 'low')}

Metrics: {'turns': 16, 'failed_turns': 0, 'fallback': 0, 'drafts_per_turn': 1.06, 'draft_errors': 0, 'latex_broken': 0, 'intent_match': 12, 'error_match': 16, 'cost_usd': 0.1199, 'cost_per_turn_usd': 0.00749, 'latency_s': 6.2, 'input_tokens': 174635, 'cached_tokens': 89088, 'output_tokens': 10906}

## t2-4c
**1. ALUMNE:** He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['camins_com_a_prova'] vs proposa_resultat/camins_com_a_prova, refs ['T2.6']]: Bé: amb els camins $y=kx$ i $y=kx^2$ has vist que el valor candidat és $0$, però això encara no et garanteix l’existència del límit. Si només saps què passa en alguns camins, què et falta per poder aplicar la definició de límit de la Funció, com a la Definició 6 del Tema 2?

**2. ALUMNE:** Què vol dir exactament que un límit existeixi?
**TUTOR** [explicar_concepte, pista 2, intents 1, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T2.6']]: Dir que un límit existeix vol dir que, quan t’acostes al punt, els valors de la funció es poden fer tan propers com vulguis d’un únic nombre $b$, independentment del camí que segueixis; això és exactament la idea de la Definició 6 del Tema 2. En dues variables, això implica que tots els camins admissibles han de donar el mateix valor candidat, però encara cal justificar-ho amb una fita que controli el mòdul de l’expressió. Vols que t’expliqui com es fa aquesta fita en aquest exercici?

**3. ALUMNE:** No sé com fitar-ho. Digues-me la solució, si us plau.
**TUTOR** [pista, pista 3, intents 1, diag demana_solucio/[] vs demana_solucio/None, refs []]: Molt bé: ja tens el candidat $0$, i ara toca justificar que el quocient queda controlat per una quantitat que també vagi a $0$. Com que $x^4+y^2\ge x^4$ i tots dos termes del denominador són no negatius, pots mirar el mòdul i escriure una desigualtat del tipus $\frac{|x|^5}{x^4+y^2}\le \frac{|x|^5}{x^4}$ quan $x\neq 0$; què et dona això després de simplificar?

**4. ALUMNE:** Com que $x^4\le x^4+y^2$, tinc $|f|\le\frac{|x|^5}{x^4}=|x|\to0$, i pel sandvitx el límit és $0$.
**TUTOR** [tancar, pista 0, intents 1, diag proposa_resultat/[] vs proposa_resultat/None, refs []]: Perfecte: has justificat bé que el límit és $0$. La idea clau ha estat acotar $|f(x,y)|$ per $|x|$ i després aplicar el sandvitx, de manera que queda controlat quan $(x,y)\to(0,0)$.

## t4-8
**1. ALUMNE:** Calculo el jacobià: $\det JG=3+6z$, que a $(1,-1,2)$ val $15$.
**TUTOR** [pista, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Bé, ja has trobat que el jacobià és invertible al punt, i ara el que falta és situar quina parella de punts estàs usant per a la inversa local. Pots comprovar si $G(1,-1,2)=(4,4,-1)$?

**2. ALUMNE:** Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?
**TUTOR** [questionar_error, pista 1, intents 1, diag pregunta_conceptual/['punt_equivocat'] vs mostra_treball/punt_equivocat, refs ['T4.5']]: Pensa en què significa exactament $DG^{-1}(4,4,-1)$ segons el Teorema 5 del Tema 4: aquest punt és on s’avalua la inversa, no la funció $G$ mateixa. Quin és, doncs, el punt del domini de $G$ que has de fer servir per calcular $JG$?

**3. ALUMNE:** Què diu exactament el teorema de la funció inversa?
**TUTOR** [explicar_concepte, pista 2, intents 2, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T4.5']]: El Teorema 5 del Tema 4 diu que, si una funció $f$ és prou regular i el seu jacobià té determinant no nul en un punt $a$, llavors existeix una inversa local al voltant d’aquell punt i aquesta inversa també és diferenciable. A més, la derivada de la inversa en un punt de la imatge es calcula com la inversa de la derivada de $f$ en el punt original corresponent, és a dir, al punt on $f$ “envia” aquell valor. Com ho voldries aplicar ara al teu exercici?

**4. ALUMNE:** Com que té inversa local a tot arreu on $3+6z\neq0$, $G$ té inversa global.
**TUTOR** [questionar_error, pista 2, intents 1, diag proposa_resultat/['local_implica_global'] vs proposa_resultat/local_implica_global, refs ['T4.5', 'T4.9']]: Bé, el Teorema 5 del Tema 4 et dona inversa local al voltant d’un punt, però per parlar d’inversa global cal una propietat més forta de la funció sencera. Si la inversa existís a tot $\mathbb{R}^3$, quina condició hauria de complir $G$ com a aplicació global segons la Definició 9 del Tema 4?

## t6-3a
**1. ALUMNE:** No sé per on començar.
**TUTOR** [pista, pista 2, intents 1, diag frustracio/[] vs demana_pista/None, refs ['T2.23']]: Pots començar mirant si el conjunt $x^2+2y^2=3$ és tancat i fitat; si ho és, per Heine-Borel és compacte. Després, com que $f(x,y)=x$ és contínua, pots aplicar el Teorema 23 del Tema 2 per garantir que hi ha màxim i mínim absoluts sobre aquest lligam. Ho pots justificar així abans de buscar els punts on s’assoleixen?

**2. ALUMNE:** Sobre l'el·lipse $x^2=3-2y^2\le3$, així que $|x|\le\sqrt3$.
**TUTOR** [validar_i_avancar, pista 2, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs ['T1.34', 'T2.23']]: Sí, això és un bon començament: has acotat $x$ sobre el lligam, i de fet veus que el conjunt no pot “escapar-se” en aquesta direcció. Per acabar de justificar l’existència dels extrems, et falta mirar si l’el·lipse és també tancada i si $f(x,y)=x$ és contínua; amb això podries aplicar el Teorema 34 del Tema 1 i el Teorema 23 del Tema 2. Ho pots comprovar?

**3. ALUMNE:** Per tant el màxim és $\sqrt3$ i el mínim $-\sqrt3$.
**TUTOR** [demanar_justificacio, pista 2, intents 1, diag proposa_resultat/[] vs proposa_resultat/None, refs ['T1.34', 'T2.23']]: Sí, el valor que proposes encaixa amb la cota que ja has trobat per a $x$, així que vas pel bon camí. Ara et falta justificar per què pots assegurar que aquests extrems existeixen sobre el lligam: has de veure que l’el·lipse és tancada i fitada, i que $f(x,y)=x$ és contínua. Si ho ajuntes amb el Teorema 34 del Tema 1 i el Teorema 23 del Tema 2, tens la justificació d’existència. Ho pots escriure així?

**4. ALUMNE:** S'assoleixen a $(\sqrt3,0)$ i $(-\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.
**TUTOR** [tancar, pista 0, intents 1, diag proposa_resultat/[] vs proposa_resultat/None, refs []]: Molt bé: el resultat és correcte, amb màxim absolut $\sqrt3$ a $(\sqrt3,0)$ i mínim absolut $-\sqrt3$ a $(-\sqrt3,0)$. La idea clau ha estat acotar $x$ sobre el lligam i veure que l’igualtat només passa quan $y=0$, cosa que identifica directament els punts on s’assoleixen els extrems.

## t3-5
**1. ALUMNE:** Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag mostra_treball/['nomes_rectes'] vs proposa_resultat/nomes_rectes, refs []]: I si proves de mirar l’origen amb un camí que no sigui una recta, com per exemple una corba on $y$ i $x$ es relacionin d’una altra manera: el límit seguiria sent $0$?

**2. ALUMNE:** A l'origen, $D_vf(0,0)=\lim_{t\to0}\frac{f(tv)}{t}=\frac{v_1^2}{v_2}$ si $v_2\neq0$. Com que existeixen totes, $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['direccionals_implica_continuitat'] vs mostra_treball/direccionals_implica_continuitat, refs ['T3.1']]: Has calculat bé una expressió sobre la recta determinada per $v$, però què et diu exactament una derivada direccional: el comportament de $f$ en tot un entorn del punt, o només sobre aquella recta, segons la Definició 1 del Tema 3?

**3. ALUMNE:** Dona'm una pista per estudiar la continuïtat a l'origen.
**TUTOR** [pista, pista 2, intents 1, diag demana_pista/[] vs demana_pista/None, refs ['T2.20']]: El que has fet a l’origen et pot servir després, però ara et convé separar primer la zona on la fórmula és “tranquil·la”. Has vist que, quan $y\neq 0$, la funció està donada per una sola expressió i el denominador no s’anul·la; en aquest cas, què et diu la Proposició 20 del Tema 2 sobre la continuïtat en aquest obert?

**4. ALUMNE:** Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.
**TUTOR** [validar_i_avancar, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs ['T2.20']]: Sí, fora de l’eix $y=0$ ho has justificat bé amb la Proposició 20 del Tema 2. I ara, què passa si fixes un punt $(x_0,0)$ amb $x_0\neq 0$ i mires el límit de $f(x,y)$ quan $(x,y)\to(x_0,0)$ pel costat amb $y\neq 0$?

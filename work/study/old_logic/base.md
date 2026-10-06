# base

Stages: {'diagnosi': ('openai', 'gpt-5.5', 'medium'), 'resposta': ('openai', 'gpt-5.4-mini', 'low'), 'guardia': ('openai', 'gpt-5.4-mini', 'low')}

Metrics: {'turns': 16, 'failed_turns': 0, 'fallback': 0, 'drafts_per_turn': 1.12, 'draft_errors': 0, 'latex_broken': 0, 'intent_match': 13, 'error_match': 15, 'cost_usd': 0.4865, 'cost_per_turn_usd': 0.0304, 'latency_s': 9.6, 'input_tokens': 164724, 'cached_tokens': 88064, 'output_tokens': 12838}

## t2-4c
**1. ALUMNE:** He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['camins_com_a_prova'] vs proposa_resultat/camins_com_a_prova, refs ['T2.10']]: Has provat alguns camins i tots et donen $0$, i això et dona un bon candidat. Però, amb la definició de límit o amb la Proposició 10 del Tema 2, això ja n’hi ha prou per assegurar que el límit existeix, o només per proposar-ne el valor?

**2. ALUMNE:** Què vol dir exactament que un límit existeixi?
**TUTOR** [demanar_justificacio, pista 1, intents 1, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs []]: Sí, $0$ és un bon candidat, però això que has comprovat amb rectes només et diu que és compatible amb el valor del límit, no que el límit existeixi. Com ho podries justificar acotant el mòdul de $\dfrac{x^5}{x^4+y^2}$ per una expressió que tendeixi a $0$ quan $(x,y)\to(0,0)$?

**3. ALUMNE:** No sé com fitar-ho. Digues-me la solució, si us plau.
**TUTOR** [demanar_justificacio, pista 1, intents 1, diag demana_solucio/[] vs demana_solucio/None, refs []]: Sí, el valor $0$ és un bon candidat, però encara et falta justificar que realment és el límit. Podries mirar de trobar una fita per a $\left|\dfrac{x^5}{x^4+y^2}\right|$ que depengui només de $|x|$ i que vagi a $0$ quan $(x,y)\to(0,0)$?

**4. ALUMNE:** Com que $x^4\le x^4+y^2$, tinc $|f|\le\frac{|x|^5}{x^4}=|x|\to0$, i pel sandvitx el límit és $0$.
**TUTOR** [tancar, pista 0, intents 1, diag mostra_treball/[] vs proposa_resultat/None, refs []]: Molt bé: has acabat la justificació i el límit és $0$. La idea clau ha estat acotar $\left|\frac{x^5}{x^4+y^2}\right|$ per $|x|$ i després aplicar el sandvitx, de manera que la cota també tendeix a $0$.

## t4-8
**1. ALUMNE:** Calculo el jacobià: $\det JG=3+6z$, que a $(1,-1,2)$ val $15$.
**TUTOR** [pista, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Molt bé: ja tens el determinant del jacobià al punt, i el pas següent és identificar quin punt del domini correspon al valor on vols avaluar la inversa. Pots comprovar que $G(1,-1,2)$ és precisament $(4,4,-1)$?

**2. ALUMNE:** Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?
**TUTOR** [questionar_error, pista 1, intents 1, diag demana_pista/['punt_equivocat'] vs mostra_treball/punt_equivocat, refs []]: El punt $(4,4,-1)$ és del domini de $G$ o de la seva inversa? I, per tant, en quin punt s’ha d’avaluar $JG$ abans d’invertir-lo?

**3. ALUMNE:** Què diu exactament el teorema de la funció inversa?
**TUTOR** [explicar_concepte, pista 2, intents 1, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T4.5']]: El Teorema 5 del Tema 4 diu que, si $f$ és $\mathcal{C}^r$ i el jacobià és invertible en un punt $a$, aleshores hi ha una inversa local diferenciable al voltant d’aquell punt. A més, la derivada de la inversa en un punt de la imatge es calcula com $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$, és a dir, primer has d’identificar quin punt del domini va a parar a $y_0$. Com ho aplicaries per relacionar el punt $(1,-1,2)$ amb el valor on et demanen $DG^{-1}$?

**4. ALUMNE:** Com que té inversa local a tot arreu on $3+6z\neq0$, $G$ té inversa global.
**TUTOR** [questionar_error, pista 2, intents 1, diag proposa_resultat/['local_implica_global'] vs proposa_resultat/local_implica_global, refs ['T4.9']]: Vas ben encaminat amb la idea de mirar el jacobià, però per parlar d’inversa global no n’hi ha prou amb que $\det(JG)$ sigui no nul en alguns punts. Segons la Definició 9 del Tema 4, què més hauria de complir $G$ a tot $\mathbb{R}^3$ perquè tingui una inversa global?

## t6-3a
**1. ALUMNE:** No sé per on començar.
**TUTOR** [pista, pista 2, intents 1, diag demana_pista/[] vs demana_pista/None, refs ['T1.34', 'T2.23']]: El bon punt de partida és comprovar si el conjunt del lligam $x^2+2y^2=3$ és tancat i fitat; si ho és, pel Teorema 34 del Tema 1 serà compacte. Com que $f(x,y)=x$ és contínua, llavors pots aplicar el Teorema 23 del Tema 2 per garantir que hi ha màxim i mínim absoluts sobre aquest conjunt. Et sembla mirar primer si l’el·lipse del lligam és tancada i fitada?

**2. ALUMNE:** Sobre l'el·lipse $x^2=3-2y^2\le3$, així que $|x|\le\sqrt3$.
**TUTOR** [validar_i_avancar, pista 2, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs ['T1.34', 'T2.23']]: Ho has fet bé: has acotat $x$ correctament a partir del lligam, i això ja mostra que el conjunt no s’escapa a l’infinit. Ara cal completar la idea mirant també si el lligam defineix un conjunt tancat i si $f(x,y)=x$ és contínua; si totes dues coses passen, què et permet concloure el Teorema 34 del Tema 1 i el Teorema 23 del Tema 2?

**3. ALUMNE:** Per tant el màxim és $\sqrt3$ i el mínim $-\sqrt3$.
**TUTOR** [questionar_error, pista 2, intents 2, diag proposa_resultat/['fita_sense_assolir', 'sense_existencia'] vs proposa_resultat/None, refs []]: Bé, ja has trobat una fita per a $x$, i això és un bon inici per pensar en els extrems absoluts sobre el lligam. Ara bé, per assegurar que hi ha un punt on s’assoleix aquesta fita, cal mirar si el valor extrem de $x$ apareix realment en algun punt de l’el·lipse. Hi ha algun punt del lligam on $x$ prengui exactament la fita que has trobat?

**4. ALUMNE:** S'assoleixen a $(\sqrt3,0)$ i $(-\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.
**TUTOR** [tancar, pista 0, intents 1, diag proposa_resultat/[] vs proposa_resultat/None, refs []]: Perfecte: has justificat bé que el conjunt del lligam és compacte i, per Weierstrass, que $f$ té extrems absoluts; després has localitzat on s’assoleixen.  
Per tant, el màxim absolut és $\sqrt3$ a $(\sqrt3,0)$ i el mínim absolut és $-\sqrt3$ a $(-\sqrt3,0)$.  
La idea clau ha estat fitar $x$ amb el lligam i veure que la fita s’assoleix quan $y=0$.

## t3-5
**1. ALUMNE:** Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 2, diag proposa_resultat/['nomes_rectes'] vs proposa_resultat/nomes_rectes, refs []]: El que has fet bé és mirar rectes que passen per l’origen i veure què passa amb el límit sobre aquestes trajectòries, però això encara no t’assegura la continuïtat segons la definició de continuïtat. Hi ha algun camí cap a l’origen que no sigui una recta i pel qual el quocient entre $x^2$ i $y$ es comporti de manera diferent?

**2. ALUMNE:** A l'origen, $D_vf(0,0)=\lim_{t\to0}\frac{f(tv)}{t}=\frac{v_1^2}{v_2}$ si $v_2\neq0$. Com que existeixen totes, $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['direccionals_implica_continuitat'] vs mostra_treball/direccionals_implica_continuitat, refs ['T3.1']]: Penses bé en la definició de derivada direccional de la Definició 1 del Tema 3, però què et diu exactament aquest límit: el comportament de $f$ en tot un entorn del punt, o només al llarg de la recta $a+tu$?

**3. ALUMNE:** Dona'm una pista per estudiar la continuïtat a l'origen.
**TUTOR** [questionar_resultat, pista 1, intents 1, diag demana_pista/[] vs demana_pista/None, refs []]: No, aquest pas no és correcte: que existeixin derivades direccionals no implica continuïtat. Pots revisar ara si la funció és contínua en els punts amb $y\neq 0$, on l’expressió $x^2/y$ està ben definida?

**4. ALUMNE:** Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.
**TUTOR** [questionar_resultat, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs ['T2.14']]: Això no és correcte: que $f(x,y)=x^2/y$ sigui quocient de polinomis amb denominador no nul només et garanteix continuïtat quan $y\neq 0$. I als punts de l’eix amb $x_0\neq 0$, com pots revisar si $\lim_{(x,y)\to(x_0,0)} \frac{x^2}{y}$ existeix i coincideix amb $f(x_0,0)$ segons la Definició 14 del Tema 2?

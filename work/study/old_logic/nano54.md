# nano54

Stages: {'diagnosi': ('openai', 'gpt-5.4-nano', 'low'), 'resposta': ('openai', 'gpt-5.4-nano', 'low'), 'guardia': ('openai', 'gpt-5.4-nano', 'low')}

Metrics: {'turns': 16, 'failed_turns': 0, 'fallback': 2, 'drafts_per_turn': 1.5, 'draft_errors': 0, 'latex_broken': 0, 'intent_match': 9, 'error_match': 15, 'cost_usd': 0.0457, 'cost_per_turn_usd': 0.00286, 'latency_s': 8.1, 'input_tokens': 205577, 'cached_tokens': 76032, 'output_tokens': 14644}

## t2-4c
**1. ALUMNE:** He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.
**TUTOR** [questionar_error, pista 0, intents 2, diag mostra_treball/['camins_com_a_prova'] vs proposa_resultat/camins_com_a_prova, refs ['T2.6']]: És cert que mirar rectes com $y=kx$ i $y=kx^2$ et dona $0$ al llarg d’aquests camins, i per tant tens un “candidat” per al límit. Però això no et garanteix que el límit existeixi, perquè el límit s’ha de poder justificar en el sentit de la Definició 6 del Tema 2 (no només per uns quants camins). Què faria falta comprovar per estar segur que, per a qualsevol punt $(x,y)$ pròxim a $(0,0)$, el quocient s’acosta a aquest mateix valor?

**2. ALUMNE:** Què vol dir exactament que un límit existeixi?
**TUTOR** [explicar_concepte, pista 2, intents 2, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T2.6']]: Que el “límit existeixi” vol dir que, quan $x$ s’acosta a $x_0$, els valors de la funció s’apropen a un únic nombre $b$ de manera verificable: segons la Definició 6 del Tema 2, per a tot $\epsilon>0$ pots trobar un $\delta>0$ perquè si $0<d(x,x_0)<\delta$ llavors $d(f(x),b)<\epsilon$. També equival a exigir que qualsevol successió que convergeixi a $x_0$ faci que $f(x_n)$ convergeixi a $b$ (Definició 6, apartat (c)), és a dir, no pot “anar a valors diferents” segons el camí. Ara bé, tu ja tens un candidat provant alguns camins: com ho planaries per verificar-ho amb la condició d’$\epsilon$ i $\delta$ de la Definició 6 del Tema 2?

**3. ALUMNE:** No sé com fitar-ho. Digues-me la solució, si us plau.
**TUTOR** [pista, pista 3, intents 2, diag demana_solucio/[] vs demana_solucio/None, refs []]: Has trobat el candidat $0$, però ara toca justificar-lo acotant el quocient: fixa’t que $x^4\ge 0$ i $y^2\ge 0$, així que $x^4+y^2\ge x^4$. Per tant, per $x\neq 0$ pots prendre valors absoluts i comparar
$\left|\frac{x^5}{x^4+y^2}\right|\le \frac{|x|^5}{x^4}$; a partir d’aquí, què et surt exactament per aquesta última expressió, i com tractaries el cas $x=0$ (amb $y\neq 0$) per completar l’acotació?

**4. ALUMNE:** Com que $x^4\le x^4+y^2$, tinc $|f|\le\frac{|x|^5}{x^4}=|x|\to0$, i pel sandvitx el límit és $0$.
**TUTOR** [tancar, pista 0, intents 1, diag mostra_treball/[] vs proposa_resultat/None, refs ['T2.6']]: Molt bé: el teu quocient queda acotat bé i això és el que realment fa falta per justificar-ho segons la Definició 6 del Tema 2. La idea clau ha estat el sandvitx $0\le |f(x,y)|\le |x|$ (i que $|x|\to 0$ quan $(x,y)\to(0,0)$), de manera que qualsevol $\epsilon>0$ es controla triant un $\delta$.  
Per tant, el límit és $0$.

## t4-8
**1. ALUMNE:** Calculo el jacobià: $\det JG=3+6z$, que a $(1,-1,2)$ val $15$.
**TUTOR** [pista, pista 2, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Bé: ja tens que $\det JG(1,-1,2)\neq 0$, així que el teorema de la funció inversa et garanteix una inversa local diferenciable prop de $(1,-1,2)$. Ara, segons la idea del pas objectiu, has de trobar quin punt d’entrada es correspon amb la imatge que et donen: busca el $(x,y,z)$ tal que $G(x,y,z)=(4,4,-1)$. Això és el que et permetrà després avaluar $DG^{-1}(4,4,-1)$ a la “zona” on està definida. Quines equacions t’obté plantejant $x+y+z^2=4$, $x-y+z=4$ i $2x+y-z=-1$?

**2. ALUMNE:** Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?
**TUTOR** [questionar_error, pista 2, intents 1, diag pregunta_conceptual/['punt_equivocat'] vs mostra_treball/punt_equivocat, refs ['T4.5']]: Bona observació que la diferencial de la inversa es relaciona amb la inversa de la diferencial de $G$ (tal com diu el punt (iii) del Teorema 5 del Tema 4). Però abans d’invertir cap matriu, cal fixar correctament on estem avaluant: el $DG^{-1}$ s’avalua en el punt de sortida $y_0$, i després s’ha de traduir a l’antiimatge $x_0$ tal que $G(x_0)=y_0$. El punt $(4,4,-1)$ pertany al domini de $G$ o al de $G^{-1}$, i en quin punt s’hauria d’avaluar $JG$?

**3. ALUMNE:** Què diu exactament el teorema de la funció inversa?
**TUTOR** [explicar_concepte, pista 2, intents 2, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T4.5']]: Quan $\det(Jf(a))\neq 0$, el Teorema 5 del Tema 4 (funció inversa) assegura que existeix un entorn $U$ de $a$ on $f$ és injectiva i té una inversa $f^{-1}$ ben definida sobre $V=f(U)$, i a més $(Df^{-1}(y_0))$ es pot obtenir invertint la matriu $Df$ al punt on s’inverteix (concretament, a $f^{-1}(y_0)$). La idea clau és que la diferencial de la inversa s’avalua al punt de sortida $y_0$, però l’has de traduir al corresponent punt d’entrada $x_0$ tal que $f(x_0)=y_0$. Com ho faries tu, en aquest exercici, per trobar quin és aquest $x_0$ quan et donen el punt $(4,4,-1)$?

**4. ALUMNE:** Com que té inversa local a tot arreu on $3+6z\neq0$, $G$ té inversa global.
**TUTOR** [questionar_error, pista 2, intents 1, diag proposa_resultat/['local_implica_global'] vs proposa_resultat/local_implica_global, refs ['T4.5']]: Has encertat que al punt $(1,-1,2)$ tens $\det(JG)\neq 0$, així que el Teorema 5 del Tema 4 et dóna una inversa només en un entorn d’aquell punt. Per tenir una inversa global a tot $\mathbb{R}^3$, quin hauria de complir $G$ (pensem en injectivitat i en la condició de $\det(JG)$) a tot $\mathbb{R}^3$, no només a $(1,-1,2)$?

## t6-3a
**1. ALUMNE:** No sé per on començar.
**TUTOR** [pista, pista 2, intents 1, diag mostra_treball/[] vs demana_pista/None, refs ['T2.23', 'T1.34']]: Una bona manera de començar és pensar en l’existència d’extrems: aquí el lligam $x^2+2y^2=3$ defineix un conjunt de punts sobre el qual miraràs $f$. La IDEA és comprovar (sense calcular encara) si aquest conjunt és compacte i si $f$ és contínua, perquè llavors pots aplicar el Teorema de Weierstrass (Teorema 23 del Tema 2). Comprovaries que el lligam dóna un conjunt tancat i fitat (i per tant compacte per Heine-Borel, Teorema 34 del Tema 1), i com que $f(x,y)=x$ és contínua, hi haurà màxim i mínim absoluts sobre el lligam. El teu conjunt de lligam és tancat i fitat a $\mathbb{R}^2$?

**2. ALUMNE:** Sobre l'el·lipse $x^2=3-2y^2\le3$, així que $|x|\le\sqrt3$.
**TUTOR (FALLBACK)** [pista, pista 3, intents 3, diag mostra_treball/[] vs mostra_treball/None, refs []]: Centrem-nos en el pas següent: existència dels extrems. Què creus que hauries d'aconseguir ara, i com ho començaries?

**3. ALUMNE:** Per tant el màxim és $\sqrt3$ i el mínim $-\sqrt3$.
**TUTOR (FALLBACK)** [questionar_error, pista 3, intents 3, diag mostra_treball/['fita_sense_assolir'] vs proposa_resultat/None, refs []]: Hi ha algun punt de l'el·lipse on $x$ valgui exactament la fita que has trobat?


**4. ALUMNE:** S'assoleixen a $(\sqrt3,0)$ i $(-\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.
**TUTOR** [tancar, pista 0, intents 1, diag mostra_treball/[] vs proposa_resultat/None, refs []]: Perfecte: has verificat que el conjunt $M=\{x^2+2y^2=3\}$ és compacte (tancat i fitat) i que $f(x,y)=x$ és contínua, de manera que pel Teorema de Weierstrass hi ha màxim i mínim absoluts, i després has trobat on s’assoleixen amb $y=0$.  
El teu resultat és correcte: màxim absolut $\sqrt3$, assolit a $(\sqrt3,0)$; mínim absolut $-\sqrt3$, assolit a $(-\sqrt3,0)$.  
La idea clau ha estat reduir el problema a l’interval possible de $x$ dins del lligam.

## t3-5
**1. ALUMNE:** Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag mostra_treball/['nomes_rectes'] vs proposa_resultat/nomes_rectes, refs []]: Molt bé que hagis comprovat la família $y=mx$, però potser és arriscat concloure només amb això: has pensat en punts d’aproximació a l’origen que no vagin per una recta? Per exemple, quan t’acostes a $(0,0)$ amb camins on $y$ es fa molt petit en relació amb $x^2$ (i no linealment com en $y=mx$), el terme $\frac{x^2}{y}$ podria comportar-se diferent de com has vist a les rectes? Quins camins no lineals cap a l’origen et semblen naturals per provar-ho?

**2. ALUMNE:** A l'origen, $D_vf(0,0)=\lim_{t\to0}\frac{f(tv)}{t}=\frac{v_1^2}{v_2}$ si $v_2\neq0$. Com que existeixen totes, $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag mostra_treball/['direccionals_implica_continuitat'] vs mostra_treball/direccionals_implica_continuitat, refs ['T2.14']]: El que has escrit sobre la derivada direccional $D_vf(0,0)$ és coherent amb la definició: estàs mirant $f$ només sobre la recta $t\mapsto (tv_1,tv_2)$. Però una derivada direccional és un límit “dins d’una recta”, mentre que la continuïtat (Teorema 14 del Tema 2) demana un límit quan $(x,y)\to(0,0)$ des de qualsevol camí. En el teu raonament, què t’està garantit que el comportament a les rectes controla el comportament a camins no lineals? Pots proposar un camí que s’acosti a l’origen i que no quedi inclòs en cap recta $y=mx$?

**3. ALUMNE:** Dona'm una pista per estudiar la continuïtat a l'origen.
**TUTOR** [questionar_resultat, pista 1, intents 1, diag demana_pista/[] vs demana_pista/None, refs ['T2.14']]: No és correcte: l’existència de totes les derivades direccionals al punt no et permet concloure la continuïtat (Teorema 14 del Tema 2 exigeix el límit $\lim_{(x,y)\to(0,0)} f(x,y)$ quan t’hi acostes per qualsevol camí, i no només per rectes). Fixa’t que el teu raonament “les rectes controlen tot” és justament el punt feble. Pots revisar el pas objectiu i indicar en quins punts la funció és clarament contínua (per exemple, fora d’on hi ha el problema amb el denominador)? On t’assegures primer que $f$ és contínua?

**4. ALUMNE:** Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.
**TUTOR** [validar_i_avancar, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs ['T2.14', 'T3.6']]: Correcte: ja has identificat que $f(x,y)=x^2/y$ és contínua a l’obert $U=\{y\neq 0\}$, perquè hi pots escriure un quocient de polinomis amb denominador no nul. I també està bé la idea sobre les derivades direccionals a l’origen: has fet el càlcul sobre la recta $t\mapsto tv$ (Teorema 14 del Tema 2 no es pot usar per concloure continuïtat només amb això, com indica l’Observació 6 del Tema 3). Ara ens toca estudiar $f$ en punts $(x_0,0)$ amb $x_0\neq 0$: agafa un punt fix $(x_0,0)$ i prova si el límit $\lim_{(x,y)\to(x_0,0)} f(x,y)$ existeix; quin camí (no una recta des de l’origen, sinó que connecti amb $(x_0,0)$) et sembla més natural per provar-ho?

# nano+oss

Stages: {'diagnosi': ('openai', 'gpt-5.4-nano', 'low'), 'resposta': ('openrouter', 'openai/gpt-oss-20b', 'low'), 'guardia': ('openrouter', 'openai/gpt-oss-20b', 'low')}

Metrics: {'turns': 16, 'failed_turns': 0, 'fallback': 0, 'drafts_per_turn': 1.31, 'draft_errors': 0, 'latex_broken': 0, 'intent_match': 9, 'error_match': 15, 'cost_usd': 0.0169, 'cost_per_turn_usd': 0.00105, 'latency_s': 14.6, 'input_tokens': 179488, 'cached_tokens': 72198, 'output_tokens': 11894}

## t2-4c
**1. ALUMNE:** He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.
**TUTOR** [questionar_error, pista 0, intents 1, diag mostra_treball/['camins_com_a_prova'] vs proposa_resultat/camins_com_a_prova, refs []]: Has provat diversos camins i tots donen el mateix resultat. Això només et dóna un candidat per al límit, però com pots comprovar que cap altre camí podria donar un valor diferent?

**2. ALUMNE:** Què vol dir exactament que un límit existeixi?
**TUTOR** [explicar_concepte, pista 2, intents 1, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T2.6', 'T2.10']]: Un límit d’una funció multivariant es defineix com a valor que la funció s’aproxima quan el punt d’interès és trobat per qualsevol successió que tendeixi a aquest punt (Definició 6 del Tema 2).  
Per comprovar que el límit existeix, cal assegurar‑lo per totes les possibles rutes o successions que es dirigeixin cap al punt; si alguna ruta dóna un valor diferent, el límit no existeix (Proposició 10 del Tema 2).  
Com creus que podries aplicar aquesta idea per verificar el límit de la funció que tens?

**3. ALUMNE:** No sé com fitar-ho. Digues-me la solució, si us plau.
**TUTOR** [demanar_justificacio, pista 2, intents 1, diag demana_solucio/[] vs demana_solucio/None, refs []]: Gràcies per contestar $0$ com a candidat.  
Per justificar-ho, comprova com es comporta la funció quan $x^4$ i $y^2$ tenen l’ordre de magnitud igual, ja que això és on el denominador pot ser de la mateixa mida que $x^5$.  
Encara, has de demostrar que en tots aquests camins el quocient es manté limitat a $0$.  
Pots provar una ruta de la forma $y=k\,x^2$ i analitzar el comportament de la funció en aquest cas?

**4. ALUMNE:** Com que $x^4\le x^4+y^2$, tinc $|f|\le\frac{|x|^5}{x^4}=|x|\to0$, i pel sandvitx el límit és $0$.
**TUTOR** [demanar_justificacio, pista 1, intents 1, diag mostra_treball/[] vs proposa_resultat/None, refs ['T2.6']]: Bon treball amb el candidat i l’acotació!  
Per arribar al límit, has d’usar la definició de límit (Definició 6 del Tema 2) i demostrar que, independentment del camí que prengui $(x,y)\to(0,0)$, el valor de $f(x,y)$ es troba dins de qualsevol $\varepsilon$‑entorn de zero.  

Com pot aplicar la definició de manera que mostri formalment que el valor és efectivament $0$?

## t4-8
**1. ALUMNE:** Calculo el jacobià: $\det JG=3+6z$, que a $(1,-1,2)$ val $15$.
**TUTOR** [pista, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Quin és el valor de $G(1,-1,2)$ i com s’assembla amb el punt $(4,4,-1)$ on es demana la diferencial de la inversa?

**2. ALUMNE:** Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?
**TUTOR** [questionar_error, pista 1, intents 2, diag demana_pista/['punt_equivocat'] vs mostra_treball/punt_equivocat, refs []]: El punt $G(1,-1,2)$ és $G(1,-1,2)=(4,4,-1)$. Quan demanem $DG^{-1}(4,4,-1)$, en quina variable has d’avaluar la jacobiana de $G$?

**3. ALUMNE:** Què diu exactament el teorema de la funció inversa?
**TUTOR** [explicar_concepte, pista 2, intents 1, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs []]: El Teorema de la funció inversa (T4.5) estableix que, si $a$ és un punt del domini i $\det(JG(a))\neq0$, llavors la inversa de $G$ és diferentiable a la imatge $y_0=G(a)$, i la seva diferencial és l’inversa de la diferencial de $G$ al punt corresponent en el domini; és a dir, $DG^{-1}(y_0)=\big(DG(G^{-1}(y_0))\big)^{-1}$.  
Per tant, per avaluar $DG^{-1}$ en el punt $(4,4,-1)$ cal mirar en quina variable s’ha de calcular: s’empra la diferencial de $G$ a l’entrada que s’inverteix, no a l’entrada del punt de sortida.  
En el teu cas, $(4,4,-1)$ és la imatge de $(1,-1,2)$, així que s’ha d’invertir la matriu Jacobiana de $G$ al punt $(1,-1,2)$.  
Què creus que és el pas següent per trobar $DG^{-1}(4,4,-1)$?

**4. ALUMNE:** Com que té inversa local a tot arreu on $3+6z\neq0$, $G$ té inversa global.
**TUTOR** [questionar_error, pista 2, intents 2, diag mostra_treball/['local_implica_global'] vs proposa_resultat/local_implica_global, refs []]: Què hauria de complir la funció $G$ a tot $\mathbb{R}^3$ per tenir una inversa global?

## t6-3a
**1. ALUMNE:** No sé per on començar.
**TUTOR** [pista, pista 2, intents 1, diag frustracio/[] vs demana_pista/None, refs []]: Per a saber si \(f\) atén un màxim o mínim condicionat, primer comprova que el conjunt de les solucions del lligam és tancat i fitat.  
A continuació, assegura que la funció \(f(x,y)=x\) és contínua sobre aquest conjunt.  
Si el conjunt és compacte, el teorema de Weierstrass garanteix que \(f\) assumeix els seus extrems.  
Quin és el conjunt definit per \(x^{2}+2y^{2}=3\) i és efectivament tancat i fitat?

**2. ALUMNE:** Sobre l'el·lipse $x^2=3-2y^2\le3$, així que $|x|\le\sqrt3$.
**TUTOR** [pista, pista 3, intents 2, diag mostra_treball/[] vs mostra_treball/None, refs []]: Has demostrat que el conjunt $M=\{(x,y)\mid x^2+2y^2=3\}$ és tancat i fitat i que $f(x,y)=x$ és contínua.  
Per assegurar la presència d’un màxim i mínim absolut, pots aplicar el teorema de Weierstrass.  
Tens la referència teòrica que indica que una funció contínua sobre un conjunt compacte atén extrems.  
Ho has fet a nivell de C1, però quines són les coordenades del punt amb el màxim i el mínim segons aquesta teoria?

**3. ALUMNE:** Per tant el màxim és $\sqrt3$ i el mínim $-\sqrt3$.
**TUTOR** [questionar_error, pista 3, intents 1, diag proposa_resultat/['fita_sense_assolir'] vs proposa_resultat/None, refs []]: Per a confirmar que el petit que has trobat d’$\pm\sqrt3$ és realment assolit, com hauries de comprovar que el conjunt de lligam conté un punt exactament amb $x=\sqrt3$? Quin valor d’$y$ hauries de prendre?

**4. ALUMNE:** S'assoleixen a $(\sqrt3,0)$ i $(-\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.
**TUTOR** [tancar, pista 0, intents 2, diag mostra_treball/[] vs proposa_resultat/None, refs []]: Bon treball! Has demostrat correctament que \(x\) està restringit a \([-\,\sqrt3,\sqrt3]\) per laigualtat \(x^{2}=3-2y^{2}\le3\) i que és solament quan \(y=0\). Per tant, els punts \((\sqrt3,0)\) i \((-\,\sqrt3,0)\) estan a la lligadura i aconsegueixen els valors \(\sqrt3\) i \(-\,\sqrt3\), respectivament. Així, el màxim absolut és \(\sqrt3\) a \((\sqrt3,0)\) i el mínim absolut és \(-\,\sqrt3\) a \((-\,\sqrt3,0)\).

## t3-5
**1. ALUMNE:** Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 2, diag mostra_treball/['nomes_rectes'] vs proposa_resultat/nomes_rectes, refs []]: Quina podria ser una trajectòria cap a l’origen que no sigui una recta i que faci que el quocient $\dfrac{x^2}{y}$ no tendeixi a $0$?

**2. ALUMNE:** A l'origen, $D_vf(0,0)=\lim_{t\to0}\frac{f(tv)}{t}=\frac{v_1^2}{v_2}$ si $v_2\neq0$. Com que existeixen totes, $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag mostra_treball/['direccionals_implica_continuitat'] vs mostra_treball/direccionals_implica_continuitat, refs []]: Quina part del càlcul de la derivada direccional establixes que $\dfrac{v_{1}^{2}}{v_{2}}$ és el valor de $D_v f(0,0)$? És correcte pensar que això garanteix la continuïtat de $f$ a l’origen?

**3. ALUMNE:** Dona'm una pista per estudiar la continuïtat a l'origen.
**TUTOR** [questionar_resultat, pista 1, intents 1, diag demana_pista/[] vs demana_pista/None, refs []]: El resultat que proposis no és correcte. Per a comprovar la continuïtat fora de l’eix, revisa on la funció s’escriu de forma clara. Quina part de l’expressió de \(f\) indica que és contínua quan \(y\neq0\)?

**4. ALUMNE:** Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.
**TUTOR** [validar_i_avancar, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs ['T2.20']]: Has demostrat correctament que, quan \(y\neq0\), el quocient \(\frac{x^{2}}{y}\) és continu perquè és un quocient de polinomis amb denominador no nul, segons la Proposició 20 del Tema 2. Ara necessitem veure el que passa en els punts de l’eix \(y=0\) amb \(x_0\neq0\). En aquests punts, el valor de la funció és zero, però el límit quan \(y\to0\) pot dependre com evoluciona \(x\) respecte a \(y\). Què crec que hauria de verificar per establir si hi ha discontinuïtat als punts \((x_0,0)\) amb \(x_0\neq0\)?

# hybrid

Stages: {'diagnosi': ('openai', 'gpt-5.4-mini', 'low'), 'resposta': ('openrouter', 'openai/gpt-oss-20b', 'low'), 'guardia': ('openrouter', 'openai/gpt-oss-20b', 'low')}

Metrics: {'turns': 16, 'failed_turns': 0, 'fallback': 0, 'drafts_per_turn': 1.5, 'draft_errors': 0, 'latex_broken': 0, 'intent_match': 14, 'error_match': 15, 'cost_usd': 0.0514, 'cost_per_turn_usd': 0.00321, 'latency_s': 24.8, 'input_tokens': 191065, 'cached_tokens': 66553, 'output_tokens': 17380}

## t2-4c
**1. ALUMNE:** He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['camins_com_a_prova'] vs proposa_resultat/camins_com_a_prova, refs []]: Has provat diversos camins i tots donen el mateix resultat, però això només et dóna un candidat.  
Per demostrar que el límit és real, necessites assegurar-te que el quocient es manté dins d’un interval petit per a *tots* camins que es dirigeixen a $(0,0)$.  
Què hauria de passar amb un camí que no sigui ni recta ni paràbola, per exemple $y=x^3$?  
Quin resultat obtindries si substituïssis aquest camí en la funció?

**2. ALUMNE:** Què vol dir exactament que un límit existeixi?
**TUTOR** [explicar_concepte, pista 2, intents 2, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs []]: Un límit d’una funció multivariants és l’extrem que assumeix la funció quan el punt d’interès es converteix en el punt on la funció es "observa", i es formalitza amb la definició 6 del Tema 2: s’ha de demostrar que, per a qualsevol $\varepsilon>0$, existeix un $\delta>0$ tal que si $(x,y)$ està dins el ball de radi $\delta$ sobre $(0,0)$ i és diferent d’aquest punt, llavors l’absència entre el valor de la funció i el límit és menor que $\varepsilon$. Així, la prova d’un límit es basa en trobar accions que assegurin que el valor de la funció es manté dins d’un interval tan petit com vulguis en tots els camins que es dirigeixen a $(0,0)$. Tens alguna idea sobre com podries usar una desigualtat que compare el denominador amb un dels seus sumands per acotar el quocient i aconseguir la prova?

**3. ALUMNE:** No sé com fitar-ho. Digues-me la solució, si us plau.
**TUTOR** [pista, pista 3, intents 2, diag demana_solucio/[] vs demana_solucio/None, refs []]: Has trobat que per a $y=kx$ el quocient tendeix a $0$.  
Per demostrar que això és cert per a *tots* camins, intenta comparar el denominador amb un dels seus sumands.  
Per exemple, quan $x\neq0$ pots escriure  
\[
\frac{|x|^5}{x^4+y^2}\le\frac{|x|^5}{x^4}=|x|.
\]  
Què passa amb aquesta desigualtat quan $(x,y)\to(0,0)$?

**4. ALUMNE:** Com que $x^4\le x^4+y^2$, tinc $|f|\le\frac{|x|^5}{x^4}=|x|\to0$, i pel sandvitx el límit és $0$.
**TUTOR** [tancar, pista 0, intents 1, diag proposa_resultat/[] vs proposa_resultat/None, refs []]: Bon treball! Has demonstrat correctament que el candidat és $0$ i que el quocient es troba entre $0$ i $|x|$, i que $|x|\le\|(x,y)\|$, de manera que per a qualsevol $\varepsilon$ podem triar $\delta=\varepsilon$ i aconseguir el sandvitx. L’idea clau és acotar el denominador per un dels seus sumands i conduir la funció a la norma del vector, tal com has fet. El límit final és, per tant, $\displaystyle\lim_{(x,y)\to(0,0)}\frac{x^5}{x^4+y^2}=0$.

## t4-8
**1. ALUMNE:** Calculo el jacobià: $\det JG=3+6z$, que a $(1,-1,2)$ val $15$.
**TUTOR** [validar_i_avancar, pista 1, intents 2, diag mostra_treball/[] vs mostra_treball/None, refs []]: Has calculat correctament la jacobiana i la seva determinació; el teu càlcul mostra que a $(1,-1,2)$ el determinant és diferent de zero, cosa que compleix el requisit del teorema de la funció inversa. Això garanteix la existència de l’inversa local.  

Seguent un pas, quina relació estableixes entre el punt $(1,-1,2)$ i el punt $G(1,-1,2)$ que et demanen?

**2. ALUMNE:** Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?
**TUTOR** [questionar_error, pista 1, intents 1, diag pregunta_conceptual/['punt_equivocat'] vs mostra_treball/punt_equivocat, refs []]: Quin és el punt $x_0$ tal que $G(x_0)=(4,4,-1)$? i en quin punt s’ha de calcular $J G$ per trobar $DG^{-1}(4,4,-1)$?

**3. ALUMNE:** Què diu exactament el teorema de la funció inversa?
**TUTOR** [explicar_concepte, pista 2, intents 1, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs []]: El teorema de la funció inversa (T4.5) estableix que, si a un punt \(a\) el determinant de la jacobiana és diferent de zero, existeix un entorn \(U\) de \(a\) tal que la funció és injectiva i la seva inversa és de classe \(C^r\).  
A més, la diferencial de la inversa en un punt \(y_0\) és l’invers de la diferencial de la funció original al punt \(x_0=f^{-1}(y_0)\).  
Quin és el punt \(x_0\) que s’inverteix per obtenir \(DG^{-1}(4,4,-1)\)?

**4. ALUMNE:** Com que té inversa local a tot arreu on $3+6z\neq0$, $G$ té inversa global.
**TUTOR** [questionar_error, pista 2, intents 1, diag proposa_resultat/['local_implica_global'] vs proposa_resultat/local_implica_global, refs []]: Els passos que has fet fins ara són correctes; has establert que a \((1,-1,2)\) el determinant de la jacobiana de \(G\) és diferent de zero i, per tant, el teorema de la funció inversa garanteix una inversa local. En la pràctica, quan necessitem la diferencial de l’inversa a un punt de sortida, hem de recuperar el punt del domini que s’obra en aquest valor de sortida. Per detectar si la funció \(G\) té inversa global, què hauria de complir \(G\) a tot \(\mathbb{R}^3\) que garanteixi que sigui bijectiva i que el determinant de la jacobiana sigui diferent de zero en cada punt?

## t6-3a
**1. ALUMNE:** No sé per on començar.
**TUTOR** [pista, pista 2, intents 1, diag demana_pista/[] vs demana_pista/None, refs []]: Per a comprovar l'existència d'extrems condicionats, comença per analitzar el conjunt definit pel lligam \(x^{2}+2y^{2}=3\). Aquesta és una el·lipse, per tant és tancada i fitada, i per tant compacte segons el Teorema de Heine‑Borel (T1.34). La funció \(f(x,y)=x\) és contínua, així que el teorema de Weierstrass (T2.23) garanteix que \(f\) assoleix un màxim i un mínim sobre aquesta el·lipse. Quins valors d' \(x\) i \(y\) satisfan aquest lligam i maximitzen/minimitzen \(x\)?

**2. ALUMNE:** Sobre l'el·lipse $x^2=3-2y^2\le3$, així que $|x|\le\sqrt3$.
**TUTOR** [validar_i_avancar, pista 2, intents 3, diag mostra_treball/[] vs mostra_treball/None, refs []]: Has fet bé el pas de determinar que l’el·lipse és tancada i fitada, i que per tant és compacte (T1.34). També has reconegut que la funció \(f(x,y)=x\) és contínua, de manera que, segons el Teorema de Weierstrass (T2.23), \(f\) assolirà un màxim i un mínim sobre aquest conjunt.  

Quin és el següent pas que has de fer per trobar els valors de \(x\) i \(y\) que maximitzen i minimitzen \(x\) dins l’el·lipse?

**3. ALUMNE:** Per tant el màxim és $\sqrt3$ i el mínim $-\sqrt3$.
**TUTOR** [questionar_error, pista 2, intents 2, diag proposa_resultat/['fita_sense_assolir'] vs proposa_resultat/None, refs []]: Has comprovat que l’ellipses és tancada i fitada i que \(f\) és contínua?  
Hi ha algun punt de l’ellipses on el valor de \(x\) sigui exactament \(\sqrt{3}\) (o \(-\sqrt{3}\))?

**4. ALUMNE:** S'assoleixen a $(\sqrt3,0)$ i $(-\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.
**TUTOR** [tancar, pista 0, intents 1, diag proposa_resultat/[] vs proposa_resultat/None, refs []]: Bé fet! Has mostrat correctament que l’ellipses \(M=\{x^2+2y^2=3\}\) és compacte i que la funció \(f(x,y)=x\) és contínua, de manera que perquè es
parsa el teorema de Weierstrass. Has evidenciat que \(x\) està limitada a \([-\,\sqrt3,\sqrt3]\) i que el límit s’assoleix només quan \(y=0\). Així, els extrems assolits són a \((\sqrt3,0)\) i \((-\,\sqrt3,0)\) amb \(f_{\max}=\sqrt3\) i \(f_{\min}=-\sqrt3\). La clau va ser la base de la frontera i la desigualtat \(-\sqrt3\le x\le\sqrt3\).

## t3-5
**1. ALUMNE:** Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 2, diag proposa_resultat/['nomes_rectes'] vs proposa_resultat/nomes_rectes, refs []]: Has comprovat si hi ha altres camins cap a l’origen que no siguin rectes, on el comportament de $x^2/y$ pot diferir del que veus a les rectes $y=mx$?

**2. ALUMNE:** A l'origen, $D_vf(0,0)=\lim_{t\to0}\frac{f(tv)}{t}=\frac{v_1^2}{v_2}$ si $v_2\neq0$. Com que existeixen totes, $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 2, diag proposa_resultat/['direccionals_implica_continuitat'] vs mostra_treball/direccionals_implica_continuitat, refs []]: Què et diu exactament una derivada direccional: el comportament de $f$ en tot un entorn, o només sobre una recta?

**3. ALUMNE:** Dona'm una pista per estudiar la continuïtat a l'origen.
**TUTOR** [pista, pista 2, intents 1, diag demana_pista/[] vs demana_pista/None, refs ['T2.14']]: Para estudiar la continuïtat fora de l’eix, pensa que on $y\neq0$ només fer el càlcul
\(f(x,y)=x^2/y\), una funció que és contínua perquè és una fracció de polinomis
d’on $y\ne0$. Aquesta és la teva estratègia: comprova la continuïtat en un
entorn on el denominador no s’anul·la. Segons la Definició 14 del Tema 2, això assegura
continuïtat en aquest conjunt. Pregunta: quin patró de camí pot mostrar que $f$,
malgrat tenir totes les derivades direccionals a l’origen, no és contínua aquí?

**4. ALUMNE:** Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.
**TUTOR** [validar_i_avancar, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Bon treball confirmant la continuïtat fora del eix i la existència de totes les derivades direccionals a l’origen. Ara, per a un punt \((x_{0},0)\) amb \(x_{0}\neq0\), com pot sorgir una discontinuïtat? Quins passejades hi ha de considerar per comprovar si \(\lim_{(x,y)\to(x_{0},0)}f(x,y)\) coincideix amb \(f(x_{0},0)=0\)?

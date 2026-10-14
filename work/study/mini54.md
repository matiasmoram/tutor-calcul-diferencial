# mini54

Stages: {'diagnosis': ['openai', 'gpt-5.4-mini', 'low'], 'reply': ['openai', 'gpt-5.4-mini', 'low'], 'guard': ['openai', 'gpt-5.4-mini', 'low']}

Metrics: {'turns': 16, 'failed_turns': 0, 'fallback': 0, 'drafts_per_turn': 1.31, 'draft_errors': 0, 'latex_broken': 0, 'intent_match': 12, 'error_match': 15, 'cost_usd': 0.1429, 'cost_per_turn_usd': 0.00893, 'latency_s': 5.9, 'input_tokens': 220048, 'cached_tokens': 115456, 'output_tokens': 12409}

## t2-4c
**1. ALUMNE:** He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.
**TUTOR** [questionar_error, pista 0, intents 3, diag proposa_resultat/['camins_com_a_prova'] vs proposa_resultat/camins_com_a_prova, refs []]: Bona observació: has comprovat alguns camins i tots et donen el mateix valor. Però això et permet concloure que el límit existeix, o només que has trobat un candidat?

**2. ALUMNE:** Què vol dir exactament que un límit existeixi?
**TUTOR** [explicar_concepte, pista 0, intents 2, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T2.6']]: Que un límit existeixi vol dir que la funció s’acosta a un valor únic quan t’hi apropes, i això s’ha de poder justificar amb la definició formal. A la Definició 6 del Tema 2, això es pot expressar amb la condició $\varepsilon$-$\delta$ o, de manera equivalent, amb successions. T’agradaria veure com es fa servir aquesta definició en el teu cas?

**3. ALUMNE:** No sé com fitar-ho. Digues-me la solució, si us plau.
**TUTOR** [pista, pista 2, intents 1, diag demana_solucio/[] vs demana_solucio/None, refs []]: Bona, ja tens un candidat i ara falta una fita que et permeti justificar-lo. Com que $x^4$ i $y^2$ són no negatius, quin dels dos sumands del denominador et convé comparar amb ell per obtenir una cota superior del quocient?

**4. ALUMNE:** Com que $x^4\le x^4+y^2$, tinc $|f|\le\frac{|x|^5}{x^4}=|x|\to0$, i pel sandvitx el límit és $0$.
**TUTOR** [tancar, pista 0, intents 1, diag mostra_treball/[] vs proposa_resultat/None, refs []]: Molt bé: la justificació és correcta i el límit és $0$. La idea clau ha estat acotar el denominador amb $x^4+y^2\ge x^4$, de manera que $\lvert f(x,y)\rvert\le \lvert x\rvert$, i així el sandvitx et dona el resultat.

## t4-8
**1. ALUMNE:** Calculo el jacobià: $\det JG=3+6z$, que a $(1,-1,2)$ val $15$.
**TUTOR** [validar_i_avancar, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs ['T4.5']]: Bé: has calculat correctament el jacobià i has vist que a $(1,-1,2)$ el determinant no s’anul·la, així que pel Teorema 5 del Tema 4 tens inversa local diferenciable en un entorn d’aquest punt. Ara, quin és el valor de $G(1,-1,2)$ per saber quin punt de l’espai d’arribada correspon a aquest entorn?

**2. ALUMNE:** Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?
**TUTOR** [explicar_concepte, pista 1, intents 1, diag pregunta_conceptual/['punt_equivocat'] vs mostra_treball/punt_equivocat, refs ['T4.5']]: No exactament: la diferencial de la inversa no es calcula al punt de partida, sinó al punt d’arribada $y_0$ on vols avaluar $f^{-1}$. Segons el Teorema 5 del Tema 4, si $y_0=f(x_0)$ i la inversa local existeix, aleshores $Df^{-1}(y_0)=\big(Df(x_0)\big)^{-1}$. Així, per trobar $DG^{-1}(y_0)$ primer has de saber quin $x_0$ es correspon amb aquest $y_0$; com ho identificaries en aquest cas?

**3. ALUMNE:** Què diu exactament el teorema de la funció inversa?
**TUTOR** [explicar_concepte, pista 1, intents 1, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T4.5']]: El Teorema 5 del Tema 4 diu que, si una funció $f$ és de classe $C^r$ i el determinant de la seva jacobiana no s’anul·la en un punt, llavors al voltant d’aquest punt hi ha un entorn on $f$ és injectiva i té una inversa local també de classe $C^r$. A més, la diferencial de la inversa en un punt de la imatge es calcula com la inversa de la diferencial de $f$ al punt preimatge corresponent. Quina relació et sembla que has d’identificar entre el punt del domini i el punt on vols avaluar la inversa?

**4. ALUMNE:** Com que té inversa local a tot arreu on $3+6z\neq0$, $G$ té inversa global.
**TUTOR** [questionar_error, pista 1, intents 1, diag proposa_resultat/['local_implica_global'] vs proposa_resultat/local_implica_global, refs ['T4.9']]: El teorema de la funció inversa et dona una inversa local en un entorn, però per passar a una inversa global necessites alguna cosa més forta. Què hauria de complir $G$ a tot $\mathbb{R}^3$ perquè sigui bijectiva, com demana la definició de difeomorfisme de la Definició 9 del Tema 4?

## t6-3a
**1. ALUMNE:** No sé per on començar.
**TUTOR** [pista, pista 2, intents 1, diag frustracio/[] vs demana_pista/None, refs []]: És normal no saber per on començar. Abans de buscar candidats, què et diu el lligam $x^2+2y^2=3$ sobre el conjunt on treballes: és tancat i fitat, i $f(x,y)=x$ és contínua?

**2. ALUMNE:** Sobre l'el·lipse $x^2=3-2y^2\le3$, així que $|x|\le\sqrt3$.
**TUTOR** [pista, pista 3, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs ['T1.34', 'T2.23']]: Bé, ja tens una part de la fita: has vist que $x$ queda fitat. Et falta mirar també què passa amb $y$ i, sobretot, decidir si el conjunt del lligam és tancat i fitat; si ho és, pel Teorema 34 del Tema 1 serà compacte. I com que $f(x,y)=x$ és contínua, què et permet concloure el Teorema 23 del Tema 2 sobre l’existència d’un màxim i un mínim absoluts?

**3. ALUMNE:** Per tant el màxim és $\sqrt3$ i el mínim $-\sqrt3$.
**TUTOR** [questionar_error, pista 3, intents 1, diag proposa_resultat/['fita_sense_assolir'] vs proposa_resultat/None, refs []]: Vas ben encaminat amb la fita de $x$, però encara falta comprovar si aquest valor es pot assolir al lligam. Hi ha algun punt de l’el·lipse on $x$ valgui exactament $\sqrt3$?

**4. ALUMNE:** S'assoleixen a $(\sqrt3,0)$ i $(-\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.
**TUTOR** [demanar_justificacio, pista 3, intents 1, diag proposa_resultat/[] vs proposa_resultat/None, refs ['T1.34', 'T2.23']]: Sí, el valor que has dit és correcte, i també has identificat bé els punts on s’assoleix. Ara et falta justificar per què podem assegurar a priori que aquests extrems existeixen sobre el lligam: què pots dir del conjunt $M=\{x^2+2y^2=3\}$ amb el Teorema 34 del Tema 1 i de $f(x,y)=x$ amb el Teorema 23 del Tema 2?

## t3-5
**1. ALUMNE:** Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag mostra_treball/['nomes_rectes'] vs proposa_resultat/nomes_rectes, refs []]: I si en lloc de seguir rectes t’hi acostes per un camí on $y$ depèn d’una altra manera de $x$, també et surt el mateix valor a l’origen?

**2. ALUMNE:** A l'origen, $D_vf(0,0)=\lim_{t\to0}\frac{f(tv)}{t}=\frac{v_1^2}{v_2}$ si $v_2\neq0$. Com que existeixen totes, $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag mostra_treball/['direccionals_implica_continuitat'] vs mostra_treball/direccionals_implica_continuitat, refs []]: Has calculat bé que les derivades direccionals a l’origen existeixen. Ara bé, què et diu exactament una derivada direccional: el comportament de $f$ en tot un entorn del punt, o només al llarg d’una recta?

**3. ALUMNE:** Dona'm una pista per estudiar la continuïtat a l'origen.
**TUTOR** [pista, pista 2, intents 3, diag demana_pista/[] vs demana_pista/None, refs []]: Bona idea mirar la continuïtat a l’origen, però abans convé separar el problema en parts. On et sembla que la funció és automàticament contínua perquè allà només hi tens una expressió coneguda, amb $y\neq 0$?

**4. ALUMNE:** Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.
**TUTOR** [validar_i_avancar, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Exacte: fora de l’eix $y=0$ tens una expressió de quocient amb denominador no nul, i per tant la funció és contínua allà. Ara bé, què passa si et fixes en un punt de l’eix, $(x_0,0)$ amb $x_0\neq 0$, i mires el límit quan $y\to 0$?

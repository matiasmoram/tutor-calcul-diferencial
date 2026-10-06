# base

Stages: {'diagnosi': ('openai', 'gpt-5.5', 'medium'), 'resposta': ('openai', 'gpt-5.4-mini', 'low'), 'guardia': ('openai', 'gpt-5.4-mini', 'low')}

Metrics: {'turns': 16, 'failed_turns': 0, 'fallback': 0, 'drafts_per_turn': 1.0, 'draft_errors': 0, 'latex_broken': 0, 'intent_match': 14, 'error_match': 14, 'cost_usd': 0.5601, 'cost_per_turn_usd': 0.03501, 'latency_s': 11.8, 'input_tokens': 164528, 'cached_tokens': 91648, 'output_tokens': 15038}

## t2-4c
**1. ALUMNE:** He provat les rectes $y=kx$ i sempre dona $0$, per tant el límit és $0$.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['camins_com_a_prova'] vs proposa_resultat/camins_com_a_prova, refs []]: Has provat alguns camins i tots et donen $0$, però això et garanteix que el límit existeix, o només et dona un candidat?

**2. ALUMNE:** Què vol dir exactament que un límit existeixi?
**TUTOR** [explicar_concepte, pista 0, intents 1, diag pregunta_conceptual/[] vs pregunta_conceptual/None, refs ['T2.6']]: Que un límit existeixi vol dir que, quan $x$ s’acosta al punt, els valors de la funció s’acosten tots al mateix nombre, sense dependre del camí que triïs; aquesta és la idea de la Definició 6 del Tema 2. Formalment, això s’expressa amb $\epsilon$ i $\delta$, o equivalentment amb successions que s’acosten al punt. Si vols, com podries usar aquesta idea per mirar el teu quocient?

**3. ALUMNE:** No sé com fitar-ho. Digues-me la solució, si us plau.
**TUTOR** [pista, pista 2, intents 1, diag demana_solucio/[] vs demana_solucio/None, refs []]: Tens ben encaminat el fet de buscar un candidat, però ara et falta una fita uniforme que no depengui del camí. Com que $x^4$ i $y^2$ són no negatius, no et sembla natural comparar $x^4+y^2$ amb un dels seus sumands per obtenir una cota superior per a $\left|\frac{x^5}{x^4+y^2}\right|$ i després veure si aquesta cota va a $0$?

**4. ALUMNE:** Com que $x^4\le x^4+y^2$, tinc $|f|\le\frac{|x|^5}{x^4}=|x|\to0$, i pel sandvitx el límit és $0$.
**TUTOR** [tancar, pista 0, intents 1, diag proposa_resultat/[] vs proposa_resultat/None, refs []]: Molt bé: la teva justificació ja tanca l’exercici, i el límit és $0$. Has fet servir la idea clau d’obtenir una cota uniforme, $0\le |f(x,y)|\le |x|$, i després aplicar el sandvitx, que és exactament el que calia.

## t4-8
**1. ALUMNE:** Calculo el jacobià: $\det JG=3+6z$, que a $(1,-1,2)$ val $15$.
**TUTOR** [pista, pista 1, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Molt bé: ja tens el punt on el jacobià no s’anul·la. Ara, quin és el valor de $G(1,-1,2)$, i coincideix amb el punt $(4,4,-1)$ on et demanen $DG^{-1}$?

**2. ALUMNE:** Llavors $DG^{-1}(4,4,-1)$ és la jacobiana de $G$ al punt $(4,4,-1)$ invertida, no?
**TUTOR** [questionar_error, pista 1, intents 1, diag pregunta_conceptual/['punt_equivocat'] vs mostra_treball/punt_equivocat, refs []]: Pensa en què significa exactament $DG^{-1}(4,4,-1)$: aquest punt és una entrada de $G$ o és la imatge d’algun punt? En quin punt has d’avaluar realment $JG$ per relacionar-lo amb la inversa local?

**3. ALUMNE:** Què diu exactament el teorema de la funció inversa?
**TUTOR** [questionar_error, pista 1, intents 1, diag pregunta_conceptual/['altre'] vs pregunta_conceptual/None, refs []]: Perfecte: ja tens identificat el punt $(1,-1,2)$ i també has calculat la seva imatge. Quan et demanen $DG^{-1}(4,4,-1)$, quin dels dos punts ha de servir-te per avaluar la jacobiana de $G$: el punt original o el punt imatge?

**4. ALUMNE:** Com que té inversa local a tot arreu on $3+6z\neq0$, $G$ té inversa global.
**TUTOR** [questionar_error, pista 1, intents 1, diag proposa_resultat/['local_implica_global'] vs proposa_resultat/local_implica_global, refs []]: El Teorema de la funció inversa et garanteix una inversa en un entorn del punt on $\det(JG)\neq 0$, però això no et diu encara res sobre tot $\mathbb{R}^3$. Si vols una inversa global, què hauria de complir $G$ a tot el domini segons la definició de difeomorfisme?

## t6-3a
**1. ALUMNE:** No sé per on començar.
**TUTOR** [pista, pista 2, intents 1, diag demana_pista/[] vs demana_pista/None, refs []]: Bé, abans de buscar candidats, el primer és veure si pots garantir que hi haurà màxim i mínim. El lligam $x^2+2y^2=3$ descriu un conjunt tancat i fitat, i $f(x,y)=x$ és contínua; això et permet aplicar el Teorema de Weierstrass del Tema 2. Et sembla que comencem comprovant aquestes dues propietats del conjunt?

**2. ALUMNE:** Sobre l'el·lipse $x^2=3-2y^2\le3$, així que $|x|\le\sqrt3$.
**TUTOR** [validar_i_avancar, pista 2, intents 1, diag mostra_treball/[] vs mostra_treball/None, refs []]: Molt bé: has fitat $x$ correctament a partir del lligam, i això ja et dona una informació útil sobre el conjunt. Ara fixa’t en la idea global: pots justificar que el conjunt $x^2+2y^2=3$ és tancat i fitat, i que $f(x,y)=x$ és contínua, per poder aplicar el Teorema de Weierstrass del Tema 2?

**3. ALUMNE:** Per tant el màxim és $\sqrt3$ i el mínim $-\sqrt3$.
**TUTOR** [questionar_error, pista 2, intents 1, diag proposa_resultat/['fita_sense_assolir', 'sense_existencia'] vs proposa_resultat/None, refs []]: La idea d’acotar $x$ està bé, i també tens el criteri per garantir extrems amb el Teorema de Weierstrass del Tema 2. Però per concloure que la fita és un extrem absolut, et falta comprovar si aquesta fita s’assoleix en algun punt del lligam. Hi ha algun punt de l’el·lipse on $x$ valgui exactament $\sqrt3$ o $-\sqrt3$?

**4. ALUMNE:** S'assoleixen a $(\sqrt3,0)$ i $(-\sqrt3,0)$, perquè quan $y=0$ tenim $x^2=3$, i l'el·lipse és compacta.
**TUTOR** [questionar_error, pista 2, intents 1, diag proposa_resultat/['sense_existencia'] vs proposa_resultat/None, refs []]: Vas ben encaminat amb la idea de l’el·lipse, però encara et falta justificar el pas que et dona dret a parlar de màxim i mínim absoluts: per aplicar el Teorema de Weierstrass del Tema 2, quin fet sobre el conjunt del lligam et cal comprovar a més que la funció $f(x,y)=x$ és contínua?

## t3-5
**1. ALUMNE:** Sobre les rectes $y=mx$ el límit a l'origen és $0$, per tant $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['nomes_rectes'] vs proposa_resultat/nomes_rectes, refs []]: Quan mires només rectes com $y=mx$, estàs comprovant tots els camins possibles cap a l’origen, o n’hi podria haver algun altre on $x^2/y$ es comporti d’una altra manera?

**2. ALUMNE:** A l'origen, $D_vf(0,0)=\lim_{t\to0}\frac{f(tv)}{t}=\frac{v_1^2}{v_2}$ si $v_2\neq0$. Com que existeixen totes, $f$ és contínua a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag proposa_resultat/['direccionals_implica_continuitat'] vs mostra_treball/direccionals_implica_continuitat, refs ['T3.1', 'T2.14']]: La teva expressió de $D_vf(0,0)$ com a límit al llarg de la recta està ben plantejada segons la Definició 1 del Tema 3, però pensa una cosa: aquest límit et diu com es comporta $f$ només sobre la recta $t\mapsto tv$, o en tots els camins que s’acosten a $(0,0)$? Quina és exactament la diferència amb el que demana la continuïtat a la Definició 14 del Tema 2?

**3. ALUMNE:** Dona'm una pista per estudiar la continuïtat a l'origen.
**TUTOR** [questionar_error, pista 0, intents 1, diag demana_pista/['altre'] vs demana_pista/None, refs []]: Si mires la continuïtat a $(0,0)$, el que has calculat sobre cada recta et garanteix el comportament de $f$ quan t’hi acostes per qualsevol camí, o només per aquests camins concrets? Què passaria si provessis un acostament diferent de $y=mx$?

**4. ALUMNE:** Fora de l'eix $y=0$ és un quocient de polinomis amb denominador no nul, així que és contínua.
**TUTOR** [questionar_error, pista 1, intents 1, diag mostra_treball/['altre'] vs mostra_treball/None, refs ['T2.20']]: Bé, ja tens justificada la continuïtat a l’obert $U=\{y\neq 0\}$ amb la Proposició 20 del Tema 2. I què passa, per exemple, en un punt de l’eix com $(x_0,0)$ amb $x_0\neq 0$ si t’hi acostes per punts amb $y\neq 0$?

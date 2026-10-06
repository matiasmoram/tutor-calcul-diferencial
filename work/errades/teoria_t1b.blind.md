## T1.26:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.26] Teorema 26 (Tema 1) — Teorema de Bolzano-Weierstrass
(Bolzano-Weierstrass.) Sigui $(M,d)$ espai mètric i $A\subseteq M$. Aleshores:
$A$ és compacte $\Leftrightarrow$ $A$ és seqüencialment compacte.
Demostració: **Demostració del teorema 26:**

$\Rightarrow$): Suposem que $A$ és compacte. Volem veure que $A$ és seqüencialment compacte. Apliquem un argument de _R.A._: sigui $(x_n)_n$ una successió d'elements $x_n\in A$ tal que no admet cap parcial convergent.

Clarament, $(x_n)_n$ no pot contenir infinites còpies d'un mateix element $x_{n_0}$ (en cas contrari, la subsuccessió o parcial $x_n=x_{n_0}$ $\forall n$ seria convergent). Definim ara la successió $(y_n)_n\subset A$ formada pels elements de $(x_n)_n$ que són diferents dos a dos; és a dir, eliminem les còpies de punts de $(x_n)_n$. Noteu que $(y_n)_n$ és una subsuccessió de $(x_n)_n$.

**Afirmació:** Existeix una successió d'oberts $(U_n)_n$, amb $U_n\subseteq M$, tal que $y_n\in U_n$ és l'únic punt de la successió $(y_n)_n$ que pertany a $U_n$.

**Demostració de l'afirmació:** Novament, per _R.A._: la successió d'oberts $(U_n)_n$ es pot construir de manera trivial considerant boles d'un determinat radi (fixat o no). El fet de suposar que l'afirmació no és certa implica que no podem construir cap successió $(U_n)_n$ tal que cada $U_n$ contingui un, i només un, punt $y_n$ de la successió $(y_n)_n$. És a dir, qualsevol d'aquestes successions $(U_n)_n$ satisfà que existeix almenys un $y_{n_0}\in U_{n_0}$ de manera que $U_{n_0}$ conté una infinitat de punts (diferents entre ells per construcció) de la successió $(y_n)_n$ a banda del punt $y_{n_0}$. En particular, això s'ha de donar també pel següent conjunt d'entorns del punt $y_{n_0}$ :

$$V_m=B_{\frac{1}{m}}(y_{n_0})\cap U_{n_0},\qquad m\geq 1.$$

Anomenem $y_m^0\in V_m\setminus\{y_{n_0}\}$ a cadascun d'aquests punts i definim la successió $(y_m^0)_m$. Del fet que $y_m^0\in V_m$ i que el radi d'aquestes boles $\frac{1}{m}\to 0$ si $m\to+\infty$, s'obté que la subsuccessió $(y_m^0)_m$ és convergent al punt $y_{n_0}\in A$. Això contradiu la hipòtesi que $(x_n)_n$ no tingui cap parcial convergent dins del conjunt $A$.

Per tant, continuant amb la demostració del teorema, podem considerar aquesta successió d'oberts $(U_n)_n$ d'$A$ que satisfà que cada $U_n$ conté un i només un element $y_n$ de la successió $(y_n)_n$.

Sigui $Y$ el conjunt format pels elements de la successió $(y_n)_n$, és a dir, $Y=\{y_1,y_2,\ldots,y_n,\ldots\}\subseteq A$. Per l'afirmació anterior, $Y$ no té punts d'acumulació. Això implica que $\overline{Y}=Y\Rightarrow Y$ és un conjunt tancat dins d'$A$. A més $\cup_{n\geq 1}U_m\ni Y$ és un recobriment d'oberts de $Y$. Pel Lema 28, car $A$ és compacte, es dedueix que $Y$ és també un compacte. En canvi, però, del recobriment $\cup_{n\geq 1}U_m$ no se'n pot extraure cap recobriment finit perquè cada obert $U_m$ conté exactament un punt diferent $y_m\in Y$ i tots són essencials. Contradicció!! Per tant, $(x_n)_n$ admet una subsuccessió convergent. Falta veure que és convergent a un punt de $A$.

En efecte, sigui $(x_{n_k})_k\subseteq(x_n)_n$ aquesta parcial convergent i sigui $x=\lim_k x_{n_k}$ el seu límit. En principi $x\in M$. Del fet que $x_{n_k}\in A$ per a tot $k\geq 1$ es dedueix, per definició de punt adherent, que $x\in\overline{A}$. Però, aplicant el Lema 28, $A$ compacte $\Rightarrow A$ tancat $\Leftrightarrow\overline{A}=A$. En conclusió, $x=\lim_k x_{n_k}\in A$.

$\Leftarrow$) : Suposem ara que $A$ és seqüencialment compacte. Vegem que aleshores és compacte.

Sigui $\bigcup_{i\in I}U_i\supseteq A$ un recobriment (de fet infinit) per oberts d'$A$. Cal veure que podem extraure un subrecobriment finit. Aleshores:

- Pel Lema 29 existeix un $\delta>0$ de manera que per a tot $a\in A$ tenim $B_\delta(a)\subseteq U_i$, per a un cert $i\in I$ (que depèn de $a$).
- Prenem ara, al Lema 30, $\varepsilon=\delta$, on $\delta>0$ és el valor trobat al punt anterior. Aleshores, tenim que existeixen $y_1,y_2,\ldots,y_r$ punts de $A$ tals que

$$A\subseteq B_\delta(y_1)\cup B_\delta(y_2)\cup\ldots\cup B_\delta(y_r)\subseteq U_{i_1}\cup U_{i_2}\cup\ldots\cup U_{i_r}.$$

És a dir, hem extret un subrecobriment finit d'$A$. Per tant, $A$ és compacte.

RESULTATS DELS APUNTS QUE CITA:
[T1.28] Lema 28 (Tema 1) — Tancat d'un compacte és compacte
Tot tancat d'un compacte és un compacte.

[T1.29] Lema 29 (Tema 1) — Nombre de Lebesgue
Sigui $A\subset M$ seqüencialment compacte i sigui $\bigcup_{i\in I}U_i\supseteq A$ un recobriment per oberts d'$A$. Aleshores, existeix $\delta>0$ tal que per a tot $a\in A$ es té que $B_\delta(a)\subseteq U_{i_0}$, per a algun $i_0=i_0(a)\in I$.

[T1.30] Lema 30 (Tema 1) — Recobriment finit per boles
Suposem que $A$ és seqüencialment compacte. Aleshores, per a tot $\varepsilon>0$, existeixen $y_1,y_2,\ldots,y_r\in A$ tals que $A\subseteq\cup_{i=1}^r B_\varepsilon(y_i)$, és a dir, $A$ està recobert per una unió finita de boles centrades en punts de $A$ i de radi $\varepsilon$.
</apunts>

### Document a revisar

[1] (enunciat) (Bolzano-Weierstrass.) Sigui $(M,d)$ espai mètric i $A\subseteq M$.
[2] (enunciat) Aleshores, $A$ és compacte si i només si $A$ és seqüencialment compacte, és a dir, si i només si tota successió $(x_n)_n\subseteq A$ és convergent a un punt de $A$.
[3] (demostració) $\Rightarrow$) Suposem que $A$ és compacte i vegem que és seqüencialment compacte. Per reducció a l'absurd, sigui $(x_n)_n$ una successió d'elements de $A$ que no admet cap parcial convergent.
[4] (demostració) La successió $(x_n)_n$ no pot contenir infinites còpies d'un mateix element (altrament, la parcial constant formada per aquestes còpies seria convergent). Eliminant les còpies repetides obtenim una subsuccessió $(y_n)_n\subseteq A$ de punts diferents dos a dos.
[5] (demostració) Afirmació: existeix una successió d'oberts $(U_n)_n$ de $M$ tal que $y_n\in U_n$ és l'únic punt de la successió $(y_n)_n$ que pertany a $U_n$.
[6] (demostració) Ho demostrem també per reducció a l'absurd: si l'afirmació no fos certa, per a qualsevol tria d'oberts $(U_n)_n$ (per exemple, boles) hi hauria un $y_{n_0}\in U_{n_0}$ tal que $U_{n_0}$ conté infinits punts de $(y_n)_n$ diferents de $y_{n_0}$. En particular, això ha de passar també per als entorns $V_m=B_{1/m}(y_{n_0})\cap U_{n_0}$, $m\geq 1$.
[7] (demostració) Triem, per a cada $m\geq 1$, un punt $y_m^0\in V_m\setminus\{y_{n_0}\}$ de la successió, amb índexs creixents. Com que $d(y_m^0,y_{n_0})<\frac{1}{m}\to 0$, la parcial $(y_m^0)_m$ convergeix a $y_{n_0}\in A$, en contradicció amb el fet que $(x_n)_n$ no admet cap parcial convergent.
[8] (demostració) Sigui $Y=\{y_1,y_2,\ldots\}\subseteq A$. Per l'afirmació, cap $y_n$ és punt d'acumulació de $Y$, i un punt d'acumulació $x\notin Y$ seria límit d'una parcial de $(y_n)_n$; per tant, $Y$ no té punts d'acumulació, $\overline{Y}=Y$ i $Y$ és tancat. Pel Lema 28, com que $A$ és compacte, $Y$ també és compacte.
[9] (demostració) Però el recobriment per oberts $Y\subseteq\bigcup_{n\geq 1}U_n$ no admet cap subrecobriment finit, ja que cada $U_n$ conté exactament un punt de $Y$ i tots són necessaris. Contradicció: per tant, $(x_n)_n$ admet una parcial convergent.
[10] (demostració) Falta veure que el límit és a $A$. Sigui $(x_{n_k})_k$ aquesta parcial i $x=\lim_k x_{n_k}\in M$. Com que $x_{n_k}\in A$ per a tot $k$, $x$ és un punt adherent d'$A$, és a dir, $x\in\overline{A}$; pel Lema 27, $A$ és tancat, d'on $\overline{A}=A$ i $x\in A$.
[11] (demostració) $\Leftarrow$) Suposem ara que $A$ és seqüencialment compacte i sigui $A\subseteq\bigcup_{i\in I}U_i$ un recobriment per oberts. Pel Lema 29, existeix $\delta>0$ tal que per a tot $a\in A$ es té $B_\delta(a)\subseteq U_i$ per a un cert $i\in I$ (que depèn de $a$).
[12] (demostració) Aplicant el Lema 30 amb $\varepsilon=\delta$, existeixen $y_1,\ldots,y_r\in A$ tals que $A\subseteq B_\delta(y_1)\cup\cdots\cup B_\delta(y_r)\subseteq U_{i_1}\cup\cdots\cup U_{i_r}$, on $U_{i_j}$ és un obert del recobriment que conté $B_\delta(y_j)$. Hem extret un subrecobriment finit i, per tant, $A$ és compacte.


## T1.26:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.26] Teorema 26 (Tema 1) — Teorema de Bolzano-Weierstrass
(Bolzano-Weierstrass.) Sigui $(M,d)$ espai mètric i $A\subseteq M$. Aleshores:
$A$ és compacte $\Leftrightarrow$ $A$ és seqüencialment compacte.
Demostració: **Demostració del teorema 26:**

$\Rightarrow$): Suposem que $A$ és compacte. Volem veure que $A$ és seqüencialment compacte. Apliquem un argument de _R.A._: sigui $(x_n)_n$ una successió d'elements $x_n\in A$ tal que no admet cap parcial convergent.

Clarament, $(x_n)_n$ no pot contenir infinites còpies d'un mateix element $x_{n_0}$ (en cas contrari, la subsuccessió o parcial $x_n=x_{n_0}$ $\forall n$ seria convergent). Definim ara la successió $(y_n)_n\subset A$ formada pels elements de $(x_n)_n$ que són diferents dos a dos; és a dir, eliminem les còpies de punts de $(x_n)_n$. Noteu que $(y_n)_n$ és una subsuccessió de $(x_n)_n$.

**Afirmació:** Existeix una successió d'oberts $(U_n)_n$, amb $U_n\subseteq M$, tal que $y_n\in U_n$ és l'únic punt de la successió $(y_n)_n$ que pertany a $U_n$.

**Demostració de l'afirmació:** Novament, per _R.A._: la successió d'oberts $(U_n)_n$ es pot construir de manera trivial considerant boles d'un determinat radi (fixat o no). El fet de suposar que l'afirmació no és certa implica que no podem construir cap successió $(U_n)_n$ tal que cada $U_n$ contingui un, i només un, punt $y_n$ de la successió $(y_n)_n$. És a dir, qualsevol d'aquestes successions $(U_n)_n$ satisfà que existeix almenys un $y_{n_0}\in U_{n_0}$ de manera que $U_{n_0}$ conté una infinitat de punts (diferents entre ells per construcció) de la successió $(y_n)_n$ a banda del punt $y_{n_0}$. En particular, això s'ha de donar també pel següent conjunt d'entorns del punt $y_{n_0}$ :

$$V_m=B_{\frac{1}{m}}(y_{n_0})\cap U_{n_0},\qquad m\geq 1.$$

Anomenem $y_m^0\in V_m\setminus\{y_{n_0}\}$ a cadascun d'aquests punts i definim la successió $(y_m^0)_m$. Del fet que $y_m^0\in V_m$ i que el radi d'aquestes boles $\frac{1}{m}\to 0$ si $m\to+\infty$, s'obté que la subsuccessió $(y_m^0)_m$ és convergent al punt $y_{n_0}\in A$. Això contradiu la hipòtesi que $(x_n)_n$ no tingui cap parcial convergent dins del conjunt $A$.

Per tant, continuant amb la demostració del teorema, podem considerar aquesta successió d'oberts $(U_n)_n$ d'$A$ que satisfà que cada $U_n$ conté un i només un element $y_n$ de la successió $(y_n)_n$.

Sigui $Y$ el conjunt format pels elements de la successió $(y_n)_n$, és a dir, $Y=\{y_1,y_2,\ldots,y_n,\ldots\}\subseteq A$. Per l'afirmació anterior, $Y$ no té punts d'acumulació. Això implica que $\overline{Y}=Y\Rightarrow Y$ és un conjunt tancat dins d'$A$. A més $\cup_{n\geq 1}U_m\ni Y$ és un recobriment d'oberts de $Y$. Pel Lema 28, car $A$ és compacte, es dedueix que $Y$ és també un compacte. En canvi, però, del recobriment $\cup_{n\geq 1}U_m$ no se'n pot extraure cap recobriment finit perquè cada obert $U_m$ conté exactament un punt diferent $y_m\in Y$ i tots són essencials. Contradicció!! Per tant, $(x_n)_n$ admet una subsuccessió convergent. Falta veure que és convergent a un punt de $A$.

En efecte, sigui $(x_{n_k})_k\subseteq(x_n)_n$ aquesta parcial convergent i sigui $x=\lim_k x_{n_k}$ el seu límit. En principi $x\in M$. Del fet que $x_{n_k}\in A$ per a tot $k\geq 1$ es dedueix, per definició de punt adherent, que $x\in\overline{A}$. Però, aplicant el Lema 28, $A$ compacte $\Rightarrow A$ tancat $\Leftrightarrow\overline{A}=A$. En conclusió, $x=\lim_k x_{n_k}\in A$.

$\Leftarrow$) : Suposem ara que $A$ és seqüencialment compacte. Vegem que aleshores és compacte.

Sigui $\bigcup_{i\in I}U_i\supseteq A$ un recobriment (de fet infinit) per oberts d'$A$. Cal veure que podem extraure un subrecobriment finit. Aleshores:

- Pel Lema 29 existeix un $\delta>0$ de manera que per a tot $a\in A$ tenim $B_\delta(a)\subseteq U_i$, per a un cert $i\in I$ (que depèn de $a$).
- Prenem ara, al Lema 30, $\varepsilon=\delta$, on $\delta>0$ és el valor trobat al punt anterior. Aleshores, tenim que existeixen $y_1,y_2,\ldots,y_r$ punts de $A$ tals que

$$A\subseteq B_\delta(y_1)\cup B_\delta(y_2)\cup\ldots\cup B_\delta(y_r)\subseteq U_{i_1}\cup U_{i_2}\cup\ldots\cup U_{i_r}.$$

És a dir, hem extret un subrecobriment finit d'$A$. Per tant, $A$ és compacte.

RESULTATS DELS APUNTS QUE CITA:
[T1.28] Lema 28 (Tema 1) — Tancat d'un compacte és compacte
Tot tancat d'un compacte és un compacte.

[T1.29] Lema 29 (Tema 1) — Nombre de Lebesgue
Sigui $A\subset M$ seqüencialment compacte i sigui $\bigcup_{i\in I}U_i\supseteq A$ un recobriment per oberts d'$A$. Aleshores, existeix $\delta>0$ tal que per a tot $a\in A$ es té que $B_\delta(a)\subseteq U_{i_0}$, per a algun $i_0=i_0(a)\in I$.

[T1.30] Lema 30 (Tema 1) — Recobriment finit per boles
Suposem que $A$ és seqüencialment compacte. Aleshores, per a tot $\varepsilon>0$, existeixen $y_1,y_2,\ldots,y_r\in A$ tals que $A\subseteq\cup_{i=1}^r B_\varepsilon(y_i)$, és a dir, $A$ està recobert per una unió finita de boles centrades en punts de $A$ i de radi $\varepsilon$.
</apunts>

### Document a revisar

[1] (enunciat) (Bolzano-Weierstrass.) Sigui $(M,d)$ espai mètric i $A\subseteq M$.
[2] (enunciat) Aleshores, $A$ és compacte si i només si $A$ és seqüencialment compacte, és a dir, si i només si tota successió $(x_n)_n\subseteq A$ admet una parcial convergent.
[3] (demostració) $\Rightarrow$) Suposem que $A$ és compacte i vegem que és seqüencialment compacte. Per reducció a l'absurd, sigui $(x_n)_n$ una successió d'elements de $A$ que no admet cap parcial convergent.
[4] (demostració) La successió $(x_n)_n$ no pot contenir infinites còpies d'un mateix element (altrament, la parcial constant formada per aquestes còpies seria convergent). Eliminant les còpies repetides obtenim una subsuccessió $(y_n)_n\subseteq A$ de punts diferents dos a dos.
[5] (demostració) Afirmació: existeix una successió d'oberts $(U_n)_n$ de $M$ tal que $y_n\in U_n$ és l'únic punt de la successió $(y_n)_n$ que pertany a $U_n$.
[6] (demostració) Ho demostrem també per reducció a l'absurd: si l'afirmació no fos certa, per a qualsevol tria d'oberts $(U_n)_n$ (per exemple, boles) hi hauria un $y_{n_0}\in U_{n_0}$ tal que $U_{n_0}$ conté infinits punts de $(y_n)_n$ diferents de $y_{n_0}$. En particular, això ha de passar també per als entorns $V_m=B_{1/m}(y_{n_0})\cap U_{n_0}$, $m\geq 1$.
[7] (demostració) Triem, per a cada $m\geq 1$, un punt $y_m^0\in V_m\setminus\{y_{n_0}\}$ de la successió, amb índexs creixents. Com que $d(y_m^0,y_{n_0})<\frac{1}{m}\to 0$, la parcial $(y_m^0)_m$ convergeix a $y_{n_0}\in A$, en contradicció amb el fet que $(x_n)_n$ no admet cap parcial convergent.
[8] (demostració) Sigui $Y=\{y_1,y_2,\ldots\}\subseteq A$. Per l'afirmació, cap $y_n$ és punt d'acumulació de $Y$, i un punt d'acumulació $x\notin Y$ seria límit d'una parcial de $(y_n)_n$; per tant, $Y$ no té punts d'acumulació, $\overline{Y}=Y$ i $Y$ és tancat. Pel Lema 28, com que $A$ és compacte, $Y$ també és compacte.
[9] (demostració) Però el recobriment per oberts $Y\subseteq\bigcup_{n\geq 1}U_n$ no admet cap subrecobriment finit, ja que cada $U_n$ conté exactament un punt de $Y$ i tots són necessaris. Contradicció: per tant, $(x_n)_n$ admet una parcial convergent.
[10] (demostració) Falta veure que el límit és a $A$. Sigui $(x_{n_k})_k$ aquesta parcial i $x=\lim_k x_{n_k}\in M$. Com que $x_{n_k}\in A$ per a tot $k$, $x$ és un punt adherent d'$A$, és a dir, $x\in\overline{A}$; pel Lema 27, $A$ és tancat, d'on $\overline{A}=A$ i $x\in A$.
[11] (demostració) $\Leftarrow$) Suposem ara que $A$ és seqüencialment compacte i sigui $A\subseteq\bigcup_{i\in I}U_i$ un recobriment per oberts. Pel Lema 29, existeix $\delta>0$ tal que per a tot $a\in A$ es té $B_\delta(a)\subseteq U_i$ per a un cert $i\in I$ (que depèn de $a$).
[12] (demostració) Aplicant el Lema 30 amb $\varepsilon=2\delta$, existeixen $y_1,\ldots,y_r\in A$ tals que $A\subseteq B_{2\delta}(y_1)\cup\cdots\cup B_{2\delta}(y_r)\subseteq U_{i_1}\cup\cdots\cup U_{i_r}$, on $U_{i_j}$ és un obert del recobriment que conté $B_{2\delta}(y_j)$. Hem extret un subrecobriment finit i, per tant, $A$ és compacte.


## T1.26:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.26] Teorema 26 (Tema 1) — Teorema de Bolzano-Weierstrass
(Bolzano-Weierstrass.) Sigui $(M,d)$ espai mètric i $A\subseteq M$. Aleshores:
$A$ és compacte $\Leftrightarrow$ $A$ és seqüencialment compacte.
Demostració: **Demostració del teorema 26:**

$\Rightarrow$): Suposem que $A$ és compacte. Volem veure que $A$ és seqüencialment compacte. Apliquem un argument de _R.A._: sigui $(x_n)_n$ una successió d'elements $x_n\in A$ tal que no admet cap parcial convergent.

Clarament, $(x_n)_n$ no pot contenir infinites còpies d'un mateix element $x_{n_0}$ (en cas contrari, la subsuccessió o parcial $x_n=x_{n_0}$ $\forall n$ seria convergent). Definim ara la successió $(y_n)_n\subset A$ formada pels elements de $(x_n)_n$ que són diferents dos a dos; és a dir, eliminem les còpies de punts de $(x_n)_n$. Noteu que $(y_n)_n$ és una subsuccessió de $(x_n)_n$.

**Afirmació:** Existeix una successió d'oberts $(U_n)_n$, amb $U_n\subseteq M$, tal que $y_n\in U_n$ és l'únic punt de la successió $(y_n)_n$ que pertany a $U_n$.

**Demostració de l'afirmació:** Novament, per _R.A._: la successió d'oberts $(U_n)_n$ es pot construir de manera trivial considerant boles d'un determinat radi (fixat o no). El fet de suposar que l'afirmació no és certa implica que no podem construir cap successió $(U_n)_n$ tal que cada $U_n$ contingui un, i només un, punt $y_n$ de la successió $(y_n)_n$. És a dir, qualsevol d'aquestes successions $(U_n)_n$ satisfà que existeix almenys un $y_{n_0}\in U_{n_0}$ de manera que $U_{n_0}$ conté una infinitat de punts (diferents entre ells per construcció) de la successió $(y_n)_n$ a banda del punt $y_{n_0}$. En particular, això s'ha de donar també pel següent conjunt d'entorns del punt $y_{n_0}$ :

$$V_m=B_{\frac{1}{m}}(y_{n_0})\cap U_{n_0},\qquad m\geq 1.$$

Anomenem $y_m^0\in V_m\setminus\{y_{n_0}\}$ a cadascun d'aquests punts i definim la successió $(y_m^0)_m$. Del fet que $y_m^0\in V_m$ i que el radi d'aquestes boles $\frac{1}{m}\to 0$ si $m\to+\infty$, s'obté que la subsuccessió $(y_m^0)_m$ és convergent al punt $y_{n_0}\in A$. Això contradiu la hipòtesi que $(x_n)_n$ no tingui cap parcial convergent dins del conjunt $A$.

Per tant, continuant amb la demostració del teorema, podem considerar aquesta successió d'oberts $(U_n)_n$ d'$A$ que satisfà que cada $U_n$ conté un i només un element $y_n$ de la successió $(y_n)_n$.

Sigui $Y$ el conjunt format pels elements de la successió $(y_n)_n$, és a dir, $Y=\{y_1,y_2,\ldots,y_n,\ldots\}\subseteq A$. Per l'afirmació anterior, $Y$ no té punts d'acumulació. Això implica que $\overline{Y}=Y\Rightarrow Y$ és un conjunt tancat dins d'$A$. A més $\cup_{n\geq 1}U_m\ni Y$ és un recobriment d'oberts de $Y$. Pel Lema 28, car $A$ és compacte, es dedueix que $Y$ és també un compacte. En canvi, però, del recobriment $\cup_{n\geq 1}U_m$ no se'n pot extraure cap recobriment finit perquè cada obert $U_m$ conté exactament un punt diferent $y_m\in Y$ i tots són essencials. Contradicció!! Per tant, $(x_n)_n$ admet una subsuccessió convergent. Falta veure que és convergent a un punt de $A$.

En efecte, sigui $(x_{n_k})_k\subseteq(x_n)_n$ aquesta parcial convergent i sigui $x=\lim_k x_{n_k}$ el seu límit. En principi $x\in M$. Del fet que $x_{n_k}\in A$ per a tot $k\geq 1$ es dedueix, per definició de punt adherent, que $x\in\overline{A}$. Però, aplicant el Lema 28, $A$ compacte $\Rightarrow A$ tancat $\Leftrightarrow\overline{A}=A$. En conclusió, $x=\lim_k x_{n_k}\in A$.

$\Leftarrow$) : Suposem ara que $A$ és seqüencialment compacte. Vegem que aleshores és compacte.

Sigui $\bigcup_{i\in I}U_i\supseteq A$ un recobriment (de fet infinit) per oberts d'$A$. Cal veure que podem extraure un subrecobriment finit. Aleshores:

- Pel Lema 29 existeix un $\delta>0$ de manera que per a tot $a\in A$ tenim $B_\delta(a)\subseteq U_i$, per a un cert $i\in I$ (que depèn de $a$).
- Prenem ara, al Lema 30, $\varepsilon=\delta$, on $\delta>0$ és el valor trobat al punt anterior. Aleshores, tenim que existeixen $y_1,y_2,\ldots,y_r$ punts de $A$ tals que

$$A\subseteq B_\delta(y_1)\cup B_\delta(y_2)\cup\ldots\cup B_\delta(y_r)\subseteq U_{i_1}\cup U_{i_2}\cup\ldots\cup U_{i_r}.$$

És a dir, hem extret un subrecobriment finit d'$A$. Per tant, $A$ és compacte.

RESULTATS DELS APUNTS QUE CITA:
[T1.28] Lema 28 (Tema 1) — Tancat d'un compacte és compacte
Tot tancat d'un compacte és un compacte.

[T1.29] Lema 29 (Tema 1) — Nombre de Lebesgue
Sigui $A\subset M$ seqüencialment compacte i sigui $\bigcup_{i\in I}U_i\supseteq A$ un recobriment per oberts d'$A$. Aleshores, existeix $\delta>0$ tal que per a tot $a\in A$ es té que $B_\delta(a)\subseteq U_{i_0}$, per a algun $i_0=i_0(a)\in I$.

[T1.30] Lema 30 (Tema 1) — Recobriment finit per boles
Suposem que $A$ és seqüencialment compacte. Aleshores, per a tot $\varepsilon>0$, existeixen $y_1,y_2,\ldots,y_r\in A$ tals que $A\subseteq\cup_{i=1}^r B_\varepsilon(y_i)$, és a dir, $A$ està recobert per una unió finita de boles centrades en punts de $A$ i de radi $\varepsilon$.
</apunts>

### Document a revisar

[1] (enunciat) (Bolzano-Weierstrass.) Sigui $(M,d)$ espai mètric i $A\subseteq M$.
[2] (enunciat) Aleshores, $A$ és compacte si i només si $A$ és seqüencialment compacte, és a dir, si i només si tota successió $(x_n)_n\subseteq M$ admet una parcial convergent a un punt de $A$.
[3] (demostració) $\Rightarrow$) Suposem que $A$ és compacte i vegem que és seqüencialment compacte. Per reducció a l'absurd, sigui $(x_n)_n$ una successió d'elements de $A$ que no admet cap parcial convergent.
[4] (demostració) La successió $(x_n)_n$ no pot contenir infinites còpies d'un mateix element (altrament, la parcial constant formada per aquestes còpies seria convergent). Eliminant les còpies repetides obtenim una subsuccessió $(y_n)_n\subseteq A$ de punts diferents dos a dos.
[5] (demostració) Afirmació: existeix una successió d'oberts $(U_n)_n$ de $M$ tal que $y_n\in U_n$ és l'únic punt de la successió $(y_n)_n$ que pertany a $U_n$.
[6] (demostració) Ho demostrem també per reducció a l'absurd: si l'afirmació no fos certa, per a qualsevol tria d'oberts $(U_n)_n$ (per exemple, boles) hi hauria un $y_{n_0}\in U_{n_0}$ tal que $U_{n_0}$ conté infinits punts de $(y_n)_n$ diferents de $y_{n_0}$. En particular, això ha de passar també per als entorns $V_m=B_{1/m}(y_{n_0})\cap U_{n_0}$, $m\geq 1$.
[7] (demostració) Triem, per a cada $m\geq 1$, un punt $y_m^0\in V_m\setminus\{y_{n_0}\}$ de la successió, amb índexs creixents. Com que $d(y_m^0,y_{n_0})<\frac{1}{m}\to 0$, la parcial $(y_m^0)_m$ convergeix a $y_{n_0}\in A$, en contradicció amb el fet que $(x_n)_n$ no admet cap parcial convergent.
[8] (demostració) Sigui $Y=\{y_1,y_2,\ldots\}\subseteq A$. Per l'afirmació, cap $y_n$ és punt d'acumulació de $Y$, i un punt d'acumulació $x\notin Y$ seria límit d'una parcial de $(y_n)_n$; per tant, $Y$ no té punts d'acumulació, $\overline{Y}=Y$ i $Y$ és tancat. Pel Lema 28, com que $A$ és compacte, $Y$ també és compacte.
[9] (demostració) Però el recobriment per oberts $Y\subseteq\bigcup_{n\geq 1}U_n$ no admet cap subrecobriment finit, ja que cada $U_n$ conté exactament un punt de $Y$ i tots són necessaris. Contradicció: per tant, $(x_n)_n$ admet una parcial convergent.
[10] (demostració) Falta veure que el límit és a $A$. Sigui $(x_{n_k})_k$ aquesta parcial i $x=\lim_k x_{n_k}\in M$. Com que $x_{n_k}\in A$ per a tot $k$, $x$ és un punt adherent d'$A$, és a dir, $x\in\overline{A}$; com que $A$ és compacte, és fitat, d'on $\overline{A}=A$ i $x\in A$.
[11] (demostració) $\Leftarrow$) Suposem ara que $A$ és seqüencialment compacte i sigui $A\subseteq\bigcup_{i\in I}U_i$ un recobriment per oberts. Pel Lema 29, existeixen $\delta>0$ i $i\in I$ tals que $B_\delta(a)\subseteq U_i$ per a tot $a\in A$.
[12] (demostració) Aplicant el Lema 30 amb $\varepsilon=\delta$, existeixen $y_1,\ldots,y_r\in A$ tals que $A\subseteq B_\delta(y_1)\cup\cdots\cup B_\delta(y_r)\subseteq U_{i_1}\cup\cdots\cup U_{i_r}$, on $U_{i_j}$ és un obert del recobriment que conté $B_\delta(y_j)$. Hem extret un subrecobriment finit i, per tant, $A$ és compacte.


## T1.27:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.27] Lema 27 (Tema 1) — Compacte implica tancat
$A$ compacte $\Rightarrow$ $A$ tancat.
Demostració: **Demostració del lema 27:** Vegem que $A^c$ és obert. Per fer-ho cal comprovar que si $x\in A^c$, aleshores existeix una bola centrada en $x$ continguda en $A^c$. Definim la següent família d'oberts:

$$U_n=\left(\overline{B}_{1/n}(x)\right)^c.$$

Observeu que:

- $U_n$ és un obert (per a tot $n\geq 1$) perquè és el complementari d'un tancat.
- Per construcció, $\overline{B}_1(x)\supset\overline{B}_{1/2}(x)\supset\overline{B}_{1/3}(x)\supset\ldots$, de forma que $U_1\subset U_2\subset U_3\subset\ldots$
- $(U_n)_n$ és un recobriment d'$A$ per oberts: $A\subseteq\bigcup_{n\in\mathbb{N}}U_n$; de fet, $\bigcup_{n\in\mathbb{N}}U_n=M\setminus\{x\}$.

Atès que $A$ és compacte, d'aquest recobriment en podem extraure un recobriment finit, és a dir, existeixen índexs $i_1,i_2,\ldots,i_r$ tals que $A\subseteq U_{i_1}\cup U_{i_2}\cup\cdots\cup U_{i_r}$. Si ordenem aquests índexs, podem suposar que $i_1\leq i_2\leq i_3\leq\ldots\leq i_r$, de manera que $U_{i_1}\subset U_{i_2}\subset U_{i_3}\subset\ldots\subset U_{i_r}$. Per tant $A\subset U_{i_r}=\left(\overline{B}_{1/i_r}(x)\right)^c$, que implica $\overline{B}_{1/i_r}(x)\subset A^c\Rightarrow B_{1/i_r}(x)\subset A^c$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $(M,d)$ espai mètric i $A\subseteq M$. Aleshores, $A$ és compacte si i només si $A$ és tancat.
[2] (demostració) Vegem que $A^c$ és obert, és a dir, que per a cada $x\in A^c$ existeix una bola centrada en $x$ continguda en $A^c$. Fixat $x\in A^c$, definim $U_n=\left(\overline{B}_{1/n}(x)\right)^c$ per a $n\geq 1$.
[3] (demostració) Cada $U_n$ és obert, perquè és el complementari d'un tancat.
[4] (demostració) Com que $\overline{B}_1(x)\supset\overline{B}_{1/2}(x)\supset\overline{B}_{1/3}(x)\supset\cdots$, prenent complementaris tenim $U_1\subset U_2\subset U_3\subset\cdots$.
[5] (demostració) A més, $\bigcup_{n\geq 1}U_n=M$, ja que tot punt de $M$ és a algun $U_n$; per tant, la família $(U_n)_n$ és un recobriment d'$A$ per oberts.
[6] (demostració) Com que $A$ és compacte, d'aquest recobriment en podem extreure un de finit: existeixen índexs $i_1\leq i_2\leq\cdots\leq i_r$ tals que $A\subseteq U_{i_1}\cup\cdots\cup U_{i_r}$ i, com que els $U_n$ són encaixats, aquesta unió és $U_{i_r}$.
[7] (demostració) Per tant, $A\subseteq U_{i_r}=\left(\overline{B}_{1/i_r}(x)\right)^c$, és a dir, $\overline{B}_{1/i_r}(x)\subseteq A^c$ i, en particular, $B_{1/i_r}(x)\subseteq A^c$. Així $A^c$ és obert i $A$ és tancat.


## T1.28:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.28] Lema 28 (Tema 1) — Tancat d'un compacte és compacte
Tot tancat d'un compacte és un compacte.
Demostració: **Demostració del lema 28:** Suposem que $B\subseteq A\subseteq M$, amb $A$ compacte i $B$ tancat. Volem veure que $B$ és compacte.

Considerem un recobriment de $B$ per oberts $U_i$ de $M$: $B\subseteq\bigcup_{i\in I}U_i\subseteq M$. Comprovem que en podem extraure un recobriment finit.

Del fet que $B$ és tancat, es deriva que $B^c\subseteq M$ és obert; llavors, usant que $B\subseteq A$, obtenim que $(\cup_{i\in I}U_i)\cup B^c$ és un recobriment per oberts d'$A$. En ser $A$ compacte, n'existeix un subrecobriment finit, és a dir: $A\subseteq U_{i_1}\cup U_{i_2}\ldots\cup U_{i_r}\cup B^c$. Però com que $B\subseteq A$, es dedueix que $B\subseteq U_{i_1}\cup U_{i_2}\cup\ldots\cup U_{i_r}$ (podem ignorar $B^c$ al recobriment ja que $B\cap B^c=\varnothing$). Per tant, $B$ admet un subrecobriment finit i, en conseqüència, és compacte.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $(M,d)$ espai mètric i $B\subseteq A\subseteq M$, amb $A$ compacte i $B$ tancat.
[2] (enunciat) Aleshores, $B$ és compacte, i també ho és $A\setminus B$.
[3] (demostració) Sigui $B\subseteq\bigcup_{i\in I}U_i$ un recobriment de $B$ per oberts $U_i$ de $M$. Cal veure que en podem extreure un subrecobriment finit.
[4] (demostració) Com que $B$ és tancat, $B^c=M\setminus B$ és obert.
[5] (demostració) Aleshores $\{U_i\}_{i\in I}\cup\{B^c\}$ és un recobriment per oberts d'$A$: els punts de $B$ són coberts pels $U_i$, i els de $A\setminus B$ pertanyen a $B^c$.
[6] (demostració) Com que $A$ és compacte, en podem extreure un subrecobriment finit: $A\subseteq U_{i_1}\cup\cdots\cup U_{i_r}\cup B^c$.
[7] (demostració) Com que $B\subseteq A$ i $B^c\subseteq A^c$, podem prescindir de $B^c$: $B\subseteq U_{i_1}\cup\cdots\cup U_{i_r}$. Per tant, $B$ és compacte.


## T1.29:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.29] Lema 29 (Tema 1) — Nombre de Lebesgue
Sigui $A\subset M$ seqüencialment compacte i sigui $\bigcup_{i\in I}U_i\supseteq A$ un recobriment per oberts d'$A$. Aleshores, existeix $\delta>0$ tal que per a tot $a\in A$ es té que $B_\delta(a)\subseteq U_{i_0}$, per a algun $i_0=i_0(a)\in I$.
Demostració: **Demostració del lema 29:** Ho provem per _R.A._: suposem que no existeix tal $\delta>0$, és a dir, que per a tot $\delta>0$ existeix $a_\delta\in A$ tal que $B_\delta(a_\delta)\not\subseteq U_i$, $\forall i\in I$. Si prenem, per exemple, una successió $(\delta_n)_n$ amb $\delta_n=\frac{1}{n}$, tenim que $\forall n\geq 1$ existeix $a_n=a_n(\delta_n)\in A$ tal que $B_{1/n}(a_n)\not\subseteq U_i$, $\forall i\in I$. Del fet que $A$ sigui seqüencialment compacte es dedueix que la successió $(a_n)_n$ admet una parcial $(a_{n_k})_k$ convergent a $A$. És a dir $a=\lim_k a_{n_k}$, amb $a\in A$. Com que $a\in A\subseteq\bigcup_{i\in I}U_i$ tenim que existeix $i_0\in I$ tal que $a\in U_{i_0}$.

Prenem ara $\varepsilon>0$ tal que $B_\varepsilon(a)\in U_{i_0}$. Sigui $K\gg 0$ de manera que

$$d(a_{n_k},a)<\frac{\varepsilon}{2}\qquad\text{i}\qquad\frac{1}{n_k}<\frac{\varepsilon}{2},\qquad\forall k\geq K.$$

Sigui $z\in B_{1/n_k}(a_{n_k})$, per a $k\geq K$. Aleshores,

$$d(z,a)\leq d(z,a_{n_k})+d(a_{n_k},a)<\frac{1}{n_k}+\frac{\varepsilon}{2}<\frac{\varepsilon}{2}+\frac{\varepsilon}{2}=\varepsilon\Rightarrow z\in B_\varepsilon(a).$$

Per tant, tenim que per a tot $k\geq K$,

$$B_{1/n_k}(a_{n_k})\subseteq B_\varepsilon(a)\subseteq U_{i_0},$$

que és una contradicció (!!) perquè estem suposant que $B_{1/n}(a_n)\not\subseteq U_i$, per a tot $i\in I$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $A\subset M$ seqüencialment compacte i sigui $\bigcup_{i\in I}U_i\supseteq A$ un recobriment per oberts d'$A$.
[2] (enunciat) Aleshores, existeixen $\delta>0$ i $i_0\in I$ tals que per a tot $a\in A$ es té $B_\delta(a)\subseteq U_{i_0}$.
[3] (demostració) Per reducció a l'absurd, suposem que per a tot $\delta>0$ existeix $a_\delta\in A$ tal que $B_\delta(a_\delta)\not\subseteq U_i$ per a tot $i\in I$. Prenent $\delta_n=\frac{1}{n}$, obtenim per a cada $n\geq 1$ un $a_n\in A$ tal que $B_{1/n}(a_n)\not\subseteq U_i$ per a tot $i\in I$.
[4] (demostració) Com que $A$ és seqüencialment compacte, $(a_n)_n$ admet una parcial $(a_{n_k})_k$ convergent a un punt $a\in A$. Com que $a\in A\subseteq\bigcup_{i\in I}U_i$, existeix $i_0\in I$ tal que $a\in U_{i_0}$.
[5] (demostració) Com que $U_{i_0}$ és obert, existeix $\varepsilon>0$ tal que $B_\varepsilon(a)\subseteq U_{i_0}$. Sigui $K$ tal que $d(a_{n_k},a)<\frac{\varepsilon}{2}$ i $\frac{1}{n_k}<\frac{\varepsilon}{2}$ per a tot $k\geq K$.
[6] (demostració) Sigui $k\geq K$ i $z\in B_{1/n_k}(a_{n_k})$. Aleshores $d(z,a)\leq d(z,a_{n_k})+d(a_{n_k},a)<\frac{1}{n_k}+\frac{\varepsilon}{2}<\frac{\varepsilon}{2}+\frac{\varepsilon}{2}=\varepsilon$, és a dir, $z\in B_\varepsilon(a)$.
[7] (demostració) Per tant, per a tot $k\geq K$, $B_\varepsilon(a)\subseteq B_{1/n_k}(a_{n_k})$ i, com que $B_\varepsilon(a)\subseteq U_{i_0}$, també $B_{1/n_k}(a_{n_k})\subseteq U_{i_0}$, que contradiu el fet que $B_{1/n}(a_n)\not\subseteq U_i$ per a tot $n$ i tot $i\in I$.


## T1.30:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.30] Lema 30 (Tema 1) — Recobriment finit per boles
Suposem que $A$ és seqüencialment compacte. Aleshores, per a tot $\varepsilon>0$, existeixen $y_1,y_2,\ldots,y_r\in A$ tals que $A\subseteq\cup_{i=1}^r B_\varepsilon(y_i)$, és a dir, $A$ està recobert per una unió finita de boles centrades en punts de $A$ i de radi $\varepsilon$.
Demostració: **Demostració del lema 30:** Ho tornem a provar per _R.A._. En efecte, suposem el contrari, és a dir, que existeix $\varepsilon_0>0$ tal que $A$ no està recobert per cap unió finita de boles de radi $\varepsilon_0$ i centre a punts d'$A$. Definim aleshores la següent successió $(y_n)_n$:

$$y_1\in A\text{ qualsevol},\qquad y_2\in A\setminus B_{\varepsilon_0}(y_1),\qquad y_3\in A\setminus\left(B_{\varepsilon_0}(y_1)\cup B_{\varepsilon_0}(y_2)\right)$$

i, en general,

$$y_k\in A\setminus\bigcup_{j=1}^{k-1}B_{\varepsilon_0}(y_j).$$

Observeu que la successió $(y_n)_n$ satisfà, per construcció que si $k>j$ llavors $d(y_k,y_j)>\varepsilon_0$. Per tant, $(y_n)_n$ no admet cap parcial convergent, que és una contradicció (!!) amb el fet que $A$ sigui seqüencialment compacte.

Abordem ara la demostració del teorema.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Suposem que $A\subseteq M$ és seqüencialment compacte. Aleshores, per a tot $\varepsilon>0$, existeixen $y_1,y_2,\ldots,y_r\in A$ tals que $A=\bigcup_{i=1}^rB_\varepsilon(y_i)$, és a dir, $A$ és una unió finita de boles de radi $\varepsilon$ centrades en punts de $A$.
[2] (demostració) Per reducció a l'absurd, suposem que existeix $\varepsilon_0>0$ tal que $A$ no està recobert per cap unió finita de boles de radi $\varepsilon_0$ centrades en punts de $A$.
[3] (demostració) Definim la successió $(y_n)_n$ així: $y_1\in A$ qualsevol, $y_2\in A\setminus B_{\varepsilon_0}(y_1)$, $y_3\in A\setminus\left(B_{\varepsilon_0}(y_1)\cup B_{\varepsilon_0}(y_2)\right)$ i, en general, $y_k\in A\setminus\bigcup_{j=1}^{k-1}B_{\varepsilon_0}(y_j)$. Aquests punts existeixen perquè les boles $B_{\varepsilon_0}(y_1),\ldots,B_{\varepsilon_0}(y_{k-1})$ no recobreixen $A$.
[4] (demostració) Per construcció, si $k>j$ aleshores $y_k\notin B_{\varepsilon_0}(y_j)$, és a dir, $d(y_k,y_j)\geq\varepsilon_0$.
[5] (demostració) Per tant, $(y_n)_n$ no és fitada i, en conseqüència, no admet cap parcial convergent, en contradicció amb el fet que $A$ és seqüencialment compacte.


## T1.31:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.31] Corol·lari 31 (Tema 1) — Propietat de l'encaixament
(Propietat de l'encaixament.) Sigui $(M,d)$ espai mètric, $M$ compacte. Sigui

$$K_1\supseteq K_2\supseteq\cdots\supseteq K_n\supseteq K_{n+1}\supseteq\ldots$$

una cadena descendent de tancats no buits. Aleshores, es té que $\displaystyle\bigcap_{n=1}^{\infty}K_n\neq\varnothing$.
Demostració: **Demostració del corol·lari 31:** D'un costat, sabem que la intersecció arbitrària de tancats és un tancat. Per tant $\bigcap_{n=1}^{+\infty}K_n$ és un tancat. Vegem que és no buit.

Fem-ho per _R.A._: suposem que $\bigcap_{n=1}^{+\infty}K_n=\varnothing$. Del fet que $K_1\supseteq K_2\supseteq\ldots\supseteq K_n\supseteq\ldots$ és una cadena de tancats encaixats es dedueix que

$$K_1^c\subseteq K_2^c\subseteq K_3^c\subseteq\ldots\subseteq\bigcup_{n=1}^{+\infty}K_n^c\tag{3}$$

és una cadena de conjunts oberts $(K_j^c)_j$ encaixats. Ara,

$$\bigcup_{n=1}^{+\infty}K_n^c=\left(\bigcap_{n=1}^{+\infty}K_n\right)^c=(\varnothing)^c=M.\tag{4}$$

Per tant, en particular, $\cup_{n=1}^{+\infty}K_n^c$ és un recobriment per oberts de $M$. Com que $M$ és compacte, en podem extraure un subrecobriment finit, és a dir, existeixen $n_1,n_2,n_3,\ldots,n_s$ tals que

$$M\subseteq K_{n_1}^c\cup K_{n_2}^c\cup\ldots\cup K_{n_s}^c.$$

A més, del fet que aquests oberts estiguin encaixats, fa que

$$M\subseteq K_{n_1}^c\cup K_{n_2}^c\cup\ldots\cup K_{n_s}^c=K_N^c,$$

on $N=\max\{n_1,n_2,\ldots,n_s\}$. Noteu que $K_N^c$ és un dels oberts a (3).

Així doncs, tenim que $M\subseteq K_N^c$. Però, a més, si usem (3) i (4), tenim també que $K_N^c\subseteq M$.

Per tant, $M=K_N^c\Rightarrow K_N=M^c=\varnothing$, que és una contradicció (!!) perquè els tancats $K_j$ són tots no buits. En conclusió, $\bigcap_{n=1}^{+\infty}K_n\neq\varnothing$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Propietat de l'encaixament.) Sigui $(M,d)$ espai mètric, $M$ complet, i sigui $K_1\supseteq K_2\supseteq\cdots\supseteq K_n\supseteq K_{n+1}\supseteq\cdots$ una cadena descendent de tancats no buits.
[2] (enunciat) Aleshores, $\bigcap_{n=1}^{\infty}K_n\neq\varnothing$.
[3] (demostració) La intersecció arbitrària de tancats és un tancat, de manera que $\bigcap_{n=1}^{\infty}K_n$ és tancat; vegem que és no buit. Per reducció a l'absurd, suposem que $\bigcap_{n=1}^{\infty}K_n=\varnothing$.
[4] (demostració) Com que $K_1\supseteq K_2\supseteq\cdots$, prenent complementaris obtenim $K_1^c\subseteq K_2^c\subseteq K_3^c\subseteq\cdots$, una cadena encaixada de conjunts oberts.
[5] (demostració) Per les lleis de De Morgan, $\bigcup_{n=1}^{\infty}K_n^c=\left(\bigcap_{n=1}^{\infty}K_n\right)^c=\varnothing^c=M$, és a dir, $(K_n^c)_n$ és un recobriment per oberts de $M$.
[6] (demostració) Com que $M$ és compacte, en podem extreure un subrecobriment finit: existeixen $n_1,\ldots,n_s$ tals que $M\subseteq K_{n_1}^c\cup\cdots\cup K_{n_s}^c$.
[7] (demostració) Com que els oberts estan encaixats, $K_{n_1}^c\cup\cdots\cup K_{n_s}^c=K_N^c$, on $N=\min\{n_1,\ldots,n_s\}$. Així $M\subseteq K_N^c\subseteq M$, és a dir, $K_N^c=M$.
[8] (demostració) Aleshores $K_N=M^c=\varnothing$, que contradiu que tots els $K_n$ són no buits. En conclusió, $\bigcap_{n=1}^{\infty}K_n\neq\varnothing$.


## T1.34:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.
Demostració: **Demostració del teorema 34:**

$\Rightarrow$) Si $A$ compacte, aleshores $A$ és seqüencialment compacte (pel Teorema de Bolzano-Weierstrass) i, en particular, es pot aplicar el Lema 30. És a dir, per a tot $\varepsilon>0$ existeixen $y_1,y_2,\ldots,y_r\in A$ tals que $A\subseteq\bigcup_{i=1}^r B(y_i,\varepsilon)$. Prenem, per exemple, $\varepsilon=1$ i definim $L=\max\{d(y_1,y_2),d(y_1,y_3),\ldots,d(y_1,y_r)\}$.

Aquest màxim està ben definit ja que el conjunt $\{y_1,y_2,\ldots,y_r\}$ és finit. Aleshores, $A\subseteq B(y_1,L+1)$ i, per tant, és fitat.

En efecte, donat $a\in A$ existeix $i\in\{1,2,\ldots,r\}$ tal que $a\in B(y_i,1)\Rightarrow d(a,y_i)<1\Rightarrow d(a,y_1)\leq d(a,y_i)+d(y_i,y_1)\leq 1+L$.

D'altra banda, pel Lema 27, sabem que si $A$ és compacte, també és tancat.

$\Leftarrow$) Suposem ara que $A\subseteq\mathbb{R}^n$ és tancat i fitat i vegem que $A$ és compacte.

A $\mathbb{R}$ (és a dir $n=1$), ja és conegut: $A$ fitat implica que tota successió $(a_n)_n\subset A$ és també fitada i, per tant, admet una parcial $(a_{n_k})_k$ convergent, amb $\lim_k a_{n_k}=a^*\in\overline{A}=A$, perquè $A$ tancat.

Vegem que també és certa a $\mathbb{R}^n$ amb $n>1$. En efecte, per a $i\in\{1,2,\ldots,n\}$, considerem $\pi_i:\mathbb{R}^n\to\mathbb{R}$ definida per $\pi_i(x)=\pi_i(x_1,x_2,\ldots,x_n)=x_i$. És a dir, $\pi_i(x)$, amb $x\in\mathbb{R}^n$, és la projecció de $x$ sobre la seva component $i$-èsima. Si $A\in\mathbb{R}^n$ és fitat $\Rightarrow$, existeix $L>0$ tal que $A\subseteq B(0,L)$. En particular, això implica que $\pi_i(A)\subseteq[-L,L]$. Fem l'argument per a $\mathbb{R}^2$ (és a dir $n=2$). Anàlogament es pot reproduir per a $n\geq 3$.

Clarament, $A\subseteq[-L,L]\times[-L,L]$ i, com que $A$ és tancat, pel lema 28, si demostrem que $[-L,L]\times[-L,L]$ és compacte, ja haurem acabat.

Fent ús del teorema 26 (Bolzano-Weierstrass), demostrarem que $[-L,L]\times[-L,L]$ és seqüencialment compacte. Així doncs, prenem $(a_n,b_n)_n$ una successió de punts de $[-L,L]\times[-L,L]$. Com que $[-L,L]$ és fitat, la successió "projecció" $(a_n)_n=\pi_1((a_n,b_n)_n)\subseteq[-L,L]$ és fitada i, per tant, admet una subsuccessió parcial $(a_{n_k})_k$ convergent a un punt $a^*\in[-L,L]$. Considerem la successió $(a_{n_k},b_{n_k})_k$, que anomenarem $(a_k',b_k')_k$ per simplificar la notació. Ja sabem que $(a_k')_k$ convergeix a $a^*$. Considerem ara la projecció sobre la segona coordenada, $(b_k')_k=\pi_2((a_k',b_k')_k)\subseteq[-L,L]$; pels mateixos arguments, admet una subsuccessió parcial $(b_{k_s})_s$ convergent a un punt $b^*\in[-L,L]$. Per tant, la parcial $(a_{k_s}',b_{k_s}')_s\xrightarrow{s\uparrow+\infty}(a^*,b^*)\in[-L,L]\times[-L,L]$. Hem demostrat, doncs, que $[-L,L]\times[-L,L]$ és seqüencialment compacte.

RESULTATS DELS APUNTS QUE CITA:
[T1.30] Lema 30 (Tema 1) — Recobriment finit per boles
Suposem que $A$ és seqüencialment compacte. Aleshores, per a tot $\varepsilon>0$, existeixen $y_1,y_2,\ldots,y_r\in A$ tals que $A\subseteq\cup_{i=1}^r B_\varepsilon(y_i)$, és a dir, $A$ està recobert per una unió finita de boles centrades en punts de $A$ i de radi $\varepsilon$.

[T1.27] Lema 27 (Tema 1) — Compacte implica tancat
$A$ compacte $\Rightarrow$ $A$ tancat.
</apunts>

### Document a revisar

[1] (enunciat) (Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$.
[2] (enunciat) Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és fitat.
[3] (demostració) $\Rightarrow$) Si $A$ és compacte, pel Teorema de Bolzano-Weierstrass és seqüencialment compacte i podem aplicar el Lema 30 amb $\varepsilon=1$: existeixen $y_1,\ldots,y_r\in A$ tals que $A\subseteq\bigcup_{i=1}^r B(y_i,1)$.
[4] (demostració) Sigui $L=\max\{d(y_1,y_2),\ldots,d(y_1,y_r)\}$, ben definit perquè el conjunt $\{y_1,\ldots,y_r\}$ és finit. Donat $a\in A$, existeix $i$ amb $d(a,y_i)<1$ i aleshores $d(a,y_1)\leq d(a,y_i)+d(y_i,y_1)<1+L$. Per tant, $A\subseteq B(y_1,L+1)$ i $A$ és fitat.
[5] (demostració) D'altra banda, pel Lema 27, com que $A$ és compacte també és tancat.
[6] (demostració) $\Leftarrow$) Suposem ara que $A\subseteq\mathbb{R}^n$ és tancat i fitat. Si $n=1$, ja és conegut: tota successió $(a_m)_m\subseteq A$ és fitada i, per tant, admet una parcial $(a_{m_k})_k$ convergent a un $a^*\in\overline{A}=A$, perquè $A$ és tancat; així $A$ és seqüencialment compacte i, pel Teorema 26, compacte.
[7] (demostració) Per a $n>1$ fem l'argument per a $n=2$ (per a $n\geq 3$ és anàleg). Com que $A$ és fitat, existeix $L>0$ tal que $A\subseteq B(0,L)$; en particular, les projeccions $\pi_i(x_1,x_2)=x_i$ satisfan $\pi_i(A)\subseteq[-L,L]$, i per tant $A\subseteq[-L,L]\times[-L,L]$.
[8] (demostració) Com que $A$ és tancat i està contingut en $[-L,L]\times[-L,L]$, pel Lema 28 n'hi ha prou de veure que $[-L,L]\times[-L,L]$ és compacte i, pel Teorema 26 (Bolzano-Weierstrass), que és seqüencialment compacte.
[9] (demostració) Sigui $(a_m,b_m)_m$ una successió de punts de $[-L,L]\times[-L,L]$. La successió $(a_m)_m\subseteq[-L,L]$ és fitada i, per tant, admet una parcial $(a_{m_k})_k$ convergent a un punt $a^*\in[-L,L]$.
[10] (demostració) La successió $(b_{m_k})_k\subseteq[-L,L]$ també és fitada i admet una parcial $(b_{m_{k_s}})_s$ convergent a un punt $b^*\in[-L,L]$; com que $(a_{m_{k_s}})_s$ és una parcial de $(a_{m_k})_k$, també convergeix a $a^*$.
[11] (demostració) Per tant, la parcial $(a_{m_{k_s}},b_{m_{k_s}})_s$ convergeix a $(a^*,b^*)\in[-L,L]\times[-L,L]$, i $[-L,L]\times[-L,L]$ és seqüencialment compacte. En conclusió, $A$ és compacte.


## T1.34:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.
Demostració: **Demostració del teorema 34:**

$\Rightarrow$) Si $A$ compacte, aleshores $A$ és seqüencialment compacte (pel Teorema de Bolzano-Weierstrass) i, en particular, es pot aplicar el Lema 30. És a dir, per a tot $\varepsilon>0$ existeixen $y_1,y_2,\ldots,y_r\in A$ tals que $A\subseteq\bigcup_{i=1}^r B(y_i,\varepsilon)$. Prenem, per exemple, $\varepsilon=1$ i definim $L=\max\{d(y_1,y_2),d(y_1,y_3),\ldots,d(y_1,y_r)\}$.

Aquest màxim està ben definit ja que el conjunt $\{y_1,y_2,\ldots,y_r\}$ és finit. Aleshores, $A\subseteq B(y_1,L+1)$ i, per tant, és fitat.

En efecte, donat $a\in A$ existeix $i\in\{1,2,\ldots,r\}$ tal que $a\in B(y_i,1)\Rightarrow d(a,y_i)<1\Rightarrow d(a,y_1)\leq d(a,y_i)+d(y_i,y_1)\leq 1+L$.

D'altra banda, pel Lema 27, sabem que si $A$ és compacte, també és tancat.

$\Leftarrow$) Suposem ara que $A\subseteq\mathbb{R}^n$ és tancat i fitat i vegem que $A$ és compacte.

A $\mathbb{R}$ (és a dir $n=1$), ja és conegut: $A$ fitat implica que tota successió $(a_n)_n\subset A$ és també fitada i, per tant, admet una parcial $(a_{n_k})_k$ convergent, amb $\lim_k a_{n_k}=a^*\in\overline{A}=A$, perquè $A$ tancat.

Vegem que també és certa a $\mathbb{R}^n$ amb $n>1$. En efecte, per a $i\in\{1,2,\ldots,n\}$, considerem $\pi_i:\mathbb{R}^n\to\mathbb{R}$ definida per $\pi_i(x)=\pi_i(x_1,x_2,\ldots,x_n)=x_i$. És a dir, $\pi_i(x)$, amb $x\in\mathbb{R}^n$, és la projecció de $x$ sobre la seva component $i$-èsima. Si $A\in\mathbb{R}^n$ és fitat $\Rightarrow$, existeix $L>0$ tal que $A\subseteq B(0,L)$. En particular, això implica que $\pi_i(A)\subseteq[-L,L]$. Fem l'argument per a $\mathbb{R}^2$ (és a dir $n=2$). Anàlogament es pot reproduir per a $n\geq 3$.

Clarament, $A\subseteq[-L,L]\times[-L,L]$ i, com que $A$ és tancat, pel lema 28, si demostrem que $[-L,L]\times[-L,L]$ és compacte, ja haurem acabat.

Fent ús del teorema 26 (Bolzano-Weierstrass), demostrarem que $[-L,L]\times[-L,L]$ és seqüencialment compacte. Així doncs, prenem $(a_n,b_n)_n$ una successió de punts de $[-L,L]\times[-L,L]$. Com que $[-L,L]$ és fitat, la successió "projecció" $(a_n)_n=\pi_1((a_n,b_n)_n)\subseteq[-L,L]$ és fitada i, per tant, admet una subsuccessió parcial $(a_{n_k})_k$ convergent a un punt $a^*\in[-L,L]$. Considerem la successió $(a_{n_k},b_{n_k})_k$, que anomenarem $(a_k',b_k')_k$ per simplificar la notació. Ja sabem que $(a_k')_k$ convergeix a $a^*$. Considerem ara la projecció sobre la segona coordenada, $(b_k')_k=\pi_2((a_k',b_k')_k)\subseteq[-L,L]$; pels mateixos arguments, admet una subsuccessió parcial $(b_{k_s})_s$ convergent a un punt $b^*\in[-L,L]$. Per tant, la parcial $(a_{k_s}',b_{k_s}')_s\xrightarrow{s\uparrow+\infty}(a^*,b^*)\in[-L,L]\times[-L,L]$. Hem demostrat, doncs, que $[-L,L]\times[-L,L]$ és seqüencialment compacte.

RESULTATS DELS APUNTS QUE CITA:
[T1.30] Lema 30 (Tema 1) — Recobriment finit per boles
Suposem que $A$ és seqüencialment compacte. Aleshores, per a tot $\varepsilon>0$, existeixen $y_1,y_2,\ldots,y_r\in A$ tals que $A\subseteq\cup_{i=1}^r B_\varepsilon(y_i)$, és a dir, $A$ està recobert per una unió finita de boles centrades en punts de $A$ i de radi $\varepsilon$.

[T1.27] Lema 27 (Tema 1) — Compacte implica tancat
$A$ compacte $\Rightarrow$ $A$ tancat.
</apunts>

### Document a revisar

[1] (enunciat) (Heine-Borel.) Sigui $(M,d)$ un espai mètric i $A\subseteq M$.
[2] (enunciat) Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.
[3] (demostració) $\Rightarrow$) Si $A$ és compacte, pel Teorema de Bolzano-Weierstrass és seqüencialment compacte i podem aplicar el Lema 30 amb $\varepsilon=1$: existeixen $y_1,\ldots,y_r\in A$ tals que $A\subseteq\bigcup_{i=1}^r B(y_i,1)$.
[4] (demostració) Sigui $L=\max\{d(y_1,y_2),\ldots,d(y_1,y_r)\}$, ben definit perquè el conjunt $\{y_1,\ldots,y_r\}$ és finit. Donat $a\in A$, existeix $i$ amb $d(a,y_i)<1$ i aleshores $d(a,y_1)\leq d(a,y_i)+d(y_i,y_1)<1+L$. Per tant, $A\subseteq B(y_1,L)$ i $A$ és fitat.
[5] (demostració) D'altra banda, pel Lema 27, com que $A$ és compacte també és tancat.
[6] (demostració) $\Leftarrow$) Suposem ara que $A\subseteq\mathbb{R}^n$ és tancat i fitat. Si $n=1$, ja és conegut: tota successió $(a_m)_m\subseteq A$ és fitada i, per tant, admet una parcial $(a_{m_k})_k$ convergent a un $a^*\in\overline{A}=A$, perquè $A$ és tancat; així $A$ és seqüencialment compacte i, pel Teorema 26, compacte.
[7] (demostració) Per a $n>1$ fem l'argument per a $n=2$ (per a $n\geq 3$ és anàleg). Com que $A$ és fitat, existeix $L>0$ tal que $A\subseteq B(0,L)$; en particular, les projeccions $\pi_i(x_1,x_2)=x_i$ satisfan $\pi_i(A)\subseteq[-L,L]$, i per tant $A\subseteq[-L,L]\times[-L,L]$.
[8] (demostració) Com que $A$ és tancat i està contingut en $[-L,L]\times[-L,L]$, pel Lema 28 n'hi ha prou de veure que $[-L,L]\times[-L,L]$ és compacte i, pel Teorema 26 (Bolzano-Weierstrass), que és seqüencialment compacte.
[9] (demostració) Sigui $(a_m,b_m)_m$ una successió de punts de $[-L,L]\times[-L,L]$. La successió $(a_m)_m\subseteq[-L,L]$ és fitada i, per tant, admet una parcial $(a_{m_k})_k$ convergent a un punt $a^*\in[-L,L]$.
[10] (demostració) La successió $(b_{m_k})_k\subseteq[-L,L]$ també és fitada i admet una parcial $(b_{m_{k_s}})_s$ convergent a un punt $b^*\in[-L,L]$; com que $(a_{m_{k_s}})_s$ és una parcial de $(a_{m_k})_k$, també convergeix a $a^*$.
[11] (demostració) Per tant, la parcial $(a_{m_{k_s}},b_{m_{k_s}})_s$ convergeix a $(a^*,b^*)\in[-L,L]\times[-L,L]$, i $[-L,L]\times[-L,L]$ és seqüencialment compacte. En conclusió, $A$ és compacte.


## T1.34:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.
Demostració: **Demostració del teorema 34:**

$\Rightarrow$) Si $A$ compacte, aleshores $A$ és seqüencialment compacte (pel Teorema de Bolzano-Weierstrass) i, en particular, es pot aplicar el Lema 30. És a dir, per a tot $\varepsilon>0$ existeixen $y_1,y_2,\ldots,y_r\in A$ tals que $A\subseteq\bigcup_{i=1}^r B(y_i,\varepsilon)$. Prenem, per exemple, $\varepsilon=1$ i definim $L=\max\{d(y_1,y_2),d(y_1,y_3),\ldots,d(y_1,y_r)\}$.

Aquest màxim està ben definit ja que el conjunt $\{y_1,y_2,\ldots,y_r\}$ és finit. Aleshores, $A\subseteq B(y_1,L+1)$ i, per tant, és fitat.

En efecte, donat $a\in A$ existeix $i\in\{1,2,\ldots,r\}$ tal que $a\in B(y_i,1)\Rightarrow d(a,y_i)<1\Rightarrow d(a,y_1)\leq d(a,y_i)+d(y_i,y_1)\leq 1+L$.

D'altra banda, pel Lema 27, sabem que si $A$ és compacte, també és tancat.

$\Leftarrow$) Suposem ara que $A\subseteq\mathbb{R}^n$ és tancat i fitat i vegem que $A$ és compacte.

A $\mathbb{R}$ (és a dir $n=1$), ja és conegut: $A$ fitat implica que tota successió $(a_n)_n\subset A$ és també fitada i, per tant, admet una parcial $(a_{n_k})_k$ convergent, amb $\lim_k a_{n_k}=a^*\in\overline{A}=A$, perquè $A$ tancat.

Vegem que també és certa a $\mathbb{R}^n$ amb $n>1$. En efecte, per a $i\in\{1,2,\ldots,n\}$, considerem $\pi_i:\mathbb{R}^n\to\mathbb{R}$ definida per $\pi_i(x)=\pi_i(x_1,x_2,\ldots,x_n)=x_i$. És a dir, $\pi_i(x)$, amb $x\in\mathbb{R}^n$, és la projecció de $x$ sobre la seva component $i$-èsima. Si $A\in\mathbb{R}^n$ és fitat $\Rightarrow$, existeix $L>0$ tal que $A\subseteq B(0,L)$. En particular, això implica que $\pi_i(A)\subseteq[-L,L]$. Fem l'argument per a $\mathbb{R}^2$ (és a dir $n=2$). Anàlogament es pot reproduir per a $n\geq 3$.

Clarament, $A\subseteq[-L,L]\times[-L,L]$ i, com que $A$ és tancat, pel lema 28, si demostrem que $[-L,L]\times[-L,L]$ és compacte, ja haurem acabat.

Fent ús del teorema 26 (Bolzano-Weierstrass), demostrarem que $[-L,L]\times[-L,L]$ és seqüencialment compacte. Així doncs, prenem $(a_n,b_n)_n$ una successió de punts de $[-L,L]\times[-L,L]$. Com que $[-L,L]$ és fitat, la successió "projecció" $(a_n)_n=\pi_1((a_n,b_n)_n)\subseteq[-L,L]$ és fitada i, per tant, admet una subsuccessió parcial $(a_{n_k})_k$ convergent a un punt $a^*\in[-L,L]$. Considerem la successió $(a_{n_k},b_{n_k})_k$, que anomenarem $(a_k',b_k')_k$ per simplificar la notació. Ja sabem que $(a_k')_k$ convergeix a $a^*$. Considerem ara la projecció sobre la segona coordenada, $(b_k')_k=\pi_2((a_k',b_k')_k)\subseteq[-L,L]$; pels mateixos arguments, admet una subsuccessió parcial $(b_{k_s})_s$ convergent a un punt $b^*\in[-L,L]$. Per tant, la parcial $(a_{k_s}',b_{k_s}')_s\xrightarrow{s\uparrow+\infty}(a^*,b^*)\in[-L,L]\times[-L,L]$. Hem demostrat, doncs, que $[-L,L]\times[-L,L]$ és seqüencialment compacte.

RESULTATS DELS APUNTS QUE CITA:
[T1.30] Lema 30 (Tema 1) — Recobriment finit per boles
Suposem que $A$ és seqüencialment compacte. Aleshores, per a tot $\varepsilon>0$, existeixen $y_1,y_2,\ldots,y_r\in A$ tals que $A\subseteq\cup_{i=1}^r B_\varepsilon(y_i)$, és a dir, $A$ està recobert per una unió finita de boles centrades en punts de $A$ i de radi $\varepsilon$.

[T1.27] Lema 27 (Tema 1) — Compacte implica tancat
$A$ compacte $\Rightarrow$ $A$ tancat.
</apunts>

### Document a revisar

[1] (enunciat) (Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$.
[2] (enunciat) Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat, és a dir, $A$ és tancat i per a tot $a\in A$ existeix $L>0$ tal que $\|a\|<L$.
[3] (demostració) $\Rightarrow$) Si $A$ és compacte, pel Teorema de Bolzano-Weierstrass és seqüencialment compacte i podem aplicar el Lema 30 amb $\varepsilon=1$: existeixen $y_1,\ldots,y_r\in A$ tals que $A\subseteq\bigcup_{i=1}^r B(y_i,1)$.
[4] (demostració) Sigui $L=\max\{d(y_1,y_2),\ldots,d(y_1,y_r)\}$, ben definit perquè el conjunt $\{y_1,\ldots,y_r\}$ és finit. Donat $a\in A$, existeix $i$ amb $d(a,y_i)<1$ i aleshores $d(a,y_1)\leq d(a,y_i)+d(y_i,y_1)<1+L$. Per tant, $A\subseteq B(y_1,L+1)$ i $A$ és fitat.
[5] (demostració) D'altra banda, pel Lema 27, com que $A$ és compacte també és tancat.
[6] (demostració) $\Leftarrow$) Suposem ara que $A\subseteq\mathbb{R}^n$ és tancat i fitat. Si $n=1$, ja és conegut: tota successió $(a_m)_m\subseteq A$ és fitada i, per tant, admet una parcial $(a_{m_k})_k$ convergent a un $a^*\in\overline{A}=A$, perquè $A$ és tancat; així $A$ és seqüencialment compacte i, pel Teorema 26, compacte.
[7] (demostració) Per a $n>1$ fem l'argument per a $n=2$ (per a $n\geq 3$ és anàleg). Com que $A$ és fitat, existeix $L>0$ tal que $A\subseteq B(0,L)$; en particular, les projeccions $\pi_i(x_1,x_2)=x_i$ satisfan $\pi_i(A)\subseteq[-L,L]$, i per tant $A\subseteq[-L,L]\times[-L,L]$.
[8] (demostració) Com que $A$ és fitat i està contingut en $[-L,L]\times[-L,L]$, pel Lema 28 n'hi ha prou de veure que $[-L,L]\times[-L,L]$ és compacte i, pel Teorema 26 (Bolzano-Weierstrass), que és seqüencialment compacte.
[9] (demostració) Sigui $(a_m,b_m)_m$ una successió de punts de $[-L,L]\times[-L,L]$. La successió $(a_m)_m\subseteq[-L,L]$ és fitada i, per tant, admet una parcial $(a_{m_k})_k$ convergent a un punt $a^*\in[-L,L]$.
[10] (demostració) La successió $(b_m)_m\subseteq[-L,L]$ també és fitada i admet una parcial $(b_{m_s})_s$ convergent a un punt $b^*\in[-L,L]$; per tant, la parcial $(a_{m_s},b_{m_s})_s$ convergeix a $(a^*,b^*)$.
[11] (demostració) Així, $[-L,L]\times[-L,L]$ és seqüencialment compacte i, en conclusió, $A$ és compacte.

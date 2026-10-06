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
[2] (enunciat) Aleshores, $A$ és compacte si i només si $A$ és seqüencialment compacte, és a dir, si i només si tota successió fitada $(x_n)_n\subseteq A$ admet una parcial convergent a un punt de $A$.
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


## t1-5b:dificil

### Referència

<solucio_de_referencia>
ENUNCIAT: Siguin $A,B$ subconjunts no buits de $\mathbb{R}^m$ i $d$ la distància euclídia. Definim $d(A,B)=\inf\{d(a,b)\mid a\in A,\ b\in B\}$.

(b) Demostreu $|d(x,A)-d(y,A)|\leq d(x,y)$, $\forall x,y\in\mathbb{R}^m$, on $d(x,A)=d(\{x\},A)$.
RESULTAT CORRECTE: Per a tot $a\in A$, $d(x,A)\leq d(x,a)\leq d(x,y)+d(y,a)$; prenent l'ínfim en $a$, $d(x,A)\leq d(x,y)+d(y,A)$, és a dir $d(x,A)-d(y,A)\leq d(x,y)$. Intercanviant $x$ i $y$ (i usant $d(x,y)=d(y,x)$) s'obté $d(y,A)-d(x,A)\leq d(x,y)$, i les dues juntes donen $|d(x,A)-d(y,A)|\leq d(x,y)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [fita_per_a] Fita per a cada punt d'$A$  (teoria: T1.5)
     objectiu: Relacionar $d(x,A)$ amb $d(x,y)$ i $d(y,a)$ per a un $a\in A$ qualsevol.
     idea: $d(x,A)$ és una fita inferior de totes les distàncies $d(x,a)$; combinar-ho amb la desigualtat triangular passant per $y$.
     detall: Per a tot $a\in A$: $d(x,A)\leq d(x,a)\leq d(x,y)+d(y,a)$.
  2. [prendre_infim] Prendre l'ínfim
     objectiu: Eliminar el punt $a$ de la desigualtat anterior.
     idea: Aïllar $d(y,a)$: el nombre que queda a l'altre costat és una fita inferior de tots els $d(y,a)$, $a\in A$, i per tant és com a molt l'ínfim (l'ínfim és la més gran de les fites inferiors).
     detall: $d(x,A)-d(x,y)\leq d(y,a)$ per a tot $a\in A$, per tant $d(x,A)-d(x,y)\leq\inf_{a\in A}d(y,a)=d(y,A)$, és a dir $d(x,A)-d(y,A)\leq d(x,y)$.
  3. [simetritzar] Intercanviar els papers  (teoria: T1.5)
     objectiu: Passar de la desigualtat d'un sol sentit a la desigualtat amb valor absolut.
     idea: L'argument és simètric en $x$ i $y$; recordar que $|t|\leq c$ equival a $-c\leq t\leq c$.
     detall: Intercanviant $x$ i $y$: $d(y,A)-d(x,A)\leq d(y,x)=d(x,y)$. Juntament amb l'anterior, $-d(x,y)\leq d(x,A)-d(y,A)\leq d(x,y)$, és a dir $|d(x,A)-d(y,A)|\leq d(x,y)$.
ERRORS COMUNS:
  - [infim_com_minim] Pren un $a_0\in A$ amb $d(x,a_0)=d(x,A)$ (o amb $d(y,a_0)=d(y,A)$), suposant que l'ínfim s'assoleix, cosa que no cal que passi si $A$ no és tancat.
  - [infim_sentit] Pren l'ínfim en un sentit incorrecte, per exemple passa de $d(x,A)\leq d(x,y)+d(y,a)$ per a cada $a$ a una conclusió del tipus $d(x,A)\geq\dots$, o tracta l'ínfim d'una diferència com la diferència d'ínfims.
  - [un_sol_sentit] Prova només $d(x,A)-d(y,A)\leq d(x,y)$ i conclou el valor absolut.

TEORIA DEL CURS QUE FA SERVIR:
[T1.5] Definició 5 (Tema 1) — Distància
Sigui $M$ un conjunt. Una funció $d(\cdot,\cdot):M\times M\longrightarrow\mathbb{R}$ es diu que és una _distància_ si per a tot $x,y,z\in M$, es compleixen:

i) $d(x,y)\geq 0$; $d(x,y)=0\iff x=y$.

ii) $d(x,y)=d(y,x)$ (simètrica).

iii) $d(x,y)\leq d(x,z)+d(z,y)$ (desigualtat triangular).

Direm en aquest cas que $(M,d)$ és un _espai mètric_.
</solucio_de_referencia>

### Document a revisar

[1] Fixem $x,y\in\mathbb{R}^m$. Com que $A\neq\emptyset$, el conjunt $\{d(x,a)\mid a\in A\}$ és no buit i fitat inferiorment per $0$, i $d(x,A)$ és el seu ínfim; el mateix val per a $d(y,A)$.
[2] Sigui $a\in A$ qualsevol. Per definició d'ínfim, $d(x,A)\leq d(x,a)$, i per la desigualtat triangular, $d(x,a)\leq d(x,y)+d(y,a)$.
[3] Per tant, $d(x,A)-d(x,y)\leq d(y,a)$ per a algun $a\in A$, i així $d(x,A)-d(x,y)$ és una fita inferior del conjunt $\{d(y,a)\mid a\in A\}$.
[4] Com que $d(y,A)$ també és una fita inferior del mateix conjunt, per transitivitat obtenim $d(x,A)-d(x,y)\leq d(y,A)$, és a dir, $d(x,A)-d(y,A)\leq d(x,y)$.
[5] Per a l'altra desigualtat, sigui $a_0\in A$ el punt d'$A$ més proper a $x$, de manera que $d(x,a_0)=d(x,A)$. Aleshores $d(y,A)\leq d(y,a_0)\leq d(y,x)+d(x,a_0)=d(x,y)+d(x,A)$, és a dir, $d(y,A)-d(x,A)\leq d(x,y)$.
[6] Juntant les dues desigualtats, $-d(x,y)\leq d(x,A)-d(y,A)\leq d(x,y)$, que és exactament $|d(x,A)-d(y,A)|\leq d(x,y)$.


## t3-7:dificil

### Referència

<solucio_de_referencia>
ENUNCIAT: Estudieu la continuïtat i la diferenciabilitat de la funció
$$f(x,y)=\begin{cases}\dfrac{x|y|}{\sqrt{x^2+y^2}} & \text{si } (x,y)\neq(0,0)\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$
RESULTAT CORRECTE: $f$ és contínua a tot $\mathbb{R}^2$. És diferenciable exactament a $\{(x,y): y\neq0\}$: no és diferenciable en cap punt de l'eix $y=0$. Als punts $(x_0,0)$, $x_0\neq0$, no existeix $\partial f/\partial y$; a l'origen les parcials valen $0$ però $\dfrac{f(x,y)}{\|(x,y)\|}=\dfrac{x|y|}{x^2+y^2}$ no tendeix a $0$ (per exemple val $\pm\frac12$ sobre $y=x$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [continuitat_fora] Continuïtat fora de l'origen  (teoria: T2.19, T2.20)
     objectiu: Justificar la continuïtat als punts $(x,y)\neq(0,0)$.
     idea: Fora de l'origen $f$ és una combinació (productes, quocients, composicions) de funcions contínues amb denominador no nul.
     detall: $x$, $|y|$ i $\sqrt{x^2+y^2}$ són contínues i el denominador no s'anul·la a $\mathbb{R}^2\setminus\{(0,0)\}$, per tant $f$ hi és contínua.
  2. [continuitat_origen] Continuïtat a l'origen  (teoria: T2.14)
     objectiu: Decidir si $\lim_{(x,y)\to(0,0)}f(x,y)=0$.
     idea: Fita el mòdul del quocient: compara un dels factors del numerador amb el denominador.
     detall: $|x|\le\sqrt{x^2+y^2}$, per tant $|f(x,y)|\le|y|\to0$. Per sandvitx el límit és $0=f(0,0)$: $f$ és contínua a l'origen, i doncs a tot $\mathbb{R}^2$.
  3. [diferenciable_fora_eix] Diferenciabilitat on y no és zero  (teoria: T3.18)
     objectiu: Estudiar la diferenciabilitat als punts amb $y\neq0$.
     idea: En un entorn d'un punt amb $y\neq0$, el valor absolut té un signe fix: estudia la regularitat de les parcials allà.
     detall: A l'obert $\{y>0\}$ (resp. $\{y<0\}$), $f=\pm\dfrac{xy}{\sqrt{x^2+y^2}}$, amb parcials contínues (quocients de funcions $\mathcal C^1$, denominador no nul). Per la condició suficient, $f$ és diferenciable a tot punt amb $y\neq0$.
  4. [eix_sense_origen] Punts de l'eix fora de l'origen  (teoria: T3.2, T3.9)
     objectiu: Estudiar la diferenciabilitat als punts $(x_0,0)$ amb $x_0\neq0$.
     idea: Si fos diferenciable, existirien totes les parcials. Calcula la parcial respecte de $y$ amb la definició i mira els límits laterals.
     detall: $\dfrac{f(x_0,t)-f(x_0,0)}{t}=\dfrac{x_0|t|}{t\sqrt{x_0^2+t^2}}\to\pm\dfrac{x_0}{|x_0|}$ quan $t\to0^\pm$: els laterals són $\pm1$ (amb signe de $x_0$), no existeix $\partial f/\partial y(x_0,0)$. Per tant no és diferenciable.
  5. [origen] Diferenciabilitat a l'origen  (teoria: T3.8, T3.9, T2.10)
     objectiu: Decidir si $f$ és diferenciable a $(0,0)$.
     idea: Calcula les parcials a l'origen per obtenir l'única candidata a diferencial i estudia el límit de la definició amb aquesta candidata.
     detall: $f(t,0)=f(0,t)=0$, així $\nabla f(0,0)=(0,0)$ i la candidata és $Df(0,0)=0$. Cal $\dfrac{f(x,y)}{\sqrt{x^2+y^2}}=\dfrac{x|y|}{x^2+y^2}\to0$, però sobre $y=x$ val $\dfrac{x|x|}{2x^2}=\pm\dfrac12$. No és diferenciable a l'origen. (Equivalentment: $D_uf(0,0)=u_1|u_2|$ per a $u$ unitari, que no és lineal en $u$.)
ERRORS COMUNS:
  - [parcials_implica_diferenciable] A l'origen calcula que les parcials existeixen (i valen $0$) i conclou que és diferenciable.
  - [oblida_eix] Només estudia l'origen i diu que fora és diferenciable "per ser composició de funcions diferenciables", oblidant que $|y|$ no és derivable a $y=0$.
  - [camins_rectes_continuitat] Conclou la continuïtat a l'origen només provant rectes.

TEORIA DEL CURS QUE FA SERVIR:
[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$

[T2.19] Observació 19 (Tema 2) — Composició de funcions contínues
Siguin $f:\Omega\subseteq M\to N$ i $g:\Theta\subseteq N\to P$ amb $f(\Omega)\subseteq\Theta$. Aleshores,

(i) si $f$ és contínua en $x_0\in\Omega'$ i $g$ és contínua en $f(x_0)\in\Theta'$ $\Rightarrow g\circ f$ és contínua en $x_0$;

(ii) si $f$ i $g$ són contínues, $g\circ f$ és contínua.

[T2.20] Proposició 20 (Tema 2) — Àlgebra de funcions contínues
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $h:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, contínues. Llavors

(i) $f+g,\ \lambda f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $\lambda\in\mathbb{R}$, són contínues;

(ii) $hf:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ és contínua;

(iii) per a $m=1$, si $g(x)\neq0\ \forall x\in\Omega$, $f/g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(iv) $\langle f,g\rangle:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(v) $\|f\|:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua.

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T3.9] Proposició 9 (Tema 3) — Derivades direccionals, jacobiana i hiperplà tangent
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, diferenciable en $a\in\mathring{\Omega}$. Llavors:

(i) Existeixen totes les derivades direccionals de $f$ al punt $a$ i, a més, $D_uf(a)=Df(a)\,u$, $\forall u\neq0$.

(ii) La diferencial $Df(a)$ és única i, fixades les bases canòniques a $\mathbb{R}^n$ i $\mathbb{R}^m$, té matriu
$$Jf(a)=\begin{pmatrix}\dfrac{\partial f_1}{\partial x_1}(a)&\cdots&\dfrac{\partial f_1}{\partial x_n}(a)\\ \dfrac{\partial f_2}{\partial x_1}(a)&\cdots&\dfrac{\partial f_2}{\partial x_n}(a)\\ \vdots&\ddots&\vdots\\ \dfrac{\partial f_m}{\partial x_1}(a)&\cdots&\dfrac{\partial f_m}{\partial x_n}(a)\end{pmatrix}=\left(\frac{\partial f_i}{\partial x_j}(a)\right)_{i,j}.\tag{4}$$

(iii) Per al cas $m=1$, és a dir, $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, l'hiperplà tangent al graf de $f$, $x_{n+1}=f(x)$, en el punt $(a,f(a))$ ve donat per
$$x_{n+1}=f(a)+Jf(a)(x-a).\tag{5}$$
En el cas particular $n=2$, és a dir $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}$, l'equació del pla tangent a la superfície $z=f(x,y)$ al punt $(a,f(a))=(a_1,a_2,f(a_1,a_2))$ és
$$z=f(a)+\frac{\partial f}{\partial x}(a)\,(x-a_1)+\frac{\partial f}{\partial y}(a)\,(y-a_2).\tag{6}$$
En aquest cas, tenim que
$$D_uf(a)=Df(a)\,u=\langle\nabla f(a),u\rangle,\quad\forall u\neq0.$$

[T2.10] Proposició 10 (Tema 2) — Límit per camins
Límit per camins. Si $F:D\subseteq\mathbb{R}^2\longrightarrow\mathbb{R}^m$ i $(a,b)\in D'$ tal que $\displaystyle\exists\lim_{(x,y)\to(a,b)}F(x,y)=L$, llavors per a tota funció real i contínua $g$ definida en un entorn d'$a$, tal que $g(a)=b$, es compleix que
$$\lim_{x\to a}F(x,g(x))=L.$$
</solucio_de_referencia>

### Document a revisar

[1] Fora de l'origen, les funcions $x$, $|y|$ i $\sqrt{x^2+y^2}$ són contínues i el denominador no s'anul·la a $\mathbb{R}^2\setminus\{(0,0)\}$, de manera que $f$ hi és contínua.
[2] A l'origen, $|f(x,y)|=\dfrac{|x|\,|y|}{\sqrt{x^2+y^2}}\le|x|\,|y|$, i com que $|x|\,|y|\to0$ quan $(x,y)\to(0,0)$, pel criteri del sandvitx el límit a l'origen és $0=f(0,0)$. Per tant $f$ és contínua a tot $\mathbb{R}^2$.
[3] A l'obert $\{y>0\}$ tenim $f=\dfrac{xy}{\sqrt{x^2+y^2}}$, amb $\dfrac{\partial f}{\partial x}=\dfrac{y^3}{(x^2+y^2)^{3/2}}$ i $\dfrac{\partial f}{\partial y}=\dfrac{x^3}{(x^2+y^2)^{3/2}}$; a l'obert $\{y<0\}$ són les mateixes amb el signe canviat. Com que les dues derivades parcials existeixen a tot punt d'aquests oberts, $f$ és diferenciable a tot punt amb $y\neq0$.
[4] En un punt $(x_0,0)$ amb $x_0\neq0$: $\dfrac{f(x_0,t)-f(x_0,0)}{t}=\dfrac{x_0|t|}{t\sqrt{x_0^2+t^2}}$, que tendeix a $\dfrac{x_0}{|x_0|}$ quan $t\to0^+$ i a $-\dfrac{x_0}{|x_0|}$ quan $t\to0^-$. Els límits laterals són diferents, no existeix $\dfrac{\partial f}{\partial y}(x_0,0)$ i, per tant, $f$ no és diferenciable en aquests punts.
[5] A l'origen, $f(t,0)=0$ i $f(0,t)=0$ per a tot $t$, així que $\nabla f(0,0)=(0,0)$ i l'única candidata a diferencial és l'aplicació lineal nul·la.
[6] Per a la diferenciabilitat a l'origen cal que $\dfrac{f(x,y)}{x^2+y^2}=\dfrac{x|y|}{(x^2+y^2)^{3/2}}$ tendeixi a $0$. Sobre la recta $y=x$, amb $x>0$, val $\dfrac{x^2}{2\sqrt2\,x^3}=\dfrac{1}{2\sqrt2\,x}\to+\infty$, de manera que $f$ no és diferenciable a l'origen.
[7] En resum, $f$ és contínua a tot $\mathbb{R}^2$ i és diferenciable exactament als punts amb $y\neq0$: no ho és en cap punt de l'eix $y=0$.


## t3-10:dificil

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $D\subseteq\mathbb{R}^2$ obert i $f:D\to\mathbb{R}$ tal que les seves derivades parcials existeixen i estan fitades en $D$. Demostreu que $f(x,y)$ és contínua en $D$. És cert a $\mathbb{R}^m$, per $m>2$?

Indicació: per a provar que $f(x_n,y_n)\to f(x,y)$ per a tota successió $(x_n,y_n)$ que tendeixi a $(x,y)$, sumeu i resteu $f(x_n,y)$ a $|f(x_n,y_n)-f(x,y)|$, apliqueu la desigualtat triangular i fiteu els termes obtinguts.
RESULTAT CORRECTE: Sí. Si $M$ fita les dues parcials, per a $(x,y)$ en una bola $B\subseteq D$ centrada a $(x_0,y_0)$ es té $|f(x,y)-f(x_0,y_0)|\le M(|x-x_0|+|y-y_0|)\to0$, per tant $f$ és contínua. A $\mathbb{R}^m$ val el mateix argument, canviant una coordenada cada vegada: s'obtenen $m$ sumands $M|x_i-x_{0,i}|$, i també és cert.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [plantejament] Plantejar què cal fitar  (teoria: T2.14, T2.17)
     objectiu: Traduir "$f$ és contínua a $(x_0,y_0)$" a una afirmació concreta sobre una diferència.
     idea: Fixa un punt del domini i estudia la diferència $|f(x,y)-f(x_0,y_0)|$.
     detall: Cal veure que $|f(x,y)-f(x_0,y_0)|\to0$ quan $(x,y)\to(x_0,y_0)$ (o, amb successions, $f(x_n,y_n)\to f(x_0,y_0)$); per tant, fitar-la per una expressió que tendeixi a $0$.
  2. [punt_intermedi] Moure una coordenada cada vegada  (teoria: T3.18+dem)
     objectiu: Descompondre la diferència en variacions que només depenguin d'una variable.
     idea: Passa per un punt intermedi que comparteixi una coordenada amb cada extrem i usa la desigualtat triangular.
     detall: Amb el punt $(x,y_0)$: $|f(x,y)-f(x_0,y_0)|\le|f(x,y)-f(x,y_0)|+|f(x,y_0)-f(x_0,y_0)|$.
  3. [dins_domini] Els segments són dins de D  (teoria: T1.11)
     objectiu: Garantir que els segments horitzontal i vertical que fas servir estan continguts a $D$.
     idea: Fes servir que $D$ és obert i treballa en un entorn petit del punt.
     detall: Com que $D$ és obert, hi ha una bola $B$ centrada a $(x_0,y_0)$ dins de $D$; si $(x,y)\in B$, el punt intermedi $(x,y_0)$ (que és més a prop del centre) i els dos segments paral·lels als eixos també són a $B\subseteq D$, per convexitat de la bola.
  4. [valor_mitja] Teorema del valor mitjà en una variable  (teoria: T3.2, T3.18+dem)
     objectiu: Fitar cada terme usant només la informació sobre les parcials.
     idea: Cada terme és la variació d'una funció d'una variable derivable, la derivada de la qual és una parcial; aplica-hi el teorema del valor mitjà d'una variable.
     detall: $g(t)=f(x,t)$ és derivable amb $g'(t)=\partial_yf(x,t)$; pel TVM, $|f(x,y)-f(x,y_0)|=|\partial_yf(x,\tilde y)|\,|y-y_0|\le M|y-y_0|$. Igualment $|f(x,y_0)-f(x_0,y_0)|\le M|x-x_0|$.
  5. [concloure] Concloure i generalitzar
     objectiu: Tancar la demostració i respondre la pregunta per a $\mathbb{R}^m$.
     idea: Suma les dues fites; per a $m$ variables, repeteix l'argument canviant una coordenada cada vegada.
     detall: $|f(x,y)-f(x_0,y_0)|\le M(|x-x_0|+|y-y_0|)\to0$. A $\mathbb{R}^m$ es passa de $x_0$ a $x$ per $m$ segments paral·lels als eixos (dins d'una bola continguda a $D$) i s'obtenen $m$ sumands $M|x_i-x_{0,i}|$: també és cert.
ERRORS COMUNS:
  - [suposa_diferenciable] Suposa que $f$ és diferenciable o de classe $\mathcal C^1$, cosa que l'enunciat no diu.
  - [tvm_diagonal] Aplica un teorema del valor mitjà sobre el segment que uneix els dos punts, cosa que requeriria diferenciabilitat.
  - [oblida_domini] No comprova que els segments que fa servir estan dins de $D$.
  - [sense_fita] Intenta concloure només amb l'existència de parcials, sense usar que estan fitades.

TEORIA DEL CURS QUE FA SERVIR:
[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.

[T2.17] Teorema 17 (Tema 2) — Caracteritzacions de la continuïtat
Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents:

(a) $f$ és contínua en $\Omega$;

(b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;

(c) per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$;

(d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.
Demostració: Primer, recordem que a $\mathbb{R}^n$ totes les normes són equivalents. En particular, existeix $\mu>0$ de manera que $\|x\|=\|x\|_2\leq\mu\|x\|_1$.

Reduirem la demostració a provar que totes les funcions component $f_i$ ($i=1,2,\ldots,m$) són diferenciables al punt $a$. Suposem que el següent resultat és cert.

Afirmació. Totes les funcions component de $f$, o sigui $f_i$, per a $i=1,2,\ldots,m$, són diferenciables al punt $x=a$.

Si aquesta afirmació és certa, llavors $f$ és diferenciable al punt $x=a$. En efecte, fixat $\varepsilon>0$, sabem que existeix $\delta_i>0$ de manera que si $\|x-a\|<\delta_i$ aleshores
$$|f_i(x)-f_i(a)-Jf_i(a)(x-a)|<\frac{\varepsilon}{\mu m}\|x-a\|,$$
per a $i=1,2,\ldots,m$ i on
$$Jf_i(a)=Df_i(a)=\left(\frac{\partial f_i}{\partial x_1}(a)\ \ \frac{\partial f_i}{\partial x_2}(a)\ \ \cdots\ \ \frac{\partial f_i}{\partial x_n}(a)\right).$$
En conseqüència, si $\|x-a\|<\delta<\min_{i\in\{1,2,\ldots,m\}}\delta_i$, es dedueix que
$$\begin{aligned}\|f(x)-f(a)-Jf(a)(x-a)\|&\leq\mu\|f(x)-f(a)-Jf(a)(x-a)\|_1\\&=\mu\sum_{i=1}^m|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\mu\sum_{i=1}^m\frac{\varepsilon}{\mu m}\|x-a\|=\varepsilon\|x-a\|,\end{aligned}$$
que és el que volíem provar. Per tant, demostrem ara l'Afirmació anterior. Prenem $i\in\{1,2,\ldots,m\}$ qualsevol i vegem que $f_i$ és diferenciable a $x=a$. Cal provar que, fixat $\varepsilon>0$, existeix un $\delta=\delta(\varepsilon)>0$ tal que si $x\in\Omega$, $\|x-a\|<\delta$ aleshores
$$|f_i(x)-f_i(a)-Jf_i(a)(x-a)|<\varepsilon\|x-a\|,$$
per a $i=1,2\ldots,m$. La idea és aplicar, coordenada a coordenada, el teorema del valor mitjà (TVM) per a funcions d'una variable. (Nota: Sigui $f:[a,b]\to\mathbb{R}$ contínua a $[a,b]$ i derivable a $(a,b)$. Aleshores, existeix $\xi\in(a,b)$ tal que $f(b)-f(a)=f'(\xi)(b-a)$.) Del fet que $a\in\mathring{\Omega}$ es deriva que existeix un $\delta_0>0$ tal que $R(a,\delta_0):=(a_1-\delta_0,a_1+\delta_0)\times\cdots\times(a_n-\delta_0,a_n+\delta_0)\subseteq\Omega$. Aleshores, per a valors de $x\in R(a,\delta_0)$, podem escriure
$$\begin{aligned}f_i(x)-f_i(a)&=f_i(x_1,x_2,x_3,\ldots,x_n)-f_i(a_1,a_2,a_3,\ldots,a_n)\\&=f_i(x_1,x_2,x_3,x_4,\ldots,x_n)-f_i(a_1,x_2,x_3,x_4,\ldots,x_n)\\&\quad+f_i(a_1,x_2,x_3,x_4,\ldots,x_n)-f_i(a_1,a_2,x_3,x_4,\ldots,x_n)\\&\quad+f_i(a_1,a_2,x_3,x_3,\ldots,x_n)-f_i(a_1,a_2,a_3,x_4,\ldots,x_n)\\&\quad+\cdots\\&\quad+f_i(a_1,a_2,\ldots,a_{n-1},x_n)-f_i(a_1,a_2,\ldots,a_{n-1},a_n)\\&\overset{\text{TVM}}{=}\frac{\partial f_i}{\partial x_1}(\xi_1,x_2,x_3,x_4,\ldots,x_n)(x_1-a_1)\\&\quad+\frac{\partial f_i}{\partial x_2}(a_1,\xi_2,x_3,x_4,\ldots,x_n)(x_2-a_2)\\&\quad+\frac{\partial f_i}{\partial x_3}(a_1,a_2,\xi_3,x_4,\ldots,x_n)(x_3-a_3)\\&\quad+\cdots\\&\quad+\frac{\partial f_i}{\partial x_n}(a_1,a_2,\ldots,a_{n-1},\xi_n)(x_n-a_n),\end{aligned}$$
on cada $\xi_j$, $j=1,2,\ldots,n$ pertany a l'interior del mínim interval (a $\mathbb{R}$) que conté $x_j$ i $a_j$ i, per tant a $R(a,\delta_0)$. En particular, això implica que $x_j$ tendeix a $a_j$, aleshores $\xi_j$ tendeix a $a_j$. Així doncs, si denotem $(a_{<j},\xi_j,x_{>j}):=(a_1,a_2,\ldots,a_{j-1},\xi_j,x_{j+1},\ldots,x_n)$, (Nota: Entenent que $a_{<1}=\emptyset$ i $x_{>n}=\emptyset$) tenim que
$$\begin{aligned}&|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\\&=\left|\sum_{j=1}^n\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})(x_j-a_j)-\sum_{j=1}^n\frac{\partial f_i}{\partial x_j}(a)(x_j-a_j)\right|\\&\leq\sum_{j=1}^n\left|\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right|\,|x_j-a_j|\,.\end{aligned}$$
De la continuïtat de les derivades parcials al punt $a$, es dedueix que existeix un $0<\delta_0'<\delta_0$, prou petit, tal que $R(a,\delta_0'):=(a_1-\delta_0',a_1+\delta_0')\times\cdots\times(a_n-\delta_0',a_n+\delta_0')\subseteq\Omega$ de manera que $\xi_j\in(a_j-\delta_0',a_j+\delta_0')$ per a tot $j\in\{1,2,\ldots,n\}$ i, a més, que
$$\sum_{j=1}^n\left|\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right|\,|x_j-a_j|<\varepsilon\|x-a\|,$$
per a tot $x\in R(a,\delta_0')$. En particular, verificant que
$$|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\varepsilon\|x-a\|$$
si $\|x-a\|<\delta_0'$.
</solucio_de_referencia>

### Document a revisar

[1] Fixem un punt $p=(x_0,y_0)\in D$ i triem $M>0$ tal que $|\partial_x f|\le M$ i $|\partial_y f|\le M$ a tot $D$, cosa possible perquè les parcials estan fitades. Per provar la continuïtat en $p$ n'hi ha prou de veure que $|f(x,y)-f(x_0,y_0)|\to0$ quan $(x,y)\to p$.
[2] Introduïm el punt intermedi $(x,y_0)$ i apliquem la desigualtat triangular: $|f(x,y)-f(x_0,y_0)|\le |f(x,y)-f(x,y_0)|+|f(x,y_0)-f(x_0,y_0)|$. Així separem la variació vertical de la variació horitzontal.
[3] Com que $D$ és obert, per a qualsevol $(x,y)\in D$ el punt $(x,y_0)$ i els segments que uneixen $(x,y)$ amb $(x,y_0)$ i $(x,y_0)$ amb $(x_0,y_0)$ queden dins de $D$.
[4] Considerem $g(t)=f(x,t)$ per a $t$ entre $y_0$ i $y$, i $h(s)=f(s,y_0)$ per a $s$ entre $x_0$ i $x$. Com que les parcials existeixen en aquests segments, $g$ i $h$ són de classe $\mathcal{C}^1$ en els intervals corresponents, amb $g'(t)=\partial_y f(x,t)$ i $h'(s)=\partial_x f(s,y_0)$.
[5] Pel teorema del valor mitjà aplicat a $g$, existeix $\tilde y$ entre $y_0$ i $y$ tal que $|f(x,y)-f(x,y_0)|=|\partial_y f(x,\tilde y)|\,|y-y_0|\le M|y-y_0|$. Anàlogament, aplicant-lo a $h$, $|f(x,y_0)-f(x_0,y_0)|\le M|x-x_0|$.
[6] Sumant les dues estimacions, $|f(x,y)-f(x_0,y_0)|\le M(|x-x_0|+|y-y_0|)$, que tendeix a $0$ quan $(x,y)\to p$. Per tant $f$ és contínua en $p$ i, com que $p$ era arbitrari, $f$ és contínua a tot $D$.
[7] A $\mathbb{R}^m$ l'argument és el mateix: es passa de $x_0$ a $x$ canviant una coordenada cada vegada i s'obté $|f(x)-f(x_0)|\le M\sum_{i=1}^m |x_i-x_{0,i}|$. Com que $\sum_{i=1}^m |x_i-x_{0,i}|\le \|x-x_0\|_2$, aquesta fita tendeix a $0$ i el resultat també és cert per a $m>2$.

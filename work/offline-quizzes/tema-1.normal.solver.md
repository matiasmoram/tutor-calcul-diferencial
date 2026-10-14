# solver

## Instructions

Ets un expert en Càlcul Diferencial. Per a cada afirmació, decideix tu mateix si és CERTA o FALSA amb les definicions dels apunts, abans de mirar res més. Raona-ho de debò: per a una de falsa, troba un contraexemple concret i comprova'l; per a una de certa, esbossa la demostració.
"ben_plantejada": false si l'afirmació és ambigua, depèn de convencions no dites, té hipòtesis contradictòries o no té un valor de veritat clar.
"confianca": "alta" només si tens una demostració o un contraexemple comprovat.
"justificacio": breu (1-3 frases), amb el contraexemple o la idea de la demostració.

## Notes

<apunts tema="1" titol="Topologia a $\mathbb{R}^n$">
[T1.x1] Apunts del Tema 1, § — Introducció del tema
El protagonista d'aquest curs és, essencialment, $\mathbb{R}^n$. Els conceptes més importants que s'introduiran al final d'aquest tema són: completesa, compacitat i connexió.

[T1.x2] Apunts del Tema 1, §1.1 — Espai vectorial de partida
Sigui $E$ un $\mathbb{R}$-espai vectorial ($\mathbb{R}$-e.v.).

[T1.1] Definició 1 (Tema 1) — Producte escalar
Una funció $\langle\cdot,\cdot\rangle: E\times E\longrightarrow\mathbb{R}$ es diu que és un _producte escalar_ si compleix; $\forall u,u_j,v\in E$:

i) $\langle u,u\rangle\geq 0$; $\langle u,u\rangle=0\iff u=0$.

ii) $\langle u,v\rangle=\langle v,u\rangle$ (simètric).

iii) $\langle\lambda u,v\rangle=\lambda\langle u,v\rangle$, $\forall\lambda\in\mathbb{R}$ (i, per tant, $\langle u,\lambda v\rangle=\lambda\langle u,v\rangle$).

iv) $\langle u_1+u_2,v\rangle=\langle u_1,v\rangle+\langle u_2,v\rangle$ (ídem respecte a la segona component).

En aquest cas es diu que $(E,\langle\cdot,\cdot\rangle)$ és un _espai euclidià_.

[T1.x3] Apunts del Tema 1, §1.1 — Linealitat del producte escalar
Observem que les condicions (iii) o (iv) ens asseguren la linealitat del producte escalar.

[T1.2] Exemple 2 (Tema 1) — Exemples de productes escalars
a) $E=\mathbb{R}^2$, amb $\langle(a,b),(c,d)\rangle=ac+bd$.

b) $E=\mathcal{C}([a,b])=\{f:[a,b]\to\mathbb{R}\mid f \text{ contínua}\}$, amb

$$\begin{aligned}E\times E&\longrightarrow\mathbb{R}\\(f,g)&\longmapsto\langle f,g\rangle=\int_a^b f(x)g(x)\,dx.\end{aligned}$$

[T1.3] Definició 3 (Tema 1) — Norma
Una funció $\|\cdot\|:E\longrightarrow\mathbb{R}$ es diu que és una _norma_ si compleix, $\forall u,v\in E$:

i) $\|u\|\geq 0$; $\|u\|=0\iff u=0$.

ii) $\|\lambda u\|=|\lambda|\,\|u\|$, $\forall\lambda\in\mathbb{R}$.

iii) $\|u+v\|\leq\|u\|+\|v\|$ (desigualtat triangular).

En aquest cas es diu que $(E,\|\cdot\|)$ és un _espai normat_.

[T1.4] Exemple 4 (Tema 1) — Exemples de normes
a) $E=\mathbb{R}^2$, $\|(u_1,u_2)\|=\sqrt{u_1^2+u_2^2}$.

b) $E=\mathcal{C}([a,b])$, amb

$$\|f\|_1=\int_a^b|f(t)|dt.$$

En aquest cas, les propietats (i), (ii), (iii) es verifiquen fàcilment. La propietat $\|f\|_1>0\iff f\equiv 0$ es demostra com a conseqüència del teorema del valor mitjà (que veurem més endavant).

[T1.5] Definició 5 (Tema 1) — Distància
Sigui $M$ un conjunt. Una funció $d(\cdot,\cdot):M\times M\longrightarrow\mathbb{R}$ es diu que és una _distància_ si per a tot $x,y,z\in M$, es compleixen:

i) $d(x,y)\geq 0$; $d(x,y)=0\iff x=y$.

ii) $d(x,y)=d(y,x)$ (simètrica).

iii) $d(x,y)\leq d(x,z)+d(z,y)$ (desigualtat triangular).

Direm en aquest cas que $(M,d)$ és un _espai mètric_.

[T1.6] Proposició 6 (Tema 1) — Euclidià implica normat implica mètric
i) Tot espai euclidià és un espai normat si definim $\|u\|=\sqrt{\langle u,u\rangle}$.

ii) Tot espai normat és un espai mètric si prenem $d(u,v)=\|u-v\|$.

[Figura: diagrama de conjunts imbricats: espais euclidians dins d'espais normats dins d'espais mètrics.]

Figura 1: Espais euclidians $\subset$ espais normats $\subset$ espais mètrics.

Per a demostrar aquesta proposició usarem, en algun moment, el següent resultat:

[T1.7] Proposició 7 (Tema 1) — Desigualtat de Cauchy-Schwarz
(Desigualtat de Cauchy-Schwarz.) Sigui $(E,\langle\cdot,\cdot\rangle)$ un espai euclidià (normat si definim $\|u\|=\sqrt{\langle u,u\rangle}$). Aleshores es verifica que

$$|\langle u,v\rangle|\leq\|u\|\cdot\|v\|.$$

(Nota: Augustin Louis Cauchy (1789-1857), Hermann Schwarz (1843-1921).)

[T1.8] Exemple 8 (Tema 1) — Norma i distància en exemples
a) A $\mathbb{R}^2$, definim $\langle(a,b),(c,d)\rangle=ac+bd$. Llavors,

$$\begin{aligned}\|(a,b)\|&=\sqrt{\langle(a,b),(a,b)\rangle}=\sqrt{a^2+b^2},\\d((a,b),(c,d))&=\|(a,b)-(c,d)\|=\|(a-c,b-d)\|\\&=\sqrt{\langle(a-c,b-d),(a-c,b-d)\rangle}=\sqrt{(a-c)^2+(b-d)^2}\quad\text{(Pitàgores).}\end{aligned}$$

b) A $\mathbb{R}^3$, $\|(a,b,c)\|=\sqrt{a^2+b^2+c^2}$ i, en general, a $\mathbb{R}^n$:

$$\begin{aligned}\langle(a_1,a_2,\ldots,a_n),(b_1,b_2,\ldots,b_n)\rangle&:=\sum_{i=1}^n a_i\cdot b_i;\\\|(a_1,a_2,\ldots,a_n)\|&=\sqrt{\sum_{i=1}^n a_i^2};\\d((a_1,a_2,\ldots,a_n),(b_1,b_2,\ldots,b_n))&=\sqrt{\sum_{i=1}^n(a_i-b_i)^2}.\end{aligned}$$

c) $E=\mathcal{C}([a,b])$. Aleshores:

$$\begin{aligned}\langle f,g\rangle&:=\int_a^b f(x)g(x)\,dx;\\\|f\|&=\sqrt{\int_a^b f^2(x)\,dx};\\d(f,g)=\|f-g\|&=\sqrt{\int_a^b(f(x)-g(x))^2dx}\quad\text{("àrea" entre }y=f(x)\text{ i }y=g(x)\text{).}\end{aligned}$$

d) $E=\mathcal{B}(A)=$ conjunt de funcions $f:A\to\mathbb{R}$ fitades (inferiorment i superior), amb $A$ conjunt arbitrari. Aleshores, $d(f,g)=\displaystyle\sup_{t\in A}|f(t)-g(t)|$ és una distància.

[T1.9] Definició 9 (Tema 1) — Ortogonalitat i angle
Sigui $(E,\langle\cdot,\cdot\rangle)$ un espai euclidià. Aleshores:

i) $u$ i $v$ són _ortogonals_ $\Leftrightarrow\langle u,v\rangle=0$.

ii) L'angle entre dos vectors $u$ i $v$ es defineix com

$$\alpha=\Delta(u,v)=\arccos\frac{\langle u,v\rangle}{\|u\|\,\|v\|}\in[0,\pi].$$

[T1.10] Observació 10 (Tema 1) — Espais mètrics no normats
Hi ha espais mètrics que no són normats. Per exemple:

a) Donat $M$ un conjunt, definim la següent _distància discreta_:

$$d(x,y)=\begin{cases}0&\text{si }x=y,\\1&\text{si }x\neq y.\end{cases}$$

Aleshores, la norma induïda, $\|x-y\|=d(x,y)$, no té sentit en un espai vectorial.

b) En un espai mètric $(M,d)$, $M$ és un conjunt arbitrari (en particular, podria ser finit) mentre que per a ser normat caldria que fos espai vectorial (en particular, infinit).

[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.

[T1.12] Proposició 12 (Tema 1) — Propietats dels conjunts oberts
(Propietats dels conjunts oberts.) Sigui $(M,d)$ un espai mètric. Aleshores,

i) tota bola oberta $B_r(x)$ és un conjunt obert;

ii) la unió arbitrària (finita o infinita) d'oberts és un obert;

iii) la intersecció finita d'oberts és un obert;

iv) $M$ i $\varnothing$ són conjunts oberts.

[T1.x4] Apunts del Tema 1, §1.2 — Comentaris sobre oberts
**Comentaris:**

1) Per exemple, a $\mathbb{R}$, tot interval del tipus $(a,+\infty)$ és un obert car $(a,+\infty)=\bigcup_{x>a}(a,x)$. (usem (ii)). De manera anàloga es mostra que $(-\infty,a)$ és un obert de $\mathbb{R}$.

2) En general, la intersecció infinita d'oberts no és un obert. Per exemple $O_n=\left(-\dfrac{1}{n},\dfrac{1}{n}\right)$ és un obert de $\mathbb{R}$. En canvi

$$\bigcap_{n\geq 1}O_n=\{0\},$$

que no és obert (ja que $\forall r>0$, $B(0,r)\not\subset\{0\}$ a $\mathbb{R}$).

[T1.x5] Apunts del Tema 1, §1.2 — Topologia discreta sobre un conjunt
**Comentari (topologia discreta sobre un conjunt $M$):**
Donat un conjunt $M$ es defineix la _topologia discreta sobre_ $M$, com aquella topologia $\mathcal{T}$ en la qual tots els seus subconjunts són oberts. És a dir

$$\mathcal{T}=\mathcal{P}(M),$$

on $\mathcal{P}(M)$ denota el conjunt de les parts de $M$. És la topologia més fina sobre $M$ (conté tots els oberts de qualsevol altra topologia $\mathcal{T}_1$ sobre $M$). Satisfà, entre d'altres, les següents propietats:

(i) Tot element de $M$ és un obert: en efecte, si $x\in M$ aleshores $\{x\}\in\mathcal{P}(M)$. Del fet que l'unió arbitrària d'oberts és un obert, es dedueix que tot subconjunt $A\subseteq M$ és un conjunt obert, ja que

$$A=\bigcup_{x\in A}\{x\}.$$

(ii) Tot subconjunt $A\subset M$ és també tancat: en efecte, $A^c=M\setminus A\in\mathcal{P}(M)$ és un obert.

Per tant, amb la topologia discreta, tot subconjunt $A\subseteq M$ és tancat i obert a la vegada.

(iii) La topologia discreta sobre $M$ es pot definir també a través de la distància

$$d(x,y)=\begin{cases}0&\text{si }x=y,\\1&\text{si }x\neq y.\end{cases}$$

**Exemple 1:** Si considerem $M=\mathbb{Z}$ amb la topologia discreta, aleshores qualsevol conjunt de nombres enters és un obert. En particular també ho són $\mathbb{Z}$ i $\varnothing$.

**Exemple 2:** Si $M=\{a,b,c\}$ aleshores la topologia discreta associada a $M$ és

$$\mathcal{T}=\mathcal{P}(M)=\{\varnothing,\{a\},\{b\},\{c\},\{a,b\},\{a,c\},\{b,c\},\{a,b,c\}\}.$$

[T1.x6] Apunts del Tema 1, §1.2 — Topologia euclidiana sobre Z
Sigui ara $M=\mathbb{Z}$ i considereu sobre $\mathbb{Z}$ la topologia induïda per la distància euclidiana

$$d(m,n)=|m-n|.$$

És aleshores $\mathbb{N}$ un obert a $\mathbb{Z}$?

Observeu que si $n\in\mathbb{Z}$ i $r>0$, aleshores la bola oberta de centre $n$ i radi $r$ es defineix com

$$B_r(n)=\left\{m\in\mathbb{Z}\ \middle|\ |m-n|<r\right\}.$$

Així, per exemple, $B_{1/2}(n)=\{n\}$ i $B_{3/2}(n)=\{n-1,n,n+1\}$. Per tant, del fet que

$$\mathbb{N}=\bigcup_{n\in\mathbb{N}}B_{1/2}(n)$$

és unió arbitrària d'oberts es dedueix que $\mathbb{N}$ és un obert de $\mathbb{Z}$ en la topologia induïda per aquesta distància euclidiana.

Recordeu que $A\subseteq M$ és tancat $\Leftrightarrow A^c=M\setminus A$ és obert.

[T1.13] Proposició 13 (Tema 1) — Propietats dels conjunts tancats
Sigui $M$ un conjunt i $d$ una distància definida sobre ell. Considereu la topologia sobre $M$ induïda per $d$. Aleshores:

i) les boles tancades de $M$ són conjunts tancats.

ii) La intersecció arbitrària de tancats és un tancat.

iii) La unió finita de tancats és un tancat.

iv) $M$ i $\varnothing$ són conjunts tancats.

[T1.14] Definició 14 (Tema 1) — Tipus de punts d'un conjunt
Sigui $A\subseteq M$. Aleshores:

i) Un punt $x\in A$ és _interior_ a $A$ si existeix $r>0$ tal que $B_r(x)\subseteq A$.

ii) Un punt $x\in M$ és _d'acumulació_ d'$A$ si per a tot $r>0$ es té que $B_r(x)\cap(A\setminus\{x\})\neq\varnothing$.

iii) Un punt $x\in M$ és de la frontera d'$A$, si per a tot $r>0$ es té que $B_r(x)\cap A\neq\varnothing$ i també $B_r(x)\cap A^c\neq\varnothing$.

iv) Un punt $x\in M$ és _exterior_ d'$A$ si $x$ és interior a $A^c$ (és a dir, si existeix $r>0$ tal que $B_r(x)\subseteq A^c$).

[T1.15] Exemple 15 (Tema 1) — Punts d'un conjunt a R
Siguin $M=\mathbb{R}$ i $A=(1,2]\cup[3,5]$. Aleshores:

- Tot punt $x\in(1,2)\cup(3,5)$ és interior a $A$;
- $x=1$ i $x=3$ són punts d'acumulació d'$A$; de fet, tot $x\in[1,2]\cup[3,5]$ ho és;
- $x=1,2,3,5$ són punts de la frontera d'$A$;
- Tot $x\in(-\infty,1)\cup(2,3)\cup(5,+\infty)$ és exterior a $A$. En efecte, $A^c=(-\infty,1]\cup(2,3)\cup[5,+\infty)$ i els seus punts interiors són $(-\infty,1)\cup(2,3)\cup(5,+\infty)$.

[T1.16] Definició 16 (Tema 1) — Interior, derivat, frontera, clausura
Sigui $A\subseteq M$. Aleshores es defineixen:

i) _Interior_ d'$A$: $\mathring{A}=\{x\in A\mid x\text{ és interior a }A\}$. També s'acostuma a denotar per $\mathrm{int}(A)$.

ii) _Conjunt derivat_ d'$A$: $A'=\{x\in M\mid x\text{ és punt d'acumulació d'}A\}$.

iii) _Frontera_ d'$A$: $\mathrm{Fr}A=\{x\in M\mid x\text{ és de la frontera d'}A\}$. També és denota per $\partial A$.

iv) _Clausura_ o _adherència_ d'$A$: $\overline{A}=\{x\in M\mid\forall r>0\text{ es té que }B_r(x)\cap A\neq\varnothing\}$.
De manera equivalent, es pot definir de les dues maneres següents:
a) $\overline{A}=A\cup A'$; b) $\overline{A}$ és el conjunt tancat més petit que conté $A$.

v) _Exterior_ d'$A$: $\mathrm{ext}(A)=\mathrm{int}(A^c)$.

[T1.17] Proposició 17 (Tema 1) — Propietats de la clausura
Les següents afirmacions són certes:

i) $A\subseteq B\Rightarrow\overline{A}\subseteq\overline{B}$.

ii) $A$ és tancat $\Leftrightarrow\overline{A}=A$.

iii) $\overline{A\cup B}=\overline{A}\cup\overline{B}$.

iv) $\overline{A\cap B}\subseteq\overline{A}\cap\overline{B}$.

[T1.18] Definició 18 (Tema 1) — Successió convergent
Sigui $(M,d)$ un espai mètric. Direm que una successió $(x_n)_{n\in\mathbb{N}}$ és _convergent_ a $M$ si existeix $x\in M$ tal que $\forall\varepsilon>0,\exists n_0\in\mathbb{N}$ tal que $d(x_n,x)<\varepsilon$ $\forall n\geq n_0$. En aquest cas, diem que $x$ és el límit de la successió, i ho denotem per $x=\displaystyle\lim_{n\to\infty}x_n$ (el límit, si existeix, és únic).

[T1.19] Proposició 19 (Tema 1) — Caracterització amb successions
Sigui $(M,d)$ un espai mètric, $A\subseteq M$ i $x\in M$. Aleshores:

i) $x$ és un punt d'acumulació d'$A\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\neq x$, $a_n\in A$, tal que $x=\lim_n a_n$.

ii) $x\in\overline{A}\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\in A$ tal que $x=\lim_n a_n$.

iii) $A$ és tancat $\Leftrightarrow$ el límit de tota successió convergent d'elements d'$A$ és d'$A$.

[T1.20] Definició 20 (Tema 1) — Successió de Cauchy
Sigui $(M,d)$ un espai mètric. Una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\in M$ per a tot $n$, es diu que és de _Cauchy_ si per a tot $\varepsilon>0$, existeix $n_0$ tal que per a tot $n,m\geqslant n_0$, es té que $d(a_n,a_m)<\varepsilon$.

[T1.21] Proposició 21 (Tema 1) — Convergent, Cauchy i fitada
Sigui $(M,d)$ espai mètric.

i) Si $(x_n)_{n\in\mathbb{N}}$ és convergent, aleshores és de Cauchy.

ii) Si $(x_n)_{n\in\mathbb{N}}$ és convergent, aleshores és fitada.

iii) Si $(x_n)_{n\in\mathbb{N}}$ és de Cauchy i té una subsuccessió convergent, aleshores és convergent.

[T1.22] Definició 22 (Tema 1) — Espai mètric complet
Un espai mètric $(M,d)$ es diu que és _complet_ si tota successió de Cauchy en $M$ és convergent a $M$.

[T1.23] Exemple 23 (Tema 1) — R complet, Q no complet
$\mathbb{R}$ amb la distància euclidiana és complet. En canvi, $\mathbb{Q}$ amb la distància euclidiana no és complet. Per exemple: considereu el nombre $\sqrt{2}$. Del fet que sigui irracional, $\sqrt{2}$ admet una expressió en forma decimal infinita on cap bloc es repeteix de forma periòdica (en cas contrari seria racional). Considereu la successió $(a_n)_n$ definida de la forma següent: $a_1$ és el truncament a $1$ xifra decimal de l'expressió (infinita) de $\sqrt{2}$; el terme $a_2$ és el mateix però truncant a $2$ xifres decimals; en general, $a_n$ serà el seu truncament a $n$ xifres decimals. Per exemple:

$$a_1=1.4,\qquad a_2=1.41,\qquad a_3=1.414,\qquad a_4=1.4142,\qquad\ldots$$

Aleshores, la successió $(a_n)_n$, amb $a_n\in\mathbb{Q}$, és de Cauchy perquè la diferència entre els seus termes es fa cada cop més petita. En canvi, aquesta successió no convergeix a un valor a $\mathbb{Q}$ (perquè $\sqrt{2}\notin\mathbb{Q}$).

[T1.x7] Apunts del Tema 1, §1.3 — R^n és complet
**Comentari:** $\mathbb{R}^n$ és complet. En efecte: suposem que $(x_k)_{k\in\mathbb{N}}$ és una successió de Cauchy en $\mathbb{R}^n$. Denotem els seus elements com $x_k=(x_{k_1},\ldots,x_{k_n})$. Per a cada component $j=1,\ldots,n$, la successió $(x_{k_j})_j$ és una successió de Cauchy en $\mathbb{R}$, complet, d'on se dedueix que $(x_{k_j})_j$ convergeix a un cert $x_j$ en $\mathbb{R}$. Per tant, la successió $(x_k)_k\subset\mathbb{R}^n$ convergeix al punt $x=(x_1,\ldots,x_n)\in\mathbb{R}^n$.

[T1.24] Definició 24 (Tema 1) — Compacte i seqüencialment compacte
Sigui $(M,d)$ espai mètric, $A\subseteq M$.

i) $A$ és _compacte_ si tot recobriment per oberts de $A$ admet un subrecobriment finit, és a dir: si $A\subseteq\bigcup_{i\in I}U_i$, amb $U_i$ obert, aleshores existeixen $i_1,\ldots,i_k\in I$ tals que $A\subseteq\bigcup_{j=1}^k U_{i_j}$.

ii) $A$ és _seqüencialment compacte_ si tota successió $(x_n)_{n\in\mathbb{N}}\subseteq A$ admet una subsuccessió (una parcial) convergent a un punt de $A$.

[T1.25] Exemple 25 (Tema 1) — Intervals compactes i no compactes
i) $[0,1]$ a $\mathbb{R}$ és compacte.

ii) $(0,1)$ a $\mathbb{R}$ no és compacte.

[T1.x8] Apunts del Tema 1, §1.4 — Mètode de l'interval de Cantor
**Comentari:** La primera prova de que l'interval $[0,1]$ és compacte (a $\mathbb{R}$) va ser donada pel matemàtic alemany Georg Cantor. Va usar el posteriorment anomenat "mètode de l'interval (de Cantor)".

Es fa per reducció a l'absurd (_R.A._): Donat $\cup_i U_i$ un recobriment obert (infinit) de $[0,1]$, suposem que no es pot obtenir d'ell cap subrecobriment finit. Hi apliquem un mètode iteratiu tipus bisecció. En efecte:

_Pas 1_: Del fet que $I_0=[0,1]$ no admet cap subrecobriment finit es pot deduir que o bé l'interval $\left[0,\frac{1}{2}\right]$ o l'interval $\left[\frac{1}{2},1\right]$ tampoc l'admeten (en cas contrari hauríem arribat a que $[0,1]$ l'admet!) Suposem que és, per exemple, $I_1=\left[0,\frac{1}{2}\right]$ qui no admet cap subrecobriment finit. Noteu que $I_1\subset I_0$.

_Pas n_: De la mateixa manera, construïm una successió d'intervals $(I_n)_n$, encaixats, la longitud dels quals satisfà $\mathrm{long}(I_n)=\frac{1}{2^n}$, amb la propietat que cap d'ells admet un recobriment finit: $I_{n+1}\subset I_n$. Si fem $n\to\infty$ aleshores $\mathrm{long}(I_n)\to 0$ i tenim que $\cap_n I_n=\{x^*\}$. Aquest punt $x^*$ ha de pertànyer, necessàriament, a algun dels oberts $U_i$ del recobriment inicial de $I_0=[0,1]$, ja que el recobreixen. Sigui $U^*\in\{U_i\}_i$ un d'aquests oberts tal que $x^*\in U^*$. A més, $\exists N$ tal que $x^*\in I_N\subset U^*$. Però, per construcció, cap interval $I_n$ pot ser recobert per un nombre finit d'oberts del recobriment (i ara acabem de trobar un únic obert que recobreix $I_N$). Contradicció !! Per tant, l'interval $[0,1]$ és compacte.

(Nota: Georg Cantor, Saint Petersburg 1845 - Halle 1918.)

[T1.26] Teorema 26 (Tema 1) — Teorema de Bolzano-Weierstrass
(Bolzano-Weierstrass.) Sigui $(M,d)$ espai mètric i $A\subseteq M$. Aleshores:
$A$ és compacte $\Leftrightarrow$ $A$ és seqüencialment compacte.

[T1.x9] Apunts del Tema 1, §1.4 — Lemes previs a Bolzano-Weierstrass
La demostració del Teorema de Bolzano-Weierstrass està basada en la prova d'un seguit de lemes previs que presentem i demostrem a continuació.

[T1.27] Lema 27 (Tema 1) — Compacte implica tancat
$A$ compacte $\Rightarrow$ $A$ tancat.

[T1.28] Lema 28 (Tema 1) — Tancat d'un compacte és compacte
Tot tancat d'un compacte és un compacte.

[T1.x10] Apunts del Tema 1, §1.4 — Hipòtesi dels dos lemes següents
Els dos lemes següents parteixen de la hipòtesi que $A$ és seqüencialment compacte.

[T1.29] Lema 29 (Tema 1) — Nombre de Lebesgue
Sigui $A\subset M$ seqüencialment compacte i sigui $\bigcup_{i\in I}U_i\supseteq A$ un recobriment per oberts d'$A$. Aleshores, existeix $\delta>0$ tal que per a tot $a\in A$ es té que $B_\delta(a)\subseteq U_{i_0}$, per a algun $i_0=i_0(a)\in I$.

[T1.30] Lema 30 (Tema 1) — Recobriment finit per boles
Suposem que $A$ és seqüencialment compacte. Aleshores, per a tot $\varepsilon>0$, existeixen $y_1,y_2,\ldots,y_r\in A$ tals que $A\subseteq\cup_{i=1}^r B_\varepsilon(y_i)$, és a dir, $A$ està recobert per una unió finita de boles centrades en punts de $A$ i de radi $\varepsilon$.

[T1.31] Corol·lari 31 (Tema 1) — Propietat de l'encaixament
(Propietat de l'encaixament.) Sigui $(M,d)$ espai mètric, $M$ compacte. Sigui

$$K_1\supseteq K_2\supseteq\cdots\supseteq K_n\supseteq K_{n+1}\supseteq\ldots$$

una cadena descendent de tancats no buits. Aleshores, es té que $\displaystyle\bigcap_{n=1}^{\infty}K_n\neq\varnothing$.

[T1.32] Exemple 32 (Tema 1) — Exemples de la propietat d'encaixament
Aquí teniu dos exemples que il·lustren aquest resultat:

1) $[0,1]\supseteq[0,1/2]\supseteq[0,1/3]\supseteq\ldots$ Aleshores, $\displaystyle\bigcap_{n=1}^{\infty}[0,1/n]=\{0\}\neq\varnothing$.

2) $(0,1]\supseteq(0,1/2]\supseteq(0,1/3]\supseteq\ldots$ Aleshores, $\displaystyle\bigcap_{n=1}^{\infty}(0,1/n]=\varnothing$.

Fixeu-vos que, en aquest cas, els intervals de la forma $(0,1/n]$ no són conjunts tancats (a $\mathbb{R}$) i, per tant, no cauen dins de les hipòtesis del corol·lari.

[T1.33] Definició 33 (Tema 1) — Conjunt fitat
Es diu que $A\subseteq M$ és _fitat_ si i només si existeix un $x\in M$ i un valor $L>0$ tal que $A\subseteq B_L(x)$.

[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.

[T1.x11] Apunts del Tema 1, §1.4 — Dimensió finita i Teorema de Riesz
**Comentari:** Al Teorema de Heine-Borel, la finitud de la dimensió de l'espai $\mathbb{R}^n$ on viu $A$ és essencial. De fet, si $A$ visqués a un espai de dimensió infinita aquesta afirmació seria falsa. Quan estudieu _anàlisi funcional_ veureu l'anomenat Teorema de Riesz, que diu que la bola unitat tancada $\overline{B}_1(0)=\{x\in E\mid\|x\|\leq 1\}$ d'un espai normat $(E,\|\cdot\|)$ és compacta si i només si l'espai té dimensió finita.

[T1.35] Definició 35 (Tema 1) — Conjunt connex
Sigui $(M,d)$ espai mètric, i $A\subseteq M$. Direm que $A$ és _disconnex_ si existeixen dos oberts disjunts $U$ i $V$ tals que $A\subseteq U\cup V$ i $U\cap A\neq\varnothing$ i $V\cap A\neq\varnothing$ i $U\cap V\cap A=\varnothing$. En cas contrari direm que $A$ és un conjunt _connex_.

[T1.36] Exemple 36 (Tema 1) — Exemples de connexió
Casos simples són aquests:

1) $A\subset\mathbb{R}$, $A=[0,1]\cup[3,4]$ és disconnex.

2) $A\subset\mathbb{R}^2$, $A=B_L((0,0))$ és connex.

3) L'interval $[0,1]$ és connex a $\mathbb{R}$.

[T1.x12] Apunts del Tema 1, §1.5 — Clausura d'un connex és connexa
**Comentari:** Si $A$ és connex $\Rightarrow\overline{A}$ és connex.

El recíproc és fals: $A=[0,1)\cup(1,2]$; noteu que $\overline{A}=[0,2]$ és connex i en canvi $A$ és disconnex: en efecte, podem considerar els oberts $U=(-\infty,1)$ i $V=(1,+\infty)$, que satisfan: $A\subseteq U\cup V$, $A\cap U=[0,1)\neq\varnothing$, $A\cap V=(1,2]\neq\varnothing$ i $U\cap V\cap A=\varnothing$.

[T1.37] Teorema 37 (Tema 1) — Obert i tancat en un connex
Sigui $(M,d)$ espai mètric connex i sigui $A\subseteq M$. Si $A$ és obert i tancat a la vegada, aleshores, o bé $A=M$, o bé $A=\varnothing$.
</apunts>

## Statements

<afirmacions>
[1] Sigui $K_1\supseteq K_2\supseteq K_3\supseteq\cdots$ una cadena descendent de subconjunts tancats i no buits de $\mathbb{R}$ (amb la distància euclidiana). Aleshores $\bigcap_{n=1}^{\infty}K_n\neq\varnothing$.
[2] Sigui $A\subseteq\mathbb{R}^2$ un conjunt connex. Aleshores el seu interior $\mathrm{int}(A)$ també és connex.
[3] Sigui $A\subseteq\mathbb{R}$ un conjunt no buit, amb la distància euclidiana $d(x,y)=|x-y|$ restringida a $A$. Com que $\mathbb{R}$ és complet, l'espai mètric $(A,d)$ també és complet.
[4] Sigui $(M,d)$ un espai mètric i sigui $A\subseteq M$ un conjunt tancat i fitat. Aleshores $A$ és compacte.
[5] Sigui $(M,d)$ un espai mètric i sigui $A\subseteq M$ un conjunt que és alhora obert i tancat a $M$. Aleshores $A=\varnothing$ o $A=M$.
[6] Sigui $(x_n)_{n\in\mathbb{N}}$ una successió de nombres reals tal que $\lim_{n\to\infty}|x_{n+1}-x_n|=0$. Aleshores $(x_n)$ és de Cauchy.
[7] Sigui $A\subseteq\mathbb{R}^n$ un conjunt compacte i sigui $(x_k)_{k\in\mathbb{N}}$ una successió de Cauchy amb $x_k\in A$ per a tot $k$. Aleshores $(x_k)$ convergeix a un punt d'$A$.
[8] Sigui $A\subseteq\mathbb{R}^n$ un conjunt qualsevol. Aleshores la seva frontera $\mathrm{Fr}A$ és un conjunt tancat.
[9] Sigui $A\subseteq\mathbb{R}^n$ i sigui $x\in\mathbb{R}^n$ un punt d'acumulació d'$A$. Aleshores, per a tot $r>0$, la bola $B_r(x)$ conté infinits punts d'$A$.
[10] Sigui $(E,\|\cdot\|)$ un espai normat. Aleshores, per a tot $u,v\in E$, es compleix $\big|\,\|u\|-\|v\|\,\big|\leq\|u-v\|$.
[11] Sigui $A\subseteq\mathbb{R}^n$ un conjunt fitat (no necessàriament tancat). Aleshores la seva clausura $\overline{A}$ és compacta.
</afirmacions>

## Output

Write tema-1.normal.solver.json following this schema:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "respostes"
  ],
  "properties": {
    "respostes": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "num",
          "justificacio",
          "veredicte",
          "confianca",
          "ben_plantejada"
        ],
        "properties": {
          "num": {
            "type": "integer"
          },
          "justificacio": {
            "type": "string"
          },
          "veredicte": {
            "type": "string",
            "enum": [
              "cert",
              "fals"
            ]
          },
          "confianca": {
            "type": "string",
            "enum": [
              "alta",
              "mitjana",
              "baixa"
            ]
          },
          "ben_plantejada": {
            "type": "boolean"
          }
        }
      }
    }
  }
}
```

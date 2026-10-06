## t1-5a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Siguin $A,B$ subconjunts no buits de $\mathbb{R}^m$ i $d$ la distància euclídia. Definim $d(A,B)=\inf\{d(a,b)\mid a\in A,\ b\in B\}$.

(a) És cert que $d(A,B)=0\Leftrightarrow A\cap B\neq\emptyset$ ?
RESULTAT CORRECTE: No és cert en general. La implicació $A\cap B\neq\emptyset\Rightarrow d(A,B)=0$ sí que val (si $c\in A\cap B$, $0\leq d(A,B)\leq d(c,c)=0$), però la recíproca és falsa: per exemple, a $\mathbb{R}^m$, $A=\{0\}$ i $B=B(0,1)\setminus\{0\}$ són disjunts i $d(A,B)=\inf_{0<\|b\|<1}\|b\|=0$ (prenent $b=\frac1k e_1$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [implicacio_facil] La implicació $\Leftarrow$  (teoria: T1.5)
     objectiu: Estudiar si $A\cap B\neq\emptyset$ implica $d(A,B)=0$.
     idea: Si hi ha un punt comú, quina parella $(a,b)$ dona la distància més petita possible? Recordar que $d\geq 0$ i que l'ínfim és una fita inferior.
     detall: Si $c\in A\cap B$, prenent $a=b=c$ tenim $d(c,c)=0$ dins el conjunt; com que totes les distàncies són $\geq 0$, $0\leq d(A,B)\leq d(c,c)=0$, i per tant $d(A,B)=0$.
  2. [analitzar_reciproca] Què diu $d(A,B)=0$
     objectiu: Entendre què implica exactament $d(A,B)=0$ i si n'hi ha prou per obtenir un punt comú.
     idea: Usar la caracterització de l'ínfim: ser $0$ vol dir que hi ha parelles $(a,b)$ amb distància tan petita com es vulgui, però no necessàriament una parella amb distància exactament $0$.
     detall: $d(A,B)=0$ equival a: per a tot $\varepsilon>0$ existeixen $a\in A$, $b\in B$ amb $d(a,b)<\varepsilon$; és a dir, hi ha successions $a_k\in A$, $b_k\in B$ amb $d(a_k,b_k)\to 0$. Això no força que l'ínfim s'assoleixi: n'hi ha prou que els conjunts s'"acostin" sense tocar-se, per exemple si un punt d'$A$ és adherent a $B$ sense ser-hi.
  3. [contraexemple] Contraexemple  (teoria: T1.8)
     objectiu: Decidir si la recíproca és certa i justificar-ho completament.
     idea: Buscar dos conjunts disjunts que "es toquin a la vora": un conjunt i un altre que tingui aquell punt a la seva adherència però no el contingui.
     detall: $A=\{0\}$, $B=B(0,1)\setminus\{0\}=\{x\in\mathbb{R}^m\mid 0<\|x\|<1\}$. Són no buits i $A\cap B=\emptyset$, però $d(0,\tfrac1k e_1)=\tfrac1k\to 0$, així que $d(A,B)=0$. (A $\mathbb{R}$ també serveixen $A=(0,1)$, $B=(1,2)$.)
ERRORS COMUNS:
  - [infim_assolit] Suposa que l'ínfim és un mínim, és a dir, que existeixen $a\in A$, $b\in B$ amb $d(a,b)=d(A,B)$.
  - [nomes_una_implicacio] Demostra només una de les dues implicacions i conclou sobre l'equivalència.
  - [contraexemple_buit] Proposa un contraexemple amb algun conjunt buit, o amb conjunts que sí que es tallen.

TEORIA DEL CURS QUE FA SERVIR:
[T1.5] Definició 5 (Tema 1) — Distància
Sigui $M$ un conjunt. Una funció $d(\cdot,\cdot):M\times M\longrightarrow\mathbb{R}$ es diu que és una _distància_ si per a tot $x,y,z\in M$, es compleixen:

i) $d(x,y)\geq 0$; $d(x,y)=0\iff x=y$.

ii) $d(x,y)=d(y,x)$ (simètrica).

iii) $d(x,y)\leq d(x,z)+d(z,y)$ (desigualtat triangular).

Direm en aquest cas que $(M,d)$ és un _espai mètric_.

[T1.8] Exemple 8 (Tema 1) — Norma i distància en exemples
a) A $\mathbb{R}^2$, definim $\langle(a,b),(c,d)\rangle=ac+bd$. Llavors,

$$\begin{aligned}\|(a,b)\|&=\sqrt{\langle(a,b),(a,b)\rangle}=\sqrt{a^2+b^2},\\d((a,b),(c,d))&=\|(a,b)-(c,d)\|=\|(a-c,b-d)\|\\&=\sqrt{\langle(a-c,b-d),(a-c,b-d)\rangle}=\sqrt{(a-c)^2+(b-d)^2}\quad\text{(Pitàgores).}\end{aligned}$$

b) A $\mathbb{R}^3$, $\|(a,b,c)\|=\sqrt{a^2+b^2+c^2}$ i, en general, a $\mathbb{R}^n$:

$$\begin{aligned}\langle(a_1,a_2,\ldots,a_n),(b_1,b_2,\ldots,b_n)\rangle&:=\sum_{i=1}^n a_i\cdot b_i;\\\|(a_1,a_2,\ldots,a_n)\|&=\sqrt{\sum_{i=1}^n a_i^2};\\d((a_1,a_2,\ldots,a_n),(b_1,b_2,\ldots,b_n))&=\sqrt{\sum_{i=1}^n(a_i-b_i)^2}.\end{aligned}$$

c) $E=\mathcal{C}([a,b])$. Aleshores:

$$\begin{aligned}\langle f,g\rangle&:=\int_a^b f(x)g(x)\,dx;\\\|f\|&=\sqrt{\int_a^b f^2(x)\,dx};\\d(f,g)=\|f-g\|&=\sqrt{\int_a^b(f(x)-g(x))^2dx}\quad\text{("àrea" entre }y=f(x)\text{ i }y=g(x)\text{).}\end{aligned}$$

d) $E=\mathcal{B}(A)=$ conjunt de funcions $f:A\to\mathbb{R}$ fitades (inferiorment i superior), amb $A$ conjunt arbitrari. Aleshores, $d(f,g)=\displaystyle\sup_{t\in A}|f(t)-g(t)|$ és una distància.
</solucio_de_referencia>

### Document a revisar

[1] Una equivalència són dues implicacions; les estudiem per separat. Suposem primer $A\cap B\neq\emptyset$ i sigui $c\in A\cap B$.
[2] Prenent $a=b=c$, el valor $d(c,c)=0$ pertany al conjunt $\{d(a,b)\mid a\in A,\ b\in B\}$. Com que l'ínfim és una fita superior del conjunt, $d(A,B)\leq d(c,c)=0$; i com que totes les distàncies són $\geq 0$, també $d(A,B)\geq 0$. Per tant $d(A,B)=0$.
[3] Recíprocament, suposem $d(A,B)=0$. Per la caracterització de l'ínfim, per a tot $\varepsilon>0$ existeixen $a\in A$ i $b\in B$ amb $d(a,b)<\varepsilon$.
[4] Això no garanteix que l'ínfim s'assoleixi: hi ha parelles a distància tan petita com vulguem, però potser cap a distància exactament $0$. Busquem, doncs, un contraexemple.
[5] Prenem $A=\{0\}$ i $B=B(0,1)\setminus\{0\}=\{x\in\mathbb{R}^m\mid 0<\|x\|<1\}$. Tots dos són no buits i $A\cap B=\emptyset$, perquè $0\notin B$.
[6] Per a tot $k\geq 2$, el punt $\frac1k e_1$ és de $B$ (té norma $\frac1k\in(0,1)$) i $d(0,\frac1k e_1)=\frac1k$. Com que $\frac1k\to 0$, existeix un punt $b\in B$ amb $d(0,b)=0$, i per tant $d(A,B)=0$.
[7] En conclusió, la implicació $A\cap B\neq\emptyset\Rightarrow d(A,B)=0$ és certa, però la recíproca és falsa: l'equivalència no és certa en general.


## t1-9a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Siguin $A\subset\mathbb{R}^m$ i $x\in\mathbb{R}^m$. Proveu que:

(a) $x\in Fr(A)\Leftrightarrow\exists$ successions convergents $(x_n)_{n\in\mathbb{N}}$ i $(y_n)_{n\in\mathbb{N}}$, ambdues amb límit $x$, tals que $\forall n\in\mathbb{N}$, $x_n\in A$ i $y_n\notin A$.
RESULTAT CORRECTE: Demostració de les dues implicacions. ($\Rightarrow$) Si $x\in Fr(A)$, per a cada $n\geq 1$ les interseccions $B_{1/n}(x)\cap A$ i $B_{1/n}(x)\cap A^c$ són no buides; triant $x_n$ a la primera i $y_n$ a la segona, $d(x_n,x)<1/n$ i $d(y_n,x)<1/n$, de manera que $x_n\to x$, $y_n\to x$, amb $x_n\in A$ i $y_n\notin A$. ($\Leftarrow$) Donat $r>0$, per convergència hi ha termes $x_n\in B_r(x)\cap A$ i $y_m\in B_r(x)\cap A^c$, així que $x\in Fr(A)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [directa_construir] Construir les successions  (teoria: T1.14, T1.16)
     objectiu: Suposant $x\in Fr(A)$, construir una successió de punts d'$A$ i una de punts d'$A^c$ que s'acostin a $x$.
     idea: Aplicar la definició de punt frontera amb una família numerable de radis que tendeixin a $0$, i triar un punt a cada intersecció.
     detall: Per a cada $n\geq 1$, com que $x\in Fr(A)$, tenim $B_{1/n}(x)\cap A\neq\varnothing$ i $B_{1/n}(x)\cap A^c\neq\varnothing$. Triem $x_n\in B_{1/n}(x)\cap A$ i $y_n\in B_{1/n}(x)\cap A^c$. Llavors $x_n\in A$, $y_n\notin A$ i $d(x_n,x)<1/n$, $d(y_n,x)<1/n$.
  2. [directa_convergencia] Comprovar la convergència  (teoria: T1.18)
     objectiu: Demostrar que les dues successions construïdes convergeixen a $x$.
     idea: Usar la fita de la distància de cada terme a $x$ i la definició de successió convergent.
     detall: Donat $\varepsilon>0$, prenem $n_0\in\mathbb{N}$ amb $n_0>1/\varepsilon$. Per a $n\geq n_0$: $d(x_n,x)<1/n\leq 1/n_0<\varepsilon$, i igualment $d(y_n,x)<\varepsilon$. Per tant $x_n\to x$ i $y_n\to x$.
  3. [reciproca] Implicació recíproca  (teoria: T1.18, T1.14)
     objectiu: Suposant que existeixen les dues successions, demostrar que $x\in Fr(A)$.
     idea: Fixat un radi qualsevol, la convergència de cada successió garanteix que algun terme cau dins la bola corresponent.
     detall: Sigui $r>0$. Com que $x_n\to x$, existeix $n$ amb $d(x_n,x)<r$, és a dir $x_n\in B_r(x)\cap A$. Com que $y_n\to x$, existeix $m$ amb $y_m\in B_r(x)\cap A^c$. Les dues interseccions són no buides per a tot $r>0$, per tant $x\in Fr(A)$.
ERRORS COMUNS:
  - [radi_fix] Tria tots els punts dins d'una mateixa bola de radi fix (o no fa dependre el radi de $n$), i per tant no pot garantir la convergència.
  - [confon_acumulacio] Exigeix $x_n\neq x$ o creu que $x$ no pot pertànyer a $A$, confonent frontera amb acumulació.
  - [reciproca_un_sol_radi] A la recíproca només comprova la condició per a radis de la forma $1/n$, o per a un radi concret, i no per a tot $r>0$.

TEORIA DEL CURS QUE FA SERVIR:
[T1.14] Definició 14 (Tema 1) — Tipus de punts d'un conjunt
Sigui $A\subseteq M$. Aleshores:

i) Un punt $x\in A$ és _interior_ a $A$ si existeix $r>0$ tal que $B_r(x)\subseteq A$.

ii) Un punt $x\in M$ és _d'acumulació_ d'$A$ si per a tot $r>0$ es té que $B_r(x)\cap(A\setminus\{x\})\neq\varnothing$.

iii) Un punt $x\in M$ és de la frontera d'$A$, si per a tot $r>0$ es té que $B_r(x)\cap A\neq\varnothing$ i també $B_r(x)\cap A^c\neq\varnothing$.

iv) Un punt $x\in M$ és _exterior_ d'$A$ si $x$ és interior a $A^c$ (és a dir, si existeix $r>0$ tal que $B_r(x)\subseteq A^c$).

[T1.16] Definició 16 (Tema 1) — Interior, derivat, frontera, clausura
Sigui $A\subseteq M$. Aleshores es defineixen:

i) _Interior_ d'$A$: $\mathring{A}=\{x\in A\mid x\text{ és interior a }A\}$. També s'acostuma a denotar per $\mathrm{int}(A)$.

ii) _Conjunt derivat_ d'$A$: $A'=\{x\in M\mid x\text{ és punt d'acumulació d'}A\}$.

iii) _Frontera_ d'$A$: $\mathrm{Fr}A=\{x\in M\mid x\text{ és de la frontera d'}A\}$. També és denota per $\partial A$.

iv) _Clausura_ o _adherència_ d'$A$: $\overline{A}=\{x\in M\mid\forall r>0\text{ es té que }B_r(x)\cap A\neq\varnothing\}$.
De manera equivalent, es pot definir de les dues maneres següents:
a) $\overline{A}=A\cup A'$; b) $\overline{A}$ és el conjunt tancat més petit que conté $A$.

v) _Exterior_ d'$A$: $\mathrm{ext}(A)=\mathrm{int}(A^c)$.

[T1.18] Definició 18 (Tema 1) — Successió convergent
Sigui $(M,d)$ un espai mètric. Direm que una successió $(x_n)_{n\in\mathbb{N}}$ és _convergent_ a $M$ si existeix $x\in M$ tal que $\forall\varepsilon>0,\exists n_0\in\mathbb{N}$ tal que $d(x_n,x)<\varepsilon$ $\forall n\geq n_0$. En aquest cas, diem que $x$ és el límit de la successió, i ho denotem per $x=\displaystyle\lim_{n\to\infty}x_n$ (el límit, si existeix, és únic).
</solucio_de_referencia>

### Document a revisar

[1] ($\Rightarrow$) Suposem $x\in Fr(A)$. Per definició, per a tot $r>0$ les interseccions $B_r(x)\cap A$ i $B_r(x)\cap A^c$ són no buides.
[2] Per a cada $n\geq 1$ ho apliquem amb $r=1/n$: triem $x_n\in B_{1/n}(x)\cap A$ i $y_n\in B_{1/n}(x)\cap A^c$. Així $x_n\in A$, $y_n\notin A$, $d(x_n,x)<1/n$ i $d(y_n,x)<1/n$.
[3] Vegem que $x_n\to x$. Donat $\varepsilon>0$, prenem $n_0\in\mathbb{N}$ amb $n_0>\varepsilon$; per a $n\geq n_0$ tenim $d(x_n,x)<1/n\leq 1/n_0<\varepsilon$.
[4] Exactament igual, de $d(y_n,x)<1/n$ es dedueix $y_n\to x$. Per tant tenim dues successions amb límit $x$, una de punts d'$A$ i l'altra de punts que no són d'$A$.
[5] ($\Leftarrow$) Suposem ara que existeixen successions $(x_n)$ i $(y_n)$, ambdues amb límit $x$, amb $x_n\in A$ i $y_n\notin A$ per a tot $n$.
[6] Sigui $r>0$ qualsevol. Com que $x_n\to x$, tenim $d(x_n,x)<r$ per a tot $n\in\mathbb{N}$; en particular $x_1\in B_r(x)\cap A$. Anàlogament, com que $y_n\to x$, existeix $m$ amb $d(y_m,x)<r$, és a dir, $y_m\in B_r(x)\cap A^c$. Com que $r>0$ és arbitrari, les dues interseccions són no buides per a tot $r>0$, i per tant $x\in Fr(A)$.
[7] Hem demostrat les dues implicacions, i per tant l'equivalència.

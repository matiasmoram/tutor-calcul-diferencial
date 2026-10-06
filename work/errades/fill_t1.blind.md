## t1-1a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Demostreu que a $\mathbb{R}^n$ les aplicacions $d_k$ són distàncies i, per tant, $(\mathbb{R}^n, d_k)$ són espais mètrics:

(a) $d_2(x,y)=\sqrt{\displaystyle\sum_{i=1}^{n}(x_i-y_i)^2}$.
RESULTAT CORRECTE: $d_2$ és una distància a $\mathbb{R}^n$: és no negativa i només s'anul·la si $x=y$, és simètrica i compleix la desigualtat triangular (aquesta última gràcies a la desigualtat de Cauchy-Schwarz per al producte escalar ordinari $\sum_i u_iv_i$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [positivitat] Positivitat  (teoria: T1.5)
     objectiu: Comprovar que $d_2(x,y)\geq 0$ i que $d_2(x,y)=0$ si i només si $x=y$.
     idea: Mirar el signe de cada sumand dins l'arrel i quan una suma de termes no negatius pot valer zero.
     detall: L'arrel quadrada positiva d'un nombre $\geq 0$ és $\geq 0$, així que $d_2(x,y)\geq 0$. Si $d_2(x,y)=0$, aleshores $\sum_{i=1}^n (x_i-y_i)^2=0$; com que cada sumand és $\geq 0$, tots són nuls, és a dir $x_i=y_i$ per a tot $i$, i per tant $x=y$. Recíprocament, si $x=y$ tots els sumands són $0$.
  2. [simetria] Simetria  (teoria: T1.5)
     objectiu: Comprovar que $d_2(x,y)=d_2(y,x)$.
     idea: Comparar terme a terme els sumands de les dues expressions.
     detall: $(x_i-y_i)^2=(y_i-x_i)^2$ per a cada $i$, per tant les dues sumes, i les seves arrels, coincideixen.
  3. [reduir_triangular] Reduir la desigualtat triangular  (teoria: T1.6+dem)
     objectiu: Reescriure la desigualtat triangular $d_2(x,y)\leq d_2(x,z)+d_2(z,y)$ com una desigualtat més simple sobre sumes.
     idea: Anomenar $u=x-z$, $v=z-y$ (de manera que $u+v=x-y$), observar que els dos costats són no negatius i elevar al quadrat per treure les arrels.
     detall: Amb $u=x-z$, $v=z-y$ cal veure $\sqrt{\sum_i(u_i+v_i)^2}\leq\sqrt{\sum_i u_i^2}+\sqrt{\sum_i v_i^2}$. Com que els dos costats són $\geq 0$, equival a la desigualtat dels quadrats:
$\sum_i u_i^2+2\sum_i u_iv_i+\sum_i v_i^2\leq\sum_i u_i^2+2\sqrt{\sum_i u_i^2}\sqrt{\sum_i v_i^2}+\sum_i v_i^2$,
és a dir, a $\sum_i u_iv_i\leq\sqrt{\sum_i u_i^2}\,\sqrt{\sum_i v_i^2}$.
  4. [cauchy_schwarz] Aplicar Cauchy-Schwarz  (teoria: T1.7, T1.8)
     objectiu: Justificar la desigualtat entre sumes obtinguda al pas anterior.
     idea: Reconèixer $\sum_i u_iv_i$ com el producte escalar ordinari de $\mathbb{R}^n$ i les arrels com les normes associades; aplicar el resultat del curs que fita el producte escalar per les normes.
     detall: Amb $\langle u,v\rangle=\sum_i u_iv_i$ (producte escalar ordinari) i $\|u\|=\sqrt{\langle u,u\rangle}$, Cauchy-Schwarz dona $\sum_i u_iv_i\leq|\langle u,v\rangle|\leq\|u\|\,\|v\|=\sqrt{\sum_i u_i^2}\sqrt{\sum_i v_i^2}$. Desfent el canvi, $d_2(x,y)\leq d_2(x,z)+d_2(z,y)$.
ERRORS COMUNS:
  - [quadrat_no_triangular] Demostra la desigualtat triangular per a $d_2^2$ (sense arrels) o eleva al quadrat i "simplifica" de manera que acaba provant una desigualtat diferent de la que cal.
  - [arrel_suma] Usa $\sqrt{a+b}=\sqrt{a}+\sqrt{b}$ (fals) per separar l'arrel en sumes de components.
  - [suma_zero] Afirma que de $\sum_i (x_i-y_i)^2=0$ se segueix $x=y$ sense justificar-ho (o amb un argument que també valdria per a sumes de termes de signe qualsevol).

TEORIA DEL CURS QUE FA SERVIR:
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
Demostració: **Demostració de la proposició 6:**

i) Sigui $E$ un espai euclidià i definim la norma $\|u\|=\sqrt{\langle u,u\rangle}$.
Vegem que satisfà les propietats que defineixen una norma:

- $\|u\|=\sqrt{\langle u,u\rangle}\geq 0$ ja que $\langle u,u\rangle\geq 0$. $\|u\|=0\iff\langle u,u\rangle=0\iff u=0$.
- $\|\lambda u\|=\sqrt{\langle\lambda u,\lambda u\rangle}=\sqrt{\lambda^2\langle u,u\rangle}=|\lambda|\sqrt{\langle u,u\rangle}=|\lambda|\,\|u\|$.
- Veure que $\|u+v\|\leq\|u\|+\|v\|$ és equivalent a veure que $(\|u+v\|)^2\leq(\|u\|+\|v\|)^2$ (ja que ambdós costats són positius).

Aleshores,

$$\|u+v\|^2=\langle u+v,u+v\rangle=\langle u,u\rangle+2\langle u,v\rangle+\langle v,v\rangle=\|u\|^2+\|v\|^2+2\langle u,v\rangle\ \underset{\text{Cauchy-Schwarz}}{\leq}\ \|u\|^2+\|v\|^2+2\|u\|\,\|v\|=(\|u\|+\|v\|)^2.$$

Per tant, $\|u\|=\sqrt{\langle u,u\rangle}$ és una norma i $(E,\|\cdot\|)$ és un espai normat.

ii) Anàlogament, veiem que si $(E,\|\cdot\|)$ és un espai normat i definim $d(u,v)=\|u-v\|$, aleshores $d(\cdot,\cdot)$ satisfà les propietats per a ser una distància i, per tant, $(E,d)$ és un espai mètric.

- $d(u,v)=\|u-v\|\geq 0$; $d(u,v)=0\iff\|u-v\|=0\iff u-v=0\iff u=v$.
- $d(u,v)=\|u-v\|=\|(-1)(v-u)\|=|-1|\,\|v-u\|=\|v-u\|=d(v,u)$.
- Respecte la desigualtat triangular:

$$\begin{aligned}d(u,w)&=\|u-w\|=\|u-v+v-w\|=\|(u-v)+(v-w)\|\\&\leq\|u-v\|+\|v-w\|=d(u,v)+d(v,w).\end{aligned}$$

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
</solucio_de_referencia>

### Document a revisar

[1] Cal veure que $d_2$ compleix les propietats de distància. Primer, $d_2(x,y)$ és l'arrel quadrada positiva del nombre $\sum_{i=1}^n(x_i-y_i)^2\geq 0$, per tant $d_2(x,y)\geq 0$.
[2] Si $d_2(x,y)=0$, aleshores $\sum_{i=1}^n(x_i-y_i)^2=0$, i com que una suma de nombres reals només pot valer $0$ si tots els sumands són nuls, $x_i=y_i$ per a tot $i$, és a dir, $x=y$. Recíprocament, si $x=y$ tots els sumands són $0$ i $d_2(x,y)=0$.
[3] Simetria: per a cada $i$, $(x_i-y_i)^2=(y_i-x_i)^2$, així que les dues sumes coincideixen i $d_2(x,y)=d_2(y,x)$.
[4] Desigualtat triangular: siguin $x,y,z\in\mathbb{R}^n$ i posem $u=x-z$, $v=z-y$, de manera que $u+v=x-y$. Cal veure que $\sqrt{\sum_i(u_i+v_i)^2}\leq\sqrt{\sum_i u_i^2}+\sqrt{\sum_i v_i^2}$.
[5] Elevar al quadrat conserva el sentit de qualsevol desigualtat entre nombres reals, de manera que això equival a $\sum_i u_i^2+2\sum_i u_iv_i+\sum_i v_i^2\leq\sum_i u_i^2+2\sqrt{\sum_i u_i^2}\sqrt{\sum_i v_i^2}+\sum_i v_i^2$, és a dir, a $\sum_i u_iv_i\leq\sqrt{\sum_i u_i^2}\sqrt{\sum_i v_i^2}$.
[6] Amb el producte escalar ordinari $\langle u,v\rangle=\sum_i u_iv_i$, la desigualtat de Cauchy-Schwarz dona $\sum_i u_iv_i\leq|\langle u,v\rangle|\leq\sqrt{\sum_i u_i^2}\sqrt{\sum_i v_i^2}$, que és el que calia.
[7] Desfent el canvi, $d_2(x,y)\leq d_2(x,z)+d_2(z,y)$, i per tant $d_2$ és una distància a $\mathbb{R}^n$.


## t1-2:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Demostreu que a $\mathbb{N}$ l'aplicació
$$d(m,n)=\begin{cases}\dfrac{1}{m}+\dfrac{1}{n} & \text{si } m\neq n\\ 0 & \text{si } m=n\end{cases}$$
és una distància i, per tant, $(\mathbb{N},d)$ és un espai mètric.
RESULTAT CORRECTE: $d$ és una distància a $\mathbb{N}=\{1,2,3,\dots\}$: és $\geq 0$ i nul·la només si $m=n$ (perquè $\frac1m+\frac1n>0$), és simètrica, i la desigualtat triangular $d(m,n)\leq d(m,k)+d(k,n)$ es comprova per casos (si $m=n$ és trivial; si $k=m$ o $k=n$ és una igualtat; si $k\neq m,n$ el costat dret val $\frac1m+\frac2k+\frac1n>\frac1m+\frac1n$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [positivitat] Positivitat  (teoria: T1.5)
     objectiu: Comprovar que $d(m,n)\geq 0$ i que $d(m,n)=0\iff m=n$.
     idea: Mirar el signe de $\frac1m+\frac1n$ per a naturals $m,n$.
     detall: Si $m=n$, $d=0$. Si $m\neq n$, $d(m,n)=\frac1m+\frac1n>0$ perquè $m,n\geq 1$. Per tant $d\geq 0$ i $d(m,n)=0\iff m=n$.
  2. [simetria] Simetria  (teoria: T1.5)
     objectiu: Comprovar que $d(m,n)=d(n,m)$.
     idea: La condició $m\neq n$ i l'expressió de la fórmula són simètriques en $m$ i $n$.
     detall: Si $m=n$ tots dos valen $0$; si $m\neq n$, $\frac1m+\frac1n=\frac1n+\frac1m$.
  3. [triangular_casos] Desigualtat triangular per casos  (teoria: T1.5)
     objectiu: Demostrar que $d(m,n)\leq d(m,k)+d(k,n)$ per a tots $m,n,k\in\mathbb{N}$.
     idea: Com que la definició va per casos, separar segons quins dels tres naturals coincideixen.
     detall: Si $m=n$: el costat esquerre és $0$ i el dret és $\geq 0$.
Si $m\neq n$ i $k=m$: el costat dret és $0+d(m,n)$, igualtat. Anàlogament si $k=n$.
Si $k\neq m$ i $k\neq n$ (i $m\neq n$): el costat dret és $\frac1m+\frac1k+\frac1k+\frac1n=\frac1m+\frac1n+\frac2k>\frac1m+\frac1n=d(m,n)$.
ERRORS COMUNS:
  - [oblida_casos] Només tracta el cas en què $m,n,k$ són diferents dos a dos i oblida els casos en què $k$ coincideix amb $m$ o amb $n$ (o $m=n$).
  - [zero_natural] Considera $0\in\mathbb{N}$, on la fórmula no té sentit ($\frac10$), o no fa servir enlloc que $m,n\geq 1$.
  - [positivitat_sense_justificar] Afirma $d(m,n)=0\iff m=n$ sense justificar que $\frac1m+\frac1n$ no pot ser $0$.

TEORIA DEL CURS QUE FA SERVIR:
[T1.5] Definició 5 (Tema 1) — Distància
Sigui $M$ un conjunt. Una funció $d(\cdot,\cdot):M\times M\longrightarrow\mathbb{R}$ es diu que és una _distància_ si per a tot $x,y,z\in M$, es compleixen:

i) $d(x,y)\geq 0$; $d(x,y)=0\iff x=y$.

ii) $d(x,y)=d(y,x)$ (simètrica).

iii) $d(x,y)\leq d(x,z)+d(z,y)$ (desigualtat triangular).

Direm en aquest cas que $(M,d)$ és un _espai mètric_.
</solucio_de_referencia>

### Document a revisar

[1] Treballem a $\mathbb{N}=\{1,2,3,\dots\}$, on $\frac1m$ té sentit per a tot $m$. Positivitat: si $m=n$, $d(m,n)=0$; si $m\neq n$, $d(m,n)=\frac1m+\frac1n\geq1$ perquè $m,n\geq1$, i en particular $d(m,n)>0$. Per tant $d\geq 0$ i $d(m,n)=0\iff m=n$.
[2] Simetria: si $m=n$ tots dos valors són $0$, i si $m\neq n$, $d(m,n)=\frac1m+\frac1n=\frac1n+\frac1m=d(n,m)$.
[3] Desigualtat triangular: volem $d(m,n)\leq d(m,k)+d(k,n)$ per a tots $m,n,k\in\mathbb{N}$. Com que la definició va per casos, separem segons quins dels tres naturals coincideixen. Si $m=n$, el costat esquerre és $0$ i el dret és $\geq 0$.
[4] Si $m\neq n$ i $k=m$, el costat dret és $d(m,m)+d(m,n)=\frac2m+\frac1n$, que és més gran que $d(m,n)=\frac1m+\frac1n$. El cas $k=n$ és anàleg.
[5] Finalment, si $m\neq n$, $k\neq m$ i $k\neq n$, el costat dret és $\frac1m+\frac1k+\frac1k+\frac1n=\frac1m+\frac1n+\frac2k$, que és més gran que $\frac1m+\frac1n=d(m,n)$ perquè $\frac2k>0$.
[6] Com que aquests casos cobreixen totes les possibilitats, $d$ compleix la desigualtat triangular. Per tant $d$ és una distància i $(\mathbb{N},d)$ és un espai mètric.


## t1-3a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Demostreu que a $\mathbb{R}^n$ les aplicacions següents són normes:

(a) $\|x\|_2=\sqrt{\sum_{i=1}^{n}x_i^2}$.
RESULTAT CORRECTE: $\|\cdot\|_2$ és una norma a $\mathbb{R}^n$: és $\geq 0$ i nul·la només per a $x=0$, és homogènia ($\|\lambda x\|_2=|\lambda|\,\|x\|_2$) i compleix la desigualtat triangular (via Cauchy-Schwarz per al producte escalar ordinari). Equivalentment, és la norma induïda pel producte escalar ordinari.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [positivitat] Positivitat  (teoria: T1.3)
     objectiu: Comprovar que $\|x\|_2\geq 0$ i que $\|x\|_2=0\iff x=0$.
     idea: Signe dels sumands dins l'arrel i quan una suma de termes no negatius s'anul·la.
     detall: $\|x\|_2$ és l'arrel positiva d'una suma de quadrats, per tant $\geq 0$. Si $\sum_i x_i^2=0$, com que cada $x_i^2\geq 0$, tots són $0$ i $x=0$; el recíproc és immediat.
  2. [homogeneitat] Homogeneïtat  (teoria: T1.3)
     objectiu: Comprovar que $\|\lambda x\|_2=|\lambda|\,\|x\|_2$ per a tot $\lambda\in\mathbb{R}$.
     idea: Treure el factor comú dins l'arrel i recordar quant val $\sqrt{\lambda^2}$.
     detall: $\|\lambda x\|_2=\sqrt{\sum_i\lambda^2x_i^2}=\sqrt{\lambda^2}\sqrt{\sum_i x_i^2}=|\lambda|\,\|x\|_2$.
  3. [triangular] Desigualtat triangular  (teoria: T1.7, T1.8, T1.6+dem)
     objectiu: Demostrar que $\|x+y\|_2\leq\|x\|_2+\|y\|_2$.
     idea: Com que els dos costats són no negatius, comparar-ne els quadrats; desenvolupar $\|x+y\|_2^2$ i fitar el terme creuat amb un resultat del curs sobre productes escalars.
     detall: $\|x+y\|_2^2=\sum_i(x_i+y_i)^2=\|x\|_2^2+2\sum_i x_iy_i+\|y\|_2^2$. Per Cauchy-Schwarz amb el producte escalar ordinari $\langle x,y\rangle=\sum_i x_iy_i$ (que compleix $\|x\|_2=\sqrt{\langle x,x\rangle}$): $\sum_i x_iy_i\leq\|x\|_2\|y\|_2$. Per tant $\|x+y\|_2^2\leq(\|x\|_2+\|y\|_2)^2$ i, prenent arrels (tots dos costats $\geq 0$), $\|x+y\|_2\leq\|x\|_2+\|y\|_2$.
ERRORS COMUNS:
  - [lambda_sense_valor_absolut] Escriu $\sqrt{\lambda^2}=\lambda$, oblidant el cas $\lambda<0$.
  - [arrel_suma] Usa $\sqrt{a+b}=\sqrt a+\sqrt b$ per "separar" l'arrel en la desigualtat triangular.
  - [quadrats_sense_signe] Passa de $A^2\leq B^2$ a $A\leq B$ sense comprovar que $A,B\geq 0$.

TEORIA DEL CURS QUE FA SERVIR:
[T1.3] Definició 3 (Tema 1) — Norma
Una funció $\|\cdot\|:E\longrightarrow\mathbb{R}$ es diu que és una _norma_ si compleix, $\forall u,v\in E$:

i) $\|u\|\geq 0$; $\|u\|=0\iff u=0$.

ii) $\|\lambda u\|=|\lambda|\,\|u\|$, $\forall\lambda\in\mathbb{R}$.

iii) $\|u+v\|\leq\|u\|+\|v\|$ (desigualtat triangular).

En aquest cas es diu que $(E,\|\cdot\|)$ és un _espai normat_.

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

[T1.6] Proposició 6 (Tema 1) — Euclidià implica normat implica mètric
i) Tot espai euclidià és un espai normat si definim $\|u\|=\sqrt{\langle u,u\rangle}$.

ii) Tot espai normat és un espai mètric si prenem $d(u,v)=\|u-v\|$.

[Figura: diagrama de conjunts imbricats: espais euclidians dins d'espais normats dins d'espais mètrics.]

Figura 1: Espais euclidians $\subset$ espais normats $\subset$ espais mètrics.

Per a demostrar aquesta proposició usarem, en algun moment, el següent resultat:
Demostració: **Demostració de la proposició 6:**

i) Sigui $E$ un espai euclidià i definim la norma $\|u\|=\sqrt{\langle u,u\rangle}$.
Vegem que satisfà les propietats que defineixen una norma:

- $\|u\|=\sqrt{\langle u,u\rangle}\geq 0$ ja que $\langle u,u\rangle\geq 0$. $\|u\|=0\iff\langle u,u\rangle=0\iff u=0$.
- $\|\lambda u\|=\sqrt{\langle\lambda u,\lambda u\rangle}=\sqrt{\lambda^2\langle u,u\rangle}=|\lambda|\sqrt{\langle u,u\rangle}=|\lambda|\,\|u\|$.
- Veure que $\|u+v\|\leq\|u\|+\|v\|$ és equivalent a veure que $(\|u+v\|)^2\leq(\|u\|+\|v\|)^2$ (ja que ambdós costats són positius).

Aleshores,

$$\|u+v\|^2=\langle u+v,u+v\rangle=\langle u,u\rangle+2\langle u,v\rangle+\langle v,v\rangle=\|u\|^2+\|v\|^2+2\langle u,v\rangle\ \underset{\text{Cauchy-Schwarz}}{\leq}\ \|u\|^2+\|v\|^2+2\|u\|\,\|v\|=(\|u\|+\|v\|)^2.$$

Per tant, $\|u\|=\sqrt{\langle u,u\rangle}$ és una norma i $(E,\|\cdot\|)$ és un espai normat.

ii) Anàlogament, veiem que si $(E,\|\cdot\|)$ és un espai normat i definim $d(u,v)=\|u-v\|$, aleshores $d(\cdot,\cdot)$ satisfà les propietats per a ser una distància i, per tant, $(E,d)$ és un espai mètric.

- $d(u,v)=\|u-v\|\geq 0$; $d(u,v)=0\iff\|u-v\|=0\iff u-v=0\iff u=v$.
- $d(u,v)=\|u-v\|=\|(-1)(v-u)\|=|-1|\,\|v-u\|=\|v-u\|=d(v,u)$.
- Respecte la desigualtat triangular:

$$\begin{aligned}d(u,w)&=\|u-w\|=\|u-v+v-w\|=\|(u-v)+(v-w)\|\\&\leq\|u-v\|+\|v-w\|=d(u,v)+d(v,w).\end{aligned}$$
</solucio_de_referencia>

### Document a revisar

[1] Hem de veure que $\|x\|_2=\sqrt{\sum_{i=1}^n x_i^2}$ compleix les propietats de norma. És l'arrel quadrada positiva d'una suma de quadrats, per tant $\|x\|_2\geq 0$.
[2] Si $\|x\|_2=0$, aleshores $\sum_i x_i^2=0$; com que cada $x_i^2\geq 0$, tots els sumands són nuls, $x_i=0$ per a tot $i$ i $x=0$. Recíprocament, $\|0\|_2=0$.
[3] Homogeneïtat: per a $\lambda\in\mathbb{R}$, $\|\lambda x\|_2=\sqrt{\sum_i\lambda^2x_i^2}=\sqrt{\lambda^2}\sqrt{\sum_i x_i^2}$, i com que $\sqrt{\lambda^2}=\lambda$, obtenim $\|\lambda x\|_2=\lambda\|x\|_2$.
[4] Desigualtat triangular: desenvolupant el quadrat, $\|x+y\|_2^2=\sum_i(x_i+y_i)^2=\|x\|_2^2+2\sum_i x_iy_i+\|y\|_2^2$.
[5] Considerem el producte escalar ordinari $\langle x,y\rangle=\sum_i x_iy_i$, que compleix $\|x\|_2=\sqrt{\langle x,x\rangle}$. Per Cauchy-Schwarz, $|\langle x,y\rangle|=\|x\|_2\|y\|_2$, i en particular $\sum_i x_iy_i\leq\|x\|_2\|y\|_2$.
[6] Per tant $\|x+y\|_2^2\leq\|x\|_2^2+2\|x\|_2\|y\|_2+\|y\|_2^2=(\|x\|_2+\|y\|_2)^2$.
[7] Com que $\|x+y\|_2$ i $\|x\|_2+\|y\|_2$ són tots dos $\geq 0$, prenent arrels obtenim $\|x+y\|_2\leq\|x\|_2+\|y\|_2$. Així $\|\cdot\|_2$ és una norma a $\mathbb{R}^n$.


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
[6] Per a tot $k\geq 1$, el punt $\frac1k e_1$ és de $B$ i $d(0,\frac1k e_1)=\frac1k$, així que $0\leq d(A,B)\leq\frac1k$ per a tots aquests $k$ i, per tant, $d(A,B)=0$.
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
[6] Com que $x_n\to x$, existeix $n$ amb $d(x_n,x)<1$, és a dir, $x_n\in B_1(x)\cap A$; anàlogament existeix $m$ amb $y_m\in B_1(x)\cap A^c$. Com que la bola $B_1(x)$ talla $A$ i $A^c$, $x\in Fr(A)$.
[7] Hem demostrat les dues implicacions, i per tant l'equivalència.


## t1-10b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Si $A\subset\mathbb{R}^m$, demostreu que

(b) $\overline{A}$ és el conjunt tancat més petit que conté $A$, és a dir, si $C$ és un tancat que conté $A$, aleshores $\overline{A}\subset C$.
RESULTAT CORRECTE: (1) $A\subseteq\overline{A}$, ja que $x\in B_r(x)\cap A$ si $x\in A$. (2) $\overline{A}$ és tancat: si $x\notin\overline{A}$ hi ha $r>0$ amb $B_r(x)\cap A=\varnothing$; per a $y\in B_r(x)$, una bola $B_s(y)\subseteq B_r(x)$ tampoc talla $A$, així $B_r(x)\subseteq(\overline{A})^c$, que és obert. (3) Si $C\supseteq A$ és tancat i $x\notin C$, existeix $r>0$ amb $B_r(x)\subseteq C^c\subseteq A^c$, és a dir $B_r(x)\cap A=\varnothing$ i $x\notin\overline{A}$; per tant $\overline{A}\subseteq C$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [conte_A] A està contingut a la clausura  (teoria: T1.16, T1.11)
     objectiu: Comprovar que $A\subseteq\overline{A}$.
     idea: Usar la definició de clausura amb boles i el fet que el centre pertany a la bola.
     detall: Si $x\in A$, per a tot $r>0$, $x\in B_r(x)\cap A$, que és no buit. Per tant $x\in\overline{A}$.
  2. [clausura_tancada] La clausura és tancada  (teoria: T1.11, T1.12, T1.16)
     objectiu: Demostrar que $\overline{A}$ és un conjunt tancat.
     idea: Veure que el complementari és obert: negar la definició de clausura i usar que les boles obertes són oberts.
     detall: Sigui $x\notin\overline{A}$: existeix $r>0$ amb $B_r(x)\cap A=\varnothing$. Per a $y\in B_r(x)$, amb $s=r-d(x,y)>0$ es té $B_s(y)\subseteq B_r(x)$ (Proposició 12(i)), de manera que $B_s(y)\cap A=\varnothing$ i $y\notin\overline{A}$. Així $B_r(x)\subseteq(\overline{A})^c$, que és obert, i $\overline{A}$ és tancat.
  3. [minimalitat] Minimalitat  (teoria: T1.11, T1.16)
     objectiu: Demostrar que si $C$ és tancat i $A\subseteq C$, llavors $\overline{A}\subseteq C$.
     idea: Provar la inclusió contrarecíproca: un punt fora de $C$ queda fora de $\overline{A}$, usant que $C^c$ és obert.
     detall: Sigui $x\notin C$. Com que $C^c$ és obert, existeix $r>0$ amb $B_r(x)\subseteq C^c\subseteq A^c$, és a dir $B_r(x)\cap A=\varnothing$. Per tant $x\notin\overline{A}$. Així $C^c\subseteq(\overline{A})^c$, és a dir $\overline{A}\subseteq C$.
ERRORS COMUNS:
  - [cita_definicio] Cita la caracterització "$\overline{A}$ és el tancat més petit que conté $A$" de la Definició 16 com a prova, que és justament el que es demana demostrar.
  - [oblida_tancat] Demostra la minimalitat però no comprova que $\overline{A}$ sigui tancat.
  - [circular_17] Per veure que $\overline{A}$ és tancat, usa $\overline{\overline{A}}=\overline{A}$ sense demostrar-ho.

TEORIA DEL CURS QUE FA SERVIR:
[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.

[T1.16] Definició 16 (Tema 1) — Interior, derivat, frontera, clausura
Sigui $A\subseteq M$. Aleshores es defineixen:

i) _Interior_ d'$A$: $\mathring{A}=\{x\in A\mid x\text{ és interior a }A\}$. També s'acostuma a denotar per $\mathrm{int}(A)$.

ii) _Conjunt derivat_ d'$A$: $A'=\{x\in M\mid x\text{ és punt d'acumulació d'}A\}$.

iii) _Frontera_ d'$A$: $\mathrm{Fr}A=\{x\in M\mid x\text{ és de la frontera d'}A\}$. També és denota per $\partial A$.

iv) _Clausura_ o _adherència_ d'$A$: $\overline{A}=\{x\in M\mid\forall r>0\text{ es té que }B_r(x)\cap A\neq\varnothing\}$.
De manera equivalent, es pot definir de les dues maneres següents:
a) $\overline{A}=A\cup A'$; b) $\overline{A}$ és el conjunt tancat més petit que conté $A$.

v) _Exterior_ d'$A$: $\mathrm{ext}(A)=\mathrm{int}(A^c)$.

[T1.12] Proposició 12 (Tema 1) — Propietats dels conjunts oberts
(Propietats dels conjunts oberts.) Sigui $(M,d)$ un espai mètric. Aleshores,

i) tota bola oberta $B_r(x)$ és un conjunt obert;

ii) la unió arbitrària (finita o infinita) d'oberts és un obert;

iii) la intersecció finita d'oberts és un obert;

iv) $M$ i $\varnothing$ són conjunts oberts.
</solucio_de_referencia>

### Document a revisar

[1] Hem de veure tres coses: que $A\subseteq\overline{A}$, que $\overline{A}$ és tancat i que tot tancat $C\supseteq A$ conté $\overline{A}$. Recordem que $x\in\overline{A}$ si i només si $B_r(x)\cap A\neq\varnothing$ per a tot $r>0$.
[2] Si $x\in A$, per a tot $r>0$ tenim $x\in B_r(x)\cap A$, que per tant és no buit. Així $A\subseteq\overline{A}$.
[3] Per veure que $\overline{A}$ és tancat, veurem que el seu complementari és obert. Sigui $x\notin\overline{A}$: existeix $r>0$ amb $B_r(x)\cap A=\varnothing$.
[4] Per a $y\in B_r(x)$, amb $s=r+d(x,y)>0$ es té $B_s(y)\subseteq B_r(x)$, i per tant $B_s(y)\cap A=\varnothing$, és a dir, $y\notin\overline{A}$.
[5] Així $B_r(x)\subseteq(\overline{A})^c$ per a cada $x\in(\overline{A})^c$, de manera que $(\overline{A})^c$ és obert i $\overline{A}$ és tancat.
[6] Minimalitat: sigui $C$ un tancat amb $A\subseteq C$, i sigui $x\notin C$. Com que $C^c$ és obert, existeix $r>0$ amb $B_r(x)\subseteq C^c$.
[7] Com que $A\subseteq C$, tenim $A^c\subseteq C^c$, i per tant $B_r(x)\subseteq A^c$.
[8] És a dir, $B_r(x)\cap A=\varnothing$ i $x\notin\overline{A}$. Hem vist $C^c\subseteq(\overline{A})^c$, o sigui, $\overline{A}\subseteq C$: $\overline{A}$ és el tancat més petit que conté $A$.


## t1-11a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Donats dos subconjunts $A,B\subseteq\mathbb{R}^n$, es defineix $A+B=\{x+y\mid x\in A,\ y\in B\}$. Suposem que $A$ és obert.

(a) Demostreu que si $y\in\mathbb{R}^n$, el conjunt $A+\{y\}$ és obert.
RESULTAT CORRECTE: Sigui $z\in A+\{y\}$; llavors $a=z-y\in A$ i, com que $A$ és obert, hi ha $r>0$ amb $B_r(a)\subseteq A$. Si $w\in B_r(z)$, $\|(w-y)-a\|=\|w-z\|<r$, així $w-y\in A$ i $w=(w-y)+y\in A+\{y\}$. Per tant $B_r(z)\subseteq A+\{y\}$ i $A+\{y\}$ és obert (el traslladat d'una bola és la bola del mateix radi centrada al punt traslladat).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [pertinenca] Caracteritzar la pertinença
     objectiu: Descriure quan un punt $z$ pertany a $A+\{y\}$ en termes d'$A$.
     idea: Restar $y$.
     detall: $z\in A+\{y\}\iff z=a+y$ amb $a\in A\iff z-y\in A$.
  2. [bola_traslladada] Trobar una bola  (teoria: T1.11, T1.6)
     objectiu: Donat $z\in A+\{y\}$, trobar una bola centrada en $z$ continguda a $A+\{y\}$.
     idea: Usar que $A$ és obert en el punt $z-y$ i veure que la distància és invariant per translacions.
     detall: Sigui $a=z-y\in A$ i $r>0$ amb $B_r(a)\subseteq A$. Si $w\in B_r(z)$, llavors $\|(w-y)-a\|=\|w-z\|<r$, de manera que $w-y\in B_r(a)\subseteq A$ i $w\in A+\{y\}$. Per tant $B_r(z)\subseteq A+\{y\}$.
ERRORS COMUNS:
  - [radi_canviat] Busca un radi nou o diferent sense adonar-se que la translació conserva distàncies.
  - [nomes_intuicio] Diu que "una translació d'un obert és obert" sense comprovar la inclusió de boles.

TEORIA DEL CURS QUE FA SERVIR:
[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.

[T1.6] Proposició 6 (Tema 1) — Euclidià implica normat implica mètric
i) Tot espai euclidià és un espai normat si definim $\|u\|=\sqrt{\langle u,u\rangle}$.

ii) Tot espai normat és un espai mètric si prenem $d(u,v)=\|u-v\|$.

[Figura: diagrama de conjunts imbricats: espais euclidians dins d'espais normats dins d'espais mètrics.]

Figura 1: Espais euclidians $\subset$ espais normats $\subset$ espais mètrics.

Per a demostrar aquesta proposició usarem, en algun moment, el següent resultat:
</solucio_de_referencia>

### Document a revisar

[1] Recordem que un conjunt $U\subseteq\mathbb{R}^n$ és obert si existeix $r>0$ tal que $B_r(u)\subseteq U$ per a tot $u\in U$.
[2] Primer caracteritzem la pertinença: $z\in A+\{y\}\iff z=a+y$ per a algun $a\in A\iff z-y\in A$.
[3] Sigui $z\in A+\{y\}$ i posem $a=z-y$, que és d'$A$. Com que $A$ és obert, existeix $r>0$ amb $B_r(a)\subseteq A$.
[4] Vegem que $B_r(z)\subseteq A+\{y\}$. Sigui $w\in B_r(z)$. Aleshores $\|(w-y)-a\|=\|w-y-(z-y)\|=\|w-z\|<r$, és a dir, $w-y\in B_r(a)\subseteq A$.
[5] Per tant $w=(w-y)-y$ amb $w-y\in A$, i $w\in A+\{y\}$.
[6] Així $B_r(z)\subseteq A+\{y\}$. Com que $z\in A+\{y\}$ era arbitrari, $A+\{y\}$ és obert: la translació conserva les distàncies i porta boles a boles del mateix radi.


## t1-12b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Estudieu si són compactes els conjunts següents. Per als que no ho siguin, trobeu el compacte més petit que els conté (si és que n'hi ha cap).

(b) $B=\{(x,y,z)\in\mathbb{R}^3\mid x=2,\ y=3,\ \text{i } z\in(-1,1)\}$.
RESULTAT CORRECTE: $B$ no és compacte: és fitat però no tancat ($(2,3,1)\in\overline{B}\setminus B$). El compacte més petit que el conté és $\overline{B}=\{(2,3,z)\mid z\in[-1,1]\}$ (el conjunt $C$ de l'apartat (c)).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [fitat] Fitat  (teoria: T1.33)
     objectiu: Decidir si $B$ és fitat.
     idea: Trobar una bola que el contingui.
     detall: Per a $(2,3,z)\in B$, $\|(2,3,z)-(2,3,0)\|=|z|<1$, així $B\subseteq B_1((2,3,0))$: és fitat.
  2. [tancat] Tancat?  (teoria: T1.19, T1.34, T1.27)
     objectiu: Decidir si $B$ és tancat.
     idea: Usar la caracterització dels tancats amb successions: estudiar on poden anar a parar els límits de successions de punts de $B$.
     detall: $(2,3,1-1/n)\in B$ i convergeix a $(2,3,1)\notin B$. Per la Proposició 19(iii), $B$ no és tancat, i per Heine-Borel (o Lema 27) no és compacte.
  3. [minim] Compacte més petit  (teoria: T1.27, T1.16, T1.19, T1.34)
     objectiu: Trobar el compacte més petit que conté $B$, si n'hi ha.
     idea: Tot compacte és tancat, i el tancat més petit que conté un conjunt és la seva clausura (problema 10b). Calcular la clausura i comprovar que és compacta.
     detall: Si $K\supseteq B$ és compacte, és tancat (Lema 27), i llavors $K\supseteq\overline{B}$. El segment $S=\{(2,3,z)\mid z\in[-1,1]\}$ és tancat i conté $B$, i els seus extrems $(2,3,\pm1)$ són límits de punts de $B$; per tant $\overline{B}=S$. $S$ és tancat i fitat, compacte per Heine-Borel. Així $S$ és el compacte més petit que conté $B$.
ERRORS COMUNS:
  - [fitat_implica_compacte] Conclou que $B$ és compacte només perquè és fitat.
  - [compacte_minim_arbitrari] Proposa un compacte que conté $B$ (una bola tancada, un cub) però no el més petit, o no justifica la minimalitat.
  - [tancat_en_recta] Pensa que $B$ és tancat perquè és la intersecció dels plans $x=2$, $y=3$ amb alguna cosa, sense mirar els extrems.

TEORIA DEL CURS QUE FA SERVIR:
[T1.24] Definició 24 (Tema 1) — Compacte i seqüencialment compacte
Sigui $(M,d)$ espai mètric, $A\subseteq M$.

i) $A$ és _compacte_ si tot recobriment per oberts de $A$ admet un subrecobriment finit, és a dir: si $A\subseteq\bigcup_{i\in I}U_i$, amb $U_i$ obert, aleshores existeixen $i_1,\ldots,i_k\in I$ tals que $A\subseteq\bigcup_{j=1}^k U_{i_j}$.

ii) $A$ és _seqüencialment compacte_ si tota successió $(x_n)_{n\in\mathbb{N}}\subseteq A$ admet una subsuccessió (una parcial) convergent a un punt de $A$.

[T1.33] Definició 33 (Tema 1) — Conjunt fitat
Es diu que $A\subseteq M$ és _fitat_ si i només si existeix un $x\in M$ i un valor $L>0$ tal que $A\subseteq B_L(x)$.

[T1.19] Proposició 19 (Tema 1) — Caracterització amb successions
Sigui $(M,d)$ un espai mètric, $A\subseteq M$ i $x\in M$. Aleshores:

i) $x$ és un punt d'acumulació d'$A\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\neq x$, $a_n\in A$, tal que $x=\lim_n a_n$.

ii) $x\in\overline{A}\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\in A$ tal que $x=\lim_n a_n$.

iii) $A$ és tancat $\Leftrightarrow$ el límit de tota successió convergent d'elements d'$A$ és d'$A$.

[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.

[T1.27] Lema 27 (Tema 1) — Compacte implica tancat
$A$ compacte $\Rightarrow$ $A$ tancat.

[T1.16] Definició 16 (Tema 1) — Interior, derivat, frontera, clausura
Sigui $A\subseteq M$. Aleshores es defineixen:

i) _Interior_ d'$A$: $\mathring{A}=\{x\in A\mid x\text{ és interior a }A\}$. També s'acostuma a denotar per $\mathrm{int}(A)$.

ii) _Conjunt derivat_ d'$A$: $A'=\{x\in M\mid x\text{ és punt d'acumulació d'}A\}$.

iii) _Frontera_ d'$A$: $\mathrm{Fr}A=\{x\in M\mid x\text{ és de la frontera d'}A\}$. També és denota per $\partial A$.

iv) _Clausura_ o _adherència_ d'$A$: $\overline{A}=\{x\in M\mid\forall r>0\text{ es té que }B_r(x)\cap A\neq\varnothing\}$.
De manera equivalent, es pot definir de les dues maneres següents:
a) $\overline{A}=A\cup A'$; b) $\overline{A}$ és el conjunt tancat més petit que conté $A$.

v) _Exterior_ d'$A$: $\mathrm{ext}(A)=\mathrm{int}(A^c)$.
</solucio_de_referencia>

### Document a revisar

[1] Per Heine-Borel, un subconjunt de $\mathbb{R}^3$ és compacte si i només si és tancat i fitat. Estudiem les dues condicions per a $B=\{(2,3,z)\mid z\in(-1,1)\}$.
[2] Fitat: per a $(2,3,z)\in B$, $\|(2,3,z)\|=|z|<1$, així $B\subseteq B_1((0,0,0))$ i $B$ és fitat.
[3] Tancat: la successió $(2,3,1-\frac1n)$ és de $B$ per a tot $n\geq 1$ i convergeix a $(2,3,1)\notin B$. Per la caracterització seqüencial dels tancats, $B$ no és tancat, i per tant no és compacte.
[4] Busquem el compacte més petit que conté $B$. Tot tancat que conté $B$ és compacte, de manera que el compacte més petit que conté $B$ és el tancat més petit que el conté, és a dir, $\overline{B}$.
[5] Calculem $\overline{B}$. El segment $S=\{(2,3,z)\mid z\in[-1,1]\}$ és tancat i conté $B$, així que $\overline{B}\subseteq S$; a més els extrems $(2,3,\pm1)$ són límits de punts de $B$, així que $S\subseteq\overline{B}$. Per tant $\overline{B}=S$.
[6] $S$ és tancat i fitat, i per tant compacte per Heine-Borel. Així el compacte més petit que conté $B$ és $S=\{(2,3,z)\mid z\in[-1,1]\}$.


## t1-13a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Demostreu que

(a) la intersecció d'un nombre arbitrari (finit o infinit) de subconjunts compactes de $\mathbb{R}^n$ també és compacte,
RESULTAT CORRECTE: Sigui $\{K_i\}_{i\in I}$ ($I\neq\varnothing$) una família de compactes. Cada $K_i$ és tancat (Lema 27), així $K=\bigcap_i K_i$ és tancat (Proposició 13(ii)). Fixat $i_0\in I$, $K\subseteq K_{i_0}$, compacte, i un tancat contingut en un compacte és compacte (Lema 28). Per tant $K$ és compacte.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [tancat] La intersecció és tancada  (teoria: T1.27, T1.13)
     objectiu: Demostrar que $\bigcap_{i\in I}K_i$ és un conjunt tancat.
     idea: Relacionar compacte amb tancat i usar com es comporten els tancats per interseccions.
     detall: Cada $K_i$ és tancat pel Lema 27, i la intersecció arbitrària de tancats és tancada (Proposició 13(ii)).
  2. [dins_compacte] Tancat dins d'un compacte  (teoria: T1.28)
     objectiu: Deduir la compacitat de la intersecció.
     idea: La intersecció està continguda en qualsevol dels $K_i$; usar el resultat sobre tancats continguts en compactes.
     detall: Fixat $i_0\in I$, $\bigcap_i K_i\subseteq K_{i_0}$, compacte. Pel Lema 28, un tancat contingut en un compacte és compacte.
ERRORS COMUNS:
  - [subrecobriment_directe] Intenta extreure directament un subrecobriment finit de la intersecció sense justificar per què el recobriment d'un subconjunt es pot "estendre".
  - [oblida_tancat] Diu que la intersecció és compacta "perquè està dins d'un compacte", oblidant que cal que sigui tancada.

TEORIA DEL CURS QUE FA SERVIR:
[T1.24] Definició 24 (Tema 1) — Compacte i seqüencialment compacte
Sigui $(M,d)$ espai mètric, $A\subseteq M$.

i) $A$ és _compacte_ si tot recobriment per oberts de $A$ admet un subrecobriment finit, és a dir: si $A\subseteq\bigcup_{i\in I}U_i$, amb $U_i$ obert, aleshores existeixen $i_1,\ldots,i_k\in I$ tals que $A\subseteq\bigcup_{j=1}^k U_{i_j}$.

ii) $A$ és _seqüencialment compacte_ si tota successió $(x_n)_{n\in\mathbb{N}}\subseteq A$ admet una subsuccessió (una parcial) convergent a un punt de $A$.

[T1.27] Lema 27 (Tema 1) — Compacte implica tancat
$A$ compacte $\Rightarrow$ $A$ tancat.

[T1.13] Proposició 13 (Tema 1) — Propietats dels conjunts tancats
Sigui $M$ un conjunt i $d$ una distància definida sobre ell. Considereu la topologia sobre $M$ induïda per $d$. Aleshores:

i) les boles tancades de $M$ són conjunts tancats.

ii) La intersecció arbitrària de tancats és un tancat.

iii) La unió finita de tancats és un tancat.

iv) $M$ i $\varnothing$ són conjunts tancats.

[T1.28] Lema 28 (Tema 1) — Tancat d'un compacte és compacte
Tot tancat d'un compacte és un compacte.
</solucio_de_referencia>

### Document a revisar

[1] Sigui $\{K_i\}_{i\in I}$ una família no buida ($I\neq\varnothing$) de compactes de $\mathbb{R}^n$ i $K=\bigcap_{i\in I}K_i$.
[2] Cada $K_i$ és compacte i, per tant, tancat, ja que tot compacte d'un espai mètric és tancat.
[3] La intersecció d'una família arbitrària de tancats és tancada: el seu complementari és $\bigcap_{i\in I}K_i^c$, una intersecció d'oberts, i tota intersecció d'oberts és oberta. Per tant $K$ és tancat.
[4] Fixem $i_0\in I$, que existeix perquè $I\neq\varnothing$. Aleshores $K\subseteq K_{i_0}$.
[5] Tot subconjunt d'un compacte és compacte. Com que $K\subseteq K_{i_0}$ i $K_{i_0}$ és compacte, $K$ és compacte.


## t1-15:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Demostreu que, donada una successió $(x_n)_{n\in\mathbb{N}}$ amb $\lim_{n\to\infty}x_n=x_0$, el conjunt $(x_n)_{n\in\mathbb{N}}\cup\{x_0\}$ és compacte.
RESULTAT CORRECTE: Sigui $K=\{x_n\mid n\in\mathbb{N}\}\cup\{x_0\}$ i $K\subseteq\bigcup_{i\in I}U_i$ un recobriment per oberts. Existeix $i_0$ amb $x_0\in U_{i_0}$ i $r>0$ amb $B_r(x_0)\subseteq U_{i_0}$. Per la convergència, existeix $n_0$ tal que $x_n\in B_r(x_0)\subseteq U_{i_0}$ per a tot $n\ge n_0$. Els termes $x_1,\dots,x_{n_0-1}$ són un nombre finit: cadascun és en algun $U_{i_n}$. Aleshores $K\subseteq U_{i_0}\cup U_{i_1}\cup\dots\cup U_{i_{n_0-1}}$, un subrecobriment finit, i $K$ és compacte.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [recobriment] Partir d'un recobriment arbitrari  (teoria: T1.24, T1.11)
     objectiu: Fixar un recobriment per oberts qualsevol del conjunt i veure què se'n pot dir a prop del punt límit $x_0$.
     idea: Per definició de compacte cal treballar amb un recobriment arbitrari. El punt $x_0$ és del conjunt, per tant és en algun obert del recobriment, i ser obert dona una bola al seu voltant.
     detall: Sigui $K=\{x_n\}_n\cup\{x_0\}\subseteq\bigcup_{i\in I}U_i$ amb $U_i$ oberts. Com que $x_0\in K$, existeix $i_0\in I$ amb $x_0\in U_{i_0}$, i com que $U_{i_0}$ és obert existeix $r>0$ tal que $B_r(x_0)\subseteq U_{i_0}$.
  2. [cua] Un sol obert conté la cua  (teoria: T1.18)
     objectiu: Veure que un únic obert del recobriment conté tots els termes de la successió a partir d'un cert índex.
     idea: Aplicar la definició de convergència amb una tolerància ben triada, relacionada amb la bola que tenim al voltant de $x_0$.
     detall: Prenent $\varepsilon=r$ a la definició de límit, existeix $n_0$ tal que $d(x_n,x_0)<r$ per a tot $n\ge n_0$, és a dir, $x_n\in B_r(x_0)\subseteq U_{i_0}$ per a tot $n\ge n_0$.
  3. [finits] Cobrir la resta i concloure  (teoria: T1.24)
     objectiu: Cobrir els punts del conjunt que encara no estan coberts i extreure'n un subrecobriment finit.
     idea: Els termes que queden fora de la cua són un nombre finit, i cadascun és en algun obert del recobriment.
     detall: Per a cada $n=1,\dots,n_0-1$ triem $i_n\in I$ amb $x_n\in U_{i_n}$. Aleshores $K\subseteq U_{i_0}\cup U_{i_1}\cup\dots\cup U_{i_{n_0-1}}$, que és un subrecobriment finit. Com que el recobriment era arbitrari, $K$ és compacte.
ERRORS COMUNS:
  - [recobriment_particular] Comprova la propietat només per a un recobriment concret (per exemple, boles centrades als punts del conjunt) en lloc d'un recobriment arbitrari.
  - [conjunt_finit] Argumenta com si el conjunt fos finit, o diu que "només hi ha un nombre finit de punts", quan en general la successió pren infinits valors.
  - [oblida_x0] Oblida incloure el punt límit $x_0$ o no l'aprofita: sense $x_0$ el conjunt no tindria per què ser compacte.
  - [heine_borel_sense_justificar] Aplica Heine-Borel (tancat i fitat) sense justificar que el conjunt és tancat, o en un espai mètric general on Heine-Borel no s'aplica.

TEORIA DEL CURS QUE FA SERVIR:
[T1.18] Definició 18 (Tema 1) — Successió convergent
Sigui $(M,d)$ un espai mètric. Direm que una successió $(x_n)_{n\in\mathbb{N}}$ és _convergent_ a $M$ si existeix $x\in M$ tal que $\forall\varepsilon>0,\exists n_0\in\mathbb{N}$ tal que $d(x_n,x)<\varepsilon$ $\forall n\geq n_0$. En aquest cas, diem que $x$ és el límit de la successió, i ho denotem per $x=\displaystyle\lim_{n\to\infty}x_n$ (el límit, si existeix, és únic).

[T1.24] Definició 24 (Tema 1) — Compacte i seqüencialment compacte
Sigui $(M,d)$ espai mètric, $A\subseteq M$.

i) $A$ és _compacte_ si tot recobriment per oberts de $A$ admet un subrecobriment finit, és a dir: si $A\subseteq\bigcup_{i\in I}U_i$, amb $U_i$ obert, aleshores existeixen $i_1,\ldots,i_k\in I$ tals que $A\subseteq\bigcup_{j=1}^k U_{i_j}$.

ii) $A$ és _seqüencialment compacte_ si tota successió $(x_n)_{n\in\mathbb{N}}\subseteq A$ admet una subsuccessió (una parcial) convergent a un punt de $A$.

[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.
</solucio_de_referencia>

### Document a revisar

[1] Recordem que $K$ és compacte si existeix algun recobriment de $K$ per oberts que admet un subrecobriment finit. Sigui $K=\{x_n\mid n\in\mathbb{N}\}\cup\{x_0\}$ i sigui $K\subseteq\bigcup_{i\in I}U_i$ un recobriment de $K$ per oberts $U_i$.
[2] Com que $x_0\in K$, existeix $i_0\in I$ amb $x_0\in U_{i_0}$. Com que $U_{i_0}$ és obert, existeix $r>0$ amb $B_r(x_0)\subseteq U_{i_0}$.
[3] Apliquem la definició de límit amb $\varepsilon=2r$: existeix $n_0$ tal que $d(x_n,x_0)<2r$ per a tot $n\geq n_0$, i per tant $x_n\in B_r(x_0)\subseteq U_{i_0}$ per a tot $n\geq n_0$.
[4] Els termes que queden fora d'aquesta cua, $x_1,\dots,x_{n_0-1}$, són un nombre finit. Per a cada $n=1,\dots,n_0-1$ triem $i_n\in I$ amb $x_n\in U_{i_n}$.
[5] Aleshores $K\subseteq U_{i_0}\cup U_{i_1}\cup\dots\cup U_{i_{n_0-1}}$: el punt $x_0$ i la cua són a $U_{i_0}$, i els termes restants als $U_{i_n}$. És un subrecobriment finit.
[6] Com que el recobriment de partida era arbitrari, $K$ és compacte.


## t1-16a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Doneu exemples de subconjunts $A,B\subseteq\mathbb{R}^n$, $A\neq B$, que satisfacin les condicions següents, o justifiqueu que no n'existeixen.

(a) $A\subseteq B$ però $Fr(B)\subseteq Fr(A)$.
RESULTAT CORRECTE: Existeixen. Per exemple, a $\mathbb{R}$: $A=(0,1)\cup(1,2)\subseteq B=(0,2)$, amb $Fr(B)=\{0,2\}\subseteq Fr(A)=\{0,1,2\}$ (fins i tot inclusió estricta). A $\mathbb{R}^n$: $B=B_1(\mathbf 0)$ i $A=B_1(\mathbf 0)\setminus\{\mathbf 0\}$, amb $Fr(B)=\{\|x\|=1\}\subsetneq Fr(A)=\{\|x\|=1\}\cup\{\mathbf 0\}$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [mecanisme] Com pot perdre frontera un conjunt més gran  (teoria: T1.14)
     objectiu: Entendre com pot ser que, en ampliar un conjunt, la frontera es faci més petita (o no creixi).
     idea: Pensa en "forats": si a un conjunt li treus un punt de l'interior, aquest punt passa a ser de frontera. Ampliar el conjunt omplint el forat elimina aquest punt de la frontera.
     detall: Si $B$ és obert i $p\in B$, el conjunt $A=B\setminus\{p\}\subseteq B$ té $p$ com a punt de frontera (tota bola centrada en $p$ conté $p\notin A$ i punts d'$A$), mentre que $p$ és interior a $B$ i, per tant, no és de $Fr(B)$.
  2. [exemple] Proposar un exemple concret
     objectiu: Escriure dos conjunts concrets $A\neq B$ amb $A\subseteq B$ que encaixin amb aquest mecanisme.
     idea: A $\mathbb{R}$ (és a dir, $n=1$) n'hi ha prou amb intervals: un interval obert i el mateix interval amb un punt interior tret.
     detall: $A=(0,1)\cup(1,2)$ i $B=(0,2)$ a $\mathbb{R}$. Clarament $A\subseteq B$ i $A\neq B$ ($1\in B\setminus A$).
  3. [verificar] Calcular les fronteres  (teoria: T1.14, T1.16)
     objectiu: Calcular $Fr(A)$ i $Fr(B)$ i comprovar la inclusió demanada.
     idea: Aplica la definició de punt frontera: tota bola centrada al punt talla el conjunt i el seu complementari. Mira els extrems dels intervals i el punt tret.
     detall: $Fr(B)=\{0,2\}$. Per a $A$: $0$ i $2$ són de frontera com abans, i $1$ també, perquè tota bola $(1-r,1+r)$ conté $1\notin A$ i punts d'$A$. Els altres punts són interiors a $A$ o exteriors. Per tant $Fr(A)=\{0,1,2\}\supseteq Fr(B)$.
ERRORS COMUNS:
  - [frontera_monotona] Creu que $A\subseteq B$ implica $Fr(A)\subseteq Fr(B)$ i, per tant, que no hi ha exemples.
  - [frontera_dins_conjunt] Confon la frontera amb "els punts del conjunt que estan a la vora", oblidant punts de frontera que no pertanyen al conjunt (com el punt tret).
  - [oblida_A_neq_B] Proposa $A=B$, cosa que l'enunciat exclou.

TEORIA DEL CURS QUE FA SERVIR:
[T1.16] Definició 16 (Tema 1) — Interior, derivat, frontera, clausura
Sigui $A\subseteq M$. Aleshores es defineixen:

i) _Interior_ d'$A$: $\mathring{A}=\{x\in A\mid x\text{ és interior a }A\}$. També s'acostuma a denotar per $\mathrm{int}(A)$.

ii) _Conjunt derivat_ d'$A$: $A'=\{x\in M\mid x\text{ és punt d'acumulació d'}A\}$.

iii) _Frontera_ d'$A$: $\mathrm{Fr}A=\{x\in M\mid x\text{ és de la frontera d'}A\}$. També és denota per $\partial A$.

iv) _Clausura_ o _adherència_ d'$A$: $\overline{A}=\{x\in M\mid\forall r>0\text{ es té que }B_r(x)\cap A\neq\varnothing\}$.
De manera equivalent, es pot definir de les dues maneres següents:
a) $\overline{A}=A\cup A'$; b) $\overline{A}$ és el conjunt tancat més petit que conté $A$.

v) _Exterior_ d'$A$: $\mathrm{ext}(A)=\mathrm{int}(A^c)$.

[T1.14] Definició 14 (Tema 1) — Tipus de punts d'un conjunt
Sigui $A\subseteq M$. Aleshores:

i) Un punt $x\in A$ és _interior_ a $A$ si existeix $r>0$ tal que $B_r(x)\subseteq A$.

ii) Un punt $x\in M$ és _d'acumulació_ d'$A$ si per a tot $r>0$ es té que $B_r(x)\cap(A\setminus\{x\})\neq\varnothing$.

iii) Un punt $x\in M$ és de la frontera d'$A$, si per a tot $r>0$ es té que $B_r(x)\cap A\neq\varnothing$ i també $B_r(x)\cap A^c\neq\varnothing$.

iv) Un punt $x\in M$ és _exterior_ d'$A$ si $x$ és interior a $A^c$ (és a dir, si existeix $r>0$ tal que $B_r(x)\subseteq A^c$).
</solucio_de_referencia>

### Document a revisar

[1] Sí que n'existeixen. La idea és que, si a un conjunt obert li traiem un punt interior, aquest punt passa a ser de frontera, de manera que el conjunt més petit pot tenir més frontera.
[2] Concretament, si $B$ és obert i $p\in B$, posem $A=B\setminus\{p\}\subseteq B$. Tota bola centrada en $p$ conté $p\notin A$ i punts d'$A$, així que $p\in Fr(A)$; en canvi, $p\in B$ i un punt d'un conjunt mai no pertany a la seva frontera, així que $p\notin Fr(B)$.
[3] Prenem a $\mathbb{R}$ els conjunts $A=(0,1)\cup(1,2)$ i $B=(0,2)$. Clarament $A\subseteq B$, i $A\neq B$ perquè $1\in B\setminus A$.
[4] $Fr(B)=\{0,2\}$: com que $0,2\notin B$, no són interiors a $B$ i, per tant, són de frontera; els punts de $(0,2)$ són interiors a $B$ i els de fora de $[0,2]$ són exteriors.
[5] Per a $A$: $0$ i $2$ en són punts de frontera com abans, i també $1$, perquè tota bola $(1-r,1+r)$ conté $1\notin A$ i punts d'$A$. Els altres punts són interiors o exteriors a $A$, així que $Fr(A)=\{0,1,2\}$.
[6] Per tant $Fr(B)=\{0,2\}\subseteq\{0,1,2\}=Fr(A)$, amb $A\subseteq B$ i $A\neq B$: l'exemple compleix totes les condicions.


## t1-17b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui
$$A=\left\{\left(\cos\frac{1}{t}+2t\sin\frac{1}{t},\ 2t\cos\frac{1}{t}-\sin\frac{1}{t}\right)\in\mathbb{R}^2\ \middle|\ t\in\mathbb{R}\setminus\{0\}\right\}.$$

(b) Què podeu dir sobre l'existència de punts d'acumulació del conjunt $A$ sobre la circumferència unitat $C=\{(x,y)\in\mathbb{R}^2\mid x^2+y^2=1\}$ ?
RESULTAT CORRECTE: Tot punt de $C$ és punt d'acumulació d'$A$, és a dir, $C\subseteq A'$. Per a $p=(\cos\theta,\sin\theta)$, la successió $t_k=\frac{1}{2\pi k-\theta}\to 0$ dona punts $\mathbf a(t_k)=p+2t_k(-\sin\theta,\cos\theta)\in A$, diferents de $p$ i amb $\|\mathbf a(t_k)-p\|=2t_k\to 0$. A més, per (a), cap d'aquests punts d'acumulació pertany a $A$ ($A\cap C=\varnothing$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [descomposicio] Comportament quan $t\to 0$
     objectiu: Entendre on van els punts d'$A$ quan el paràmetre $t$ és petit.
     idea: Separa cada punt en una part que no depèn del factor $2t$ i una altra que sí. Usa també la norma de l'apartat (a), que es pot donar per coneguda.
     detall: $\mathbf a(t)=\left(\cos\frac1t,-\sin\frac1t\right)+2t\left(\sin\frac1t,\cos\frac1t\right)$. El primer sumand és a $C$ i el segon té norma $2|t|\to 0$: quan $t\to 0$ els punts d'$A$ s'apropen a $C$ girant-hi al voltant infinites vegades.
  2. [successio] Successió que s'acosta a un punt de $C$  (teoria: T1.19, T1.18)
     objectiu: Donat un punt $p=(\cos\theta,\sin\theta)$ de $C$, construir una successió de punts d'$A$, diferents de $p$, que hi convergeixi.
     idea: Tria valors del paràmetre que tendeixin a $0$ i per als quals la part sobre $C$ sigui exactament $p$; després usa la caracterització de punt d'acumulació per successions.
     detall: Cal $\cos\frac1t=\cos\theta$ i $-\sin\frac1t=\sin\theta$, és a dir, $\frac1t=-\theta+2\pi k$. Prenem $t_k=\frac{1}{2\pi k-\theta}$, positiu per a $k$ gran i amb $t_k\to 0$. Aleshores $\mathbf a(t_k)=p+2t_k(-\sin\theta,\cos\theta)$, amb $\|\mathbf a(t_k)-p\|=2t_k$, que és $>0$ i tendeix a $0$. Per la Proposició 19(i), $p\in A'$.
  3. [conclusio] Concloure  (teoria: T1.16)
     objectiu: Resumir què passa amb els punts d'acumulació d'$A$ sobre $C$ i si pertanyen a $A$.
     idea: El punt $p$ era arbitrari. Per a la pertinença, recorda la norma dels punts d'$A$.
     detall: Com que $p\in C$ era qualsevol, $C\subseteq A'$. Per (a), $\|\mathbf a\|>1$ per a tot $\mathbf a\in A$, així que $A\cap C=\varnothing$: els punts de $C$ són d'acumulació però no pertanyen a $A$ (en particular, $A$ no és tancat).
ERRORS COMUNS:
  - [nomes_existencia] Només troba un punt d'acumulació (per exemple $(1,0)$) i no veu que tots els punts de $C$ ho són.
  - [punt_igual] No comprova que els punts de la successió són diferents del punt límit, o confon punt d'acumulació amb punt adherent.
  - [pertinenca] Afirma que els punts de $C$ són d'$A$ (punts d'acumulació "dins" del conjunt).

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

[T1.19] Proposició 19 (Tema 1) — Caracterització amb successions
Sigui $(M,d)$ un espai mètric, $A\subseteq M$ i $x\in M$. Aleshores:

i) $x$ és un punt d'acumulació d'$A\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\neq x$, $a_n\in A$, tal que $x=\lim_n a_n$.

ii) $x\in\overline{A}\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\in A$ tal que $x=\lim_n a_n$.

iii) $A$ és tancat $\Leftrightarrow$ el límit de tota successió convergent d'elements d'$A$ és d'$A$.

[T1.18] Definició 18 (Tema 1) — Successió convergent
Sigui $(M,d)$ un espai mètric. Direm que una successió $(x_n)_{n\in\mathbb{N}}$ és _convergent_ a $M$ si existeix $x\in M$ tal que $\forall\varepsilon>0,\exists n_0\in\mathbb{N}$ tal que $d(x_n,x)<\varepsilon$ $\forall n\geq n_0$. En aquest cas, diem que $x$ és el límit de la successió, i ho denotem per $x=\displaystyle\lim_{n\to\infty}x_n$ (el límit, si existeix, és únic).
</solucio_de_referencia>

### Document a revisar

[1] Escrivim $\mathbf a(t)=\left(\cos\frac1t,-\sin\frac1t\right)+2t\left(\sin\frac1t,\cos\frac1t\right)$. El primer sumand és un punt de $C$ i el segon té norma $2|t|$, que tendeix a $0$ quan $t\to0$.
[2] Per tant, quan $t\to 0$ els punts d'$A$ s'acosten a $C$ donant-hi infinites voltes, i esperem que tot punt de $C$ sigui d'acumulació. Sigui $p=(\cos\theta,\sin\theta)$ un punt qualsevol de $C$.
[3] Volem $t$ amb $\cos\frac1t=\cos\theta$ i $-\sin\frac1t=\sin\theta$, és a dir, $\frac1t=-\theta+2\pi k$ amb $k\in\mathbb{Z}$. Prenem $t_k=\frac{1}{2\pi k-\theta}$, que és positiu per a $k$ prou gran i tendeix a $0$.
[4] Per a aquests $k$, $\mathbf a(t_k)=p+2t_k(\sin\theta,\cos\theta)$, i com que $t_k>0$, $\|\mathbf a(t_k)-p\|=2t_k$.
[5] Com que $2t_k\to 0$, la successió $\mathbf a(t_k)$ de punts d'$A$ convergeix a $p$; per tant $p$ és adherent a $A$ i, com que tot punt adherent a un conjunt n'és d'acumulació, $p\in A'$.
[6] Com que $p\in C$ era arbitrari, $C\subseteq A'$: tots els punts de la circumferència són punts d'acumulació d'$A$.
[7] A més, per l'apartat (a), $\|\mathbf a\|=\sqrt{1+4t^2}>1$ per a tot $\mathbf a\in A$, així que $A\cap C=\varnothing$: aquests punts d'acumulació no pertanyen a $A$ (en particular, $A$ no és tancat).


## t1-18b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem $A,B\subseteq\mathbb{R}^n$ i $V=A\cap B$.

(b) Doneu un contraexemple que provi la falsedat de $\overline{V}=\overline{A}\cap\overline{B}$.
RESULTAT CORRECTE: Per exemple, a $\mathbb{R}$: $A=(0,1)$, $B=(1,2)$. Llavors $V=A\cap B=\varnothing$ i $\overline V=\varnothing$, mentre que $\overline A\cap\overline B=[0,1]\cap[1,2]=\{1\}\neq\overline V$. (Sempre es té $\overline V\subseteq\overline A\cap\overline B$; la inclusió que falla és l'altra.) Altres: $A=\mathbb{Q}$, $B=\mathbb{R}\setminus\mathbb{Q}$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [inclusio_certa] Quina inclusió sempre és certa  (teoria: T1.16)
     objectiu: Esbrinar quina de les dues inclusions es compleix sempre, per saber quina ha de fallar al contraexemple.
     idea: Si un conjunt està contingut en un altre, què passa amb les seves clausures? Aplica-ho a $V\subseteq A$ i $V\subseteq B$ amb la definició de clausura.
     detall: Si $x\in\overline V$, tota bola centrada en $x$ talla $V\subseteq A$, per tant talla $A$; igual amb $B$. Així $\overline V\subseteq\overline A\cap\overline B$ sempre. El contraexemple ha de tenir un punt de $\overline A\cap\overline B$ que no sigui de $\overline V$.
  2. [contraexemple] Triar els conjunts
     objectiu: Trobar $A$ i $B$ amb intersecció molt petita però amb clausures que es tallin.
     idea: Pensa en dos conjunts disjunts que "es toquin" en un punt que no pertany a cap dels dos.
     detall: A $\mathbb{R}$: $A=(0,1)$ i $B=(1,2)$, disjunts però amb el punt $1$ a la vora de tots dos.
  3. [verificar] Comprovar el contraexemple  (teoria: T1.16)
     objectiu: Calcular $\overline V$ i $\overline A\cap\overline B$ per al teu exemple i veure que són diferents.
     idea: La clausura d'un interval obert afegeix els extrems.
     detall: $V=\varnothing$, així que $\overline V=\varnothing$. En canvi $\overline A=[0,1]$, $\overline B=[1,2]$ i $\overline A\cap\overline B=\{1\}\neq\varnothing$.
ERRORS COMUNS:
  - [inclusio_equivocada] Busca un exemple on $\overline A\cap\overline B$ sigui més petit que $\overline V$, cosa impossible.
  - [conjunts_tancats] Prova amb conjunts tancats (o massa "grans"), per als quals no es pot trobar el contraexemple tan fàcilment.
  - [clausura_interval] Calcula malament la clausura d'un interval obert (no hi afegeix els extrems).

TEORIA DEL CURS QUE FA SERVIR:
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
</solucio_de_referencia>

### Document a revisar

[1] Primer vegem quina inclusió és sempre certa. Si $x\in\overline V$, tota bola centrada en $x$ talla $V$; com que $A\subseteq V$, també talla $A$, i igualment talla $B$. Així $\overline V\subseteq\overline A\cap\overline B$ sempre.
[2] Per tant, un contraexemple ha de tenir un punt de $\overline V$ que no sigui de $\overline A\cap\overline B$. Busquem dos conjunts disjunts que es toquin en un punt que no pertanyi a cap dels dos.
[3] A $\mathbb{R}$ prenem $A=(0,1)$ i $B=(1,2)$. Aleshores $V=A\cap B=\varnothing$, i per tant $\overline V=\varnothing$.
[4] D'altra banda, $\overline A=[0,1]$: $A\subseteq\overline A$, tota bola centrada en $0$ o en $1$ talla $(0,1)$, i cada punt de fora de $[0,1]$ té una bola que no talla $(0,1)$. Anàlogament $\overline B=[1,2]$.
[5] Així $\overline A\cap\overline B=[0,1]\cap[1,2]=\{1\}\neq\varnothing=\overline V$, i la igualtat $\overline V=\overline A\cap\overline B$ és falsa en general.


## t1-19c:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considereu els conjunts i aplicacions següents:

(c) $(\{0,1\}^{\mathbb{N}},d)$, $d(a,b)=\begin{cases}0 & a=b\\ 1/\min\{k\in\mathbb{N}\mid a_k\neq b_k\} & a\neq b.\end{cases}$

Indicació: Digueu quins són espais mètrics i quins no, demostrant les propietats de la distància si és el cas o proporcionant contraexemples en cas contrari. En els casos que siguin espai mètric, descriviu la bola oberta $B(\mathbf{0},\epsilon)$, per a $\epsilon>0$.
RESULTAT CORRECTE: Sí que és un espai mètric (de fet, $d(a,b)\le\max\{d(a,c),d(c,b)\}$). Si $\mathbf 0$ és la successió nul·la i $N=\lfloor 1/\epsilon\rfloor$:
$B(\mathbf 0,\epsilon)=\{b\in\{0,1\}^{\mathbb{N}}\mid b_k=0\ \text{per a tot}\ k\le 1/\epsilon\}=\{b\mid b_1=\dots=b_N=0\}$. Si $\epsilon>1$ ($N=0$), la bola és tot l'espai.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [positivitat_simetria] Positivitat i simetria  (teoria: T1.5)
     objectiu: Comprovar que $d$ està ben definida i les propietats (i) i (ii) de distància.
     idea: Si $a\neq b$ el conjunt d'índexs on difereixen és no buit; tot subconjunt no buit de $\mathbb{N}$ té mínim. La condició "$a_k\neq b_k$" és simètrica en $a$ i $b$.
     detall: Si $a\neq b$, $k(a,b)=\min\{k\mid a_k\neq b_k\}$ existeix (bon ordre de $\mathbb{N}$) i $d(a,b)=1/k(a,b)>0$; si $a=b$, $d=0$. Per tant $d\ge 0$ i $d(a,b)=0\iff a=b$. A més $k(a,b)=k(b,a)$, d'on $d(a,b)=d(b,a)$.
  2. [triangular] Desigualtat triangular  (teoria: T1.5)
     objectiu: Demostrar $d(a,b)\le d(a,c)+d(c,b)$.
     idea: Compara el primer índex on difereixen $a$ i $b$ amb els primers índexs on difereixen $a,c$ i $c,b$: si dues successions coincideixen fins a un cert punt amb una tercera, coincideixen entre elles fins al menor dels dos punts.
     detall: Si dos dels tres punts coincideixen és immediat. Si no, $a_j=c_j$ per a $j<k(a,c)$ i $c_j=b_j$ per a $j<k(c,b)$, així que $a_j=b_j$ per a $j<\min\{k(a,c),k(c,b)\}$, i $k(a,b)\ge\min\{k(a,c),k(c,b)\}$. Per tant $d(a,b)\le\max\{d(a,c),d(c,b)\}\le d(a,c)+d(c,b)$.
  3. [bola] Descriure la bola  (teoria: T1.11)
     objectiu: Descriure la bola oberta $B(\mathbf 0,\epsilon)$ centrada a la successió nul·la.
     idea: Tradueix $d(\mathbf 0,b)<\epsilon$ a una condició sobre el primer índex on $b$ no és zero.
     detall: $d(\mathbf 0,b)<\epsilon\iff b=\mathbf 0$ o $k(\mathbf 0,b)>1/\epsilon\iff b_k=0$ per a tot $k\le 1/\epsilon$. Amb $N=\lfloor 1/\epsilon\rfloor$: $B(\mathbf 0,\epsilon)=\{b\mid b_1=\dots=b_N=0\}$, les successions que comencen amb $N$ zeros. Si $\epsilon>1$, no hi ha cap condició i la bola és tot l'espai.
ERRORS COMUNS:
  - [desigualtat_invertida] Confon el sentit: com més tard difereixen dues successions, pensa que més lluny són.
  - [bola_frontera] Descriu la bola amb una condició incorrecta en el límit (per exemple $k<1/\epsilon$ en lloc de $k\le 1/\epsilon$), o oblida el cas $\epsilon>1$.
  - [triangular_sense_cas] A la desigualtat triangular no tracta el cas en què alguns dels punts coincideixen, on $k$ no està definit.

TEORIA DEL CURS QUE FA SERVIR:
[T1.5] Definició 5 (Tema 1) — Distància
Sigui $M$ un conjunt. Una funció $d(\cdot,\cdot):M\times M\longrightarrow\mathbb{R}$ es diu que és una _distància_ si per a tot $x,y,z\in M$, es compleixen:

i) $d(x,y)\geq 0$; $d(x,y)=0\iff x=y$.

ii) $d(x,y)=d(y,x)$ (simètrica).

iii) $d(x,y)\leq d(x,z)+d(z,y)$ (desigualtat triangular).

Direm en aquest cas que $(M,d)$ és un _espai mètric_.

[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.
</solucio_de_referencia>

### Document a revisar

[1] Prenem $\mathbb{N}=\{1,2,\dots\}$. Si $a\neq b$, el conjunt $\{k\mid a_k\neq b_k\}$ és un subconjunt no buit de $\mathbb{N}$ i té mínim, que denotem $k(a,b)$; així $d(a,b)=1/k(a,b)$ està ben definida.
[2] Si $a\neq b$, $d(a,b)=1/k(a,b)>0$, i si $a=b$, $d(a,b)=0$; per tant $d\geq 0$ i $d(a,b)=0\iff a=b$. A més $a_k\neq b_k\iff b_k\neq a_k$, així que $k(a,b)=k(b,a)$ i $d(a,b)=d(b,a)$.
[3] Desigualtat triangular: si dos dels tres punts $a,b,c$ coincideixen, és immediata. Altrament, $a_j=c_j$ per a $j<k(a,c)$ i $c_j=b_j$ per a $j<k(c,b)$, d'on $a_j=b_j$ per a tot $j<\min\{k(a,c),k(c,b)\}$.
[4] Per tant $k(a,b)\geq\min\{k(a,c),k(c,b)\}$ i, prenent inversos, $d(a,b)\leq\min\{d(a,c),d(c,b)\}$, que és $\leq d(a,c)+d(c,b)$. Així $d$ és una distància i $(\{0,1\}^{\mathbb{N}},d)$ és un espai mètric.
[5] Bola: sigui $\mathbf 0$ la successió nul·la i $\epsilon>0$. Per a $b\neq\mathbf 0$, $d(\mathbf 0,b)<\epsilon\iff 1/k(\mathbf 0,b)<\epsilon\iff k(\mathbf 0,b)>1/\epsilon$, és a dir, el primer índex on $b$ val $1$ és més gran que $1/\epsilon$.
[6] Equivalentment, $b_k=0$ per a tot $k<1/\epsilon$: la bola $B(\mathbf 0,\epsilon)$ està formada per $\mathbf 0$ i les successions que s'anul·len en tots aquests índexs.
[7] En particular, si $\epsilon>1$, aleshores $1/\epsilon<1$ i no hi ha cap condició: la bola és tot l'espai $\{0,1\}^{\mathbb{N}}$.


## t1-20a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Siguin $A,B\subseteq\mathbb{R}$ i $E=\{xy\in\mathbb{R}\mid x\in A,\ y\in B\}$. Demostreu:

(a) $A$ obert i $B\subseteq(0,+\infty)\Rightarrow E$ obert.
RESULTAT CORRECTE: $E=\bigcup_{y\in B}yA$, amb $yA=\{xy\mid x\in A\}$. Per a $y>0$, si $(a-r,a+r)\subseteq A$ aleshores $(ya-yr,ya+yr)=y(a-r,a+r)\subseteq yA$, de manera que $yA$ és obert. La unió arbitrària d'oberts és oberta, per tant $E$ és obert (si $B=\varnothing$, $E=\varnothing$, també obert).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [descomposar] Escriure $E$ com una unió
     objectiu: Expressar $E$ en termes de conjunts més senzills, fixant un dels dos factors.
     idea: Fixa $y\in B$ i mira quins productes s'obtenen variant $x\in A$.
     detall: $E=\bigcup_{y\in B}yA$, on $yA=\{xy\mid x\in A\}$.
  2. [dilatacio_oberta] Cada dilatació és oberta  (teoria: T1.11)
     objectiu: Veure que $yA$ és obert per a cada $y>0$.
     idea: Multiplicar per $y>0$ multiplica les distàncies per $y$: una bola de radi $r$ al voltant de $a$ es transforma en una bola de radi proporcional al voltant de $ya$.
     detall: Sigui $z=ya\in yA$ amb $a\in A$; com que $A$ és obert, existeix $r>0$ amb $(a-r,a+r)\subseteq A$. Si $|w-ya|<yr$, aleshores $w=y\cdot\frac wy$ amb $\left|\frac wy-a\right|<r$, és a dir, $\frac wy\in A$ i $w\in yA$. Així $(ya-yr,ya+yr)\subseteq yA$ (cal $y>0$ perquè el radi $yr$ sigui positiu).
  3. [unio] Concloure  (teoria: T1.12)
     objectiu: Concloure que $E$ és obert.
     idea: Propietats dels oberts respecte de les unions.
     detall: $E$ és unió (arbitrària) dels oberts $yA$, $y\in B$, i per tant és obert. Si $B=\varnothing$, $E=\varnothing$, que també és obert.
ERRORS COMUNS:
  - [producte_intervals] Suposa que $A$ és un interval obert, o que $B$ és obert, i raona només en aquest cas.
  - [radi_mal_escalat] Usa el mateix radi $r$ per a la bola al voltant de $ya$, sense escalar-lo per $y$.
  - [un_sol_factor] Intenta trobar una bola al voltant de $xy$ movent $x$ i $y$ alhora, i s'embolica amb una fita conjunta.

TEORIA DEL CURS QUE FA SERVIR:
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
</solucio_de_referencia>

### Document a revisar

[1] Per a cada $y\in B$ posem $yA=\{xy\mid x\in A\}$. Aleshores $E=\bigcup_{y\in B}yA$: cada producte $xy$ amb $x\in A$, $y\in B$ és de $yA$, i cada $yA$ amb $y\in B$ està contingut a $E$.
[2] Vegem que $yA$ és obert per a cada $y\in B$; per hipòtesi, $y>0$. Sigui $z=ya\in yA$ amb $a\in A$; com que $A$ és obert, existeix $r>0$ amb $(a-r,a+r)\subseteq A$.
[3] Afirmem que $(ya-r,ya+r)\subseteq yA$. Sigui $w$ amb $|w-ya|<r$. Aleshores $\left|\frac wy-a\right|=\frac{|w-ya|}{y}<r$, de manera que $\frac wy\in A$ i $w=y\cdot\frac wy\in yA$.
[4] Així $yA$ conté un interval obert centrat en cadascun dels seus punts, i per tant és obert.
[5] $E$ és la unió (arbitrària) dels oberts $yA$, $y\in B$, i la unió arbitrària d'oberts és oberta: $E$ és obert. Si $B=\varnothing$, aleshores $E=\mathbb{R}$, que també és obert.

## t1-4c:facil

### Referència

<solucio_de_referencia>
ENUNCIAT: Si $\|\cdot\|$ és la norma ordinària i $\langle\cdot,\cdot\rangle$ és el producte escalar ordinari a $\mathbb{R}^n$, proveu:

(c) $\|x+y\|\,\|x-y\|\leqslant\|x\|^2+\|y\|^2$.
RESULTAT CORRECTE: Per la llei del paral·lelogram, $\|x+y\|^2+\|x-y\|^2=2\|x\|^2+2\|y\|^2$, i per a reals $a,b$ es té $ab\leq\frac{a^2+b^2}{2}$ (de $(a-b)^2\geq 0$). Amb $a=\|x+y\|$, $b=\|x-y\|$: $\|x+y\|\,\|x-y\|\leq\frac{\|x+y\|^2+\|x-y\|^2}{2}=\|x\|^2+\|y\|^2$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [paralelogram] Llei del paral·lelogram  (teoria: T1.1, T1.8)
     objectiu: Calcular $\|x+y\|^2+\|x-y\|^2$ en termes de $\|x\|$ i $\|y\|$.
     idea: Desenvolupar els dos quadrats com a productes escalars (com a l'apartat (a)) i ara sumar-los en lloc de restar-los.
     detall: $\|x\pm y\|^2=\|x\|^2\pm2\langle x,y\rangle+\|y\|^2$; sumant, els termes creuats es cancel·len: $\|x+y\|^2+\|x-y\|^2=2\|x\|^2+2\|y\|^2$.
  2. [desigualtat_producte] Fitar un producte per quadrats
     objectiu: Fitar el producte $ab$ de dos nombres reals en termes de $a^2$ i $b^2$.
     idea: Partir d'un quadrat, que sempre és no negatiu, i desenvolupar-lo.
     detall: $0\leq(a-b)^2=a^2-2ab+b^2$, per tant $ab\leq\frac{a^2+b^2}{2}$.
  3. [combinar] Combinar
     objectiu: Obtenir la desigualtat de l'enunciat a partir dels dos passos anteriors.
     idea: Aplicar la fita del producte a dos nombres ben triats i substituir la suma de quadrats.
     detall: Amb $a=\|x+y\|$, $b=\|x-y\|$: $\|x+y\|\,\|x-y\|\leq\frac{\|x+y\|^2+\|x-y\|^2}{2}=\frac{2\|x\|^2+2\|y\|^2}{2}=\|x\|^2+\|y\|^2$.
ERRORS COMUNS:
  - [cauchy_schwarz_sentit] Intenta usar Cauchy-Schwarz amb $\langle x+y,x-y\rangle=\|x\|^2-\|y\|^2$, però Cauchy-Schwarz dona $|\langle x+y,x-y\rangle|\leq\|x+y\|\,\|x-y\|$, una fita inferior del producte, no superior.
  - [triangular_massa_grossa] Fita cada factor per la desigualtat triangular, $\|x\pm y\|\leq\|x\|+\|y\|$, i obté $(\|x\|+\|y\|)^2$, que és més gran que $\|x\|^2+\|y\|^2$ i no serveix.
  - [norma_quadrat_producte] Escriu $\|x+y\|\,\|x-y\|=\|x\|^2-\|y\|^2$ confonent el producte de normes amb el producte escalar.

TEORIA DEL CURS QUE FA SERVIR:
[T1.8] Exemple 8 (Tema 1) — Norma i distància en exemples
a) A $\mathbb{R}^2$, definim $\langle(a,b),(c,d)\rangle=ac+bd$. Llavors,

$$\begin{aligned}\|(a,b)\|&=\sqrt{\langle(a,b),(a,b)\rangle}=\sqrt{a^2+b^2},\\d((a,b),(c,d))&=\|(a,b)-(c,d)\|=\|(a-c,b-d)\|\\&=\sqrt{\langle(a-c,b-d),(a-c,b-d)\rangle}=\sqrt{(a-c)^2+(b-d)^2}\quad\text{(Pitàgores).}\end{aligned}$$

b) A $\mathbb{R}^3$, $\|(a,b,c)\|=\sqrt{a^2+b^2+c^2}$ i, en general, a $\mathbb{R}^n$:

$$\begin{aligned}\langle(a_1,a_2,\ldots,a_n),(b_1,b_2,\ldots,b_n)\rangle&:=\sum_{i=1}^n a_i\cdot b_i;\\\|(a_1,a_2,\ldots,a_n)\|&=\sqrt{\sum_{i=1}^n a_i^2};\\d((a_1,a_2,\ldots,a_n),(b_1,b_2,\ldots,b_n))&=\sqrt{\sum_{i=1}^n(a_i-b_i)^2}.\end{aligned}$$

c) $E=\mathcal{C}([a,b])$. Aleshores:

$$\begin{aligned}\langle f,g\rangle&:=\int_a^b f(x)g(x)\,dx;\\\|f\|&=\sqrt{\int_a^b f^2(x)\,dx};\\d(f,g)=\|f-g\|&=\sqrt{\int_a^b(f(x)-g(x))^2dx}\quad\text{("àrea" entre }y=f(x)\text{ i }y=g(x)\text{).}\end{aligned}$$

d) $E=\mathcal{B}(A)=$ conjunt de funcions $f:A\to\mathbb{R}$ fitades (inferiorment i superior), amb $A$ conjunt arbitrari. Aleshores, $d(f,g)=\displaystyle\sup_{t\in A}|f(t)-g(t)|$ és una distància.

[T1.1] Definició 1 (Tema 1) — Producte escalar
Una funció $\langle\cdot,\cdot\rangle: E\times E\longrightarrow\mathbb{R}$ es diu que és un _producte escalar_ si compleix; $\forall u,u_j,v\in E$:

i) $\langle u,u\rangle\geq 0$; $\langle u,u\rangle=0\iff u=0$.

ii) $\langle u,v\rangle=\langle v,u\rangle$ (simètric).

iii) $\langle\lambda u,v\rangle=\lambda\langle u,v\rangle$, $\forall\lambda\in\mathbb{R}$ (i, per tant, $\langle u,\lambda v\rangle=\lambda\langle u,v\rangle$).

iv) $\langle u_1+u_2,v\rangle=\langle u_1,v\rangle+\langle u_2,v\rangle$ (ídem respecte a la segona component).

En aquest cas es diu que $(E,\langle\cdot,\cdot\rangle)$ és un _espai euclidià_.
</solucio_de_referencia>

### Document a revisar

[1] Volem provar $\|x+y\|\,\|x-y\|\leq\|x\|^2+\|y\|^2$. Primer desenvolupem els quadrats amb el producte escalar: $\|x\pm y\|^2=\langle x\pm y,x\pm y\rangle=\|x\|^2\pm\langle x,y\rangle+\|y\|^2$.
[2] Sumant les dues expressions, els termes creuats es cancel·len i obtenim la llei del paral·lelogram: $\|x+y\|^2+\|x-y\|^2=2\|x\|^2+2\|y\|^2$.
[3] D'altra banda, per a nombres reals $a,b$ qualssevol tenim $0\leq(a-b)^2=a^2-2ab+b^2$, d'on $ab\leq\frac{a^2+b^2}{2}$.
[4] Ho apliquem a $a=\|x+y\|$ i $b=\|x-y\|$: $\|x+y\|\,\|x-y\|\leq\frac{\|x+y\|^2+\|x-y\|^2}{2}$.
[5] Substituint-hi la llei del paral·lelogram, $\|x+y\|\,\|x-y\|\leq\frac{2\|x\|^2+2\|y\|^2}{2}=\|x\|^2+\|y\|^2$, que és la desigualtat que volíem.


## t1-6:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Donat $A\subset\mathbb{R}^m$, sigui $D_A=\{d(x,y)\mid x,y\in A\}\subset\mathbb{R}$. Proveu que aquest conjunt és fitat si, i només si, $A$ ho és. Aleshores, es defineix _diàmetre_ de $A$ per $\mathrm{diam}(A)=\sup D_A$. Siguin ara $B_1=\{x\in\mathbb{R}^m\mid\sum_{i=1}^{m}|x_i|<1\}$, $B_2=\{x\in\mathbb{R}^m\mid\|x\|<1\}$, i $B_3=\{x\in\mathbb{R}^m\mid\max|x_i|<1\}$. Calculeu el diàmetre de $B_1$, $B_2$ i $B_3$.

Indicació: dibuixeu aquests conjunts en $\mathbb{R}^2$ i $\mathbb{R}^3$.
RESULTAT CORRECTE: (Amb $d$ la distància euclidiana i $A\neq\emptyset$.) $D_A$ és fitat $\iff$ $A$ és fitat: si $A\subseteq B_L(p)$, aleshores $d(x,y)\leq d(x,p)+d(p,y)<2L$; si $d(x,y)\leq K$ per a tots $x,y\in A$, fixat $a_0\in A$ es té $A\subseteq B_{K+1}(a_0)$.
Diàmetres: $\mathrm{diam}(B_1)=2$, $\mathrm{diam}(B_2)=2$, $\mathrm{diam}(B_3)=2\sqrt m$ (cap dels tres suprems no s'assoleix, perquè els conjunts són oberts).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [fitat_implica] $A$ fitat $\Rightarrow$ $D_A$ fitat  (teoria: T1.33, T1.11, T1.5)
     objectiu: Suposant que $A$ és fitat, trobar una fita superior per a totes les distàncies $d(x,y)$ amb $x,y\in A$.
     idea: Usar la definició de conjunt fitat (contingut en una bola) i la desigualtat triangular passant pel centre de la bola. Recordar que $D_A\subset[0,\infty)$, així que només cal fitar-lo per dalt.
     detall: Si $A\subseteq B_L(p)$, per a $x,y\in A$: $0\leq d(x,y)\leq d(x,p)+d(p,y)<2L$. Per tant $D_A\subseteq[0,2L]$ és fitat.
  2. [reciproc] $D_A$ fitat $\Rightarrow$ $A$ fitat  (teoria: T1.33, T1.11)
     objectiu: Suposant que totes les distàncies entre punts d'$A$ són $\leq K$, trobar una bola que contingui $A$.
     idea: Si $A$ és no buit, fixar un punt d'$A$ com a centre i escollir un radi adequat (cal desigualtat estricta a la definició de bola oberta).
     detall: Fixem $a_0\in A$. Per a tot $x\in A$, $d(x,a_0)\leq K<K+1$, així que $A\subseteq B_{K+1}(a_0)$. (Si $A=\emptyset$, tant $A$ com $D_A=\emptyset$ són trivialment fitats.)
  3. [diam_B2] Diàmetre de $B_2$  (teoria: T1.5)
     objectiu: Calcular $\mathrm{diam}(B_2)$: trobar una fita superior de $d(x,y)$ per a $x,y\in B_2$ i veure que és la més petita possible.
     idea: Fita: desigualtat triangular passant per l'origen. Optimalitat: prendre parelles de punts diametralment oposats sobre un eix, cada cop més a prop de la vora.
     detall: Per a $x,y\in B_2$: $\|x-y\|\leq\|x\|+\|y\|<2$. Amb $x_t=te_1$, $y_t=-te_1$, $0<t<1$: $\|x_t-y_t\|=2t\to 2$ quan $t\to 1^-$. Per tant el suprem és $2$ (no assolit).
  4. [diam_B1] Diàmetre de $B_1$  (teoria: T1.5)
     objectiu: Calcular $\mathrm{diam}(B_1)$ amb la distància euclidiana.
     idea: Comparar la norma euclidiana amb la suma dels valors absoluts de les components per obtenir una fita, i buscar punts de $B_1$ que la gairebé assoleixin.
     detall: Per a $v\in\mathbb{R}^m$, $\|v\|^2=\sum_i v_i^2\leq\left(\sum_i|v_i|\right)^2$, és a dir $\|v\|\leq\sum_i|v_i|$. Per a $x,y\in B_1$: $\|x-y\|\leq\sum_i|x_i-y_i|\leq\sum_i|x_i|+\sum_i|y_i|<2$. Els punts $\pm te_1$ ($0<t<1$) són a $B_1$ i són a distància $2t\to 2$. Per tant el suprem és $2$.
  5. [diam_B3] Diàmetre de $B_3$  (teoria: T1.5)
     objectiu: Calcular $\mathrm{diam}(B_3)$ amb la distància euclidiana.
     idea: Fitar cada component de $x-y$ i sumar els quadrats; per a l'optimalitat, pensar en vèrtexs oposats del cub (la diagonal).
     detall: Per a $x,y\in B_3$: $|x_i-y_i|\leq|x_i|+|y_i|<2$ per a cada $i$, d'on $\|x-y\|^2=\sum_{i=1}^m(x_i-y_i)^2<4m$ i $\|x-y\|<2\sqrt m$. Amb $x_t=t(1,\dots,1)$, $y_t=-x_t$, $0<t<1$: $\|x_t-y_t\|=2t\sqrt m\to 2\sqrt m$. Per tant el suprem és $2\sqrt m$.
ERRORS COMUNS:
  - [fita_sense_optimalitat] Troba una fita superior de $D_B$ i la dona com a diàmetre sense comprovar que és la més petita (que hi ha parelles de punts amb distància tan a prop com es vulgui de la fita).
  - [maxim_assolit] Pren punts de la vora (per exemple $\pm e_1$ o els vèrtexs del cub) com si fossin del conjunt, sense notar que els conjunts són oberts i el suprem no s'assoleix.
  - [distancia_equivocada] Calcula cada diàmetre amb la distància "pròpia" del conjunt ($d_1$ per a $B_1$, $d_\infty$ per a $B_3$) en lloc de la distància euclidiana, o barreja distàncies.
  - [fitat_sense_bola] Al recíproc, afirma que $A$ és fitat "perquè les distàncies ho són" sense exhibir cap bola que contingui $A$ (o pren com a centre un punt que no està ben definit).

TEORIA DEL CURS QUE FA SERVIR:
[T1.33] Definició 33 (Tema 1) — Conjunt fitat
Es diu que $A\subseteq M$ és _fitat_ si i només si existeix un $x\in M$ i un valor $L>0$ tal que $A\subseteq B_L(x)$.

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

[1] Treballem amb la distància euclidiana i $A\neq\emptyset$ (si $A=\emptyset$, $D_A=\emptyset$ i tots dos són trivialment fitats). Si $A$ és fitat, $A\subseteq B_L(p)$ per a algun $p$ i algun $L>0$, i per a $x,y\in A$: $0\leq d(x,y)\leq d(x,p)+d(p,y)<2L$. Per tant $D_A\subseteq[0,2L]$ és fitat.
[2] Recíprocament, suposem que $D_A$ és fitat, és a dir, que existeix $K\geq0$ amb $d(x,y)\leq K$ per a tots $x,y\in A$. Aleshores, per a tot $x\in A$, $\|x\|=d(x,0)\leq K<K+1$, de manera que $A\subseteq B_{K+1}(0)$ i $A$ és fitat.
[3] Diàmetre de $B_2$: per a $x,y\in B_2$, $\|x-y\|\leq\|x\|+\|y\|<2$. Els punts $\pm te_1$, amb $0<t<1$, són de $B_2$ i són a distància $2t$, que tendeix a $2$ quan $t\to1^-$. Per tant $\mathrm{diam}(B_2)=2$ (el suprem no s'assoleix).
[4] Diàmetre de $B_1$: per a tot $v\in\mathbb{R}^m$, $\|v\|^2=\sum_i v_i^2\leq\left(\sum_i|v_i|\right)^2$, és a dir, $\|v\|\leq\sum_i|v_i|$. Així, per a $x,y\in B_1$, $\|x-y\|\leq\sum_i|x_i-y_i|\leq\sum_i|x_i|+\sum_i|y_i|<2$.
[5] Els punts $\pm te_1$, amb $0<t<1$, també són de $B_1$ i són a distància $2t\to2$. Per tant $\mathrm{diam}(B_1)=2$, i tampoc no s'assoleix.
[6] Diàmetre de $B_3$: per a $x,y\in B_3$, $|x_i-y_i|\leq|x_i|+|y_i|<2$ per a cada $i$, d'on $\|x-y\|^2=\sum_{i=1}^m(x_i-y_i)^2<4m$, és a dir, $\|x-y\|<2\sqrt m$.
[7] Els vèrtexs $x=(1,\dots,1)$ i $y=(-1,\dots,-1)$ del cub són punts de $B_3$ i $\|x-y\|=\sqrt{4m}=2\sqrt m$. Per tant el suprem s'assoleix i $\mathrm{diam}(B_3)=2\sqrt m$.


## t1-7g:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Descriviu l'interior, la frontera, l'adherència i el conjunt de punts d'acumulació dels conjunts següents:

(g) $G=\{(x,y)\in\mathbb{R}^2\mid x^2+y^2\leq 1,\ x\neq 0\}$.
RESULTAT CORRECTE: $\mathring{G}=\{(x,y)\mid x^2+y^2<1,\ x\neq0\}$; $\mathrm{Fr}\,G=\{(x,y)\mid x^2+y^2=1\}\cup\{(0,y)\mid |y|\leq 1\}$ (la circumferència unitat i el diàmetre vertical); $\overline{G}=G'=\{(x,y)\mid x^2+y^2\leq1\}$ (el disc tancat).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [interior] Interior  (teoria: T1.14, T1.12, T2.18)
     objectiu: Determinar l'interior de $G$.
     idea: Proposar com a candidat un obert contingut a $G$ definit per desigualtats estrictes, i comprovar que els punts de $G$ que hi queden fora no són interiors.
     detall: $U=\{x^2+y^2<1\}\cap\{x^2>0\}$ és obert (Corol·lari 18(i) del Tema 2 i Proposició 12(iii)) i $U\subseteq G$, així que $U\subseteq\mathring{G}$. Si $p\in G$ amb $\|p\|=1$, els punts $(1+t)p$, $t>0$ petit, són a tota bola centrada en $p$ i no són de $G$. Per tant $\mathring{G}=\{x^2+y^2<1,\ x\neq0\}$.
  2. [frontera] Frontera  (teoria: T1.14)
     objectiu: Determinar la frontera de $G$.
     idea: Classificar els punts del pla: els de l'interior ja trobat, els altres punts de $G$, els punts del disc tancat que no són de $G$ i els de fora del disc. Per a cada tipus, decidir si tota bola centrada en ell talla $G$ i el seu complementari.
     detall: Si $x_0^2+y_0^2=1$ i $x_0\neq0$: el punt és de $G$ i tota bola conté $(1+t)(x_0,y_0)\notin G$. Si $x_0^2+y_0^2=1$ i $x_0=0$, o bé $x_0=0$, $|y_0|<1$: el punt no és de $G$, i tota bola $B_r$ conté punts $(s,(1-s)y_0)\in G$ amb $s>0$ petit ($s^2+(1-s)^2y_0^2\leq s^2+(1-s)^2<1$ per $0<s<1$). Els punts amb $x^2+y^2>1$ són exteriors i els de $\mathring{G}$ són interiors. Per tant $\mathrm{Fr}\,G=\{x^2+y^2=1\}\cup\{(0,y)\mid |y|\leq1\}$.
  3. [adherencia] Adherència  (teoria: T1.13, T1.16, T1.19)
     objectiu: Determinar l'adherència $\overline{G}$.
     idea: Trobar un tancat senzill que contingui $G$ i comprovar que cada punt seu és límit de punts de $G$, especialment els del segment que s'ha tret.
     detall: El disc tancat $\overline{B}_1(0)=\{x^2+y^2\leq1\}$ és tancat (Proposició 13(i)) i conté $G$, així que $\overline{G}\subseteq\overline{B}_1(0)$. Si $x_0\neq0$ el punt ja és de $G$. Si $x_0=0$, $|y_0|\leq1$, la successió $(1/n,(1-1/n)y_0)$ és de $G$ i hi convergeix. Per tant $\overline{G}=\{(x,y)\mid x^2+y^2\leq1\}$.
  4. [acumulacio] Punts d'acumulació  (teoria: T1.14, T1.19)
     objectiu: Determinar el conjunt derivat $G'$.
     idea: Mirar si les successions que has fet servir per a l'adherència tenen els termes diferents del límit, o si es poden modificar perquè ho siguin.
     detall: Sigui $p=(x_0,y_0)$ del disc tancat. Si $x_0=0$, la successió anterior $(1/n,(1-1/n)y_0)$ té termes diferents de $p$ (primera coordenada no nul·la). Si $x_0\neq0$, $p_n=(1-\frac1n)(x_0,y_0)$ és de $G$ per $n\geq2$ (norma $<1$ i primera coordenada no nul·la), diferent de $p$ i convergeix a $p$. Per la Proposició 19(i), $\overline{G}\subseteq G'\subseteq\overline{G}$: $G'=\{(x,y)\mid x^2+y^2\leq1\}$.
ERRORS COMUNS:
  - [oblida_diametre] Dona com a frontera només la circumferència, oblidant el segment $\{x=0\}$ que s'ha tret del disc.
  - [interior_inclou_vora] Inclou a l'interior els punts de la circumferència amb $x\neq0$, perquè són de $G$.
  - [adherencia_sense_segment] Creu que l'adherència és $G$ amb la circumferència, però sense els punts del segment vertical.

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

[T1.12] Proposició 12 (Tema 1) — Propietats dels conjunts oberts
(Propietats dels conjunts oberts.) Sigui $(M,d)$ un espai mètric. Aleshores,

i) tota bola oberta $B_r(x)$ és un conjunt obert;

ii) la unió arbitrària (finita o infinita) d'oberts és un obert;

iii) la intersecció finita d'oberts és un obert;

iv) $M$ i $\varnothing$ són conjunts oberts.

[T2.18] Corol·lari 18 (Tema 2) — Conjunts definits per desigualtats
Siguin $f,g:\mathbb{R}^n\longrightarrow\mathbb{R}$, funcions contínues. Llavors:

(i) $A=\{x\in\mathbb{R}^n:f(x)>g(x)\}$ és un conjunt obert.

(ii) $B=\{x\in\mathbb{R}^n:f(x)\geq g(x)\}$ és un conjunt tancat.

[T1.13] Proposició 13 (Tema 1) — Propietats dels conjunts tancats
Sigui $M$ un conjunt i $d$ una distància definida sobre ell. Considereu la topologia sobre $M$ induïda per $d$. Aleshores:

i) les boles tancades de $M$ són conjunts tancats.

ii) La intersecció arbitrària de tancats és un tancat.

iii) La unió finita de tancats és un tancat.

iv) $M$ i $\varnothing$ són conjunts tancats.

[T1.19] Proposició 19 (Tema 1) — Caracterització amb successions
Sigui $(M,d)$ un espai mètric, $A\subseteq M$ i $x\in M$. Aleshores:

i) $x$ és un punt d'acumulació d'$A\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\neq x$, $a_n\in A$, tal que $x=\lim_n a_n$.

ii) $x\in\overline{A}\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\in A$ tal que $x=\lim_n a_n$.

iii) $A$ és tancat $\Leftrightarrow$ el límit de tota successió convergent d'elements d'$A$ és d'$A$.
</solucio_de_referencia>

### Document a revisar

[1] Interior: el conjunt $U=\{x^2+y^2<1\}\cap\{x\neq0\}$ és obert, perquè és intersecció de dos oberts (antiimatges d'oberts per funcions contínues), i $U\subseteq G$; per tant $U\subseteq\mathring{G}$.
[2] Cap punt $p\in G$ amb $\|p\|=1$ no és interior: els punts $(1+t)p$, amb $t>0$ petit, són a tota bola centrada en $p$ i no són de $G$. Per tant $\mathring{G}=\{(x,y)\mid x^2+y^2<1,\ x\neq0\}$.
[3] Frontera: si $x_0^2+y_0^2=1$ i $x_0\neq0$, el punt és de $G$ i tota bola centrada en ell conté punts $(1+t)(x_0,y_0)\notin G$; per tant és de la frontera.
[4] Si $x_0=0$ i $|y_0|\leq1$, el punt $(0,y_0)$ no és de $G$, i tota bola centrada en ell conté punts $(s,(1-s)y_0)$ amb $s>0$ petit, que són de $G$ perquè $s\neq0$ i $s^2+(1-s)^2y_0^2\leq s^2+y_0^2\leq1$. Per tant també és de la frontera.
[5] Els punts amb $x^2+y^2>1$ són exteriors (formen un obert disjunt de $G$) i els de $\mathring{G}$ són interiors. Així, $\mathrm{Fr}\,G=\{x^2+y^2=1\}\cup\{(0,y)\mid |y|\leq1\}$: la circumferència unitat i el diàmetre vertical.
[6] Adherència: el disc tancat $\{x^2+y^2\leq1\}$ és un tancat que conté $G$, així que $\overline{G}$ hi està contingut. Recíprocament, els punts del disc amb $x_0\neq0$ ja són de $G$, i si $x_0=0$ la successió $(1/n,(1-1/n)y_0)$ és de $G$ i hi convergeix. Per tant $\overline{G}=\{x^2+y^2\leq1\}$.
[7] Punts d'acumulació: sigui $p=(x_0,y_0)$ del disc tancat. Si $x_0\neq0$, la successió $p_n=(1+\frac1n)(x_0,y_0)$ és de $G$, té termes diferents de $p$ i convergeix a $p$; si $x_0=0$, la successió $(1/n,(1-1/n)y_0)$ anterior té primera coordenada no nul·la i convergeix a $p$. Per tant $G'=\{x^2+y^2\leq1\}$.


## t1-8e:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Estudieu l'interior, la frontera, l'adherència i el conjunt de punts d'acumulació dels subconjunts següents, i decidiu si són oberts o tancats, o cap de les dues coses:

(e) $E=\{(x,y)\in\mathbb{R}^2\mid x^2+|y|=5\}$.
RESULTAT CORRECTE: $E$ és la corba tancada formada pels arcs de paràbola $y=5-x^2$ i $y=x^2-5$, $|x|\leq\sqrt5$. $\mathring{E}=\varnothing$; $\mathrm{Fr}\,E=\overline{E}=E'=E$. $E$ és tancat i no és obert.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [descriure] Descriure el conjunt
     objectiu: Entendre la forma del conjunt $E$.
     idea: Separar els casos segons el signe de $y$.
     detall: Si $y\geq0$: $y=5-x^2$ (cal $x^2\leq5$). Si $y<0$: $y=x^2-5$ (amb $x^2<5$). $E$ és la unió dels dos arcs de paràbola, que s'uneixen als punts $(\pm\sqrt5,0)$: una corba tancada i fitada.
  2. [interior] Interior  (teoria: T1.14, T1.16)
     objectiu: Decidir si $E$ té punts interiors.
     idea: Donat un punt de $E$, trobar dins de qualsevol bola centrada en ell un punt on $x^2+|y|$ sigui diferent de $5$; per exemple, allunyant-se una mica de l'origen.
     detall: Sigui $p=(x_0,y_0)\in E$ (llavors $p\neq0$) i $r>0$. Per a $s>1$, $sp$ compleix $s^2x_0^2+s|y_0|>x_0^2+|y_0|=5$, per tant $sp\notin E$, i $\|sp-p\|=(s-1)\|p\|<r$ si $s$ és prou proper a $1$. Per tant $E$ no té punts interiors, $\mathring{E}=\varnothing$.
  3. [adherencia] Adherència  (teoria: T2.17, T1.17)
     objectiu: Determinar l'adherència $\overline{E}$.
     idea: Escriure $E$ com a antiimatge d'un tancat per una funció contínua.
     detall: $E=f^{-1}(\{5\})$ amb $f(x,y)=x^2+|y|$ contínua; pel Teorema 17(d) del Tema 2, $E$ és tancat i, per la Proposició 17(ii), $\overline{E}=E$.
  4. [frontera] Frontera  (teoria: T1.14, T1.11)
     objectiu: Determinar la frontera de $E$.
     idea: Combinar el que saps de l'interior i de l'adherència.
     detall: Tot punt de $E$ és de la frontera (tota bola el conté i, com que $\mathring{E}=\varnothing$, conté punts de $E^c$); els de fora són exteriors perquè $E^c$ és obert. $\mathrm{Fr}\,E=E$.
  5. [acumulacio] Punts d'acumulació  (teoria: T1.14, T1.19)
     objectiu: Determinar el conjunt derivat $E'$.
     idea: Moure's sobre la corba, amb cura als punts on s'uneixen els dos arcs.
     detall: Sigui $p=(x_0,y_0)\in E$. Prenem $x_n=(1-\frac1n)x_0$ si $x_0\neq0$ i $x_n=\frac1n$ si $x_0=0$ (llavors $x_n\to x_0$, $x_n\neq x_0$ i $x_n^2<5$ per $n\geq3$). Si $y_0\geq0$, $p_n=(x_n,5-x_n^2)$; si $y_0<0$, $p_n=(x_n,x_n^2-5)$. En tots dos casos $p_n\in E$, $p_n\neq p$ i $p_n\to p$. Per la Proposició 19(i), $E'=E$.
  6. [obert_tancat] Obert o tancat  (teoria: T1.17, T1.11)
     objectiu: Classificar $E$: obert, tancat, totes dues coses o cap.
     idea: Comparar $E$ amb la seva adherència i amb el seu interior.
     detall: $\overline{E}=E$: és tancat. $\mathring{E}=\varnothing\neq E$: no és obert. Per tant $E$ és tancat però no és obert.
ERRORS COMUNS:
  - [interior_regio] Confon $E$ amb la regió que tanca la corba ($x^2+|y|\leq5$) i li atribueix interior.
  - [valor_absolut_no_continu] Dubta que $x^2+|y|$ sigui contínua (pel valor absolut) i no sap justificar que $E$ és tancat.
  - [punts_unio] Pensa que als punts on s'uneixen els dos arcs la corba "fa punta" i que això els fa especials topològicament (aïllats o interiors).

TEORIA DEL CURS QUE FA SERVIR:
[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.

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

[T2.17] Teorema 17 (Tema 2) — Caracteritzacions de la continuïtat
Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents:

(a) $f$ és contínua en $\Omega$;

(b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;

(c) per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$;

(d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.

[T1.17] Proposició 17 (Tema 1) — Propietats de la clausura
Les següents afirmacions són certes:

i) $A\subseteq B\Rightarrow\overline{A}\subseteq\overline{B}$.

ii) $A$ és tancat $\Leftrightarrow\overline{A}=A$.

iii) $\overline{A\cup B}=\overline{A}\cup\overline{B}$.

iv) $\overline{A\cap B}\subseteq\overline{A}\cap\overline{B}$.

[T1.19] Proposició 19 (Tema 1) — Caracterització amb successions
Sigui $(M,d)$ un espai mètric, $A\subseteq M$ i $x\in M$. Aleshores:

i) $x$ és un punt d'acumulació d'$A\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\neq x$, $a_n\in A$, tal que $x=\lim_n a_n$.

ii) $x\in\overline{A}\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\in A$ tal que $x=\lim_n a_n$.

iii) $A$ és tancat $\Leftrightarrow$ el límit de tota successió convergent d'elements d'$A$ és d'$A$.
</solucio_de_referencia>

### Document a revisar

[1] Si $y\geq0$, la condició és $y=5-x^2$ (amb $x^2\leq5$); si $y<0$, és $y=x^2-5$ (amb $x^2<5$). Així $E$ és la unió de dos arcs de paràbola que s'uneixen als punts $(\pm\sqrt5,0)$: una corba tancada i fitada.
[2] Interior: sigui $p=(x_0,y_0)\in E$ (llavors $p\neq(0,0)$) i $r>0$. Per a $s>1$, $s^2x_0^2+s|y_0|>x_0^2+|y_0|=5$, de manera que $sp\notin E$, i $\|sp-p\|=(s-1)\|p\|<r$ si $s$ és prou proper a $1$. Per tant cap punt de $E$ és interior: $\mathring{E}=\varnothing$.
[3] Adherència: com que $E$ és fitat ($|x|\leq\sqrt5$ i $|y|\leq5$), és un conjunt tancat, i per tant $\overline{E}=E$.
[4] Frontera: tota bola centrada en un punt de $E$ conté aquest punt i, com que $\mathring{E}=\varnothing$, també punts de $E^c$; i els punts de fora de $E$ són exteriors, perquè $E^c$ és obert. Per tant $\mathrm{Fr}\,E=E$.
[5] Punts d'acumulació: sigui $p=(x_0,y_0)\in E$. Prenem $x_n=(1-\frac1n)x_0$, que compleix $x_n\to x_0$, $x_n\neq x_0$ i $x_n^2<5$. Si $y_0\geq0$, posem $p_n=(x_n,5-x_n^2)$, i si $y_0<0$, $p_n=(x_n,x_n^2-5)$.
[6] En tots dos casos $p_n\in E$, $p_n\neq p$ i $p_n\to p$, així que $p\in E'$. Com que $E'\subseteq\overline{E}=E$, obtenim $E'=E$.
[7] Finalment, $\overline{E}=E$, de manera que $E$ és tancat, i $\mathring{E}=\varnothing\neq E$, de manera que no és obert.


## t1-14a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Demostreu que si $K_1\subset\mathbb{R}^{n_1}$ i $K_2\subset\mathbb{R}^{n_2}$ són compactes, aleshores $K_1\times K_2\subset\mathbb{R}^{n_1+n_2}$ també és compacte.
RESULTAT CORRECTE: Per Bolzano-Weierstrass n'hi ha prou de veure que $K_1\times K_2$ és seqüencialment compacte. Sigui $(a_k,b_k)\in K_1\times K_2$. Com que $K_1$ és seqüencialment compacte, hi ha una parcial $a_{k_j}\to a\in K_1$; com que $K_2$ ho és, $(b_{k_j})_j$ té una parcial $b_{k_{j_s}}\to b\in K_2$. Llavors $a_{k_{j_s}}\to a$ també, i com que $\|(u,v)\|^2=\|u\|^2+\|v\|^2$, $(a_{k_{j_s}},b_{k_{j_s}})\to(a,b)\in K_1\times K_2$. (Alternativa: Heine-Borel, $K_1\times K_2$ és tancat i fitat.)
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [estrategia] Reduir a successions  (teoria: T1.26)
     objectiu: Triar una caracterització de la compacitat que sigui còmoda per a productes.
     idea: Pel Teorema de Bolzano-Weierstrass, compacte equival a seqüencialment compacte; o bé, a $\mathbb{R}^n$, Heine-Borel.
     detall: Pel Teorema de Bolzano-Weierstrass, $K_1$ i $K_2$ són seqüencialment compactes, i n'hi ha prou de veure que $K_1\times K_2$ també ho és: que tota successió $((a_k,b_k))_k$ de $K_1\times K_2$ té una parcial convergent a un punt de $K_1\times K_2$.
  2. [parcials_encaixades] Extreure parcials successives  (teoria: T1.24, T1.34+dem)
     objectiu: Donada una successió $((a_k,b_k))_k$ de $K_1\times K_2$, trobar-ne una parcial que convergeixi a $K_1\times K_2$.
     idea: Treballar primer amb la primera component i després, sobre la parcial obtinguda, amb la segona (com a la demostració de Heine-Borel).
     detall: $(a_k)_k\subseteq K_1$ té una parcial $a_{k_j}\to a\in K_1$. La successió $(b_{k_j})_j\subseteq K_2$ té una parcial $b_{k_{j_s}}\to b\in K_2$. Com que $(a_{k_{j_s}})_s$ és parcial d'una successió convergent, també $a_{k_{j_s}}\to a$.
  3. [convergencia_producte] Convergència al producte  (teoria: T1.8, T1.18, T1.26)
     objectiu: Comprovar que la parcial obtinguda convergeix a $\mathbb{R}^{n_1+n_2}$ cap a un punt de $K_1\times K_2$.
     idea: Expressar la norma euclidiana de $\mathbb{R}^{n_1+n_2}$ en termes de les normes de les dues components.
     detall: $\|(a_{k_{j_s}},b_{k_{j_s}})-(a,b)\|^2=\|a_{k_{j_s}}-a\|^2+\|b_{k_{j_s}}-b\|^2\to0$, així la parcial convergeix a $(a,b)\in K_1\times K_2$. Per Bolzano-Weierstrass, $K_1\times K_2$ és compacte.
ERRORS COMUNS:
  - [mateixa_parcial] Agafa parcials convergents de $(a_k)$ i de $(b_k)$ independentment, amb índexs diferents, i les combina.
  - [recobriment_producte] Intenta fer productes de recobriments oberts sense justificar que tot obert de $\mathbb{R}^{n_1+n_2}$ es pugui descompondre així.
  - [convergencia_components] No justifica que la convergència de les components implica la convergència del parell.

TEORIA DEL CURS QUE FA SERVIR:
[T1.24] Definició 24 (Tema 1) — Compacte i seqüencialment compacte
Sigui $(M,d)$ espai mètric, $A\subseteq M$.

i) $A$ és _compacte_ si tot recobriment per oberts de $A$ admet un subrecobriment finit, és a dir: si $A\subseteq\bigcup_{i\in I}U_i$, amb $U_i$ obert, aleshores existeixen $i_1,\ldots,i_k\in I$ tals que $A\subseteq\bigcup_{j=1}^k U_{i_j}$.

ii) $A$ és _seqüencialment compacte_ si tota successió $(x_n)_{n\in\mathbb{N}}\subseteq A$ admet una subsuccessió (una parcial) convergent a un punt de $A$.

[T1.26] Teorema 26 (Tema 1) — Teorema de Bolzano-Weierstrass
(Bolzano-Weierstrass.) Sigui $(M,d)$ espai mètric i $A\subseteq M$. Aleshores:
$A$ és compacte $\Leftrightarrow$ $A$ és seqüencialment compacte.

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

[T1.8] Exemple 8 (Tema 1) — Norma i distància en exemples
a) A $\mathbb{R}^2$, definim $\langle(a,b),(c,d)\rangle=ac+bd$. Llavors,

$$\begin{aligned}\|(a,b)\|&=\sqrt{\langle(a,b),(a,b)\rangle}=\sqrt{a^2+b^2},\\d((a,b),(c,d))&=\|(a,b)-(c,d)\|=\|(a-c,b-d)\|\\&=\sqrt{\langle(a-c,b-d),(a-c,b-d)\rangle}=\sqrt{(a-c)^2+(b-d)^2}\quad\text{(Pitàgores).}\end{aligned}$$

b) A $\mathbb{R}^3$, $\|(a,b,c)\|=\sqrt{a^2+b^2+c^2}$ i, en general, a $\mathbb{R}^n$:

$$\begin{aligned}\langle(a_1,a_2,\ldots,a_n),(b_1,b_2,\ldots,b_n)\rangle&:=\sum_{i=1}^n a_i\cdot b_i;\\\|(a_1,a_2,\ldots,a_n)\|&=\sqrt{\sum_{i=1}^n a_i^2};\\d((a_1,a_2,\ldots,a_n),(b_1,b_2,\ldots,b_n))&=\sqrt{\sum_{i=1}^n(a_i-b_i)^2}.\end{aligned}$$

c) $E=\mathcal{C}([a,b])$. Aleshores:

$$\begin{aligned}\langle f,g\rangle&:=\int_a^b f(x)g(x)\,dx;\\\|f\|&=\sqrt{\int_a^b f^2(x)\,dx};\\d(f,g)=\|f-g\|&=\sqrt{\int_a^b(f(x)-g(x))^2dx}\quad\text{("àrea" entre }y=f(x)\text{ i }y=g(x)\text{).}\end{aligned}$$

d) $E=\mathcal{B}(A)=$ conjunt de funcions $f:A\to\mathbb{R}$ fitades (inferiorment i superior), amb $A$ conjunt arbitrari. Aleshores, $d(f,g)=\displaystyle\sup_{t\in A}|f(t)-g(t)|$ és una distància.

[T1.18] Definició 18 (Tema 1) — Successió convergent
Sigui $(M,d)$ un espai mètric. Direm que una successió $(x_n)_{n\in\mathbb{N}}$ és _convergent_ a $M$ si existeix $x\in M$ tal que $\forall\varepsilon>0,\exists n_0\in\mathbb{N}$ tal que $d(x_n,x)<\varepsilon$ $\forall n\geq n_0$. En aquest cas, diem que $x$ és el límit de la successió, i ho denotem per $x=\displaystyle\lim_{n\to\infty}x_n$ (el límit, si existeix, és únic).
</solucio_de_referencia>

### Document a revisar

[1] Pel teorema de Bolzano-Weierstrass, un subconjunt de $\mathbb{R}^n$ és compacte si i només si tota successió del conjunt té una parcial convergent a un punt del conjunt. Ho comprovarem per a $K_1\times K_2$.
[2] Sigui $((a_k,b_k))_k$ una successió de $K_1\times K_2$, és a dir, amb $a_k\in K_1$ i $b_k\in K_2$ per a tot $k$.
[3] La successió $(a_k)_k$ és fitada, perquè $K_1$ és fitat, i per Bolzano-Weierstrass té una parcial convergent $a_{k_j}\to a$. Com que $K_1$ és obert, el límit $a$ és de $K_1$.
[4] Igualment, la successió $(b_{k_j})_j$ és fitada, perquè $K_2$ és fitat, i com que $K_2$ és tancat convergeix a un punt $b\in K_2$.
[5] Aleshores $\|(a_{k_j},b_{k_j})-(a,b)\|^2=\|a_{k_j}-a\|^2+\|b_{k_j}-b\|^2\to0$, és a dir, la parcial $((a_{k_j},b_{k_j}))_j$ convergeix a $(a,b)$.
[6] Com que $(a,b)\in K_1\times K_2$, tota successió de $K_1\times K_2$ té una parcial convergent a un punt de $K_1\times K_2$, i per tant $K_1\times K_2$ és compacte.


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
[4] Com que l'ínfim és la més petita de les fites inferiors, $d(x,A)-d(x,y)\leq d(y,A)$, és a dir, $d(x,A)-d(y,A)\leq d(x,y)$.
[5] Per a l'altra desigualtat, sigui $a_0\in A$ el punt d'$A$ més proper a $x$, de manera que $d(x,a_0)=d(x,A)$. Aleshores $d(y,A)\leq d(y,a_0)\leq d(y,x)+d(x,a_0)=d(x,y)+d(x,A)$, és a dir, $d(y,A)-d(x,A)\leq d(x,y)$.
[6] Juntant les dues desigualtats, $-d(x,y)\leq d(x,A)-d(y,A)\leq d(x,y)$, que és exactament $|d(x,A)-d(y,A)|\leq d(x,y)$.


## t2-15a:facil

### Referència

<solucio_de_referencia>
ENUNCIAT: Justifiqueu adequadament si els conjunts següents són compactes:

(a) $A=\{(x,y,z,t)\in\mathbb{R}^4\ \mid\ 2x^2+y^2-z^2=2,\ y^2+2z^2\leqslant10,\ |z|\geqslant|t|\ \}$.
RESULTAT CORRECTE: $A$ és compacte. És tancat (intersecció de conjunts definits per una igualtat i desigualtats no estrictes entre funcions contínues a $\mathbb{R}^4$) i fitat: de $y^2+2z^2\le10$ surt $y^2\le10$ i $z^2\le5$; llavors $t^2\le z^2\le5$ i $x^2=1+\frac{z^2-y^2}{2}\le\frac72$. Pel teorema de Heine-Borel, $A$ és compacte.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [criteri] Triar el criteri  (teoria: T1.34)
     objectiu: Decidir quines propietats de $A$ cal estudiar per saber si és compacte.
     idea: A $\mathbb{R}^n$ hi ha una caracterització dels compactes en termes de dues propietats més fàcils de comprovar que la definició amb recobriments.
     detall: Pel teorema de Heine-Borel, un subconjunt de $\mathbb{R}^4$ és compacte si i només si és tancat i fitat.
  2. [tancat] $A$ és tancat  (teoria: T2.18, T1.13, T2.20)
     objectiu: Determinar si $A$ és tancat.
     idea: Cada condició és una igualtat o desigualtat no estricta entre funcions contínues a tot $\mathbb{R}^4$.
     detall: $2x^2+y^2-z^2$, $y^2+2z^2$, $|z|$ i $|t|$ són contínues a $\mathbb{R}^4$. Els conjunts $\{2x^2+y^2-z^2\ge2\}$, $\{2\ge2x^2+y^2-z^2\}$, $\{10\ge y^2+2z^2\}$ i $\{|z|\ge|t|\}$ són tancats pel corol·lari de les desigualtats, i $A$ n'és la intersecció, per tant tancat.
  3. [fitat] $A$ és fitat  (teoria: T1.33)
     objectiu: Trobar una fita per a cadascuna de les quatre coordenades dels punts de $A$.
     idea: Començar per la desigualtat que fita directament algunes coordenades, i usar-ne el resultat a les altres condicions per fitar les restants.
     detall: De $y^2+2z^2\le10$: $y^2\le10$ i $z^2\le5$. De $|t|\le|z|$: $t^2\le5$. De la igualtat, $2x^2=2-y^2+z^2\le2+5=7$, és a dir $x^2\le\frac72$. Per tant $\|(x,y,z,t)\|^2\le\frac72+10+5+5$, i $A$ està contingut en una bola centrada a l'origen: és fitat.
  4. [concloure] Concloure  (teoria: T1.34)
     objectiu: Combinar les propietats obtingudes per respondre la pregunta.
     idea: Aplicar el criteri triat al primer pas.
     detall: $A$ és tancat i fitat a $\mathbb{R}^4$, i per Heine-Borel és compacte.
ERRORS COMUNS:
  - [x_no_fitada] Pensa que $x$ no està fitada perquè cap desigualtat la conté directament (o perquè la igualtat defineix un hiperboloide, no fitat).
  - [t_oblidada] Fita $x,y,z$ però s'oblida de la coordenada $t$.
  - [nomes_tancat] Conclou compacitat només a partir de ser tancat (o només de ser fitat).

TEORIA DEL CURS QUE FA SERVIR:
[T1.24] Definició 24 (Tema 1) — Compacte i seqüencialment compacte
Sigui $(M,d)$ espai mètric, $A\subseteq M$.

i) $A$ és _compacte_ si tot recobriment per oberts de $A$ admet un subrecobriment finit, és a dir: si $A\subseteq\bigcup_{i\in I}U_i$, amb $U_i$ obert, aleshores existeixen $i_1,\ldots,i_k\in I$ tals que $A\subseteq\bigcup_{j=1}^k U_{i_j}$.

ii) $A$ és _seqüencialment compacte_ si tota successió $(x_n)_{n\in\mathbb{N}}\subseteq A$ admet una subsuccessió (una parcial) convergent a un punt de $A$.

[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.

[T2.18] Corol·lari 18 (Tema 2) — Conjunts definits per desigualtats
Siguin $f,g:\mathbb{R}^n\longrightarrow\mathbb{R}$, funcions contínues. Llavors:

(i) $A=\{x\in\mathbb{R}^n:f(x)>g(x)\}$ és un conjunt obert.

(ii) $B=\{x\in\mathbb{R}^n:f(x)\geq g(x)\}$ és un conjunt tancat.

[T1.13] Proposició 13 (Tema 1) — Propietats dels conjunts tancats
Sigui $M$ un conjunt i $d$ una distància definida sobre ell. Considereu la topologia sobre $M$ induïda per $d$. Aleshores:

i) les boles tancades de $M$ són conjunts tancats.

ii) La intersecció arbitrària de tancats és un tancat.

iii) La unió finita de tancats és un tancat.

iv) $M$ i $\varnothing$ són conjunts tancats.

[T2.20] Proposició 20 (Tema 2) — Àlgebra de funcions contínues
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $h:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, contínues. Llavors

(i) $f+g,\ \lambda f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $\lambda\in\mathbb{R}$, són contínues;

(ii) $hf:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ és contínua;

(iii) per a $m=1$, si $g(x)\neq0\ \forall x\in\Omega$, $f/g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(iv) $\langle f,g\rangle:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(v) $\|f\|:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua.

[T1.33] Definició 33 (Tema 1) — Conjunt fitat
Es diu que $A\subseteq M$ és _fitat_ si i només si existeix un $x\in M$ i un valor $L>0$ tal que $A\subseteq B_L(x)$.
</solucio_de_referencia>

### Document a revisar

[1] Pel teorema de Heine-Borel, un subconjunt de $\mathbb{R}^4$ és compacte si i només si és tancat i fitat. Comprovem les dues coses.
[2] Tancat: les funcions $2x^2+y^2-z^2$, $y^2+2z^2$, $|z|$ i $|t|$ són contínues a $\mathbb{R}^4$. La igualtat equival a les dues desigualtats $2x^2+y^2-z^2\geq2$ i $2x^2+y^2-z^2\leq2$, i els conjunts $\{2x^2+y^2-z^2\geq2\}$, $\{2x^2+y^2-z^2\leq2\}$, $\{y^2+2z^2\leq10\}$ i $\{|z|\geq|t|\}$ són tancats perquè vénen de desigualtats no estrictes entre funcions contínues. $A$ n'és la intersecció, i per tant és tancat.
[3] Fitat: de $y^2+2z^2\leq10$ obtenim $y^2\leq10$ i $2z^2\leq10$, és a dir, $z^2\leq5$.
[4] De $|t|\leq|z|$ obtenim $t^2\leq z^2\leq5$.
[5] De la igualtat, $2x^2=2+y^2-z^2\leq2+10=12$, és a dir, $x^2\leq6$.
[6] Per tant les quatre coordenades estan fitades, $A$ està contingut en una bola centrada a l'origen i és fitat. Com que és tancat i fitat, per Heine-Borel $A$ és compacte.


## t2-1c:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Determineu el domini d'existència i el recorregut (imatge) de les funcions següents, i digueu si aquests conjunts són oberts o tancats:

(c) $f(x,y)=\arcsin\left(x/y\right)$,
RESULTAT CORRECTE: $\mathrm{Dom}(f)=\{(x,y)\mid y\neq 0,\ |x|\le|y|\}=\{|x|\le|y|\}\setminus\{(0,0)\}$ (la regió entre les diagonals que conté l'eix $y$, sense l'origen): no és ni obert ni tancat.
$\mathrm{Im}(f)=[-\pi/2,\pi/2]$, que és tancat i no és obert.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [domini] Calcular el domini  (teoria: T2.3)
     objectiu: Determinar el conjunt de punts $(x,y)$ on l'expressió de $f$ té sentit.
     idea: Hi ha dues condicions: que el quocient existeixi i que estigui dins del domini de l'arcsinus. Després, reescriu la segona sense quocients.
     detall: Cal $y\neq0$ i $-1\le x/y\le 1$, és a dir $|x/y|\le1$, que (multiplicant per $|y|>0$) equival a $|x|\le|y|$. Per tant $\mathrm{Dom}(f)=\{(x,y)\mid |x|\le|y|\}\setminus\{(0,0)\}$: la regió tancada entre les rectes $y=x$ i $y=-x$ que conté l'eix $y$, sense l'origen.
  2. [domini_topologia] Topologia del domini  (teoria: T1.11, T1.16, T1.19)
     objectiu: Decidir si el domini és obert, tancat, totes dues coses o cap de les dues.
     idea: Mira els punts de les dues rectes que limiten la regió (per a l'obertura) i el punt que s'ha hagut d'excloure (per al tancament).
     detall: No és obert: $(1,1)\in\mathrm{Dom}(f)$, però tota bola centrada en $(1,1)$ conté punts $(1+\varepsilon,1)$ amb $|x|>|y|$. No és tancat: els punts $(0,1/n)$ són del domini i convergeixen a $(0,0)$, que no hi és; per tant $(0,0)$ és adherent al domini sense pertànyer-hi, i un tancat conté tots els seus punts adherents. El domini no és ni obert ni tancat.
  3. [imatge] Calcular la imatge  (teoria: T2.3)
     objectiu: Determinar el conjunt de valors que pren $f$.
     idea: Determina quins valors pren el quocient $x/y$ sobre el domini i aplica-hi l'arcsinus, que és bijectiu des del seu domini a la seva imatge.
     detall: Sobre el domini $x/y$ pren tots els valors de $[-1,1]$ (per exemple als punts $(t,1)$, $t\in[-1,1]$), i $\arcsin([-1,1])=[-\pi/2,\pi/2]$. Per tant $\mathrm{Im}(f)=[-\pi/2,\pi/2]$.
  4. [imatge_topologia] Topologia de la imatge  (teoria: T1.13, T1.11)
     objectiu: Decidir si la imatge, com a subconjunt de $\mathbb{R}$, és oberta, tancada, totes dues coses o cap.
     idea: Reconeix la imatge com una bola tancada de $\mathbb{R}$ i mira si els extrems admeten una bola oberta dins del conjunt.
     detall: És la bola tancada $\overline{B}(0,\pi/2)$, per tant tancada. No és oberta: tota bola centrada en $\pi/2$ conté punts més grans que $\pi/2$.
ERRORS COMUNS:
  - [multiplicar_sense_signe] Passa de $-1\le x/y\le 1$ a $-y\le x\le y$ multiplicant per $y$ sense tenir en compte que $y$ pot ser negatiu.
  - [oblidar_origen] Inclou l'origen al domini (o conclou que el domini és tancat) oblidant que cal $y\neq0$.
  - [obert_si_no_tancat] Conclou que el domini és obert perquè no és tancat (o a l'inrevés).

TEORIA DEL CURS QUE FA SERVIR:
[T2.3] Definició 3 (Tema 2) — Conceptes bàsics de funcions
Conceptes bàsics (extensions de concepte de càlcul en una variable).

- El domini de $f$ és el subconjunt de $M$ on $f$ està definida: $\mathrm{Dom}(f)=\{x\in M \text{ tals que } \exists f(x)\}$.
- La imatge de $f$ és $\mathrm{Im}(f)=\{y\in N\mid\exists x\in M \text{ amb } f(x)=y\}\subseteq N$.
- La gràfica de $f$ és $\mathrm{Graf}(f)=\{(x,f(x))\mid x\in\mathrm{Dom}(f)\}\subseteq M\times N$.
- $f$ és injectiva $\Leftrightarrow\forall x,y\in M$, si $f(x)=f(y)$, aleshores $x=y$.
- $f$ és exhaustiva $\Leftrightarrow\forall y\in N,\exists x\in M$ tal que $f(x)=y$.
- $f$ és bijectiva $\Leftrightarrow\forall y\in N,\exists!\,x\in M$ tal que $f(x)=y$.

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

[T1.19] Proposició 19 (Tema 1) — Caracterització amb successions
Sigui $(M,d)$ un espai mètric, $A\subseteq M$ i $x\in M$. Aleshores:

i) $x$ és un punt d'acumulació d'$A\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\neq x$, $a_n\in A$, tal que $x=\lim_n a_n$.

ii) $x\in\overline{A}\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\in A$ tal que $x=\lim_n a_n$.

iii) $A$ és tancat $\Leftrightarrow$ el límit de tota successió convergent d'elements d'$A$ és d'$A$.

[T1.13] Proposició 13 (Tema 1) — Propietats dels conjunts tancats
Sigui $M$ un conjunt i $d$ una distància definida sobre ell. Considereu la topologia sobre $M$ induïda per $d$. Aleshores:

i) les boles tancades de $M$ són conjunts tancats.

ii) La intersecció arbitrària de tancats és un tancat.

iii) La unió finita de tancats és un tancat.

iv) $M$ i $\varnothing$ són conjunts tancats.
</solucio_de_referencia>

### Document a revisar

[1] La funció $\arcsin$ està definida a $[-1,1]$, i el quocient $x/y$ demana $y\neq0$. Per tant el domini està format pels punts amb $y\neq0$ i $-1\le x/y\le1$.
[2] Multiplicant les desigualtats per $y$ obtenim $-y\le x\le y$. Per tant $\mathrm{Dom}(f)=\{(x,y)\mid -y\le x\le y\}\setminus\{(0,0)\}$: la regió entre les rectes $y=x$ i $y=-x$ situada per sobre de l'origen.
[3] El domini no és obert: $(1,1)$ hi pertany, però tota bola centrada en $(1,1)$ conté punts $(1+\varepsilon,1)$ amb $\varepsilon>0$, que no hi pertanyen perquè $x>y$.
[4] Tampoc no és tancat: els punts $(0,1/n)$ són del domini i convergeixen a $(0,0)$, que no hi és. Així $(0,0)$ és un punt adherent que no hi pertany, i el domini no és ni obert ni tancat.
[5] Imatge: sobre els punts $(t,1)$ amb $t\in[-1,1]$, que són del domini, el quocient $x/y=t$ recorre tot $[-1,1]$, i $\arcsin([-1,1])=[-\pi/2,\pi/2]$. Per tant $\mathrm{Im}(f)=[-\pi/2,\pi/2]$.
[6] La imatge no és oberta: tota bola centrada en $\pi/2$ conté punts més grans que $\pi/2$, que no hi són. Com que no és oberta, és un conjunt tancat de $\mathbb{R}$.


## t2-9a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considereu la funció $F:\mathbb{R}^2\to\mathbb{R}^2$ que té components
$$F_1(x,y)=\begin{cases}\dfrac{xy}{(x^2+y^2)^{1/2}} & \text{si } (x,y)\neq(0,0),\\ 0 & \text{si } (x,y)=(0,0),\end{cases}\qquad F_2(x,y)=\begin{cases}\dfrac{x}{x+y^2} & \text{si } x\neq-y^2,\\ 0 & \text{si } x=-y^2.\end{cases}$$

(a) Estudieu la continuïtat de $F$ i proveu que el seu conjunt de punts de discontinuïtat és tancat.
RESULTAT CORRECTE: $F_1$ és contínua a tot $\mathbb{R}^2$ (a l'origen, $|F_1|\le\frac12\sqrt{x^2+y^2}\to0$). $F_2$ és contínua a $\{x+y^2\neq0\}$ i discontínua a tots els punts de la paràbola $P=\{(x,y)\mid x+y^2=0\}$: als punts $(a,b)\in P$ diferents de l'origen no és fitada a prop (numerador $\to a\neq0$, denominador $\to0$), i a l'origen val $1$ sobre $y=0$ i $0$ sobre $x=0$. Per tant $F$ és contínua exactament a $\mathbb{R}^2\setminus P$, i el conjunt de discontinuïtats és $P=h^{-1}(\{0\})$ amb $h(x,y)=x+y^2$ contínua: és tancat.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [components] Reduir a les components  (teoria: T2.9, T2.14)
     objectiu: Relacionar la continuïtat de $F$ amb la de les seves components.
     idea: Un límit a $\mathbb{R}^2$ existeix si i només si existeixen els límits de cada component.
     detall: $F$ és contínua en un punt si i només si $F_1$ i $F_2$ ho són: si les components tenen límit, $F$ també (àlgebra de límits), i recíprocament $|F_i(x)-L_i|\le\|F(x)-L\|$. El conjunt de discontinuïtats de $F$ és la unió dels de $F_1$ i $F_2$.
  2. [F1] Continuïtat de la primera component  (teoria: T2.20, T2.14)
     objectiu: Estudiar la continuïtat de $F_1$, en particular a l'origen.
     idea: Fora de l'origen és un quocient de funcions contínues; a l'origen, fitar $|xy|$ en termes de $x^2+y^2$.
     detall: A $\mathbb{R}^2\setminus\{(0,0)\}$, $F_1$ és quocient de funcions contínues ($xy$ i la norma) amb denominador no nul. A l'origen: $|xy|\le\frac{x^2+y^2}{2}$, d'on $|F_1(x,y)|\le\frac12\sqrt{x^2+y^2}\to0=F_1(0,0)$. $F_1$ és contínua a tot $\mathbb{R}^2$.
  3. [F2] Continuïtat de la segona component  (teoria: T2.20, T2.10, T2.14)
     objectiu: Determinar en quins punts $F_2$ és contínua i en quins no.
     idea: Separar els punts on el denominador no s'anul·la dels punts on sí; en aquests últims, mirar si el numerador també s'anul·la i provar camins.
     detall: Sigui $P=\{x+y^2=0\}$. A $\mathbb{R}^2\setminus P$ (obert), $F_2$ coincideix amb el quocient $\frac{x}{x+y^2}$ de polinomis amb denominador no nul: contínua. Si $(a,b)\in P$ i $(a,b)\neq(0,0)$, aleshores $a=-b^2\neq0$ i $F_2(a+t,b)=\frac{a+t}{t}$ per a $t\neq0$, que no és fitat quan $t\to0$: discontínua. A l'origen: $F_2(x,0)=1$ per a $x\neq0$ i $F_2(0,y)=0$ per a $y\neq0$; no hi ha límit: discontínua.
  4. [tancat] El conjunt de discontinuïtats és tancat  (teoria: T2.17, T2.18)
     objectiu: Demostrar que el conjunt de punts de discontinuïtat obtingut és tancat.
     idea: Escriure'l com l'antiimatge d'un tancat per una funció contínua definida a tot $\mathbb{R}^2$.
     detall: El conjunt de discontinuïtats de $F$ és $P=\{(x,y)\mid x+y^2=0\}=h^{-1}(\{0\})$ amb $h(x,y)=x+y^2$ polinòmica, contínua a $\mathbb{R}^2$. Com que $\{0\}$ és tancat a $\mathbb{R}$, $P$ és tancat (caracterització de la continuïtat amb tancats). Alternativament, $\mathbb{R}^2\setminus P=\{h>0\}\cup\{h<0\}$ és unió d'oberts.
ERRORS COMUNS:
  - [origen_continua_F2] Pensa que a l'origen $F_2$ és contínua perquè el numerador també s'anul·la, o només comprova un camí.
  - [nomes_origen] Només estudia l'origen i oblida els altres punts de la corba on s'anul·la el denominador.
  - [tancat_sense_justificar] Afirma que el conjunt és tancat "perquè és una corba" sense cap justificació.

TEORIA DEL CURS QUE FA SERVIR:
[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.

[T2.9] Proposició 9 (Tema 2) — Àlgebra de límits
Sigui $x_0\in\Omega'\subseteq\mathbb{R}^n$, i siguin $F_1$ i $F_2:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^m$ tals que $\displaystyle\lim_{x\to x_0}F_j(x)=L_j$, i siguin $f_1$ i $f_2:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}$ tals que $\displaystyle\lim_{x\to x_0}f_j(x)=b_j$, per a $j=1,2$; aleshores,

(i) $\displaystyle\lim_{x\to x_0}(F_1\pm F_2)(x)=L_1\pm L_2$;

(ii) $\displaystyle\lim_{x\to x_0}(\lambda F_j)(x)=\lambda L_j,\ \forall\lambda\in\mathbb{R}$;

(iii) $\displaystyle\lim_{x\to x_0}\langle F_1(x),F_2(x)\rangle=\langle L_1,L_2\rangle$; en particular, $\displaystyle\lim_{x\to x_0}\|F_j(x)\|=\|L_j\|$;

(iv) $\displaystyle\lim_{x\to x_0}(f_1\,f_2)(x)=b_1\,b_2$; $\displaystyle\lim_{x\to x_0}(f_1/f_2)(x)=b_1/b_2$, sempre que la divisió tingui sentit;

(v) $\displaystyle\lim_{x\to x_0}(f_1,f_2)(x)=(b_1,b_2)$.

[T2.20] Proposició 20 (Tema 2) — Àlgebra de funcions contínues
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $h:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, contínues. Llavors

(i) $f+g,\ \lambda f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $\lambda\in\mathbb{R}$, són contínues;

(ii) $hf:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ és contínua;

(iii) per a $m=1$, si $g(x)\neq0\ \forall x\in\Omega$, $f/g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(iv) $\langle f,g\rangle:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(v) $\|f\|:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua.

[T2.10] Proposició 10 (Tema 2) — Límit per camins
Límit per camins. Si $F:D\subseteq\mathbb{R}^2\longrightarrow\mathbb{R}^m$ i $(a,b)\in D'$ tal que $\displaystyle\exists\lim_{(x,y)\to(a,b)}F(x,y)=L$, llavors per a tota funció real i contínua $g$ definida en un entorn d'$a$, tal que $g(a)=b$, es compleix que
$$\lim_{x\to a}F(x,g(x))=L.$$

[T2.17] Teorema 17 (Tema 2) — Caracteritzacions de la continuïtat
Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents:

(a) $f$ és contínua en $\Omega$;

(b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;

(c) per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$;

(d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.

[T2.18] Corol·lari 18 (Tema 2) — Conjunts definits per desigualtats
Siguin $f,g:\mathbb{R}^n\longrightarrow\mathbb{R}$, funcions contínues. Llavors:

(i) $A=\{x\in\mathbb{R}^n:f(x)>g(x)\}$ és un conjunt obert.

(ii) $B=\{x\in\mathbb{R}^n:f(x)\geq g(x)\}$ és un conjunt tancat.

[T2.11] Exemple 11 (Tema 2) — No existència de límit per camins
La proposició 10 es pot fer servir per demostrar la no existència de límits. Considerem, per exemple,
$$f(x,y)=\begin{cases}\dfrac{y}{y+x^2}, & y\neq-x^2,\\ \alpha, & y=-x^2,\end{cases}$$
on $\alpha$ és un nombre real qualsevol. Calculem el límit de la restricció de $f$ a un parell de corbes "distingides" que passen per l'origen:

- Sobre $y=-x^2$, $\displaystyle\lim_{x\to0}f(x,-x^2)=\alpha$, per definició.
- Sobre $y=x^2$, $\displaystyle\lim_{x\to0}f(x,x^2)=\lim_{x\to0}\frac{x^2}{x^2+x^2}=\frac{1}{2}$.

Clarament, una condició necessària perquè existeixi $\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$ és que $\alpha=1/2$. Tot i així, si calculem el límit sobre una paràbola "qualsevol" (ens en deixem alguna, però no és rellevant per a l'exercici) que passi per l'origen, $y=m\,x^2$ amb $m\in\mathbb{R}$, tenim que:
$$\lim_{x\to0}f(x,m\,x^2)=\lim_{x\to0}\frac{m\,x^2}{m\,x^2+x^2}=\frac{m}{m+1},$$
que depèn de $m$, i només coincideix amb $1/2$ si $m=1$. Per tant, podem afirmar que $\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$ no existeix.
</solucio_de_referencia>

### Document a revisar

[1] $F$ és contínua en un punt si i només si ho són les dues components $F_1$ i $F_2$, perquè $|F_i(x)-L_i|\le\|F(x)-L\|\le|F_1(x)-L_1|+|F_2(x)-L_2|$. Per tant el conjunt de discontinuïtats de $F$ és la unió dels de $F_1$ i $F_2$.
[2] Fora de l'origen, $F_1$ és el quocient de $xy$ i de la norma $(x^2+y^2)^{1/2}$, que són contínues, amb denominador no nul: és contínua.
[3] A l'origen: de $(|x|-|y|)^2\ge0$ surt $|xy|\le\frac{x^2+y^2}{2}$, d'on $|F_1(x,y)|\le\frac12(x^2+y^2)\to0=F_1(0,0)$. Per tant $F_1$ és contínua a tot $\mathbb{R}^2$.
[4] Sigui $P=\{(x,y)\mid x+y^2=0\}$. El conjunt $\mathbb{R}^2\setminus P=\{x+y^2>0\}\cup\{x+y^2<0\}$ és obert, i en ell $F_2$ coincideix amb el quocient de polinomis $\frac{x}{x+y^2}$, amb denominador no nul: $F_2$ és contínua a cada punt de $\mathbb{R}^2\setminus P$.
[5] Si $(a,b)\in P$ i $(a,b)\neq(0,0)$, aleshores $a=-b^2\neq0$ i, per a $t\neq0$, $F_2(a+t,b)=\frac{a+t}{t}$, que no és fitat quan $t\to0$. Per tant $F_2$ no és contínua en aquests punts.
[6] A l'origen, $F_2(x,0)=1$ per a $x\neq0$ i $F_2(0,y)=0$ per a $y\neq0$: els límits per aquests dos camins són diferents i $F_2$ tampoc no és contínua a $(0,0)$.
[7] Per tant el conjunt de discontinuïtats de $F$ és exactament $P=h^{-1}(\{0\})$, amb $h(x,y)=x+y^2$ contínua. Com que $\{0\}$ és compacte, la seva antiimatge $P$ és compacta i, en particular, tancada.


## t2-10:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Estudieu la continuïtat a $\mathbb{R}^2$ de la funció
$$f(x,y)=\begin{cases}\dfrac{x^3y}{x^2+y^2-1} & \text{si } x^2+y^2-1\neq0\\ 0 & \text{si } x^2+y^2-1=0.\end{cases}$$
RESULTAT CORRECTE: $f$ és contínua a $\mathbb{R}^2\setminus S$, on $S=\{x^2+y^2=1\}$, i discontínua a tots els punts de $S$. Si $(a,b)\in S$ amb $ab\neq0$, el numerador tendeix a $a^3b\neq0$ i el denominador a $0$ ($f$ no és fitada a prop). Als quatre punts $(\pm1,0)$, $(0,\pm1)$, on el numerador s'anul·la, tampoc no és contínua: $f(\pm1,y)=\pm\frac1y$ i, sobre $y=\pm\sqrt{1-x^2+x^4}$, $f=\frac{y}{x}$, no fitada.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [fora_cercle] Fora de la circumferència  (teoria: T2.18, T2.20)
     objectiu: Estudiar la continuïtat als punts on el denominador no s'anul·la.
     idea: Aquests punts formen un obert on $f$ coincideix amb un quocient de polinomis.
     detall: $U=\{x^2+y^2\neq1\}$ és obert (unió de $\{x^2+y^2<1\}$ i $\{x^2+y^2>1\}$) i a $U$ la funció és un quocient de polinomis amb denominador no nul: $f$ és contínua a cada punt de $U$.
  2. [punts_generics] Punts de la circumferència amb numerador no nul  (teoria: T2.10, T2.14)
     objectiu: Estudiar la continuïtat als punts $(a,b)$ de la circumferència on el numerador no s'anul·la.
     idea: Comparar a què tendeixen el numerador i el denominador a prop d'aquests punts, i triar un camí concret cap al punt (que no vagi per sobre la circumferència) per fer-ho explícit.
     detall: Si $a^2+b^2=1$ i $ab\neq0$, prenem $(x,y)=(1+t)(a,b)$, $t\to0$, $t\neq0$: $f=\frac{(1+t)^4a^3b}{(1+t)^2-1}=\frac{(1+t)^4a^3b}{t(2+t)}$, que no és fitat. $f$ no és contínua a $(a,b)$.
  3. [punts_especials] Els quatre punts on el numerador s'anul·la  (teoria: T2.10, T2.14)
     objectiu: Estudiar la continuïtat als punts de la circumferència on també s'anul·la el numerador.
     idea: Són $(\pm1,0)$ i $(0,\pm1)$. Busca camins cap a aquests punts sobre els quals el denominador sigui molt més petit que el numerador.
     detall: A $(1,0)$: $f(1,y)=\frac{y}{1+y^2-1}=\frac{1}{y}$ per a $y\neq0$, no fitat (anàlogament a $(-1,0)$, $f(-1,y)=-\frac1y$). A $(0,1)$: sobre $y=\sqrt{1-x^2+x^4}$ (que tendeix a $1$) el denominador val $x^4$ i $f=\frac{x^3y}{x^4}=\frac{y}{x}$, no fitat quan $x\to0$ (anàlogament a $(0,-1)$ amb $y=-\sqrt{1-x^2+x^4}$). $f$ no és contínua en cap d'aquests punts.
  4. [conclusio] Conclusió  (teoria: T2.14)
     objectiu: Resumir on és contínua $f$.
     idea: Ajuntar els tres casos.
     detall: $f$ és contínua exactament a $\{x^2+y^2\neq1\}$ i discontínua a tots els punts de la circumferència unitat.
ERRORS COMUNS:
  - [especials_continus] Conclou que als punts $(\pm1,0)$, $(0,\pm1)$ la funció és contínua perquè el numerador s'hi anul·la (o perquè sobre la circumferència i sobre rectes radials val $0$).
  - [nomes_circumferencia] Estudia el límit només movent-se per sobre la circumferència (on $f=0$) i conclou continuïtat.
  - [fora_sense_justificar] No justifica la continuïtat fora de la circumferència o no s'adona que cal que el conjunt sigui obert.

TEORIA DEL CURS QUE FA SERVIR:
[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T2.18] Corol·lari 18 (Tema 2) — Conjunts definits per desigualtats
Siguin $f,g:\mathbb{R}^n\longrightarrow\mathbb{R}$, funcions contínues. Llavors:

(i) $A=\{x\in\mathbb{R}^n:f(x)>g(x)\}$ és un conjunt obert.

(ii) $B=\{x\in\mathbb{R}^n:f(x)\geq g(x)\}$ és un conjunt tancat.

[T2.20] Proposició 20 (Tema 2) — Àlgebra de funcions contínues
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $h:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, contínues. Llavors

(i) $f+g,\ \lambda f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $\lambda\in\mathbb{R}$, són contínues;

(ii) $hf:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ és contínua;

(iii) per a $m=1$, si $g(x)\neq0\ \forall x\in\Omega$, $f/g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(iv) $\langle f,g\rangle:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(v) $\|f\|:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua.

[T2.10] Proposició 10 (Tema 2) — Límit per camins
Límit per camins. Si $F:D\subseteq\mathbb{R}^2\longrightarrow\mathbb{R}^m$ i $(a,b)\in D'$ tal que $\displaystyle\exists\lim_{(x,y)\to(a,b)}F(x,y)=L$, llavors per a tota funció real i contínua $g$ definida en un entorn d'$a$, tal que $g(a)=b$, es compleix que
$$\lim_{x\to a}F(x,g(x))=L.$$
</solucio_de_referencia>

### Document a revisar

[1] Sigui $S=\{x^2+y^2=1\}$. El conjunt $U=\mathbb{R}^2\setminus S=\{x^2+y^2<1\}\cup\{x^2+y^2>1\}$ és obert, i a $U$ la funció és un quocient de polinomis amb denominador no nul. Per tant $f$ és contínua a cada punt de $U$.
[2] Sigui $(a,b)\in S$ amb $ab\neq0$. Sobre els punts $(1+t)(a,b)$, $t\neq0$ petit, $f=\frac{(1+t)^4a^3b}{(1+t)^2-1}=\frac{(1+t)^4a^3b}{t^2}$, que no és fitat quan $t\to0$ perquè el numerador tendeix a $a^3b\neq0$. Per tant $f$ no és contínua a $(a,b)$.
[3] A $(1,0)$: per a $y\neq0$, $f(1,y)=\frac{y}{1+y^2-1}=\frac1y$, que no és fitat quan $y\to0$. Anàlogament, $f(-1,y)=-\frac1y$. Per tant $f$ no és contínua a $(\pm1,0)$.
[4] A $(0,1)$: sobre la recta $y=1$, $f(x,1)=\frac{x^3}{x^2}=x\to0$, i sobre la circumferència $f$ val $0$; com que els dos camins donen $0=f(0,1)$, $f$ és contínua a $(0,1)$, i per simetria també a $(0,-1)$.
[5] Conclusió: $f$ és contínua a $\mathbb{R}^2\setminus S$ i als punts $(0,\pm1)$, i és discontínua a la resta de punts de la circumferència unitat.


## t2-18b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $M_2(\mathbb{R})$ el conjunt de matrius quadrades $2\times2$ amb coeficients reals, que identifiquem amb $\mathbb{R}^4$ mitjançant l'aplicació $F:M_2(\mathbb{R})\longrightarrow\mathbb{R}^4$ donada per
$$F\left(\begin{pmatrix}a&c\\b&d\end{pmatrix}\right)=(a,b,c,d)^T$$

(b) Determineu si els conjunts següents són oberts, tancats o compactes:
$$C_1=\{A\in M_2(\mathbb{R})\text{ invertibles}\},\ C_2=\{A\in M_2(\mathbb{R})\mid\det A=1\},\ C_3=\{A\in M_2(\mathbb{R})\mid\det A>0\}.$$
RESULTAT CORRECTE: $C_1=\det^{-1}(\mathbb{R}\setminus\{0\})$: obert, no tancat, no compacte.
$C_2=\det^{-1}(\{1\})$: tancat, no obert, no compacte (no fitat).
$C_3=\det^{-1}((0,+\infty))$: obert, no tancat, no compacte.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [c1] Estudiar $C_1$  (teoria: T2.17, T1.19)
     objectiu: Classificar $C_1$ quant a obertura i tancament.
     idea: Escriure $C_1$ com l'antiimatge per $\det$ (contínua per l'apartat (a)) d'un subconjunt de $\mathbb{R}$, i buscar una successió de $C_1$ que convergeixi fora de $C_1$.
     detall: $C_1=\det^{-1}(\mathbb{R}\setminus\{0\})$ i $\mathbb{R}\setminus\{0\}$ és obert, per tant $C_1$ és obert (teorema 17(c) amb $\Omega=M_2(\mathbb{R})$). No és tancat: $\frac1n I\in C_1$ ($\det=\frac1{n^2}\neq0$) i $\frac1n I\to 0\notin C_1$.
  2. [c2] Estudiar $C_2$  (teoria: T2.17, T1.14)
     objectiu: Classificar $C_2$ quant a obertura i tancament.
     idea: Antiimatge per $\det$ d'un subconjunt de $\mathbb{R}$; per veure si un punt és interior, mirar matrius properes a la identitat.
     detall: $C_2=\det^{-1}(\{1\})$ amb $\{1\}$ tancat, per tant $C_2$ és tancat (teorema 17(d)). No és obert: $I\in C_2$ però $(1+\frac1n)I\to I$ i $\det\big((1+\frac1n)I\big)=(1+\frac1n)^2\neq1$; tota bola centrada a $I$ conté punts fora de $C_2$, i $I$ no és interior.
  3. [c3] Estudiar $C_3$  (teoria: T2.17, T2.18, T1.19)
     objectiu: Classificar $C_3$ quant a obertura i tancament.
     idea: Mateixa estratègia: antiimatge d'un subconjunt de $\mathbb{R}$ i, per al tancament, una successió que surti del conjunt al límit.
     detall: $C_3=\det^{-1}((0,+\infty))$ amb $(0,+\infty)$ obert, per tant $C_3$ és obert (també pel corol·lari 18(i) amb $f=\det$, $g=0$). No és tancat: $\frac1n I\in C_3$ ($\det=\frac1{n^2}>0$) i $\frac1nI\to0$, amb $\det 0=0$.
  4. [compacitat] Compacitat  (teoria: T1.27, T1.33, T1.34)
     objectiu: Decidir quins dels tres conjunts són compactes.
     idea: A $\mathbb{R}^4$, compacte equival a tancat i fitat: només cal estudiar els que són tancats, i mirar si són fitats.
     detall: $C_1$ i $C_3$ no són tancats, per tant no són compactes (compacte $\Rightarrow$ tancat). $C_2$ és tancat però no fitat: $\begin{pmatrix}n&0\\0&1/n\end{pmatrix}\in C_2$ i $\|F(A_n)\|\geq n\to\infty$ per a aquesta matriu $A_n$. Per Heine-Borel, $C_2$ no és compacte. Cap dels tres és compacte.
ERRORS COMUNS:
  - [no_obert_implica_tancat] Conclou que un conjunt és tancat perquè no és obert (o a l'inrevés).
  - [imatge_vs_antiimatge] Aplica el teorema al revés: dedueix propietats de la imatge per $\det$ en lloc de l'antiimatge, o pensa que $\det$ de tancat és tancat.
  - [tancat_implica_compacte] Diu que $C_2$ és compacte perquè és tancat.
  - [fitat_falsament] Creu que $\det A=1$ obliga les entrades a ser petites.

TEORIA DEL CURS QUE FA SERVIR:
[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.

[T1.24] Definició 24 (Tema 1) — Compacte i seqüencialment compacte
Sigui $(M,d)$ espai mètric, $A\subseteq M$.

i) $A$ és _compacte_ si tot recobriment per oberts de $A$ admet un subrecobriment finit, és a dir: si $A\subseteq\bigcup_{i\in I}U_i$, amb $U_i$ obert, aleshores existeixen $i_1,\ldots,i_k\in I$ tals que $A\subseteq\bigcup_{j=1}^k U_{i_j}$.

ii) $A$ és _seqüencialment compacte_ si tota successió $(x_n)_{n\in\mathbb{N}}\subseteq A$ admet una subsuccessió (una parcial) convergent a un punt de $A$.

[T2.17] Teorema 17 (Tema 2) — Caracteritzacions de la continuïtat
Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents:

(a) $f$ és contínua en $\Omega$;

(b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;

(c) per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$;

(d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.

[T1.19] Proposició 19 (Tema 1) — Caracterització amb successions
Sigui $(M,d)$ un espai mètric, $A\subseteq M$ i $x\in M$. Aleshores:

i) $x$ és un punt d'acumulació d'$A\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\neq x$, $a_n\in A$, tal que $x=\lim_n a_n$.

ii) $x\in\overline{A}\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\in A$ tal que $x=\lim_n a_n$.

iii) $A$ és tancat $\Leftrightarrow$ el límit de tota successió convergent d'elements d'$A$ és d'$A$.

[T1.14] Definició 14 (Tema 1) — Tipus de punts d'un conjunt
Sigui $A\subseteq M$. Aleshores:

i) Un punt $x\in A$ és _interior_ a $A$ si existeix $r>0$ tal que $B_r(x)\subseteq A$.

ii) Un punt $x\in M$ és _d'acumulació_ d'$A$ si per a tot $r>0$ es té que $B_r(x)\cap(A\setminus\{x\})\neq\varnothing$.

iii) Un punt $x\in M$ és de la frontera d'$A$, si per a tot $r>0$ es té que $B_r(x)\cap A\neq\varnothing$ i també $B_r(x)\cap A^c\neq\varnothing$.

iv) Un punt $x\in M$ és _exterior_ d'$A$ si $x$ és interior a $A^c$ (és a dir, si existeix $r>0$ tal que $B_r(x)\subseteq A^c$).

[T2.18] Corol·lari 18 (Tema 2) — Conjunts definits per desigualtats
Siguin $f,g:\mathbb{R}^n\longrightarrow\mathbb{R}$, funcions contínues. Llavors:

(i) $A=\{x\in\mathbb{R}^n:f(x)>g(x)\}$ és un conjunt obert.

(ii) $B=\{x\in\mathbb{R}^n:f(x)\geq g(x)\}$ és un conjunt tancat.

[T1.27] Lema 27 (Tema 1) — Compacte implica tancat
$A$ compacte $\Rightarrow$ $A$ tancat.

[T1.33] Definició 33 (Tema 1) — Conjunt fitat
Es diu que $A\subseteq M$ és _fitat_ si i només si existeix un $x\in M$ i un valor $L>0$ tal que $A\subseteq B_L(x)$.

[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.
</solucio_de_referencia>

### Document a revisar

[1] Via la identificació $F$, el determinant és $\det(a,b,c,d)=ad-bc$, un polinomi en les coordenades de $\mathbb{R}^4$, i per tant és una funció contínua a $M_2(\mathbb{R})$.
[2] $C_1=\det^{-1}(\mathbb{R}\setminus\{0\})$ i $\mathbb{R}\setminus\{0\}$ és obert, per tant $C_1$ és obert. No és tancat: $\frac1nI\in C_1$, perquè $\det(\frac1nI)=\frac1{n^2}\neq0$, i $\frac1nI\to0\notin C_1$.
[3] $C_2=\det^{-1}(\{1\})$ i $\{1\}$ és tancat, per tant $C_2$ és tancat. En canvi, no és obert, perquè $\{1\}$ no és un obert de $\mathbb{R}$.
[4] $C_3=\det^{-1}((0,+\infty))$ i $(0,+\infty)$ és obert, per tant $C_3$ és obert. No és tancat: $\frac1nI\in C_3$, ja que $\det(\frac1nI)=\frac1{n^2}>0$, però $\frac1nI\to0$ i $\det0=0$.
[5] Compacitat: un compacte és tancat, així que $C_1$ i $C_3$, que no són tancats, no són compactes.
[6] $C_2$ és tancat però no és fitat: les matrius $A_n=nI$ són de $C_2$ i $\|F(A_n)\|=n\sqrt2\to\infty$. Per Heine-Borel, $C_2$ tampoc no és compacte. Cap dels tres conjunts és compacte.


## t2-7c:dificil

### Referència

<solucio_de_referencia>
ENUNCIAT: Límits i coordenades polars.

(c) Discutiu l'existència de $\displaystyle\lim_{(x,y)\to(0,0)}\frac{x^py^q}{x^2+y^2-xy}$, segons els valors de $p,q\in\mathbb{N}$.
RESULTAT CORRECTE: El denominador compleix $\frac12(x^2+y^2)\le x^2+y^2-xy\le\frac32(x^2+y^2)$ (en particular, només s'anul·la a l'origen).
- Si $p+q\ge3$: el límit existeix i val $0$, ja que $|f|\le2r^{p+q-2}\to0$.
- Si $p+q=2$: sobre $y=mx$ el quocient val $\frac{m^q}{1-m+m^2}$, que depèn de $m$; el límit no existeix.
- Si $p+q\le1$ (només si $0\in\mathbb{N}$): el quocient no és fitat a prop de l'origen (per exemple $p=q=0$ dona $+\infty$; $p=1,q=0$ dona $\frac1x$ sobre $y=0$); no hi ha límit finit.
Amb el conveni $\mathbb{N}=\{1,2,\dots\}$: el límit existeix (i val $0$) si i només si $(p,q)\neq(1,1)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [denominador] Comparar el denominador amb la norma
     objectiu: Trobar fites superior i inferior del denominador en termes de $x^2+y^2$.
     idea: Fitar el terme creuat $xy$ en funció de $x^2+y^2$ (desigualtat elemental a partir d'un quadrat no negatiu).
     detall: De $(|x|-|y|)^2\ge0$ surt $|xy|\le\frac{x^2+y^2}{2}$. Per tant $\frac12(x^2+y^2)\le x^2+y^2-xy\le\frac32(x^2+y^2)$: el denominador es comporta com $r^2$ i només s'anul·la a l'origen.
  2. [grau_gran] Cas en què el numerador domina  (teoria: T2.6)
     objectiu: Determinar per a quins $p,q$ el quocient tendeix a $0$ i demostrar-ho.
     idea: Fitar el numerador per una potència de $r=\sqrt{x^2+y^2}$ i usar la fita inferior del denominador; després aplicar l'apartat (a) (fita que només depèn de $r$).
     detall: $|x^py^q|\le r^{p+q}$, de manera que $\left|\frac{x^py^q}{x^2+y^2-xy}\right|\le\frac{r^{p+q}}{r^2/2}=2r^{p+q-2}$. Si $p+q\ge3$, aquesta fita tendeix a $0$ quan $r\to0^+$ i, per l'apartat (a), el límit és $0$.
  3. [grau_petit] Casos sense límit  (teoria: T2.10)
     objectiu: Estudiar els valors de $p,q$ restants i veure si hi ha límit.
     idea: Provar les rectes $y=mx$ i mirar si el resultat depèn de $m$, o si el quocient no és fitat.
     detall: Sobre $y=mx$: $\frac{m^qx^{p+q}}{x^2(1-m+m^2)}$ (notem $1-m+m^2>0$). Si $p+q=2$, el límit és $\frac{m^q}{1-m+m^2}$, que depèn de $m$: per $(1,1)$ val $0$ per $m=0$ i $1$ per $m=1$; si $0\in\mathbb{N}$, per $(2,0)$ val $1$ per $m=0$ i $\frac13$ per $m=2$, i per $(0,2)$ val $0$ per $m=0$ i $1$ per $m=1$. No hi ha límit. Si $p+q\le1$ (cas $0\in\mathbb{N}$), el valor absolut és $\ge\frac{|x|^p|y|^q}{\frac32 r^2}$ i sobre els eixos adequats val $\frac1{x}$, $\frac1{y}$ o $\frac{1}{x^2}$: no és fitat i no hi ha límit finit.
ERRORS COMUNS:
  - [denominador_zero] Pensa que el denominador $x^2+y^2-xy$ es pot anul·lar fora de l'origen (o hi tracta com si pogués ser negatiu).
  - [polars_sense_fita] Passa a polars i obté $r^{p+q-2}\cdot\frac{\cos^p\varphi\sin^q\varphi}{1-\cos\varphi\sin\varphi}$ però no comprova que el factor angular és fitat.
  - [cas_frontera] Inclou el cas $p+q=2$ entre els que tenen límit $0$ (per exemple, pensa que $\frac{xy}{x^2+y^2-xy}$ tendeix a $0$).

TEORIA DEL CURS QUE FA SERVIR:
[T2.6] Definició 6 (Tema 2) — Límit d'una funció
Límit d'una funció. Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $\Omega$ un domini qualsevol de $M$, $x_0\in\Omega'$, $b\in\mathbb{R}^m$, i $f:\Omega\subseteq M\longrightarrow N$ una funció. Aleshores, direm que existeix el límit de $f$ quan $x$ tendeix a $x_0$ i val $b$, $\displaystyle\lim_{x\to x_0}f(x)=b$, si es dona qualsevol de les següents condicions:

(a) $\forall\epsilon>0,\exists\delta>0$ tal que $\forall x\in\Omega$ amb $0<d(x,x_0)<\delta$, es té que $d(f(x),b)<\epsilon$.

(b) Per a tot obert $\mathcal{V}$ que conté $b$, existeix un obert $\mathcal{U}$ que conté $x_0$ tal que $f\left((\mathcal{U}\setminus\{x_0\})\cap\Omega\right)\subseteq\mathcal{V}$. (Nota: Dir que $V$ és un obert que conté $A\subseteq M$, és equivalent a dir que $V$ és un entorn obert d'$A$. En aquesta situació, un conjunt que contingui $V$, s'anomena simplement entorn. En aquest curs, considerarem sempre entorns oberts. En el cas que $A=\{x\}$, denotarem amb $\mathcal{E}_{\mathbf{x}}$ el conjunt d'entorns oberts d'$x$ (abusant del llenguatge, ja que hauria de ser $\{x\}$).)

(c) Per a tota successió $(x_n)_{n\in\mathbb{N}}$ amb $x_0\neq x_n\in\Omega$ i $\displaystyle\lim_{n\to+\infty}x_n=x_0$, es té que $\displaystyle\lim_{n\to+\infty}f(x_n)=b$.

[T2.10] Proposició 10 (Tema 2) — Límit per camins
Límit per camins. Si $F:D\subseteq\mathbb{R}^2\longrightarrow\mathbb{R}^m$ i $(a,b)\in D'$ tal que $\displaystyle\exists\lim_{(x,y)\to(a,b)}F(x,y)=L$, llavors per a tota funció real i contínua $g$ definida en un entorn d'$a$, tal que $g(a)=b$, es compleix que
$$\lim_{x\to a}F(x,g(x))=L.$$
</solucio_de_referencia>

### Document a revisar

[1] Prenem el conveni $\mathbb{N}=\{1,2,\dots\}$, de manera que $p,q\geq1$ i $p+q\geq2$. Escrivim $r=\sqrt{x^2+y^2}$ i $f(x,y)=\frac{x^py^q}{x^2+y^2-xy}$.
[2] Observem que $x^2+y^2-xy=(x-y)^2+xy$; com que tots dos sumands són no negatius, el denominador només s'anul·la quan $x=y$ i $xy=0$, és a dir, a l'origen.
[3] A més, de $(|x|-|y|)^2\geq0$ surt $|xy|\leq\frac{x^2+y^2}{2}$, i per tant $\frac12r^2\leq x^2+y^2-xy\leq\frac32r^2$: el denominador es comporta com $r^2$.
[4] Com que $|x|\leq r$ i $|y|\leq r$, tenim $|x^py^q|\leq r^{p+q}$, i dividint per la fita del denominador, $|f(x,y)|\leq\frac{r^{p+q}}{\frac32r^2}=\frac23r^{p+q-2}$.
[5] Si $p+q\geq3$, aquesta fita tendeix a $0$ quan $r\to0^+$, i per tant el límit existeix i val $0$.
[6] Si $p+q=2$, és a dir, $p=q=1$: sobre la recta $y=mx$, $f(x,mx)=\frac{mx^2}{x^2(1-m+m^2)}=\frac{m}{1-m+m^2}$ (amb $1-m+m^2>0$). Per a $m=0$ dona $0$ i per a $m=1$ dona $1$: el límit depèn de la recta i no existeix.
[7] Conclusió: el límit existeix (i val $0$) si i només si $p\geq2$ i $q\geq2$; en cas contrari no existeix.

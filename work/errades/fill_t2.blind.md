## t2-2i:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Identifiqueu les corbes de nivell de les funcions següents:

(i) $$f(x,y)=\begin{cases}\dfrac{x}{x+y^2} & \text{si } x\neq-y^2\\ 0 & \text{si } x=-y^2.\end{cases}$$
RESULTAT CORRECTE: $C_0(f)=\{x=0\}\cup\{x=-y^2\}$ (l'eix $y$ i la paràbola $x=-y^2$, on $f$ val $0$ per definició).
$C_1(f)=\{(x,0)\mid x\neq0\}$ (l'eix $x$ sense l'origen).
Per a $k\neq0,1$: $C_k(f)=\{x=\frac{k}{1-k}y^2\}\setminus\{(0,0)\}$, una paràbola de vèrtex l'origen i eix l'eix $x$, sense el vèrtex; s'obre cap a $x>0$ si $0<k<1$ i cap a $x<0$ si $k<0$ o $k>1$. Hi apareixen totes les paràboles $x=cy^2$ amb $c\neq0,-1$ (sense el vèrtex); la de $c=-1$ forma part de $C_0(f)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [equacio] Equació fora de la paràbola  (teoria: T2.4)
     objectiu: Escriure la condició $f(x,y)=k$ per als punts on $f$ ve donada pel quocient.
     idea: Fora del conjunt on s'anul·la el denominador, pots multiplicar per ell; agrupa després els termes en $x$.
     detall: Si $x\neq-y^2$: $\frac{x}{x+y^2}=k\iff x=k(x+y^2)\iff x(1-k)=ky^2$.
  2. [k_u] Cas $k=1$
     objectiu: Determinar $C_1$.
     idea: Substitueix $k=1$ a l'equació obtinguda i recorda la condició d'estar fora del conjunt on el denominador s'anul·la.
     detall: Si $k=1$: $0=y^2$, és a dir $y=0$, i cal $x\neq-0^2=0$. Així $C_1$ és l'eix d'abscisses sense l'origen (i, en efecte, $f(x,0)=x/x=1$). Cap punt de la paràbola $x=-y^2$ hi és, perquè allà $f=0$.
  3. [k_zero] Cas $k=0$
     objectiu: Determinar $C_0$, tenint en compte tots els punts on $f$ val $0$.
     idea: Hi ha dues fonts de zeros: els del quocient i els punts on $f$ està definida directament.
     detall: Fora de la paràbola, $k=0$ dona $x=0$ amb $y\neq0$ (l'eix $y$ sense l'origen). Sobre la paràbola $x=-y^2$, $f=0$ per definició. Per tant $C_0=\{x=0\}\cup\{x=-y^2\}$ (l'origen hi és, perquè és de la paràbola).
  4. [k_general] Cas $k\neq 0,1$
     objectiu: Determinar $C_k$ per a la resta de valors de $k$.
     idea: Aïlla $x$ en funció de $y^2$ i reconeix la corba. Comprova si talla el conjunt on $f$ es defineix a part.
     detall: $x=\frac{k}{1-k}y^2$: paràbola de vèrtex l'origen i eix l'eix $x$. Com que $c=\frac{k}{1-k}\neq-1$ per a tot $k$, aquesta paràbola només talla $x=-y^2$ a l'origen, on $f=0\neq k$. Per tant $C_k$ és la paràbola sense l'origen. Si $0<k<1$, $c>0$ (s'obre cap a la dreta); si $k<0$, $-1<c<0$; si $k>1$, $c<-1$ (s'obre cap a l'esquerra).
ERRORS COMUNS:
  - [oblidar_definicio] Ignora la segona línia de la definició i no inclou la paràbola $x=-y^2$ a $C_0$.
  - [incloure_origen] Inclou l'origen a $C_k$ per a $k\neq0$, perquè satisfà l'equació $x(1-k)=ky^2$.
  - [dividir_per_1_menys_k] Divideix per $1-k$ sense separar el cas $k=1$.

TEORIA DEL CURS QUE FA SERVIR:
[T2.4] Definició 4 (Tema 2) — Conjunt de nivell
Donada una funció escalar $f$, es defineix el conjunt de nivell $k$ com
$$C_k(f)=\{x\in M\mid f(x)=k\}\subseteq M.$$
</solucio_de_referencia>

### Document a revisar

[1] La funció està definida a tot $\mathbb{R}^2$: fora de la paràbola $x=-y^2$ val el quocient i sobre la paràbola val $0$. Per a $x\neq-y^2$ tenim $\frac{x}{x+y^2}=k\iff x=k(x+y^2)\iff x(1-k)=ky^2$.
[2] Si $k=1$, l'equació queda $0=y^2$, és a dir $y=0$, i a més cal $x\neq-0^2=0$. Així $C_1(f)=\{(x,0)\mid x\neq0\}$, l'eix d'abscisses sense l'origen; en efecte, $f(x,0)=\frac{x}{x}=1$.
[3] Si $k=0$, fora de la paràbola l'equació dona $x=0$, i la condició $x\neq-y^2$ obliga $y\neq0$. Per tant $C_0(f)=\{(0,y)\mid y\neq0\}$, l'eix d'ordenades sense l'origen.
[4] Si $k\neq0,1$ podem dividir per $1-k$: $x=\frac{k}{1-k}y^2$, una paràbola de vèrtex l'origen i eix l'eix $x$. Com que $\frac{k}{1-k}=-1$ exigiria $k=k-1$, que és impossible, aquesta paràbola no és $x=-y^2$, i totes dues només es tallen a l'origen.
[5] L'origen compleix l'equació $x(1-k)=ky^2$, de manera que, per a $k\neq0,1$, $C_k(f)$ és tota la paràbola $x=\frac{k}{1-k}y^2$, vèrtex inclòs.
[6] Pel que fa a l'orientació, si $0<k<1$ el coeficient $\frac{k}{1-k}$ és positiu i la paràbola s'obre cap a $x>0$; si $k<0$ el coeficient és de $(-1,0)$ i si $k>1$ és menor que $-1$: en aquests dos casos s'obre cap a $x<0$.


## t2-3b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Identifiqueu les superfícies de nivell de les funcions següents:

(b) $f(x,y,z)=x^2+y^2-z^2$.
RESULTAT CORRECTE: $C_k(f)=\{x^2+y^2-z^2=k\}$. Per a $k>0$: hiperboloide d'una fulla d'eix $Oz$ (secció a l'altura $z$: circumferència de radi $\sqrt{k+z^2}$). Per a $k=0$: el con circular $x^2+y^2=z^2$ de vèrtex l'origen i eix $Oz$. Per a $k<0$: hiperboloide de dues fulles d'eix $Oz$ (només hi ha punts amb $|z|\ge\sqrt{-k}$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [equacio] Escriure el conjunt de nivell  (teoria: T2.4)
     objectiu: Escriure l'equació del conjunt de nivell $k$ i decidir quins casos de $k$ cal separar.
     idea: Aplicar la definició de conjunt de nivell i observar que el signe de $k$ pot canviar la forma de la superfície.
     detall: $C_k(f)=\{(x,y,z)\mid x^2+y^2-z^2=k\}$. Cal distingir $k>0$, $k=0$ i $k<0$.
  2. [seccions] Estudiar les seccions horitzontals
     objectiu: Descriure la intersecció de la superfície amb cada pla horitzontal $z=z_0$.
     idea: Fixar $z=z_0$ i mirar quina corba del pla $(x,y)$ queda; després observar com depèn el seu radi de $z_0$.
     detall: Amb $z=z_0$: $x^2+y^2=k+z_0^2$, circumferència de radi $\sqrt{k+z_0^2}$ (si $k+z_0^2>0$), un punt si $k+z_0^2=0$, buit si $k+z_0^2<0$. La superfície és de revolució al voltant de l'eix $Oz$.
  3. [classificar] Classificar segons el signe de k
     objectiu: Identificar la quàdrica que s'obté en cada un dels tres casos.
     idea: Mirar si totes les seccions horitzontals són no buides, si n'hi ha una que és un sol punt, o si hi ha una franja de $z$ sense punts.
     detall: $k>0$: totes les seccions són circumferències (la més petita, de radi $\sqrt{k}$, a $z=0$): hiperboloide d'una fulla. $k=0$: $x^2+y^2=z^2$, radi $|z_0|$: con de vèrtex l'origen. $k<0$: no hi ha punts per a $|z|<\sqrt{-k}$: hiperboloide de dues fulles.
ERRORS COMUNS:
  - [un_sol_cas] Dona una única descripció per a tots els $k$ sense distingir el signe.
  - [confon_fulles] Intercanvia els casos d'una i dues fulles.
  - [oblida_k0] Oblida el cas degenerat $k=0$ o el descriu com un punt.

TEORIA DEL CURS QUE FA SERVIR:
[T2.4] Definició 4 (Tema 2) — Conjunt de nivell
Donada una funció escalar $f$, es defineix el conjunt de nivell $k$ com
$$C_k(f)=\{x\in M\mid f(x)=k\}\subseteq M.$$
</solucio_de_referencia>

### Document a revisar

[1] El conjunt de nivell $k$ és $C_k(f)=\{(x,y,z)\mid x^2+y^2-z^2=k\}$. Com que el signe de $k$ pot canviar la forma de la superfície, distingim els casos $k>0$, $k=0$ i $k<0$.
[2] Tallem amb el pla $z=z_0$: queda $x^2+y^2=k+z_0^2$, que és una circumferència de centre $(0,0,z_0)$ i radi $\sqrt{k+z_0^2}$ si $k+z_0^2>0$, un sol punt si $k+z_0^2=0$ i el buit si $k+z_0^2<0$. Per tant la superfície és de revolució al voltant de l'eix $Oz$.
[3] Si $k>0$, $k+z_0^2>0$ per a tot $z_0$: totes les seccions horitzontals són circumferències, i la més petita, a $z=0$, té radi $k$. És un hiperboloide d'una fulla d'eix $Oz$.
[4] Si $k=0$, l'equació és $x^2+y^2=z^2$: la secció a l'altura $z_0$ és una circumferència de radi $|z_0|$, que es redueix a l'origen per a $z_0=0$. És el con circular de vèrtex l'origen i eix $Oz$.
[5] Si $k<0$, la secció és buida quan $z_0^2<-k$, és a dir, per a $|z_0|<\sqrt{-k}$, i és una circumferència per a $|z_0|>\sqrt{-k}$. Com que només hi ha punts amb $|z|\geq\sqrt{-k}$, la superfície és un hiperboloide d'una fulla d'eix $Oz$.


## t2-5b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Estudieu el límit a $(0,0)$ de la restricció de les funcions següents a qualsevol recta que passa per $(0,0)$ i esbrineu si existeix el límit $\lim_{(x,y)\to(0,0)}f(x,y)$ per a les funcions següents:

(b) $f(x,y)=\dfrac{xy^2}{x^2y+xy^2}$.
RESULTAT CORRECTE: El domini és $\{xy(x+y)\neq0\}$, de manera que les rectes $x=0$, $y=0$ i $y=-x$ queden fora del domini. Sobre les altres rectes, $y=mx$ amb $m\neq0,-1$, el límit és $\frac{m}{1+m}$, que depèn de $m$; per tant el límit $\lim_{(x,y)\to(0,0)}f(x,y)$ no existeix.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [domini] Domini i simplificació
     objectiu: Determinar el domini de $f$ i quines rectes per l'origen hi són contingudes (llevat de l'origen).
     idea: Factoritza el denominador; les rectes on s'anul·la no formen part del domini.
     detall: $x^2y+xy^2=xy(x+y)$. Domini: $x\neq0$, $y\neq0$, $y\neq-x$. Allà $f(x,y)=\frac{y}{x+y}$. Sobre els eixos i sobre $y=-x$ la restricció no està definida.
  2. [restriccio] Restringir a les rectes
     objectiu: Calcular el límit de $f$ sobre les rectes per l'origen que són dins del domini.
     idea: Substitueix $y=mx$ per als valors de $m$ admissibles i simplifica.
     detall: $f(x,mx)=\frac{m^2x^3}{mx^3+m^2x^3}=\frac{m}{1+m}$ ($m\neq0,-1$), constant: el límit sobre la recta és $\frac{m}{1+m}$.
  3. [concloure] Concloure sobre el límit  (teoria: T2.10)
     objectiu: Decidir si existeix el límit a $(0,0)$.
     idea: Si el límit existís, totes les restriccions a corbes contínues per l'origen dins del domini haurien de tenir el mateix límit.
     detall: Per $m=1$ el límit és $\frac12$ i per $m=2$ és $\frac23$: valors diferents, de manera que, per la proposició de límit per camins, el límit a $(0,0)$ no existeix (l'origen sí que és punt d'acumulació del domini).
ERRORS COMUNS:
  - [ignora_domini] Calcula la restricció a $x=0$ o $y=0$ com si estigués definida (p. ex. obtenint $0$ o $1$).
  - [simplificacio_global] Simplifica a $\frac{y}{x+y}$ i oblida que la funció original no està definida als eixos, o bé creu que la simplificació canvia el límit.
  - [rectes_com_a_prova] Pensa que, com que cada restricció té límit, el límit global existeix.

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

[1] Factoritzem el denominador: $x^2y+xy^2=xy(x+y)$. El domini de $f$ és, doncs, $\{(x,y)\mid x\neq0,\ y\neq0,\ x+y\neq0\}$, i en aquest domini podem simplificar: $f(x,y)=\frac{y}{x+y}$.
[2] Comencem per l'eix d'abscisses: sobre $y=0$ tenim $f(x,0)=\frac{0}{x+0}=0$, de manera que la restricció de $f$ a aquesta recta té límit $0$ quan $x\to0$.
[3] Ara les rectes $y=mx$ amb $m\neq0,-1$, que (llevat de l'origen) són dins del domini: per a $x\neq0$, $f(x,mx)=\frac{x\cdot m^2x^2}{x^2\cdot mx+x\cdot m^2x^2}=\frac{m^2x^3}{mx^3+m^2x^3}=\frac{m}{1+m^2}$.
[4] Per tant la restricció a cada una d'aquestes rectes és constant per a $x\neq0$, i el seu límit quan $x\to0$ és aquest mateix valor, que no és el mateix per a totes les $m$.
[5] L'origen és punt d'acumulació del domini. Si existís $\lim_{(x,y)\to(0,0)}f(x,y)$, per la proposició de límit per camins totes aquestes restriccions haurien de tenir el mateix límit; com que no és així, el límit $\lim_{(x,y)\to(0,0)}f(x,y)$ no existeix.


## t2-6:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Siguin $A=\left\{(x,y)\in\mathbb{R}^2\mid 0<y<x^2\right\}$ i $f(x,y)=\begin{cases}0 & \text{si } (x,y)\in A,\\ 1 & \text{altrament.}\end{cases}$

Demostreu que el límit quan $(x,y)\to(0,0)$ de la restricció de $f$ a qualsevol recta que passi per $(0,0)$ val 1; però tanmateix no existeix $\lim_{(x,y)\to(0,0)}f(x,y)$.
RESULTAT CORRECTE: Sobre la recta $x=0$ i sobre $y=0$, $f\equiv1$. Sobre $y=mx$ amb $m\neq0$, el punt $(x,mx)$ és a $A$ només si $0<mx<x^2$, cosa que exigeix $|x|>|m|$; per tant $f(x,mx)=1$ per a $0<|x|<|m|$ i el límit sobre cada recta val $1$. En canvi, sobre la paràbola $y=\frac{x^2}{2}$ (que és dins $A$ per a $x\neq0$) $f\equiv0$, i el límit sobre aquest camí val $0\neq1$. Per la proposició de límit per camins, $\lim_{(x,y)\to(0,0)}f(x,y)$ no existeix.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [rectes] Restricció a les rectes per l'origen  (teoria: T2.6)
     objectiu: Veure que, sobre cada recta que passa per $(0,0)$, la funció val $1$ en tots els punts prou propers a l'origen.
     idea: Separar la recta vertical $x=0$ de les rectes $y=mx$. Per a cada recta, esbrinar per a quins $x$ el punt de la recta satisfà les dues desigualtats que defineixen $A$.
     detall: - $x=0$: cap punt $(0,y)$ compleix $0<y<0$, així que $f(0,y)=1$.
- $y=0$: no es compleix $0<0$, així que $f(x,0)=1$.
- $y=mx$, $m>0$: cal $mx>0$ (és a dir $x>0$) i $mx<x^2$ (és a dir $x>m$). Si $m<0$: cal $x<0$ i, dividint per $x<0$, $x<m$. En tots dos casos el punt és a $A$ només si $|x|>|m|$.
Per tant, si $0<|x|<|m|$, $f(x,mx)=1$, i el límit de la restricció quan $x\to0$ és $1$ (la restricció és constant a prop de $0$).
  2. [cami_dins_A] Un camí per dins d'A  (teoria: T2.10)
     objectiu: Trobar una corba que passi per l'origen sobre la qual $f$ tingui un límit diferent de $1$.
     idea: El conjunt $A$ és la regió compresa entre l'eix $y=0$ i la paràbola $y=x^2$; cap recta no hi entra a prop de l'origen, però una corba que quedi entre aquestes dues sí que hi pot quedar.
     detall: Sobre $y=\frac{x^2}{2}$ (o $y=cx^2$ amb $0<c<1$) i $x\neq0$ es té $0<\frac{x^2}{2}<x^2$, és a dir, el punt és a $A$ i $f=0$. Per tant $\lim_{x\to0}f\left(x,\frac{x^2}{2}\right)=0$.
  3. [concloure] Concloure la no existència  (teoria: T2.10, T2.8)
     objectiu: Deduir de tot plegat que el límit doble no existeix.
     idea: Si el límit existís valdria el mateix sobre qualsevol corba contínua que passi per l'origen.
     detall: Si existís $\lim_{(x,y)\to(0,0)}f(x,y)=L$, per la proposició de límit per camins hauria de ser $L=1$ (sobre $y=0$) i també $L=0$ (sobre la paràbola de l'apartat anterior). Per unicitat del límit, això és impossible: el límit no existeix.
ERRORS COMUNS:
  - [rectes_suficients] Creu que si el límit sobre totes les rectes per l'origen val el mateix, aleshores el límit doble existeix.
  - [A_lluny_origen] Pensa que $A$ no s'acosta a l'origen (perquè cap recta hi entra) i que per tant $f=1$ en un entorn de $(0,0)$.
  - [oblida_vertical] Només estudia les rectes $y=mx$ i oblida la recta vertical $x=0$.

TEORIA DEL CURS QUE FA SERVIR:
[T2.6] Definició 6 (Tema 2) — Límit d'una funció
Límit d'una funció. Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $\Omega$ un domini qualsevol de $M$, $x_0\in\Omega'$, $b\in\mathbb{R}^m$, i $f:\Omega\subseteq M\longrightarrow N$ una funció. Aleshores, direm que existeix el límit de $f$ quan $x$ tendeix a $x_0$ i val $b$, $\displaystyle\lim_{x\to x_0}f(x)=b$, si es dona qualsevol de les següents condicions:

(a) $\forall\epsilon>0,\exists\delta>0$ tal que $\forall x\in\Omega$ amb $0<d(x,x_0)<\delta$, es té que $d(f(x),b)<\epsilon$.

(b) Per a tot obert $\mathcal{V}$ que conté $b$, existeix un obert $\mathcal{U}$ que conté $x_0$ tal que $f\left((\mathcal{U}\setminus\{x_0\})\cap\Omega\right)\subseteq\mathcal{V}$. (Nota: Dir que $V$ és un obert que conté $A\subseteq M$, és equivalent a dir que $V$ és un entorn obert d'$A$. En aquesta situació, un conjunt que contingui $V$, s'anomena simplement entorn. En aquest curs, considerarem sempre entorns oberts. En el cas que $A=\{x\}$, denotarem amb $\mathcal{E}_{\mathbf{x}}$ el conjunt d'entorns oberts d'$x$ (abusant del llenguatge, ja que hauria de ser $\{x\}$).)

(c) Per a tota successió $(x_n)_{n\in\mathbb{N}}$ amb $x_0\neq x_n\in\Omega$ i $\displaystyle\lim_{n\to+\infty}x_n=x_0$, es té que $\displaystyle\lim_{n\to+\infty}f(x_n)=b$.

[T2.10] Proposició 10 (Tema 2) — Límit per camins
Límit per camins. Si $F:D\subseteq\mathbb{R}^2\longrightarrow\mathbb{R}^m$ i $(a,b)\in D'$ tal que $\displaystyle\exists\lim_{(x,y)\to(a,b)}F(x,y)=L$, llavors per a tota funció real i contínua $g$ definida en un entorn d'$a$, tal que $g(a)=b$, es compleix que
$$\lim_{x\to a}F(x,g(x))=L.$$

[T2.8] Proposició 8 (Tema 2) — Unicitat del límit
Unicitat del límit. Si existeix $\displaystyle\lim_{x\to x_0}f(x)$, aquest és únic.
</solucio_de_referencia>

### Document a revisar

[1] Les rectes que passen per l'origen són les de la forma $y=mx$ amb $m\in\mathbb{R}$, de manera que n'hi ha prou d'estudiar la restricció de $f$ a cada una d'aquestes rectes.
[2] Si $m=0$, la recta és l'eix $y=0$ i cap dels seus punts compleix $0<0$: $f(x,0)=1$ per a tot $x$, i el límit de la restricció és $1$.
[3] Si $m>0$, el punt $(x,mx)$ és de $A$ si i només si $mx>0$ i $mx<x^2$, és a dir, $x>0$ i (dividint per $x>0$) $x>m$. Si $m<0$, cal $x<0$ i, dividint $mx<x^2$ per $x<0$, $x<m$. En tots dos casos, $(x,mx)\in A$ implica $|x|>|m|$.
[4] Per tant, per a $0<|x|<|m|$ es té $f(x,mx)=1$: la restricció és constant a prop de $x=0$ i el seu límit quan $x\to0$ és $1$.
[5] Busquem ara un camí per dins de $A$. Per a $x\neq0$, el punt $\left(x,\frac{x^2}{2}\right)$ compleix $0<\frac{x^2}{2}<x^2$, així que és de $A$ i $f\left(x,\frac{x^2}{2}\right)=0$; el mateix passa sobre qualsevol paràbola $y=cx^2$ amb $0<c\leq1$.
[6] En conseqüència, $\lim_{x\to0}f\left(x,\frac{x^2}{2}\right)=0$.
[7] Si existís $\lim_{(x,y)\to(0,0)}f(x,y)=L$, per la proposició de límit per camins hauria de ser $L=1$ (sobre l'eix $y=0$) i també $L=0$ (sobre la paràbola $y=\frac{x^2}{2}$), cosa impossible per la unicitat del límit. Per tant el límit no existeix.


## t2-8e:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem les funcions
$$f(x,y)=\begin{cases}0 & \text{si } (x,y)=(0,0),\\ \dfrac{xy^2}{x^2+y^4} & \text{altrament,}\end{cases}\qquad g(x,y)=\begin{cases}0 & \text{si } (x,y)=(0,0),\\ \dfrac{xy^2}{x^2+y^6} & \text{altrament.}\end{cases}$$
Demostreu la veracitat o falsedat de les afirmacions següents:

(e) $g$ no és contínua a $\mathbb{R}^2$ però ho és a la regió
$$D_\delta=\left\{(r\cos\varphi,r\sin\varphi)\mid r\geqslant0,\ |\cos\varphi|>\delta\right\}\qquad(0<\delta<1).$$
RESULTAT CORRECTE: Cert. $g$ no és contínua a l'origen (per (d), o perquè sobre $x=y^3$ val $\frac1{2y}$). Però $D_\delta=\{(0,0)\}\cup\{(x,y)\mid |x|>\delta\|(x,y)\|\}$ i, per a $(x,y)\in D_\delta\setminus\{(0,0)\}$, amb $r=\|(x,y)\|$: $|g(x,y)|\le\frac{|x|y^2}{x^2}=\frac{y^2}{|x|}<\frac{r^2}{\delta r}=\frac{r}{\delta}\to0$. Per tant el límit de $g|_{D_\delta}$ a l'origen és $0=g(0,0)$ i $g|_{D_\delta}$ és contínua a l'origen; als altres punts de $D_\delta$ ho és perquè $g$ ja és contínua a $\mathbb{R}^2\setminus\{(0,0)\}$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [no_continua] No continuïtat a tot el pla  (teoria: T2.14, T2.6)
     objectiu: Decidir si $g$ és contínua com a funció definida a tot $\mathbb{R}^2$.
     idea: Aprofitar l'apartat (d): una funció contínua en un punt és fitada en algun entorn d'aquest punt.
     detall: Si $g$ fos contínua a $(0,0)$, existiria $\rho>0$ amb $|g|<|g(0,0)|+1=1$ a $B((0,0),\rho)$, en contradicció amb (d). (Directament: sobre $x=y^3$, $g=\frac1{2y}\not\to0$.)
  2. [regio] Entendre la regió  (teoria: T1.14)
     objectiu: Descriure $D_\delta$ en coordenades cartesianes i veure que l'origen hi és un punt d'acumulació.
     idea: Traduir la condició sobre $\cos\varphi$ usant $x=r\cos\varphi$ i $r=\|(x,y)\|$.
     detall: Per a $r>0$, $|\cos\varphi|>\delta$ equival a $|x|>\delta\|(x,y)\|$: és un parell de sectors angulars oberts al voltant de l'eix $x$ (que no toquen l'eix $y$). Amb $r=0$ s'obté l'origen. Els punts $(t,0)$, $t\neq0$, són a $D_\delta$, així que $(0,0)\in D_\delta'$.
  3. [fita] Fitar g dins la regió
     objectiu: Esbrinar si $|g|$ admet a $D_\delta\setminus\{(0,0)\}$ una fita que només depengui de $r$ i tendeixi a $0$ amb $r$.
     idea: Dins la regió, $|x|$ és comparable a $r$; eliminar un sumand del denominador i usar aquesta comparació.
     detall: $|g(x,y)|=\frac{|x|y^2}{x^2+y^6}\le\frac{|x|y^2}{x^2}=\frac{y^2}{|x|}<\frac{r^2}{\delta r}=\frac{r}{\delta}$.
  4. [concloure] Concloure la continuïtat a la regió  (teoria: T2.14, T2.20)
     objectiu: Decidir si la restricció $g|_{D_\delta}$ és contínua a tots els punts de $D_\delta$.
     idea: Aplicar la definició de continuïtat a la funció restringida, separant l'origen dels altres punts.
     detall: Per la fita anterior, el límit de $g|_{D_\delta}$ quan $(x,y)\to(0,0)$ és $0=g(0,0)$, de manera que $g|_{D_\delta}$ és contínua a l'origen. Als altres punts de $D_\delta$, $g$ és contínua (quocient de polinomis amb denominador no nul), i per tant també ho és la restricció.
ERRORS COMUNS:
  - [confon_restriccio] Entén "contínua a $D_\delta$" com que $g$, definida a tot $\mathbb{R}^2$, és contínua a cada punt de $D_\delta$, i conclou que és fals perquè l'origen hi pertany.
  - [fita_sense_delta] Fita $|g|$ sense usar la condició $|x|>\delta r$, i obté una fita que no tendeix a $0$.
  - [oblida_origen_regio] No s'adona que l'origen pertany a $D_\delta$ (amb $r=0$) i només estudia punts amb $r>0$.

TEORIA DEL CURS QUE FA SERVIR:
[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T1.14] Definició 14 (Tema 1) — Tipus de punts d'un conjunt
Sigui $A\subseteq M$. Aleshores:

i) Un punt $x\in A$ és _interior_ a $A$ si existeix $r>0$ tal que $B_r(x)\subseteq A$.

ii) Un punt $x\in M$ és _d'acumulació_ d'$A$ si per a tot $r>0$ es té que $B_r(x)\cap(A\setminus\{x\})\neq\varnothing$.

iii) Un punt $x\in M$ és de la frontera d'$A$, si per a tot $r>0$ es té que $B_r(x)\cap A\neq\varnothing$ i també $B_r(x)\cap A^c\neq\varnothing$.

iv) Un punt $x\in M$ és _exterior_ d'$A$ si $x$ és interior a $A^c$ (és a dir, si existeix $r>0$ tal que $B_r(x)\subseteq A^c$).

[T2.6] Definició 6 (Tema 2) — Límit d'una funció
Límit d'una funció. Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $\Omega$ un domini qualsevol de $M$, $x_0\in\Omega'$, $b\in\mathbb{R}^m$, i $f:\Omega\subseteq M\longrightarrow N$ una funció. Aleshores, direm que existeix el límit de $f$ quan $x$ tendeix a $x_0$ i val $b$, $\displaystyle\lim_{x\to x_0}f(x)=b$, si es dona qualsevol de les següents condicions:

(a) $\forall\epsilon>0,\exists\delta>0$ tal que $\forall x\in\Omega$ amb $0<d(x,x_0)<\delta$, es té que $d(f(x),b)<\epsilon$.

(b) Per a tot obert $\mathcal{V}$ que conté $b$, existeix un obert $\mathcal{U}$ que conté $x_0$ tal que $f\left((\mathcal{U}\setminus\{x_0\})\cap\Omega\right)\subseteq\mathcal{V}$. (Nota: Dir que $V$ és un obert que conté $A\subseteq M$, és equivalent a dir que $V$ és un entorn obert d'$A$. En aquesta situació, un conjunt que contingui $V$, s'anomena simplement entorn. En aquest curs, considerarem sempre entorns oberts. En el cas que $A=\{x\}$, denotarem amb $\mathcal{E}_{\mathbf{x}}$ el conjunt d'entorns oberts d'$x$ (abusant del llenguatge, ja que hauria de ser $\{x\}$).)

(c) Per a tota successió $(x_n)_{n\in\mathbb{N}}$ amb $x_0\neq x_n\in\Omega$ i $\displaystyle\lim_{n\to+\infty}x_n=x_0$, es té que $\displaystyle\lim_{n\to+\infty}f(x_n)=b$.

[T2.20] Proposició 20 (Tema 2) — Àlgebra de funcions contínues
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $h:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, contínues. Llavors

(i) $f+g,\ \lambda f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $\lambda\in\mathbb{R}$, són contínues;

(ii) $hf:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ és contínua;

(iii) per a $m=1$, si $g(x)\neq0\ \forall x\in\Omega$, $f/g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(iv) $\langle f,g\rangle:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(v) $\|f\|:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua.
</solucio_de_referencia>

### Document a revisar

[1] Primer, $g$ no és contínua a l'origen: sobre la corba $x=y^3$, amb $y\neq0$, $g(y^3,y)=\frac{y^5}{y^6+y^6}=\frac{1}{2y}$, que no tendeix a $0=g(0,0)$ quan $y\to0$ (ni tan sols és fitada). Per tant $g$ no és contínua a $\mathbb{R}^2$.
[2] Per a $r>0$ tenim $x=r\cos\varphi$ i $r=\|(x,y)\|$, de manera que $|\cos\varphi|>\delta$ equival a $|x|>\delta\|(x,y)\|$; amb $r=0$ s'obté l'origen. Així $D_\delta=\{(0,0)\}\cup\{(x,y)\mid |x|>\delta\|(x,y)\|\}$: l'origen i dos sectors angulars oberts al voltant de l'eix $x$.
[3] L'origen és punt d'acumulació de $D_\delta$, ja que els punts $(0,t)$ amb $t\neq0$ hi pertanyen.
[4] Sigui $(x,y)\in D_\delta\setminus\{(0,0)\}$ i $r=\|(x,y)\|$. Com que $y^6\geq0$, $|g(x,y)|=\frac{|x|y^2}{x^2+y^6}\leq\frac{|x|y^2}{x^2}=\frac{y^2}{|x|}$.
[5] Ara, com que $y^2\leq r^2$ i $|x|\leq r$, tenim $\frac{y^2}{|x|}\leq\frac{r^2}{r}=r$, i per tant $|g(x,y)|\leq r$ per a tot $(x,y)\in D_\delta\setminus\{(0,0)\}$.
[6] Per aquesta fita, el límit de $g|_{D_\delta}$ quan $(x,y)\to(0,0)$ és $0=g(0,0)$, i la restricció és contínua a l'origen. Als altres punts de $D_\delta$, $g$ és contínua perquè és un quocient de polinomis amb denominador no nul, i per tant també ho és la restricció. L'afirmació és certa.


## t2-11:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Estudieu la continuïtat de la funció $f:\mathbb{R}^2\to\mathbb{R}$ definida per
$$f(x,y)=\frac{(x-1)^3y^2}{(x-1)^4+y^4},\quad\text{si }(x,y)\neq(1,0)\ \text{ i }\ f(1,0)=0.$$
RESULTAT CORRECTE: $f$ és contínua a tot $\mathbb{R}^2$. Fora de $(1,0)$ és un quocient de polinomis amb denominador no nul. A $(1,0)$, amb $u=x-1$: $u^2y^2\le\frac{u^4+y^4}{2}$, d'on $|f(x,y)|\le\frac{|u|}{2}=\frac{|x-1|}{2}\to0=f(1,0)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [fora] Fora del punt (1,0)  (teoria: T2.20)
     objectiu: Estudiar la continuïtat als punts diferents de $(1,0)$.
     idea: Mirar on s'anul·la el denominador i usar l'àlgebra de funcions contínues.
     detall: $(x-1)^4+y^4=0$ només si $(x,y)=(1,0)$. A l'obert $\mathbb{R}^2\setminus\{(1,0)\}$, $f$ és quocient de polinomis amb denominador no nul: contínua.
  2. [fita] Fitar a prop de (1,0)
     objectiu: Trobar una fita de $|f(x,y)-f(1,0)|$ que tendeixi a $0$ quan $(x,y)\to(1,0)$.
     idea: Traslladar el punt a l'origen ($u=x-1$) i comparar el producte $u^2y^2$ amb la suma $u^4+y^4$.
     detall: Amb $u=x-1$: de $(u^2-y^2)^2\ge0$ surt $u^2y^2\le\frac{u^4+y^4}{2}$, i llavors $|f|=\frac{|u|\,u^2y^2}{u^4+y^4}\le\frac{|u|}{2}=\frac{|x-1|}{2}$.
  3. [concloure] Concloure  (teoria: T2.6, T2.14)
     objectiu: Decidir la continuïtat al punt $(1,0)$ i donar la conclusió global.
     idea: Criteri del sandvitx amb la fita trobada i definició de continuïtat.
     detall: $0\le|f(x,y)|\le\frac{|x-1|}{2}\to0$, per tant $\lim_{(x,y)\to(1,0)}f(x,y)=0=f(1,0)$. La funció és contínua a $(1,0)$ i, per tant, a tot $\mathbb{R}^2$.
ERRORS COMUNS:
  - [camins_com_a_prova] Prova rectes $y=m(x-1)$ (totes donen $0$) i conclou la continuïtat sense una fita.
  - [grau_igual] Pensa que, com que numerador i denominador tenen grau $5$ i $4$ en "variables barrejades", el límit no existeix (confonent amb el cas $\frac{u^2y^2}{u^4+y^4}$).

TEORIA DEL CURS QUE FA SERVIR:
[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T2.20] Proposició 20 (Tema 2) — Àlgebra de funcions contínues
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $h:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, contínues. Llavors

(i) $f+g,\ \lambda f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $\lambda\in\mathbb{R}$, són contínues;

(ii) $hf:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ és contínua;

(iii) per a $m=1$, si $g(x)\neq0\ \forall x\in\Omega$, $f/g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(iv) $\langle f,g\rangle:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(v) $\|f\|:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua.

[T2.6] Definició 6 (Tema 2) — Límit d'una funció
Límit d'una funció. Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $\Omega$ un domini qualsevol de $M$, $x_0\in\Omega'$, $b\in\mathbb{R}^m$, i $f:\Omega\subseteq M\longrightarrow N$ una funció. Aleshores, direm que existeix el límit de $f$ quan $x$ tendeix a $x_0$ i val $b$, $\displaystyle\lim_{x\to x_0}f(x)=b$, si es dona qualsevol de les següents condicions:

(a) $\forall\epsilon>0,\exists\delta>0$ tal que $\forall x\in\Omega$ amb $0<d(x,x_0)<\delta$, es té que $d(f(x),b)<\epsilon$.

(b) Per a tot obert $\mathcal{V}$ que conté $b$, existeix un obert $\mathcal{U}$ que conté $x_0$ tal que $f\left((\mathcal{U}\setminus\{x_0\})\cap\Omega\right)\subseteq\mathcal{V}$. (Nota: Dir que $V$ és un obert que conté $A\subseteq M$, és equivalent a dir que $V$ és un entorn obert d'$A$. En aquesta situació, un conjunt que contingui $V$, s'anomena simplement entorn. En aquest curs, considerarem sempre entorns oberts. En el cas que $A=\{x\}$, denotarem amb $\mathcal{E}_{\mathbf{x}}$ el conjunt d'entorns oberts d'$x$ (abusant del llenguatge, ja que hauria de ser $\{x\}$).)

(c) Per a tota successió $(x_n)_{n\in\mathbb{N}}$ amb $x_0\neq x_n\in\Omega$ i $\displaystyle\lim_{n\to+\infty}x_n=x_0$, es té que $\displaystyle\lim_{n\to+\infty}f(x_n)=b$.
</solucio_de_referencia>

### Document a revisar

[1] El denominador $(x-1)^4+y^4$ només s'anul·la si $x=1$ i $y=0$. A l'obert $\mathbb{R}^2\setminus\{(1,0)\}$, $f$ és quocient de polinomis amb denominador no nul, i per tant hi és contínua.
[2] Estudiem el punt $(1,0)$. Posem $u=x-1$, de manera que $(x,y)\to(1,0)$ equival a $(u,y)\to(0,0)$ i $f(x,y)=\frac{u^3y^2}{u^4+y^4}$.
[3] De la desigualtat $(u^2+y^2)^2\geq0$ surt $u^2y^2\leq\frac{u^4+y^4}{2}$.
[4] Aleshores, per a $(x,y)\neq(1,0)$, $|f(x,y)|=\frac{|u|\,u^2y^2}{u^4+y^4}\leq\frac{|u|}{2}=\frac{|x-1|}{2}$.
[5] I com que $|x-1|\leq\|(x,y)\|$, tenim $0\leq|f(x,y)|\leq\frac{\|(x,y)\|}{2}\to0$ quan $(x,y)\to(1,0)$.
[6] Per tant $\lim_{(x,y)\to(1,0)}f(x,y)=0=f(1,0)$: $f$ és contínua a $(1,0)$ i, juntament amb el primer pas, és contínua a tot $\mathbb{R}^2$.


## t2-12b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem la funció $f:\mathbb{R}^2\to\mathbb{R}$ definida per
$$f(x,y)=\begin{cases}\dfrac{x^2+y^2}{x+y} & \text{si } x+y\neq0,\\ 0 & \text{si } x+y=0.\end{cases}$$

(b) Escriviu les equacions de les corbes de nivell $0$, $2$ i $-2$ de $f$. Dibuixeu-les.
RESULTAT CORRECTE: - $C_0$: la recta $x+y=0$ (incloent-hi l'origen); fora d'ella el numerador $x^2+y^2$ no s'anul·la.
- $C_2$: $(x-1)^2+(y-1)^2=2$ menys l'origen; circumferència de centre $(1,1)$ i radi $\sqrt2$, sense el punt $(0,0)$.
- $C_{-2}$: $(x+1)^2+(y+1)^2=2$ menys l'origen; circumferència de centre $(-1,-1)$ i radi $\sqrt2$, sense $(0,0)$.
Totes dues circumferències passen per l'origen i hi són tangents a la recta $x+y=0$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [nivell0] Corba de nivell 0  (teoria: T2.4)
     objectiu: Determinar el conjunt de punts on $f$ val $0$.
     idea: Separar els punts on $f$ es defineix pel quocient dels punts on es defineix com $0$.
     detall: Si $x+y\neq0$, $f=0$ exigeix $x^2+y^2=0$, és a dir $(0,0)$, que no compleix $x+y\neq0$. Per tant $C_0=\{x+y=0\}$: és tota la recta $y=-x$.
  2. [nivell_k] Corbes de nivell 2 i -2  (teoria: T2.4)
     objectiu: Escriure les equacions de $C_2$ i $C_{-2}$ i identificar-les.
     idea: Plantejar $x^2+y^2=k(x+y)$ amb $x+y\neq0$ i completar quadrats; comprovar quins punts de la corba obtinguda no compleixen $x+y\neq0$.
     detall: $x^2+y^2=2(x+y)\iff(x-1)^2+(y-1)^2=2$: circumferència de centre $(1,1)$ i radi $\sqrt2$. La intersecció amb $x+y=0$: $(x-1)^2+(x+1)^2=2\iff x=0$, és a dir, només l'origen, que cal treure. Anàlogament $x^2+y^2=-2(x+y)\iff(x+1)^2+(y+1)^2=2$, centre $(-1,-1)$, radi $\sqrt2$, sense l'origen.
  3. [dibuix] Dibuix
     objectiu: Dibuixar les tres corbes i observar com es disposen a prop de l'origen.
     idea: Situar centres i radis i mirar per quin punt passen totes.
     detall: Les dues circumferències són simètriques respecte de l'origen, passen per $(0,0)$ (on hi ha un forat) i en aquest punt són tangents a la recta $x+y=0$ (el radi des de $(1,1)$ fins a $(0,0)$ és perpendicular a la recta). En general, $C_k$ ($k\neq0$) és la circumferència de centre $(\frac k2,\frac k2)$ i radi $\frac{|k|}{\sqrt2}$ menys l'origen.
ERRORS COMUNS:
  - [oblida_forat] No treu l'origen de les circumferències (on $f$ val $0$ per definició).
  - [nivell0_buit] Diu que $C_0$ és buit o només l'origen, perquè $x^2+y^2=0$ només a l'origen, oblidant la definició a trossos.
  - [quadrats] S'equivoca completant quadrats (radi $2$ en lloc de $\sqrt2$, o centre mal situat).

TEORIA DEL CURS QUE FA SERVIR:
[T2.4] Definició 4 (Tema 2) — Conjunt de nivell
Donada una funció escalar $f$, es defineix el conjunt de nivell $k$ com
$$C_k(f)=\{x\in M\mid f(x)=k\}\subseteq M.$$
</solucio_de_referencia>

### Document a revisar

[1] Nivell $0$: si $x+y\neq0$, $f(x,y)=0$ exigeix $x^2+y^2=0$, és a dir $(x,y)=(0,0)$, que no compleix $x+y\neq0$; per tant no hi ha cap punt fora de la recta. Sobre la recta $x+y=0$, $f=0$ per definició.
[2] Així $C_0=\{(x,y)\mid x+y=0\}$: és tota la recta $y=-x$, l'origen inclòs.
[3] Nivell $2$: si $x+y\neq0$, $\frac{x^2+y^2}{x+y}=2\iff x^2+y^2=2(x+y)\iff(x-1)^2+(y-1)^2=2$, la circumferència de centre $(1,1)$ i radi $2$.
[4] Aquesta circumferència talla la recta $x+y=0$ on $(x-1)^2+(-x-1)^2=2$, és a dir, $2x^2+2=2$, $x=0$: només a l'origen. Allà $f=0\neq2$, de manera que $C_2$ és la circumferència sense l'origen.
[5] Nivell $-2$: $x^2+y^2=-2(x+y)\iff(x+1)^2+(y+1)^2=2$, la circumferència de centre $(-1,-1)$ i radi $\sqrt2$. Tots els seus punts compleixen aquesta equació, així que $C_{-2}$ és tota la circumferència.
[6] Per al dibuix: les dues circumferències són simètriques respecte de l'origen, hi passen totes dues i en aquest punt són tangents a la recta $x+y=0$, perquè el radi que va de $(1,1)$ a $(0,0)$ té la direcció $(1,1)$, perpendicular a la recta.


## t2-13b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Raoneu si són oberts els subconjunts de $\mathbb{R}^2$ o $\mathbb{R}^3$ següents:

(b) $B=\{(x,y)\in\mathbb{R}^2\ \mid\ xy\log\left(x-y\right)>5\}$.
RESULTAT CORRECTE: $B$ és obert. La funció $f(x,y)=xy\log(x-y)$ és contínua al seu domini $\Omega=\{x>y\}$, que és obert; aleshores $B=f^{-1}((5,+\infty))=U\cap\Omega$ amb $U$ obert de $\mathbb{R}^2$, intersecció de dos oberts.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [domini] Domini de la funció  (teoria: T2.18)
     objectiu: Determinar on està definida la funció que apareix a la condició de $B$, i quin tipus de conjunt és aquest domini.
     idea: El logaritme només està definit per arguments positius; el domini resultant també és un conjunt definit per una desigualtat entre funcions contínues.
     detall: $f(x,y)=xy\log(x-y)$ està definida a $\Omega=\{(x,y)\in\mathbb{R}^2: x>y\}$. Com que $(x,y)\mapsto x$ i $(x,y)\mapsto y$ són contínues a $\mathbb{R}^2$, $\Omega$ és obert (desigualtat estricta entre funcions contínues). En particular $B\subseteq\Omega$.
  2. [continuitat] Continuïtat a $\Omega$  (teoria: T2.19, T2.20)
     objectiu: Justificar on és contínua la funció que defineix $B$.
     idea: Producte i composició de funcions contínues; el logaritme és continu a $(0,+\infty)$.
     detall: $(x,y)\mapsto x-y$ és contínua i pren valors a $(0,+\infty)$ sobre $\Omega$, on $\log$ és contínua; la composició $\log(x-y)$ és contínua a $\Omega$, i multiplicada pel polinomi $xy$ dona $f$ contínua a $\Omega$.
  3. [concloure] Antiimatge d'un obert  (teoria: T2.17, T2.x4, T1.12)
     objectiu: Deduir si $B$ és obert de $\mathbb{R}^2$ (no només dins del domini).
     idea: La caracterització topològica de la continuïtat dona l'antiimatge d'un obert com la intersecció d'un obert de l'espai amb el domini; cal combinar-ho amb el caràcter del domini.
     detall: $B=f^{-1}((5,+\infty))$ i $(5,+\infty)$ és obert de $\mathbb{R}$. Per la caracterització de la continuïtat, existeix $U\subseteq\mathbb{R}^2$ obert amb $B=U\cap\Omega$. Com que $\Omega$ és obert, $B$ és intersecció finita d'oberts, i per tant és obert de $\mathbb{R}^2$.
ERRORS COMUNS:
  - [oblida_domini] Aplica el corol·lari de les desigualtats com si $f$ fos contínua a tot $\mathbb{R}^2$, sense mirar el domini del logaritme.
  - [domini_no_obert_irrellevant] Creu que l'antiimatge d'un obert per una funció contínua és sempre oberta, sigui quin sigui el domini.
  - [confon_signe_log] Posa com a domini $x-y\ge 0$ o $x-y>1$ (confusió amb el signe o el valor del logaritme).

TEORIA DEL CURS QUE FA SERVIR:
[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.

[T2.18] Corol·lari 18 (Tema 2) — Conjunts definits per desigualtats
Siguin $f,g:\mathbb{R}^n\longrightarrow\mathbb{R}$, funcions contínues. Llavors:

(i) $A=\{x\in\mathbb{R}^n:f(x)>g(x)\}$ és un conjunt obert.

(ii) $B=\{x\in\mathbb{R}^n:f(x)\geq g(x)\}$ és un conjunt tancat.

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

[T2.17] Teorema 17 (Tema 2) — Caracteritzacions de la continuïtat
Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents:

(a) $f$ és contínua en $\Omega$;

(b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;

(c) per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$;

(d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.

[T2.x4] Apunts del Tema 2, §2.3 — Comentari sobre el corol·lari 18
Observem que, en el corol·lari 18, si les funcions només estiguessin definides en un conjunt $\Omega\subseteq\mathbb{R}^n$, només podríem afirmar que $A=U\cap\Omega$, on $U$ és un obert de $\mathbb{R}^n$. En el cas que $\Omega$ fos un obert de $\mathbb{R}^n$, aleshores $A$ també seria un obert de $\mathbb{R}^n$. Anàlogament per a $B$ canviant "obert" per "tancat".

Els següents resultats ens asseguren que, de manera genèrica, les combinacions i composicions de funcions contínues donen lloc a funcions contínues.

[T1.12] Proposició 12 (Tema 1) — Propietats dels conjunts oberts
(Propietats dels conjunts oberts.) Sigui $(M,d)$ un espai mètric. Aleshores,

i) tota bola oberta $B_r(x)$ és un conjunt obert;

ii) la unió arbitrària (finita o infinita) d'oberts és un obert;

iii) la intersecció finita d'oberts és un obert;

iv) $M$ i $\varnothing$ són conjunts oberts.
</solucio_de_referencia>

### Document a revisar

[1] La funció $f(x,y)=xy\log(x-y)$ només està definida on $x-y>0$, és a dir, a $\Omega=\{(x,y)\in\mathbb{R}^2\mid x>y\}$. En particular $B\subseteq\Omega$ i $B=f^{-1}((5,+\infty))$.
[2] El conjunt $\Omega$ és obert: si $(x_0,y_0)\in\Omega$ i $d=x_0-y_0>0$, tota la bola de centre $(x_0,y_0)$ i radi $d$ està continguda a $\Omega$.
[3] La funció $(x,y)\mapsto x-y$ és contínua i, sobre $\Omega$, pren valors a $(0,+\infty)$, on $\log$ és contínua; per tant $\log(x-y)$ és contínua a $\Omega$, i també ho és $f$, producte d'aquesta funció pel polinomi $xy$.
[4] Com que $(5,+\infty)$ és obert de $\mathbb{R}$ i $f$ és contínua, la caracterització topològica de la continuïtat ens diu directament que $f^{-1}((5,+\infty))$ és un obert de $\mathbb{R}^2$, sigui quin sigui el domini de $f$.
[5] Per tant $B$ és un subconjunt obert de $\mathbb{R}^2$.


## t2-14b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Anàlogament, raoneu si són tancats els subconjunts de $\mathbb{R}^2$ o $\mathbb{R}^3$ següents:

(b) $B=\{(x,y)\in\mathbb{R}^2\ \mid\ 2x^2+3y^2\in\mathbb{N}\}$.
RESULTAT CORRECTE: $B$ és tancat: $B=f^{-1}(\mathbb{N})$ amb $f(x,y)=2x^2+3y^2$ contínua a tot $\mathbb{R}^2$, i $\mathbb{N}$ és tancat de $\mathbb{R}$ (el seu complementari és una unió d'intervals oberts). L'antiimatge d'un tancat per una funció contínua a tot $\mathbb{R}^2$ és tancada.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [antiimatge] Escriure $B$ com a antiimatge  (teoria: T2.20)
     objectiu: Expressar $B$ en termes d'una funció i d'un subconjunt de $\mathbb{R}$.
     idea: La condició diu que el valor d'una funció pertany a un cert conjunt de nombres reals.
     detall: Amb $f(x,y)=2x^2+3y^2$, polinòmica i per tant contínua a $\mathbb{R}^2$, es té $B=f^{-1}(\mathbb{N})$.
  2. [n_tancat] $\mathbb{N}$ dins de $\mathbb{R}$  (teoria: T1.12, T1.11)
     objectiu: Decidir quin tipus de subconjunt de $\mathbb{R}$ és $\mathbb{N}$.
     idea: Mirar el complementari de $\mathbb{N}$ a $\mathbb{R}$ i escriure'l com a unió de conjunts coneguts.
     detall: $\mathbb{R}\setminus\mathbb{N}=(-\infty,1)\cup\bigcup_{n\ge1}(n,n+1)$ (o $(-\infty,0)\cup\bigcup_{n\ge0}(n,n+1)$ si $0\in\mathbb{N}$), unió d'intervals oberts, i per tant obert. Així $\mathbb{N}$ és tancat de $\mathbb{R}$.
  3. [concloure] Antiimatge d'un tancat  (teoria: T2.17)
     objectiu: Concloure si $B$ és tancat de $\mathbb{R}^2$.
     idea: Caracterització de la continuïtat amb antiimatges de tancats, quan el domini és tot l'espai.
     detall: Per la caracterització topològica de la continuïtat, $f^{-1}(\mathbb{N})=F\cap\mathbb{R}^2=F$ amb $F$ tancat de $\mathbb{R}^2$. Per tant $B$ és tancat.
ERRORS COMUNS:
  - [unio_infinita] Veu $B$ com la unió de les el·lipses $\{2x^2+3y^2=n\}$ i conclou que és tancat perquè "la unió de tancats és tancada", o bé que no ho és perquè la unió és infinita.
  - [n_no_tancat] Pensa que $\mathbb{N}$ no és tancat perquè no és un interval o perquè no és fitat.
  - [confon_imatge_antiimatge] Usa que la imatge (en lloc de l'antiimatge) d'un tancat per una funció contínua és tancada.

TEORIA DEL CURS QUE FA SERVIR:
[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.

[T2.20] Proposició 20 (Tema 2) — Àlgebra de funcions contínues
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $h:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, contínues. Llavors

(i) $f+g,\ \lambda f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $\lambda\in\mathbb{R}$, són contínues;

(ii) $hf:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ és contínua;

(iii) per a $m=1$, si $g(x)\neq0\ \forall x\in\Omega$, $f/g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(iv) $\langle f,g\rangle:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(v) $\|f\|:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua.

[T1.12] Proposició 12 (Tema 1) — Propietats dels conjunts oberts
(Propietats dels conjunts oberts.) Sigui $(M,d)$ un espai mètric. Aleshores,

i) tota bola oberta $B_r(x)$ és un conjunt obert;

ii) la unió arbitrària (finita o infinita) d'oberts és un obert;

iii) la intersecció finita d'oberts és un obert;

iv) $M$ i $\varnothing$ són conjunts oberts.

[T2.17] Teorema 17 (Tema 2) — Caracteritzacions de la continuïtat
Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents:

(a) $f$ és contínua en $\Omega$;

(b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;

(c) per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$;

(d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.
</solucio_de_referencia>

### Document a revisar

[1] Considerem $f(x,y)=2x^2+3y^2$, que és polinòmica i, per tant, contínua a tot $\mathbb{R}^2$. Aleshores $B=f^{-1}(\mathbb{N})$.
[2] $\mathbb{N}=\{1,2,3,\dots\}$ és tancat de $\mathbb{R}$: el seu complementari és $\mathbb{R}\setminus\mathbb{N}=(-\infty,1)\cup\bigcup_{n\geq1}(n,n+1)$, unió d'intervals oberts, i per tant obert.
[3] Geomètricament, per a cada $n\in\mathbb{N}$ el conjunt $\{f=n\}$ és l'el·lipse $\frac{x^2}{n/2}+\frac{y^2}{n/3}=1$, de semieixos $\sqrt{2n}$ i $\sqrt{3n}$.
[4] Així $B=\bigcup_{n\geq1}\{f=n\}$ és una unió d'el·lipses, que són conjunts tancats; com que la unió de qualsevol família de tancats és tancada, això ja permet concloure que $B$ és tancat.
[5] També ho podem veure amb la continuïtat: per la caracterització topològica, l'antiimatge per $f$, contínua a tot $\mathbb{R}^2$, del tancat $\mathbb{N}$ és un tancat de $\mathbb{R}^2$. Per tant $B$ és tancat.


## t2-16a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Per a $A,B\subset\mathbb{R}^n$, recordem que $d(A,B)=\inf\{d(a,b)\mid a\in A,\ b\in B\}$, on $d(a,b)$ és la distància euclídia a $\mathbb{R}^n$ (vegeu l'exercici 5 del Tema 1). Demostreu:

(a) $A,B$ compactes $\Rightarrow\exists a_0\in A,\,b_0\in B$ tals que $d(A,B)=d(a_0,b_0)$,
RESULTAT CORRECTE: Si $A,B$ són compactes (no buits), existeixen $a_0\in A$, $b_0\in B$ amb $d(A,B)=d(a_0,b_0)$. Prova: per la definició d'ínfim hi ha $a_k\in A$, $b_k\in B$ amb $d(a_k,b_k)\to d(A,B)$; per compacitat seqüencial, passant a parcials, $a_{k_j}\to a_0\in A$ i $b_{k_j}\to b_0\in B$; com que $|d(a,b)-d(a',b')|\le d(a,a')+d(b,b')$, $d(a_{k_j},b_{k_j})\to d(a_0,b_0)$, i per unicitat del límit $d(a_0,b_0)=d(A,B)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [successio_minimitzant] Successió minimitzant
     objectiu: Traduir la definició de $d(A,B)$ com a ínfim en l'existència de parelles de punts de $A$ i $B$ adequades.
     idea: Propietat de l'ínfim: per a cada $\varepsilon>0$, hi ha elements del conjunt a distància menor que $\varepsilon$ de l'ínfim. Prendre $\varepsilon=1/k$.
     detall: Sigui $\delta=d(A,B)$. Per a cada $k\ge1$, $\delta+1/k$ no és fita inferior de $\{d(a,b)\}$, de manera que existeixen $a_k\in A$, $b_k\in B$ amb $\delta\le d(a_k,b_k)<\delta+1/k$. Així $d(a_k,b_k)\to\delta$.
  2. [parcials] Extreure parcials convergents  (teoria: T1.26, T1.24)
     objectiu: Obtenir punts candidats $a_0\in A$ i $b_0\in B$ a partir de les successions anteriors.
     idea: Compacte equival a seqüencialment compacte. Cal extreure parcials en dues etapes, perquè els índexs de les dues successions coincideixin.
     detall: Per Bolzano-Weierstrass, $A$ és seqüencialment compacte: hi ha una parcial $a_{k_j}\to a_0\in A$. La successió $(b_{k_j})_j\subseteq B$ té, per la mateixa raó, una parcial $b_{k_{j_l}}\to b_0\in B$; la corresponent $a_{k_{j_l}}$ continua convergint a $a_0$. Reanomenant, tenim una parcial comuna amb $a_{k_j}\to a_0$, $b_{k_j}\to b_0$.
  3. [pas_al_limit] Passar al límit  (teoria: T1.5)
     objectiu: Comprovar que $d(a_0,b_0)=d(A,B)$.
     idea: Veure que la distància és contínua en les dues variables usant la desigualtat triangular, i aplicar la unicitat del límit.
     detall: Per la desigualtat triangular, $|d(a,b)-d(a',b')|\le d(a,a')+d(b,b')$. Per tant $|d(a_{k_j},b_{k_j})-d(a_0,b_0)|\le d(a_{k_j},a_0)+d(b_{k_j},b_0)\to0$, i $d(a_{k_j},b_{k_j})\to d(a_0,b_0)$. Com que també tendeix a $\delta$ (és parcial d'una successió que hi tendeix), $d(a_0,b_0)=\delta=d(A,B)$.
ERRORS COMUNS:
  - [parcials_independents] Extreu una parcial convergent de $(a_k)$ i una altra, amb índexs diferents, de $(b_k)$, i les combina com si fossin la mateixa subsuccessió.
  - [continuitat_no_justificada] Afirma que $d(a_{k_j},b_{k_j})\to d(a_0,b_0)$ sense justificar la continuïtat de la distància en les dues variables.
  - [inf_es_min] Suposa d'entrada que l'ínfim s'assoleix (confon ínfim amb mínim).

TEORIA DEL CURS QUE FA SERVIR:
[T1.5] Definició 5 (Tema 1) — Distància
Sigui $M$ un conjunt. Una funció $d(\cdot,\cdot):M\times M\longrightarrow\mathbb{R}$ es diu que és una _distància_ si per a tot $x,y,z\in M$, es compleixen:

i) $d(x,y)\geq 0$; $d(x,y)=0\iff x=y$.

ii) $d(x,y)=d(y,x)$ (simètrica).

iii) $d(x,y)\leq d(x,z)+d(z,y)$ (desigualtat triangular).

Direm en aquest cas que $(M,d)$ és un _espai mètric_.

[T1.24] Definició 24 (Tema 1) — Compacte i seqüencialment compacte
Sigui $(M,d)$ espai mètric, $A\subseteq M$.

i) $A$ és _compacte_ si tot recobriment per oberts de $A$ admet un subrecobriment finit, és a dir: si $A\subseteq\bigcup_{i\in I}U_i$, amb $U_i$ obert, aleshores existeixen $i_1,\ldots,i_k\in I$ tals que $A\subseteq\bigcup_{j=1}^k U_{i_j}$.

ii) $A$ és _seqüencialment compacte_ si tota successió $(x_n)_{n\in\mathbb{N}}\subseteq A$ admet una subsuccessió (una parcial) convergent a un punt de $A$.

[T1.26] Teorema 26 (Tema 1) — Teorema de Bolzano-Weierstrass
(Bolzano-Weierstrass.) Sigui $(M,d)$ espai mètric i $A\subseteq M$. Aleshores:
$A$ és compacte $\Leftrightarrow$ $A$ és seqüencialment compacte.
</solucio_de_referencia>

### Document a revisar

[1] Suposem $A,B$ no buits i sigui $\delta=d(A,B)$. Per a cada $k\geq1$, $\delta+\frac1k$ no és fita inferior de $\{d(a,b)\mid a\in A,\ b\in B\}$, així que existeixen $a_k\in A$, $b_k\in B$ amb $\delta\leq d(a_k,b_k)<\delta+\frac1k$. Per tant $d(a_k,b_k)\to\delta$.
[2] Com que $A$ és compacte, per Bolzano-Weierstrass és seqüencialment compacte: la successió $(a_k)$ té una parcial $a_{k_j}\to a_0\in A$.
[3] Anàlogament, $B$ és seqüencialment compacte i $(b_k)$ té una parcial $b_{k_j}\to b_0\in B$, de manera que al llarg de la mateixa successió d'índexs $k_j$ tenim $a_{k_j}\to a_0$ i $b_{k_j}\to b_0$.
[4] Per la desigualtat triangular, $|d(a,b)-d(a',b')|\leq d(a,a')\,d(b,b')$, i per tant $|d(a_{k_j},b_{k_j})-d(a_0,b_0)|\leq d(a_{k_j},a_0)\,d(b_{k_j},b_0)\to0$, és a dir, $d(a_{k_j},b_{k_j})\to d(a_0,b_0)$.
[5] D'altra banda, $(d(a_{k_j},b_{k_j}))_j$ és una parcial de $(d(a_k,b_k))_k$, que tendeix a $\delta$, i per tant també tendeix a $\delta$. Per la unicitat del límit, $d(a_0,b_0)=\delta=d(A,B)$, amb $a_0\in A$ i $b_0\in B$.


## t2-17a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $E$ un subespai vectorial de $\mathbb{R}^m$.

(a) Demostreu que si $E$ té punts interiors, llavors existeix una bola oberta centrada a l'origen i continguda a $E$.
RESULTAT CORRECTE: Si $p\in E$ és interior, existeix $r>0$ amb $B(p,r)\subseteq E$. Aleshores $B(0,r)\subseteq E$: si $\|x\|<r$, llavors $p+x\in B(p,r)\subseteq E$ i, com que $E$ és subespai i $p\in E$, $x=(p+x)-p\in E$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [hipotesi] Escriure la hipòtesi  (teoria: T1.14, T1.11)
     objectiu: Escriure amb precisió què vol dir que $E$ tingui un punt interior.
     idea: Aplicar la definició de punt interior: hi ha una bola al voltant del punt continguda al conjunt.
     detall: Existeixen $p\in E$ i $r>0$ tals que $B(p,r)=\{y\in\mathbb{R}^m:\|y-p\|<r\}\subseteq E$.
  2. [traslladar] Traslladar la bola a l'origen  (teoria: T1.11)
     objectiu: Relacionar els punts de la bola centrada a l'origen amb els de la bola centrada al punt interior.
     idea: Una translació conserva les distàncies: sumar un vector fix porta boles de radi $r$ en boles de radi $r$.
     detall: Si $x\in B(0,r)$, és a dir $\|x\|<r$, llavors $\|(p+x)-p\|=\|x\|<r$, per tant $p+x\in B(p,r)\subseteq E$.
  3. [subespai] Usar l'estructura de subespai
     objectiu: Deduir que tot punt de la bola centrada a l'origen és de $E$.
     idea: Un subespai vectorial és tancat per diferències (combinacions lineals) dels seus elements.
     detall: Com que $p\in E$ i $p+x\in E$, i $E$ és subespai, $x=(p+x)-p\in E$. Per tant $B(0,r)\subseteq E$, amb el mateix radi $r$.
ERRORS COMUNS:
  - [suposa_0_interior] Suposa directament que $0$ és punt interior perquè $0\in E$, sense fer servir el punt interior donat.
  - [oblida_subespai] Trasllada la bola però no justifica per què els punts traslladats tornen a ser de $E$ (no usa que $E$ és subespai).
  - [radi_canvia] Creu que el radi de la nova bola ha de ser diferent (més petit) que el de la bola original, o no l'especifica.

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
</solucio_de_referencia>

### Document a revisar

[1] Sigui $p\in E$ un punt interior de $E$: existeix $r>0$ tal que $B(p,r)=\{y\in\mathbb{R}^m\mid\|y-p\|<r\}\subseteq E$.
[2] Veurem que $B(0,r)\subseteq E$. Sigui, doncs, $x\in\mathbb{R}^m$ amb $\|x\|<r$.
[3] Com que $\|(x-p)-p\|=\|x\|<r$, el punt $x-p$ és de $B(p,r)$, i per tant $x-p\in E$.
[4] Com que $E$ és un subespai i $x-p\in E$, multiplicant per l'escalar $-1$ obtenim $x\in E$.
[5] Per tant tot $x$ amb $\|x\|<r$ és de $E$: la bola oberta $B(0,r)$, centrada a l'origen i amb el mateix radi $r$, està continguda a $E$.


## t2-19a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Volem demostrar que el conjunt $O_2(\mathbb{R})=\{A\in M_2(\mathbb{R})\,:\,A^T\cdot A=I\}$ és un compacte de $M_2(\mathbb{R})$.

(a) Useu la funció $g:M_2(\mathbb{R})\to M_2(\mathbb{R})$, tal que $g(A)=A\cdot A^T$, per demostrar que $O_2(\mathbb{R})$ és tancat.

Indicació: Comentaris: els resultats anteriors es poden generalitzar al cas $M_n(\mathbb{R})$, $n\in\mathbb{N}$.
El conjunt $O_2(\mathbb{R})$, amb l'operació producte de matrius, s'anomena grup ortogonal de dimensió 2. Els seus elements són les matrius ortogonals i ens descriuen els girs i les simetries al pla.
RESULTAT CORRECTE: Per a matrius quadrades, $A^TA=I\Leftrightarrow AA^T=I$ (la inversa per l'esquerra és també per la dreta), per tant $O_2(\mathbb{R})=g^{-1}(\{I\})$. Amb $A=\begin{pmatrix}a&c\\b&d\end{pmatrix}$, $g(A)=\begin{pmatrix}a^2+c^2&ab+cd\\ab+cd&b^2+d^2\end{pmatrix}$: les components de $g$ (via $F$) són polinomis, per tant $g$ és contínua. Com que $\{I\}$ és tancat, $g^{-1}(\{I\})$ és tancat.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [reescriure] Expressar $O_2(\mathbb{R})$ amb $g$
     objectiu: Expressar $O_2(\mathbb{R})$ en termes de la funció $g$.
     idea: La definició usa $A^T A$ i $g$ usa $AA^T$: cal relacionar les dues condicions. Per a matrius quadrades, una inversa per l'esquerra és també inversa per la dreta.
     detall: Si $A^TA=I$, aleshores $(\det A)^2=\det(A^T)\det A=1$, de manera que $A$ és invertible i $A^T=A^T(AA^{-1})=(A^TA)A^{-1}=A^{-1}$; per tant també $AA^T=I$. Recíprocament, si $AA^T=I$, el mateix argument dona $A^T=A^{-1}$ i $A^TA=I$. Per tant $O_2(\mathbb{R})=\{A:g(A)=I\}=g^{-1}(\{I\})$.
  2. [g_continua] Continuïtat de $g$  (teoria: T2.20, T2.27, T2.28)
     objectiu: Justificar que $g$ és contínua.
     idea: Calcular $g(A)$ en coordenades: cada component és un polinomi en $a,b,c,d$, i una funció vectorial és contínua si ho són les seves components.
     detall: $g(A)=\begin{pmatrix}a^2+c^2&ab+cd\\ab+cd&b^2+d^2\end{pmatrix}$, és a dir, $F\circ g\circ F^{-1}(a,b,c,d)=(a^2+c^2,\,ab+cd,\,ab+cd,\,b^2+d^2)$. Les coordenades $a,b,c,d$ són funcions lineals de $\mathbb{R}^4$, per tant contínues (exemple 27 i proposició 28); cada component $h_i$ és suma de productes de coordenades, contínua per la proposició 20(i)(ii). Aleshores $F\circ g\circ F^{-1}=\sum_{i=1}^4 h_i\,e_i$ és contínua, també per la proposició 20(i)(ii) (funció escalar contínua per un vector constant, i sumes); per tant $g$ és contínua.
  3. [tancat] Antiimatge d'un tancat  (teoria: T2.17)
     objectiu: Concloure que $O_2(\mathbb{R})$ és tancat.
     idea: Caracterització de la continuïtat per tancats, amb la funció definida a tot l'espai.
     detall: Un punt $\{I\}$ és tancat a $M_2(\mathbb{R})\cong\mathbb{R}^4$. Pel teorema 17(d) amb $\Omega=M_2(\mathbb{R})$, $g^{-1}(\{I\})=D$ és tancat. Per tant $O_2(\mathbb{R})$ és tancat.
ERRORS COMUNS:
  - [confon_AtA_AAt] Escriu $O_2(\mathbb{R})=g^{-1}(\{I\})$ sense observar que la definició usa $A^TA$ i $g$ usa $AA^T$.
  - [antiimatge_de_quin] No identifica quin conjunt tancat del codomini es pren (o pren l'antiimatge d'un conjunt que no és tancat).
  - [continuitat_g] Afirma que $g$ és contínua sense justificar-ho, o diu que és lineal.

TEORIA DEL CURS QUE FA SERVIR:
[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.

[T2.20] Proposició 20 (Tema 2) — Àlgebra de funcions contínues
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $h:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, contínues. Llavors

(i) $f+g,\ \lambda f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $\lambda\in\mathbb{R}$, són contínues;

(ii) $hf:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ és contínua;

(iii) per a $m=1$, si $g(x)\neq0\ \forall x\in\Omega$, $f/g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(iv) $\langle f,g\rangle:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(v) $\|f\|:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua.

[T2.27] Exemple 27 (Tema 2) — Aplicacions lineals són Lipschitz
Tota aplicació lineal $f:\mathbb{R}^n\to\mathbb{R}^m$ és de Lipschitz.

En efecte, considerem $f(x)=Ax$, amb $x=(x_1,\dots,x_n)^t$ i $A=(a_{i,j})_{i=1,\dots,m;j=1,\dots,n}$. Denotem amb $c_j=(a_{1,j},\dots,a_{m,j})^t$ la $j$-èsima columna de $A$ i definim la norma $\|A\|_{=}\max_j\{\|c_j\|\}$, a partir de la norma $\ell_1$ de vectors ($\|v\|_1=\sum_{j=1}^m|v_j|$). (Nota: Al final del tema es fa un repàs de normes equivalents, normes de vectors i normes de matrus. En particular, seguint la definició 36, a l'exemple 37 veurem que $\|A\|_1$ és una norma subordinada a la normal vectorial $\|v\|_1$ i que, per tant, és consistent i $\|A(x-y)\|_1\leq\|A\|_1\|x-y\|_1$. Directament, veiem, doncs, que l'aplicació lineal és Lipschitz amb $C=1$.)

Per a un parell de punts qualssevol $x,y\in\mathbb{R}^n$, ometent el subíndex $1$ de les normes, tenim que:
$$\begin{aligned}\|f(x)-f(y)\|&=\|Ax-Ay\|=\|A(x-y)\|=\Big\|A\sum_{i=1}^n(x_i-y_i)e_i\Big\|=\Big\|\sum_{i=1}^n(x_i-y_i)A\,e_i\Big\|\\&=\Big\|\sum_{i=1}^n(x_i-y_i)c_i\Big\|\leq\sum_{i=1}^n|x_i-y_i|\,\|c_i\|\leq\sum_{i=1}^n|x_i-y_i|\,\|A\|\\&\leq n\,\|x-y\|\,\|A\|=C\|x-y\|,\end{aligned}$$
amb $C=n\|A\|$ i, per tant, $f$ és Lipschitz.

[T2.28] Proposició 28 (Tema 2) — Lipschitz, uniforme i contínua
Lipschitz $\Rightarrow$ uniformement contínua $\Rightarrow$ contínua. Els recíprocs són falsos.

[T2.17] Teorema 17 (Tema 2) — Caracteritzacions de la continuïtat
Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents:

(a) $f$ és contínua en $\Omega$;

(b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;

(c) per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$;

(d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.
</solucio_de_referencia>

### Document a revisar

[1] La definició de $O_2(\mathbb{R})$ usa $A^TA=I$, mentre que $g(A)=AA^T$; per escriure $O_2(\mathbb{R})$ com una antiimatge de $g$, primer cal veure que totes dues condicions són equivalents.
[2] Si $A^TA=I$, prenent determinants, $(\det A)^2=\det(A^T)\det A=\det I=1$, d'on $\det A=1$. Per tant $A$ és invertible i $A^T=A^T(AA^{-1})=(A^TA)A^{-1}=A^{-1}$, de manera que també $AA^T=I$.
[3] Recíprocament, si $AA^T=I$, el mateix argument (intercanviant els papers de $A$ i $A^T$) dona $A^T=A^{-1}$ i $A^TA=I$. Per tant $O_2(\mathbb{R})=\{A\mid g(A)=I\}=g^{-1}(\{I\})$.
[4] Amb $A=\begin{pmatrix}a&c\\b&d\end{pmatrix}$, tenim $g(A)=AA^T=\begin{pmatrix}a^2+c^2&ac+bd\\ac+bd&b^2+d^2\end{pmatrix}$.
[5] Identificant $M_2(\mathbb{R})\cong\mathbb{R}^4$, cada component de $g$ és una suma de productes de les coordenades $a,b,c,d$, que són funcions lineals i per tant contínues; per tant cada component és contínua i $g$ és contínua.
[6] El conjunt $\{I\}$, un sol punt, és tancat a $M_2(\mathbb{R})\cong\mathbb{R}^4$. Per la caracterització topològica de la continuïtat (amb domini tot $M_2(\mathbb{R})$), $g^{-1}(\{I\})$ és tancat. Per tant $O_2(\mathbb{R})$ és tancat.


## t2-20:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Doneu un exemple de dues funcions $f,g:A\subset\mathbb{R}^m\to\mathbb{R}$ uniformement contínues, tals que el producte $h=f\cdot g$ no ho sigui.
RESULTAT CORRECTE: $m=1$, $A=\mathbb{R}$, $f(x)=g(x)=x$. $f$ és uniformement contínua (amb $\delta=\varepsilon$), però $h(x)=x^2$ no ho és: per a $\varepsilon=1$ i qualsevol $\delta>0$, $x=\frac1\delta$, $y=\frac1\delta+\frac\delta2$ compleixen $|x-y|<\delta$ i $|x^2-y^2|=\frac\delta2\left(\frac2\delta+\frac\delta2\right)=1+\frac{\delta^2}4\geq1$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [on_buscar] On buscar l'exemple  (teoria: T2.25)
     objectiu: Entendre quina característica han de tenir $f$ i $g$ perquè el producte pugui deixar de ser uniformement continu.
     idea: Mirar què passa si $f$ i $g$ són fitades: estimar $|f(x)g(x)-f(y)g(y)|$ sumant i restant un terme creuat. Si això ja dona continuïtat uniforme, l'exemple ha de tenir funcions no fitades (domini no fitat).
     detall: Si $|f|,|g|\leq K$: $|fg(x)-fg(y)|\leq K|f(x)-f(y)|+K|g(x)-g(y)|$, i $h$ seria uniformement contínua. Cal, doncs, funcions no fitades: la més senzilla és la identitat $f(x)=g(x)=x$ a $A=\mathbb{R}$.
  2. [f_uniforme] Les funcions són uniformement contínues  (teoria: T2.25)
     objectiu: Demostrar que les funcions triades són uniformement contínues.
     idea: Aplicar la definició: trobar un $\delta$ que només depengui de $\varepsilon$.
     detall: Per a $f(x)=x$: donat $\varepsilon>0$, prenem $\delta=\varepsilon$; si $|x-y|<\delta$, $|f(x)-f(y)|=|x-y|<\varepsilon$.
  3. [negacio] Negar la continuïtat uniforme del producte  (teoria: T2.25)
     objectiu: Escriure què cal demostrar per veure que $h$ no és uniformement contínua.
     idea: Negar la definició amb els quantificadors en ordre: existeix un $\varepsilon$ per al qual cap $\delta$ funciona.
     detall: Cal: $\exists\varepsilon>0$ tal que $\forall\delta>0$ $\exists x,y\in A$ amb $|x-y|<\delta$ i $|h(x)-h(y)|\geq\varepsilon$.
  4. [parells] Construir els parells de punts  (teoria: T2.25)
     objectiu: Per a cada $\delta>0$, trobar dos punts propers on $h$ prengui valors allunyats.
     idea: Factoritzar la diferència de valors de $h$: un factor és $|x-y|$ i l'altre creix amb la mida dels punts. Prendre punts lluny de l'origen, tant més lluny com més petit sigui $\delta$.
     detall: $\varepsilon=1$, $x=\frac1\delta$, $y=\frac1\delta+\frac\delta2$: $|x-y|=\frac\delta2<\delta$ i $|x^2-y^2|=|x-y|\,|x+y|=\frac\delta2\left(\frac2\delta+\frac\delta2\right)=1+\frac{\delta^2}4\geq1$.
ERRORS COMUNS:
  - [domini_fitat] Proposa funcions sobre un domini compacte o fitat (per exemple $[0,1]$), on el producte acaba sent uniformement continu.
  - [quantificadors] Nega malament la definició: tria $\delta$ concret i troba punts, o fa dependre $\varepsilon$ de $\delta$.
  - [punts_fixos] Mostra que la diferència de valors és gran per a uns punts fixos, sense que s'acostin quan $\delta\to0$.
  - [no_continu] Proposa funcions que no són uniformement contínues (per exemple $1/x$ a $(0,1)$) com a $f$ o $g$.

TEORIA DEL CURS QUE FA SERVIR:
[T2.25] Definició 25 (Tema 2) — Continuïtat uniforme
Una funció $f:\Omega\subseteq M\to N$ és uniformement contínua si $\forall\epsilon>0\ \exists\delta>0$ t.q. $\forall x,y\in\Omega$, $d(x,y)<\delta$ tenim que $d'(f(x),f(y))<\epsilon$.
</solucio_de_referencia>

### Document a revisar

[1] Si $f$ i $g$ fossin fitades, $|f|,|g|\leq K$, tindríem $|f(x)g(x)-f(y)g(y)|\leq|f(x)|\,|g(x)-g(y)|+|g(y)|\,|f(x)-f(y)|\leq K|g(x)-g(y)|+K|f(x)-f(y)|$, i el producte seria uniformement continu.
[2] Per tant, per trobar un exemple, n'hi ha prou que alguna de les dues funcions no sigui fitada. La tria més senzilla és $m=1$, $A=\mathbb{R}$ i $f(x)=g(x)=x$.
[3] La funció $f(x)=x$ és uniformement contínua: donat $\varepsilon>0$, prenem $\delta=\varepsilon$, i si $|x-y|<\delta$ aleshores $|f(x)-f(y)|=|x-y|<\varepsilon$. El mateix val per a $g=f$.
[4] Hem de veure que $h(x)=x^2$ no és uniformement contínua, és a dir: existeix $\varepsilon>0$ tal que per a tot $\delta>0$ existeixen $x,y\in\mathbb{R}$ amb $|x-y|<\delta$ i $|h(x)-h(y)|\geq\varepsilon$.
[5] Prenem $\varepsilon=1$ i, donat $\delta>0$, $x=\frac1\delta$ i $y=\frac1\delta+\frac\delta2$. Aleshores $|x-y|=\frac\delta2<\delta$ i $|x^2-y^2|=|x-y|\,|x+y|=\frac\delta2\left(\frac2\delta+\frac\delta2\right)=1+\frac{\delta^2}{2}\geq1$.
[6] Per tant, per a $\varepsilon=1$ cap $\delta>0$ no serveix: $h=f\cdot g$ no és uniformement contínua, tot i que $f$ i $g$ ho són.


## t2-21a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Siguin $F:\mathbb{R}^m\to\mathbb{R}^n$ una funció contínua i $A\subseteq\mathbb{R}^m$ un conjunt fitat.

(a) Demostreu que $\overline{F(A)}\subseteq F(\overline{A})$.
RESULTAT CORRECTE: $\overline A$ és tancat i fitat (si $A\subseteq B(x,L)$, aleshores $\overline A\subseteq\overline B(x,L)$), per tant compacte per Heine-Borel. Com que $F$ és contínua, $F(\overline A)$ és compacte i, per tant, tancat. Com que $F(A)\subseteq F(\overline A)$ i $\overline{F(A)}$ és el tancat més petit que conté $F(A)$, $\overline{F(A)}\subseteq F(\overline A)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [clausura_compacta] L'adherència d'$A$ és compacta  (teoria: T1.16, T1.13, T1.17, T1.33, T1.34)
     objectiu: Obtenir una propietat forta de $\overline{A}$ a partir de la fitació d'$A$.
     idea: Veure que $\overline A$ és tancat i fitat, i aplicar Heine-Borel.
     detall: $\overline A$ és tancat. Si $A\subseteq B(x,L)\subseteq\overline B(x,L)$, que és tancat, aleshores $\overline A\subseteq\overline B(x,L)\subseteq B(x,L+1)$: $\overline A$ és fitat. Per Heine-Borel, $\overline A$ és compacte.
  2. [imatge] La imatge és tancada  (teoria: T2.21, T1.27)
     objectiu: Deduir una propietat topològica de $F(\overline A)$.
     idea: La imatge contínua d'un compacte és compacta, i els compactes són tancats.
     detall: Per la proposició 21(i), $F(\overline A)$ és compacte; pel lema 27 del Tema 1, és tancat.
  3. [concloure] Concloure la inclusió  (teoria: T1.17, T1.16)
     objectiu: Comparar $\overline{F(A)}$ amb $F(\overline A)$.
     idea: Usar que l'adherència d'un conjunt és el tancat més petit que el conté.
     detall: $A\subseteq\overline A\Rightarrow F(A)\subseteq F(\overline A)$, i $F(\overline A)$ és tancat; per tant $\overline{F(A)}\subseteq\overline{F(\overline A)}=F(\overline A)$.
ERRORS COMUNS:
  - [inclusio_inversa] Demostra (o creu demostrar) la inclusió contrària $F(\overline A)\subseteq\overline{F(A)}$, que és la que val sempre per continuïtat.
  - [no_usa_fitat] Fa una demostració que no usa que $A$ és fitat (i que, per tant, no pot ser correcta, vegeu l'apartat (b)).
  - [continua_tanca] Afirma que una funció contínua envia tancats a tancats.
  - [subsuccessio] Amb successions: pren $y_n=F(x_n)\to y$ i suposa que $(x_n)$ convergeix, sense extreure una parcial.

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

[T1.33] Definició 33 (Tema 1) — Conjunt fitat
Es diu que $A\subseteq M$ és _fitat_ si i només si existeix un $x\in M$ i un valor $L>0$ tal que $A\subseteq B_L(x)$.

[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T1.13] Proposició 13 (Tema 1) — Propietats dels conjunts tancats
Sigui $M$ un conjunt i $d$ una distància definida sobre ell. Considereu la topologia sobre $M$ induïda per $d$. Aleshores:

i) les boles tancades de $M$ són conjunts tancats.

ii) La intersecció arbitrària de tancats és un tancat.

iii) La unió finita de tancats és un tancat.

iv) $M$ i $\varnothing$ són conjunts tancats.

[T1.17] Proposició 17 (Tema 1) — Propietats de la clausura
Les següents afirmacions són certes:

i) $A\subseteq B\Rightarrow\overline{A}\subseteq\overline{B}$.

ii) $A$ és tancat $\Leftrightarrow\overline{A}=A$.

iii) $\overline{A\cup B}=\overline{A}\cup\overline{B}$.

iv) $\overline{A\cap B}\subseteq\overline{A}\cap\overline{B}$.

[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.

[T2.21] Proposició 21 (Tema 2) — Imatge contínua de compactes i connexos
Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $f:\Omega\subseteq M\to N$ contínua i $K\subseteq\Omega$. Aleshores,

(i) $K$ compacte $\Rightarrow f(K)$ compacte;

(ii) $K$ connex $\Rightarrow f(K)$ connex.

[T1.27] Lema 27 (Tema 1) — Compacte implica tancat
$A$ compacte $\Rightarrow$ $A$ tancat.
</solucio_de_referencia>

### Document a revisar

[1] L'adherència $\overline A$ és sempre un conjunt tancat.
[2] Com que $A$ és fitat, existeixen $x\in\mathbb{R}^m$ i $L>0$ amb $A\subseteq B(x,L)$, i aleshores també $\overline A\subseteq B(x,L)$; per tant $\overline A$ és fitat.
[3] Així $\overline A$ és tancat i fitat a $\mathbb{R}^m$, i pel teorema de Heine-Borel és compacte.
[4] Com que $F$ és contínua, la imatge del compacte $\overline A$ és compacta, i un compacte de $\mathbb{R}^n$ és tancat: $F(\overline A)$ és tancat.
[5] D'altra banda, $A\subseteq\overline A$ implica $F(A)\subseteq F(\overline A)$. Com que $\overline{F(A)}$ és el tancat més petit que conté $F(A)$ i $F(\overline A)$ és un tancat que el conté, obtenim $\overline{F(A)}\subseteq F(\overline A)$.
[6] Observem, finalment, que la hipòtesi que $A$ és fitat només ha servit per simplificar l'argument: la inclusió $\overline{F(A)}\subseteq F(\overline A)$ és vàlida per a qualsevol $A\subseteq\mathbb{R}^m$.


## t2-22:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $f:\mathbb{R}^2\to\mathbb{R}$ definida per
$$f(x,y)=\begin{cases}0 & \text{si } y\neq0\\ 1+x^2 & \text{si } y=0.\end{cases}$$
Demostreu que $f$ no és contínua trobant un $A\subseteq\mathbb{R}$ tancat tal que $f^{-1}(A)$ no sigui tancat.
Escriviu el resultat teòric que utilitzeu, i demostreu explícitament que $f^{-1}(A)$ no és tancat.
RESULTAT CORRECTE: Teorema 17 ((a)$\Leftrightarrow$(d)) amb $\Omega=\mathbb{R}^2$: $f$ contínua $\Leftrightarrow$ $f^{-1}(E)$ tancat per a tot tancat $E\subseteq\mathbb{R}$. Prenem $A=\{0\}$ (tancat): com que $1+x^2\neq0$, $f^{-1}(\{0\})=\{(x,y):y\neq0\}$. No és tancat: $(0,\frac1n)\in f^{-1}(\{0\})$ i $(0,\frac1n)\to(0,0)\notin f^{-1}(\{0\})$. Per tant $f$ no és contínua.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [teorema] Resultat teòric  (teoria: T2.17)
     objectiu: Enunciar el resultat que relaciona la continuïtat amb antiimatges de tancats, adaptat a una funció definida a tot $\mathbb{R}^2$.
     idea: Caracterització de la continuïtat per tancats (teorema de caracteritzacions de la continuïtat), amb $\Omega=\mathbb{R}^2$.
     detall: Teorema 17, (a)$\Leftrightarrow$(d): $f:\mathbb{R}^2\to\mathbb{R}$ és contínua si i només si per a tot tancat $E\subseteq\mathbb{R}$, $f^{-1}(E)=D\cap\mathbb{R}^2=D$ és tancat. Per tant, n'hi ha prou de trobar un tancat amb antiimatge no tancada.
  2. [triar_A] Triar el tancat
     objectiu: Triar un tancat $A\subseteq\mathbb{R}$ i calcular $f^{-1}(A)$.
     idea: Mirar els valors que pren $f$ i escollir un tancat que capturi només una de les dues "branques" de la definició, de manera que l'antiimatge sigui un conjunt obert gran de $\mathbb{R}^2$.
     detall: $A=\{0\}$, tancat a $\mathbb{R}$. Com que $1+x^2\geq1\neq0$, $f(x,y)=0\Leftrightarrow y\neq0$; per tant $f^{-1}(\{0\})=\{(x,y)\in\mathbb{R}^2:y\neq0\}$, el pla sense l'eix $OX$.
  3. [no_tancat] Demostrar que l'antiimatge no és tancada  (teoria: T1.19)
     objectiu: Demostrar explícitament que $f^{-1}(A)$ no és tancat.
     idea: Caracterització dels tancats per successions: trobar una successió del conjunt que convergeixi a un punt de fora.
     detall: $p_n=(0,\frac1n)\in f^{-1}(\{0\})$ i $p_n\to(0,0)$, però $f(0,0)=1\neq0$, de manera que $(0,0)\notin f^{-1}(\{0\})$. Per la proposició 19(iii) del Tema 1, $f^{-1}(\{0\})$ no és tancat. Per tant $f$ no és contínua.
ERRORS COMUNS:
  - [tancat_trivial] Tria un tancat com $A=[1,+\infty)$ o $A=\{1\}$, l'antiimatge del qual (l'eix $OX$ o un punt) sí que és tancada.
  - [obert_no_tancat] Justifica que l'antiimatge no és tancada dient només que és oberta.
  - [imatge_en_lloc_antiimatge] Treballa amb imatges $f(B)$ de tancats de $\mathbb{R}^2$ en lloc d'antiimatges.

TEORIA DEL CURS QUE FA SERVIR:
[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.

[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

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
</solucio_de_referencia>

### Document a revisar

[1] Usem el teorema 17, (a)$\Leftrightarrow$(d), amb $\Omega=\mathbb{R}^2$: $f$ és contínua si i només si, per a tot tancat $E\subseteq\mathbb{R}$, $f^{-1}(E)$ és un tancat de $\mathbb{R}^2$. N'hi ha prou, doncs, de trobar un tancat amb antiimatge no tancada.
[2] Prenem $A=\{0\}$, que és tancat a $\mathbb{R}$. Com que $1+x^2\geq1$, mai no s'anul·la, de manera que $f(x,y)=0$ si i només si $y\neq0$.
[3] Per tant $f^{-1}(\{0\})=\{(x,y)\in\mathbb{R}^2\mid y\neq0\}$, el pla sense l'eix $OX$.
[4] Aquest conjunt és obert, perquè és el complementari de l'eix $OX$, que és tancat; i per ser obert ja no pot ser tancat.
[5] Ho comprovem explícitament: els punts $p_n=\left(\frac1n,0\right)$ són de $f^{-1}(\{0\})$ i $p_n\to(0,0)$, però $f(0,0)=1+0^2=1\neq0$, de manera que $(0,0)\notin f^{-1}(\{0\})$.
[6] Per la proposició 19(iii) del Tema 1, un conjunt que no conté el límit d'una successió convergent de punts seus no és tancat. Per tant $f^{-1}(\{0\})$ no és tancat i $f$ no és contínua.


## t2-23a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Certes o falses? Per a cada afirmació, demostreu-la si és certa o doneu-ne un contraexemple justificat si és falsa. A tots els apartats, $f:\mathbb{R}^2\to\mathbb{R}$.

(a) Si existeixen els dos límits iterats $\displaystyle\lim_{x\to0}\lim_{y\to0}f(x,y)$ i $\displaystyle\lim_{y\to0}\lim_{x\to0}f(x,y)$ i són iguals, aleshores existeix $\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$.
RESULTAT CORRECTE: Falsa. Contraexemple: $f(x,y)=\frac{xy}{x^2+y^2}$ si $(x,y)\neq(0,0)$, $f(0,0)=0$. Els dos límits iterats existeixen i valen $0$, però sobre la recta $y=mx$ el límit és $\frac{m}{1+m^2}$, que depèn de $m$; per tant no existeix el límit a $(0,0)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [decidir] Decidir i triar un candidat  (teoria: T2.12)
     objectiu: Decidir si l'afirmació és certa o falsa i, si cal un contraexemple, triar una funció candidata.
     idea: La teoria només dona una implicació: si hi ha límit doble (i existeixen els límits interiors), els iterats hi coincideixen. Per refutar el recíproc cal una funció que es comporti bé sobre els eixos (així els iterats coincideixen) però que, acostant-se a l'origen per alguna altra corba, doni un valor diferent.
     detall: És falsa. Un candidat: $f(x,y)=\frac{xy}{x^2+y^2}$ si $(x,y)\neq(0,0)$, $f(0,0)=0$. Val $0$ sobre tots dos eixos, però no és constant sobre les rectes per l'origen.
  2. [iterats] Calcular els límits iterats
     objectiu: Comprovar que, per a la funció triada, els dos límits iterats existeixen i són iguals.
     idea: Fixar una variable, distingint si el valor fixat és $0$ o no, i calcular el límit d'una variable en l'altra; després fer tendir a $0$ la variable fixada.
     detall: Fixat $y\neq0$: $\lim_{x\to0}\frac{xy}{x^2+y^2}=\frac{0}{y^2}=0$. Fixat $y=0$: $f(x,0)=0$ per a tot $x$, i el límit és $0$. Per tant $\lim_{x\to0}f(x,y)=0$ per a tot $y$ i $\lim_{y\to0}\lim_{x\to0}f(x,y)=0$. Per simetria, $\lim_{x\to0}\lim_{y\to0}f(x,y)=0$.
  3. [no_limit] Veure que no hi ha límit doble  (teoria: T2.10)
     objectiu: Demostrar que la funció triada no té límit a $(0,0)$.
     idea: Si el límit existís, la restricció a qualsevol corba contínua que passi per l'origen hauria de tendir al mateix valor. N'hi ha prou de trobar una família de corbes on el límit depengui de la corba.
     detall: Sobre $y=mx$: $f(x,mx)=\frac{mx^2}{x^2+m^2x^2}=\frac{m}{1+m^2}$ per a $x\neq0$, que depèn de $m$ (val $0$ per $m=0$ i $\frac{1}{2}$ per $m=1$). Per la proposició del límit per camins, no existeix $\lim_{(x,y)\to(0,0)}f(x,y)$.
ERRORS COMUNS:
  - [iterats_impliquen_limit] Creu que si els dos iterats coincideixen el límit doble existeix (confon el resultat de la teoria amb el seu recíproc).
  - [iterat_mal_calculat] En calcular un iterat fa tendir les dues variables a $0$ alhora, o oblida el cas en què el valor fixat és $0$.
  - [contraexemple_no_compleix_hipotesi] Proposa una funció on els iterats són diferents (per exemple $\frac{x^2-y^2}{x^2+y^2}$) o on no existeixen: no compleix la hipòtesi de l'afirmació.

TEORIA DEL CURS QUE FA SERVIR:
[T2.6] Definició 6 (Tema 2) — Límit d'una funció
Límit d'una funció. Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $\Omega$ un domini qualsevol de $M$, $x_0\in\Omega'$, $b\in\mathbb{R}^m$, i $f:\Omega\subseteq M\longrightarrow N$ una funció. Aleshores, direm que existeix el límit de $f$ quan $x$ tendeix a $x_0$ i val $b$, $\displaystyle\lim_{x\to x_0}f(x)=b$, si es dona qualsevol de les següents condicions:

(a) $\forall\epsilon>0,\exists\delta>0$ tal que $\forall x\in\Omega$ amb $0<d(x,x_0)<\delta$, es té que $d(f(x),b)<\epsilon$.

(b) Per a tot obert $\mathcal{V}$ que conté $b$, existeix un obert $\mathcal{U}$ que conté $x_0$ tal que $f\left((\mathcal{U}\setminus\{x_0\})\cap\Omega\right)\subseteq\mathcal{V}$. (Nota: Dir que $V$ és un obert que conté $A\subseteq M$, és equivalent a dir que $V$ és un entorn obert d'$A$. En aquesta situació, un conjunt que contingui $V$, s'anomena simplement entorn. En aquest curs, considerarem sempre entorns oberts. En el cas que $A=\{x\}$, denotarem amb $\mathcal{E}_{\mathbf{x}}$ el conjunt d'entorns oberts d'$x$ (abusant del llenguatge, ja que hauria de ser $\{x\}$).)

(c) Per a tota successió $(x_n)_{n\in\mathbb{N}}$ amb $x_0\neq x_n\in\Omega$ i $\displaystyle\lim_{n\to+\infty}x_n=x_0$, es té que $\displaystyle\lim_{n\to+\infty}f(x_n)=b$.

[T2.12] Proposició 12 (Tema 2) — Límits iterats
Límits iterats. Sigui $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}^m$ i $(a,b)\in\Omega$ t.q. $(a-\eta,a+\eta)\times(b-\eta,b+\eta)\subseteq\Omega$ per a $\eta>0$. Suposem que $\lim_{(x,y)\to(a,b)}f(x,y)=L$ i $\forall x\in(a-\eta,a+\eta)\ \exists\lim_{y\to b}f(x,y)$, i $\forall y\in(b-\eta,b+\eta)\ \exists\lim_{x\to a}f(x,y)$. Llavors,
$$\lim_{x\to a}\lim_{y\to b}f(x,y)=L=\lim_{y\to b}\lim_{x\to a}f(x,y).$$

[T2.10] Proposició 10 (Tema 2) — Límit per camins
Límit per camins. Si $F:D\subseteq\mathbb{R}^2\longrightarrow\mathbb{R}^m$ i $(a,b)\in D'$ tal que $\displaystyle\exists\lim_{(x,y)\to(a,b)}F(x,y)=L$, llavors per a tota funció real i contínua $g$ definida en un entorn d'$a$, tal que $g(a)=b$, es compleix que
$$\lim_{x\to a}F(x,g(x))=L.$$

[T2.13] Exemple 13 (Tema 2) — Límits iterats sense límit
Considerem la funció
$$f(x,y)=\begin{cases}\dfrac{x\,y}{x^2+y^2}, & (x,y)\neq(0,0),\\ 0, & (x,y)=(0,0).\end{cases}$$
D'entrada, $\lim_{x\to0}\lim_{y\to0}f(x,y)=\lim_{y\to0}\lim_{x\to0}f(x,y)=0$. En efecte, si fixem $y$, $\lim_{x\to0}f(x,y)=0$, tant si $y=0$ ($f(x,y)=0$) com si $y\neq0$, ja que
$$\lim_{x\to0}\frac{x\,y}{x^2+y^2}=\frac{0}{y^2}=0.$$
Per tant, $\lim_{y\to0}\lim_{x\to0}f(x,y)=0$. Per simetria, $\lim_{x\to0}\lim_{y\to0}f(x,y)=0$.
En canvi, si prenem $y=m\,x$, amb $m\in\mathbb{R}$,
$$\lim_{x\to0}\frac{x\,y}{x^2+y^2}=\lim_{x\to0}\frac{m\,x^2}{x^2+m^2\,x^2}=\frac{m}{1+m^2},$$
que depèn de $m$ i, per tant, no es compleix que existeixi $\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$.

[T2.x3] Apunts del Tema 2, §2.2 — El recíproc no és cert
Observem, no obstant, que el recíproc no és cert.
</solucio_de_referencia>

### Document a revisar

[1] L'afirmació és falsa. De fet, el que diu la teoria és el recíproc: si existeix el límit doble, aleshores existeixen els dos límits iterats i hi coincideixen.
[2] Contraexemple: $f(x,y)=\frac{xy}{x^2+y^2}$ si $(x,y)\neq(0,0)$ i $f(0,0)=0$. Val $0$ sobre tots dos eixos.
[3] Fixat $y\neq0$, $\lim_{x\to0}\frac{xy}{x^2+y^2}=\frac{0}{y^2}=0$, i fixat $y=0$, $f(x,0)=0$ per a tot $x$. Per tant $\lim_{x\to0}f(x,y)=0$ per a tot $y$, i $\lim_{y\to0}\lim_{x\to0}f(x,y)=0$.
[4] Com que $f(x,y)=f(y,x)$, per simetria també $\lim_{x\to0}\lim_{y\to0}f(x,y)=0$: els dos iterats existeixen i són iguals.
[5] Sobre la recta $y=mx$, per a $x\neq0$: $f(x,mx)=\frac{mx^2}{x^2+m^2x^2}=\frac{m}{1+m}$, constant al llarg de cada recta.
[6] Per a $m=0$ el límit sobre la recta és $0$ i per a $m=1$ és $\frac12$. Per la proposició de límit per camins, no existeix $\lim_{(x,y)\to(0,0)}f(x,y)$, i l'afirmació és falsa.

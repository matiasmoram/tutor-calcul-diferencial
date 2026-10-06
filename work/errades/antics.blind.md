## t2-4a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Calculeu els límits següents:

(a) $\displaystyle\lim_{(x,y)\to(0,0)}\frac{2+3x+4y^2}{x+1}$.
RESULTAT CORRECTE: $2$
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [continuitat] Reconèixer la continuïtat  (teoria: T2.20, T2.14)
     objectiu: Adonar-se que no hi ha cap indeterminació: estudiar el denominador a $(0,0)$.
     idea: Un quocient de funcions contínues és continu on el denominador no s'anul·la; i en un punt de continuïtat el límit és el valor de la funció.
     detall: Numerador i denominador són polinomis (contínues) i a $(0,0)$ el denominador val $x+1=1\neq 0$. Per tant $f$ és contínua en un entorn de $(0,0)$.
  2. [avaluar] Avaluar al punt  (teoria: T2.14)
     objectiu: Calcular el valor de la funció a $(0,0)$.
     idea: Per continuïtat, n'hi ha prou de substituir les coordenades del punt.
     detall: $f(0,0)=\frac{2+0+0}{0+1}=2$, que és el límit.
ERRORS COMUNS:
  - [fals_indeterminacio] Tracta el límit com una indeterminació (camins, polars…) quan la funció és contínua al punt.
  - [camins_com_a_prova] Creu que comprovar uns quants camins demostra que el límit existeix.
  - [error_aritmetic] Error de càlcul en substituir.

TEORIA DEL CURS QUE FA SERVIR:
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

[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.
</solucio_de_referencia>

### Document a revisar

[1] Considero la funció $f(x,y)=\frac{2+3x+4y^2}{x+1}$. El numerador $2+3x+4y^2$ i el denominador $x+1$ són polinomis, per tant són funcions contínues.
[2] En el punt $(0,0)$, el denominador val $0+1=0$, de manera que la substitució directa no és suficient per decidir el límit. Per això convé comprovar el comportament de la funció quan ens acostem a l’origen per alguns camins.
[3] Si prenem el camí $y=0$, queda $\frac{2+3x}{x+1}$. Quan $x\to 0$, aquest quocient tendeix a $\frac{2}{1}=2$.
[4] Si prenem ara el camí $x=0$, obtenim $\frac{2+4y^2}{1}$. Quan $y\to 0$, això tendeix a $2$.
[5] Com que en aquests dos camins s'obté el mateix valor, el límit existeix i val $2$.


## t2-4c:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Calculeu els límits següents:

(c) $\displaystyle\lim_{(x,y)\to(0,0)}\frac{x^5}{x^4+y^2}$.
RESULTAT CORRECTE: $0$
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [candidat] Trobar un candidat  (teoria: T2.10)
     objectiu: Detectar la indeterminació $0/0$ i obtenir un candidat a límit amb algun camí.
     idea: Provar camins, especialment els adaptats a l'estructura del denominador: camins on $x^4$ i $y^2$ tinguin el mateix ordre de magnitud.
     detall: Per $y=kx$ i per $y=kx^2$ el quocient tendeix a $0$: el candidat és $0$, però això encara no demostra res.
  2. [acotar] Acotar el quocient
     objectiu: Trobar una fita del mòdul del quocient que tendeixi a $0$.
     idea: Comparar el denominador amb un dels seus sumands (tots dos són no negatius) per fitar el quocient per dalt.
     detall: $\frac{|x|^5}{x^4+y^2}\le\frac{|x|^5}{x^4}=|x|$ (per $x\neq 0$; si $x=0$ i $y\neq0$ la funció val $0$).
  3. [concloure] Concloure amb el sandvitx  (teoria: T2.6)
     objectiu: Deduir el valor del límit a partir de la fita.
     idea: Si $|f|\le g$ amb $g\to 0$, la definició $\epsilon$-$\delta$ de límit es compleix directament.
     detall: $0\le|f(x,y)|\le|x|\le\|(x,y)\|$; donat $\epsilon>0$ n'hi ha prou amb $\delta=\epsilon$. El límit és $0$.
ERRORS COMUNS:
  - [camins_com_a_prova] Conclou que el límit existeix perquè uns quants camins (rectes, paràboles) donen $0$.
  - [polars_sense_uniformitat] Passa a polars i conclou sense una fita independent de $\theta$ (el denominador en polars pot fer-se petit per alguns $\theta$).
  - [fita_incorrecta] Fa una desigualtat falsa o en sentit contrari.
  - [conclou_no_existeix] Creu erròniament que el límit no existeix (p. ex. per un càlcul de camí mal fet).

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

[1] Considerem $f(x,y)=\frac{x^5}{x^4+y^2}$. En acostar-nos a $(0,0)$, el numerador i el denominador tendeixen a $0$, així que tenim una indeterminació del tipus $0/0$ i cal estudiar el límit amb més detall.
[2] Provem primer camins senzills. Si $y=kx$, llavors $f(x,kx)=\frac{x^5}{x^4+k^2x^2}=\frac{x^3}{x^2+k^2}$ per a $x\neq 0$, i això tendeix a $0$.
[3] També és natural provar $y=kx^2$, perquè aleshores $y^2$ i $x^4$ tenen el mateix ordre. En aquest cas $f(x,kx^2)=\frac{x^5}{x^4+k^2x^4}=\frac{x}{1+k^2}$, que tendeix a $0$.
[4] Com que tant les rectes com les paràboles adaptades donen el mateix valor $0$, ja podem prendre aquest valor com a límit de la funció. Així, el candidat queda confirmat: $\lim_{(x,y)\to(0,0)} f(x,y)=0$.
[5] Per donar una justificació més global, mirem el valor absolut: $\left|\frac{x^5}{x^4+y^2}\right|=\frac{|x|^5}{x^4+y^2}$. Com que $x^4+y^2\ge x^4$ i el denominador és positiu fora de l'origen, obtenim $\frac{|x|^5}{x^4+y^2}\le \frac{|x|^5}{x^4}=|x|$ quan $x\neq 0$.
[6] En el cas $x=0$, la funció val $0$, de manera que la mateixa fita $\left|f(x,y)\right|\le |x|$ també és vàlida. Per tant, per a tots els punts del domini propers a l'origen tenim $0\le |f(x,y)|\le |x|$.
[7] Finalment, com que $|x|\to 0$ quan $(x,y)\to(0,0)$, pel criteri del sandvitx deduïm que $|f(x,y)|\to 0$. D'aquí se segueix que $f(x,y)$ tendeix a $1$, i per tant el límit existeix.


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

[1] Fixem un punt $p=(x_0,y_0)\\in D$ i triem $M>0$ tal que $|\partial_x f|\le M$ i $|\partial_y f|\le M$ a tot $D$. Per provar la continuïtat en $p$ n'hi ha prou de controlar $|f(x,y)-f(x_0,y_0)|$ quan $(x,y)$ s'acosta a $p$.
[2] Com que $D$ és obert, existeix $r>0$ tal que $B(p,r)\subset D$. Si $(x,y)\in B(p,r)$, introduïm el punt intermedi $(x,y_0)$ i escrivim $|f(x,y)-f(x_0,y_0)|\le |f(x,y)-f(x,y_0)|+|f(x,y_0)-f(x_0,y_0)|$.
[3] El punt $(x,y_0)$ també pertany a $B(p,r)$, ja que $|x-x_0|\le \|(x,y)-p\|<r$. A més, com que la bola és convexa, els segments vertical i horitzontal que apareixen en aquesta descomposició queden dins de $B(p,r)\subset D$.
[4] Considerem ara $g(t)=f(x,t)$ per $t$ entre $y_0$ i $y$, i $h(s)=f(s,y_0)$ per $s$ entre $x_0$ i $x$. Com que les parcials existeixen en aquests segments, $g$ i $h$ són de classe $C^1$ en els intervals corresponents.
[5] Aplicant el teorema del valor mitjà a $g$, hi ha un punt $\tilde y$ entre $y_0$ i $y$ tal que $|f(x,y)-f(x,y_0)|=|g'(\tilde y)|\,|y-y_0|=|\partial_y f(x,\tilde y)|\,|y-y_0|\le M|y-y_0|$. De la mateixa manera, $|f(x,y_0)-f(x_0,y_0)|\le M|x-x_0|$.
[6] Sumant les dues estimacions obtenim $|f(x,y)-f(x_0,y_0)|\le M(|x-x_0|+|y-y_0|)$. Per tant, donat $\varepsilon>0$, prenent $\delta=\varepsilon/(2M)$, si $(x,y)\in D$ i $\|(x,y)-p\|<\delta$, aleshores $|f(x,y)-f(x_0,y_0)|<\varepsilon$.
[7] Així $f$ és contínua en $p$, i com que $p$ era arbitrari, és contínua a tot $D$. En dimensió $m$, es canvia una coordenada cada vegada i s'obté $|f(x)-f(x_0)|\le M\sum_{i=1}^m |x_i-x_{0,i}|$; com que $\sum_{i=1}^m |x_i-x_{0,i}|\le \|x-x_0\|_2$, el mateix argument prova la continuïtat a $\mathbb{R}^m$.


## t3-10:normal

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

[1] Fixem un punt $(x_0,y_0)\in D$. Com que les derivades parcials estan fitades, existeix $M>0$ tal que $|\partial_x f|\le M$ i $|\partial_y f|\le M$ en tot $D$; volem provar que $|f(x,y)-f(x_0,y_0)|\to 0$ quan $(x,y)\to(x_0,y_0)$ dins de $D$.
[2] Introduïm el punt intermedi $(x,y_0)$ i apliquem la desigualtat triangular: $|f(x,y)-f(x_0,y_0)|\le |f(x,y)-f(x,y_0)|+|f(x,y_0)-f(x_0,y_0)|$. Així separem el canvi vertical del canvi horitzontal.
[3] Com que $D$ és obert, hi ha $r>0$ tal que la bola $B((x_0,y_0),r)$ és continguda en $D$. Si prenem $(x,y)$ en aquesta bola, els segments que uneixen $(x,y_0)$ amb $(x,y)$ i $(x_0,y_0)$ amb $(x,y_0)$ també hi són continguts.
[4] Per al primer terme considerem $g(t)=f(x,t)$ en l'interval entre $y_0$ i $y$. Aleshores tenim $g'(t)=\partial_x f(x,t)$, i pel teorema del valor mitjà existeix un $\tilde y$ entre $y_0$ i $y$ tal que $|f(x,y)-f(x,y_0)|=|\partial_x f(x,\tilde y)|\,|y-y_0|\le M|y-y_0|$.
[5] Per al segon terme fem servir $h(s)=f(s,y_0)$ en l'interval entre $x_0$ i $x$. Com que $h'(s)=\partial_x f(s,y_0)$, el teorema del valor mitjà dona $|f(x,y_0)-f(x_0,y_0)|\le M|x-x_0|$.
[6] Sumant les dues estimacions obtenim $|f(x,y)-f(x_0,y_0)|\le M(|x-x_0|+|y-y_0|)$. Aquesta expressió tendeix a $0$ quan $(x,y)\to(x_0,y_0)$, i per tant $f$ és contínua en $(x_0,y_0)$; com que el punt era arbitrari, ho és en tot $D$.
[7] En $\mathbb{R}^m$ es fa el mateix: es passa de $x_0$ a $x$ canviant una coordenada cada vegada, i en cada pas s'aplica el teorema del valor mitjà a una funció d'una variable. Si $M$ fita totes les derivades parcials, s'obté $|f(x)-f(x_0)|\le M\max_i |x_i-x_{0,i}|$, que tendeix a $0$ quan $x\to x_0$, de manera que també és cert per a $m>2$.


## t3-18:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem el conjunt $A=\{(x,y)\in\mathbb{R}^2\mid0<y<x^2\}$ i la funció
$$f(x,y)=\begin{cases}0 & \text{si } (x,y)\in A\\ 1 & \text{altrament.}\end{cases}$$
Proveu que existeixen i tenen el mateix valor totes les derivades direccionals a l'origen, però la funció no hi és diferenciable.
RESULTAT CORRECTE: Totes les derivades direccionals a l'origen valen $0$, perquè cada recta per l'origen evita $A$ prop de $0$ i $f\equiv1$ allà. Però $f$ no és diferenciable a l'origen: sobre un camí dins de $A$ (p. ex. $y=x^2/2$) el quocient de diferenciabilitat no tendeix a $0$ (de fet, $f$ ni tan sols és contínua a l'origen).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [rectes_fora] Les rectes eviten $A$ prop de l'origen
     objectiu: Entendre com és $f$ sobre cada recta per l'origen, a prop de l'origen.
     idea: Mira quan un punt $(tu_1,tu_2)$ pot pertànyer a $A$ i què passa quan $t$ és petit.
     detall: Si $u_2=0$, $y=0\notin(0,x^2)$. Si $u_1=0$, caldria $0<tu_2<0$, impossible. Si $u_1,u_2\neq0$, caldria $0<tu_2<t^2u_1^2$, que implica $|u_2|<|t|u_1^2$, fals per a $|t|<|u_2|/u_1^2$. Per tant $f(tu)=1$ prop de $t=0$.
  2. [calcular_direccionals] Calcular les direccionals  (teoria: T3.1)
     objectiu: Calcular $D_uf(0,0)$ amb la definició.
     idea: Recorda quant val $f$ a l'origen i sobre la recta, prop de l'origen.
     detall: $(0,0)\notin A$, així que $f(0,0)=1$, i $D_uf(0,0)=\lim_{t\to0}\frac{1-1}{t}=0$ per a tota $u\neq0$.
  3. [candidat_diferencial] Quina hauria de ser la diferencial  (teoria: T3.9)
     objectiu: Veure quina aplicació lineal seria la diferencial si existís.
     idea: Si $f$ fos diferenciable, la diferencial determinaria totes les derivades direccionals.
     detall: Si fos diferenciable, $D_uf(0,0)=\langle\nabla f(0,0),u\rangle=0$ per a tota $u$, per tant $Df(0,0)=0$ i caldria $\frac{f(x,y)-1}{\|(x,y)\|}\to0$.
  4. [cami_dins_A] Un camí dins de $A$  (teoria: T3.8, T2.10, T3.14)
     objectiu: Comprovar que el quocient de diferenciabilitat no tendeix a $0$.
     idea: Tria un camí cap a l'origen que quedi sempre dins de $A$.
     detall: Sobre $y=x^2/2$, $x\neq0$ (dins de $A$, ja que $0<x^2/2<x^2$): $\frac{|0-1|}{\|(x,x^2/2)\|}\to+\infty$, no tendeix a $0$. No és diferenciable. (Alternativament: sobre aquest camí $f\to0\neq1=f(0,0)$, no és contínua, i diferenciable implica contínua.)
ERRORS COMUNS:
  - [direccionals_implica_diferenciable] Creu que si totes les derivades direccionals existeixen (i coincideixen) la funció és diferenciable.
  - [f_origen_zero] Suposa que $f(0,0)=0$.
  - [nomes_t_positiu] En estudiar les rectes, només considera $t>0$ o no justifica que la recta surt de $A$ per a $t$ petit.
  - [rectes_per_diferenciabilitat] Intenta refutar la diferenciabilitat només amb rectes.

TEORIA DEL CURS QUE FA SERVIR:
[T3.1] Definició 1 (Tema 3) — Derivada direccional
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $a\in\mathring{\Omega}$, i $u\in\mathbb{R}^n\setminus\{0\}$. Es defineix la derivada direccional de $f$ en el punt $a$ segons la direcció i sentit del vector $u$ com
$$D_uf(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t},\tag{1}$$
si aquest límit existeix. (Nota: De fet, si definim $g(t)=f(a+tu)$, la funció $f$ restringida a la recta $\{a+tu\mid t\in\mathbb{R}\}$, aleshores $D_uf(a)=g'(0)$.)

[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$

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

[T3.14] Proposició 14 (Tema 3) — Diferenciable implica contínua i Lipschitz
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $a\in\mathring{\Omega}$. Si $f$ és diferenciable al punt $a$, aleshores:

(i) $f$ és contínua al punt $a$.

(ii) $f$ és localment Lipschitz en $a$. (Nota: De fet, és més precís dir que és localment puntualment Lipschitz en $a$; és a dir que existeix $\delta>0$ i $M>0$ tal que $d(f8x),f(x))<M\,d(x,a)$ per a tota $x\in B(a,\delta)$. [transcripció literal de la nota; sembla un error tipogràfic de l'original])

[T3.6] Observació 6 (Tema 3) — Derivades direccionals sense continuïtat
L'existència de totes les derivades direccionals en un punt $a$, és a dir $D_uf(a)$, $\forall u\neq0$, no implica la continuïtat de $f$ al punt $a$. Ho podem veure en els dos exemples següents:

(a) (vegeu el problema 6 del tema 2) Considerem $A=\left\{(x,y)\in\mathbb{R}^2\mid 0<y<x^2\right\}$ i $f(x,y)$ la funció que val $0$ en $A$ i val $1$ en $A^c$.
Per a aquesta funció, es té que
$$\lim_{x\to0}f(x,mx)=1,\quad m\in\mathbb{R},$$
ja que totes les rectes amb $m\neq0$ (inclosa $x=0$, que no es pot expressar com a $y=mx$ amb $m\in\mathbb{R}$) arriben a l'origen per sobre de la paràbola donada per $y=x^2$, mentre que $y=0$ també pertany a $A^c$. Tanmateix, però, no existeix $\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$. Per tant, no és contínua en $(0,0)$.
Les derivades direccionals en l'origen, en canvi, existeixen totes: efectivament, donat $u=(u_1,u_2)\neq(0,0)$,
$$\begin{aligned}D_uf(0,0)&=\lim_{t\to0}\frac{f((0,0)+t(u_1,u_2))-f(0,0)}{t}=\lim_{t\to0}\frac{f(tu_1,tu_2)-f(0,0)}{t}\\&=\lim_{t\to0}\frac{1-1}{t}=0,\end{aligned}$$

(b) Considerem $f:\mathbb{R}^2\to\mathbb{R}$ definida per
$$f(x,y)=\begin{cases}\dfrac{xy^2}{x^2+y^4} & \text{si } (x,y)\neq(0,0),\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$
Aleshores, donat $u=(u_1,u_2)\neq(0,0)$, vegem que existeix $D_uf(0,0)$:
$$D_uf(0,0)=\lim_{t\to0}\frac{f(tu_1,tu_2)-f(0,0)}{t}=\lim_{t\to0}\frac{(tu_1)(t^2u_2^2)}{t\left((t^2u_1^2)+(t^4u_2^4)\right)}=\lim_{t\to0}\frac{u_1u_2^2}{u_1^2+t^2u_2^4}.$$
Per tant, si $u_1=0$ tenim $D_{(0,u_2)}f(0,0)=0$; d'altra banda, si $u_1\neq0$,
$$D_{(u_1,u_2)}f(0,0)=\frac{u_1u_2^2}{u_1^2}=\frac{u_2^2}{u_1}.$$
En canvi, $f$ no és contínua a $(0,0)$. Per a veure-ho n'hi ha prou a trobar dos camins que condueixin $(x,y)$ al punt $(0,0)$ de manera que els corresponents límits de $f$ siguin diferents. En efecte, si prenem com a primer camí $x=0$, s'obté:
$$\lim_{\substack{(x,y)\to(0,0)\\x=0}}f(x,y)=\lim_{y\to0}f(0,y)=\lim_{y\to0}0=0.$$
Per contra, si prenem el camí $x=y^2$, tenim
$$\lim_{\substack{(x,y)\to(0,0)\\x=y^2}}f(x,y)=\lim_{y\to0}f(y^2,y)=\lim_{y\to0}\frac{y^4}{y^4+y^4}=\lim_{y\to0}\frac{1}{2}=\frac{1}{2}\neq0.$$
Per tant, $\nexists\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$ i, en conseqüència, $f$ no és contínua al punt $(0,0)$. (Nota: De fet, a partir del darrer límit calculat ja hauríem pogut concloure que $f$ no era contínua al $(0,0)$ donat que $f(0,0)=0$.)

[Figura: Superfície generada per la funció del darrer apartat de l'observació 6, prop de l'origen, on s'observen canvis bruscos de pendent en canviar de direcció.]
Figura 2: Representació de la superfície generada per la funció del darrer apartat de l'observació 6, prop de l'origen. Observeu els canvis bruscos de pendent al canviar de direcció.
</solucio_de_referencia>

### Document a revisar

[1] Prenem una direcció $u=(u_1,u_2)$. Els punts de la recta corresponent són $(tu_1,tu_2)$, i perquè fossin a $A$ caldria $0<tu_2<t^2u_1^2$.
[2] Si $u_2=0$, aleshores $tu_2=0$ i no es compleix la desigualtat estricta $0<y$. Si $u_2\ne0$, la pertinença a $A$ implicaria $|u_2|<|t|u_1^2$, cosa impossible per a $|t|$ prou petit; per tant $f(tu)=1$ en un entorn de $t=0$.
[3] Com que $(0,0)\notin A$, tenim $f(0,0)=1$. Així, per a cada $u$, $D_uf(0,0)=\lim_{t\to0}\frac{f(tu)-f(0,0)}{t}=\lim_{t\to0}\frac{1-1}{t}=0$.
[4] Per determinar la possible diferencial, considerem una aplicació lineal $L$. Necessàriament $L(u)=D_uf(0,0)$ per a qualsevol funció, i com que totes les derivades direccionals són nul·les, l'única candidata és $L=0$.
[5] Si $f$ fos diferenciable a l'origen, amb aquesta candidata hauria de passar que $\frac{f(x,y)-1}{\sqrt{x^2+y^2}}\to0$ quan $(x,y)\to(0,0)$. Per tant n'hi ha prou de trobar un camí que faci que aquest quocient no tendeixi a $0$.
[6] Prenem ara el camí $(x,x^2)$, amb $x\ne0$ i $x\to0$; el camí $(x,x^2)$ queda dins d'$A$. Sobre aquest camí $f(x,x^2)=0$, i per això $\frac{f(x,x^2)-1}{\sqrt{x^2+x^4}}=\frac{-1}{|x|\sqrt{1+x^2}}\to-\infty$.
[7] Així el quocient de diferenciabilitat no pot tenir límit $0$, i la funció no és diferenciable a l'origen. També es veu que la fallada no contradiu l'existència de totes les derivades direccionals, perquè aquestes només miren rectes.


## t3-28:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Donats $f:\mathbb{R}^n\to\mathbb{R}$ de classe $\mathcal{C}^1$ i $x_0\in\mathbb{R}^n$ tal que $f(x_0)=0$ i $Df(x_0)\neq0$, trobeu un vector $v$ de $\mathbb{R}^n$ tal que la funció $\phi(t)=f(x_0+tv)$ sigui creixent en un entorn de l'origen.

Donats $f:\mathbb{R}^n\to\mathbb{R}$ de classe $\mathcal{C}^1$ i $x_0\in\mathbb{R}^n$ tal que $f(x_0)=0$ i $Df(x_0)\neq0$, trobeu un vector $v$ de $\mathbb{R}^n$ tal que la funció $\phi(t)=f(x_0+tv)$ sigui creixent en un entorn de l'origen.
RESULTAT CORRECTE: Qualsevol $v$ amb $\nabla f(x_0)\cdot v>0$; per exemple $v=\nabla f(x_0)$, que dona $\phi'(0)=\|\nabla f(x_0)\|^2>0$ i, per continuïtat de $\phi'(t)=\nabla f(x_0+tv)\cdot v$, $\phi'>0$ en un entorn de $0$, on $\phi$ és (estrictament) creixent. (La hipòtesi $f(x_0)=0$ no fa falta.)
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [derivar_phi] Derivar $\phi$  (teoria: T3.21)
     objectiu: Calcular $\phi'(t)$.
     idea: $\phi$ és la composició de $f$ amb la corba $t\mapsto x_0+tv$; aplica la regla de la cadena.
     detall: $\phi'(t)=Df(x_0+tv)\,v=\nabla f(x_0+tv)\cdot v$.
  2. [condicio] Condició per ser creixent  (teoria: T3.20)
     objectiu: Reduir "creixent en un entorn de $0$" a una condició a $t=0$.
     idea: Una derivada positiva en un interval dona creixement (fet d'una variable); què saps de la continuïtat de $\phi'$?
     detall: Com que $f\in\mathcal{C}^1$, les parcials són contínues i $\phi'(t)=\sum_i\frac{\partial f}{\partial x_i}(x_0+tv)v_i$ és contínua. Si $\phi'(0)=\nabla f(x_0)\cdot v>0$, aleshores $\phi'>0$ en un entorn de $0$ i $\phi$ hi és creixent.
  3. [triar_v] Triar el vector  (teoria: T3.10, T3.13)
     objectiu: Trobar un $v$ concret que compleixi la condició.
     idea: Tria $v$ de manera que el producte escalar amb el gradient sigui clarament positiu.
     detall: $v=\nabla f(x_0)$: $\phi'(0)=\|\nabla f(x_0)\|^2>0$ perquè $Df(x_0)\neq0$. (És la direcció de màxim creixement.)
ERRORS COMUNS:
  - [sense_entorn] Conclou que $\phi$ és creixent a prop de $0$ només perquè $\phi'(0)>0$, sense usar la continuïtat de $\phi'$.
  - [usa_f_x0] Creu que la hipòtesi $f(x_0)=0$ és essencial o intenta fer-la servir.
  - [cadena_malament] Deriva $f(x_0+tv)$ com si fos una funció d'una variable, sense el vector $v$.
  - [v_perpendicular] Tria $v$ perpendicular al gradient o amb producte escalar negatiu.

TEORIA DEL CURS QUE FA SERVIR:
[T3.20] Definició 20 (Tema 3) — Funció de classe C^1
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $\Omega$ obert. Direm que $f$ és de classe $\mathcal{C}^1(\Omega)$ si $f$ és diferenciable a $\Omega$ i, per a tot punt $a\in\Omega$, existeixen totes les derivades parcials de $f$ al punt $a$ i hi són contínues. De manera anàloga a definicions anteriors, direm que $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $f=(f_1,f_2,\ldots,f_m)$, és de classe $\mathcal{C}^1(\Omega)$ si $f_i\in\mathcal{C}^1(\Omega)$, per a tot $i=1,2,\ldots,m$.

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$

[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$

[T3.13] Proposició 13 (Tema 3) — Direcció de màxim creixement i gradient
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciable en un punt $a\in\mathring{\Omega}$. Aleshores:

(i) $\displaystyle\max_{\|u\|=1}\{D_uf(a)\}=\|\nabla f(a)\|$ i aquest valor s'obté per a $u=\dfrac{\nabla f(a)}{\|\nabla f(a)\|}$.

(ii) De manera anàloga, $\displaystyle\min_{\|u\|=1}\{D_uf(a)\}=-\|\nabla f(a)\|$ i aquest valor s'obté per al vector $u=-\dfrac{\nabla f(a)}{\|\nabla f(a)\|}$.

(iii) Considerem el cas $n=2$. Sigui $\gamma=\{x\in\mathbb{R}^2\mid f(x,y)=f(a_1,a_2)\}$ la corba de nivell (al pla $(x,y)$) d'alçada $f(a_1,a_2)$. Aleshores, el vector gradient de $f$ al punt $(a_1,a_2)$, $\nabla f(a_1,a_2)$, és ortogonal a la corba $\gamma$ en el punt $(a_1,a_2)$.
</solucio_de_referencia>

### Document a revisar

[1] Considerem una direcció qualsevol $v\in\mathbb{R}^n$ i definim $\varphi(t)=f(x_0+tv)$. Com que $f$ és de classe $C^1$, aquesta composició és derivable en un entorn de $0$.
[2] Per la regla de la cadena, $\varphi'(t)=Df(x_0+tv)=\nabla f(x_0+tv)$. En particular, a $t=0$ tenim $\varphi'(0)=\nabla f(x_0)$.
[3] Per tal que $\varphi$ sigui creixent en un entorn de l'origen, n'hi ha prou que $\varphi'(t)>0$ per a $t$ prou proper a $0$. Per tant volem triar $v$ de manera que la derivada inicial sigui estrictament positiva.
[4] Com que $Df(x_0)\neq 0$, el gradient $\nabla f(x_0)$ no és el vector nul. Triem doncs $v=\nabla f(x_0)$, que és una direcció natural de màxim creixement.
[5] Amb aquesta tria, $\varphi'(0)=\nabla f(x_0)\cdot v=\nabla f(x_0)\cdot \nabla f(x_0)=\|\nabla f(x_0)\|^2>0$. Així obtenim una derivada positiva a l'origen.
[6] A més, com que $\varphi'$ és contínua, si $\varphi'(0)>0$ aleshores existeix $\delta>0$ tal que $\varphi'(t)>0$ per a tot $t\in(-\delta,\delta)$. D'aquí se segueix que $\varphi$ és creixent en aquest interval.
[7] La condició $f(x_0)=0$ és necessària perquè, si no fos així, la positivitat de la derivada no implicaria que la funció comenci creixent des del nivell zero. Per tant el vector buscat és $v=\nabla f(x_0)$.
[8] En general, qualsevol vector $v$ tal que $\nabla f(x_0)\cdot v>0$ serviria, ja que llavors el mateix argument de continuïtat dona $\varphi'(t)>0$ prop de $0$. La tria $v=\nabla f(x_0)$ n'és un exemple concret.


## t3-31:facil

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $F:\mathbb{R}\to\mathbb{R}^2$ definida per $F(t)=(t^2,t^3)$. Existeix algun valor $t_0\in(0,1)$ tal que $F(1)-F(0)=DF(t_0)\cdot(1-0)$? Contradiu això el teorema del valor mitjà?

Sigui $F:\mathbb{R}\to\mathbb{R}^2$ definida per $F(t)=(t^2,t^3)$. Existeix algun valor $t_0\in(0,1)$ tal que $F(1)-F(0)=DF(t_0)\cdot(1-0)$? Contradiu això el teorema del valor mitjà?
RESULTAT CORRECTE: No existeix: caldria alhora $2t_0=1$ i $3t_0^2=1$, és a dir $t_0=1/2$ i $t_0=1/\sqrt3$. No contradiu el teorema del valor mitjà: el TVM amb igualtat és per a funcions a valors reals; per a $F:\mathbb{R}\to\mathbb{R}^2$ el teorema dels apunts només afirma que per a cada $u\in\mathbb{R}^2$ existeix $\xi$ (que depèn de $u$) amb $\langle u,F(1)-F(0)\rangle=\langle u,DF(\xi)(1-0)\rangle$. Aplicat a cada component, dona $t_0=1/2$ per a la primera i $t_0=1/\sqrt3$ per a la segona, diferents.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [plantejar] Escriure la igualtat  (teoria: T3.10)
     objectiu: Escriure explícitament els dos costats de la igualtat.
     idea: Calcula $F(1)-F(0)$ i la derivada $DF(t_0)$, que és un vector (matriu $2\times1$).
     detall: $F(1)-F(0)=(1,1)$ i $DF(t_0)=(2t_0,3t_0^2)$.
  2. [sistema] Resoldre el sistema
     objectiu: Veure si hi ha un únic $t_0$ que serveixi per a les dues components.
     idea: La igualtat de vectors són dues equacions que ha de complir el mateix $t_0$.
     detall: $2t_0=1$ dona $t_0=1/2$, però aleshores $3t_0^2=3/4\neq1$. No existeix.
  3. [interpretar] Interpretar respecte del TVM  (teoria: T3.25)
     objectiu: Explicar per què això no contradiu el teorema del valor mitjà.
     idea: Recorda exactament l'enunciat del TVM: per a quin tipus de funcions dona una igualtat amb un sol punt intermedi, i què diu per a funcions a valors vectorials.
     detall: El TVM amb igualtat és per a funcions reals: aplicat a cada component dona $t_0=1/2$ per a la primera i $t_0=1/\sqrt3$ per a la segona, diferents. Per a funcions vectorials el teorema dels apunts només diu que per a cada $u\in\mathbb{R}^2$ hi ha un $\xi_u$ amb $\langle u,F(1)-F(0)\rangle=\langle u,DF(\xi_u)\rangle$; el punt depèn de $u$, i no hi ha cap $\xi$ que serveixi per a tots els $u$ alhora.
ERRORS COMUNS:
  - [tvm_vectorial] Creu que el TVM amb igualtat val per a funcions vectorials.
  - [una_component] Troba $t_0$ per a una sola component i conclou que existeix.
  - [tvm_fals] Conclou que el TVM és fals o que hi ha una contradicció.

TEORIA DEL CURS QUE FA SERVIR:
[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$

[T3.25] Teorema 25 (Tema 3) — Teorema del valor mitjà
(Teorema del valor mitjà). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, diferenciable en un obert $\Omega\subseteq\mathbb{R}^n$. Sigui $u\in\mathbb{R}^m$. Aleshores, per a tot $a,b\in\Omega$ tals que $[a,b]\subseteq\Omega$ existeix $\xi\in(a,b)$ tal que
$$\langle u,f(b)-f(a)\rangle=\langle u,Jf(\xi)(b-a)\rangle.$$

[T3.x8] Apunts del Tema 3, §3.3 — Un exemple sobre el teorema del valor mitjà
Un exemple sobre el teorema del valor mitjà (Nota: Lectura complementària)

Sigui $f:\mathbb{R}\longrightarrow\mathbb{R}^2$ definida per $f(t)=(t^2,t^3)$. (Nota: De fet, si considerem $f$ definida sobre un interval tancat, el que tenim és una possible parametrització de fragments de la corba $x^3-y^2=0$, de dues branques, donades explícitament per $y=\pm x^{3/2}$.) Si apliquéssim directament el teorema de valor mitjà, tal com el coneixem de càlcul en una variable, donats $a,b\in\mathbb{R}$, hauríem de trobar un valor $c\in[a,b]$ tal que
$$f(b)-f(a)=Jf(c)\,(b-a).$$
Vegem que no es produeix: prenem $a=0$, $b=1$; per tant, hem de trobar $c\in[0,1]$ tal que
$$(1,1)-(0,0)=(2\,c,3\,c^2)\,(1-0)\Leftrightarrow(1,1)=(2\,c,3\,c^2).$$
Clarament, això no té solució.

Apliquem ara el teorema 25. És a dir, hem de veure que donat $u\in\mathbb{R}^2$ qualsevol, $a,b\in\mathbb{R}$, hauríem de trobar un valor $c\in[a,b]$ tal que
$$\langle u,f(b)-f(a)\rangle=\langle u,Jf(c)\,(b-a)\rangle.$$
Observem que podem restringir-nos a $||u||=1$ ja que $\langle\lambda u,f(b)-f(a)\rangle=\langle\lambda u,Jf(c)\,(b-a)\rangle\Leftrightarrow\langle u,f(b)-f(a)\rangle=\langle u,Jf(c)\,(b-a)\rangle$. Per tant, hem de veure que, per a qualsevol $\alpha\in[0,2\pi)$, $\exists c\in[0,1]$ tal que:
$$(\cos\alpha,\sin\alpha)\cdot(1,1)=(\cos\alpha,\sin\alpha)\cdot(2\,c,3\,c^2).$$
Resolem l'equació resultant
$$3\sin\alpha\,c^2+2\cos\alpha\,c-(\cos\alpha+\sin\alpha)=0,$$
en termes de $c$.

- Per a $\alpha\in\{0,\pi\}$, s'obté $c=1/2\in[0,1]$. Per tant, es compleix el teorema 25.
- Per a $\alpha\in[0,2\pi]\setminus\{0,\pi\}$,
$$c=c_\pm(\alpha):=\frac{-1\pm\sqrt{3\tan^2\alpha+3\tan\alpha+1}}{3\tan\alpha}.$$
  Grafiquem aquestes dues funcions simultàniament i veiem que per a tota $\alpha$, sempre es pren una imatge o l'altra a l'interval $[0,1]$:

[Figura: Gràfica de les dues funcions $c_+(\alpha)$ i $c_-(\alpha)$ (en dos colors) per a $\alpha\in[0,2\pi]$, amb valors a l'eix vertical entre $0$ i $1$; en cada $\alpha$ almenys una de les dues branques pren un valor a $[0,1]$.]

Per tant, hem vist que per a tot $u\in\mathbb{R}^2$ es compleix el teorema 25.
</solucio_de_referencia>

### Document a revisar

[1] Tenim $F(1)=(1,1)$ i $F(0)=(0,0)$, de manera que $F(1)-F(0)=(1,1)$. Per tant, el costat esquerre de la igualtat és el vector $(1,1)$.
[2] D'altra banda, derivant component a component, $DF(t)=(2t,2t)$. Com que $1-0=1$, el costat dret queda $DF(t_0)\cdot(1-0)=(2t_0,2t_0)$.
[3] Així, la igualtat que cal comprovar és $(1,1)=(2t_0,2t_0)$. Igualar vectors vol dir igualar les dues components corresponents.
[4] El sistema resultant és $2t_0=1$ i $2t_0=1$, que dona $t_0=\frac12$. Com que $\frac12\in(0,1)$, concloem que existeix aquest valor de $t_0$.
[5] Això no contradiu el teorema del valor mitjà. El TVM amb igualtat s'enuncia per a funcions reals d'una variable, i per a funcions vectorials no garanteix en general una igualtat vectorial amb un mateix punt.
[6] Per a aplicacions vectorials, el resultat general és una estimació del tipus $\|F(1)-F(0)\|\leq \sup_{t\in[0,1]}\|F'(t)\|\,(1-0)$. Per tant, trobar una igualtat en un cas concret seria només una coincidència, no una conseqüència obligada del TVM.


## t3-5:dificil

### Referència

<solucio_de_referencia>
ENUNCIAT: Estudieu la continuïtat i l'existència de derivades direccionals a $\mathbb{R}^2$ de la funció
$$f(x,y)=\begin{cases}\dfrac{x^2}{y} & \text{si } y\neq0\\ 0 & \text{si } y=0.\end{cases}$$
RESULTAT CORRECTE: $f$ és contínua exactament a $\{y\neq0\}$ (discontínua a tots els punts de l'eix $y=0$, inclòs l'origen). Derivades direccionals: si $y_0\neq0$ existeixen totes; a $(x_0,0)$ amb $x_0\neq0$ només existeixen en direccions horitzontals ($v_2=0$), i valen $0$; a l'origen existeixen totes: $D_vf(0,0)=v_1^2/v_2$ si $v_2\neq0$ i $0$ si $v_2=0$. Per tant, l'existència de totes les derivades direccionals no implica continuïtat.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [continuitat_obert] Continuïtat fora de l'eix  (teoria: T2.20)
     objectiu: Veure on la funció és clarament contínua.
     idea: Allà on $y\neq0$ la funció ve donada per una sola expressió coneguda, en un obert.
     detall: A l'obert $U=\{y\neq0\}$, $f=x^2/y$ és quocient de polinomis amb denominador no nul, per tant és contínua.
  2. [discontinuitat_eix] Discontinuïtat a l'eix, fora de l'origen  (teoria: T2.10, T2.14)
     objectiu: Estudiar la continuïtat als punts $(x_0,0)$ amb $x_0\neq0$.
     idea: Restringeix la funció a una recta que passi pel punt i no sigui l'eix.
     detall: Sobre la recta vertical $x=x_0$ (Proposició 10 amb els papers de $x$ i $y$ intercanviats): $f(x_0,y)=x_0^2/y\to\pm\infty$ quan $y\to0^\pm$, mentre que $f(x_0,0)=0$. No existeix el límit a $(x_0,0)$ i $f$ no hi és contínua.
  3. [discontinuitat_origen] Discontinuïtat a l'origen  (teoria: T2.10, T2.14)
     objectiu: Decidir si $f$ és contínua a $(0,0)$.
     idea: Les rectes per l'origen no ho decideixen; busca un camí on numerador i denominador siguin del mateix ordre.
     detall: Sobre la paràbola $y=x^2$: $f(x,x^2)=1\to1\neq0=f(0,0)$. No és contínua a l'origen.
  4. [direccionals_obert] Direccionals fora de l'eix  (teoria: T3.1)
     objectiu: Veure si existeixen les derivades direccionals als punts amb $y_0\neq0$.
     idea: La restricció a una recta pel punt és, a prop del punt, una funció d'una variable derivable.
     detall: Si $y_0\neq0$, $t\mapsto f(x_0+tv_1,y_0+tv_2)=\dfrac{(x_0+tv_1)^2}{y_0+tv_2}$ és quocient de funcions derivables amb denominador no nul prop de $t=0$: totes les direccionals existeixen, $D_vf(x_0,y_0)=\dfrac{2x_0y_0v_1-x_0^2v_2}{y_0^2}$.
  5. [direccionals_eix] Direccionals a l'eix, fora de l'origen  (teoria: T3.1)
     objectiu: Estudiar $D_vf(x_0,0)$ amb $x_0\neq0$ segons la direcció.
     idea: Separa el cas de la direcció horitzontal de la resta i aplica la definició.
     detall: Si $v_2\neq0$: $\dfrac{f(x_0+tv_1,tv_2)}{t}=\dfrac{(x_0+tv_1)^2}{t^2v_2}\to\infty$, no existeix. Si $v_2=0$, la funció val $0$ sobre l'eix i $D_vf(x_0,0)=0$.
  6. [direccionals_origen] Direccionals a l'origen  (teoria: T3.1, T3.6)
     objectiu: Calcular $D_vf(0,0)$ per a tota direcció.
     idea: Aplica la definició de derivada direccional directament a l'origen.
     detall: Si $v_2\neq0$: $\dfrac{f(tv_1,tv_2)}{t}=\dfrac{t^2v_1^2}{t^2v_2}=\dfrac{v_1^2}{v_2}$; si $v_2=0$ val $0$. Totes existeixen, tot i que $f$ no és contínua a l'origen.
ERRORS COMUNS:
  - [direccionals_implica_continuitat] Creu que si existeixen totes les derivades direccionals la funció és contínua.
  - [nomes_rectes] Estudia la continuïtat a l'origen només amb rectes i conclou que és contínua.
  - [oblida_eix] Només estudia l'origen i s'oblida dels altres punts de l'eix $y=0$.
  - [direccio_eix_malament] Als punts $(x_0,0)$ confon quines direccions donen derivada direccional (p. ex. diu que totes o cap).

TEORIA DEL CURS QUE FA SERVIR:
[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T3.1] Definició 1 (Tema 3) — Derivada direccional
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $a\in\mathring{\Omega}$, i $u\in\mathbb{R}^n\setminus\{0\}$. Es defineix la derivada direccional de $f$ en el punt $a$ segons la direcció i sentit del vector $u$ com
$$D_uf(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t},\tag{1}$$
si aquest límit existeix. (Nota: De fet, si definim $g(t)=f(a+tu)$, la funció $f$ restringida a la recta $\{a+tu\mid t\in\mathbb{R}\}$, aleshores $D_uf(a)=g'(0)$.)

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

[T3.6] Observació 6 (Tema 3) — Derivades direccionals sense continuïtat
L'existència de totes les derivades direccionals en un punt $a$, és a dir $D_uf(a)$, $\forall u\neq0$, no implica la continuïtat de $f$ al punt $a$. Ho podem veure en els dos exemples següents:

(a) (vegeu el problema 6 del tema 2) Considerem $A=\left\{(x,y)\in\mathbb{R}^2\mid 0<y<x^2\right\}$ i $f(x,y)$ la funció que val $0$ en $A$ i val $1$ en $A^c$.
Per a aquesta funció, es té que
$$\lim_{x\to0}f(x,mx)=1,\quad m\in\mathbb{R},$$
ja que totes les rectes amb $m\neq0$ (inclosa $x=0$, que no es pot expressar com a $y=mx$ amb $m\in\mathbb{R}$) arriben a l'origen per sobre de la paràbola donada per $y=x^2$, mentre que $y=0$ també pertany a $A^c$. Tanmateix, però, no existeix $\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$. Per tant, no és contínua en $(0,0)$.
Les derivades direccionals en l'origen, en canvi, existeixen totes: efectivament, donat $u=(u_1,u_2)\neq(0,0)$,
$$\begin{aligned}D_uf(0,0)&=\lim_{t\to0}\frac{f((0,0)+t(u_1,u_2))-f(0,0)}{t}=\lim_{t\to0}\frac{f(tu_1,tu_2)-f(0,0)}{t}\\&=\lim_{t\to0}\frac{1-1}{t}=0,\end{aligned}$$

(b) Considerem $f:\mathbb{R}^2\to\mathbb{R}$ definida per
$$f(x,y)=\begin{cases}\dfrac{xy^2}{x^2+y^4} & \text{si } (x,y)\neq(0,0),\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$
Aleshores, donat $u=(u_1,u_2)\neq(0,0)$, vegem que existeix $D_uf(0,0)$:
$$D_uf(0,0)=\lim_{t\to0}\frac{f(tu_1,tu_2)-f(0,0)}{t}=\lim_{t\to0}\frac{(tu_1)(t^2u_2^2)}{t\left((t^2u_1^2)+(t^4u_2^4)\right)}=\lim_{t\to0}\frac{u_1u_2^2}{u_1^2+t^2u_2^4}.$$
Per tant, si $u_1=0$ tenim $D_{(0,u_2)}f(0,0)=0$; d'altra banda, si $u_1\neq0$,
$$D_{(u_1,u_2)}f(0,0)=\frac{u_1u_2^2}{u_1^2}=\frac{u_2^2}{u_1}.$$
En canvi, $f$ no és contínua a $(0,0)$. Per a veure-ho n'hi ha prou a trobar dos camins que condueixin $(x,y)$ al punt $(0,0)$ de manera que els corresponents límits de $f$ siguin diferents. En efecte, si prenem com a primer camí $x=0$, s'obté:
$$\lim_{\substack{(x,y)\to(0,0)\\x=0}}f(x,y)=\lim_{y\to0}f(0,y)=\lim_{y\to0}0=0.$$
Per contra, si prenem el camí $x=y^2$, tenim
$$\lim_{\substack{(x,y)\to(0,0)\\x=y^2}}f(x,y)=\lim_{y\to0}f(y^2,y)=\lim_{y\to0}\frac{y^4}{y^4+y^4}=\lim_{y\to0}\frac{1}{2}=\frac{1}{2}\neq0.$$
Per tant, $\nexists\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$ i, en conseqüència, $f$ no és contínua al punt $(0,0)$. (Nota: De fet, a partir del darrer límit calculat ja hauríem pogut concloure que $f$ no era contínua al $(0,0)$ donat que $f(0,0)=0$.)

[Figura: Superfície generada per la funció del darrer apartat de l'observació 6, prop de l'origen, on s'observen canvis bruscos de pendent en canviar de direcció.]
Figura 2: Representació de la superfície generada per la funció del darrer apartat de l'observació 6, prop de l'origen. Observeu els canvis bruscos de pendent al canviar de direcció.
</solucio_de_referencia>

### Document a revisar

[1] A l'obert $U=\{(x,y):y\neq0\}$ la funció coincideix amb $x^2/y$. Com que és un quocient de polinomis i el denominador no s'anul·la en $U$, $f$ és contínua en tots aquests punts.
[2] Considerem ara un punt $(x_0,0)$ amb $x_0\neq0$. Si ens hi acostem per la recta vertical $x=x_0$, tenim $f(x_0,y)=x_0^2/y$, que no tendeix a cap valor finit quan $y\to0$, mentre que $f(x_0,0)=0$; per tant, $f$ no és contínua en aquests punts.
[3] A l'origen cal mirar algun camí no lineal. Prenent $y=x^2$ amb $x\neq0$, resulta $f(x,x^2)=1$, de manera que el límit al llarg d'aquest camí és $1\neq0=f(0,0)$; així doncs, tampoc és contínua a $(0,0)$.
[4] Si $y_0\neq0$, per a $t$ prou petit el denominador $y_0+tv_2$ continua sent no nul, i la funció d'una variable $t\mapsto f(x_0+tv_1,y_0+tv_2)$ és derivable a $0$. Aplicant la regla del quocient s'obté $D_vf(x_0,y_0)=\frac{2x_0y_0v_1+x_0^2v_2}{y_0^2}$, de manera que existeixen totes les derivades direccionals fora de l'eix.
[5] Per a $(x_0,0)$ amb $x_0\neq0$, si $v_2\neq0$ aleshores $\frac{f(x_0+tv_1,tv_2)-f(x_0,0)}{t}=\frac{(x_0+tv_1)^2}{t^2v_2}$. El terme dominant és $\frac{x_0^2}{t^2v_2}$, de manera que els dos límits laterals són de signes oposats i no hi ha límit finit; si $v_2=0$, el recorregut queda sobre l'eix i la derivada direccional val $0$.
[6] A l'origen, si $v_2\neq0$, la definició dona $\frac{f(tv_1,tv_2)-f(0,0)}{t}$, que queda $\frac{t^2v_1^2}{t^2|v_2|}=\frac{v_1^2}{|v_2|}$. Si $v_2=0$, tots els punts $(tv_1,0)$ són a l'eix i el quocient incremental és $0$, així que en aquest punt existeixen totes les derivades direccionals.
[7] En resum, $f$ és contínua exactament fora de l'eix $y=0$. Les derivades direccionals existeixen totes quan $y_0\neq0$, a l'eix fora de l'origen només en direccions horitzontals, i a l'origen existeixen en totes les direccions; per tant, tenir totes les derivades direccionals en un punt no garanteix la continuïtat.


## t3-5:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Estudieu la continuïtat i l'existència de derivades direccionals a $\mathbb{R}^2$ de la funció
$$f(x,y)=\begin{cases}\dfrac{x^2}{y} & \text{si } y\neq0\\ 0 & \text{si } y=0.\end{cases}$$
RESULTAT CORRECTE: $f$ és contínua exactament a $\{y\neq0\}$ (discontínua a tots els punts de l'eix $y=0$, inclòs l'origen). Derivades direccionals: si $y_0\neq0$ existeixen totes; a $(x_0,0)$ amb $x_0\neq0$ només existeixen en direccions horitzontals ($v_2=0$), i valen $0$; a l'origen existeixen totes: $D_vf(0,0)=v_1^2/v_2$ si $v_2\neq0$ i $0$ si $v_2=0$. Per tant, l'existència de totes les derivades direccionals no implica continuïtat.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [continuitat_obert] Continuïtat fora de l'eix  (teoria: T2.20)
     objectiu: Veure on la funció és clarament contínua.
     idea: Allà on $y\neq0$ la funció ve donada per una sola expressió coneguda, en un obert.
     detall: A l'obert $U=\{y\neq0\}$, $f=x^2/y$ és quocient de polinomis amb denominador no nul, per tant és contínua.
  2. [discontinuitat_eix] Discontinuïtat a l'eix, fora de l'origen  (teoria: T2.10, T2.14)
     objectiu: Estudiar la continuïtat als punts $(x_0,0)$ amb $x_0\neq0$.
     idea: Restringeix la funció a una recta que passi pel punt i no sigui l'eix.
     detall: Sobre la recta vertical $x=x_0$ (Proposició 10 amb els papers de $x$ i $y$ intercanviats): $f(x_0,y)=x_0^2/y\to\pm\infty$ quan $y\to0^\pm$, mentre que $f(x_0,0)=0$. No existeix el límit a $(x_0,0)$ i $f$ no hi és contínua.
  3. [discontinuitat_origen] Discontinuïtat a l'origen  (teoria: T2.10, T2.14)
     objectiu: Decidir si $f$ és contínua a $(0,0)$.
     idea: Les rectes per l'origen no ho decideixen; busca un camí on numerador i denominador siguin del mateix ordre.
     detall: Sobre la paràbola $y=x^2$: $f(x,x^2)=1\to1\neq0=f(0,0)$. No és contínua a l'origen.
  4. [direccionals_obert] Direccionals fora de l'eix  (teoria: T3.1)
     objectiu: Veure si existeixen les derivades direccionals als punts amb $y_0\neq0$.
     idea: La restricció a una recta pel punt és, a prop del punt, una funció d'una variable derivable.
     detall: Si $y_0\neq0$, $t\mapsto f(x_0+tv_1,y_0+tv_2)=\dfrac{(x_0+tv_1)^2}{y_0+tv_2}$ és quocient de funcions derivables amb denominador no nul prop de $t=0$: totes les direccionals existeixen, $D_vf(x_0,y_0)=\dfrac{2x_0y_0v_1-x_0^2v_2}{y_0^2}$.
  5. [direccionals_eix] Direccionals a l'eix, fora de l'origen  (teoria: T3.1)
     objectiu: Estudiar $D_vf(x_0,0)$ amb $x_0\neq0$ segons la direcció.
     idea: Separa el cas de la direcció horitzontal de la resta i aplica la definició.
     detall: Si $v_2\neq0$: $\dfrac{f(x_0+tv_1,tv_2)}{t}=\dfrac{(x_0+tv_1)^2}{t^2v_2}\to\infty$, no existeix. Si $v_2=0$, la funció val $0$ sobre l'eix i $D_vf(x_0,0)=0$.
  6. [direccionals_origen] Direccionals a l'origen  (teoria: T3.1, T3.6)
     objectiu: Calcular $D_vf(0,0)$ per a tota direcció.
     idea: Aplica la definició de derivada direccional directament a l'origen.
     detall: Si $v_2\neq0$: $\dfrac{f(tv_1,tv_2)}{t}=\dfrac{t^2v_1^2}{t^2v_2}=\dfrac{v_1^2}{v_2}$; si $v_2=0$ val $0$. Totes existeixen, tot i que $f$ no és contínua a l'origen.
ERRORS COMUNS:
  - [direccionals_implica_continuitat] Creu que si existeixen totes les derivades direccionals la funció és contínua.
  - [nomes_rectes] Estudia la continuïtat a l'origen només amb rectes i conclou que és contínua.
  - [oblida_eix] Només estudia l'origen i s'oblida dels altres punts de l'eix $y=0$.
  - [direccio_eix_malament] Als punts $(x_0,0)$ confon quines direccions donen derivada direccional (p. ex. diu que totes o cap).

TEORIA DEL CURS QUE FA SERVIR:
[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T3.1] Definició 1 (Tema 3) — Derivada direccional
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $a\in\mathring{\Omega}$, i $u\in\mathbb{R}^n\setminus\{0\}$. Es defineix la derivada direccional de $f$ en el punt $a$ segons la direcció i sentit del vector $u$ com
$$D_uf(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t},\tag{1}$$
si aquest límit existeix. (Nota: De fet, si definim $g(t)=f(a+tu)$, la funció $f$ restringida a la recta $\{a+tu\mid t\in\mathbb{R}\}$, aleshores $D_uf(a)=g'(0)$.)

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

[T3.6] Observació 6 (Tema 3) — Derivades direccionals sense continuïtat
L'existència de totes les derivades direccionals en un punt $a$, és a dir $D_uf(a)$, $\forall u\neq0$, no implica la continuïtat de $f$ al punt $a$. Ho podem veure en els dos exemples següents:

(a) (vegeu el problema 6 del tema 2) Considerem $A=\left\{(x,y)\in\mathbb{R}^2\mid 0<y<x^2\right\}$ i $f(x,y)$ la funció que val $0$ en $A$ i val $1$ en $A^c$.
Per a aquesta funció, es té que
$$\lim_{x\to0}f(x,mx)=1,\quad m\in\mathbb{R},$$
ja que totes les rectes amb $m\neq0$ (inclosa $x=0$, que no es pot expressar com a $y=mx$ amb $m\in\mathbb{R}$) arriben a l'origen per sobre de la paràbola donada per $y=x^2$, mentre que $y=0$ també pertany a $A^c$. Tanmateix, però, no existeix $\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$. Per tant, no és contínua en $(0,0)$.
Les derivades direccionals en l'origen, en canvi, existeixen totes: efectivament, donat $u=(u_1,u_2)\neq(0,0)$,
$$\begin{aligned}D_uf(0,0)&=\lim_{t\to0}\frac{f((0,0)+t(u_1,u_2))-f(0,0)}{t}=\lim_{t\to0}\frac{f(tu_1,tu_2)-f(0,0)}{t}\\&=\lim_{t\to0}\frac{1-1}{t}=0,\end{aligned}$$

(b) Considerem $f:\mathbb{R}^2\to\mathbb{R}$ definida per
$$f(x,y)=\begin{cases}\dfrac{xy^2}{x^2+y^4} & \text{si } (x,y)\neq(0,0),\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$
Aleshores, donat $u=(u_1,u_2)\neq(0,0)$, vegem que existeix $D_uf(0,0)$:
$$D_uf(0,0)=\lim_{t\to0}\frac{f(tu_1,tu_2)-f(0,0)}{t}=\lim_{t\to0}\frac{(tu_1)(t^2u_2^2)}{t\left((t^2u_1^2)+(t^4u_2^4)\right)}=\lim_{t\to0}\frac{u_1u_2^2}{u_1^2+t^2u_2^4}.$$
Per tant, si $u_1=0$ tenim $D_{(0,u_2)}f(0,0)=0$; d'altra banda, si $u_1\neq0$,
$$D_{(u_1,u_2)}f(0,0)=\frac{u_1u_2^2}{u_1^2}=\frac{u_2^2}{u_1}.$$
En canvi, $f$ no és contínua a $(0,0)$. Per a veure-ho n'hi ha prou a trobar dos camins que condueixin $(x,y)$ al punt $(0,0)$ de manera que els corresponents límits de $f$ siguin diferents. En efecte, si prenem com a primer camí $x=0$, s'obté:
$$\lim_{\substack{(x,y)\to(0,0)\\x=0}}f(x,y)=\lim_{y\to0}f(0,y)=\lim_{y\to0}0=0.$$
Per contra, si prenem el camí $x=y^2$, tenim
$$\lim_{\substack{(x,y)\to(0,0)\\x=y^2}}f(x,y)=\lim_{y\to0}f(y^2,y)=\lim_{y\to0}\frac{y^4}{y^4+y^4}=\lim_{y\to0}\frac{1}{2}=\frac{1}{2}\neq0.$$
Per tant, $\nexists\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$ i, en conseqüència, $f$ no és contínua al punt $(0,0)$. (Nota: De fet, a partir del darrer límit calculat ja hauríem pogut concloure que $f$ no era contínua al $(0,0)$ donat que $f(0,0)=0$.)

[Figura: Superfície generada per la funció del darrer apartat de l'observació 6, prop de l'origen, on s'observen canvis bruscos de pendent en canviar de direcció.]
Figura 2: Representació de la superfície generada per la funció del darrer apartat de l'observació 6, prop de l'origen. Observeu els canvis bruscos de pendent al canviar de direcció.
</solucio_de_referencia>

### Document a revisar

[1] 1. En el conjunt obert $U=\{(x,y):y\neq 0\}$, la funció està donada per $f(x,y)=x^2/y$. Com que és un quocient de polinomis i el denominador no s'anul·la, $f$ és contínua en tots els punts de $U$.
[2] 2. Considerem ara un punt $(x_0,0)$ amb $x_0\neq 0$. Si ens hi acostem per la recta vertical $x=x_0$, tenim $f(x_0,y)=x_0^2/y$, que no té límit finit quan $y\to 0$, mentre que $f(x_0,0)=0$; per tant $f$ no és contínua en aquests punts.
[3] 3. A l'origen, sobre qualsevol recta $y=mx$ amb $m\neq 0$ s'obté $f(x,mx)=x/m\to 0$, i sobre l'eix $y=0$ també val $0$. Així, el límit a $(0,0)$ és $0=f(0,0)$ i $f$ és contínua a l'origen.
[4] 4. Si $y_0\neq 0$, per a $t$ prou petit també es té $y_0+tv_2\neq 0$. Aleshores $t\mapsto f(x_0+tv_1,y_0+tv_2)$ és derivable a prop de $0$, i per tant totes les derivades direccionals existeixen, amb valor $D_vf(x_0,y_0)=\frac{2x_0y_0v_1-x_0^2v_2}{y_0^2}$.
[5] 5. Siguem ara a $(x_0,0)$ amb $x_0\neq 0$ i calculem la derivada en una direcció $v=(v_1,v_2)$. Si $v_2\neq 0$, $\frac{f(x_0+tv_1,tv_2)-f(x_0,0)}{t}=\frac{(x_0+tv_1)^2}{t^2v_2}$, que divergeix quan $t\to 0$, de manera que la derivada direccional no existeix.
[6] 6. En canvi, si $v_2=0$, el segment queda dins l'eix $y=0$ i $f(x_0+tv_1,0)=0$. Per tant $\frac{f(x_0+tv_1,0)-f(x_0,0)}{t}=0$ i $D_vf(x_0,0)=0$ per a les direccions horitzontals.
[7] 7. A l'origen, si $v_2\neq 0$, tenim $\frac{f(tv_1,tv_2)-f(0,0)}{t}=\frac{t^2v_1^2/(tv_2)}{t}=\frac{v_1^2}{v_2}$. Si $v_2=0$, el camí és l'eix i el quocient incremental val $0$, de manera que existeixen totes les derivades direccionals a $(0,0)$.
[8] 8. En conclusió, $f$ és contínua a $\{y\neq0\}\cup\{(0,0)\}$ i és discontínua a la resta de l'eix $y=0$. Les derivades direccionals existeixen totes fora de l'eix i a l'origen, mentre que als punts $(x_0,0)$ amb $x_0\neq0$ només existeixen en direccions horitzontals.

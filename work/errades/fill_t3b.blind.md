## t3-19:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem $g(x,y)=f(x,y)+x+2y$, on $f(x,y)$ és la funció de l'exercici anterior. Calculeu les derivades parcials de $g(x,y)$ a l'origen. Comproveu que, usant la matriu de les derivades parcials, no se satisfà la condició de diferenciabilitat a l'origen. És $z=x+2y+1$ el pla tangent a la gràfica de la funció $g(x,y)$?
RESULTAT CORRECTE: $\frac{\partial g}{\partial x}(0,0)=1$, $\frac{\partial g}{\partial y}(0,0)=2$ ($g(0,0)=1$). Amb la matriu $(1\ \ 2)$, el quocient $\frac{|g(x,y)-1-x-2y|}{\|(x,y)\|}=\frac{|f(x,y)-1|}{\|(x,y)\|}$ val $\frac{1}{\|(x,y)\|}\to\infty$ sobre punts de $A$ (p. ex. $y=x^2/2$), així que no tendeix a $0$: $g$ no és diferenciable a l'origen. Per tant, $z=x+2y+1$ no és el pla tangent: la gràfica no en té (tot i que aquest pla conté les rectes tangents en totes les direccions, ja que $D_ug(0,0)=u_1+2u_2$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [parcials] Derivades parcials a l'origen  (teoria: T3.2)
     objectiu: Calcular $\frac{\partial g}{\partial x}(0,0)$ i $\frac{\partial g}{\partial y}(0,0)$.
     idea: Aplica la definició de derivada parcial; recorda quant val $f$ sobre els eixos prop de l'origen.
     detall: Sobre els eixos $f=1$ (no són a $A$), i $g(0,0)=1$. $\frac{\partial g}{\partial x}(0,0)=\lim_{t\to0}\frac{1+t-1}{t}=1$, $\frac{\partial g}{\partial y}(0,0)=\lim_{t\to0}\frac{1+2t-1}{t}=2$.
  2. [quocient] Plantejar la condició de diferenciabilitat  (teoria: T3.8, T3.9)
     objectiu: Escriure el quocient de la definició de diferenciabilitat amb la matriu de les parcials i simplificar-lo.
     idea: L'única candidata a diferencial és la de matriu $(1\ \ 2)$; substitueix $g=f+x+2y$ al numerador.
     detall: $\frac{|g(x,y)-g(0,0)-x-2y|}{\|(x,y)\|}=\frac{|f(x,y)-1|}{\|(x,y)\|}$.
  3. [no_diferenciable] El quocient no tendeix a 0  (teoria: T3.8, T2.10)
     objectiu: Comprovar que aquest quocient no tendeix a $0$.
     idea: Acosta't a l'origen per un camí que quedi dins de $A$.
     detall: Sobre $y=x^2/2$ ($x\neq0$), que és dins de $A$: el quocient val $\frac{1}{\|(x,x^2/2)\|}\to+\infty$. No tendeix a $0$; $g$ no és diferenciable a l'origen.
  4. [pla_tangent] És el pla tangent?  (teoria: T3.9, T3.14)
     objectiu: Decidir si $z=x+2y+1$ és el pla tangent a la gràfica de $g$ a l'origen.
     idea: Recorda per a quines funcions està definit el pla tangent a la gràfica. Què fa aquest pla amb les derivades direccionals?
     detall: El pla tangent només existeix si $g$ és diferenciable al punt, i no ho és: $z=x+2y+1$ no és el pla tangent. És el pla que formaria la candidata ($g(0,0)+Jg$), i conté les rectes tangents a les seccions per totes les rectes ($D_ug(0,0)=u_1+2u_2$), però no aproxima la gràfica (que ni tan sols és contínua a l'origen).
ERRORS COMUNS:
  - [parcials_implica_pla] Creu que si existeixen les parcials ja hi ha pla tangent.
  - [g_origen] Pren $g(0,0)=0$.
  - [rectes_per_diferenciabilitat] Estudia el quocient de diferenciabilitat només sobre rectes i conclou que tendeix a $0$.

TEORIA DEL CURS QUE FA SERVIR:
[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

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

[1] Recordem que $A=\{(x,y)\in\mathbb{R}^2: 0<y<x^2\}$ i que $f$ val $0$ a $A$ i $1$ fora de $A$. L'origen no és de $A$, per tant $f(0,0)=1$ i $g(0,0)=f(0,0)+0+0=1$.
[2] Cap punt dels eixos és de $A$ (sobre $y=0$ falla $0<y$, i sobre $x=0$ caldria $0<y<0$), així que $g(t,0)=1+t$ i $g(0,t)=1+2t$. Per tant $\dfrac{\partial g}{\partial x}(0,0)=\lim_{t\to0}\dfrac{1+t-1}{t}=1$ i $\dfrac{\partial g}{\partial y}(0,0)=\lim_{t\to0}\dfrac{1+2t-1}{t}=2$.
[3] Si $g$ fos diferenciable a l'origen, la seva diferencial tindria matriu $(1\ \ 2)$; per tant $g$ és diferenciable a l'origen si i només si $\dfrac{|g(x,y)-g(0,0)-x-2y|}{\|(x,y)\|}=\dfrac{|f(x,y)-1|}{\|(x,y)\|}$ tendeix a $0$ quan $(x,y)\to(0,0)$.
[4] Prenem els punts de la paràbola $y=2x^2$, $x\neq0$, que és dins de $A$: allà $f=0$ i el quocient val $\dfrac{1}{\|(x,2x^2)\|}\to+\infty$. Per tant el quocient no tendeix a $0$ i $g$ no és diferenciable a l'origen.
[5] Observem que el problema no és de continuïtat: $g$ és contínua a l'origen, ja que sobre qualsevol recta per l'origen $g(x,y)\to1=g(0,0)$.
[6] Per a un vector unitari $u=(u_1,u_2)$, el punt $tu$ seria de $A$ només si $0<tu_2<t^2u_1^2$, cosa impossible si $u_1u_2=0$ o si $|t|<|u_2|/u_1^2$. Així, per a $t$ petit, $g(tu)=1+tu_1+2tu_2$ i $D_ug(0,0)=u_1+2u_2$: el pla $z=x+2y+1$ conté les rectes tangents a totes aquestes seccions.
[7] Però el pla tangent a la gràfica només existeix quan la funció és diferenciable al punt. Com que $g$ no ho és a l'origen, $z=x+2y+1$ no és el pla tangent a la gràfica de $g$ a $(0,0,1)$: la gràfica no en té.


## t3-20:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Calculeu les derivades parcials de la funció $f(x,y,z)=g(u(x,y,z),v(x,y,z))$, on $g(u,v)=uv^2+\sin(uv)$, $u(x,y,z)=xe^y$ i $v(x,y,z)=xy-z$.
RESULTAT CORRECTE: Amb $u=xe^y$, $v=xy-z$, $g_u=v^2+v\cos(uv)$, $g_v=2uv+u\cos(uv)$:
$\frac{\partial f}{\partial x}=\big(v^2+v\cos(uv)\big)e^y+\big(2uv+u\cos(uv)\big)y$,
$\frac{\partial f}{\partial y}=\big(v^2+v\cos(uv)\big)xe^y+\big(2uv+u\cos(uv)\big)x$,
$\frac{\partial f}{\partial z}=-\big(2uv+u\cos(uv)\big)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [diferenciabilitat] Justificar la regla de la cadena  (teoria: T3.18, T3.21)
     objectiu: Comprovar que es pot aplicar la regla de la cadena.
     idea: Mira si les funcions interior i exterior són diferenciables.
     detall: $g$, $u$ i $v$ tenen parcials contínues a tot l'espai, per tant són diferenciables, i $f=g\circ(u,v)$ també ho és.
  2. [parcials_g] Parcials de la funció exterior
     objectiu: Calcular $\frac{\partial g}{\partial u}$ i $\frac{\partial g}{\partial v}$.
     idea: Deriva $g$ tractant l'altra variable com a constant.
     detall: $\frac{\partial g}{\partial u}=v^2+v\cos(uv)$, $\frac{\partial g}{\partial v}=2uv+u\cos(uv)$.
  3. [parcials_interiors] Parcials de les funcions interiors
     objectiu: Calcular les parcials de $u$ i $v$ respecte de $x$, $y$, $z$.
     idea: Són derivades directes.
     detall: $u_x=e^y$, $u_y=xe^y$, $u_z=0$; $v_x=y$, $v_y=x$, $v_z=-1$.
  4. [cadena] Aplicar la regla de la cadena  (teoria: T3.21, T3.22)
     objectiu: Combinar-ho tot per obtenir les tres parcials de $f$.
     idea: Cada parcial de $f$ és una suma sobre les variables intermèdies (producte de la jacobiana de $g$ per la de $(u,v)$).
     detall: $\frac{\partial f}{\partial x}=g_ue^y+g_vy$, $\frac{\partial f}{\partial y}=g_uxe^y+g_vx$, $\frac{\partial f}{\partial z}=-g_v$, amb $g_u=v^2+v\cos(uv)$, $g_v=2uv+u\cos(uv)$ avaluades a $u=xe^y$, $v=xy-z$.
ERRORS COMUNS:
  - [oblida_terme] Oblida un dels termes de la suma (p. ex. només deriva a través de $u$).
  - [no_avalua] Deixa les parcials de $g$ sense avaluar a $(u(x,y,z),v(x,y,z))$ o les avalua al punt $(x,y)$.
  - [signe_z] Oblida el signe de $v_z=-1$.

TEORIA DEL CURS QUE FA SERVIR:
[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$

[T3.22] Observació 22 (Tema 3) — Regla de la cadena com a producte de jacobianes
La fórmula (10) ve de la multiplicació de les corresponents matrius jacobianes. Fem-ho, com a mostra, en el següent cas:
$$\mathbb{R}^2\xrightarrow{\ f\ }\mathbb{R}^3\xrightarrow{\ g\ }\mathbb{R}$$
$$(u,v)\longmapsto\begin{pmatrix}f_1(u,v)\\f_2(u,v)\\f_3(u,v)\end{pmatrix},\qquad(x,y,z)\longmapsto g(x,y,z)$$
Observeu que
$$(g\circ f)(u,v)=g(f(u,v))=g(f_1(u,v),f_2(u,v),f_3(u,v))$$
i, per tant,
$$\begin{aligned}\frac{\partial}{\partial u}(g\circ f)(u,v)&=\frac{\partial g}{\partial x}(f(u,v))\frac{\partial f_1}{\partial u}(u,v)+\frac{\partial g}{\partial y}(f(u,v))\frac{\partial f_2}{\partial u}(u,v)+\frac{\partial g}{\partial z}(f(u,v))\frac{\partial f_3}{\partial u}(u,v),\\\frac{\partial}{\partial v}(g\circ f)(u,v)&=\frac{\partial g}{\partial x}(f(u,v))\frac{\partial f_1}{\partial v}(u,v)+\frac{\partial g}{\partial y}(f(u,v))\frac{\partial f_2}{\partial v}(u,v)+\frac{\partial g}{\partial z}(f(u,v))\frac{\partial f_3}{\partial v}(u,v).\end{aligned}$$
Aquestes expressions són les mateixes que s'obtenen al fer el producte de les corresponents matrius jacobianes:
$$\begin{aligned}J(g\circ f)(u,v)&=Jg(f(u,v))\cdot Jf(u,v)=\\&=\left(\frac{\partial g}{\partial x}(f(u,v))\ \ \frac{\partial g}{\partial y}(f(u,v))\ \ \frac{\partial g}{\partial z}(f(u,v))\right)\begin{pmatrix}\dfrac{\partial f_1}{\partial u}(u,v)&\dfrac{\partial f_1}{\partial v}(u,v)\\\dfrac{\partial f_2}{\partial u}(u,v)&\dfrac{\partial f_2}{\partial v}(u,v)\\\dfrac{\partial f_3}{\partial u}(u,v)&\dfrac{\partial f_3}{\partial v}(u,v)\end{pmatrix}\\&=\left(\frac{\partial(g\circ f)}{\partial u}(u,v)\ \ \frac{\partial(g\circ f)}{\partial v}(u,v)\right).\end{aligned}$$
</solucio_de_referencia>

### Document a revisar

[1] Les funcions $g(u,v)=uv^2+\sin(uv)$, $u(x,y,z)=xe^y$ i $v(x,y,z)=xy-z$ tenen derivades parcials contínues a tot l'espai, per tant són diferenciables, i per la regla de la cadena $f=g\circ(u,v)$ també ho és.
[2] Les parcials de $g$ són $\dfrac{\partial g}{\partial u}=v^2+\cos(uv)$ i $\dfrac{\partial g}{\partial v}=2uv+u\cos(uv)$.
[3] Les parcials de les funcions interiors són $u_x=e^y$, $u_y=xe^y$, $u_z=0$ i $v_x=y$, $v_y=x$, $v_z=-1$.
[4] Per la regla de la cadena, $\dfrac{\partial f}{\partial x}=\dfrac{\partial g}{\partial u}\,u_x+\dfrac{\partial g}{\partial v}\,v_x=\dfrac{\partial g}{\partial u}\,e^y+\dfrac{\partial g}{\partial v}\,y$.
[5] Respecte de $y$: $\dfrac{\partial f}{\partial y}=\dfrac{\partial g}{\partial u}\,xe^y+\dfrac{\partial g}{\partial v}\,y$.
[6] Respecte de $z$: $\dfrac{\partial f}{\partial z}=\dfrac{\partial g}{\partial u}\cdot0+\dfrac{\partial g}{\partial v}\cdot(-1)=-\dfrac{\partial g}{\partial v}$.
[7] En les tres fórmules, les parcials de $g$ s'avaluen al punt $(u,v)=(xe^y,xy-z)$. Per exemple, $\dfrac{\partial f}{\partial z}=-2xe^y(xy-z)-xe^y\cos\big(xe^y(xy-z)\big)$.


## t3-23:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem la funció $f(x,y)=(\sin(y\log x),(y\log x)^2)$ definida a $D=\{(x,y)\in\mathbb{R}^2:x>0\}$. Determineu dues funcions $g:\mathbb{R}\to\mathbb{R}^2$ i $h:D\to\mathbb{R}$ tals que $f=g\circ h$ i useu la regla de la cadena per calcular $Df(x,y)$.

Considerem la funció $f(x,y)=(\sin(y\log x),(y\log x)^2)$ definida a $D=\{(x,y)\in\mathbb{R}^2:x>0\}$. Determineu dues funcions $g:\mathbb{R}\to\mathbb{R}^2$ i $h:D\to\mathbb{R}$ tals que $f=g\circ h$ i useu la regla de la cadena per calcular $Df(x,y)$.
RESULTAT CORRECTE: $h(x,y)=y\log x$, $g(s)=(\sin s,s^2)$. Llavors
$Jf(x,y)=Jg(h(x,y))\,Jh(x,y)=\begin{pmatrix}\cos(y\log x)\\ 2y\log x\end{pmatrix}\begin{pmatrix}\frac{y}{x} & \log x\end{pmatrix}=\begin{pmatrix}\frac{y}{x}\cos(y\log x) & \log x\cos(y\log x)\\ \frac{2y^2\log x}{x} & 2y(\log x)^2\end{pmatrix}$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [descomposicio] Trobar $g$ i $h$
     objectiu: Escriure $f$ com a composició $g\circ h$ amb $h$ a valors reals i $g$ d'una variable.
     idea: Busca l'expressió que es repeteix dins de les dues components de $f$: aquesta serà la funció interior.
     detall: $h(x,y)=y\log x$ (definida a $D$, on $x>0$) i $g(s)=(\sin s,s^2)$. Llavors $g(h(x,y))=(\sin(y\log x),(y\log x)^2)=f(x,y)$.
  2. [diferenciabilitat] Comprovar les hipòtesis  (teoria: T3.18, T3.23)
     objectiu: Justificar que $g$ i $h$ són diferenciables, per poder aplicar la regla de la cadena.
     idea: Escriu cada funció a partir de funcions elementals que ja saps diferenciables (o mira si les seves parcials són contínues) i usa les propietats algebraiques de la diferenciabilitat.
     detall: $h(x,y)=y\log x$ és el producte de $(x,y)\mapsto y$ i $(x,y)\mapsto\log x$, que tenen derivades parcials contínues a l'obert $D$ (on $x>0$) i per tant són diferenciables a $D$; pel producte de funcions diferenciables, $h$ és diferenciable a $D$. Les components de $g$, $\sin s$ i $s^2$, són derivables amb derivada contínua a tot $\mathbb{R}$, per tant $g$ és diferenciable a $\mathbb{R}$.
  3. [jacobianes] Jacobianes de $g$ i $h$  (teoria: T3.10)
     objectiu: Calcular $Jh(x,y)$ i $Jg(s)$, indicant la mida de cada matriu.
     idea: $h$ va de $\mathbb{R}^2$ a $\mathbb{R}$ i $g$ de $\mathbb{R}$ a $\mathbb{R}^2$: una és una fila i l'altra una columna.
     detall: $Jh(x,y)=\begin{pmatrix}\frac{y}{x} & \log x\end{pmatrix}$ ($1\times2$) i $Jg(s)=\begin{pmatrix}\cos s\\ 2s\end{pmatrix}$ ($2\times1$).
  4. [producte] Aplicar la regla de la cadena  (teoria: T3.21, T3.22)
     objectiu: Obtenir la matriu $Jf(x,y)$.
     idea: Multiplica les jacobianes en l'ordre que dona la regla de la cadena, avaluant la de $g$ al punt $h(x,y)$.
     detall: $Jf(x,y)=Jg(y\log x)\,Jh(x,y)=\begin{pmatrix}\cos(y\log x)\\ 2y\log x\end{pmatrix}\begin{pmatrix}\frac{y}{x} & \log x\end{pmatrix}=\begin{pmatrix}\frac{y}{x}\cos(y\log x) & \log x\cos(y\log x)\\ \frac{2y^2\log x}{x} & 2y(\log x)^2\end{pmatrix}$ (matriu $2\times2$).
ERRORS COMUNS:
  - [ordre_producte] Multiplica les jacobianes en l'ordre $Jh\cdot Jg$ (obtenint un nombre en lloc d'una matriu $2\times2$).
  - [avalua_g_malament] Avalua $Jg$ a $(x,y)$ o a $s$ genèric en lloc de a $h(x,y)=y\log x$.
  - [descomposicio_invertida] Intercanvia els papers de $g$ i $h$, o tria una $h$ que no fa la composició igual a $f$.

TEORIA DEL CURS QUE FA SERVIR:
[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$

[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

[T3.23] Proposició 23 (Tema 3) — Àlgebra de funcions diferenciables
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciables en $a\in\mathring{\Omega}$ i sigui $\lambda\in\mathbb{R}$. Llavors,

(i) $f+g$ és diferenciable en $a$ i $D(f+g)(a)=Df(a)+Dg(a)$.

(ii) $\lambda f$ és diferenciable en $a$ i $D(\lambda f)(a)=\lambda Df(a)$.

(iii) $fg$ és diferenciable en $a$ i $J(fg)(a)=g(a)Jf(a)+f(a)Jg(a)$.

(iv) $\dfrac{f}{g}$ és diferenciable en $a$ si $g(a)\neq0$. A més
$$J\left(\frac{f}{g}\right)(a)=\frac{g(a)Jf(a)-f(a)Jg(a)}{g(a)^2}.$$

[T3.22] Observació 22 (Tema 3) — Regla de la cadena com a producte de jacobianes
La fórmula (10) ve de la multiplicació de les corresponents matrius jacobianes. Fem-ho, com a mostra, en el següent cas:
$$\mathbb{R}^2\xrightarrow{\ f\ }\mathbb{R}^3\xrightarrow{\ g\ }\mathbb{R}$$
$$(u,v)\longmapsto\begin{pmatrix}f_1(u,v)\\f_2(u,v)\\f_3(u,v)\end{pmatrix},\qquad(x,y,z)\longmapsto g(x,y,z)$$
Observeu que
$$(g\circ f)(u,v)=g(f(u,v))=g(f_1(u,v),f_2(u,v),f_3(u,v))$$
i, per tant,
$$\begin{aligned}\frac{\partial}{\partial u}(g\circ f)(u,v)&=\frac{\partial g}{\partial x}(f(u,v))\frac{\partial f_1}{\partial u}(u,v)+\frac{\partial g}{\partial y}(f(u,v))\frac{\partial f_2}{\partial u}(u,v)+\frac{\partial g}{\partial z}(f(u,v))\frac{\partial f_3}{\partial u}(u,v),\\\frac{\partial}{\partial v}(g\circ f)(u,v)&=\frac{\partial g}{\partial x}(f(u,v))\frac{\partial f_1}{\partial v}(u,v)+\frac{\partial g}{\partial y}(f(u,v))\frac{\partial f_2}{\partial v}(u,v)+\frac{\partial g}{\partial z}(f(u,v))\frac{\partial f_3}{\partial v}(u,v).\end{aligned}$$
Aquestes expressions són les mateixes que s'obtenen al fer el producte de les corresponents matrius jacobianes:
$$\begin{aligned}J(g\circ f)(u,v)&=Jg(f(u,v))\cdot Jf(u,v)=\\&=\left(\frac{\partial g}{\partial x}(f(u,v))\ \ \frac{\partial g}{\partial y}(f(u,v))\ \ \frac{\partial g}{\partial z}(f(u,v))\right)\begin{pmatrix}\dfrac{\partial f_1}{\partial u}(u,v)&\dfrac{\partial f_1}{\partial v}(u,v)\\\dfrac{\partial f_2}{\partial u}(u,v)&\dfrac{\partial f_2}{\partial v}(u,v)\\\dfrac{\partial f_3}{\partial u}(u,v)&\dfrac{\partial f_3}{\partial v}(u,v)\end{pmatrix}\\&=\left(\frac{\partial(g\circ f)}{\partial u}(u,v)\ \ \frac{\partial(g\circ f)}{\partial v}(u,v)\right).\end{aligned}$$
</solucio_de_referencia>

### Document a revisar

[1] Prenem $h:D\to\mathbb{R}$, $h(x,y)=y\log x$ (ben definida perquè $x>0$ a $D$), i $g:\mathbb{R}\to\mathbb{R}^2$, $g(s)=(\sin s,s^2)$. Llavors $g(h(x,y))=(\sin(y\log x),(y\log x)^2)=f(x,y)$.
[2] La funció $h$ té derivades parcials $\dfrac{\partial h}{\partial x}=\dfrac{y}{x}$ i $\dfrac{\partial h}{\partial y}=\log x$ a tot punt de $D$; com que aquestes parcials existeixen a tot $D$, $h$ és diferenciable a $D$.
[3] Les components de $g$, $\sin s$ i $s^2$, són derivables amb derivada contínua a $\mathbb{R}$, per tant $g$ és diferenciable a $\mathbb{R}$, i per la regla de la cadena $f=g\circ h$ és diferenciable a $D$.
[4] Les jacobianes són $Jh(x,y)=\begin{pmatrix}\frac{y}{x} & \log x\end{pmatrix}$ ($1\times2$) i $Jg(s)=\begin{pmatrix}\cos s\\ 2s\end{pmatrix}$ ($2\times1$).
[5] Per la regla de la cadena, $Jf(x,y)=Jg(h(x,y))\,Jh(x,y)=\begin{pmatrix}\cos(y\log x)\\ 2y\log x\end{pmatrix}\begin{pmatrix}\frac{y}{x} & \log x\end{pmatrix}$, producte d'una matriu $2\times1$ per una $1\times2$, que dona la matriu $2\times2$ que correspon a $f:D\subseteq\mathbb{R}^2\to\mathbb{R}^2$.
[6] Multiplicant, la primera fila de $Jf(x,y)$ és $\left(\dfrac{y}{x}\cos(y\log x),\ \log x\cos(y\log x)\right)$ i la segona és $\left(\dfrac{2y\log x}{x},\ 2y(\log x)^2\right)$.


## t3-24:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $f:\mathbb{R}\to\mathbb{R}$ diferenciable. Proveu que la funció $\varphi(x,y)=f(2x+3y)$, definida en $\mathbb{R}^2$, satisfà l'equació en derivades parcials $3\dfrac{\partial\varphi}{\partial x}-2\dfrac{\partial\varphi}{\partial y}=0$.

Sigui $f:\mathbb{R}\to\mathbb{R}$ diferenciable. Proveu que la funció $\varphi(x,y)=f(2x+3y)$, definida en $\mathbb{R}^2$, satisfà l'equació en derivades parcials $3\dfrac{\partial\varphi}{\partial x}-2\dfrac{\partial\varphi}{\partial y}=0$.
RESULTAT CORRECTE: Per la regla de la cadena, $\varphi_x=2f'(2x+3y)$ i $\varphi_y=3f'(2x+3y)$, per tant $3\varphi_x-2\varphi_y=6f'(2x+3y)-6f'(2x+3y)=0$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [composicio] Veure-ho com una composició  (teoria: T3.18)
     objectiu: Identificar $\varphi$ com a composició de dues funcions diferenciables.
     idea: Hi ha una funció "interior" de dues variables i una "exterior" d'una variable.
     detall: $\varphi=f\circ g$ amb $g(x,y)=2x+3y$, lineal (parcials constants $2$ i $3$, contínues) i per tant diferenciable; $f$ és diferenciable per hipòtesi.
  2. [parcials] Aplicar la regla de la cadena  (teoria: T3.21)
     objectiu: Calcular $\varphi_x$ i $\varphi_y$.
     idea: La regla de la cadena multiplica la derivada de la funció exterior (avaluada al punt adequat) per la parcial de la interior.
     detall: $J\varphi(x,y)=f'(2x+3y)\,Jg(x,y)=f'(2x+3y)\begin{pmatrix}2 & 3\end{pmatrix}$, és a dir, $\varphi_x=f'(2x+3y)\cdot 2$ i $\varphi_y=f'(2x+3y)\cdot 3$.
  3. [substituir] Substituir a l'equació
     objectiu: Comprovar l'equació.
     idea: Substitueix les parcials a $3\varphi_x-2\varphi_y$.
     detall: $3\cdot2f'(2x+3y)-2\cdot3f'(2x+3y)=0$ per a tot $(x,y)\in\mathbb{R}^2$.
ERRORS COMUNS:
  - [oblida_factor] Deriva $f(2x+3y)$ oblidant el factor de la derivada interior (regla de la cadena).
  - [cas_particular] Ho comprova per a una $f$ concreta (p. ex. $f(t)=t^2$) en lloc de demostrar-ho en general.
  - [confon_derivades] Confon $f'$ amb $\varphi$ o tracta les dues parcials com a expressions sense relació entre elles.

TEORIA DEL CURS QUE FA SERVIR:
[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$
</solucio_de_referencia>

### Document a revisar

[1] Escrivim $\varphi=f\circ g$ amb $g(x,y)=2x+3y$. La funció $g$ és diferenciable a $\mathbb{R}^2$ perquè és contínua, i $f$ és diferenciable per hipòtesi.
[2] A més, com que $f$ és diferenciable, la seva derivada $f'$ és contínua, i això és el que necessitem per poder aplicar la regla de la cadena a $f\circ g$.
[3] Com que $Jg(x,y)=\begin{pmatrix}2 & 3\end{pmatrix}$, la regla de la cadena dona $J\varphi(x,y)=f'(g(x,y))\,Jg(x,y)=f'(2x+3y)\begin{pmatrix}2 & 3\end{pmatrix}$.
[4] Per tant $\dfrac{\partial\varphi}{\partial x}(x,y)=2f'(2x+3y)$ i $\dfrac{\partial\varphi}{\partial y}(x,y)=3f'(2x+3y)$.
[5] Substituint, $3\dfrac{\partial\varphi}{\partial x}-2\dfrac{\partial\varphi}{\partial y}=6f'(2x+3y)-6f'(2x+3y)=0$ per a tot $(x,y)\in\mathbb{R}^2$, que és el que volíem provar.


## t3-25a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $G$ la funció que dona el canvi de variables a coordenades polars:
$$\begin{aligned}G:\mathbb{R}^+\times(0,2\pi)\subset\mathbb{R}^2&\to\mathbb{R}^2\\(r,\varphi)&\mapsto(r\cos\varphi,r\sin\varphi).\end{aligned}$$

(a) Si $f:\mathbb{R}^2\to\mathbb{R}$ és una funció de classe $\mathcal{C}^1$, obteniu les relacions entre les derivades parcials primeres en els dos sistemes de coordenades; és a dir, si $F=f\circ G$, demostreu que:
$$\frac{\partial F}{\partial r}=\frac{\partial f}{\partial x}\cos\varphi+\frac{\partial f}{\partial y}\sin\varphi,\qquad\frac{\partial F}{\partial\varphi}=-\frac{\partial f}{\partial x}r\sin\varphi+\frac{\partial f}{\partial y}r\cos\varphi,$$
$$\frac{\partial f}{\partial x}=\frac{\partial F}{\partial r}\frac{x}{\sqrt{x^2+y^2}}-\frac{\partial F}{\partial\varphi}\frac{y}{x^2+y^2},\qquad\frac{\partial f}{\partial y}=\frac{\partial F}{\partial r}\frac{y}{\sqrt{x^2+y^2}}+\frac{\partial F}{\partial\varphi}\frac{x}{x^2+y^2}.$$
RESULTAT CORRECTE: Per la regla de la cadena, $JF(r,\varphi)=Jf(G(r,\varphi))\,JG(r,\varphi)$ amb $JG=\begin{pmatrix}\cos\varphi & -r\sin\varphi\\ \sin\varphi & r\cos\varphi\end{pmatrix}$, que dona les dues primeres fórmules (amb les parcials de $f$ avaluades a $(x,y)=G(r,\varphi)$). Com que $\det JG=r>0$, el sistema es pot resoldre: $\frac{\partial f}{\partial x}=\cos\varphi\,\frac{\partial F}{\partial r}-\frac{\sin\varphi}{r}\frac{\partial F}{\partial\varphi}$, $\frac{\partial f}{\partial y}=\sin\varphi\,\frac{\partial F}{\partial r}+\frac{\cos\varphi}{r}\frac{\partial F}{\partial\varphi}$, i substituint $r=\sqrt{x^2+y^2}$, $\cos\varphi=x/r$, $\sin\varphi=y/r$ s'obtenen les dues últimes.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [jacobiana_G] Diferenciabilitat i jacobiana de $G$  (teoria: T3.18, T3.10)
     objectiu: Justificar que es pot aplicar la regla de la cadena a $F=f\circ G$ i calcular la matriu $JG(r,\varphi)$.
     idea: Comprova que $G$ i $f$ són diferenciables (parcials contínues) i escriu la matriu de les parcials de les components de $G$ respecte de $r$ i $\varphi$.
     detall: $f\in\mathcal{C}^1$ és diferenciable, i $G$ té parcials contínues, per tant també ho és. $JG(r,\varphi)=\begin{pmatrix}\cos\varphi & -r\sin\varphi\\ \sin\varphi & r\cos\varphi\end{pmatrix}$.
  2. [cadena] Primeres fórmules  (teoria: T3.21, T3.22)
     objectiu: Obtenir $\frac{\partial F}{\partial r}$ i $\frac{\partial F}{\partial\varphi}$ en termes de les parcials de $f$.
     idea: Escriu $JF(r,\varphi)$ com a producte de la jacobiana de $f$ (avaluada a $G(r,\varphi)$) per la de $G$.
     detall: $\left(\frac{\partial F}{\partial r}\ \ \frac{\partial F}{\partial\varphi}\right)=\left(\frac{\partial f}{\partial x}\ \ \frac{\partial f}{\partial y}\right)\begin{pmatrix}\cos\varphi & -r\sin\varphi\\ \sin\varphi & r\cos\varphi\end{pmatrix}$, amb les parcials de $f$ avaluades a $(r\cos\varphi,r\sin\varphi)$. Multiplicant s'obtenen exactament les dues primeres igualtats de l'enunciat.
  3. [invertir] Aïllar les parcials de $f$
     objectiu: Expressar $\frac{\partial f}{\partial x}$ i $\frac{\partial f}{\partial y}$ en termes de $\frac{\partial F}{\partial r}$, $\frac{\partial F}{\partial\varphi}$, $r$ i $\varphi$.
     idea: Les dues fórmules anteriors són un sistema lineal $2\times2$ en les incògnites $\frac{\partial f}{\partial x}$, $\frac{\partial f}{\partial y}$; mira si la matriu és invertible al domini de $G$.
     detall: El determinant de $JG$ és $r\cos^2\varphi+r\sin^2\varphi=r>0$. Resolent (per exemple, multiplicant la primera per $r\cos\varphi$, la segona per $\sin\varphi$ i restant): $\frac{\partial f}{\partial x}=\cos\varphi\,\frac{\partial F}{\partial r}-\frac{\sin\varphi}{r}\frac{\partial F}{\partial\varphi}$ i $\frac{\partial f}{\partial y}=\sin\varphi\,\frac{\partial F}{\partial r}+\frac{\cos\varphi}{r}\frac{\partial F}{\partial\varphi}$.
  4. [cartesianes] Passar a $x$, $y$
     objectiu: Escriure els coeficients anteriors en funció de $x$ i $y$.
     idea: Usa la relació entre $(r,\varphi)$ i $(x,y)=G(r,\varphi)$.
     detall: $r=\sqrt{x^2+y^2}$, $\cos\varphi=\frac{x}{\sqrt{x^2+y^2}}$, $\sin\varphi=\frac{y}{\sqrt{x^2+y^2}}$, i per tant $\frac{\sin\varphi}{r}=\frac{y}{x^2+y^2}$, $\frac{\cos\varphi}{r}=\frac{x}{x^2+y^2}$. Substituint s'obtenen les dues últimes fórmules.
ERRORS COMUNS:
  - [punt_avaluacio] No distingeix on s'avaluen les parcials: les de $f$ a $(x,y)=G(r,\varphi)$ i les de $F$ a $(r,\varphi)$.
  - [ordre_producte] Multiplica $JG\cdot Jf$ en lloc de $Jf\cdot JG$, o fa servir la transposada de $JG$ sense adonar-se'n.
  - [inversa_per_composicio] Per obtenir les últimes fórmules intenta derivar $\varphi=\arctan(y/x)$, cosa que només val en una part del domini, sense justificar-ho.

TEORIA DEL CURS QUE FA SERVIR:
[T3.20] Definició 20 (Tema 3) — Funció de classe C^1
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $\Omega$ obert. Direm que $f$ és de classe $\mathcal{C}^1(\Omega)$ si $f$ és diferenciable a $\Omega$ i, per a tot punt $a\in\Omega$, existeixen totes les derivades parcials de $f$ al punt $a$ i hi són contínues. De manera anàloga a definicions anteriors, direm que $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $f=(f_1,f_2,\ldots,f_m)$, és de classe $\mathcal{C}^1(\Omega)$ si $f_i\in\mathcal{C}^1(\Omega)$, per a tot $i=1,2,\ldots,m$.

[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$

[T3.22] Observació 22 (Tema 3) — Regla de la cadena com a producte de jacobianes
La fórmula (10) ve de la multiplicació de les corresponents matrius jacobianes. Fem-ho, com a mostra, en el següent cas:
$$\mathbb{R}^2\xrightarrow{\ f\ }\mathbb{R}^3\xrightarrow{\ g\ }\mathbb{R}$$
$$(u,v)\longmapsto\begin{pmatrix}f_1(u,v)\\f_2(u,v)\\f_3(u,v)\end{pmatrix},\qquad(x,y,z)\longmapsto g(x,y,z)$$
Observeu que
$$(g\circ f)(u,v)=g(f(u,v))=g(f_1(u,v),f_2(u,v),f_3(u,v))$$
i, per tant,
$$\begin{aligned}\frac{\partial}{\partial u}(g\circ f)(u,v)&=\frac{\partial g}{\partial x}(f(u,v))\frac{\partial f_1}{\partial u}(u,v)+\frac{\partial g}{\partial y}(f(u,v))\frac{\partial f_2}{\partial u}(u,v)+\frac{\partial g}{\partial z}(f(u,v))\frac{\partial f_3}{\partial u}(u,v),\\\frac{\partial}{\partial v}(g\circ f)(u,v)&=\frac{\partial g}{\partial x}(f(u,v))\frac{\partial f_1}{\partial v}(u,v)+\frac{\partial g}{\partial y}(f(u,v))\frac{\partial f_2}{\partial v}(u,v)+\frac{\partial g}{\partial z}(f(u,v))\frac{\partial f_3}{\partial v}(u,v).\end{aligned}$$
Aquestes expressions són les mateixes que s'obtenen al fer el producte de les corresponents matrius jacobianes:
$$\begin{aligned}J(g\circ f)(u,v)&=Jg(f(u,v))\cdot Jf(u,v)=\\&=\left(\frac{\partial g}{\partial x}(f(u,v))\ \ \frac{\partial g}{\partial y}(f(u,v))\ \ \frac{\partial g}{\partial z}(f(u,v))\right)\begin{pmatrix}\dfrac{\partial f_1}{\partial u}(u,v)&\dfrac{\partial f_1}{\partial v}(u,v)\\\dfrac{\partial f_2}{\partial u}(u,v)&\dfrac{\partial f_2}{\partial v}(u,v)\\\dfrac{\partial f_3}{\partial u}(u,v)&\dfrac{\partial f_3}{\partial v}(u,v)\end{pmatrix}\\&=\left(\frac{\partial(g\circ f)}{\partial u}(u,v)\ \ \frac{\partial(g\circ f)}{\partial v}(u,v)\right).\end{aligned}$$
</solucio_de_referencia>

### Document a revisar

[1] $f$ és de classe $\mathcal{C}^1$, per tant diferenciable, i $G$ té derivades parcials contínues al seu domini obert $\mathbb{R}^+\times(0,2\pi)$, per tant també és diferenciable. Per la regla de la cadena, $F=f\circ G$ és diferenciable.
[2] La jacobiana de $G$ és $JG(r,\varphi)=\begin{pmatrix}\cos\varphi & -r\sin\varphi\\ \sin\varphi & r\cos\varphi\end{pmatrix}$.
[3] Així $\left(\dfrac{\partial F}{\partial r}\ \ \dfrac{\partial F}{\partial\varphi}\right)=\left(\dfrac{\partial f}{\partial x}\ \ \dfrac{\partial f}{\partial y}\right)JG(r,\varphi)$, on les parcials de $f$ s'avaluen al mateix punt $(r,\varphi)$ que les de $F$.
[4] Fent el producte, $\dfrac{\partial F}{\partial r}=\dfrac{\partial f}{\partial x}\cos\varphi+\dfrac{\partial f}{\partial y}\sin\varphi$ i $\dfrac{\partial F}{\partial\varphi}=-\dfrac{\partial f}{\partial x}r\sin\varphi+\dfrac{\partial f}{\partial y}r\cos\varphi$, que són les dues primeres igualtats.
[5] El determinant de $JG$ és $r\cos^2\varphi+r\sin^2\varphi=r>0$, de manera que el sistema es pot resoldre per a $\dfrac{\partial f}{\partial x}$ i $\dfrac{\partial f}{\partial y}$.
[6] Multiplicant la primera igualtat per $r\cos\varphi$ i la segona per $\sin\varphi$, els termes en $\dfrac{\partial f}{\partial y}$ coincideixen (tots dos són $r\sin\varphi\cos\varphi\,\dfrac{\partial f}{\partial y}$) i, sumant les dues igualtats, s'eliminen: $r\dfrac{\partial f}{\partial x}=r\cos\varphi\,\dfrac{\partial F}{\partial r}-\sin\varphi\,\dfrac{\partial F}{\partial\varphi}$, és a dir, $\dfrac{\partial f}{\partial x}=\cos\varphi\,\dfrac{\partial F}{\partial r}-\dfrac{\sin\varphi}{r}\dfrac{\partial F}{\partial\varphi}$.
[7] Anàlogament, multiplicant la primera per $r\sin\varphi$, la segona per $\cos\varphi$ i sumant, $\dfrac{\partial f}{\partial y}=\sin\varphi\,\dfrac{\partial F}{\partial r}+\dfrac{\cos\varphi}{r}\dfrac{\partial F}{\partial\varphi}$.
[8] Finalment, $r=\sqrt{x^2+y^2}$, $\cos\varphi=\dfrac{x}{\sqrt{x^2+y^2}}$ i $\sin\varphi=\dfrac{y}{\sqrt{x^2+y^2}}$, per tant $\dfrac{\sin\varphi}{r}=\dfrac{y}{x^2+y^2}$ i $\dfrac{\cos\varphi}{r}=\dfrac{x}{x^2+y^2}$; substituint s'obtenen les dues últimes fórmules de l'enunciat.


## t3-26a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considereu la funció
$$f(x,y)=\begin{cases}2(x^2+y^2)\sin\left(\dfrac{1}{\sqrt{x^2+y^2}}\right) & \text{si } (x,y)\neq(0,0)\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$

(a) Proveu que existeixen les derivades parcials de $f$, però que no són contínues a $(0,0)$.
RESULTAT CORRECTE: A l'origen, $\frac{\partial f}{\partial x}(0,0)=\lim_{t\to0}2t\sin\frac1{|t|}=0$ i, per simetria, $\frac{\partial f}{\partial y}(0,0)=0$. Fora de l'origen, amb $\rho=\sqrt{x^2+y^2}$: $\frac{\partial f}{\partial x}=4x\sin\frac1\rho-\frac{2x}{\rho}\cos\frac1\rho$ (i anàlogament $\frac{\partial f}{\partial y}$ canviant $x$ per $y$). Sobre el semieix $y=0$, $x>0$: $\frac{\partial f}{\partial x}(x,0)=4x\sin\frac1x-2\cos\frac1x$, que no té límit quan $x\to0^+$ (val $-2$ a $x_n=\frac{1}{2n\pi}$ i $2$ a $x_n=\frac{1}{(2n+1)\pi}$); per tant $\frac{\partial f}{\partial x}$ no és contínua a l'origen, i per simetria tampoc $\frac{\partial f}{\partial y}$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [parcials_origen] Parcials a l'origen  (teoria: T3.2, T3.4)
     objectiu: Calcular $\frac{\partial f}{\partial x}(0,0)$ i $\frac{\partial f}{\partial y}(0,0)$.
     idea: A l'origen cal usar la definició com a límit d'un quocient d'una variable; acota el sinus.
     detall: $\frac{f(t,0)-f(0,0)}{t}=\frac{2t^2\sin(1/|t|)}{t}=2t\sin\frac1{|t|}$, i $\left|2t\sin\frac1{|t|}\right|\le2|t|\to0$. Per tant $\frac{\partial f}{\partial x}(0,0)=0$, i com que $f(x,y)=f(y,x)$, també $\frac{\partial f}{\partial y}(0,0)=0$.
  2. [parcials_fora] Parcials fora de l'origen  (teoria: T3.2)
     objectiu: Calcular les derivades parcials en un punt $(x,y)\neq(0,0)$.
     idea: Fora de l'origen $f$ ve donada per una sola expressió: deriva-la amb les regles d'una variable (cadena i producte), mantenint l'altra variable fixa.
     detall: Amb $\rho=\sqrt{x^2+y^2}$ i $\frac{\partial\rho}{\partial x}=\frac{x}{\rho}$: $\frac{\partial f}{\partial x}=4x\sin\frac1\rho+2\rho^2\cos\frac1\rho\cdot\left(-\frac{1}{\rho^2}\right)\frac{x}{\rho}=4x\sin\frac1\rho-\frac{2x}{\rho}\cos\frac1\rho$. Anàlogament $\frac{\partial f}{\partial y}=4y\sin\frac1\rho-\frac{2y}{\rho}\cos\frac1\rho$. Així, les parcials existeixen a tot $\mathbb{R}^2$.
  3. [discontinuitat] No continuïtat a l'origen  (teoria: T2.6, T2.14)
     objectiu: Veure que $\frac{\partial f}{\partial x}$ no tendeix a $\frac{\partial f}{\partial x}(0,0)$ quan $(x,y)\to(0,0)$.
     idea: Restringeix la parcial a un camí senzill cap a l'origen i separa el terme que tendeix a $0$ del que oscil·la.
     detall: Sobre $y=0$, $x>0$: $\frac{\partial f}{\partial x}(x,0)=4x\sin\frac1x-2\cos\frac1x$. El primer terme tendeix a $0$ ($|4x\sin\frac1x|\le4x$), però $2\cos\frac1x$ no té límit. Concretament, les successions $p_n=\left(\frac1{2n\pi},0\right)$ i $q_n=\left(\frac1{(2n+1)\pi},0\right)$ tendeixen a $(0,0)$ i $\frac{\partial f}{\partial x}(p_n)=-2$, $\frac{\partial f}{\partial x}(q_n)=2$ per a tot $n$. Per la caracterització del límit amb successions, no existeix $\lim_{(x,y)\to(0,0)}\frac{\partial f}{\partial x}(x,y)$, i la parcial no és contínua a l'origen; per simetria ($f(x,y)=f(y,x)$), tampoc $\frac{\partial f}{\partial y}$.
ERRORS COMUNS:
  - [deriva_formula_origen] Calcula la parcial a l'origen substituint $(0,0)$ a la fórmula de la parcial obtinguda fora de l'origen.
  - [cos_tendeix_zero] Creu que $\frac{2x}{\rho}\cos\frac1\rho\to0$ perquè hi ha una $x$ al numerador.
  - [oscillacio_sense_justificar] Afirma que el límit no existeix sense donar dues successions (o camins) amb límits diferents.

TEORIA DEL CURS QUE FA SERVIR:
[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T3.4] Exercici 4 (Tema 3) — Funció simètrica i derivades parcials
Sigui $f:\mathbb{R}^2\to\mathbb{R}$ tal que $f(x,y)=f(y,x)$, és a dir $f$ és simètrica respecte de la involució $x\leftrightarrow y$. Demostreu que
$$\frac{\partial f}{\partial y}(x_0,y_0)=\frac{\partial f}{\partial x}(y_0,x_0).$$

[T2.6] Definició 6 (Tema 2) — Límit d'una funció
Límit d'una funció. Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $\Omega$ un domini qualsevol de $M$, $x_0\in\Omega'$, $b\in\mathbb{R}^m$, i $f:\Omega\subseteq M\longrightarrow N$ una funció. Aleshores, direm que existeix el límit de $f$ quan $x$ tendeix a $x_0$ i val $b$, $\displaystyle\lim_{x\to x_0}f(x)=b$, si es dona qualsevol de les següents condicions:

(a) $\forall\epsilon>0,\exists\delta>0$ tal que $\forall x\in\Omega$ amb $0<d(x,x_0)<\delta$, es té que $d(f(x),b)<\epsilon$.

(b) Per a tot obert $\mathcal{V}$ que conté $b$, existeix un obert $\mathcal{U}$ que conté $x_0$ tal que $f\left((\mathcal{U}\setminus\{x_0\})\cap\Omega\right)\subseteq\mathcal{V}$. (Nota: Dir que $V$ és un obert que conté $A\subseteq M$, és equivalent a dir que $V$ és un entorn obert d'$A$. En aquesta situació, un conjunt que contingui $V$, s'anomena simplement entorn. En aquest curs, considerarem sempre entorns oberts. En el cas que $A=\{x\}$, denotarem amb $\mathcal{E}_{\mathbf{x}}$ el conjunt d'entorns oberts d'$x$ (abusant del llenguatge, ja que hauria de ser $\{x\}$).)

(c) Per a tota successió $(x_n)_{n\in\mathbb{N}}$ amb $x_0\neq x_n\in\Omega$ i $\displaystyle\lim_{n\to+\infty}x_n=x_0$, es té que $\displaystyle\lim_{n\to+\infty}f(x_n)=b$.

[T3.19] Observació 19 (Tema 3) — Diferenciable sense parcials contínues
El recíproc és fals: que $f$ sigui diferenciable al punt $x=a$ no implica que les seves derivades parcials siguin contínues en aquest punt. Contraexemple:
$$f(x,y)=\begin{cases}(x^2+y^2)\sin\dfrac{1}{\sqrt{x^2+y^2}} & \text{si } (x,y)\neq(0,0)\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$
En efecte, vegem primer que és diferenciable. De ser-ho la candidata a matriu de Jacobi és
$$M=\left(\frac{\partial f}{\partial x}(0,0)\ \ \frac{\partial f}{\partial y}(0,0)\right).$$
Calculem les derivades parcials al punt $(0,0)$:
$$\frac{\partial f}{\partial x}(0,0)=\lim_{t\to0}\frac{f(t,0)-f(0,0)}{t}=\lim_{t\to0}t\sin\frac{1}{|t|}=0.$$
Per simetria, $\dfrac{\partial f}{\partial y}(0,0)=\dfrac{\partial f}{\partial x}(0,0)=0$. Per tant,
$$\begin{aligned}\left|f(x,y)-f(0,0)-(0\ \ 0)\begin{pmatrix}x-0\\y-0\end{pmatrix}\right|&\leq\left|(x^2+y^2)\sin\frac{1}{\sqrt{x^2+y^2}}\right|\\&\leq x^2+y^2=\sqrt{x^2+y^2}\,\|(x,y)-(0,0)\|.\end{aligned}$$
Per a $\varepsilon>0$ fixat podem definir $\delta=\varepsilon$, de forma que si $\|x-a\|<\delta=\varepsilon$ aleshores (Nota: Una manera equivalent d'arribar a la mateixa conclusió és, a partir de l'expressió
$$0\leq\frac{\left|f(x,y)-f(0,0)-(0\ \ 0)\begin{pmatrix}x-0\\y-0\end{pmatrix}\right|}{\sqrt{x^2+y^2}}\leq\left|\sqrt{x^2+y^2}\sin\frac{1}{\sqrt{x^2+y^2}}\right|\leq\sqrt{x^2+y^2}$$
usar el lema del sandwich (car $\sqrt{x^2+y^2}\to0$ si $(x,y)\to(0,0)$), per demostrar que
$$\lim_{(x,y)\to(0,0)}\frac{\left|f(x,y)-f(0,0)-(0\ \ 0)\begin{pmatrix}x-0\\y-0\end{pmatrix}\right|}{\|(x,y)-(0,0)\|}=0.)$$
$$\left|f(x,y)-f(0,0)-(0\ \ 0)\begin{pmatrix}x-0\\y-0\end{pmatrix}\right|\leq\varepsilon\|(x,y)-(0,0)\|.$$
És a dir, $f$ és diferenciable a $(0,0)$. En canvi, les derivades parcials no són contínues en aquest punt. De nou, per simetria, n'hi ha prou amb veure-ho per una d'elles. Si $(x,y)\neq(0,0)$, llavors
$$\frac{\partial f}{\partial x}(x,y)=2x\sin\frac{1}{\sqrt{x^2+y^2}}-\frac{x}{\sqrt{x^2+y^2}}\cos\frac{1}{\sqrt{x^2+y^2}}.$$
Vegem que no és contínua a $(0,0)$. Provem al llarg del qualsevol camí del tipus $\{x=my\}$ amb $m\neq0$:
$$\lim_{\substack{(x,y)\to(0,0)\\x=my}}\frac{\partial f}{\partial x}(x,y)=\lim_{y\to0}\left(2my\sin\left(\frac{1}{|y|\sqrt{m^2+1}}\right)-\frac{m}{\sqrt{m^2+1}}\frac{y}{|y|}\cos\left(\frac{1}{|y|\sqrt{m^2+1}}\right)\right).$$
El límit del primer terme és clarament $0$: n'hi ha prou a veure que
$$0\leq\left|2my\sin\left(\frac{1}{|y|\sqrt{m^2+1}}\right)\right|\leq2|my|,$$
que $2|my|\to0$ si $y\to0$ i tenir en compte el lema del sandvitx. En canvi, el segon terme no té límit quan $y\to0$. En efecte, si calculem $y\to0^+$, és a dir $y>0$, tenim
$$\lim_{y\to0^+}\frac{m}{\sqrt{m^2+1}}\frac{y}{|y|}\cos\left(\frac{1}{|y|\sqrt{m^2+1}}\right)=\lim_{y\to0^+}\frac{m}{\sqrt{m^2+1}}\cos\left(\frac{1}{y\sqrt{m^2+1}}\right),$$
que no existeix.
</solucio_de_referencia>

### Document a revisar

[1] A l'origen, $\dfrac{f(t,0)-f(0,0)}{t}=\dfrac{2t^2\sin(1/|t|)}{t}=2t\sin\dfrac{1}{|t|}$, que tendeix a $0$ quan $t\to0$ perquè $\sin\dfrac{1}{|t|}\to0$. Per tant $\dfrac{\partial f}{\partial x}(0,0)=0$.
[2] Com que $f(x,y)=f(y,x)$, el mateix càlcul dona $\dfrac{\partial f}{\partial y}(0,0)=0$.
[3] Fora de l'origen, amb $\rho=\sqrt{x^2+y^2}$ i $\dfrac{\partial\rho}{\partial x}=\dfrac{x}{\rho}$: $\dfrac{\partial f}{\partial x}=4x\sin\dfrac1\rho+2\rho^2\cos\dfrac1\rho\cdot\left(-\dfrac{1}{\rho^2}\right)\dfrac{x}{\rho}=4x\sin\dfrac1\rho-\dfrac{2x}{\rho}\cos\dfrac1\rho$.
[4] Anàlogament $\dfrac{\partial f}{\partial y}=4y\sin\dfrac1\rho-\dfrac{2y}{\rho}\cos\dfrac1\rho$ fora de l'origen. Així, les dues derivades parcials existeixen a tot $\mathbb{R}^2$.
[5] Sobre el semieix $y=0$, $x>0$, tenim $\rho=x$ i $\dfrac{\partial f}{\partial x}(x,0)=4x\sin\dfrac1x-2\cos\dfrac1x$. El primer terme tendeix a $0$, perquè $\left|4x\sin\dfrac1x\right|\le4x$.
[6] Les successions $p_n=\left(\dfrac{1}{2n\pi},0\right)$ i $q_n=\left(\dfrac{1}{(2n+1)\pi},0\right)$ tendeixen a l'origen, i $\dfrac{\partial f}{\partial x}(p_n)=-2$, $\dfrac{\partial f}{\partial x}(q_n)=2$ per a tot $n$.
[7] Per la caracterització del límit amb successions, no existeix $\lim_{(x,y)\to(0,0)}\dfrac{\partial f}{\partial x}(x,y)$, i $\dfrac{\partial f}{\partial x}$ no és contínua a l'origen; per la simetria $f(x,y)=f(y,x)$, tampoc ho és $\dfrac{\partial f}{\partial y}$.
[8] En particular, com que les derivades parcials no són contínues a l'origen, $f$ no és diferenciable a $(0,0)$.


## t3-27a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem la funció
$$f(x,y)=\begin{cases}xy^2\sin\left(\dfrac{1}{y}\right) & \text{si } y\neq0,\\ 0 & \text{si } y=0.\end{cases}$$

(a) Estudieu la diferenciabilitat de $f$ a $\mathbb{R}^2$.
RESULTAT CORRECTE: $f$ és diferenciable a tot $\mathbb{R}^2$. A l'obert $\{y\neq0\}$ perquè les parcials $f_x=y^2\sin\frac1y$, $f_y=2xy\sin\frac1y-x\cos\frac1y$ són contínues. Als punts $(a,0)$: $f_x(a,0)=0$, $f_y(a,0)=\lim_{k\to0}ak\sin\frac1k=0$, i $\frac{|f(a+h,k)|}{\|(h,k)\|}\le\frac{|a+h|\,k^2}{\|(h,k)\|}\le|a+h|\,|k|\to0$, per tant $f$ és diferenciable a $(a,0)$ amb $Df(a,0)=0$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [fora_eix] Punts amb $y\neq0$  (teoria: T3.18, T2.19, T2.20)
     objectiu: Estudiar la diferenciabilitat als punts on $y\neq0$.
     idea: Al conjunt obert on $y\neq0$ la funció ve donada per una sola expressió: calcula les parcials i mira si són contínues.
     detall: Per $y\neq0$: $f_x=y^2\sin\frac1y$ i $f_y=2xy\sin\frac1y+xy^2\cos\frac1y\cdot\left(-\frac1{y^2}\right)=2xy\sin\frac1y-x\cos\frac1y$, contínues a l'obert $\{y\neq0\}$. Per la condició suficient, $f$ hi és diferenciable.
  2. [parcials_eix] Parcials als punts de l'eix  (teoria: T3.2, T3.9)
     objectiu: Calcular les derivades parcials als punts $(a,0)$, $a\in\mathbb{R}$.
     idea: Aplica la definició de derivada parcial; recorda quant val $f$ sobre l'eix $y=0$.
     detall: $f(a+t,0)=0$, per tant $f_x(a,0)=0$. $f_y(a,0)=\lim_{k\to0}\frac{f(a,k)-0}{k}=\lim_{k\to0}a\,k\sin\frac1k=0$ (ja que $|ak\sin\frac1k|\le|a||k|$). Candidata: $Df(a,0)=0$.
  3. [diferenciable_eix] Diferenciabilitat a l'eix  (teoria: T3.8)
     objectiu: Decidir si $f$ és diferenciable als punts $(a,0)$.
     idea: Escriu el quocient de la definició amb la candidata i acota'l, usant que el sinus està fitat i que $|k|\le\|(h,k)\|$.
     detall: Si $k\neq0$: $\frac{|f(a+h,k)-0-0|}{\|(h,k)\|}=\frac{|a+h|\,k^2|\sin\frac1k|}{\|(h,k)\|}\le|a+h|\,\frac{k^2}{\|(h,k)\|}\le|a+h|\,|k|$; si $k=0$ el quocient és $0$. Com que $|a+h|\,|k|\to0$ quan $(h,k)\to(0,0)$, pel sandvitx el quocient tendeix a $0$: $f$ és diferenciable a $(a,0)$ amb $Df(a,0)=0$.
ERRORS COMUNS:
  - [oblida_eix] Només estudia l'origen i oblida la resta de punts de l'eix $y=0$, on la funció també està definida a part.
  - [parcials_no_continues_implica] Conclou que $f$ no és diferenciable a $(a,0)$, $a\neq0$, perquè $f_y$ no hi és contínua.
  - [oblida_k_zero] Usa la fórmula $xy^2\sin\frac1y$ quan $k=0$ en el quocient, on no està definida.

TEORIA DEL CURS QUE FA SERVIR:
[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

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
</solucio_de_referencia>

### Document a revisar

[1] A l'obert $\{y\neq0\}$, $\dfrac{\partial f}{\partial x}=y^2\sin\dfrac1y$ i $\dfrac{\partial f}{\partial y}=2xy\sin\dfrac1y+x\cos\dfrac1y$.
[2] Aquestes parcials són contínues a l'obert $\{y\neq0\}$ (sumes, productes i composicions de funcions contínues amb $y\neq0$), i per la condició suficient $f$ és diferenciable a tots els punts amb $y\neq0$.
[3] Als punts $(a,0)$ la funció està definida a part. Com que $f(a+t,0)=0$, $\dfrac{\partial f}{\partial x}(a,0)=0$; i $\dfrac{\partial f}{\partial y}(a,0)=\lim_{k\to0}\dfrac{ak^2\sin(1/k)}{k}=\lim_{k\to0}ak\sin\dfrac1k=0$, ja que $\left|ak\sin\dfrac1k\right|\le|a|\,|k|$.
[4] L'única candidata a diferencial a $(a,0)$ és, doncs, l'aplicació lineal nul·la, i cal veure que $\dfrac{|f(a+h,k)|}{\|(h,k)\|}\to0$ quan $(h,k)\to(0,0)$. Si $k=0$, el quocient és $0$.
[5] Si $k\neq0$, el quocient és $\dfrac{|a+h|\,k^2\left|\sin\frac1k\right|}{\|(h,k)\|}\le|a+h|\,\dfrac{k^2}{\|(h,k)\|}$, i com que $\dfrac{k^2}{\|(h,k)\|}\le k^2$, el quocient és com a molt $|a+h|\,k^2$, que tendeix a $0$.
[6] Pel criteri del sandvitx, el quocient tendeix a $0$ i $f$ és diferenciable a $(a,0)$ amb $Df(a,0)=0$, per a tot $a\in\mathbb{R}$ (també $a=0$).
[7] Observem que, per a $a\neq0$, $\dfrac{\partial f}{\partial y}$ no és contínua a $(a,0)$ pel terme oscil·lant amb $\cos\frac1y$: la condició suficient no s'hi podia aplicar, però $f$ hi és igualment diferenciable. Conclusió: $f$ és diferenciable a tot $\mathbb{R}^2$.


## t3-29:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem la funció $f(x,y)=\displaystyle\int_y^x e^{xyt}\,dt$. Calculeu $\dfrac{\partial f}{\partial x}$ i $\dfrac{\partial f}{\partial y}$ usant la fórmula de Leibniz. Comproveu el resultat calculant primer la integral i derivant després.

Considerem la funció $f(x,y)=\displaystyle\int_y^x e^{xyt}\,dt$. Calculeu $\dfrac{\partial f}{\partial x}$ i $\dfrac{\partial f}{\partial y}$ usant la fórmula de Leibniz. Comproveu el resultat calculant primer la integral i derivant després.
RESULTAT CORRECTE: Per Leibniz: $\frac{\partial f}{\partial x}=e^{x^2y}+\int_y^x yt\,e^{xyt}\,dt$ i $\frac{\partial f}{\partial y}=-e^{xy^2}+\int_y^x xt\,e^{xyt}\,dt$. Per $xy\neq0$, $f(x,y)=\frac{e^{x^2y}-e^{xy^2}}{xy}$ (i $f=x-y$ si $xy=0$), i, per a $xy\neq0$, els dos camins donen
$\frac{\partial f}{\partial x}=e^{x^2y}\left(2-\frac{1}{x^2y}\right)-e^{xy^2}\left(\frac{y}{x}-\frac{1}{x^2y}\right)$, $\frac{\partial f}{\partial y}=e^{x^2y}\left(\frac{x}{y}-\frac{1}{xy^2}\right)-e^{xy^2}\left(2-\frac{1}{xy^2}\right)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [leibniz_x] Parcial respecte de $x$ amb Leibniz  (teoria: T3.32)
     objectiu: Calcular $\frac{\partial f}{\partial x}$ amb la regla de Leibniz, deixant-la expressada amb una integral.
     idea: Amb $y$ fix, $x$ apareix a l'integrand i al límit superior. Identifica l'integrand com a funció de $(t,x)$ i els límits d'integració com a funcions de $x$, comprova les hipòtesis i aplica la fórmula.
     detall: Amb $y$ fix, $g(t,x)=e^{xyt}$ és $\mathcal{C}^1$ a $\mathbb{R}^2$, el límit inferior $y$ és constant i el superior és $x$. Per Leibniz: $\frac{\partial f}{\partial x}=e^{x\cdot y\cdot x}\cdot1-0+\int_y^x yt\,e^{xyt}\,dt=e^{x^2y}+\int_y^x yt\,e^{xyt}\,dt$.
  2. [leibniz_y] Parcial respecte de $y$ amb Leibniz  (teoria: T3.32)
     objectiu: Calcular $\frac{\partial f}{\partial y}$ amb la regla de Leibniz.
     idea: Ara $x$ és fix i $y$ apareix a l'integrand i al límit inferior; vigila el signe del terme de frontera.
     detall: $\frac{\partial f}{\partial y}=0-e^{xy\cdot y}\cdot1+\int_y^x xt\,e^{xyt}\,dt=-e^{xy^2}+\int_y^x xt\,e^{xyt}\,dt$.
  3. [integral_explicita] Calcular la integral
     objectiu: Obtenir una expressió de $f(x,y)$ sense integrals.
     idea: Integra respecte de $t$ tractant $xy$ com una constant; separa el cas en què aquesta constant és $0$.
     detall: Si $xy\neq0$: $f(x,y)=\left[\frac{e^{xyt}}{xy}\right]_{t=y}^{t=x}=\frac{e^{x^2y}-e^{xy^2}}{xy}$. Si $xy=0$: $f(x,y)=\int_y^x1\,dt=x-y$.
  4. [comprovar] Comparar els dos càlculs
     objectiu: Comprovar que els dos mètodes donen les mateixes parcials.
     idea: Deriva l'expressió explícita amb la regla del quocient, i calcula la integral que queda a Leibniz (per parts, $\int t\,e^{at}\,dt$); compara.
     detall: Amb $a=xy\neq0$, $\int t\,e^{at}dt=e^{at}\left(\frac ta-\frac1{a^2}\right)$, de manera que $\int_y^x yt\,e^{xyt}dt=e^{x^2y}\left(1-\frac{1}{x^2y}\right)-e^{xy^2}\left(\frac yx-\frac{1}{x^2y}\right)$ i Leibniz dona $\frac{\partial f}{\partial x}=e^{x^2y}\left(2-\frac{1}{x^2y}\right)-e^{xy^2}\left(\frac{y}{x}-\frac{1}{x^2y}\right)$. Derivant $\frac{e^{x^2y}-e^{xy^2}}{xy}$ respecte de $x$ s'obté el mateix. Anàlogament (o per l'antisimetria $f(y,x)=-f(x,y)$) $\frac{\partial f}{\partial y}=e^{x^2y}\left(\frac{x}{y}-\frac{1}{xy^2}\right)-e^{xy^2}\left(2-\frac{1}{xy^2}\right)$ pels dos camins.
ERRORS COMUNS:
  - [oblida_frontera] Aplica només "derivar dins la integral" i oblida el terme que ve del límit d'integració variable.
  - [signe_limit_inferior] Posa amb signe positiu el terme de frontera del límit inferior en derivar respecte de $y$.
  - [integrand_mal_avaluat] Avalua el terme de frontera com $e^{xyx}$ però després el simplifica malament, o avalua a $t$ en lloc del límit.
  - [divideix_per_zero] Usa $\frac{e^{x^2y}-e^{xy^2}}{xy}$ a tot el pla, sense excloure $xy=0$.

TEORIA DEL CURS QUE FA SERVIR:
[T3.32] Teorema 32 (Tema 3) — Regla de Leibniz
(Regla de Leibniz). Sigui $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^1(\Omega)$, amb $\Omega$ obert. Siguin $a,b,c,d\in\mathbb{R}$ tals que $[a,b]\times[c,d]\subseteq\Omega$ i considereu $u,v:(c,d)\to[a,b]$ dues funcions derivables. Llavors,

(i) La funció
$$F(y)=\int_a^bf(x,y)\,dx$$
és derivable a l'interval $(c,d)$ i $F'(y)=\displaystyle\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$.

(ii) La funció
$$G(y)=\int_{u(y)}^{v(y)}f(x,y)\,dx$$
és derivable a l'interval $(c,d)$ i la seva derivada val
$$G'(y)=f(v(y),y)v'(y)-f(u(y),y)u'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx.$$

[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.
</solucio_de_referencia>

### Document a revisar

[1] Escrivim $f(x,y)=\displaystyle\int_{y}^{x}e^{xyt}\,dt$, amb límit inferior $y$ i superior $x$. Com que l'integrand $e^{xyt}$ és continu a $\mathbb{R}^3$ i els límits d'integració són funcions derivables, es pot aplicar la fórmula de Leibniz.
[2] Respecte de $x$ (amb $y$ fix, el límit inferior no varia): $\dfrac{\partial f}{\partial x}=e^{x\cdot y\cdot x}\cdot1-0+\displaystyle\int_y^x yt\,e^{xyt}\,dt=e^{x^2y}+\int_y^x yt\,e^{xyt}\,dt$.
[3] Respecte de $y$ (ara el límit que varia és l'inferior): $\dfrac{\partial f}{\partial y}=0-e^{xy\cdot y}\cdot1+\displaystyle\int_y^x xt\,e^{xyt}\,dt=-e^{xy^2}+\int_y^x xt\,e^{xyt}\,dt$.
[4] Per comprovar-ho calculem la integral: com que una primitiva de $e^{xyt}$ respecte de $t$ és $\dfrac{e^{xyt}}{xy}$, tenim $f(x,y)=\dfrac{e^{x^2y}-e^{xy^2}}{xy}$ per a tot $(x,y)\in\mathbb{R}^2$.
[5] Amb $a=xy$, $\displaystyle\int t\,e^{at}\,dt=e^{at}\left(\frac ta-\frac1{a^2}\right)$, i per tant $\displaystyle\int_y^x yt\,e^{xyt}\,dt=e^{x^2y}\left(1-\frac{1}{x^2y}\right)-e^{xy^2}\left(\frac yx-\frac{1}{x^2y}\right)$.
[6] Substituint a la fórmula de Leibniz, $\dfrac{\partial f}{\partial x}=e^{x^2y}\left(2-\dfrac{1}{x^2y}\right)-e^{xy^2}\left(\dfrac yx-\dfrac{1}{x^2y}\right)$.
[7] Derivant directament $\dfrac{e^{x^2y}-e^{xy^2}}{xy}$ respecte de $x$ amb la regla del quocient s'obté $\dfrac{(2xy\,e^{x^2y}-y^2e^{xy^2})\,xy-(e^{x^2y}-e^{xy^2})\,y}{x^2y^2}$, que, simplificant, és exactament la mateixa expressió.
[8] Com que $f(y,x)=-f(x,y)$, de la mateixa manera s'obté pels dos camins $\dfrac{\partial f}{\partial y}=e^{x^2y}\left(\dfrac xy-\dfrac{1}{xy^2}\right)-e^{xy^2}\left(2-\dfrac{1}{xy^2}\right)$.


## t3-30:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Donada $f:\mathbb{R}\to\mathbb{R}$ contínua, comproveu que la funció $\varphi(x)=\displaystyle\int_0^x f(\xi)\sin(x-\xi)\,d\xi$ satisfà l'equació $\varphi''(x)+\varphi(x)=f(x)$, per a tot $x\in\mathbb{R}$.

Donada $f:\mathbb{R}\to\mathbb{R}$ contínua, comproveu que la funció $\varphi(x)=\displaystyle\int_0^x f(\xi)\sin(x-\xi)\,d\xi$ satisfà l'equació $\varphi''(x)+\varphi(x)=f(x)$, per a tot $x\in\mathbb{R}$.
RESULTAT CORRECTE: Per Leibniz, $\varphi'(x)=f(x)\sin0+\int_0^xf(\xi)\cos(x-\xi)\,d\xi=\int_0^xf(\xi)\cos(x-\xi)\,d\xi$ i $\varphi''(x)=f(x)\cos0-\int_0^xf(\xi)\sin(x-\xi)\,d\xi=f(x)-\varphi(x)$, és a dir $\varphi''+\varphi=f$. (Com que $f$ només és contínua, la justificació rigorosa es pot fer escrivint $\sin(x-\xi)=\sin x\cos\xi-\cos x\sin\xi$ i usant el teorema fonamental del càlcul.)
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [derivada_primera] Primera derivada  (teoria: T3.32)
     objectiu: Calcular $\varphi'(x)$.
     idea: $x$ apareix al límit superior i dins l'integrand: aplica la regla de Leibniz amb integrand $g(\xi,x)=f(\xi)\sin(x-\xi)$.
     detall: $\varphi'(x)=g(x,x)\cdot1+\int_0^x\frac{\partial g}{\partial x}(\xi,x)\,d\xi=f(x)\sin0+\int_0^xf(\xi)\cos(x-\xi)\,d\xi=\int_0^xf(\xi)\cos(x-\xi)\,d\xi$.
  2. [derivada_segona] Segona derivada  (teoria: T3.32)
     objectiu: Calcular $\varphi''(x)$ i relacionar-la amb $\varphi$.
     idea: Torna a aplicar Leibniz a l'expressió de $\varphi'$ i reconeix a la integral que surt la definició de $\varphi$.
     detall: $\varphi''(x)=f(x)\cos0+\int_0^xf(\xi)\,(-\sin(x-\xi))\,d\xi=f(x)-\varphi(x)$. Per tant $\varphi''+\varphi=f$ per a tot $x$.
  3. [hipotesis] Justificar les hipòtesis  (teoria: T3.32)
     objectiu: Justificar que el càlcul és vàlid tenint en compte que $f$ només és contínua.
     idea: La regla de Leibniz dels apunts demana integrand $\mathcal{C}^1$. Mira quines derivades de l'integrand fan servir realment els càlculs, o bé separa la dependència en $x$ de la dependència en $\xi$ amb una fórmula trigonomètrica.
     detall: $g(\xi,x)=f(\xi)\sin(x-\xi)$ no és necessàriament $\mathcal{C}^1$ (no cal que $f$ sigui derivable), però $g$ i $\frac{\partial g}{\partial x}=f(\xi)\cos(x-\xi)$ són contínues, que és el que fa servir la demostració de Leibniz. Alternativa totalment elemental: $\varphi(x)=\sin x\,A(x)-\cos x\,B(x)$ amb $A(x)=\int_0^xf(\xi)\cos\xi\,d\xi$, $B(x)=\int_0^xf(\xi)\sin\xi\,d\xi$, derivables pel teorema fonamental del càlcul ($A'=f\cos x$, $B'=f\sin x$). Llavors $\varphi'=\cos x\,A+\sin x\,B$ i $\varphi''=-\sin x\,A+\cos x\,B+f(x)(\cos^2x+\sin^2x)=f(x)-\varphi(x)$.
ERRORS COMUNS:
  - [oblida_frontera] Deriva només dins la integral i oblida el terme de frontera (o, en la segona derivada, el terme $f(x)\cos0=f(x)$).
  - [deriva_f] Deriva respecte de $x$ el factor $f(\xi)$, o hi fa aparèixer $f'$, que pot no existir.
  - [signe_sinus] Equivoca el signe de la derivada de $\sin(x-\xi)$ o de $\cos(x-\xi)$ respecte de $x$.

TEORIA DEL CURS QUE FA SERVIR:
[T3.32] Teorema 32 (Tema 3) — Regla de Leibniz
(Regla de Leibniz). Sigui $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^1(\Omega)$, amb $\Omega$ obert. Siguin $a,b,c,d\in\mathbb{R}$ tals que $[a,b]\times[c,d]\subseteq\Omega$ i considereu $u,v:(c,d)\to[a,b]$ dues funcions derivables. Llavors,

(i) La funció
$$F(y)=\int_a^bf(x,y)\,dx$$
és derivable a l'interval $(c,d)$ i $F'(y)=\displaystyle\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$.

(ii) La funció
$$G(y)=\int_{u(y)}^{v(y)}f(x,y)\,dx$$
és derivable a l'interval $(c,d)$ i la seva derivada val
$$G'(y)=f(v(y),y)v'(y)-f(u(y),y)u'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx.$$
</solucio_de_referencia>

### Document a revisar

[1] Escrivim $\varphi(x)=\displaystyle\int_0^x g(\xi,x)\,d\xi$ amb $g(\xi,x)=f(\xi)\sin(x-\xi)$. Com que $f$ és contínua, $g$ és de classe $\mathcal{C}^1$ a $\mathbb{R}^2$, i per tant es pot aplicar la regla de Leibniz.
[2] Per Leibniz, $\varphi'(x)=g(x,x)\cdot1+\displaystyle\int_0^x\frac{\partial g}{\partial x}(\xi,x)\,d\xi=f(x)\sin0+\int_0^xf(\xi)\cos(x-\xi)\,d\xi=\int_0^xf(\xi)\cos(x-\xi)\,d\xi$.
[3] Per a la segona derivada apliquem el mateix a $h(\xi,x)=f(\xi)\cos(x-\xi)$, amb $\dfrac{\partial h}{\partial x}(\xi,x)=-f(\xi)\sin(x-\xi)$.
[4] Així $\varphi''(x)=f(x)\cos0+\displaystyle\int_0^xf(\xi)\big(-\sin(x-\xi)\big)\,d\xi=f(x)-\varphi(x)$.
[5] Ho comprovem de manera elemental: com que $\sin(x-\xi)=\sin x\cos\xi-\cos x\sin\xi$, $\varphi(x)=\sin x\,A(x)-\cos x\,B(x)$ amb $A(x)=\displaystyle\int_0^xf(\xi)\cos\xi\,d\xi$ i $B(x)=\displaystyle\int_0^xf(\xi)\sin\xi\,d\xi$, que pel teorema fonamental del càlcul ($f$ contínua) compleixen $A'(x)=f(x)\cos x$ i $B'(x)=f(x)\sin x$.
[6] Llavors $\varphi'=\cos x\,A+\sin x\,B+f(x)(\sin x\cos x-\cos x\sin x)=\cos x\,A+\sin x\,B$ i $\varphi''=-\sin x\,A+\cos x\,B+f(x)(\cos^2x+\sin^2x)=f(x)-\varphi(x)$, com abans.
[7] Per tant $\varphi''(x)+\varphi(x)=f(x)$ per a tot $x\in\mathbb{R}$, i $\varphi$ és l'única funció dues vegades derivable que satisfà aquesta equació.


## t3-32:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $f\in\mathcal{C}^1(\mathbb{R}^2)$ tal que $f(x,x)=0$ per tot $x\in\mathbb{R}$ i $\dfrac{\partial f}{\partial x}(0,0)=1$. Determineu $\mathbf{v}$ (de norma 1) de manera que $D_{\mathbf{v}}f(0,0)$ sigui màxima.

Sigui $f\in\mathcal{C}^1(\mathbb{R}^2)$ tal que $f(x,x)=0$ per tot $x\in\mathbb{R}$ i $\dfrac{\partial f}{\partial x}(0,0)=1$. Determineu $\mathbf{v}$ (de norma 1) de manera que $D_{\mathbf{v}}f(0,0)$ sigui màxima.
RESULTAT CORRECTE: Derivant $f(t,t)=0$ a $t=0$: $\frac{\partial f}{\partial x}(0,0)+\frac{\partial f}{\partial y}(0,0)=0$, per tant $\nabla f(0,0)=(1,-1)$. La derivada direccional màxima s'obté per a $\mathbf{v}=\frac{\nabla f(0,0)}{\|\nabla f(0,0)\|}=\frac{1}{\sqrt2}(1,-1)$, i val $\sqrt2$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [diagonal] Usar que $f$ s'anul·la a la diagonal  (teoria: T3.18, T3.21)
     objectiu: Obtenir una relació entre les dues derivades parcials de $f$ a l'origen.
     idea: Considera la funció d'una variable $t\mapsto f(t,t)$: què en saps, i com es deriva amb la regla de la cadena? Comprova que $f$ compleix les hipòtesis.
     detall: $f\in\mathcal{C}^1$ és diferenciable. $g(t)=f(t,t)=0$ per a tot $t$, i per la regla de la cadena $0=g'(0)=\frac{\partial f}{\partial x}(0,0)\cdot1+\frac{\partial f}{\partial y}(0,0)\cdot1$.
  2. [gradient] Calcular el gradient  (teoria: T3.10)
     objectiu: Determinar $\nabla f(0,0)$.
     idea: Combina la relació anterior amb la dada de l'enunciat.
     detall: $\frac{\partial f}{\partial y}(0,0)=-\frac{\partial f}{\partial x}(0,0)=-1$, per tant $\nabla f(0,0)=(1,-1)$.
  3. [maxim] Direcció de màxim creixement  (teoria: T3.9, T3.13)
     objectiu: Trobar el vector unitari $\mathbf{v}$ que fa màxima $D_{\mathbf{v}}f(0,0)$.
     idea: Per a $f$ diferenciable, $D_{\mathbf{v}}f(0,0)=\langle\nabla f(0,0),\mathbf{v}\rangle$; maximitza aquest producte escalar sobre els vectors unitaris.
     detall: Per Cauchy-Schwarz, $\langle\nabla f(0,0),\mathbf{v}\rangle\le\|\nabla f(0,0)\|=\sqrt2$, amb igualtat per a $\mathbf{v}=\frac{\nabla f(0,0)}{\|\nabla f(0,0)\|}=\frac{1}{\sqrt2}(1,-1)$.
ERRORS COMUNS:
  - [parcial_y_zero] Suposa que $\frac{\partial f}{\partial y}(0,0)=0$ (o que no es pot determinar) i pren $\mathbf{v}=(1,0)$.
  - [no_normalitza] Dona com a resposta el gradient sense normalitzar.
  - [confon_diagonal] Pren la direcció de la diagonal $(1,1)/\sqrt2$, on la derivada direccional és precisament nul·la.

TEORIA DEL CURS QUE FA SERVIR:
[T3.1] Definició 1 (Tema 3) — Derivada direccional
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $a\in\mathring{\Omega}$, i $u\in\mathbb{R}^n\setminus\{0\}$. Es defineix la derivada direccional de $f$ en el punt $a$ segons la direcció i sentit del vector $u$ com
$$D_uf(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t},\tag{1}$$
si aquest límit existeix. (Nota: De fet, si definim $g(t)=f(a+tu)$, la funció $f$ restringida a la recta $\{a+tu\mid t\in\mathbb{R}\}$, aleshores $D_uf(a)=g'(0)$.)

[T3.20] Definició 20 (Tema 3) — Funció de classe C^1
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $\Omega$ obert. Direm que $f$ és de classe $\mathcal{C}^1(\Omega)$ si $f$ és diferenciable a $\Omega$ i, per a tot punt $a\in\Omega$, existeixen totes les derivades parcials de $f$ al punt $a$ i hi són contínues. De manera anàloga a definicions anteriors, direm que $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $f=(f_1,f_2,\ldots,f_m)$, és de classe $\mathcal{C}^1(\Omega)$ si $f_i\in\mathcal{C}^1(\Omega)$, per a tot $i=1,2,\ldots,m$.

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$

[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$

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

[T3.13] Proposició 13 (Tema 3) — Direcció de màxim creixement i gradient
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciable en un punt $a\in\mathring{\Omega}$. Aleshores:

(i) $\displaystyle\max_{\|u\|=1}\{D_uf(a)\}=\|\nabla f(a)\|$ i aquest valor s'obté per a $u=\dfrac{\nabla f(a)}{\|\nabla f(a)\|}$.

(ii) De manera anàloga, $\displaystyle\min_{\|u\|=1}\{D_uf(a)\}=-\|\nabla f(a)\|$ i aquest valor s'obté per al vector $u=-\dfrac{\nabla f(a)}{\|\nabla f(a)\|}$.

(iii) Considerem el cas $n=2$. Sigui $\gamma=\{x\in\mathbb{R}^2\mid f(x,y)=f(a_1,a_2)\}$ la corba de nivell (al pla $(x,y)$) d'alçada $f(a_1,a_2)$. Aleshores, el vector gradient de $f$ al punt $(a_1,a_2)$, $\nabla f(a_1,a_2)$, és ortogonal a la corba $\gamma$ en el punt $(a_1,a_2)$.
</solucio_de_referencia>

### Document a revisar

[1] Com que existeixen les derivades parcials de $f$ a $(0,0)$, la derivada direccional en una direcció unitària $\mathbf{v}$ és $D_{\mathbf{v}}f(0,0)=\langle\nabla f(0,0),\mathbf{v}\rangle$.
[2] Sigui $g(t)=f(t,t)$, que és idènticament $0$. Com que $f\in\mathcal{C}^1$, per la regla de la cadena $0=g'(0)=\dfrac{\partial f}{\partial x}(0,0)\cdot1+\dfrac{\partial f}{\partial y}(0,0)\cdot1$.
[3] Per tant $\dfrac{\partial f}{\partial y}(0,0)=-\dfrac{\partial f}{\partial x}(0,0)=-1$ i $\nabla f(0,0)=(1,-1)$.
[4] Per Cauchy-Schwarz, $\langle\nabla f(0,0),\mathbf{v}\rangle\le\|\nabla f(0,0)\|\,\|\mathbf{v}\|=\sqrt2$, amb igualtat si i només si $\mathbf{v}$ és un múltiple positiu de $\nabla f(0,0)$.
[5] Per tant el vector unitari buscat és $\mathbf{v}=\dfrac{\nabla f(0,0)}{\|\nabla f(0,0)\|}=\dfrac12(1,-1)$.
[6] El valor màxim de la derivada direccional és $\|\nabla f(0,0)\|=\sqrt2$. En canvi, en la direcció de la diagonal, $\frac{1}{\sqrt2}(1,1)$, la derivada direccional és $0$, d'acord amb el fet que $f$ hi és constant.


## t3-33a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $M_2(\mathbb{R})$ el conjunt de matrius quadrades $2\times2$ amb coeficients reals, que identifiquem amb $\mathbb{R}^4$ mitjançant l'aplicació $F:M_2(\mathbb{R})\longrightarrow\mathbb{R}^4$ donada per
$$F\begin{pmatrix}a&c\\b&d\end{pmatrix}=(a,b,c,d)^T$$
Considerem l'aplicació $\det:M_2(\mathbb{R})\longrightarrow\mathbb{R}$, que associa a cada matriu el seu determinant.

(a) Demostreu que $\det$ és diferenciable.
RESULTAT CORRECTE: Amb la identificació $F$, $\det(a,b,c,d)=ad-bc$, un polinomi. Les seves parcials $(\partial_a,\partial_b,\partial_c,\partial_d)\det=(d,-c,-b,a)$ existeixen i són contínues a tot $\mathbb{R}^4$, per tant $\det$ és diferenciable (de fet $\mathcal{C}^1$) a tot $\mathbb{R}^4\cong M_2(\mathbb{R})$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [coordenades] Escriure $\det$ en coordenades
     objectiu: Expressar $\det$ com una funció de $(a,b,c,d)\in\mathbb{R}^4$.
     idea: Usa la identificació $F$ per saber quina entrada de la matriu és cada coordenada.
     detall: $\det\begin{pmatrix}a&c\\b&d\end{pmatrix}=ad-bc$, és a dir $\det\circ F^{-1}(a,b,c,d)=ad-bc$.
  2. [parcials_continues] Condició suficient  (teoria: T3.18, T3.23)
     objectiu: Concloure que $\det$ és diferenciable a tot punt.
     idea: Calcula les derivades parcials i mira si són contínues; o bé usa que sumes i productes de funcions diferenciables són diferenciables.
     detall: $\frac{\partial\det}{\partial a}=d$, $\frac{\partial\det}{\partial b}=-c$, $\frac{\partial\det}{\partial c}=-b$, $\frac{\partial\det}{\partial d}=a$: contínues a tot $\mathbb{R}^4$. Per la condició suficient, $\det$ és diferenciable a tot $\mathbb{R}^4$. (Alternativament: les projeccions són lineals, i per tant diferenciables, i $ad-bc$ és suma de productes d'aquestes.)
ERRORS COMUNS:
  - [identificacio] Confon l'ordre de les coordenades donat per $F$ (per exemple pren $c$ com la segona coordenada).
  - [sense_justificar] Diu "és un polinomi, per tant és diferenciable" sense relacionar-ho amb cap resultat.

TEORIA DEL CURS QUE FA SERVIR:
[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

[T3.23] Proposició 23 (Tema 3) — Àlgebra de funcions diferenciables
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciables en $a\in\mathring{\Omega}$ i sigui $\lambda\in\mathbb{R}$. Llavors,

(i) $f+g$ és diferenciable en $a$ i $D(f+g)(a)=Df(a)+Dg(a)$.

(ii) $\lambda f$ és diferenciable en $a$ i $D(\lambda f)(a)=\lambda Df(a)$.

(iii) $fg$ és diferenciable en $a$ i $J(fg)(a)=g(a)Jf(a)+f(a)Jg(a)$.

(iv) $\dfrac{f}{g}$ és diferenciable en $a$ si $g(a)\neq0$. A més
$$J\left(\frac{f}{g}\right)(a)=\frac{g(a)Jf(a)-f(a)Jg(a)}{g(a)^2}.$$
</solucio_de_referencia>

### Document a revisar

[1] Amb la identificació $F$, la matriu $\begin{pmatrix}a&c\\b&d\end{pmatrix}$ correspon al punt $(a,b,c,d)\in\mathbb{R}^4$, i el seu determinant és $ad-bc$. Per tant, en coordenades, $\det(a,b,c,d)=ad-bc$.
[2] Les derivades parcials són $\dfrac{\partial\det}{\partial a}=d$, $\dfrac{\partial\det}{\partial b}=c$, $\dfrac{\partial\det}{\partial c}=-b$ i $\dfrac{\partial\det}{\partial d}=a$.
[3] Totes són funcions polinòmiques de $(a,b,c,d)$ (de fet, lineals), per tant existeixen i són contínues a tot $\mathbb{R}^4$.
[4] Per la condició suficient de diferenciabilitat (parcials que existeixen i són contínues a l'obert $\mathbb{R}^4$), $\det$ és diferenciable a tot $\mathbb{R}^4\cong M_2(\mathbb{R})$; de fet és de classe $\mathcal{C}^1$.
[5] A més, la diferencial de $\det$ en qualsevol matriu $A$ és l'aplicació $H\mapsto\det H$, és a dir, $D\det(A)(H)=\det H$.

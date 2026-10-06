## t4-2:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Comproveu que les derivades creuades de segon ordre de la funció
$$f(x,y)=\begin{cases}xy^2\sin\dfrac{1}{y} & \text{si } y\neq 0\\ 0 & \text{si } y=0\end{cases}$$
coincideixen a $(0,0)$, tot i que no se satisfà la hipòtesi del teorema de Schwarz.
RESULTAT CORRECTE: $f_x(x,y)=y^2\sin(1/y)$ si $y\neq 0$ i $f_x(x,0)=0$; $f_y(x,y)=2xy\sin(1/y)-x\cos(1/y)$ si $y\neq 0$ i $f_y(x,0)=0$. Llavors $\frac{\partial}{\partial y}(f_x)(0,0)=\lim_{k\to0}k\sin(1/k)=0$ i $\frac{\partial}{\partial x}(f_y)(0,0)=0$: les creuades coincideixen (valen $0$). Però per $y\neq 0$ les dues creuades valen $2y\sin(1/y)-\cos(1/y)$, que no té límit quan $(x,y)\to(0,0)$; per tant no són contínues en cap entorn de l'origen i la hipòtesi del teorema de Schwarz falla.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [primeres] Derivades primeres  (teoria: T3.2)
     objectiu: Calcular $f_x$ i $f_y$ en tots els punts, incloent-hi els de l'eix $y=0$.
     idea: Per $y\neq 0$ es deriva amb les regles habituals. Sobre l'eix $y=0$ la funció es defineix a part: cal usar la definició de derivada parcial com a límit.
     detall: Per $y\neq 0$: $f_x=y^2\sin(1/y)$, $f_y=2xy\sin(1/y)-x\cos(1/y)$. Per $y=0$: $f(x+h,0)=0$, així $f_x(x,0)=0$; i $f_y(x,0)=\lim_{k\to 0}\frac{xk^2\sin(1/k)}{k}=\lim_{k\to0}xk\sin(1/k)=0$ (producte d'una funció fitada per una que tendeix a $0$).
  2. [creuades_origen] Derivades creuades a l'origen  (teoria: T3.2, T5.1)
     objectiu: Calcular les dues derivades creuades a $(0,0)$.
     idea: Tornar a aplicar la definició de derivada parcial a les funcions $f_x$ (en la direcció $y$) i $f_y$ (en la direcció $x$) a l'origen.
     detall: $\frac{\partial}{\partial y}(f_x)(0,0)=\lim_{k\to0}\frac{f_x(0,k)-f_x(0,0)}{k}=\lim_{k\to0}\frac{k^2\sin(1/k)}{k}=\lim_{k\to 0}k\sin(1/k)=0$. $\frac{\partial}{\partial x}(f_y)(0,0)=\lim_{h\to0}\frac{f_y(h,0)-f_y(0,0)}{h}=\lim_{h\to 0}\frac{0}{h}=0$. Coincideixen.
  3. [hipotesi_falla] La hipòtesi de Schwarz no es compleix  (teoria: T5.6, T5.7)
     objectiu: Justificar que les derivades creuades no són contínues en cap entorn de l'origen.
     idea: Calcular les derivades creuades fora de l'eix $y=0$ i estudiar-ne el límit quan $(x,y)\to(0,0)$ per una successió de punts adequada.
     detall: Per $y\neq 0$: $\frac{\partial}{\partial y}(f_x)=2y\sin(1/y)-\cos(1/y)$ i $\frac{\partial}{\partial x}(f_y)=2y\sin(1/y)-\cos(1/y)$. Sobre els punts $(0,1/(n\pi))\to(0,0)$ valen $-\cos(n\pi)=(-1)^{n+1}$, que no té límit. Per tant cap de les dues és contínua a $(0,0)$ (de fet, en cap punt de l'eix $y=0$), i el teorema de Schwarz (ni la seva versió forta) no es pot aplicar en cap entorn de l'origen.
ERRORS COMUNS:
  - [formula_a_leix] Usa la fórmula de $f_y$ per $y\neq 0$ per calcular $f_y(x,0)$ (on no té sentit perquè hi apareix $1/y$), o afirma que $f_y(x,0)$ no existeix.
  - [coincidencia_implica_continuitat] Creu que, com que les creuades coincideixen a l'origen, les hipòtesis de Schwarz s'han de complir (confon condició suficient amb necessària).
  - [continuitat_de_f] Comprova la continuïtat de $f$ o de les derivades primeres en lloc de la de les derivades segones creuades.

TEORIA DEL CURS QUE FA SERVIR:
[T5.6] Teorema 6 (Tema 5) — Teorema de Schwarz
(Schwarz). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$ i $D_iD_jf$ i $D_jD_if$ existeixen en $\Omega$. Si $D_iD_jf$ i $D_jD_if$ són contínues en un entorn d'$\mathbf{a}\in\Omega$, aleshores
$$D_iD_jf(\mathbf{a})=D_jD_if(\mathbf{a}).$$

[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T5.1] Definició 1 (Tema 5) — Derivades parcials r-èsimes
Denotem les derivades parcials $r$-èsimes com $\dfrac{\partial^r f}{\partial x_{i_1}\cdots\partial x_{i_r}}(p)$. També farem servir la notació abreujada $D_{i_r}\ldots D_{i_1}f$ o $D_{i_1\cdots i_r}f$, i la notació $f_{i_1\ldots i_r}$. Fixem-nos que l'ordre dels subíndexos canvia segons la notació.

[T5.7] Teorema 7 (Tema 5) — Schwarz, versió forta
(Schwarz, versió forta). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$ i $D_jD_if$ existeixen en $\Omega$. Si, a més, $D_jD_if$ és contínua en $\Omega$, aleshores $D_iD_jf(\mathbf{a})$ també existeix i $D_iD_jf(\mathbf{a})=D_jD_if(\mathbf{a})$.
</solucio_de_referencia>

### Document a revisar

[1] Per $y\neq 0$ la funció és $f(x,y)=xy^2\sin(1/y)$ i, derivant, $f_x(x,y)=y^2\sin(1/y)$ i $f_y(x,y)=2xy\sin(1/y)-x\cos(1/y)$.
[2] Sobre l'eix $y=0$ la fórmula anterior no val i cal anar a la definició. Com que $f(x+h,0)=0$ per a tot $h$, tenim $f_x(x,0)=0$.
[3] També $f_y(x,0)=\lim_{k\to 0}\frac{f(x,k)-f(x,0)}{k}=\lim_{k\to 0}\frac{xk^2\sin(1/k)}{k}=\lim_{k\to 0}xk\sin(1/k)=0$, ja que $\sin(1/k)\to 0$ quan $k\to 0$.
[4] Derivada creuada $\frac{\partial}{\partial y}(f_x)$ a l'origen: $\lim_{k\to 0}\frac{f_x(0,k)-f_x(0,0)}{k}=\lim_{k\to 0}\frac{k^2\sin(1/k)}{k}=\lim_{k\to 0}k\sin(1/k)=0$, perquè $|k\sin(1/k)|\le|k|$.
[5] Derivada creuada $\frac{\partial}{\partial x}(f_y)$ a l'origen: $\lim_{h\to 0}\frac{f_y(h,0)-f_y(0,0)}{h}=\lim_{h\to 0}\frac{0-0}{h}=0$. Per tant les dues derivades creuades coincideixen a $(0,0)$ i hi valen $0$.
[6] Per veure si se satisfà la hipòtesi de Schwarz, calculem les creuades fora de l'eix: per $y\neq 0$, $\frac{\partial}{\partial y}(f_x)=2y\sin(1/y)-\cos(1/y)$ i $\frac{\partial}{\partial x}(f_y)=2y\sin(1/y)-\cos(1/y)$.
[7] Sobre els punts $(0,1/(n\pi))\to(0,0)$ aquestes derivades valen $-\cos(n\pi)=(-1)^{n+1}$, que no té límit. Per tant cap de les dues creuades és contínua a $(0,0)$, l'únic punt del pla on deixen de ser contínues, i la hipòtesi del teorema de Schwarz no se satisfà.


## t4-3:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $G(r,\varphi)=(r\cos\varphi,r\sin\varphi)$ (canvi a polars). Donada $f:\mathbb{R}^2\to\mathbb{R}$, una funció de classe $\mathcal{C}^2$, sigui $F=f\circ G$. Si $f_{ij}$ vol dir la derivada segona de $f$ respecte $x_i,x_j$, demostreu que
$$(f_{xx}+f_{yy})\circ G=F_{rr}+\frac{1}{r^2}F_{\varphi\varphi}+\frac{1}{r}F_r.$$
L'expressió $f_{xx}+f_{yy}$ s'anomena el *laplacià de $f$* i s'escriu $\Delta f$. La igualtat anterior dona l'expressió del laplacià de $f$ en coordenades polars.
RESULTAT CORRECTE: Per la regla de la cadena (amb $f_x,f_y,f_{xx},\dots$ avaluades en $G(r,\varphi)$): $F_r=\cos\varphi\,f_x+\sin\varphi\,f_y$, $F_{rr}=\cos^2\varphi\,f_{xx}+2\sin\varphi\cos\varphi\,f_{xy}+\sin^2\varphi\,f_{yy}$, $F_\varphi=-r\sin\varphi\,f_x+r\cos\varphi\,f_y$, $F_{\varphi\varphi}=r^2\sin^2\varphi\,f_{xx}-2r^2\sin\varphi\cos\varphi\,f_{xy}+r^2\cos^2\varphi\,f_{yy}-rF_r$ (usant $f_{xy}=f_{yx}$ per Schwarz). Llavors, per $r\neq 0$, $F_{rr}+\frac{1}{r^2}F_{\varphi\varphi}+\frac1rF_r=f_{xx}+f_{yy}$ avaluat en $G(r,\varphi)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [primeres] Derivades primeres de F  (teoria: T3.21, T3.22)
     objectiu: Expressar $F_r$ i $F_\varphi$ en termes de les derivades parcials de $f$.
     idea: $F$ és una composició; aplicar la regla de la cadena (producte de jacobianes) i recordar on s'avaluen les derivades de $f$.
     detall: $JG=\begin{pmatrix}\cos\varphi&-r\sin\varphi\\ \sin\varphi&r\cos\varphi\end{pmatrix}$, per tant $F_r=\cos\varphi\,f_x(G)+\sin\varphi\,f_y(G)$ i $F_\varphi=-r\sin\varphi\,f_x(G)+r\cos\varphi\,f_y(G)$.
  2. [segones] Derivades segones de F  (teoria: T3.21, T5.6)
     objectiu: Calcular $F_{rr}$ i $F_{\varphi\varphi}$ en termes de les derivades de $f$.
     idea: Derivar de nou: cada $f_x(G(r,\varphi))$ i $f_y(G(r,\varphi))$ és també una composició (regla de la cadena), i els coeficients $\cos\varphi$, $r\sin\varphi$… també depenen de les variables (regla del producte). Com que $f$ és $\mathcal{C}^2$, les derivades creuades coincideixen.
     detall: $F_{rr}=\cos\varphi(\cos\varphi f_{xx}+\sin\varphi f_{xy})+\sin\varphi(\cos\varphi f_{yx}+\sin\varphi f_{yy})=\cos^2\varphi f_{xx}+2\sin\varphi\cos\varphi f_{xy}+\sin^2\varphi f_{yy}$.
$F_{\varphi\varphi}=-r\cos\varphi f_x-r\sin\varphi f_y-r\sin\varphi(-r\sin\varphi f_{xx}+r\cos\varphi f_{xy})+r\cos\varphi(-r\sin\varphi f_{yx}+r\cos\varphi f_{yy})=r^2\sin^2\varphi f_{xx}-2r^2\sin\varphi\cos\varphi f_{xy}+r^2\cos^2\varphi f_{yy}-rF_r$, on s'ha usat $f_{xy}=f_{yx}$ (teorema de Schwarz).
  3. [combinar] Combinar
     objectiu: Comprovar la igualtat de l'enunciat.
     idea: Dividir $F_{\varphi\varphi}$ per $r^2$ (cal $r\neq 0$), sumar $F_{rr}$ i $\frac1rF_r$ i usar $\sin^2\varphi+\cos^2\varphi=1$.
     detall: $\frac{1}{r^2}F_{\varphi\varphi}=\sin^2\varphi f_{xx}-2\sin\varphi\cos\varphi f_{xy}+\cos^2\varphi f_{yy}-\frac1rF_r$. Sumant $F_{rr}$ i $\frac1rF_r$: els termes en $f_{xy}$ i en $F_r$ es cancel·len i queda $(\cos^2\varphi+\sin^2\varphi)(f_{xx}+f_{yy})=(f_{xx}+f_{yy})\circ G$.
ERRORS COMUNS:
  - [oblidar_producte] En derivar $F_\varphi$ respecte de $\varphi$ oblida derivar els coeficients $-r\sin\varphi$ i $r\cos\varphi$ (regla del producte) i perd el terme $-rF_r$.
  - [avaluacio_derivades] Tracta $f_x$, $f_y$ com a constants en tornar a derivar, en lloc de funcions de $(r,\varphi)$ a través de $G$.
  - [sense_schwarz] No justifica per què els termes amb $f_{xy}$ i $f_{yx}$ es poden agrupar.

TEORIA DEL CURS QUE FA SERVIR:
[T3.31] Definició 31 (Tema 3) — Classes C^r de funcions
Direm que $f\in\mathcal{C}^0(\Omega)\Leftrightarrow f$ és contínua a $\Omega$.

$f\in\mathcal{C}^1(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ a tot punt de $\Omega$ i totes són contínues (per tant, en particular, $f$ és diferenciable i contínua).

$f\in\mathcal{C}^2(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ d'ordre $2$:
$$\frac{\partial^2f}{\partial x_i\partial x_j}=\frac{\partial}{\partial x_j}\left(\frac{\partial f}{\partial x_i}\right),$$
a tot punt de $\Omega$ i són contínues.

En general, per a $r\geq1$, es diu que $f\in\mathcal{C}^r(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials d'ordre $r$ a $\Omega$ i totes són contínues. Clarament, $f\in\mathcal{C}^{r+1}(\Omega)\Rightarrow f\in\mathcal{C}^r(\Omega)$.

Direm que $f\in\mathcal{C}^\infty(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials a qualsevol ordre de $f$ a $\Omega$ i totes són contínues.

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

[T5.6] Teorema 6 (Tema 5) — Teorema de Schwarz
(Schwarz). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$ i $D_iD_jf$ i $D_jD_if$ existeixen en $\Omega$. Si $D_iD_jf$ i $D_jD_if$ són contínues en un entorn d'$\mathbf{a}\in\Omega$, aleshores
$$D_iD_jf(\mathbf{a})=D_jD_if(\mathbf{a}).$$
</solucio_de_referencia>

### Document a revisar

[1] Com que $G$ és de classe $\mathcal{C}^\infty$ i $f$ és de classe $\mathcal{C}^2$, la composició $F=f\circ G$ és de classe $\mathcal{C}^\infty$ i podem aplicar la regla de la cadena tantes vegades com calgui.
[2] La jacobiana del canvi és $JG=\begin{pmatrix}\cos\varphi&-r\sin\varphi\\ \sin\varphi&r\cos\varphi\end{pmatrix}$, de manera que, amb $f_x,f_y$ avaluades en $G(r,\varphi)$, $F_r=\cos\varphi\,f_x+\sin\varphi\,f_y$ i $F_\varphi=-r\sin\varphi\,f_x+r\cos\varphi\,f_y$.
[3] Per tornar a derivar cal tenir en compte que $f_x$ i $f_y$ també estan avaluades en $G(r,\varphi)$: per la regla de la cadena, $\partial_r(f_x\circ G)=\cos\varphi\,f_{xx}+\sin\varphi\,f_{xy}$, $\partial_r(f_y\circ G)=\cos\varphi\,f_{yx}+\sin\varphi\,f_{yy}$, $\partial_\varphi(f_x\circ G)=-r\sin\varphi\,f_{xx}+r\cos\varphi\,f_{xy}$ i $\partial_\varphi(f_y\circ G)=-r\sin\varphi\,f_{yx}+r\cos\varphi\,f_{yy}$.
[4] Com que existeixen totes les derivades segones de $f$, el teorema de Schwarz dona $f_{xy}=f_{yx}$, i llavors $F_{rr}=\cos^2\varphi\,f_{xx}+2\sin\varphi\cos\varphi\,f_{xy}+\sin^2\varphi\,f_{yy}$.
[5] Derivant $F_\varphi$ respecte de $\varphi$ amb la regla del producte, $F_{\varphi\varphi}=-r\cos\varphi\,f_x-r\sin\varphi\,f_y-r\sin\varphi\,\partial_\varphi(f_x\circ G)+r\cos\varphi\,\partial_\varphi(f_y\circ G)$, és a dir, $F_{\varphi\varphi}=r^2\sin^2\varphi\,f_{xx}-2r^2\sin\varphi\cos\varphi\,f_{xy}+r^2\cos^2\varphi\,f_{yy}-rF_r$.
[6] Per $r\neq 0$, dividint per $r^2$: $\frac{1}{r^2}F_{\varphi\varphi}=\sin^2\varphi\,f_{xx}-2\sin\varphi\cos\varphi\,f_{xy}+\cos^2\varphi\,f_{yy}-\frac{1}{r}F_r$.
[7] Sumant $F_{rr}+\frac{1}{r^2}F_{\varphi\varphi}+\frac{1}{r}F_r$, els termes en $f_{xy}$ i els termes en $F_r$ es cancel·len i queda $(\cos^2\varphi+\sin^2\varphi)(f_{xx}+f_{yy})=(f_{xx}+f_{yy})\circ G$, per a $r\neq 0$, que és l'expressió del laplacià en polars.


## t4-4:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Siguin $f,g:\mathbb{R}\to\mathbb{R}$ funcions dues vegades diferenciables i $c>0$ una constant. Proveu que la funció $\varphi(x,t)=f(x-ct)+g(x+ct)$ satisfà l'equació d'ones,
$$\frac{1}{c^2}\frac{\partial^2\varphi}{\partial t^2}-\frac{\partial^2\varphi}{\partial x^2}=0.$$
RESULTAT CORRECTE: Per la regla de la cadena, $\varphi_t=-cf'(x-ct)+cg'(x+ct)$, $\varphi_{tt}=c^2f''(x-ct)+c^2g''(x+ct)$, $\varphi_x=f'(x-ct)+g'(x+ct)$, $\varphi_{xx}=f''(x-ct)+g''(x+ct)$. Per tant $\frac{1}{c^2}\varphi_{tt}-\varphi_{xx}=0$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [derivades_t] Derivades respecte de t  (teoria: T3.21)
     objectiu: Calcular $\frac{\partial\varphi}{\partial t}$ i $\frac{\partial^2\varphi}{\partial t^2}$.
     idea: Cada sumand és la composició d'una funció d'una variable amb una funció afí de $(x,t)$: regla de la cadena, dues vegades.
     detall: $\varphi_t=f'(x-ct)\cdot(-c)+g'(x+ct)\cdot c$ i, com que $f',g'$ són derivables, $\varphi_{tt}=c^2f''(x-ct)+c^2g''(x+ct)$.
  2. [derivades_x] Derivades respecte de x  (teoria: T3.21)
     objectiu: Calcular $\frac{\partial\varphi}{\partial x}$ i $\frac{\partial^2\varphi}{\partial x^2}$.
     idea: Mateix procediment, ara la derivada interior de $x\mp ct$ respecte de $x$.
     detall: $\varphi_x=f'(x-ct)+g'(x+ct)$ i $\varphi_{xx}=f''(x-ct)+g''(x+ct)$.
  3. [substituir] Substituir a l'equació
     objectiu: Comprovar que es compleix l'equació d'ones.
     idea: Substituir les derivades obtingudes.
     detall: $\frac{1}{c^2}\varphi_{tt}-\varphi_{xx}=f''(x-ct)+g''(x+ct)-f''(x-ct)-g''(x+ct)=0$.
ERRORS COMUNS:
  - [signe_derivada_interior] Oblida el factor $-c$ (o $c$) de la derivada interior, o no l'eleva al quadrat a la segona derivada.
  - [confondre_variables] Escriu $f''(x)$ en lloc de $f''(x-ct)$, perdent el punt on s'avalua la derivada.

TEORIA DEL CURS QUE FA SERVIR:
[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$
</solucio_de_referencia>

### Document a revisar

[1] Escrivim $\varphi(x,t)=f(u)+g(w)$ amb $u=x-ct$ i $w=x+ct$. Per poder aplicar la regla de la cadena dues vegades cal que $f$ i $g$ siguin de classe $\mathcal{C}^2$, i això ja ho tenim perquè són dues vegades diferenciables.
[2] Derivant respecte de $t$, com que $\frac{\partial u}{\partial t}=-c$ i $\frac{\partial w}{\partial t}=c$, obtenim $\varphi_t=-c\,f'(x-ct)+c\,g'(x+ct)$.
[3] Com que $f'$ i $g'$ són derivables, tornant a derivar respecte de $t$: $\varphi_{tt}=(-c)^2f''(x-ct)+c^2g''(x+ct)=c^2f''(x-ct)+c^2g''(x+ct)$.
[4] Derivant respecte de $x$, amb $\frac{\partial u}{\partial x}=\frac{\partial w}{\partial x}=1$: $\varphi_x=f'(x-ct)+g'(x+ct)$ i $\varphi_{xx}=f''(x-ct)+g''(x+ct)$.
[5] Per tant $\frac{1}{c^2}\varphi_{tt}-\varphi_{xx}=f''(x-ct)+g''(x+ct)-f''(x-ct)-g''(x+ct)=0$ per a tot $(x,t)\in\mathbb{R}^2$.
[6] Observem que aquí és imprescindible que $c>0$: si fos $c<0$, la funció $\varphi$ ja no satisfaria l'equació d'ones.


## t4-5c:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Per a les funcions següents, determineu si $G$ satisfà les hipòtesis del teorema de la funció inversa; trobeu la imatge de $G$ i, si $G$ és injectiva, calculeu explícitament $G^{-1}$:

(c) $\mathrm{Dom}(G)=\mathbb{R}^2\setminus\{(0,0)\}$, $G(x,y)=(x^2-y^2,xy)$;
RESULTAT CORRECTE: $G$ és $\mathcal{C}^\infty$ en l'obert $\mathbb{R}^2\setminus\{(0,0)\}$ i $\det JG=2(x^2+y^2)\neq 0$: satisfà les hipòtesis del TFI a tot punt del domini. La imatge és $\mathbb{R}^2\setminus\{(0,0)\}$. No és injectiva ($G(-x,-y)=G(x,y)$), per tant no té inversa global.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [hipotesis] Hipòtesis del TFI  (teoria: T4.5, T3.31)
     objectiu: Comprovar si $G$ compleix les hipòtesis del teorema de la funció inversa en els punts del domini.
     idea: Calcular la jacobiana i el seu determinant i veure on s'anul·la.
     detall: $JG=\begin{pmatrix}2x&-2y\\ y&x\end{pmatrix}$, $\det JG=2x^2+2y^2$, que només s'anul·la a $(0,0)$, punt exclòs del domini (obert). $G$ és polinòmica, per tant $\mathcal{C}^\infty$.
  2. [injectivitat] Injectivitat
     objectiu: Decidir si $G$ és injectiva en el seu domini.
     idea: Buscar simetries de l'expressió de $G$: hi ha punts diferents amb la mateixa imatge?
     detall: $G(-x,-y)=((-x)^2-(-y)^2,(-x)(-y))=G(x,y)$ i $(-x,-y)\neq(x,y)$ si $(x,y)\neq(0,0)$. No és injectiva: no hi ha $G^{-1}$ global (només inverses locals pel TFI).
  3. [imatge] Imatge
     objectiu: Determinar $G(\mathbb{R}^2\setminus\{(0,0)\})$.
     idea: Donat $(u,v)$, resoldre $x^2-y^2=u$, $xy=v$. Pot ajudar escriure $z=x+iy$ i observar que $z^2=(x^2-y^2)+2ixy$, o bé usar polars.
     detall: $G(x,y)=(0,0)$ obliga $xy=0$ i $x^2=y^2$, és a dir $x=y=0$: l'origen no és a la imatge. Recíprocament, donat $(u,v)\neq(0,0)$, el nombre complex $w=u+2iv\neq 0$ té una arrel quadrada $z=x+iy\neq 0$, i llavors $x^2-y^2=u$, $2xy=2v$. En polars: $G(\rho\cos\theta,\rho\sin\theta)=\rho^2(\cos 2\theta,\tfrac12\sin 2\theta)$, que recorre tot el pla menys l'origen. Imatge: $\mathbb{R}^2\setminus\{(0,0)\}$.
ERRORS COMUNS:
  - [det_no_nul_injectiva] Conclou que $G$ és injectiva perquè el determinant de la jacobiana no s'anul·la en cap punt del domini.
  - [imatge_incompleta] Afirma que la imatge és tot $\mathbb{R}^2$, o només un semiplà, sense resoldre l'equació $G(x,y)=(u,v)$.

TEORIA DEL CURS QUE FA SERVIR:
[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.

[T3.31] Definició 31 (Tema 3) — Classes C^r de funcions
Direm que $f\in\mathcal{C}^0(\Omega)\Leftrightarrow f$ és contínua a $\Omega$.

$f\in\mathcal{C}^1(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ a tot punt de $\Omega$ i totes són contínues (per tant, en particular, $f$ és diferenciable i contínua).

$f\in\mathcal{C}^2(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ d'ordre $2$:
$$\frac{\partial^2f}{\partial x_i\partial x_j}=\frac{\partial}{\partial x_j}\left(\frac{\partial f}{\partial x_i}\right),$$
a tot punt de $\Omega$ i són contínues.

En general, per a $r\geq1$, es diu que $f\in\mathcal{C}^r(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials d'ordre $r$ a $\Omega$ i totes són contínues. Clarament, $f\in\mathcal{C}^{r+1}(\Omega)\Rightarrow f\in\mathcal{C}^r(\Omega)$.

Direm que $f\in\mathcal{C}^\infty(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials a qualsevol ordre de $f$ a $\Omega$ i totes són contínues.
</solucio_de_referencia>

### Document a revisar

[1] El domini $\mathbb{R}^2\setminus\{(0,0)\}$ és obert i $G(x,y)=(x^2-y^2,xy)$ té components polinòmiques, per tant $G$ és de classe $\mathcal{C}^\infty$.
[2] La jacobiana és $JG(x,y)=\begin{pmatrix}2x&-2y\\ y&x\end{pmatrix}$, amb $\det JG(x,y)=2x^2+2y^2$, que només s'anul·la a $(0,0)$, punt que no és del domini. Per tant $G$ satisfà les hipòtesis del teorema de la funció inversa a tot punt del domini.
[3] Tanmateix, $G(-x,-y)=\big((-x)^2-(-y)^2,(-x)(-y)\big)=G(x,y)$, i $(-x,-y)\neq(x,y)$ perquè $(x,y)\neq(0,0)$. Així $G$ no és injectiva i no té inversa global; el teorema només en dona inverses locals.
[4] Imatge. Si $G(x,y)=(0,0)$, aleshores $xy=0$ i $x^2=y^2$; de $xy=0$ obtenim $x=0$, i llavors $y^2=0$, és a dir $y=0$. Com que $(0,0)$ no és del domini, l'origen no és a la imatge.
[5] En polars, $G(\rho\cos\theta,\rho\sin\theta)=\big(\rho^2(\cos^2\theta-\sin^2\theta),\rho^2\sin\theta\cos\theta\big)$, és a dir, $G(\rho\cos\theta,\rho\sin\theta)=\rho^2(\cos 2\theta,\sin 2\theta)$, que, en variar $\rho>0$ i $\theta$, recorre tot el pla menys l'origen.
[6] Rigorosament: donat $(u,v)\neq(0,0)$, el nombre complex $w=u+2iv$ és no nul i té una arrel quadrada $z=x+iy\neq 0$; de $z^2=w$ surt $x^2-y^2=u$ i $2xy=2v$, és a dir, $G(x,y)=(u,v)$ amb $(x,y)\neq(0,0)$.
[7] Per tant la imatge de $G$ és $\mathbb{R}^2\setminus\{(0,0)\}$. Com que $G$ no és injectiva (cada punt de la imatge té almenys les dues antiimatges $(x,y)$ i $(-x,-y)$), no existeix $G^{-1}$.


## t4-6c:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem la funció definida per $G(s,t)=(\cosh(s)\cos(t),\sinh(s)\sin(t))$.

(c) Demostreu que la restricció de $G$ a $\{(s,t)\in A\mid 0<t<2\pi\}$ té inversa global.
RESULTAT CORRECTE: Sigui $B=\{s>0,\ 0<t<2\pi\}$. $G|_B$ és injectiva: si $G(s,t)=(x,y)$, aleshores $\frac{x^2}{\cosh^2s}+\frac{y^2}{\sinh^2s}=1$, i com que $(x,y)\neq(0,0)$ la funció $s\mapsto\frac{x^2}{\cosh^2s}+\frac{y^2}{\sinh^2s}$ és estrictament decreixent a $(0,\infty)$, $s$ queda determinat; llavors $\cos t=x/\cosh s$ i $\sin t=y/\sinh s$ determinen $t\in(0,2\pi)$. Com que $G\in\mathcal{C}^\infty$, és injectiva a $B$ i $\det JG\neq 0$ a $B$, $G:B\to G(B)$ és un difeomorfisme $\mathcal{C}^\infty$ (amb $G(B)$ obert): té inversa global $\mathcal{C}^\infty$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [el_lipses] Corbes s constant
     objectiu: Trobar una relació entre $x=\cosh s\cos t$ i $y=\sinh s\sin t$ que no depengui de $t$.
     idea: Aïllar $\cos t$ i $\sin t$ (amb $s>0$ els denominadors no s'anul·len) i usar $\cos^2t+\sin^2t=1$.
     detall: Per $s>0$: $\cos t=\frac{x}{\cosh s}$, $\sin t=\frac{y}{\sinh s}$, per tant $\frac{x^2}{\cosh^2s}+\frac{y^2}{\sinh^2s}=1$: la corba $s=$ constant és una el·lipse (de focus $(\pm1,0)$).
  2. [injectivitat] Injectivitat a B
     objectiu: Demostrar que si $G(s_1,t_1)=G(s_2,t_2)$ amb $(s_i,t_i)\in B$, aleshores $(s_1,t_1)=(s_2,t_2)$.
     idea: Veure que el punt imatge determina $s$ (estudiant la monotonia en $s$ de l'expressió del pas anterior) i que, fixat $s$, el punt determina $t$ dins d'un interval de longitud $2\pi$.
     detall: Sigui $(x,y)=G(s,t)$ amb $s>0$; no pot ser $(0,0)$ (caldria $\cos t=0$ i llavors $\sinh s\,|\sin t|=\sinh s>0$). La funció $\phi(\sigma)=\frac{x^2}{\cosh^2\sigma}+\frac{y^2}{\sinh^2\sigma}$ és estrictament decreixent a $(0,\infty)$ (cada terme és no creixent i almenys un és estrictament decreixent perquè $x$ o $y$ és no nul), per tant $\phi(\sigma)=1$ té com a única solució $\sigma=s$. Fixat $s$, $(\cos t,\sin t)=\big(\frac{x}{\cosh s},\frac{y}{\sinh s}\big)$ determina $t$ mòdul $2\pi$, i per tant de manera única a $(0,2\pi)$.
  3. [difeomorfisme] Inversa global diferenciable  (teoria: T4.9, T4.8, T4.5)
     objectiu: Concloure que $G|_B$ té inversa global (i quina regularitat té).
     idea: Combinar la injectivitat amb el que ja se sap del determinant i de la regularitat: hi ha una caracterització de difeomorfisme amb aquestes tres condicions.
     detall: $B$ és obert, $G\in\mathcal{C}^\infty(B)$, injectiva a $B$ i $\det JG>0$ a $B$. Per tant $G:B\to G(B)$ és bijectiva, $G(B)$ és obert (aplicació oberta) i la inversa és $\mathcal{C}^\infty$ (localment coincideix amb les inverses locals del TFI): $G|_B$ és un difeomorfisme sobre la seva imatge.
ERRORS COMUNS:
  - [injectivitat_per_det] Dedueix la injectivitat de $G|_B$ només de $\det JG\neq 0$.
  - [nomes_t] Demostra que, fixat $s$, $t$ és únic, però no que punts amb $s$ diferents tinguin imatges diferents.
  - [inversa_sense_regularitat] Conclou "té inversa" però no justifica que sigui contínua o diferenciable.

TEORIA DEL CURS QUE FA SERVIR:
[T4.9] Definició 9 (Tema 4) — Homeomorfisme i difeomorfisme
1. Una funció $f:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$ és un homeomorfisme si $f$ és bijectiva, contínua i la seva inversa $f^{-1}$ també és contínua.

2. Una funció $f:U\longrightarrow V$ entre dos oberts $U,V$ de $\mathbb{R}^n$ és un difeomorfisme (o una transformació regular) de classe $C^r$, amb $r\geq 1$, si $f$ és bijectiva, de classe $C^r$ i la seva inversa $f^{-1}$ també és de classe $C^r$.

Els homeomorfisme preserven la forma topològica, mentre que els difeomorfisme també preserven l'estructura diferenciable.

[Resum 91'] Una definició alternativa de difeomorfisme és: Una funció $f:U\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$, amb $U$ obert de $\mathbb{R}^n$, és un difeomorfisme si $f\in\mathcal{C}^1(U)$, $f$ és injectiva, i $\det\big(Jf(x)\big)\neq 0$ per a tot $x\in U$.

[T4.8] Corol·lari 8 (Tema 4) — Teorema de l'aplicació oberta
Teorema de l'aplicació oberta. Sigui $f:U\subseteq\mathbb{R}^n\to V\subseteq\mathbb{R}^n$ una funció $\mathcal{C}^1(U)$ tal que $\det Jf(a)\neq 0$ per a tot $a\in U$. Aleshores, per a tot obert $B\subseteq U$, $f(B)$ és també un obert.

[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.
</solucio_de_referencia>

### Document a revisar

[1] Sigui $B=\{(s,t)\in\mathbb{R}^2\mid s>0,\ 0<t<2\pi\}$, que és obert. Sabem que $G\in\mathcal{C}^\infty(\mathbb{R}^2)$ i, per l'apartat (a), $\det JG(s,t)=\sinh^2s+\sin^2t>0$ a tot $B$. Falta veure que $G|_B$ és injectiva.
[2] Sigui $(x,y)=G(s,t)$ amb $(s,t)\in B$. Com que $\cosh s>0$ i $\sinh s>0$, tenim $\cos t=\frac{x}{\cosh s}$ i $\sin t=\frac{y}{\sinh s}$, i per tant $\frac{x^2}{\cosh^2s}+\frac{y^2}{\sinh^2s}=1$.
[3] A més, $(x,y)\neq(0,0)$: si $x=0$, aleshores $\cos t=0$, $|\sin t|=1$ i $|y|=\sinh s>0$.
[4] Considerem $\phi(\sigma)=\frac{x^2}{\cosh^2\sigma}+\frac{y^2}{\sinh^2\sigma}$ per a $\sigma>0$. Com que $\cosh$ i $\sinh$ són positives i estrictament creixents a $(0,\infty)$, i $x$ o $y$ és no nul, $\phi$ és estrictament creixent a $(0,\infty)$.
[5] Per tant l'equació $\phi(\sigma)=1$ té com a única solució $\sigma=s$: el punt $(x,y)$ determina $s$.
[6] Un cop fixat $s$, la igualtat $\cos t=\frac{x}{\cosh s}$ determina $t$ de manera única a l'interval $(0,2\pi)$. Així, si $G(s,t)=G(s',t')$ amb $(s,t),(s',t')\in B$, aleshores $s=s'$ i $t=t'$: $G|_B$ és injectiva.
[7] Per tant $G:B\to G(B)$ és bijectiva; $G(B)$ és obert pel teorema de l'aplicació oberta, i la inversa és de classe $\mathcal{C}^\infty$ perquè, entorn de cada punt de $G(B)$, coincideix amb la inversa local que dona el teorema de la funció inversa. Així $G|_B$ té inversa global de classe $\mathcal{C}^\infty$.


## t4-7d:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $F:\mathbb{R}^2\to\mathbb{R}^2$ definida per $F(x,y)=(x^2y,xy^2)$.

(d) Sigui $A=\{(x,y)\in\mathbb{R}^2\mid x\neq 0,\ y\neq 0\}$. Proveu que la restricció de $F$ a $A$ és injectiva i doneu-ne explícitament la funció inversa. Calculeu $F^{-1}(4.1,1.9)$ i compareu el resultat amb l'aproximació de l'apartat anterior.
RESULTAT CORRECTE: Si $F(x,y)=(u,v)$ amb $(x,y)\in A$, aleshores $u^2/v=x^3$ i $v^2/u=y^3$, que determinen $x,y$ (l'arrel cúbica real és injectiva): $F|_A$ és injectiva, $F(A)=A$ i $F^{-1}(u,v)=\big(\sqrt[3]{u^2/v},\ \sqrt[3]{v^2/u}\big)$. Llavors $F^{-1}(4.1,1.9)=\big(\sqrt[3]{16.81/1.9},\sqrt[3]{3.61/4.1}\big)\approx(2.0683,\ 0.9585)$; l'aproximació $(2.0667,\ 0.9583)$ té errors d'ordre $2\cdot10^{-3}$ i $10^{-4}$, petits respecte de l'increment $\|(0.1,-0.1)\|\approx0.14$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [injectivitat] Injectivitat a A
     objectiu: Demostrar que $F|_A$ és injectiva.
     idea: A partir de $u=x^2y$ i $v=xy^2$, buscar combinacions (quocients de potències) que aïllin $x$ i $y$ per separat.
     detall: Si $(x,y)\in A$ i $F(x,y)=(u,v)$, llavors $u,v\neq0$ i $\frac{u^2}{v}=\frac{x^4y^2}{xy^2}=x^3$, $\frac{v^2}{u}=y^3$. Com que $t\mapsto t^3$ és injectiva a $\mathbb{R}$, $(u,v)$ determina $(x,y)$: $F|_A$ és injectiva.
  2. [inversa] Imatge i inversa explícita
     objectiu: Trobar $F(A)$ i l'expressió de $F^{-1}$.
     idea: Treure l'arrel cúbica real de les expressions anteriors i comprovar que, per a qualsevol $(u,v)$ amb $uv\neq0$, el punt obtingut és a $A$ i té imatge $(u,v)$.
     detall: $F^{-1}(u,v)=\big(\sqrt[3]{u^2/v},\sqrt[3]{v^2/u}\big)$. Per a tot $(u,v)\in A$ aquest punt és a $A$ i $x^2y=\sqrt[3]{u^4/v^2}\sqrt[3]{v^2/u}=\sqrt[3]{u^3}=u$, i anàlogament $xy^2=v$. Per tant $F(A)=A$ i $F|_A:A\to A$ és bijectiva.
  3. [comparar] Valor exacte i comparació  (teoria: T4.6, T3.8)
     objectiu: Calcular $F^{-1}(4.1,1.9)$ i comparar-lo amb l'aproximació de l'apartat (c).
     idea: Substituir a la fórmula; l'error de l'aproximació afí ha de ser petit comparat amb la mida de l'increment (és $o(\|y-q\|)$).
     detall: $F^{-1}(4.1,1.9)=\big(\sqrt[3]{8.8474},\sqrt[3]{0.8805}\big)\approx(2.0683,\ 0.9585)$. L'aproximació $(2.0667,\ 0.9583)$ difereix en $\approx1.6\cdot10^{-3}$ i $\approx1.3\cdot10^{-4}$, molt menys que $\|(0.1,-0.1)\|\approx0.14$: coherent amb que l'error de l'aproximació de primer ordre és $o(\|(0.1,-0.1)\|)$.
ERRORS COMUNS:
  - [arrel_parell] Escriu potències com $(u^2/v)^{1/3}$ pensant només en valors positius, o usa arrels quadrades, i perd els punts amb $u$ o $v$ negatius.
  - [imatge_no_justificada] Dona la fórmula de la inversa sense comprovar que tot punt de $A$ és imatge (no determina $F(A)$).
  - [injectiva_per_det] Argumenta la injectivitat a $A$ amb el fet que $\det JF\neq0$ a $A$.

TEORIA DEL CURS QUE FA SERVIR:
[T4.6] Exemple 6 (Tema 4) — Exemples d'ús del TFI
Exemples d'ús del teorema de la funció inversa.

1. Considerem la funció
$$\begin{aligned}f:\mathbb{R}^2&\longrightarrow\mathbb{R}^2\\ (x,y)&\longmapsto e^x\,(\cos y,\sin y).\end{aligned}$$
Fixem-nos que per la periodicitat d'ambdues components respecte $y$, $f$ és clarament no injectiva. Addicionalment, observem que les dues components de $f$ són les parts real i imaginària, respectivament, de la funció de variable complexa $e^z$, amb $z=x+i\,y$.

D'altra banda,
$$\det Jf(x,y)=\begin{vmatrix}e^x\cos y&-e^x\sin y\\ e^x\sin y&e^x\cos y\end{vmatrix}=e^{2x}\neq 0\qquad\forall(x,y)\in\mathbb{R}^2.$$
D'entrada, doncs, veiem que, malgrat que el determinant de la matriu jacobiana no s'anul·la mai, $f$ no té una inversa global.

Ara bé, pel teorema de la funció inversa, com que $f$ és de classe $C^\infty$, en qualsevol punt $(x_0,y_0)\in\mathbb{R}^2$ podrem definir localment una funció inversa que serà també de classe $C^\infty$. Ho veurem per a un cas concret, prenent $(x_0,y_0)=(0,\pi/3)$.

Un càlcul directe ens dona que $f(0,\pi/3)=(\frac12,\frac{\sqrt3}{2})$. Llavors, $f^{-1}$ existeix en un entorn de $(\frac12,\frac{\sqrt3}{2})$ i, a més,
$$Df^{-1}\big(\tfrac12,\tfrac{\sqrt3}{2}\big)=\big(Df(0,\pi/3)\big)^{-1}=\begin{pmatrix}\frac12&-\frac{\sqrt3}{2}\\ \frac{\sqrt3}{2}&\frac12\end{pmatrix}^{-1}=\begin{pmatrix}\frac12&\frac{\sqrt3}{2}\\ -\frac{\sqrt3}{2}&\frac12\end{pmatrix}.$$
Observem que en aquest cas també es pot calcular $f^{-1}$ explícitament i, per tant, fer el càlcul de la seva matriu jacobiana sense aplicar el TFI. En efecte, si ens plantegem el sistema
$$\begin{cases}e^x\cos y=u,\\ e^x\sin y=v,\end{cases}$$
podem expressar
$$\begin{cases}u^2+v^2=e^{2x},\\ \dfrac{v}{u}=\tan y;\end{cases}\qquad\Leftrightarrow\qquad\begin{cases}x=x(u,v)=\frac12\ln(u^2+v^2),\\ y=y(u,v)=\arctan v/u.\end{cases}$$
Lligat amb el fet que $f$ és periòdica (i, per tant, no injectiva en $y$), constatem que $y(u,v)$ ni tan sols és contínua per a $u=0$. Però localment, podem considerar la seva diferencial per a $u\neq 0$:
$$\begin{aligned}Df^{-1}\big(\tfrac12,\tfrac{\sqrt3}{2}\big)=\frac{\partial(x,y)}{\partial(u,v)}\big(\tfrac12,\tfrac{\sqrt3}{2}\big)&=\begin{pmatrix}\dfrac{u}{u^2+v^2}&\dfrac{v}{u^2+v^2}\\ \dfrac{-v/u^2}{1+v^2/u^2}&\dfrac{1/u}{1+v^2/u^2}\end{pmatrix}_{(\frac12,\frac{\sqrt3}{2})}\\ &=\begin{pmatrix}\dfrac{u}{u^2+v^2}&\dfrac{v}{u^2+v^2}\\ \dfrac{-v}{u^2+v^2}&\dfrac{u}{u^2+v^2}\end{pmatrix}_{(\frac12,\frac{\sqrt3}{2})}=\begin{pmatrix}\frac12&\frac{\sqrt3}{2}\\ -\frac{\sqrt3}{2}&\frac12\end{pmatrix}.\end{aligned}$$

2. Una aplicació rellevant del teorema de la funció inversa és el càlcul de solucions aproximades de sistemes no lineals. Suposem que volem resoldre $f(x)=y$ i que coneixem que $f(p)=q$ per a un valor $q$ proper a $y$. Si $f$ és diferenciable en un obert que contingui $p$, i $\det Df(p)\neq 0$, aleshores, $f^{-1}$ és diferenciable en un entorn de $q$, i
$$\lim_{y\to q}\frac{\|f^{-1}(y)-f^{-1}(q)-Df(p)^{-1}(y-q)\|}{\|y-q\|}=0.$$
Per tant, podem aproximar $f^{-1}(y)$ per $f^{-1}(q)+Df(p)^{-1}(y-q)$, és a dir,
$$x\approx p+Df(p)^{-1}(y-q),$$
que equival a trobar l'aproximació resolent el sistema
$$Df(p)\,(x-p)=y-q.$$
Apliquem-ho, per exemple, al sistema
$$\begin{cases}x_1^3x_2^2x_3+x_1^2x_2^3x_3^2+x_1&=3.1,\\ x_1^2x_2^3+x_2^3x_3^2+x_3&=2.9,\\ x_2^3x_3^3+x_1x_3+x_1&=3.2,\end{cases}$$
que podem escriure de manera abreujada com $f(x_1,x_2,x_3)=(3.1,2.9,3.2)=:y$. Observem que el sistema $f(x_1,x_2,x_3)=(3,3,3)=:q$ té la solució $p=(1,1,1)$, i que
$$Df(p)=\begin{pmatrix}6&5&3\\ 2&6&3\\ 2&3&4\end{pmatrix},\ \text{ amb }\det Df(p)=62\neq 0.$$
Per tant, una solució aproximada de $f(x_1,x_2,x_3)=y$ és $x^*$ tal que
$$\begin{pmatrix}6&5&3\\ 2&6&3\\ 2&3&4\end{pmatrix}\begin{pmatrix}x_1^*-1\\ x_2^*-1\\ x_3^*-1\end{pmatrix}=\begin{pmatrix}0.1\\ -0.1\\ 0.2\end{pmatrix};\ \text{ és a dir, }\ \begin{pmatrix}6&5&3\\ 2&6&3\\ 2&3&4\end{pmatrix}\begin{pmatrix}x_1^*\\ x_2^*\\ x_3^*\end{pmatrix}=\begin{pmatrix}14.1\\ 10.9\\ 9.2\end{pmatrix}.$$
La solució del sistema és $x^*\approx(1.0323,0.9290,1.0871)$. A partir d'aquest punt, podríem calcular una nova aproximació prenent $p=x^*$, $q=f(x^*)\approx(3.0740,2.8891,3.1846)$ i, igual que abans, $y=(3.1,2.9,3.2)$. Observem com $\|y-q\|$ s'ha reduït: de $\sqrt{0.1^2+0.1^2+0.2^2}=\sqrt{0.06}\approx 0.2449$, hem passat a $\sqrt{(3.1-3.0740)^2+(2.9-2.8891)^2+(3.2-3.1846)^2}\approx 0.0321$.

A https://atenea.upc.edu/mod/resource/view.php?id=5449143 podeu trobar els càlculs de dos iterats més d'aquesta aproximació a la solució del sistema $f(x_1,x_2,x_3)=(3.1,2.9,3.2)$,

[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$
</solucio_de_referencia>

### Document a revisar

[1] De l'apartat (a) sabem que $\det JF(x,y)=3x^2y^2\neq 0$ a tot $A$, de manera que $F|_A$ és injectiva. Tot i així, ho comprovem directament, perquè així obtenim la inversa.
[2] Sigui $(x,y)\in A$ i $F(x,y)=(u,v)$, és a dir $u=x^2y$ i $v=xy^2$, tots dos no nuls. Aleshores $\frac{u^2}{v}=\frac{x^4y^2}{xy^2}=x^3$ i $\frac{v^2}{u}=\frac{x^2y^4}{x^2y}=y^3$.
[3] Com que $t\mapsto t^3$ és injectiva a $\mathbb{R}$ (amb inversa l'arrel cúbica real), $x=\sqrt[3]{u^2/v}$ i $y=\sqrt[3]{v^2/u}$ queden determinats per $(u,v)$, i $F|_A$ és injectiva.
[4] Recíprocament, per a $(u,v)\in A$ el punt $(x,y)=\big(\sqrt[3]{u^2/v},\sqrt[3]{v^2/u}\big)$ és de $A$ i $x^2y=\sqrt[3]{u^4/v^2}\,\sqrt[3]{v^2/u}=\sqrt[3]{u^3}=u$, $xy^2=\sqrt[3]{u^2/v}\,\sqrt[3]{v^4/u^2}=\sqrt[3]{v^3}=v$. Per tant $F(A)=A$ i $F^{-1}(u,v)=\big(\sqrt[3]{u^2/v},\sqrt[3]{v^2/u}\big)$.
[5] Avaluant, $F^{-1}(4.1,1.9)=\big(\sqrt[3]{16.81/1.9},\sqrt[3]{3.61/4.1}\big)=\big(\sqrt[3]{8.8474},\sqrt[3]{0.8805}\big)\approx(2.0683,\ 0.9585)$.
[6] L'aproximació lineal de l'apartat anterior era $(2.0667,\ 0.9583)$: les diferències són $\approx 1.6\cdot 10^{-2}$ i $\approx 1.3\cdot 10^{-4}$, molt més petites que l'increment $\|(0.1,-0.1)\|\approx 0.14$, coherent amb que l'error de l'aproximació de primer ordre és $o(\|(0.1,-0.1)\|)$.


## t4-9a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Demostreu que les funcions següents són difeomorfismes locals de classe $\mathcal{C}^\infty$ en tot punt del domini indicat. Doneu oberts màxims dins d'aquests dominis on les seves restriccions siguin difeomorfismes:

(a) $F(r,\varphi)=(r\cos\varphi,r\sin\varphi)$, $(r,\varphi)\in(0,\infty)\times\mathbb{R}$ *(polars)*;
(Indicació: $F:(0,\infty)\times(0,2\pi)\to\mathbb{R}^2\setminus\{(x,y)\mid y=0,\ x\geqslant 0\}$ té inversa i $F^{-1}$ no es pot estendre amb continuïtat a cap obert que contingui estrictament $\mathbb{R}^2\setminus\{(x,y)\mid y=0,\ x>0\}$.)
RESULTAT CORRECTE: $F$ és de classe $\mathcal{C}^\infty$ i $\det JF(r,\varphi)=r>0$ en tot el domini; pel teorema de la funció inversa, $F$ és un difeomorfisme local de classe $\mathcal{C}^\infty$ en tot punt. Oberts màxims: per a cada $\alpha\in\mathbb{R}$, $U_\alpha=(0,\infty)\times(\alpha,\alpha+2\pi)$; $F:U_\alpha\to\mathbb{R}^2\setminus\{(t\cos\alpha,t\sin\alpha)\mid t\geq 0\}$ és un difeomorfisme, i cap obert del domini que contingui estrictament $U_\alpha$ fa $F$ injectiva.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [jacobiana] Regularitat i jacobiana  (teoria: T3.31)
     objectiu: Comprovar la regularitat de $F$ i estudiar on s'anul·la el determinant de la seva jacobiana.
     idea: Les components són productes de funcions $\mathcal{C}^\infty$. Calculeu $\det JF$ i mireu-ne el signe al domini.
     detall: $JF(r,\varphi)=\begin{pmatrix}\cos\varphi&-r\sin\varphi\\ \sin\varphi&r\cos\varphi\end{pmatrix}$, $\det JF(r,\varphi)=r\cos^2\varphi+r\sin^2\varphi=r>0$ per a tot $(r,\varphi)\in(0,\infty)\times\mathbb{R}$.
  2. [difeo_local] Difeomorfisme local  (teoria: T4.5, T4.9)
     objectiu: Deduir que $F$ és un difeomorfisme local de classe $\mathcal{C}^\infty$ en tot punt.
     idea: Aplicar el teorema de la funció inversa en cada punt del domini, per a qualsevol classe $\mathcal{C}^k$, $k\geq 1$.
     detall: Per a cada $p$ del domini, $F$ és $\mathcal{C}^\infty$ i $\det JF(p)\neq 0$; el teorema de la funció inversa dona un entorn obert $U_p$ tal que $F|_{U_p}:U_p\to F(U_p)$ és bijectiva, $F(U_p)$ és obert i la inversa és $\mathcal{C}^k$ per a tot $k$, és a dir $\mathcal{C}^\infty$. Així $F$ és un difeomorfisme local $\mathcal{C}^\infty$ en tot punt.
  3. [injectivitat] Quan dos punts tenen la mateixa imatge
     objectiu: Caracteritzar quan $F(r,\varphi)=F(r',\varphi')$.
     idea: Compareu primer les normes de les imatges i després les direccions.
     detall: Si $F(r,\varphi)=F(r',\varphi')$, prenent normes $r=r'$, i aleshores $(\cos\varphi,\sin\varphi)=(\cos\varphi',\sin\varphi')$, que equival a $\varphi-\varphi'\in 2\pi\mathbb{Z}$. Per tant $F$ no és injectiva al domini sencer: $F(r,\varphi+2\pi)=F(r,\varphi)$.
  4. [oberts_maxims] Oberts màxims  (teoria: T4.9)
     objectiu: Trobar oberts del domini on la restricció de $F$ sigui un difeomorfisme i que no es puguin ampliar.
     idea: Pel pas anterior, la restricció és injectiva si i només si l'obert no conté dos punts amb el mateix $r$ i angles que difereixin en un múltiple de $2\pi$. Injectivitat més jacobiana invertible a tot arreu dona difeomorfisme sobre la imatge.
     detall: Sigui $U_\alpha=(0,\infty)\times(\alpha,\alpha+2\pi)$. Dos angles d'aquest interval difereixen en menys de $2\pi$, per tant $F|_{U_\alpha}$ és injectiva; és $\mathcal{C}^\infty$ amb $\det JF\neq 0$, així que és un difeomorfisme sobre la seva imatge $F(U_\alpha)=\mathbb{R}^2\setminus\{(t\cos\alpha,t\sin\alpha)\mid t\geq 0\}$ (el pla menys la semirecta tancada d'angle $\alpha$). Maximalitat: sigui $W\supsetneq U_\alpha$ un obert del domini i $(r_0,\varphi_0)\in W\setminus U_\alpha$. Si $\varphi_0\not\equiv\alpha\pmod{2\pi}$, hi ha un únic $\varphi_1\in(\alpha,\alpha+2\pi)$ amb $\varphi_1\equiv\varphi_0$, i $\varphi_1\neq\varphi_0$ (perquè $\varphi_0\notin(\alpha,\alpha+2\pi)$): els punts $(r_0,\varphi_0)\in W$ i $(r_0,\varphi_1)\in U_\alpha\subseteq W$ són diferents i tenen la mateixa imatge. Si $\varphi_0=\alpha+2k\pi$ amb $k\in\mathbb{Z}$, com que $W$ és obert conté $(r_0,\varphi_0\pm\varepsilon)$ per a $\varepsilon\in(0,2\pi)$ petit; si $k\leq 0$, $\varphi_0-\varepsilon<\alpha$, i si $k\geq 1$, $\varphi_0+\varepsilon>\alpha+2\pi$, així que un d'aquests dos punts és de $W\setminus U_\alpha$ amb angle no congruent amb $\alpha$, i som al cas anterior. En tots els casos $F|_W$ no és injectiva. Per $\alpha=0$ és el cas de la indicació.
ERRORS COMUNS:
  - [global_per_jacobiana] Creu que, com que $\det JF\neq 0$ a tot el domini, $F$ és un difeomorfisme de tot el domini.
  - [interval_no_obert] Proposa $(0,\infty)\times[0,2\pi)$, que fa $F$ bijectiva sobre $\mathbb{R}^2\setminus\{0\}$ però no és obert.
  - [unicitat_maxim] Pensa que l'obert màxim és únic.

TEORIA DEL CURS QUE FA SERVIR:
[T4.9] Definició 9 (Tema 4) — Homeomorfisme i difeomorfisme
1. Una funció $f:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$ és un homeomorfisme si $f$ és bijectiva, contínua i la seva inversa $f^{-1}$ també és contínua.

2. Una funció $f:U\longrightarrow V$ entre dos oberts $U,V$ de $\mathbb{R}^n$ és un difeomorfisme (o una transformació regular) de classe $C^r$, amb $r\geq 1$, si $f$ és bijectiva, de classe $C^r$ i la seva inversa $f^{-1}$ també és de classe $C^r$.

Els homeomorfisme preserven la forma topològica, mentre que els difeomorfisme també preserven l'estructura diferenciable.

[Resum 91'] Una definició alternativa de difeomorfisme és: Una funció $f:U\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$, amb $U$ obert de $\mathbb{R}^n$, és un difeomorfisme si $f\in\mathcal{C}^1(U)$, $f$ és injectiva, i $\det\big(Jf(x)\big)\neq 0$ per a tot $x\in U$.

[T3.31] Definició 31 (Tema 3) — Classes C^r de funcions
Direm que $f\in\mathcal{C}^0(\Omega)\Leftrightarrow f$ és contínua a $\Omega$.

$f\in\mathcal{C}^1(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ a tot punt de $\Omega$ i totes són contínues (per tant, en particular, $f$ és diferenciable i contínua).

$f\in\mathcal{C}^2(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ d'ordre $2$:
$$\frac{\partial^2f}{\partial x_i\partial x_j}=\frac{\partial}{\partial x_j}\left(\frac{\partial f}{\partial x_i}\right),$$
a tot punt de $\Omega$ i són contínues.

En general, per a $r\geq1$, es diu que $f\in\mathcal{C}^r(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials d'ordre $r$ a $\Omega$ i totes són contínues. Clarament, $f\in\mathcal{C}^{r+1}(\Omega)\Rightarrow f\in\mathcal{C}^r(\Omega)$.

Direm que $f\in\mathcal{C}^\infty(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials a qualsevol ordre de $f$ a $\Omega$ i totes són contínues.

[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.

[T4.11] Exemple 11 (Tema 4) — Canvis de variables
(Canvis de variables). Exemples de difeomorfismes.

Sovint ens trobem els difeomorfismes en el context de canvis de variables. En repassarem els més habituals.

1. Coordenades polars. Considerem $f:\Omega\subset\mathbb{R}^2\longrightarrow\mathbb{R}^2$, amb $\Omega=\{(r,\theta)\in\mathbb{R}^2\mid r>0,\ \theta\in(0,2\pi)\}$, tal que $f(r,\theta)=(r\cos\theta,r\sin\theta)$. Fixem-nos en la tria del domini $\Omega$, que no comprèn l'origen ni les "rectes" $\{\theta=0\}$ i $\{\theta=2\pi\}$.

La funció $f$ és injectiva i de classe $\mathcal{C}^\infty$. A més,
$$\det Jf(r,\theta)=\begin{vmatrix}\cos\theta&-r\sin\theta\\ \sin\theta&r\cos\theta\end{vmatrix}=r\neq 0\ \text{ en }\Omega.$$
Per tant, és un difeomorfisme. Una manera d'expressar (parcialment) la seva funció inversa és
$$\begin{aligned}f^{-1}:V\subset\mathbb{R}^2&\longrightarrow\mathbb{R}^2\\ (x,y)&\longmapsto\Big(\sqrt{x^2+y^2},\arccos\frac{x}{\sqrt{x^2+y^2}}\Big).\end{aligned}$$
Fixem-nos que, amb aquesta elecció, el domini de $f^{-1}$ és $V=\{(x,y)\in\mathbb{R}^2:\ y\geq 0\}\setminus\{(0,0)\}$. En canvi, la imatge de $\Omega$ per $f$ és el conjunt $W=\mathbb{R}^2\setminus\{(x,0),\ x\geq 0\}$. A més, com a inversa tenim diverses opcions, com ara $\arctan(y/x)$ o $\arcsin(y/\sqrt{x^2+y^2})$, els dominis de les quals tampoc coincideixen amb $V$. Podríem dir que la inversa existeix en el domini $V$, però cap de les funcions inverses proposades es pot aplicar en tot el domini.

Finalment, observem que si consideréssim $\Omega=\{(r,\theta)\in\mathbb{R}^2\mid r>0,\ \theta\in[0,2\pi)\}$, aleshores el conjunt imatge seria $W=\mathbb{R}^2\setminus\{(0,0)\}$, però el domini no seria obert en $\mathbb{R}^2$.

Aquesta discordància entre dominis i l'arbitrarietat en considerar funcions inverses desapareix si ens mirem les funcions com a funcions de variable complexa, però això va més enllà dels objectius d'aquesta assignatura.

2. Coordenades cilíndriques. Considerem $f:U\subset\mathbb{R}^3\longrightarrow V\subset\mathbb{R}^3$, definida com $f(r,\theta,z)=(r\cos\theta,r\sin\theta,z)$, amb $U=\{(r,\theta,z)\in\mathbb{R}^3\mid r>0,\ \theta\in(0,2\pi),\ z\in\mathbb{R}\}$ i $V=\mathbb{R}^3\setminus\{(x,0,z)\in\mathbb{R}^3\mid x\geq 0\}$.

Observem que el determinant de la matriu jacobiana tampoc s'anul·la en $U$:
$$|Jf(r,\theta)|=\begin{vmatrix}\cos\theta&-r\sin\theta&0\\ \sin\theta&r\cos\theta&0\\ 0&0&1\end{vmatrix}=r\neq 0.$$
En aquest cas, el conjunt imatge és
$$V=\mathbb{R}^3\setminus\{(x,y,z):x\geq 0,\ y=0\}.$$

3. Coordenades esfèriques. Considerem $f:U\subset\mathbb{R}^3\longrightarrow V\subset\mathbb{R}^3$, definida com $f(r,\theta,\varphi)=(r\sin\varphi\cos\theta,r\sin\varphi\sin\theta,r\cos\varphi)$, amb $U=\{(r,\theta,\varphi)\in\mathbb{R}^3\mid r>0,\ \theta\in(0,2\pi),\ \varphi\in(0,\pi)\}$ i $V=\mathbb{R}^3\setminus\big(\{(x,0,z)\in\mathbb{R}^3\mid x\geq 0\}\cup\{z=\pm1\}\big)$.

Les variables $\theta$ i $\varphi$ representen, en coordenades geogràfiques, la longitud i la colatitud, respectivament.

Observem que el determinant de la matriu jacobiana tampoc s'anul·la en $U$:
$$|Jf(r,\theta)|=\begin{vmatrix}\sin\varphi\cos\theta&-r\sin\theta\sin\varphi&r\cos\varphi\cos\theta\\ \sin\varphi\sin\theta&r\cos\theta\sin\varphi&r\cos\varphi\sin\theta\\ \cos\varphi&0&-r\sin\varphi\end{vmatrix}=-r^2\sin\varphi\neq 0.$$
</solucio_de_referencia>

### Document a revisar

[1] $F$ té components de classe $\mathcal{C}^\infty$ i $JF(r,\varphi)=\begin{pmatrix}\cos\varphi&-r\sin\varphi\\ \sin\varphi&r\cos\varphi\end{pmatrix}$, amb $\det JF(r,\varphi)=r\cos^2\varphi+r\sin^2\varphi=r>0$ a tot el domini $(0,\infty)\times\mathbb{R}$.
[2] Pel teorema de la funció inversa, per a cada punt $p$ del domini hi ha un entorn obert $U_p$ tal que $F|_{U_p}:U_p\to F(U_p)$ és bijectiva, $F(U_p)$ és obert i la inversa és de classe $\mathcal{C}^k$ per a tot $k$, és a dir $\mathcal{C}^\infty$. Així $F$ és un difeomorfisme local $\mathcal{C}^\infty$ en tot punt.
[3] $F$ no és injectiva al domini sencer: si $F(r,\varphi)=F(r',\varphi')$, prenent normes $r=r'$ i llavors $(\cos\varphi,\sin\varphi)=(\cos\varphi',\sin\varphi')$, que equival a $\varphi-\varphi'\in 2\pi\mathbb{Z}$; per exemple, $F(r,\varphi+2\pi)=F(r,\varphi)$.
[4] Per a cada $\alpha\in\mathbb{R}$, sigui $U_\alpha=(0,\infty)\times(\alpha,\alpha+2\pi)$. Dos angles d'aquest interval difereixen en menys de $2\pi$, així que $F|_{U_\alpha}$ és injectiva i, com que és $\mathcal{C}^\infty$ amb $\det JF\neq 0$, és un difeomorfisme sobre la seva imatge.
[5] La imatge és $F(U_\alpha)=\mathbb{R}^2\setminus\{(t\cos\alpha,t\sin\alpha)\mid t>0\}$, és a dir, el pla menys la semirecta oberta d'angle $\alpha$.
[6] Maximalitat: sigui $W\supsetneq U_\alpha$ un obert del domini i $(r_0,\varphi_0)\in W\setminus U_\alpha$. Si $\varphi_0\not\equiv\alpha\pmod{2\pi}$, hi ha un únic $\varphi_1\in(\alpha,\alpha+2\pi)$ amb $\varphi_1\equiv\varphi_0$, i $\varphi_1\neq\varphi_0$ perquè $\varphi_0\notin(\alpha,\alpha+2\pi)$; els punts $(r_0,\varphi_0)$ i $(r_0,\varphi_1)$ són de $W$, són diferents i tenen la mateixa imatge.
[7] Si $\varphi_0\equiv\alpha\pmod{2\pi}$, aleshores $F(r_0,\varphi_0)=(r_0\cos\alpha,r_0\sin\alpha)$ és de la semirecta que no és a $F(U_\alpha)$, i per tant $F|_W$ tampoc no és injectiva.
[8] En tots els casos $F|_W$ no és injectiva, de manera que cada $U_\alpha$ és un obert màxim on la restricció de $F$ és un difeomorfisme; per a $\alpha=0$ és el cas de la indicació. Hi ha, doncs, infinits oberts màxims (per exemple, tots els $U_\alpha$).


## t4-11a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Per cadascun dels següents oberts $U\subseteq\mathbb{R}^2$, estudieu si la funció $G:U\to G(U)$ definida per $G(x,y)=(x^2-y^2,2xy)$ és un canvi de variables (o difeomorfisme):

(a) $U=\mathbb{R}^2$;
RESULTAT CORRECTE: No és un difeomorfisme: $G(-x,-y)=G(x,y)$, així que no és injectiva; a més $\det JG(0,0)=0$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [jacobiana] Jacobiana
     objectiu: Estudiar on la diferencial de $G$ és invertible.
     idea: Calculeu $\det JG(x,y)$ i mireu on s'anul·la.
     detall: $JG(x,y)=\begin{pmatrix}2x&-2y\\ 2y&2x\end{pmatrix}$, $\det JG(x,y)=4(x^2+y^2)$, que només s'anul·la a l'origen.
  2. [injectivitat] Injectivitat
     objectiu: Decidir si $G$ és injectiva a $\mathbb{R}^2$.
     idea: Busqueu una simetria de $G$: quines transformacions del punt deixen $x^2-y^2$ i $2xy$ invariants?
     detall: $G(-x,-y)=G(x,y)$ i $(x,y)\neq(-x,-y)$ si $(x,y)\neq(0,0)$; per exemple $G(1,0)=G(-1,0)=(1,0)$. No és injectiva.
  3. [concloure] Conclusió  (teoria: T4.9)
     objectiu: Decidir si $G:\mathbb{R}^2\to G(\mathbb{R}^2)$ és un canvi de variables.
     idea: Un difeomorfisme ha de ser bijectiu i amb inversa diferenciable.
     detall: Com que no és injectiva, no és un difeomorfisme. A més, a l'origen $\det JG(0,0)=0$, per tant cap inversa local podria ser diferenciable en $G(0,0)=(0,0)$.
ERRORS COMUNS:
  - [oblida_origen] No s'adona que la jacobiana s'anul·la a l'origen.
  - [jacobiana_suficient] Pensa que si $\det JG\neq 0$ a gairebé tot arreu, $G$ és un difeomorfisme.

TEORIA DEL CURS QUE FA SERVIR:
[T4.9] Definició 9 (Tema 4) — Homeomorfisme i difeomorfisme
1. Una funció $f:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$ és un homeomorfisme si $f$ és bijectiva, contínua i la seva inversa $f^{-1}$ també és contínua.

2. Una funció $f:U\longrightarrow V$ entre dos oberts $U,V$ de $\mathbb{R}^n$ és un difeomorfisme (o una transformació regular) de classe $C^r$, amb $r\geq 1$, si $f$ és bijectiva, de classe $C^r$ i la seva inversa $f^{-1}$ també és de classe $C^r$.

Els homeomorfisme preserven la forma topològica, mentre que els difeomorfisme també preserven l'estructura diferenciable.

[Resum 91'] Una definició alternativa de difeomorfisme és: Una funció $f:U\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$, amb $U$ obert de $\mathbb{R}^n$, és un difeomorfisme si $f\in\mathcal{C}^1(U)$, $f$ és injectiva, i $\det\big(Jf(x)\big)\neq 0$ per a tot $x\in U$.
</solucio_de_referencia>

### Document a revisar

[1] $G(x,y)=(x^2-y^2,2xy)$ té components polinòmiques, per tant és de classe $\mathcal{C}^\infty$ a $U=\mathbb{R}^2$.
[2] La jacobiana és $JG(x,y)=\begin{pmatrix}2x&-2y\\ 2y&2x\end{pmatrix}$, amb $\det JG(x,y)=4x^2+4y^2=4(x^2+y^2)$, que només s'anul·la a l'origen.
[3] Per tant, a cada punt de $\mathbb{R}^2\setminus\{(0,0)\}$ el teorema de la funció inversa dona una inversa local, però això no diu res sobre la injectivitat global de $G$.
[4] De fet, $G(-x,-y)=\big((-x)^2-(-y)^2,2(-x)(-y)\big)=G(x,y)$, i $(-x,-y)\neq(x,y)$ si $(x,y)\neq(0,0)$; per exemple, $G(1,0)=G(0,1)=(1,0)$. Així $G$ no és injectiva a $U$.
[5] A més, $\det JG(0,0)=0$ i, pel teorema de la funció inversa, això implica que $G$ no és injectiva en cap entorn de l'origen.
[6] Com que $G$ no és injectiva, $G:U\to G(U)$ no és bijectiva i, per tant, no és un canvi de variables (difeomorfisme).


## t4-12a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Comproveu quines hipòtesis i quines tesis del teorema de la funció inversa satisfà $f(x)=x^3$.
RESULTAT CORRECTE: $f$ és $\mathcal{C}^\infty$. En punts $a\neq 0$, $f'(a)=3a^2\neq 0$: es compleixen totes les hipòtesis i totes les tesis. En $a=0$ falla la hipòtesi $f'(0)\neq 0$. Tesis en $0$: (i) injectivitat — sí ($f$ és estrictament creixent, bijectiva $\mathbb{R}\to\mathbb{R}$), però $f'(z)\neq 0$ a tot l'entorn — no ($f'(0)=0$); (ii) $f(U)$ obert — sí; (iii) la inversa $f^{-1}(y)=\sqrt[3]{y}$ és contínua però no és derivable en $0$, per tant no és $\mathcal{C}^1$ (ni la fórmula de la derivada té sentit).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [hipotesis] Hipòtesis  (teoria: T4.5, T4.2)
     objectiu: Comprovar quines hipòtesis del teorema de la funció inversa compleix $f$, i en quins punts.
     idea: Les hipòtesis són regularitat $\mathcal{C}^r$ en un obert i jacobiana (aquí, derivada) no nul·la en el punt.
     detall: $f$ és polinòmica, $\mathcal{C}^\infty(\mathbb{R})$. $f'(a)=3a^2$, no nul si $a\neq 0$; en $a=0$, $f'(0)=0$ i la hipòtesi falla. En $a\neq 0$ el teorema s'aplica i dona totes les tesis, així que l'interès és el punt $0$.
  2. [tesis_i_ii] Injectivitat i obertura
     objectiu: Estudiar en $0$ les tesis (i) i (ii): injectivitat local, derivada no nul·la a l'entorn i imatge oberta.
     idea: Penseu en la monotonia de $x^3$ i en la imatge d'un interval obert per una funció contínua estrictament monòtona.
     detall: $f$ és estrictament creixent a $\mathbb{R}$, per tant injectiva en qualsevol entorn de $0$, i porta $(-\delta,\delta)$ a $(-\delta^3,\delta^3)$, obert. Però la segona part de (i), $f'(z)\neq 0$ per a tot $z$ de l'entorn, falla perquè $f'(0)=0$.
  3. [tesi_iii] Regularitat de la inversa  (teoria: T3.8)
     objectiu: Estudiar en $f(0)=0$ la tesi (iii): diferenciabilitat (i classe $\mathcal{C}^r$) de la inversa.
     idea: Escriviu la inversa explícitament i estudieu el quocient incremental en $0$.
     detall: $f^{-1}(y)=\sqrt[3]{y}=y^{1/3}$, contínua. En $0$: $\frac{f^{-1}(h)-f^{-1}(0)}{h}=h^{-2/3}\to+\infty$, de manera que $f^{-1}$ no és derivable en $0$. Falla la tesi (iii), coherent amb que la fórmula $(f^{-1})'(0)=1/f'(0)$ no té sentit.
ERRORS COMUNS:
  - [no_invertible] Creu que, com que $f'(0)=0$, $f$ no és invertible a prop de $0$.
  - [inversa_regular] Pensa que la inversa d'una funció $\mathcal{C}^\infty$ bijectiva és automàticament diferenciable.
  - [oblida_punts_no_nuls] Només estudia el punt $0$ i no diu res dels altres punts.

TEORIA DEL CURS QUE FA SERVIR:
[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.

[T4.2] Proposició 2 (Tema 4) — Inversió local (una variable)
(inversió local). Sigui $f:(a,b)\to\mathbb{R}$ una funció $\mathcal{C}^r$, $r\geqslant 1$. Si $f'(c)\neq 0$ per a un determinat $c\in(a,b)$, llavors existeixen $\varepsilon_1,\varepsilon_2,\delta>0$ tals que $f:(c-\delta,c+\delta)\to(f(c)-\varepsilon_1,f(c)+\varepsilon_2)$ és bijectiva i $f'(x)\neq 0$ $\forall x\in(c-\delta,c+\delta)$. A més, la inversa local també és $\mathcal{C}^r$.

[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$
</solucio_de_referencia>

### Document a revisar

[1] Hipòtesis: $f(x)=x^3$ és polinòmica, per tant de classe $\mathcal{C}^\infty(\mathbb{R})$, i $f'(a)=3a^2$, que és no nul si i només si $a\neq 0$.
[2] En un punt $a\neq 0$ es compleixen totes les hipòtesis i el teorema dona totes les tesis: hi ha entorns oberts $U\ni a$ i $V\ni f(a)$ amb $f|_U:U\to V$ bijectiva i inversa de classe $\mathcal{C}^\infty$, amb $(f^{-1})'(f(a))=\frac{1}{3a^2}$. L'interès és, doncs, el punt $a=0$, on falla la hipòtesi $f'(0)\neq 0$.
[3] Tesi (i) en $0$: com que $f'(x)=3x^2>0$ per a tot $x\in\mathbb{R}$, $f$ és estrictament creixent, i per tant injectiva en qualsevol entorn de $0$.
[4] En canvi, la segona part de (i), que $f'(z)\neq 0$ per a tot $z$ de l'entorn, falla, perquè $f'(0)=0$.
[5] Tesi (ii): $f$ porta $(-\delta,\delta)$ a $(-\delta^3,\delta^3)$, que és obert.
[6] Tesi (iii): la inversa és $f^{-1}(y)=\sqrt[3]{y}$, que és contínua. En $0$, $\frac{f^{-1}(h)-f^{-1}(0)}{h}=\frac{\sqrt[3]{h}}{h}$, és a dir $h^{-1/3}$, que no té límit finit quan $h\to 0$; per tant $f^{-1}$ no és derivable en $0$.
[7] Així, en $0$ es compleixen la injectivitat de (i) i la tesi (ii), però falla (iii): $f^{-1}$ no és de classe $\mathcal{C}^1$ en cap entorn de $0$, coherent amb que la fórmula $(f^{-1})'(0)=\frac{1}{f'(0)}$ no té sentit.


## t4-13a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $I\subseteq\mathbb{R}$ un interval obert. Demostreu que tota funció $g:I\to\mathbb{R}$ de classe $\mathcal{C}^1$ tal que $g'(x)\neq 0$ per tot $x\in I$ té inversa global de classe $\mathcal{C}^1$ en $g(I)$.
RESULTAT CORRECTE: $g'$ és contínua i no s'anul·la a l'interval $I$, per tant té signe constant; pel teorema del valor mitjà $g$ és estrictament monòtona, per tant injectiva, i $g:I\to g(I)$ és bijectiva, amb $g(I)$ un interval obert. En cada $y_0=g(x_0)$ la inversa local (teorema de la funció inversa) coincideix amb $g^{-1}$, que per tant és derivable amb $(g^{-1})'(y)=\frac{1}{g'(g^{-1}(y))}$, contínua: $g^{-1}\in\mathcal{C}^1(g(I))$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [signe_constant] Signe constant de la derivada  (teoria: T2.21, T1.35)
     objectiu: Veure que $g'$ no canvia de signe a $I$.
     idea: $g'$ és contínua; useu que la imatge contínua d'un connex és connexa (o el teorema de Bolzano).
     detall: $I$ és un interval, per tant connex, i $g'$ és contínua, així que $g'(I)$ és un connex de $\mathbb{R}$ (un interval) que no conté el $0$. Per tant $g'(I)\subseteq(0,\infty)$ o $g'(I)\subseteq(-\infty,0)$.
  2. [injectivitat] Monotonia estricta i injectivitat  (teoria: T3.26)
     objectiu: Provar que $g$ és injectiva a $I$.
     idea: Compareu $g(x_1)$ i $g(x_2)$ amb el teorema del valor mitjà.
     detall: Per $x_1<x_2$ de $I$, $[x_1,x_2]\subseteq I$ i existeix $\xi\in[x_1,x_2]$ amb $g(x_2)-g(x_1)=g'(\xi)(x_2-x_1)$, que té el signe (constant, no nul) de $g'$. Per tant $g$ és estrictament monòtona i injectiva, i $g:I\to g(I)$ és bijectiva.
  3. [imatge_oberta] La imatge és un interval obert  (teoria: T2.21, T4.8)
     objectiu: Descriure el conjunt $g(I)$ on ha d'estar definida la inversa.
     idea: Connexió per veure que és un interval; per veure que és obert, useu el teorema de l'aplicació oberta o la monotonia estricta.
     detall: $g(I)$ és connex (imatge contínua de connex), per tant un interval. És obert pel teorema de l'aplicació oberta ($g\in\mathcal{C}^1$, $g'\neq 0$ a tot $I$); alternativament, per monotonia estricta $g$ no assoleix ni màxim ni mínim a l'interval obert $I$.
  4. [inversa_c1] La inversa és de classe C^1  (teoria: T4.2, T4.5)
     objectiu: Provar que $g^{-1}:g(I)\to I$ és de classe $\mathcal{C}^1$.
     idea: Localment, el teorema de la funció inversa dona una inversa diferenciable; relacioneu-la amb la inversa global. Després estudieu la continuïtat de la derivada que s'obté.
     detall: Sigui $y_0=g(x_0)\in g(I)$. Com que $g'(x_0)\neq 0$, el teorema de la funció inversa (en una variable) dona entorns $U\ni x_0$, $V\ni y_0$ amb $g|_U:U\to V$ bijectiva i inversa $h$ de classe $\mathcal{C}^1$, amb $h'(y)=\frac{1}{g'(h(y))}$. Per injectivitat global, $h=g^{-1}|_V$. Per tant $g^{-1}$ és derivable a tot $g(I)$ amb $(g^{-1})'(y)=\frac{1}{g'(g^{-1}(y))}$, que és contínua (composició i quocient de contínues amb denominador no nul). Així $g^{-1}\in\mathcal{C}^1(g(I))$.
ERRORS COMUNS:
  - [local_per_global] Aplica el teorema de la funció inversa i conclou directament que hi ha inversa global, sense provar la injectivitat a tot $I$.
  - [sense_continuitat] Usa que $g'$ té signe constant sense justificar-ho (o oblida que cal la continuïtat de $g'$ i que $I$ sigui un interval).
  - [derivabilitat_inversa] Dedueix la fórmula de $(g^{-1})'$ derivant $g(g^{-1}(y))=y$ amb la regla de la cadena, suposant ja que $g^{-1}$ és derivable.

TEORIA DEL CURS QUE FA SERVIR:
[T3.20] Definició 20 (Tema 3) — Funció de classe C^1
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $\Omega$ obert. Direm que $f$ és de classe $\mathcal{C}^1(\Omega)$ si $f$ és diferenciable a $\Omega$ i, per a tot punt $a\in\Omega$, existeixen totes les derivades parcials de $f$ al punt $a$ i hi són contínues. De manera anàloga a definicions anteriors, direm que $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $f=(f_1,f_2,\ldots,f_m)$, és de classe $\mathcal{C}^1(\Omega)$ si $f_i\in\mathcal{C}^1(\Omega)$, per a tot $i=1,2,\ldots,m$.

[T2.21] Proposició 21 (Tema 2) — Imatge contínua de compactes i connexos
Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $f:\Omega\subseteq M\to N$ contínua i $K\subseteq\Omega$. Aleshores,

(i) $K$ compacte $\Rightarrow f(K)$ compacte;

(ii) $K$ connex $\Rightarrow f(K)$ connex.

[T1.35] Definició 35 (Tema 1) — Conjunt connex
Sigui $(M,d)$ espai mètric, i $A\subseteq M$. Direm que $A$ és _disconnex_ si existeixen dos oberts disjunts $U$ i $V$ tals que $A\subseteq U\cup V$ i $U\cap A\neq\varnothing$ i $V\cap A\neq\varnothing$ i $U\cap V\cap A=\varnothing$. En cas contrari direm que $A$ és un conjunt _connex_.

[T3.26] Corol·lari 26 (Tema 3) — Teorema del valor mitjà (cas m=1)
(Cas $m=1$). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciable en un obert $\Omega\subseteq\mathbb{R}^n$. Aleshores, $\forall a,b\in\Omega$ tal que $[a,b]\subseteq\Omega$ existeix un $\xi\in[a,b]$ tal que $f(b)-f(a)=\langle\nabla f(\xi),b-a\rangle$.

[T4.8] Corol·lari 8 (Tema 4) — Teorema de l'aplicació oberta
Teorema de l'aplicació oberta. Sigui $f:U\subseteq\mathbb{R}^n\to V\subseteq\mathbb{R}^n$ una funció $\mathcal{C}^1(U)$ tal que $\det Jf(a)\neq 0$ per a tot $a\in U$. Aleshores, per a tot obert $B\subseteq U$, $f(B)$ és també un obert.

[T4.2] Proposició 2 (Tema 4) — Inversió local (una variable)
(inversió local). Sigui $f:(a,b)\to\mathbb{R}$ una funció $\mathcal{C}^r$, $r\geqslant 1$. Si $f'(c)\neq 0$ per a un determinat $c\in(a,b)$, llavors existeixen $\varepsilon_1,\varepsilon_2,\delta>0$ tals que $f:(c-\delta,c+\delta)\to(f(c)-\varepsilon_1,f(c)+\varepsilon_2)$ és bijectiva i $f'(x)\neq 0$ $\forall x\in(c-\delta,c+\delta)$. A més, la inversa local també és $\mathcal{C}^r$.

[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.

[T4.1] Proposició 1 (Tema 4) — Inversió global (una variable)
(inversió global). Sigui $f:I=(a,b)\to\mathbb{R}$ una funció $\mathcal{C}^r$, $r\geqslant 1$, i tal que $f'(c)\neq 0$, $\forall c\in(a,b)$. Llavors $f:I\to f(I)$ és bijectiva, $f^{-1}:f(I)\to I$ també és $\mathcal{C}^r$. A més,
$$(f^{-1})'(y_0)=\frac{1}{f'(f^{-1}(y_0))},\qquad \text{per a } y_0\in f(I).$$
</solucio_de_referencia>

### Document a revisar

[1] Com que $g$ és de classe $\mathcal{C}^1$, $g'$ és contínua, i $I$ és un interval, per tant connex. Aleshores $g'(I)$ és un connex de $\mathbb{R}$, és a dir un interval, que no conté el $0$; per tant $g'>0$ a tot $I$ o bé $g'<0$ a tot $I$.
[2] Siguin $x_1<x_2$ de $I$. Com que $I$ és un interval, $[x_1,x_2]\subseteq I$, i pel teorema del valor mitjà existeix $\xi\in(x_1,x_2)$ amb $g(x_2)-g(x_1)=g'(\xi)(x_2-x_1)$, que té el signe (constant i no nul) de $g'$.
[3] Per tant $g$ és estrictament monòtona a $I$, i en particular injectiva; així $g:I\to\mathbb{R}$ és bijectiva i té inversa $g^{-1}:\mathbb{R}\to I$.
[4] La imatge $g(I)$ és connexa, per ser imatge contínua d'un connex, i per tant és un interval. A més, és oberta perquè $g$ és contínua i $I$ és obert.
[5] Sigui $y_0=g(x_0)\in g(I)$. Com que $g$ és $\mathcal{C}^1$ i $g'(x_0)\neq 0$, el teorema de la funció inversa dona entorns oberts $U\ni x_0$ i $V\ni y_0$ amb $g|_U:U\to V$ bijectiva i inversa $h:V\to U$ de classe $\mathcal{C}^1$, amb $h'(y)=\frac{1}{g'(h(y))}$.
[6] Per la injectivitat de $g$ a tot $I$, $h$ coincideix amb $g^{-1}$ a $V$. Per tant $g^{-1}$ és derivable a tot $g(I)$, amb $(g^{-1})'(y)=\frac{1}{g'(g^{-1}(y))}$.
[7] Aquesta derivada és contínua: $g^{-1}$ és contínua (localment coincideix amb $h$), $g'$ és contínua i el denominador no s'anul·la. Així $g^{-1}$ és una inversa global de $g$ de classe $\mathcal{C}^1$ a $g(I)$.


## t4-14a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $f:\mathbb{R}\to\mathbb{R}$ de classe $\mathcal{C}^1$ tal que existeix $k\in\mathbb{R}$ satisfent $|f'(x)|\leqslant k<1$ per a tot $x\in\mathbb{R}$. Considerem la funció $F:\mathbb{R}^2\to\mathbb{R}^2$ definida per $F(x,y)=(x+f(y),y+f(x))$.

(a) Demostreu que $F$ admet inversa global de classe $\mathcal{C}^1$.

Indicació: useu el teorema del valor mitjà.
RESULTAT CORRECTE: $F\in\mathcal{C}^1(\mathbb{R}^2)$ i $\det JF(x,y)=1-f'(x)f'(y)\geq 1-k^2>0$ a tot punt. $F$ és injectiva (pel teorema del valor mitjà, $|x-x'|\le k^2|x-x'|$ obliga $x=x'$, i llavors $y=y'$) i exhaustiva (per a $(u,v)$ donat, $x\mapsto u-f(v-f(x))$ és contractiva amb constant $k^2$ i té un punt fix). Per tant $F:\mathbb{R}^2\to\mathbb{R}^2$ és bijectiva, i pel teorema de la funció inversa aplicat a cada punt la inversa global coincideix localment amb una inversa $\mathcal{C}^1$: $F^{-1}\in\mathcal{C}^1(\mathbb{R}^2)$ ($F$ és un difeomorfisme $\mathcal{C}^1$ de $\mathbb{R}^2$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [jacobia] Determinant jacobià  (teoria: T3.10, T3.20)
     objectiu: Estudiar la regularitat de $F$ i el signe del seu determinant jacobià a tot punt de $\mathbb{R}^2$.
     idea: Calcular la matriu jacobiana de $F$ i fitar el determinant fent servir la hipòtesi sobre $|f'|$.
     detall: Les components de $F$ són sumes de funcions $\mathcal{C}^1$, així que $F\in\mathcal{C}^1(\mathbb{R}^2)$, i
$JF(x,y)=\begin{pmatrix}1 & f'(y)\\ f'(x) & 1\end{pmatrix}$, amb $\det JF(x,y)=1-f'(x)f'(y)\geq 1-|f'(x)|\,|f'(y)|\geq 1-k^2>0$.
  2. [injectivitat] Injectivitat global  (teoria: T3.26)
     objectiu: Demostrar que $F$ és injectiva a tot $\mathbb{R}^2$.
     idea: Suposar $F(x,y)=F(x',y')$ i fitar les diferències de coordenades aplicant el teorema del valor mitjà a $f$ (una variable).
     detall: Si $F(x,y)=F(x',y')$, aleshores $x-x'=f(y')-f(y)$ i $y-y'=f(x')-f(x)$. Pel teorema del valor mitjà, $|f(s)-f(t)|\le k|s-t|$ per a tot $s,t$. Per tant
$|x-x'|\le k|y-y'|= k|f(x')-f(x)|\le k^2|x-x'|$. Com que $k^2<1$, $x=x'$, i aleshores $y-y'=f(x')-f(x)=0$.
  3. [exhaustivitat] Exhaustivitat  (teoria: T2.30, T2.31, T3.26)
     objectiu: Demostrar que tot $(u,v)\in\mathbb{R}^2$ té alguna antiimatge per $F$.
     idea: Reduir el sistema $F(x,y)=(u,v)$ a una sola equació en $x$ i justificar que té solució; el teorema del punt fix és una via natural.
     detall: $F(x,y)=(u,v)$ equival a $y=v-f(x)$ i $x=u-f(v-f(x))=:\varphi(x)$. Per la regla de la cadena, $|\varphi'(x)|=|f'(v-f(x))|\,|f'(x)|\le k^2<1$, i pel teorema del valor mitjà $\varphi$ és Lipschitz amb constant $k^2<1$ (si $k=0$, amb qualsevol constant de $(0,1)$), és a dir, contractiva a $\mathbb{R}$, que és complet. Pel teorema del punt fix existeix (un únic) $x^*$ amb $\varphi(x^*)=x^*$, i $(x^*,v-f(x^*))$ és antiimatge de $(u,v)$.
(Alternativa: $\psi(x)=x+f(v-f(x))-u$ té $\psi'\ge 1-k^2>0$, per tant $\psi(x)\to\pm\infty$ quan $x\to\pm\infty$ i, pel valor intermedi, s'anul·la.)
  4. [regularitat_inversa] La inversa global és $\mathcal{C}^1$  (teoria: T4.5, T4.9)
     objectiu: Deduir que la inversa global $F^{-1}:\mathbb{R}^2\to\mathbb{R}^2$ és de classe $\mathcal{C}^1$.
     idea: Combinar la bijectivitat global amb el teorema de la funció inversa aplicat a cada punt.
     detall: $F$ és bijectiva. Donat $(u_0,v_0)=F(a)$, com que $F\in\mathcal{C}^1$ i $\det JF(a)\neq 0$, el teorema de la funció inversa dona oberts $U\ni a$ i $V=F(U)\ni(u_0,v_0)$ i una inversa local $\mathcal{C}^1$ de $F|_U$ definida a $V$. Per la injectivitat global, aquesta inversa local és exactament la restricció de $F^{-1}$ a $V$. Per tant $F^{-1}$ és $\mathcal{C}^1$ en un entorn de cada punt, és a dir, $F^{-1}\in\mathcal{C}^1(\mathbb{R}^2)$: $F$ és un difeomorfisme $\mathcal{C}^1$ de $\mathbb{R}^2$ en $\mathbb{R}^2$.
ERRORS COMUNS:
  - [global_per_jacobia] Dedueix l'existència d'inversa global només del fet que $\det JF\neq 0$ a tot punt.
  - [oblida_exhaustivitat] Demostra la injectivitat però no comprova que $F$ sigui exhaustiva sobre $\mathbb{R}^2$ (inversa global vol dir definida a tot $\mathbb{R}^2$).
  - [fita_sense_k] Fa servir només $|f'|<1$ punt a punt en lloc de la fita uniforme $k<1$, i no pot concloure (per exemple, la contracció necessita una constant fixa menor que $1$).
  - [regularitat_sense_tfi] Un cop té la bijectivitat, afirma que la inversa és $\mathcal{C}^1$ sense cap argument.

TEORIA DEL CURS QUE FA SERVIR:
[T3.20] Definició 20 (Tema 3) — Funció de classe C^1
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $\Omega$ obert. Direm que $f$ és de classe $\mathcal{C}^1(\Omega)$ si $f$ és diferenciable a $\Omega$ i, per a tot punt $a\in\Omega$, existeixen totes les derivades parcials de $f$ al punt $a$ i hi són contínues. De manera anàloga a definicions anteriors, direm que $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $f=(f_1,f_2,\ldots,f_m)$, és de classe $\mathcal{C}^1(\Omega)$ si $f_i\in\mathcal{C}^1(\Omega)$, per a tot $i=1,2,\ldots,m$.

[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$

[T3.26] Corol·lari 26 (Tema 3) — Teorema del valor mitjà (cas m=1)
(Cas $m=1$). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciable en un obert $\Omega\subseteq\mathbb{R}^n$. Aleshores, $\forall a,b\in\Omega$ tal que $[a,b]\subseteq\Omega$ existeix un $\xi\in[a,b]$ tal que $f(b)-f(a)=\langle\nabla f(\xi),b-a\rangle$.

[T2.30] Definició 30 (Tema 2) — Funció contractiva
Una funció $f:\Omega\subseteq M\to N$ és contractiva si existeix $0<k<1$ t.q. $\forall x,y\in\Omega$, $d'(f(x),f(y))\leqslant k\,d(x,y)$ (és a dir, Lipschitz amb constant $<1$).

[T2.31] Teorema 31 (Tema 2) — Teorema del punt fix
(del punt fix). Sigui $(M,d)$ un espai mètric complet, i sigui $f:M\to M$ una funció contractiva. Aleshores:

(a) $f$ té un únic punt fix $x^*$ a $M$, és a dir, existeix un únic $x^*\in M$ tal que $f(x^*)=x^*$.

(b) Per a qualsevol punt inicial $x_0\in M$ (condició inicial), la successió definida per iteració $x_{n+1}=f(x_n)$ convergeix cap a $x^*$.

Aquest teorema és fonamental en anàlisi numèrica, equacions diferencials i optimització, ja que assegura la convergència de molts mètodes iteratius.

[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.

[T4.9] Definició 9 (Tema 4) — Homeomorfisme i difeomorfisme
1. Una funció $f:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$ és un homeomorfisme si $f$ és bijectiva, contínua i la seva inversa $f^{-1}$ també és contínua.

2. Una funció $f:U\longrightarrow V$ entre dos oberts $U,V$ de $\mathbb{R}^n$ és un difeomorfisme (o una transformació regular) de classe $C^r$, amb $r\geq 1$, si $f$ és bijectiva, de classe $C^r$ i la seva inversa $f^{-1}$ també és de classe $C^r$.

Els homeomorfisme preserven la forma topològica, mentre que els difeomorfisme també preserven l'estructura diferenciable.

[Resum 91'] Una definició alternativa de difeomorfisme és: Una funció $f:U\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$, amb $U$ obert de $\mathbb{R}^n$, és un difeomorfisme si $f\in\mathcal{C}^1(U)$, $f$ és injectiva, i $\det\big(Jf(x)\big)\neq 0$ per a tot $x\in U$.
</solucio_de_referencia>

### Document a revisar

[1] Les components $x+f(y)$ i $y+f(x)$ són sumes de funcions de classe $\mathcal{C}^1$, així que $F\in\mathcal{C}^1(\mathbb{R}^2)$, amb $JF(x,y)=\begin{pmatrix}1&f'(y)\\ f'(x)&1\end{pmatrix}$.
[2] El determinant és $\det JF(x,y)=1+f'(x)f'(y)\geq 1-|f'(x)|\,|f'(y)|\geq 1-k^2>0$, de manera que $JF$ és invertible a tot punt.
[3] Pel teorema del valor mitjà, per a tot $s,t\in\mathbb{R}$ hi ha $\xi$ entre $s$ i $t$ amb $f(s)-f(t)=f'(\xi)(s-t)$, i per tant $|f(s)-f(t)|\le k|s-t|$.
[4] Injectivitat: si $F(x,y)=F(x',y')$, aleshores $x-x'=f(y')-f(y)$ i $y-y'=f(x')-f(x)$. Llavors $|x-x'|\le k|y-y'|=k|f(x')-f(x)|\le k^2|x-x'|$, i com que $k^2<1$, $x=x'$; aleshores $y-y'=f(x')-f(x)=0$.
[5] Exhaustivitat: donat $(u,v)$, $F(x,y)=(u,v)$ equival a $y=v-f(x)$ i $x=u-f(v-f(x))=:\varphi(x)$. Per la regla de la cadena, $|\varphi'(x)|=|f'(v-f(x))|\,|f'(x)|<1$ per a tot $x$, i per tant $\varphi$ és contractiva a $\mathbb{R}$.
[6] Com que $\mathbb{R}$ és complet, pel teorema del punt fix existeix $x^*$ amb $\varphi(x^*)=x^*$, i $(x^*,v-f(x^*))$ és una antiimatge de $(u,v)$. Per tant $F:\mathbb{R}^2\to\mathbb{R}^2$ és bijectiva.
[7] Donat $(u_0,v_0)=F(a)$, com que $F\in\mathcal{C}^1$ i $\det JF(a)\neq 0$, el teorema de la funció inversa dona oberts $U\ni a$ i $V=F(U)\ni(u_0,v_0)$ i una inversa local de classe $\mathcal{C}^1$ de $F|_U$ definida a $V$. Per la injectivitat global, aquesta inversa local és la restricció de $F^{-1}$ a $V$.
[8] Per tant $F^{-1}$ és de classe $\mathcal{C}^1$ en un entorn de cada punt, és a dir $F^{-1}\in\mathcal{C}^1(\mathbb{R}^2)$: $F$ admet inversa global de classe $\mathcal{C}^1$.

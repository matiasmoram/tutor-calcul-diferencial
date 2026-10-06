## t4-15b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $f:\mathbb{R}\to\mathbb{R}$ de classe $\mathcal{C}^1$ i tal que $f'(x)\neq 0$, $\forall x\in\mathbb{R}$. Considerem $G:\mathbb{R}^2\to\mathbb{R}^2$ definida per
$$G(x,y)=(f(x),-y+xf(x)).$$

(b) Donat $(u_0,v_0)\in\mathrm{Im}\,G$, calculeu $DG^{-1}(u_0,v_0)$.
RESULTAT CORRECTE: Amb $x_0=f^{-1}(u_0)$ (l'únic $x$ amb $f(x)=u_0$):
$DG^{-1}(u_0,v_0)=\begin{pmatrix}\frac{1}{f'(x_0)}&0\\ x_0+\frac{u_0}{f'(x_0)}&-1\end{pmatrix}$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [antiimatge] Punt on avaluar la jacobiana  (teoria: T4.1)
     objectiu: Identificar el punt $(x_0,y_0)$ tal que $G(x_0,y_0)=(u_0,v_0)$.
     idea: La primera component de $G$ només depèn de $x$; fer servir que $f$ és injectiva perquè la seva derivada no s'anul·la.
     detall: $f'$ és contínua i no s'anul·la, per tant té signe constant i $f$ és estrictament monòtona: $f:\mathbb{R}\to f(\mathbb{R})$ és bijectiva. De $f(x_0)=u_0$ surt $x_0=f^{-1}(u_0)$, i de $-y_0+x_0f(x_0)=v_0$, $y_0=x_0u_0-v_0$.
  2. [jacobiana] Jacobiana al punt  (teoria: T3.10)
     objectiu: Calcular $JG(x_0,y_0)$, expressada en termes de $x_0$ i $u_0$.
     idea: Derivar les components de $G$ i substituir $f(x_0)=u_0$.
     detall: $JG(x_0,y_0)=\begin{pmatrix}f'(x_0)&0\\ u_0+x_0f'(x_0)&-1\end{pmatrix}$.
  3. [invertir] Diferencial de la inversa  (teoria: T4.5)
     objectiu: Obtenir $DG^{-1}(u_0,v_0)$.
     idea: Aplicar la fórmula de la diferencial de la inversa que dona el teorema de la funció inversa i invertir una matriu $2\times 2$.
     detall: $DG^{-1}(u_0,v_0)=\big(DG(x_0,y_0)\big)^{-1}=\frac{1}{-f'(x_0)}\begin{pmatrix}-1&0\\ -(u_0+x_0f'(x_0))&f'(x_0)\end{pmatrix}=\begin{pmatrix}\frac{1}{f'(x_0)}&0\\ x_0+\frac{u_0}{f'(x_0)}&-1\end{pmatrix}$.
ERRORS COMUNS:
  - [punt_equivocat] Avalua $JG$ al punt $(u_0,v_0)$ en lloc de l'antiimatge $(x_0,y_0)=G^{-1}(u_0,v_0)$.
  - [inversa_entrada_a_entrada] Inverteix la matriu prenent l'invers de cada entrada.
  - [no_identifica_x0] Deixa el resultat en termes d'un $x_0$ indeterminat, sense justificar que és únic i val $f^{-1}(u_0)$.

TEORIA DEL CURS QUE FA SERVIR:
[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.

[T4.1] Proposició 1 (Tema 4) — Inversió global (una variable)
(inversió global). Sigui $f:I=(a,b)\to\mathbb{R}$ una funció $\mathcal{C}^r$, $r\geqslant 1$, i tal que $f'(c)\neq 0$, $\forall c\in(a,b)$. Llavors $f:I\to f(I)$ és bijectiva, $f^{-1}:f(I)\to I$ també és $\mathcal{C}^r$. A més,
$$(f^{-1})'(y_0)=\frac{1}{f'(f^{-1}(y_0))},\qquad \text{per a } y_0\in f(I).$$

[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$
</solucio_de_referencia>

### Document a revisar

[1] Com que $f'$ és contínua i no s'anul·la enlloc, pel teorema de Bolzano té signe constant, i per tant $f$ és estrictament monòtona i injectiva. Així, donat $(u_0,v_0)\in\mathrm{Im}\,G$, hi ha un únic $x_0\in\mathbb{R}$ amb $f(x_0)=u_0$, és a dir, $x_0=f^{-1}(u_0)$.
[2] La segona component de $G(x_0,y_0)=(u_0,v_0)$ dona $-y_0+x_0f(x_0)=v_0$, és a dir, $-y_0+x_0u_0=v_0$, d'on $y_0=v_0-x_0u_0$. Per tant $(x_0,y_0)$ és l'única antiimatge de $(u_0,v_0)$, i $G$ és injectiva.
[3] $G$ és de classe $\mathcal{C}^1$ i la seva matriu jacobiana és $JG(x,y)=\begin{pmatrix}f'(x)&0\\ f(x)+xf'(x)&-1\end{pmatrix}$, amb $\det JG(x,y)=-f'(x)\neq0$ per a tot $(x,y)\in\mathbb{R}^2$.
[4] Pel teorema de la funció inversa, hi ha entorns oberts $U$ de $(x_0,y_0)$ i $V$ de $(u_0,v_0)$ tals que $G:U\to V$ és bijectiva amb inversa de classe $\mathcal{C}^1$; com que $G$ és injectiva, aquesta inversa coincideix amb $G^{-1}$ a $V$. Per tant $G^{-1}$ és diferenciable en $(u_0,v_0)$ i $DG^{-1}(u_0,v_0)=\big(DG(x_0,y_0)\big)^{-1}$.
[5] Al punt $(x_0,y_0)$, usant $f(x_0)=u_0$: $JG(x_0,y_0)=\begin{pmatrix}f'(x_0)&0\\ u_0+x_0f'(x_0)&-1\end{pmatrix}$, de determinant $-f'(x_0)$.
[6] Invertint la matriu $2\times2$: $\big(JG(x_0,y_0)\big)^{-1}=\frac{1}{-f'(x_0)}\begin{pmatrix}-1&0\\ u_0+x_0f'(x_0)&f'(x_0)\end{pmatrix}=\begin{pmatrix}\frac{1}{f'(x_0)}&0\\ -x_0-\frac{u_0}{f'(x_0)}&-1\end{pmatrix}$.
[7] Per tant, amb $x_0=f^{-1}(u_0)$, $DG^{-1}(u_0,v_0)=\begin{pmatrix}\frac{1}{f'(x_0)}&0\\ -x_0-\frac{u_0}{f'(x_0)}&-1\end{pmatrix}$.


## t4-17a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considereu el sistema
$$\left.\begin{aligned}x-2y-z&=0\\ x+yt&=0\end{aligned}\right\}$$

(a) Proveu que defineix implícitament funcions diferenciables $z=g_1(x,y)$ i $t=g_2(x,y)$ al voltant del punt $(1,1,-1,-1)$.
RESULTAT CORRECTE: Amb $\Phi(x,y,z,t)=(x-2y-z,\,x+yt)\in\mathcal{C}^\infty$, $\Phi(1,1,-1,-1)=(0,0)$ i $\det\frac{\partial\Phi}{\partial(z,t)}(1,1,-1,-1)=\det\begin{pmatrix}-1&0\\0&1\end{pmatrix}=-1\neq 0$. Pel teorema de la funció implícita existeixen $g_1,g_2$ de classe $\mathcal{C}^\infty$ en un entorn de $(1,1)$, amb $g_1(1,1)=-1$, $g_2(1,1)=-1$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [comprovar_punt] El punt és solució
     objectiu: Escriure el sistema com $\Phi=0$ i comprovar que el punt donat hi pertany.
     idea: Definir $\Phi:\mathbb{R}^4\to\mathbb{R}^2$ amb les dues equacions i avaluar-la al punt, respectant l'ordre $(x,y,z,t)$.
     detall: $\Phi(x,y,z,t)=(x-2y-z,\,x+yt)$; $\Phi(1,1,-1,-1)=(1-2+1,\,1-1)=(0,0)$.
  2. [menor] Menor respecte de $(z,t)$  (teoria: T3.10)
     objectiu: Comprovar la condició de no-degeneració respecte de les variables que es volen aïllar.
     idea: Calcular la submatriu de la jacobiana de $\Phi$ formada per les derivades respecte de $z$ i $t$, i el seu determinant al punt.
     detall: $\frac{\partial\Phi}{\partial(z,t)}=\begin{pmatrix}-1&0\\0&y\end{pmatrix}$, de determinant $-y$, que al punt val $-1\neq 0$.
  3. [aplicar_tfi] Aplicar el teorema de la funció implícita  (teoria: T4.13, T3.31)
     objectiu: Concloure l'existència de $g_1$ i $g_2$ diferenciables.
     idea: Comprovar totes les hipòtesis del teorema de la funció implícita (regularitat, punt solució, determinant) i llegir-ne la conclusió.
     detall: $\Phi$ és polinòmica, per tant $\mathcal{C}^\infty$. Pel teorema de la funció implícita existeixen un entorn $\Omega$ de $(1,1)$ i $(g_1,g_2)\in\mathcal{C}^\infty(\Omega)$ amb $g_1(1,1)=-1$, $g_2(1,1)=-1$ i $\Phi(x,y,g_1(x,y),g_2(x,y))=0$; a més, a prop del punt aquestes són les úniques solucions.
ERRORS COMUNS:
  - [menor_equivocat] Calcula el determinant respecte de $(x,y)$ en lloc de $(z,t)$.
  - [no_comprova_punt] No comprova que el punt satisfà el sistema.
  - [ordre_coordenades] Assigna malament les coordenades del punt (per exemple, pren $z=1$, $t=-1$ o $y=-1$).

TEORIA DEL CURS QUE FA SERVIR:
[T4.12] Nota 12 (Tema 4) — Motivació del teorema de la implícita
Explicació 12 (motivació del teorema de la funció implícita). El teorema de la funció implícita es pot interpretar des de dos punts de vista diferents, l'analític i el geomètric.

Per il·lustrar la versió analítica, prenem una funció de dues variables $f(x,y)$ definida en un domini $U\subset\mathbb{R}^2$. Aleshores, diem que l'equació $f(x,y)=0$ defineix implícitament $y=\varphi(x)$ en $\Omega$ si $f(x,y)=0$ i $y=\varphi(x)$ són equivalents per a tot $(x,y)\in\Omega$.

Geomètricament, equival a dir que el conjunt $M=\{(x,y)\in\Omega:f(x,y)=0\}$ és la gràfica d'alguna funció $\varphi$, és a dir, que per a cada $x_0$ del domini, $M$ talla $\{x=x_0\}$ exactament una vegada.

El teorema de la funció implícita s'enuncia per al cas general en què $x\in\mathbb{R}^n$ i $y\in\mathbb{R}^m$ i $f:\Omega\subseteq\mathbb{R}^{n+m}\to\mathbb{R}^m$, però, per prendre consciència del problema, igual que vam fer amb el teorema de la funció inversa, començarem fixant-nos en dues situacions que ens són familiars: les funcions de la dimensió més baixa possible ($n=1$, $m=1$) i les funcions lineals amb $n+m$ variables i $m$ components.

1. Considerem l'equació d'una recta al pla $ax+by+c=0$. Sabem que si $a\neq 0$, podem posar $x$ en funció de $y$, i que si $b\neq 0$, podem posar $y$ en funció de $x$:
$$x=-(by+c)/a;\qquad y=-(ax+c)/b.$$
En aquest exemple, $f(x,y)=ax+by+c$, mentre que en un cas tindríem $\varphi(y):=-(by+c)/a$ i en l'altre, $\varphi(x):=-(ax+c)/b$. En tots dos casos, observem que si el coeficient que acompanya una variable és diferent de zero, aleshores podem posar aquella variable en funció de l'altra. Observem que
$$a=\frac{\partial f}{\partial x};\qquad b=\frac{\partial f}{\partial y}.$$
En aquest exemple, hem pogut calcular $\varphi$ de manera explícita, però veurem més endavant que no és el més habitual... i d'aquí el terme *implícita* que acompanya els resultats d'aquesta secció.

2. Considerem ara una funció no lineal senzilla: $f(x,y)=x^2+y^2-1$. Clarament, $f(x,y)=0$ és un cercle de radi 1 centrat a l'origen.

Si volem escriure una variable en funció de l'altra, per exemple, $y$ en funció de $x$ (per simetria, l'altre cas és idèntic), tenim que
$$y=\pm\sqrt{1-x^2}=:\pm\varphi(x),\ \text{ amb }x\in[-1,1].$$
D'entrada, si bé es pot escriure explícitament, ja veiem que tenim dues funcions per a cada $x$. Però si ens situem a $(-1,0)$ o a $(1,0)$ ja veiem que $\varphi(x)$ no està definida en un entorn del punt. En canvi, en qualsevol punt de la forma $(x_0,\sqrt{1-x_0^2})$, amb $x_0\in(-1,1)$, sí que, localment, podem definir $y=\varphi(x)$ tal que $\varphi(x_0)=\sqrt{1-x_0^2}$ (anàlogament per a punts de la forma $(x_0,-\sqrt{1-x_0^2})$, amb $x_0\in(-1,1)$).

Acabem observant, amb tota la intenció, que $\dfrac{\partial f}{\partial y}=2\,y$ i, per tant, que
$$\frac{\partial f}{\partial y}(\pm1,0)=0;\qquad\frac{\partial f}{\partial y}\Big(x_0,\sqrt{1-x_0^2}\Big)\neq 0,\ \text{ si }x_0\in(-1,1).$$

3. El significat del terme "implícit", el veurem plenament en funcions com
$$f(x,y)=y+x^2y+e^xy^3+x^4y^5+\sin x=0$$
en què es pot definir localment $y=\varphi(x)$ per a tot $x\in\mathbb{R}$ perquè
$$\frac{\partial f}{\partial y}(x,y)=1+x^2+3e^xy^2+5x^4y^4>0,$$
però que $y$ no es pot aïllar explícitament.

4. Considerem, per exemple, el sistema
$$\begin{cases}3x_1+x_2+x_3+x_4&=0,\\ x_1+x_2+x_3+x_4&=0.\end{cases}$$
Té rang 2 i 4 variables; per tant, és un sistema compatible indeterminat amb dos graus de llibertat, que es pot interpretar com $f(x)=0$, on $x=(x_1,x_2,x_3,x_4)$ i $f:\mathbb{R}^4\to\mathbb{R}^2$, amb $f(x)=(3x_1+x_2+x_3+x_4,\,x_1+x_2+x_3+x_4)$.

La solució del sistema és $x_1=0$ i $x_2+x_3+x_4=0$. Per tant, podem expressar $(x_1,x_j)$, per a $j=2,3,4$, en funció de les altres dues variables, però, en canvi, no podem expressar $(x_j,x_k)$ amb $j,k\in\{2,3,4\}$ en funció de $x_1$ i la variable restant. "Casualment", es dona la circumstància que
$$\left|\frac{\partial f}{\partial(x_1,x_j)}\right|=\begin{vmatrix}3&1\\ 1&1\end{vmatrix}=2\neq 0,\qquad\forall j\in\{2,3,4\},$$
$$\left|\frac{\partial f}{\partial(x_j,x_k)}\right|=\begin{vmatrix}1&1\\ 1&1\end{vmatrix}=0,\qquad\forall j,k\in\{2,3,4\}.$$
Es pot veure fàcilment que, si consideréssim, per exemple, el sistema
$$\begin{cases}3x_1+\mathbf{2}x_2+x_3+x_4&=0,\\ x_1+x_2+x_3+x_4&=0,\end{cases}$$
aleshores $(x_3,x_4)$ és l'únic parell de variables que no podríem posar simultàniament en funció de les altres dues variables.

El teorema de la funció implícita generalitza aquestes situacions. En el cas de les funcions lineals, ens dirà (cosa que ja sabem d'àlgebra lineal) que per al sistema
$$\begin{cases}a_{11}x_1+\cdots+a_{1n}x_n+b_{11}y_1+\cdots+b_{1m}y_m&=0,\\ \vdots&\vdots\\ a_{m1}x_1+\cdots+a_{mn}x_n+b_{m1}y_1+\cdots+b_{mm}y_m&=0,\end{cases}$$
si tenim que
$$\det\begin{pmatrix}b_{11}&\ldots&b_{1m}\\ \vdots&\vdots&\vdots\\ b_{m1}&\ldots&b_{mm}\end{pmatrix}\neq 0,$$
aleshores $(y_1,\ldots,y_m)$ es poden posar en funció de $(x_1,\ldots,x_n)$.

[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$

[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]

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

[1] Volem aïllar $z$ i $t$ en funció de $x$ i $y$. Escrivim el sistema com $\Phi(x,y,z,t)=(0,0)$, amb $\Phi(x,y,z,t)=(x-2y-z,\,x+yt)$, que és polinòmica i per tant de classe $\mathcal{C}^\infty$ a $\mathbb{R}^4$.
[2] El punt $(x,y,z,t)=(1,1,-1,-1)$ és solució del sistema: $\Phi(1,1,-1,-1)=(1-2+1,\,1+1\cdot(-1))=(0,0)$.
[3] La matriu de derivades parcials respecte de les variables que volem aïllar és $\frac{\partial\Phi}{\partial(z,t)}=\begin{pmatrix}-1&0\\0&t\end{pmatrix}$, de determinant $-t$, que al punt val $1\neq0$.
[4] Per tant es compleixen les hipòtesis del teorema de la funció implícita: $\Phi$ és de classe $\mathcal{C}^\infty$, s'anul·la al punt i el menor respecte de $(z,t)$ hi és invertible.
[5] El teorema dona un entorn obert $\Omega$ de $(-1,-1)$ i funcions $g_1,g_2\in\mathcal{C}^\infty(\Omega)$, amb $g_1(-1,-1)=1$ i $g_2(-1,-1)=1$, tals que $\Phi(x,y,g_1(x,y),g_2(x,y))=(0,0)$ per a tot $(x,y)\in\Omega$; en particular, $z=g_1(x,y)$ i $t=g_2(x,y)$ són diferenciables.


## t4-18:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Proveu que el sistema
$$\left.\begin{aligned}xz^3+y^2u^3&=1\\ 2xy^3+u^2z&=0\end{aligned}\right\}$$
permet definir $x$ i $y$ com a funcions implícites diferenciables de $z$ i de $u$ en un entorn de $(0,1,0,1)$. Si $x=g_1(z,u)$ i $y=g_2(z,u)$ són les funcions esmentades, proveu que la funció $g(z,u)=(g_1(z,u),g_2(z,u))$ té inversa local diferenciable al voltant del punt $(0,1)$.
RESULTAT CORRECTE: Amb $\Phi(x,y,z,u)=(xz^3+y^2u^3-1,\,2xy^3+u^2z)\in\mathcal{C}^\infty$: $\Phi(0,1,0,1)=(0,0)$ i $\frac{\partial\Phi}{\partial(x,y)}(0,1,0,1)=\begin{pmatrix}0&2\\2&0\end{pmatrix}$, de determinant $-4\neq 0$. Pel teorema de la funció implícita, $g=(g_1,g_2)$ és $\mathcal{C}^\infty$ en un entorn de $(0,1)$ amb $g(0,1)=(0,1)$, i
$Dg(0,1)=-\begin{pmatrix}0&2\\2&0\end{pmatrix}^{-1}\begin{pmatrix}0&3\\1&0\end{pmatrix}=\begin{pmatrix}-\frac12&0\\0&-\frac32\end{pmatrix}$, amb $\det Dg(0,1)=\frac34\neq 0$. Pel teorema de la funció inversa, $g$ té inversa local diferenciable (de fet $\mathcal{C}^\infty$) a prop de $(0,1)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [comprovar_punt] El punt és solució
     objectiu: Escriure el sistema com $\Phi=0$ i comprovar que el punt hi pertany.
     idea: Passar tot a un costat, definir $\Phi:\mathbb{R}^4\to\mathbb{R}^2$ i avaluar al punt amb l'ordre $(x,y,z,u)$.
     detall: $\Phi(x,y,z,u)=(xz^3+y^2u^3-1,\,2xy^3+u^2z)$; $\Phi(0,1,0,1)=(0+1-1,\,0+0)=(0,0)$.
  2. [menor_xy] Menor respecte de $(x,y)$  (teoria: T3.10)
     objectiu: Comprovar la condició del teorema de la funció implícita respecte de les variables $x$, $y$.
     idea: Submatriu de la jacobiana de $\Phi$ formada per les derivades respecte de $x$ i $y$, avaluada al punt.
     detall: $\frac{\partial\Phi}{\partial(x,y)}=\begin{pmatrix}z^3&2yu^3\\2y^3&6xy^2\end{pmatrix}$; al punt, $\begin{pmatrix}0&2\\2&0\end{pmatrix}$, de determinant $-4\neq 0$.
  3. [implicita] Existència de $g$  (teoria: T4.13, T3.31)
     objectiu: Concloure que $x$ i $y$ són funcions diferenciables de $(z,u)$ a prop del punt.
     idea: Aplicar el teorema de la funció implícita amb totes les seves hipòtesis.
     detall: $\Phi$ és polinòmica, $\mathcal{C}^\infty$. Pel teorema de la funció implícita existeix $g=(g_1,g_2)$ de classe $\mathcal{C}^\infty$ en un entorn obert $\Omega$ de $(0,1)$, amb $g(0,1)=(0,1)$ i $\Phi(g_1(z,u),g_2(z,u),z,u)=0$.
  4. [diferencial_g] Diferencial de $g$ al punt  (teoria: T4.15)
     objectiu: Calcular $Dg(0,1)$.
     idea: Derivar $\Phi(g(z,u),z,u)=0$ amb la regla de la cadena (fórmula de la diferencial de la funció implícita).
     detall: $\frac{\partial\Phi}{\partial(z,u)}=\begin{pmatrix}3xz^2&3y^2u^2\\u^2&2uz\end{pmatrix}$, al punt $\begin{pmatrix}0&3\\1&0\end{pmatrix}$. Llavors
$Dg(0,1)=-\begin{pmatrix}0&2\\2&0\end{pmatrix}^{-1}\begin{pmatrix}0&3\\1&0\end{pmatrix}=-\begin{pmatrix}0&\frac12\\ \frac12&0\end{pmatrix}\begin{pmatrix}0&3\\1&0\end{pmatrix}=\begin{pmatrix}-\frac12&0\\0&-\frac32\end{pmatrix}$.
  5. [inversa_g] Inversa local de $g$  (teoria: T4.5)
     objectiu: Demostrar que $g$ té inversa local diferenciable a prop de $(0,1)$.
     idea: Aplicar el teorema de la funció inversa a $g:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}^2$.
     detall: $g\in\mathcal{C}^\infty(\Omega)$, $\Omega$ obert, i $\det Dg(0,1)=\frac12\cdot\frac32=\frac34\neq 0$. Pel teorema de la funció inversa, $g$ és injectiva en un entorn de $(0,1)$, la imatge d'aquest entorn és un obert que conté $g(0,1)=(0,1)$ i la inversa local és $\mathcal{C}^\infty$ (en particular diferenciable).
ERRORS COMUNS:
  - [menor_equivocat] Calcula el menor respecte de $(z,u)$ en lloc de $(x,y)$.
  - [sense_formula_explicita] Creu que cal trobar $g$ explícitament per poder aplicar el teorema de la funció inversa.
  - [signe_o_ordre] Oblida el signe menys a $Dg=-\big(\frac{\partial\Phi}{\partial(x,y)}\big)^{-1}\frac{\partial\Phi}{\partial(z,u)}$ o multiplica en l'ordre equivocat.
  - [regularitat_g] Aplica el TFI a $g$ sense justificar que $g$ és de classe $\mathcal{C}^1$.

TEORIA DEL CURS QUE FA SERVIR:
[T4.12] Nota 12 (Tema 4) — Motivació del teorema de la implícita
Explicació 12 (motivació del teorema de la funció implícita). El teorema de la funció implícita es pot interpretar des de dos punts de vista diferents, l'analític i el geomètric.

Per il·lustrar la versió analítica, prenem una funció de dues variables $f(x,y)$ definida en un domini $U\subset\mathbb{R}^2$. Aleshores, diem que l'equació $f(x,y)=0$ defineix implícitament $y=\varphi(x)$ en $\Omega$ si $f(x,y)=0$ i $y=\varphi(x)$ són equivalents per a tot $(x,y)\in\Omega$.

Geomètricament, equival a dir que el conjunt $M=\{(x,y)\in\Omega:f(x,y)=0\}$ és la gràfica d'alguna funció $\varphi$, és a dir, que per a cada $x_0$ del domini, $M$ talla $\{x=x_0\}$ exactament una vegada.

El teorema de la funció implícita s'enuncia per al cas general en què $x\in\mathbb{R}^n$ i $y\in\mathbb{R}^m$ i $f:\Omega\subseteq\mathbb{R}^{n+m}\to\mathbb{R}^m$, però, per prendre consciència del problema, igual que vam fer amb el teorema de la funció inversa, començarem fixant-nos en dues situacions que ens són familiars: les funcions de la dimensió més baixa possible ($n=1$, $m=1$) i les funcions lineals amb $n+m$ variables i $m$ components.

1. Considerem l'equació d'una recta al pla $ax+by+c=0$. Sabem que si $a\neq 0$, podem posar $x$ en funció de $y$, i que si $b\neq 0$, podem posar $y$ en funció de $x$:
$$x=-(by+c)/a;\qquad y=-(ax+c)/b.$$
En aquest exemple, $f(x,y)=ax+by+c$, mentre que en un cas tindríem $\varphi(y):=-(by+c)/a$ i en l'altre, $\varphi(x):=-(ax+c)/b$. En tots dos casos, observem que si el coeficient que acompanya una variable és diferent de zero, aleshores podem posar aquella variable en funció de l'altra. Observem que
$$a=\frac{\partial f}{\partial x};\qquad b=\frac{\partial f}{\partial y}.$$
En aquest exemple, hem pogut calcular $\varphi$ de manera explícita, però veurem més endavant que no és el més habitual... i d'aquí el terme *implícita* que acompanya els resultats d'aquesta secció.

2. Considerem ara una funció no lineal senzilla: $f(x,y)=x^2+y^2-1$. Clarament, $f(x,y)=0$ és un cercle de radi 1 centrat a l'origen.

Si volem escriure una variable en funció de l'altra, per exemple, $y$ en funció de $x$ (per simetria, l'altre cas és idèntic), tenim que
$$y=\pm\sqrt{1-x^2}=:\pm\varphi(x),\ \text{ amb }x\in[-1,1].$$
D'entrada, si bé es pot escriure explícitament, ja veiem que tenim dues funcions per a cada $x$. Però si ens situem a $(-1,0)$ o a $(1,0)$ ja veiem que $\varphi(x)$ no està definida en un entorn del punt. En canvi, en qualsevol punt de la forma $(x_0,\sqrt{1-x_0^2})$, amb $x_0\in(-1,1)$, sí que, localment, podem definir $y=\varphi(x)$ tal que $\varphi(x_0)=\sqrt{1-x_0^2}$ (anàlogament per a punts de la forma $(x_0,-\sqrt{1-x_0^2})$, amb $x_0\in(-1,1)$).

Acabem observant, amb tota la intenció, que $\dfrac{\partial f}{\partial y}=2\,y$ i, per tant, que
$$\frac{\partial f}{\partial y}(\pm1,0)=0;\qquad\frac{\partial f}{\partial y}\Big(x_0,\sqrt{1-x_0^2}\Big)\neq 0,\ \text{ si }x_0\in(-1,1).$$

3. El significat del terme "implícit", el veurem plenament en funcions com
$$f(x,y)=y+x^2y+e^xy^3+x^4y^5+\sin x=0$$
en què es pot definir localment $y=\varphi(x)$ per a tot $x\in\mathbb{R}$ perquè
$$\frac{\partial f}{\partial y}(x,y)=1+x^2+3e^xy^2+5x^4y^4>0,$$
però que $y$ no es pot aïllar explícitament.

4. Considerem, per exemple, el sistema
$$\begin{cases}3x_1+x_2+x_3+x_4&=0,\\ x_1+x_2+x_3+x_4&=0.\end{cases}$$
Té rang 2 i 4 variables; per tant, és un sistema compatible indeterminat amb dos graus de llibertat, que es pot interpretar com $f(x)=0$, on $x=(x_1,x_2,x_3,x_4)$ i $f:\mathbb{R}^4\to\mathbb{R}^2$, amb $f(x)=(3x_1+x_2+x_3+x_4,\,x_1+x_2+x_3+x_4)$.

La solució del sistema és $x_1=0$ i $x_2+x_3+x_4=0$. Per tant, podem expressar $(x_1,x_j)$, per a $j=2,3,4$, en funció de les altres dues variables, però, en canvi, no podem expressar $(x_j,x_k)$ amb $j,k\in\{2,3,4\}$ en funció de $x_1$ i la variable restant. "Casualment", es dona la circumstància que
$$\left|\frac{\partial f}{\partial(x_1,x_j)}\right|=\begin{vmatrix}3&1\\ 1&1\end{vmatrix}=2\neq 0,\qquad\forall j\in\{2,3,4\},$$
$$\left|\frac{\partial f}{\partial(x_j,x_k)}\right|=\begin{vmatrix}1&1\\ 1&1\end{vmatrix}=0,\qquad\forall j,k\in\{2,3,4\}.$$
Es pot veure fàcilment que, si consideréssim, per exemple, el sistema
$$\begin{cases}3x_1+\mathbf{2}x_2+x_3+x_4&=0,\\ x_1+x_2+x_3+x_4&=0,\end{cases}$$
aleshores $(x_3,x_4)$ és l'únic parell de variables que no podríem posar simultàniament en funció de les altres dues variables.

El teorema de la funció implícita generalitza aquestes situacions. En el cas de les funcions lineals, ens dirà (cosa que ja sabem d'àlgebra lineal) que per al sistema
$$\begin{cases}a_{11}x_1+\cdots+a_{1n}x_n+b_{11}y_1+\cdots+b_{1m}y_m&=0,\\ \vdots&\vdots\\ a_{m1}x_1+\cdots+a_{mn}x_n+b_{m1}y_1+\cdots+b_{mm}y_m&=0,\end{cases}$$
si tenim que
$$\det\begin{pmatrix}b_{11}&\ldots&b_{1m}\\ \vdots&\vdots&\vdots\\ b_{m1}&\ldots&b_{mm}\end{pmatrix}\neq 0,$$
aleshores $(y_1,\ldots,y_m)$ es poden posar en funció de $(x_1,\ldots,x_n)$.

[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$

[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]

[T3.31] Definició 31 (Tema 3) — Classes C^r de funcions
Direm que $f\in\mathcal{C}^0(\Omega)\Leftrightarrow f$ és contínua a $\Omega$.

$f\in\mathcal{C}^1(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ a tot punt de $\Omega$ i totes són contínues (per tant, en particular, $f$ és diferenciable i contínua).

$f\in\mathcal{C}^2(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ d'ordre $2$:
$$\frac{\partial^2f}{\partial x_i\partial x_j}=\frac{\partial}{\partial x_j}\left(\frac{\partial f}{\partial x_i}\right),$$
a tot punt de $\Omega$ i són contínues.

En general, per a $r\geq1$, es diu que $f\in\mathcal{C}^r(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials d'ordre $r$ a $\Omega$ i totes són contínues. Clarament, $f\in\mathcal{C}^{r+1}(\Omega)\Rightarrow f\in\mathcal{C}^r(\Omega)$.

Direm que $f\in\mathcal{C}^\infty(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials a qualsevol ordre de $f$ a $\Omega$ i totes són contínues.

[T4.15] Observació 15 (Tema 4) — Diferencial de la funció implícita
$D\varphi(a)$ es pot calcular aplicant la regla de la cadena a l'equació $\Phi(x,\varphi(x))=0$ en un entorn de $(a,b)$:
$$\frac{\partial\Phi}{\partial x}(a,b)+\frac{\partial\Phi}{\partial y}(a,b)\cdot\frac{\partial\varphi}{\partial x}(a)=0.$$

A l'enunciat de l'observació hem mantingut la notació en derivades parcials, però cal tenir en compte que $\dfrac{\partial\varphi}{\partial x}(a)$ és simplement $D\varphi(a)$.

[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.
</solucio_de_referencia>

### Document a revisar

[1] Escrivim el sistema com $\Phi(x,y,z,u)=(0,0)$ amb $\Phi(x,y,z,u)=(xz^3+y^2u^3-1,\,2xy^3+u^2z)$, polinòmica i per tant de classe $\mathcal{C}^\infty$. El punt és solució: $\Phi(0,1,0,1)=(0+1-1,\,0+0)=(0,0)$.
[2] Com que volem aïllar $x$ i $y$, calculem $\frac{\partial\Phi}{\partial(x,y)}=\begin{pmatrix}z^3&2yu^3\\2y^3&6xy^2\end{pmatrix}$, que al punt $(0,1,0,1)$ val $\begin{pmatrix}0&2\\2&0\end{pmatrix}$, de determinant $-4\neq0$.
[3] Pel teorema de la funció implícita existeixen un entorn obert $\Omega$ de $(0,1)$ i $g=(g_1,g_2)\in\mathcal{C}^\infty(\Omega)$ amb $g(0,1)=(0,1)$ i $\Phi(g_1(z,u),g_2(z,u),z,u)=(0,0)$ per a tot $(z,u)\in\Omega$.
[4] Derivant aquesta identitat amb la regla de la cadena, $\frac{\partial\Phi}{\partial(x,y)}\,Dg+\frac{\partial\Phi}{\partial(z,u)}=0$, és a dir, $Dg(0,1)=-\Big(\frac{\partial\Phi}{\partial(x,y)}\Big)^{-1}\frac{\partial\Phi}{\partial(z,u)}$, amb les dues matrius avaluades a $(0,1,0,1)$.
[5] $\frac{\partial\Phi}{\partial(z,u)}=\begin{pmatrix}3xz^2&3y^2u^2\\u^2&2uz\end{pmatrix}$, que al punt val $\begin{pmatrix}0&3\\1&0\end{pmatrix}$; a més, $\begin{pmatrix}0&2\\2&0\end{pmatrix}^{-1}=\begin{pmatrix}0&\frac12\\ \frac12&0\end{pmatrix}$.
[6] Llavors $Dg(0,1)=-\begin{pmatrix}0&3\\1&0\end{pmatrix}\begin{pmatrix}0&\frac12\\ \frac12&0\end{pmatrix}=-\begin{pmatrix}\frac32&0\\0&\frac12\end{pmatrix}=\begin{pmatrix}-\frac32&0\\0&-\frac12\end{pmatrix}$.
[7] Per tant $\det Dg(0,1)=\left(-\frac32\right)\left(-\frac12\right)=\frac34\neq0$.
[8] Com que $g$ és de classe $\mathcal{C}^\infty$ a l'obert $\Omega$ i $\det Dg(0,1)\neq0$, el teorema de la funció inversa garanteix que $g$ és injectiva a tot $\Omega$ i que la seva inversa és de classe $\mathcal{C}^\infty$. En particular, $g$ té inversa local diferenciable al voltant de $(0,1)$.


## t4-19a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considereu el sistema d'equacions
$$\left.\begin{aligned}x-u-v&=0\\ y-u^2-v^2&=0\\ z-u^3-v^3&=0\end{aligned}\right\}$$
Trobeu els punts $p=(x_0,y_0,z_0,u_0,v_0)\in\mathbb{R}^5$ que compleixin les dues condicions següents:

(a) el sistema defineix funcions implícites diferenciables, $z=f_1(x,y)$, $u=f_2(x,y)$ i $v=f_3(x,y)$ al voltant de $p$;
RESULTAT CORRECTE: Els punts $p=(u_0+v_0,\ u_0^2+v_0^2,\ u_0^3+v_0^3,\ u_0,\ v_0)$ amb $u_0\neq v_0$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [punts_solucio] Punts del sistema
     objectiu: Descriure tots els punts $p\in\mathbb{R}^5$ que satisfan el sistema.
     idea: Les equacions donen $x$, $y$, $z$ directament en funció de $u$, $v$.
     detall: $p$ és solució si i només si $x_0=u_0+v_0$, $y_0=u_0^2+v_0^2$, $z_0=u_0^3+v_0^3$, amb $(u_0,v_0)\in\mathbb{R}^2$ arbitrari.
  2. [menor] Menor respecte de $(z,u,v)$  (teoria: T3.10)
     objectiu: Calcular el determinant que controla si $(z,u,v)$ es poden posar en funció de $(x,y)$.
     idea: Submatriu $3\times 3$ de la jacobiana de $\Phi$ formada per les derivades respecte de $z$, $u$, $v$.
     detall: Amb $\Phi=(x-u-v,\,y-u^2-v^2,\,z-u^3-v^3)$: $\frac{\partial\Phi}{\partial(z,u,v)}=\begin{pmatrix}0&-1&-1\\0&-2u&-2v\\1&-3u^2&-3v^2\end{pmatrix}$, de determinant $\begin{vmatrix}-1&-1\\-2u&-2v\end{vmatrix}=2v-2u=2(v-u)$.
  3. [concloure] Condició sobre $p$  (teoria: T4.13, T3.21)
     objectiu: Determinar exactament en quins punts del sistema existeixen les funcions implícites diferenciables.
     idea: On el determinant no s'anul·la, aplicar el teorema de la funció implícita; on s'anul·la, veure si la regla de la cadena porta a contradicció suposant que les funcions existeixen.
     detall: $\Phi$ és polinòmica. Si $u_0\neq v_0$, el determinant és no nul i el teorema de la funció implícita dona $f_1,f_2,f_3$ de classe $\mathcal{C}^\infty$ a prop de $(x_0,y_0)$. Si $u_0=v_0$ i existissin $f_2,f_3$ diferenciables, derivant $x=f_2+f_3$ i $y=f_2^2+f_3^2$ respecte de $y$ al punt: $0=\frac{\partial f_2}{\partial y}+\frac{\partial f_3}{\partial y}$ i $1=2u_0\big(\frac{\partial f_2}{\partial y}+\frac{\partial f_3}{\partial y}\big)=0$, contradicció. Per tant la condició és exactament $u_0\neq v_0$.
ERRORS COMUNS:
  - [menor_equivocat] Calcula el determinant respecte d'unes variables que no són $(z,u,v)$, o una submatriu que no és quadrada.
  - [oblida_punts_solucio] Dona la condició sobre $(u_0,v_0)$ però no imposa que $p$ satisfaci el sistema (deixa $x_0,y_0,z_0$ lliures).
  - [condicio_nomes_suficient] Diu que quan el determinant s'anul·la "no es pot aplicar el teorema" i conclou que no hi ha funcions implícites, sense justificar-ho.

TEORIA DEL CURS QUE FA SERVIR:
[T4.12] Nota 12 (Tema 4) — Motivació del teorema de la implícita
Explicació 12 (motivació del teorema de la funció implícita). El teorema de la funció implícita es pot interpretar des de dos punts de vista diferents, l'analític i el geomètric.

Per il·lustrar la versió analítica, prenem una funció de dues variables $f(x,y)$ definida en un domini $U\subset\mathbb{R}^2$. Aleshores, diem que l'equació $f(x,y)=0$ defineix implícitament $y=\varphi(x)$ en $\Omega$ si $f(x,y)=0$ i $y=\varphi(x)$ són equivalents per a tot $(x,y)\in\Omega$.

Geomètricament, equival a dir que el conjunt $M=\{(x,y)\in\Omega:f(x,y)=0\}$ és la gràfica d'alguna funció $\varphi$, és a dir, que per a cada $x_0$ del domini, $M$ talla $\{x=x_0\}$ exactament una vegada.

El teorema de la funció implícita s'enuncia per al cas general en què $x\in\mathbb{R}^n$ i $y\in\mathbb{R}^m$ i $f:\Omega\subseteq\mathbb{R}^{n+m}\to\mathbb{R}^m$, però, per prendre consciència del problema, igual que vam fer amb el teorema de la funció inversa, començarem fixant-nos en dues situacions que ens són familiars: les funcions de la dimensió més baixa possible ($n=1$, $m=1$) i les funcions lineals amb $n+m$ variables i $m$ components.

1. Considerem l'equació d'una recta al pla $ax+by+c=0$. Sabem que si $a\neq 0$, podem posar $x$ en funció de $y$, i que si $b\neq 0$, podem posar $y$ en funció de $x$:
$$x=-(by+c)/a;\qquad y=-(ax+c)/b.$$
En aquest exemple, $f(x,y)=ax+by+c$, mentre que en un cas tindríem $\varphi(y):=-(by+c)/a$ i en l'altre, $\varphi(x):=-(ax+c)/b$. En tots dos casos, observem que si el coeficient que acompanya una variable és diferent de zero, aleshores podem posar aquella variable en funció de l'altra. Observem que
$$a=\frac{\partial f}{\partial x};\qquad b=\frac{\partial f}{\partial y}.$$
En aquest exemple, hem pogut calcular $\varphi$ de manera explícita, però veurem més endavant que no és el més habitual... i d'aquí el terme *implícita* que acompanya els resultats d'aquesta secció.

2. Considerem ara una funció no lineal senzilla: $f(x,y)=x^2+y^2-1$. Clarament, $f(x,y)=0$ és un cercle de radi 1 centrat a l'origen.

Si volem escriure una variable en funció de l'altra, per exemple, $y$ en funció de $x$ (per simetria, l'altre cas és idèntic), tenim que
$$y=\pm\sqrt{1-x^2}=:\pm\varphi(x),\ \text{ amb }x\in[-1,1].$$
D'entrada, si bé es pot escriure explícitament, ja veiem que tenim dues funcions per a cada $x$. Però si ens situem a $(-1,0)$ o a $(1,0)$ ja veiem que $\varphi(x)$ no està definida en un entorn del punt. En canvi, en qualsevol punt de la forma $(x_0,\sqrt{1-x_0^2})$, amb $x_0\in(-1,1)$, sí que, localment, podem definir $y=\varphi(x)$ tal que $\varphi(x_0)=\sqrt{1-x_0^2}$ (anàlogament per a punts de la forma $(x_0,-\sqrt{1-x_0^2})$, amb $x_0\in(-1,1)$).

Acabem observant, amb tota la intenció, que $\dfrac{\partial f}{\partial y}=2\,y$ i, per tant, que
$$\frac{\partial f}{\partial y}(\pm1,0)=0;\qquad\frac{\partial f}{\partial y}\Big(x_0,\sqrt{1-x_0^2}\Big)\neq 0,\ \text{ si }x_0\in(-1,1).$$

3. El significat del terme "implícit", el veurem plenament en funcions com
$$f(x,y)=y+x^2y+e^xy^3+x^4y^5+\sin x=0$$
en què es pot definir localment $y=\varphi(x)$ per a tot $x\in\mathbb{R}$ perquè
$$\frac{\partial f}{\partial y}(x,y)=1+x^2+3e^xy^2+5x^4y^4>0,$$
però que $y$ no es pot aïllar explícitament.

4. Considerem, per exemple, el sistema
$$\begin{cases}3x_1+x_2+x_3+x_4&=0,\\ x_1+x_2+x_3+x_4&=0.\end{cases}$$
Té rang 2 i 4 variables; per tant, és un sistema compatible indeterminat amb dos graus de llibertat, que es pot interpretar com $f(x)=0$, on $x=(x_1,x_2,x_3,x_4)$ i $f:\mathbb{R}^4\to\mathbb{R}^2$, amb $f(x)=(3x_1+x_2+x_3+x_4,\,x_1+x_2+x_3+x_4)$.

La solució del sistema és $x_1=0$ i $x_2+x_3+x_4=0$. Per tant, podem expressar $(x_1,x_j)$, per a $j=2,3,4$, en funció de les altres dues variables, però, en canvi, no podem expressar $(x_j,x_k)$ amb $j,k\in\{2,3,4\}$ en funció de $x_1$ i la variable restant. "Casualment", es dona la circumstància que
$$\left|\frac{\partial f}{\partial(x_1,x_j)}\right|=\begin{vmatrix}3&1\\ 1&1\end{vmatrix}=2\neq 0,\qquad\forall j\in\{2,3,4\},$$
$$\left|\frac{\partial f}{\partial(x_j,x_k)}\right|=\begin{vmatrix}1&1\\ 1&1\end{vmatrix}=0,\qquad\forall j,k\in\{2,3,4\}.$$
Es pot veure fàcilment que, si consideréssim, per exemple, el sistema
$$\begin{cases}3x_1+\mathbf{2}x_2+x_3+x_4&=0,\\ x_1+x_2+x_3+x_4&=0,\end{cases}$$
aleshores $(x_3,x_4)$ és l'únic parell de variables que no podríem posar simultàniament en funció de les altres dues variables.

El teorema de la funció implícita generalitza aquestes situacions. En el cas de les funcions lineals, ens dirà (cosa que ja sabem d'àlgebra lineal) que per al sistema
$$\begin{cases}a_{11}x_1+\cdots+a_{1n}x_n+b_{11}y_1+\cdots+b_{1m}y_m&=0,\\ \vdots&\vdots\\ a_{m1}x_1+\cdots+a_{mn}x_n+b_{m1}y_1+\cdots+b_{mm}y_m&=0,\end{cases}$$
si tenim que
$$\det\begin{pmatrix}b_{11}&\ldots&b_{1m}\\ \vdots&\vdots&\vdots\\ b_{m1}&\ldots&b_{mm}\end{pmatrix}\neq 0,$$
aleshores $(y_1,\ldots,y_m)$ es poden posar en funció de $(x_1,\ldots,x_n)$.

[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$

[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$
</solucio_de_referencia>

### Document a revisar

[1] Un punt $p=(x_0,y_0,z_0,u_0,v_0)$ és solució del sistema si i només si $x_0=u_0+v_0$, $y_0=u_0^2+v_0^2$ i $z_0=u_0^3+v_0^3$, amb $(u_0,v_0)\in\mathbb{R}^2$ qualsevol.
[2] Sigui $\Phi=(x-u-v,\,y-u^2-v^2,\,z-u^3-v^3)$, polinòmica i per tant de classe $\mathcal{C}^\infty$. Com que volem aïllar $z,u,v$, calculem $\frac{\partial\Phi}{\partial(z,u,v)}=\begin{pmatrix}0&-1&-1\\0&-2u&-2v\\1&-3u^2&-3v^2\end{pmatrix}$.
[3] Desenvolupant per la primera columna, $\det\frac{\partial\Phi}{\partial(z,u,v)}=\begin{vmatrix}-1&-1\\-2u&-2v\end{vmatrix}$, que val $2u-2v$.
[4] Si $u_0\neq v_0$, aquest determinant és no nul a $p$, i el teorema de la funció implícita dona $f_1,f_2,f_3$ de classe $\mathcal{C}^\infty$ en un entorn de $(x_0,y_0)$, amb $(f_1,f_2,f_3)(x_0,y_0)=(z_0,u_0,v_0)$.
[5] Si $u_0=v_0$, el determinant s'anul·la a $p$ i, per tant, pel teorema de la funció implícita, el sistema no defineix funcions implícites diferenciables al voltant de $p$.
[6] Per tant, els punts buscats són $p=(u_0+v_0,\ u_0^2+v_0^2,\ u_0^3+v_0^3,\ u_0,\ v_0)$ amb $u_0\neq v_0$.


## t4-21a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considereu l'equació $x^2+y^2+z^2=\psi(ax+by+cz)$, amb $a,b,c\in\mathbb{R}$, $c\neq 0$, on $\psi:\mathbb{R}\to\mathbb{R}$ és de classe $\mathcal{C}^2$ i satisfà $\psi(0)=0$ i $\psi'(0)\neq 0$.

(a) Proveu que en un entorn de $(0,0,0)$ les solucions de l'equació es poden expressar de la forma $(x,y,f(x,y))$, amb $f$ diferenciable en un entorn de $(0,0)$.
RESULTAT CORRECTE: Sigui $G(x,y,z)=x^2+y^2+z^2-\psi(ax+by+cz)$, de classe $\mathcal{C}^2$, amb $G(0,0,0)=0$ i $\frac{\partial G}{\partial z}(0,0,0)=-c\psi'(0)\neq 0$. Pel teorema de la funció implícita existeixen entorns oberts $U$ de $(0,0,0)$ i $\Omega$ de $(0,0)$ i $f\in\mathcal{C}^2(\Omega)$ amb $f(0,0)=0$ tals que $\{(x,y,z)\in U: G=0\}=\{(x,y,f(x,y)):(x,y)\in\Omega\}$; en particular $f$ és diferenciable.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [plantejar_g] Escriure l'equació com G=0  (teoria: T3.31, T3.21)
     objectiu: Escriure el problema en el llenguatge del teorema de la funció implícita i comprovar la regularitat i que l'origen és solució.
     idea: Passar-ho tot a un costat i justificar la classe de la funció resultant (polinomi més composició de $\psi$ amb una funció lineal).
     detall: $G(x,y,z)=x^2+y^2+z^2-\psi(ax+by+cz)$. És de classe $\mathcal{C}^2$ perquè $\psi\in\mathcal{C}^2$ i $ax+by+cz$ és lineal, i $G(0,0,0)=-\psi(0)=0$.
  2. [derivada_z] Condició sobre la derivada respecte de z  (teoria: T4.13, T3.21)
     objectiu: Comprovar la hipòtesi del teorema que permet aïllar $z$ i concloure.
     idea: Calcular la derivada parcial de $G$ respecte de la variable que es vol aïllar en l'origen (regla de la cadena per al terme amb $\psi$) i usar les hipòtesis sobre $c$ i $\psi'(0)$.
     detall: $\frac{\partial G}{\partial z}=2z-c\,\psi'(ax+by+cz)$, que en l'origen val $-c\,\psi'(0)\neq 0$ perquè $c\neq 0$ i $\psi'(0)\neq 0$. El teorema de la funció implícita (amb $r=2$) dona entorns $U\ni(0,0,0)$, $\Omega\ni(0,0)$ i $f\in\mathcal{C}^2(\Omega)$, $f(0,0)=0$, amb $\{(x,y,z)\in U:G=0\}=\{(x,y,f(x,y)):(x,y)\in\Omega\}$. En particular $f$ és diferenciable en $\Omega$.
ERRORS COMUNS:
  - [oblidar_cadena_psi] Deriva $\psi(ax+by+cz)$ respecte de $z$ oblidant el factor $c$ de la regla de la cadena, i aleshores no veu per què cal $c\neq 0$.
  - [nomes_existencia] Conclou només que hi ha alguna funció $f$ amb $G(x,y,f(x,y))=0$, sense dir que totes les solucions properes a l'origen són d'aquesta forma.

TEORIA DEL CURS QUE FA SERVIR:
[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$

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

[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]
</solucio_de_referencia>

### Document a revisar

[1] Sigui $G(x,y,z)=x^2+y^2+z^2-\psi(ax+by+cz)$. És de classe $\mathcal{C}^2$, perquè $\psi\in\mathcal{C}^2$ i $(x,y,z)\mapsto ax+by+cz$ és lineal, i les solucions de l'equació són exactament els zeros de $G$.
[2] A l'origen, $G(0,0,0)=0-\psi(0)=0$, de manera que $(0,0,0)$ és solució.
[3] Derivant respecte de $z$, $\frac{\partial G}{\partial z}=2z-\psi'(ax+by+cz)$, que a l'origen val $-\psi'(0)\neq0$.
[4] Pel teorema de la funció implícita (amb $r=2$), existeixen entorns oberts $U$ de $(0,0,0)$ i $\Omega$ de $(0,0)$ i una funció $f\in\mathcal{C}^2(\Omega)$ amb $f(0,0)=0$ tals que $\{(x,y,z)\in U: G(x,y,z)=0\}=\{(x,y,f(x,y)):(x,y)\in\Omega\}$.
[5] Així, a prop de l'origen totes les solucions són de la forma $(x,y,f(x,y))$, i com que $f$ és de classe $\mathcal{C}^2$, $f$ és diferenciable a tot $\mathbb{R}^2$.


## t4-22:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Proveu que l'equació $2x^2+y^2+z^3-5xz-2=0$ defineix implícitament $z=g(x,y)$, amb $g$ de classe $C^\infty$, en un entorn de $p=(1,2,1)$. Proveu que el gradient de $g$ en el punt $(1,2)$ val $(-1/2,2)$.
RESULTAT CORRECTE: Amb $G(x,y,z)=2x^2+y^2+z^3-5xz-2$ (polinòmica, $\mathcal{C}^\infty$), $G(1,2,1)=0$ i $\frac{\partial G}{\partial z}(1,2,1)=3-5=-2\neq0$; el teorema de la funció implícita dona $g\in\mathcal{C}^\infty$ amb $g(1,2)=1$. A més $\nabla g(1,2)=-\frac{1}{G_z}(G_x,G_y)=-\frac{1}{-2}(-1,4)=(-1/2,2)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [hipotesis] Hipòtesis del teorema de la funció implícita  (teoria: T4.13, T3.31, T3.21)
     objectiu: Justificar l'existència de $g$ de classe $\mathcal{C}^\infty$ en un entorn de $(1,2)$.
     idea: Comprovar que $p$ és solució, la regularitat de la funció que defineix l'equació i la condició sobre la derivada respecte de $z$. Per a la classe $\mathcal{C}^\infty$, pensar en com depèn la classe de la funció implícita de la de $G$.
     detall: $G(x,y,z)=2x^2+y^2+z^3-5xz-2$ és un polinomi, per tant $\mathcal{C}^r$ per a tot $r$. $G(1,2,1)=2+4+1-5-2=0$. $\frac{\partial G}{\partial z}=3z^2-5x$, i en $p$ val $3-5=-2\neq 0$. Pel teorema de la funció implícita (amb $r=1$) existeixen un obert $\Omega\ni(1,2)$ i $g\in\mathcal{C}^1(\Omega)$ amb $g(1,2)=1$ i $G(x,y,g(x,y))=0$, i $G_z(x,y,g(x,y))\neq0$ en $\Omega$ (apartat (i) del teorema). Per la regla de la cadena, $g_x=-\frac{G_x(x,y,g)}{G_z(x,y,g)}$ i $g_y=-\frac{G_y(x,y,g)}{G_z(x,y,g)}$ en $\Omega$; si $g\in\mathcal{C}^k$, el segon membre és $\mathcal{C}^k$ i per tant $g\in\mathcal{C}^{k+1}$. Per inducció, $g\in\mathcal{C}^\infty(\Omega)$. (Les notes ho abreugen aplicant directament el teorema amb $r=\infty$.)
  2. [gradient] Calcular el gradient  (teoria: T4.15, T3.21)
     objectiu: Calcular $\nabla g(1,2)$.
     idea: Derivar $G(x,y,g(x,y))=0$ respecte de $x$ i de $y$ amb la regla de la cadena, o usar la fórmula de la diferencial de la funció implícita.
     detall: $\frac{\partial G}{\partial x}=4x-5z$, que en $p$ val $-1$; $\frac{\partial G}{\partial y}=2y$, que val $4$. Llavors $g_x(1,2)=-\frac{G_x}{G_z}=-\frac{-1}{-2}=-\frac12$ i $g_y(1,2)=-\frac{G_y}{G_z}=-\frac{4}{-2}=2$. Per tant $\nabla g(1,2)=(-1/2,2)$.
ERRORS COMUNS:
  - [signe_formula] Oblida el signe menys de $g_x=-G_x/G_z$ o fa el quocient al revés.
  - [cinf_sense_justificar] Afirma que $g$ és $\mathcal{C}^\infty$ sense lligar-ho amb la regularitat de $G$.
  - [derivada_z_xz] En derivar respecte de $z$ oblida el terme $-5x$ del producte $-5xz$.

TEORIA DEL CURS QUE FA SERVIR:
[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$

[T3.31] Definició 31 (Tema 3) — Classes C^r de funcions
Direm que $f\in\mathcal{C}^0(\Omega)\Leftrightarrow f$ és contínua a $\Omega$.

$f\in\mathcal{C}^1(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ a tot punt de $\Omega$ i totes són contínues (per tant, en particular, $f$ és diferenciable i contínua).

$f\in\mathcal{C}^2(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ d'ordre $2$:
$$\frac{\partial^2f}{\partial x_i\partial x_j}=\frac{\partial}{\partial x_j}\left(\frac{\partial f}{\partial x_i}\right),$$
a tot punt de $\Omega$ i són contínues.

En general, per a $r\geq1$, es diu que $f\in\mathcal{C}^r(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials d'ordre $r$ a $\Omega$ i totes són contínues. Clarament, $f\in\mathcal{C}^{r+1}(\Omega)\Rightarrow f\in\mathcal{C}^r(\Omega)$.

Direm que $f\in\mathcal{C}^\infty(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials a qualsevol ordre de $f$ a $\Omega$ i totes són contínues.

[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$

[T4.15] Observació 15 (Tema 4) — Diferencial de la funció implícita
$D\varphi(a)$ es pot calcular aplicant la regla de la cadena a l'equació $\Phi(x,\varphi(x))=0$ en un entorn de $(a,b)$:
$$\frac{\partial\Phi}{\partial x}(a,b)+\frac{\partial\Phi}{\partial y}(a,b)\cdot\frac{\partial\varphi}{\partial x}(a)=0.$$

A l'enunciat de l'observació hem mantingut la notació en derivades parcials, però cal tenir en compte que $\dfrac{\partial\varphi}{\partial x}(a)$ és simplement $D\varphi(a)$.
</solucio_de_referencia>

### Document a revisar

[1] Sigui $G(x,y,z)=2x^2+y^2+z^3-5xz-2$. Com que és polinòmica, és de classe $\mathcal{C}^1$, i $G(1,2,1)=2+4+1-5-2=0$.
[2] $\frac{\partial G}{\partial z}=3z^2-5x$, que en $p=(1,2,1)$ val $3-5=-2\neq0$.
[3] Pel teorema de la funció implícita aplicat a $G\in\mathcal{C}^1$, existeixen un obert $\Omega\ni(1,2)$ i $g:\Omega\to\mathbb{R}$ de classe $\mathcal{C}^\infty$ amb $g(1,2)=1$ i $G(x,y,g(x,y))=0$ per a tot $(x,y)\in\Omega$.
[4] Derivant aquesta identitat respecte de $x$ i de $y$ amb la regla de la cadena: $G_x+G_z\,g_x=0$ i $G_y+G_z\,g_y=0$, amb $G_x,G_y,G_z$ avaluades a $(x,y,g(x,y))$. Al punt, com que $G_z(p)\neq0$, $g_x(1,2)=-\frac{G_x(p)}{G_z(p)}$ i $g_y(1,2)=-\frac{G_y(p)}{G_z(p)}$.
[5] $\frac{\partial G}{\partial x}=4x-5$, que en $p$ val $-1$, i $\frac{\partial G}{\partial y}=2y$, que en $p$ val $4$.
[6] Per tant $g_x(1,2)=-\frac{-1}{-2}=-\frac12$ i $g_y(1,2)=-\frac{4}{-2}=2$, és a dir, $\nabla g(1,2)=(-1/2,2)$.


## t4-23a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $F:\mathbb{R}^3\to\mathbb{R}$ de classe $\mathcal{C}^1$ tal que per a tot punt $p$ on $F(p)=0$ se satisfà $\frac{\partial F}{\partial x}(p)\neq 0$, $\frac{\partial F}{\partial y}(p)\neq 0$ i $\frac{\partial F}{\partial z}(p)\neq 0$.

(a) Proveu que si $F(p)=0$, aleshores en un entorn de $p$ es pot escriure cadascuna de les variables $x,y,z$ en termes de les altres dues; és a dir, existeixen funcions $X,Y,Z$ diferenciables tals que $F(X(y,z),y,z)=0$, $F(x,Y(x,z),z)=0$ i $F(x,y,Z(x,y))=0$.
RESULTAT CORRECTE: Sigui $p=(p_1,p_2,p_3)$ amb $F(p)=0$. Com que $F\in\mathcal{C}^1$ i $\frac{\partial F}{\partial z}(p)\neq0$, el teorema de la funció implícita (amb $z$ com a variable a aïllar) dona $Z$ de classe $\mathcal{C}^1$ (per tant diferenciable) en un entorn de $(p_1,p_2)$ amb $Z(p_1,p_2)=p_3$ i $F(x,y,Z(x,y))=0$. Igualment, amb $\frac{\partial F}{\partial x}(p)\neq0$ s'obté $X(y,z)$ i amb $\frac{\partial F}{\partial y}(p)\neq0$ s'obté $Y(x,z)$ (reordenant les variables).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [aillar_z] Aïllar una variable  (teoria: T4.13, T3.31)
     objectiu: Obtenir $Z(x,y)$ diferenciable amb $F(x,y,Z(x,y))=0$ prop de $p$.
     idea: Aplicar el teorema de la funció implícita amb $n=2$, $m=1$, prenent com a variable "dependent" la que es vol aïllar.
     detall: $F\in\mathcal{C}^1$, $F(p)=0$ i $\frac{\partial F}{\partial z}(p)\neq0$ (el determinant $1\times1$ del teorema). Per tant existeix $Z\in\mathcal{C}^1$ en un entorn de $(p_1,p_2)$, amb $Z(p_1,p_2)=p_3$ i $F(x,y,Z(x,y))=0$. Com que és $\mathcal{C}^1$, és diferenciable.
  2. [altres_variables] Les altres dues variables  (teoria: T4.13)
     objectiu: Obtenir també $X(y,z)$ i $Y(x,z)$.
     idea: El teorema no depèn de quines variables posem al final: reordenar les variables (o aplicar-lo a $F$ composta amb una permutació de coordenades) i usar les altres dues hipòtesis.
     detall: Considerant $\tilde F(y,z,x)=F(x,y,z)$, que és $\mathcal{C}^1$ i té $\frac{\partial\tilde F}{\partial x}=\frac{\partial F}{\partial x}(p)\neq0$, s'obté $X\in\mathcal{C}^1$ prop de $(p_2,p_3)$ amb $X(p_2,p_3)=p_1$ i $F(X(y,z),y,z)=0$. Anàlogament, amb $\frac{\partial F}{\partial y}(p)\neq0$, $Y\in\mathcal{C}^1$ prop de $(p_1,p_3)$ amb $Y(p_1,p_3)=p_2$ i $F(x,Y(x,z),z)=0$.
ERRORS COMUNS:
  - [global_vs_local] Pensa que les funcions $X,Y,Z$ estan definides globalment, no només en un entorn.
  - [diferenciable_sense_justificar] Obté les funcions implícites però no justifica que siguin diferenciables.

TEORIA DEL CURS QUE FA SERVIR:
[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T3.20] Definició 20 (Tema 3) — Funció de classe C^1
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $\Omega$ obert. Direm que $f$ és de classe $\mathcal{C}^1(\Omega)$ si $f$ és diferenciable a $\Omega$ i, per a tot punt $a\in\Omega$, existeixen totes les derivades parcials de $f$ al punt $a$ i hi són contínues. De manera anàloga a definicions anteriors, direm que $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $f=(f_1,f_2,\ldots,f_m)$, és de classe $\mathcal{C}^1(\Omega)$ si $f_i\in\mathcal{C}^1(\Omega)$, per a tot $i=1,2,\ldots,m$.

[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]

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

[1] Sigui $p=(p_1,p_2,p_3)$ amb $F(p)=0$. Per hipòtesi, $F$ és de classe $\mathcal{C}^1$ i les tres derivades parcials de $F$ són no nul·les en $p$.
[2] Com que $\frac{\partial F}{\partial z}(p)\neq0$ (és el determinant $1\times1$ que demana el teorema), el teorema de la funció implícita dona una funció $Z$ de classe $\mathcal{C}^1$ definida a tot $\mathbb{R}^2$, amb $Z(p_1,p_2)=p_3$ i $F(x,y,Z(x,y))=0$.
[3] Per aïllar $x$, considerem $\tilde F(y,z,x)=F(x,y,z)$, que també és de classe $\mathcal{C}^1$, i apliquem el teorema prenent $x$ com a variable a aïllar. Com que $\frac{\partial F}{\partial y}(p)\neq0$, existeix $X$ de classe $\mathcal{C}^1$ en un entorn de $(p_2,p_3)$ amb $X(p_2,p_3)=p_1$ i $F(X(y,z),y,z)=0$.
[4] Anàlogament, com que $\frac{\partial F}{\partial y}(p)\neq0$, existeix $Y$ de classe $\mathcal{C}^1$ en un entorn de $(p_1,p_3)$ amb $Y(p_1,p_3)=p_2$ i $F(x,Y(x,z),z)=0$.
[5] Les funcions $X,Y,Z$ són de classe $\mathcal{C}^1$ i, per tant, diferenciables. Així, en un entorn de $p$ cadascuna de les variables $x,y,z$ s'escriu en funció de les altres dues.


## t4-24a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem el sistema d'equacions
$$\left.\begin{aligned}tx^3+xy^2+y-\tfrac{25}{4}t^3&=0\\ 3xy+t^2y^3-3x^2(t+1)-t+3&=0\end{aligned}\right\}$$

(a) Al voltant de quins punts solució del sistema, de la forma $(x,y,t)=(1,0,t_0)$, el sistema defineix localment $x,y$ com a funcions derivables de $t$?

Considerem $\gamma(t)=(x(t),y(t))$, on les funcions $x(t),y(t)$ venen definides localment per l'anterior sistema d'equacions. A $\gamma$ se l'anomena corba parametritzada.
RESULTAT CORRECTE: L'únic punt solució de la forma $(1,0,t_0)$ és $(1,0,0)$, i en ell el determinant de la jacobiana respecte de $(x,y)$ val $6\neq0$: el sistema defineix $x(t),y(t)$ de classe $\mathcal{C}^\infty$ en un entorn de $t=0$, amb $x(0)=1$, $y(0)=0$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [punts_solucio] Trobar els punts solució
     objectiu: Determinar per a quins $t_0$ el punt $(1,0,t_0)$ és solució del sistema.
     idea: Substituir $x=1$, $y=0$ a les dues equacions i imposar que s'anul·lin les dues alhora.
     detall: Primera equació: $t_0-\frac{25}{4}t_0^3=0$, amb solucions $t_0\in\{0,\pm\frac25\}$. Segona: $-3(t_0+1)-t_0+3=-4t_0=0$, és a dir $t_0=0$. L'únic punt solució és $(1,0,0)$.
  2. [jacobiana] Hipòtesi del teorema de la funció implícita  (teoria: T4.13)
     objectiu: Decidir si en el punt trobat es pot aplicar el teorema per aïllar $(x,y)$ en funció de $t$.
     idea: Calcular la submatriu jacobiana respecte de les variables que es volen aïllar, avaluar-la i mirar-ne el determinant.
     detall: Amb $\Phi_1=tx^3+xy^2+y-\frac{25}{4}t^3$, $\Phi_2=3xy+t^2y^3-3x^2(t+1)-t+3$ (polinòmiques, $\mathcal{C}^\infty$): $\frac{\partial(\Phi_1,\Phi_2)}{\partial(x,y)}=\begin{pmatrix}3tx^2+y^2 & 2xy+1\\ 3y-6x(t+1) & 3x+3t^2y^2\end{pmatrix}$, que en $(1,0,0)$ és $\begin{pmatrix}0&1\\-6&3\end{pmatrix}$, amb determinant $0\cdot3-1\cdot(-6)=6\neq0$. Pel teorema de la funció implícita, $x(t),y(t)$ existeixen i són $\mathcal{C}^\infty$ (en particular derivables) en un entorn de $t=0$.
ERRORS COMUNS:
  - [nomes_una_equacio] Imposa només la primera equació i dona també $t_0=\pm\frac25$ com a punts vàlids.
  - [jacobiana_variables] Calcula el determinant amb columnes equivocades (inclou la derivada respecte de $t$) o la jacobiana completa $2\times3$.

TEORIA DEL CURS QUE FA SERVIR:
[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]
</solucio_de_referencia>

### Document a revisar

[1] Substituint $(x,y,t)=(1,0,t_0)$ a la primera equació: $t_0+0+0-\frac{25}{4}t_0^3=t_0\left(1-\frac{25}{4}t_0^2\right)=0$, d'on $t_0\in\{0,\pm\frac52\}$.
[2] A la segona equació: $0+0-3(t_0+1)-t_0+3=-4t_0=0$, és a dir, $t_0=0$. Per tant, l'únic punt solució de la forma $(1,0,t_0)$ és $(1,0,0)$.
[3] Siguin $\Phi_1=tx^3+xy^2+y-\frac{25}{4}t^3$ i $\Phi_2=3xy+t^2y^3-3x^2(t+1)-t+3$, polinòmiques i per tant de classe $\mathcal{C}^\infty$. Com que volem aïllar $x$ i $y$, calculem $\frac{\partial(\Phi_1,\Phi_2)}{\partial(x,y)}=\begin{pmatrix}3tx^2+y^2&2xy+1\\ 3y-6x&3x+3t^2y^2\end{pmatrix}$.
[4] En $(1,0,0)$ aquesta matriu val $\begin{pmatrix}0&1\\-6&3\end{pmatrix}$, amb determinant $0\cdot3-1\cdot(-6)=6\neq0$.
[5] Pel teorema de la funció implícita, existeixen un interval obert $I\ni0$ i funcions $x(t),y(t)$ de classe $\mathcal{C}^\infty$ (en particular derivables) en $I$, amb $x(0)=1$ i $y(0)=0$, que satisfan el sistema.
[6] Per tant, l'únic punt de la forma $(1,0,t_0)$ al voltant del qual el sistema defineix $x,y$ com a funcions derivables de $t$ és $(1,0,0)$.


## t4-25:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Determineu si la corba definida en forma implícita per $x^2+y+\cos(xy)=1$ es pot escriure de la forma $y=g(x)$ en un entorn de l'origen. I de la forma $x=h(y)$?
RESULTAT CORRECTE: Sí de la forma $y=g(x)$ (amb $g\in\mathcal{C}^\infty$, $g(0)=0$), perquè $\frac{\partial F}{\partial y}(0,0)=1\neq0$ per a $F=x^2+y+\cos(xy)-1$. No de la forma $x=h(y)$: per a $0<y<\sqrt2$ no hi ha cap punt de la corba amb aquesta ordenada (de $1-\cos u\le u^2/2$ surt $y\le x^2(y^2/2-1)\le 0$), de manera que cap $h$ pot estar definida en un entorn de $y=0$; a més, per a $y<0$ petit hi ha dos punts $(\pm x,y)$ de la corba.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [y_de_x] Forma y=g(x)  (teoria: T4.13)
     objectiu: Decidir si la corba es pot escriure com $y=g(x)$ prop de l'origen.
     idea: Escriure la corba com $F(x,y)=0$, comprovar que l'origen hi és i la hipòtesi del teorema de la funció implícita per aïllar $y$.
     detall: $F(x,y)=x^2+y+\cos(xy)-1$, de classe $\mathcal{C}^\infty$, $F(0,0)=0$. $\frac{\partial F}{\partial y}=1-x\sin(xy)$, que en $(0,0)$ val $1\neq0$. Pel teorema de la funció implícita existeix $g\in\mathcal{C}^\infty$ en un entorn de $0$, $g(0)=0$, i prop de l'origen la corba és exactament la gràfica de $g$.
  2. [x_de_y_tfi] El teorema no decideix x=h(y)  (teoria: T4.13)
     objectiu: Veure si el teorema de la funció implícita permet aïllar $x$.
     idea: Comprovar la hipòtesi del teorema respecte de $x$ i recordar que és una condició suficient, no necessària.
     detall: $\frac{\partial F}{\partial x}=2x-y\sin(xy)$, i $\frac{\partial F}{\partial x}(0,0)=0$. El teorema no s'aplica; cal estudiar la corba directament.
  3. [x_de_y_directe] Estudi directe
     objectiu: Decidir si existeix alguna $h$ definida en un entorn de $y=0$ amb $x=h(y)$ descrivint la corba prop de l'origen.
     idea: Mirar quin signe pot tenir $y$ en els punts de la corba propers a l'origen. Una fita útil d'una variable: $1-\cos u\le \frac{u^2}{2}$ per a tot $u$ (no és a les notes, és de Càlcul d'una variable).
     detall: A la corba, $y=1-\cos(xy)-x^2\le\frac{x^2y^2}{2}-x^2=x^2\left(\frac{y^2}{2}-1\right)$. Si $|y|<\sqrt2$, el segon membre és $\le0$, per tant tot punt de la corba amb $|y|<\sqrt2$ té $y\le0$. Així, per a $0<y<\sqrt2$ no hi ha cap $x$ amb $(x,y)$ a la corba, i no pot existir $h$ definida en un entorn de $0$. (A més, $F(-x,y)=F(x,y)$: per a $y<0$ petit els punts són parells $(\pm x,y)$, i tampoc hi hauria unicitat.) Coherentment, $g'(0)=0$ i $g''(0)=-2$: la corba és com la paràbola $y=-x^2$.
ERRORS COMUNS:
  - [tfi_necessaria] Conclou que no es pot escriure $x$ en funció de $y$ només perquè $\partial F/\partial x(0,0)=0$.
  - [confondre_variables] Comprova la derivada respecte de $x$ per a la forma $y=g(x)$ (intercanvia els papers).
  - [argument_camins] Argumenta amb dibuixos o aproximacions ($y\approx-x^2$) sense una justificació rigorosa que per a $y>0$ no hi ha solucions.

TEORIA DEL CURS QUE FA SERVIR:
[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]
</solucio_de_referencia>

### Document a revisar

[1] Sigui $F(x,y)=x^2+y+\cos(xy)-1$, de classe $\mathcal{C}^\infty$, amb $F(0,0)=0+0+1-1=0$. Tenim $\frac{\partial F}{\partial y}=1-x\sin(xy)$, que en $(0,0)$ val $1\neq0$.
[2] Pel teorema de la funció implícita existeix $g$ de classe $\mathcal{C}^\infty$ en un interval obert que conté $0$, amb $g(0)=0$, tal que prop de l'origen la corba és exactament la gràfica de $g$. Per tant, sí que es pot escriure $y=g(x)$.
[3] Per a la forma $x=h(y)$: $\frac{\partial F}{\partial x}=2x+y\sin(xy)$, que en $(0,0)$ val $0$. El teorema de la funció implícita no s'aplica, i cal estudiar la corba directament.
[4] Com que $1-\cos s\le\frac{s^2}{2}$ per a tot $s\in\mathbb{R}$, sobre la corba tenim $y=1-\cos(xy)-x^2\le\frac{x^2y^2}{2}-x^2=x^2\left(\frac{y^2}{2}-1\right)$.
[5] Si $|y|<2$, el factor $\frac{y^2}{2}-1$ és negatiu, i per tant el segon membre és $\le0$. Així, tot punt de la corba amb $|y|<2$ té $y\le0$, i per a $0<y<2$ no hi ha cap punt de la corba amb ordenada $y$.
[6] Si existís $h$ definida en un interval $(-\delta,\delta)$ amb $F(h(y),y)=0$ per a tot $y$, per a $0<y<\delta$ el punt $(h(y),y)$ seria un punt de la corba amb ordenada positiva i petita, cosa impossible.
[7] Conclusió: prop de l'origen la corba es pot escriure de la forma $y=g(x)$, però no de la forma $x=h(y)$.


## t4-26:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Demostreu que existeix un entorn obert $U\subseteq\mathbb{R}$ de $-1$ i funcions $u,v:U\to\mathbb{R}$ de classe $\mathcal{C}^1$ tals que $u(-1)=v(-1)=1$ i
$$\left.\begin{aligned}xe^{u(x)}+u(x)e^{v(x)}&=0\\ xe^{v(x)}+v(x)e^{u(x)}&=0\end{aligned}\right\}$$
RESULTAT CORRECTE: Sigui $\Phi(x,u,v)=(xe^u+ue^v,\,xe^v+ve^u)$, de classe $\mathcal{C}^\infty$, amb $\Phi(-1,1,1)=(0,0)$ i $\det\frac{\partial\Phi}{\partial(u,v)}(-1,1,1)=\det\begin{pmatrix}0&e\\e&0\end{pmatrix}=-e^2\neq0$. Pel teorema de la funció implícita existeixen un entorn obert $U$ de $-1$ i $(u,v):U\to\mathbb{R}^2$ de classe $\mathcal{C}^\infty$ (en particular $\mathcal{C}^1$) amb $u(-1)=v(-1)=1$ i $\Phi(x,u(x),v(x))=0$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [plantejar] Plantejar el sistema com Φ=0  (teoria: T3.31)
     objectiu: Escriure el problema en el llenguatge del teorema de la funció implícita i comprovar que el punt de partida és solució.
     idea: Definir $\Phi:\mathbb{R}^3\to\mathbb{R}^2$ amb variables $(x,u,v)$, on $x$ és la independent, i avaluar-la en el punt que dicten les condicions inicials.
     detall: $\Phi(x,u,v)=(xe^u+ue^v,\,xe^v+ve^u)$ és $\mathcal{C}^\infty$ (sumes i productes d'exponencials i polinomis). $\Phi(-1,1,1)=(-e+e,-e+e)=(0,0)$.
  2. [jacobiana] Determinant respecte de (u,v)  (teoria: T4.13)
     objectiu: Comprovar la hipòtesi del teorema que permet aïllar $(u,v)$ en funció de $x$, i concloure.
     idea: Calcular la matriu de derivades parcials de $\Phi$ respecte de $u$ i $v$ en el punt i el seu determinant.
     detall: $\frac{\partial\Phi}{\partial(u,v)}=\begin{pmatrix}xe^u+e^v & ue^v\\ ve^u & xe^v+e^u\end{pmatrix}$, que en $(-1,1,1)$ és $\begin{pmatrix}0&e\\e&0\end{pmatrix}$, amb determinant $-e^2\neq0$. El teorema de la funció implícita dona un obert $U\ni-1$ i $(u,v)\in\mathcal{C}^\infty(U)\subseteq\mathcal{C}^1(U)$ amb $(u,v)(-1)=(1,1)$ i que satisfan el sistema per a tot $x\in U$.
ERRORS COMUNS:
  - [derivar_respecte_x] Calcula el determinant respecte de variables equivocades (inclou $x$) o pren la jacobiana $2\times3$ completa.
  - [oblidar_derivar_productes] En derivar $ue^v$ respecte de $u$ oblida un dels termes, o respecte de $v$ oblida el factor $u$.

TEORIA DEL CURS QUE FA SERVIR:
[T3.31] Definició 31 (Tema 3) — Classes C^r de funcions
Direm que $f\in\mathcal{C}^0(\Omega)\Leftrightarrow f$ és contínua a $\Omega$.

$f\in\mathcal{C}^1(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ a tot punt de $\Omega$ i totes són contínues (per tant, en particular, $f$ és diferenciable i contínua).

$f\in\mathcal{C}^2(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ d'ordre $2$:
$$\frac{\partial^2f}{\partial x_i\partial x_j}=\frac{\partial}{\partial x_j}\left(\frac{\partial f}{\partial x_i}\right),$$
a tot punt de $\Omega$ i són contínues.

En general, per a $r\geq1$, es diu que $f\in\mathcal{C}^r(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials d'ordre $r$ a $\Omega$ i totes són contínues. Clarament, $f\in\mathcal{C}^{r+1}(\Omega)\Rightarrow f\in\mathcal{C}^r(\Omega)$.

Direm que $f\in\mathcal{C}^\infty(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials a qualsevol ordre de $f$ a $\Omega$ i totes són contínues.

[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]
</solucio_de_referencia>

### Document a revisar

[1] Sigui $\Phi(x,u,v)=(xe^u+ue^v,\,xe^v+ve^u)$, de classe $\mathcal{C}^\infty$ a $\mathbb{R}^3$ perquè és suma i producte de polinomis i exponencials. Volem veure que $\Phi(x,u,v)=(0,0)$ defineix $u,v$ com a funcions de $x$ a prop de $x=-1$.
[2] El punt $(-1,1,1)$ és solució: $\Phi(-1,1,1)=(-e+e,\,-e+e)=(0,0)$.
[3] Derivant respecte de $u$ i de $v$: $\frac{\partial\Phi}{\partial(u,v)}=\begin{pmatrix}xe^u+e^v&e^v\\ ve^u&xe^v+e^u\end{pmatrix}$.
[4] En $(-1,1,1)$ aquesta matriu val $\begin{pmatrix}0&e\\e&0\end{pmatrix}$, de determinant $-e^2\neq0$.
[5] Com que $\Phi$ és contínua, s'anul·la en $(-1,1,1)$ i el determinant anterior és no nul, el teorema de la funció implícita dona un entorn obert $U$ de $-1$ i funcions $u,v:U\to\mathbb{R}$, amb $u(-1)=v(-1)=1$, que satisfan el sistema per a tot $x\in U$.
[6] A més, el teorema dona $u,v$ de la mateixa classe que $\Phi$, és a dir $\mathcal{C}^\infty$, i en particular de classe $\mathcal{C}^1$, com es demanava.


## t4-28a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considereu $F:U\subseteq\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^1$ i $p\in U$ tal que $F(p)=0$. Suposem que, en un entorn de $p$, l'equació $F(x,y)=0$ defineix localment $y$ com a funció implícita de $x$, $y=g(x)$. Demostreu que, si $\frac{\partial F}{\partial x}(p)\neq 0$ i $\frac{\partial F}{\partial y}(p)=0$, llavors $g$ no és de classe $\mathcal{C}^1$.
RESULTAT CORRECTE: Sigui $p=(x_0,y_0)$. Si $g$ fos $\mathcal{C}^1$ (en particular derivable en $x_0$), derivant $F(x,g(x))=0$ amb la regla de la cadena en $x_0$ s'obtindria $\frac{\partial F}{\partial x}(p)+\frac{\partial F}{\partial y}(p)\,g'(x_0)=0$, és a dir $\frac{\partial F}{\partial x}(p)=0$, contradicció. Per tant $g$ no és $\mathcal{C}^1$ (de fet, ni tan sols derivable en $x_0$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [suposar] Plantejar per reducció a l'absurd
     objectiu: Escriure què es té si se suposa que $g$ és $\mathcal{C}^1$.
     idea: Suposar el contrari i escriure la identitat que satisfà $g$ en un entorn de $x_0$, on $p=(x_0,y_0)$.
     detall: Suposem $g\in\mathcal{C}^1$ en un entorn de $x_0$, amb $g(x_0)=y_0$ i $F(x,g(x))=0$ per a tot $x$ d'aquest entorn.
  2. [derivar] Derivar la identitat i arribar a contradicció  (teoria: T3.21, T3.18)
     objectiu: Obtenir una contradicció amb les hipòtesis sobre les derivades parcials de $F$.
     idea: Derivar la identitat amb la regla de la cadena (cal que $F$ sigui diferenciable i $g$ derivable) i avaluar en $x_0$.
     detall: $F$ és $\mathcal{C}^1$, per tant diferenciable, i $x\mapsto(x,g(x))$ és derivable. Per la regla de la cadena, $0=\frac{d}{dx}F(x,g(x))\big|_{x_0}=\frac{\partial F}{\partial x}(p)+\frac{\partial F}{\partial y}(p)g'(x_0)=\frac{\partial F}{\partial x}(p)$, que contradiu $\frac{\partial F}{\partial x}(p)\neq0$.
ERRORS COMUNS:
  - [aplicar_formula] Escriu $g'=-F_x/F_y$ i diu que "divideix per zero", sense justificar d'on surt la fórmula ni que sigui aplicable.
  - [invoca_tfi] Diu que el teorema de la funció implícita "no s'aplica" i per tant $g$ no és $\mathcal{C}^1$.

TEORIA DEL CURS QUE FA SERVIR:
[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

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

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.
</solucio_de_referencia>

### Document a revisar

[1] Sigui $p=(x_0,y_0)$. Raonem per reducció a l'absurd: suposem que $g$ és de classe $\mathcal{C}^1$ en un interval obert $I$ que conté $x_0$, amb $g(x_0)=y_0$ i $F(x,g(x))=0$ per a tot $x\in I$.
[2] Com que $F$ té derivades parcials en $p$, és diferenciable en $p$; a més, $\gamma(x)=(x,g(x))$ és derivable en $x_0$, amb $\gamma(x_0)=p$ i $\gamma'(x_0)=(1,g'(x_0))$.
[3] Per la regla de la cadena, la funció $x\mapsto F(x,g(x))$, que és idènticament nul·la a $I$, té derivada nul·la en $x_0$: $0=\frac{\partial F}{\partial x}(p)+\frac{\partial F}{\partial y}(p)\,g'(x_0)$.
[4] Com que $\frac{\partial F}{\partial y}(p)=0$, queda $\frac{\partial F}{\partial x}(p)=0$, que contradiu la hipòtesi $\frac{\partial F}{\partial x}(p)\neq0$. Per tant, $g$ no és de classe $\mathcal{C}^1$.
[5] De fet, el raonament mostra una mica més: $g$ no pot ser ni tan sols contínua en $x_0$.

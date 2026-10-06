## t5-3:facil

### Referència

<solucio_de_referencia>
ENUNCIAT: Feu servir el polinomi de Taylor de grau 2 de $f(x,y)=e^x+e^y$ a $(0,0)$ per donar un valor aproximat de $f(0.2,-0.1)$. Doneu també una fita superior de l'error comès amb aquesta aproximació.
RESULTAT CORRECTE: $P_2(x,y)=2+x+y+\frac{x^2+y^2}{2}$, de manera que $f(0.2,-0.1)\approx P_2(0.2,-0.1)=2.125$.
Error: $R_3=\frac{1}{6}\left(e^{\xi_1}(0.2)^3+e^{\xi_2}(-0.1)^3\right)$ amb $\xi_1\in(0,0.2)$, $\xi_2\in(-0.1,0)$, i $|R_3|\leq\frac{1}{6}\left(e^{0.2}\cdot 0.008+0.001\right)<\frac{1.25\cdot0.008+0.001}{6}=\frac{0.011}{6}<1.84\cdot10^{-3}$ (n'hi ha prou amb qualsevol fita correcta d'aquest ordre, p. ex. $<2\cdot 10^{-3}$). El valor real és $e^{0.2}+e^{-0.1}\approx 2.12624$ (error real $\approx 1.24\cdot10^{-3}$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [polinomi] Polinomi de grau 2  (teoria: T5.14)
     objectiu: Calcular el polinomi de Taylor de grau $2$ de $f$ a l'origen.
     idea: Calcular les derivades parcials fins a ordre $2$ a l'origen (o sumar els desenvolupaments de $e^x$ i $e^y$).
     detall: $f(0,0)=2$, $D_1f=e^x\to1$, $D_2f=e^y\to1$, $D_{11}f\to1$, $D_{22}f\to1$, $D_{12}f=0$. Per tant $P_2=2+x+y+\frac{x^2}{2}+\frac{y^2}{2}$.
  2. [aproximacio] Valor aproximat
     objectiu: Obtenir el valor aproximat de $f(0.2,-0.1)$.
     idea: Avaluar $P_2$ al punt donat.
     detall: $P_2(0.2,-0.1)=2+0.2-0.1+\frac{0.04+0.01}{2}=2.125$.
  3. [residu] Expressió del residu  (teoria: T5.14)
     objectiu: Escriure exactament l'error $f(0.2,-0.1)-P_2(0.2,-0.1)$.
     idea: Fer servir l'expressió del residu del teorema de Taylor amb derivades d'ordre $3$ avaluades en un punt intermedi del segment entre $(0,0)$ i $(0.2,-0.1)$; observar quines derivades terceres són nul·les.
     detall: Les úniques derivades terceres no nul·les són $D_{111}f=e^x$ i $D_{222}f=e^y$. Per tant $R_3=\frac{1}{3!}\left(e^{\xi_1}(0.2)^3+e^{\xi_2}(-0.1)^3\right)$ amb $(\xi_1,\xi_2)=\tau(0.2,-0.1)$, $\tau\in(0,1)$, és a dir $0<\xi_1<0.2$ i $-0.1<\xi_2<0$.
  4. [fita] Fitar l'error
     objectiu: Donar una fita superior segura de $|R_3|$.
     idea: Fitar cada exponencial pel seu valor màxim possible al segment, amb una fita numèrica que sigui segurament més gran (no un arrodoniment).
     detall: $e^{\xi_1}<e^{0.2}<3^{0.2}<1.25$ (perquè $1.25^5\approx3.05>3>e$) i $e^{\xi_2}<1$. Així $|R_3|\leq\frac{1}{6}(1.25\cdot0.008+0.001)=\frac{0.011}{6}\approx1.83\cdot10^{-3}<2\cdot10^{-3}$.
ERRORS COMUNS:
  - [derivades_a_l_origen] Avalua les derivades terceres del residu a l'origen ($e^0=1$) en lloc de fitar-les al segment, i obté $\frac{0.008-0.001}{6}$ com a "fita".
  - [termes_creuats_residu] Inclou al residu termes amb derivades creuades, o calcula malament el nombre de termes.
  - [fita_no_segura] Fa servir una aproximació de $e^{0.2}$ arrodonida per sota (p. ex. $1.22$) com si fos una fita superior.

TEORIA DEL CURS QUE FA SERVIR:
[T5.14] Teorema 14 (Tema 5) — Teorema de Taylor (diverses variables)
(de Taylor). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^{r+1}(\Omega)$, i $\mathbf{a}\in\Omega$. Per a tot $\mathbf{x}\in\Omega$ amb $[\mathbf{a},\mathbf{x}]\subseteq\Omega$, existeix $\xi_\mathbf{x}\in(\mathbf{a},\mathbf{x})$ tal que $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$, on

(i) El polinomi
$$\begin{aligned}P_r(\mathbf{x})={}&f(\mathbf{a})+\sum_{i=1}^{n}D_if(\mathbf{a})(x_i-a_i)+\frac{1}{2!}\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_i)(x_j-a_j)+\cdots\\
&\cdots+\frac{1}{r!}\sum_{i_1,\ldots,i_r=1}^{n}D_{i_1,\ldots,i_r}f(\mathbf{a})(x_{i_1}-a_{i_1})\cdots(x_{i_r}-a_{i_r})\end{aligned}$$
s'anomena el polinomi de Taylor de grau $r$ de la funció $f$ en el punt $\mathbf{a}$,

(ii) El residu de grau $r$ de la funció $f$ en el punt $\mathbf{a}$ és
$$R_{r+1}(\mathbf{x})=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})(x_{i_1}-a_{i_1})\cdots(x_{i_{r+1}}-a_{i_{r+1}}).$$
A més, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$
</solucio_de_referencia>

### Document a revisar

[1] Calculem les derivades de $f(x,y)=e^x+e^y$ a l'origen: $f(0,0)=2$, $D_1f=e^x$ i $D_2f=e^y$ hi valen $1$, $D_{11}f=e^x$ i $D_{22}f=e^y$ també hi valen $1$, i $D_{12}f=0$ perquè cada sumand depèn d'una sola variable.
[2] Per tant el polinomi de Taylor de grau 2 a l'origen és $P_2(x,y)=2+x+y+\frac{x^2}{2}+\frac{y^2}{2}$.
[3] Avaluant al punt: $P_2(0.2,-0.1)=2+0.2-0.1+\frac{0.04+0.01}{2}=2.1+0.05=2.15$, que és el valor aproximat de $f(0.2,-0.1)$.
[4] Per al residu calen les derivades terceres: les úniques no nul·les són $D_{111}f=e^x$ i $D_{222}f=e^y$. Per la fórmula de Taylor amb residu de Lagrange, $R_3=\frac{1}{3!}\left(e^{\xi_1}(0.2)^3+e^{\xi_2}(-0.1)^3\right)$, on $(\xi_1,\xi_2)=\tau(0.2,-0.1)$ per a algun $\tau\in(0,1)$.
[5] Així $0<\xi_1<0.2$ i $-0.1<\xi_2<0$. Fitem les exponencials: $e^{\xi_1}<e^{0.2}<1.25$, perquè $1.25^5\approx3.05>e$, i $e^{\xi_2}<1$.
[6] Per la desigualtat triangular, $|R_3|\leq\frac{1}{6}\left(1.25\cdot0.008+0.001\right)=\frac{0.011}{6}\approx1.83\cdot10^{-3}<2\cdot10^{-3}$, que és una fita superior de l'error comès.


## t5-4:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $g:\mathbb{R}^2\to\mathbb{R}$ una funció de classe $\mathcal{C}^2(\mathbb{R}^2)$ satisfent $g(0,1)=0$, $Jg(0,1)=(2\ \ -3)$ i
$$Hg(0,1)=\begin{pmatrix}3/4&5/4\\5/4&5/4\end{pmatrix}.$$
Sigui $f:\mathbb{R}\to\mathbb{R}$ una funció de classe $\mathcal{C}^1$ amb $f(0)=1$ i $f'(0)=-1/8$. Calculeu el polinomi de Taylor de grau $\leqslant2$, en el punt $(0,1)$, de la funció
$$F(x,y)=\log\left(1+x^2+xy+y^2\right)+\int_0^{g(x,y)}f(t)\,dt.$$
RESULTAT CORRECTE: $P_2(x,y)=\log 2+\dfrac{5}{2}x-2(y-1)+\dfrac{1}{2}x^2+2x(y-1)+\dfrac{1}{16}(y-1)^2$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [valor] Valor al punt
     objectiu: Calcular $F(0,1)$.
     idea: Avaluar cada sumand; recordar que $g(0,1)=0$.
     detall: $1+0+0+1=2$, i la integral va de $0$ a $g(0,1)=0$, per tant val $0$: $F(0,1)=\log 2$.
  2. [part_log] Taylor del logaritme  (teoria: T5.8, T5.16)
     objectiu: Obtenir el polinomi de Taylor de grau $2$ a $(0,1)$ de $L(x,y)=\log(1+x^2+xy+y^2)$.
     idea: Posar $v=y-1$ i escriure l'argument com $2+w$, amb $w$ un polinomi en $(x,v)$ sense terme constant; després fer servir $\log(2+w)=\log 2+\frac{w}{2}-\frac{w^2}{8}+O(w^3)$ i, per unicitat, truncar a grau $2$. (També es pot fer amb derivades.)
     detall: $1+x^2+x(1+v)+(1+v)^2=2+w$ amb $w=x+2v+x^2+xv+v^2$. Llavors $\frac{w}{2}=\frac{x}{2}+v+\frac{x^2+xv+v^2}{2}$ i $\frac{w^2}{8}=\frac{(x+2v)^2}{8}+O_3=\frac{x^2+4xv+4v^2}{8}+O_3$. Per tant $L=\log2+\frac{x}{2}+(y-1)+\frac{3}{8}x^2+O_3$ (els termes en $xv$ i $v^2$ es cancel·len).
  3. [part_integral] Taylor de la part integral  (teoria: T3.21, T5.32, T5.14)
     objectiu: Obtenir el polinomi de Taylor de grau $2$ a $(0,1)$ de $G(x,y)=\int_0^{g(x,y)}f(t)\,dt$.
     idea: Escriure $G=\Phi\circ g$ amb $\Phi(s)=\int_0^sf(t)\,dt$; pel teorema fonamental del càlcul $\Phi'=f$ i $\Phi''=f'$, així que $\Phi$ és $\mathcal{C}^2$ i $G$ també. Calcular el gradient i la hessiana de $G$ amb la regla de la cadena (i la del producte per a les derivades segones).
     detall: $D_iG=f(g)\,D_ig$, i $D_{ij}G=f'(g)\,D_ig\,D_jg+f(g)\,D_{ij}g$. A $(0,1)$, amb $g=0$: $JG=(2\ \ -3)$ i $HG=-\frac18\begin{pmatrix}4&-6\\-6&9\end{pmatrix}+\begin{pmatrix}3/4&5/4\\5/4&5/4\end{pmatrix}=\begin{pmatrix}1/4&2\\2&1/8\end{pmatrix}$. Per tant el polinomi de $G$ és $2x-3(y-1)+\frac{1}{8}x^2+2x(y-1)+\frac{1}{16}(y-1)^2$.
  4. [sumar] Sumar  (teoria: T5.14)
     objectiu: Obtenir el polinomi de Taylor de grau $\leq 2$ de $F$ a $(0,1)$.
     idea: El polinomi de Taylor d'una suma és la suma dels polinomis de Taylor (les derivades són lineals).
     detall: $P_2=\log2+\left(\frac12+2\right)x+(1-3)(y-1)+\left(\frac38+\frac18\right)x^2+2x(y-1)+\frac{1}{16}(y-1)^2$.
ERRORS COMUNS:
  - [log_mal_centrat] Desenvolupa $\log(1+u)\approx u-\frac{u^2}{2}$ amb $u=x^2+xy+y^2$, que al punt $(0,1)$ val $1$ i no és petit.
  - [cadena_integral] Deriva la integral com si el límit superior fos $x$ o $y$ (oblida el factor $D_ig$), o avalua $f$ a $(x,y)$ en lloc de $g(x,y)$.
  - [hessiana_incompleta] Calcula $HG=f(g)\,Hg$ i oblida el terme $f'(g)\,\nabla g^T\nabla g$ que surt de la regla del producte.
  - [factor_meitat] Oblida el factor $\frac12$ davant de la forma quadràtica hessiana (o el compta dues vegades al terme creuat).

TEORIA DEL CURS QUE FA SERVIR:
[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$

[T5.32] Definició 32 (Tema 5) — Matriu hessiana
Sigui $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$. La matriu (o la forma quadràtica) hessiana de $f$ en un punt $\mathbf{a}\in\Omega$ és $Hf(\mathbf{a})$ (o $q_{Hf(\mathbf{a})}$), on
$$Hf(\mathbf{a})=\begin{pmatrix}D_{1,1}f(\mathbf{a})&\cdots&D_{1,n}f(\mathbf{a})\\\vdots&&\vdots\\D_{n,1}f(\mathbf{a})&\cdots&D_{n,n}f(\mathbf{a})\end{pmatrix}.$$

[T5.14] Teorema 14 (Tema 5) — Teorema de Taylor (diverses variables)
(de Taylor). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^{r+1}(\Omega)$, i $\mathbf{a}\in\Omega$. Per a tot $\mathbf{x}\in\Omega$ amb $[\mathbf{a},\mathbf{x}]\subseteq\Omega$, existeix $\xi_\mathbf{x}\in(\mathbf{a},\mathbf{x})$ tal que $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$, on

(i) El polinomi
$$\begin{aligned}P_r(\mathbf{x})={}&f(\mathbf{a})+\sum_{i=1}^{n}D_if(\mathbf{a})(x_i-a_i)+\frac{1}{2!}\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_i)(x_j-a_j)+\cdots\\
&\cdots+\frac{1}{r!}\sum_{i_1,\ldots,i_r=1}^{n}D_{i_1,\ldots,i_r}f(\mathbf{a})(x_{i_1}-a_{i_1})\cdots(x_{i_r}-a_{i_r})\end{aligned}$$
s'anomena el polinomi de Taylor de grau $r$ de la funció $f$ en el punt $\mathbf{a}$,

(ii) El residu de grau $r$ de la funció $f$ en el punt $\mathbf{a}$ és
$$R_{r+1}(\mathbf{x})=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})(x_{i_1}-a_{i_1})\cdots(x_{i_{r+1}}-a_{i_{r+1}}).$$
A més, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$

[T5.8] Teorema 8 (Tema 5) — Teorema de Taylor (una variable)
(de Taylor). Sigui $\Omega\subseteq\mathbb{R}$ obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^{r+1}(\Omega)$, i $a\in\Omega$. Per a tot $x\in\Omega$ amb $[a,x]\subseteq\Omega$ (Nota: Fem servir la notació d'intervals a $\mathbb{R}^n$ introduïda al tema 3, de manera que, a $\mathbb{R}$, $[a,x]$ pot ser tant $[a,x]$, si $x\geq a$, com $[x,a]$, si $x\leq a$.), existeix $\xi_x\in(a,x)$ tal que $f(x)=P_r(x)+R_{r+1}(x)$, on

(i) $P_r(x)=f(a)+f'(a)(x-a)+\dfrac{1}{2!}f''(a)(x-a)^2+\cdots+\dfrac{1}{r!}f^{(r)}(a)(x-a)^r$ s'anomena el polinomi de Taylor de grau $r$ de la funció $f$ en el punt $a$, i

(ii) $R_{r+1}(x)=\dfrac{1}{(r+1)!}f^{(r+1)}(\xi_x)(x-a)^{r+1}$ s'anomena el residu de grau $r$ de la funció $f$ en el punt $a$. A més,
$$\lim_{x\to a}\frac{R_{r+1}(x)}{(x-a)^r}=0.$$

[T5.16] Observació 16 (Tema 5) — Unicitat del polinomi de Taylor
Per a una funció $f\in\mathcal{C}^{r+1}(\Omega)$, el seu polinomi de Taylor de grau $r$, $P_r(\mathbf{x})$, és l'únic polinomi de grau $\leqslant r$ que compleix $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-P_r(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$
</solucio_de_referencia>

### Document a revisar

[1] Escrivim $F=L+G$, amb $L(x,y)=\log(1+x^2+xy+y^2)$ i $G(x,y)=\int_0^{g(x,y)}f(t)\,dt$. Al punt $(0,1)$ l'argument del logaritme val $1+0+0+1=2$ i la integral va de $0$ a $g(0,1)=0$, de manera que $F(0,1)=\log2$.
[2] Per a $L$ posem $v=y-1$: $1+x^2+x(1+v)+(1+v)^2=2+w$ amb $w=x+2v+x^2+xv+v^2$, i $\log(2+w)=\log2+\log\left(1+\frac{w}{2}\right)=\log2+\frac{w}{2}-\frac{w^2}{8}+O_3$.
[3] Com que $\frac{w}{2}=\frac{x}{2}+v+\frac{x^2+xv+v^2}{2}$ i $\frac{w^2}{8}=\frac{x^2+4xv+4v^2}{8}+O_3$, els termes en $xv$ i en $v^2$ es cancel·len i el de $x^2$ queda $\left(\frac12+\frac18\right)x^2=\frac58x^2$. Així $L=\log2+\frac{x}{2}+(y-1)+\frac58x^2+O_3$.
[4] Per a $G$, pel teorema fonamental del càlcul i la regla de la cadena, $D_iG=f(g)\,D_ig$; derivant de nou amb la regla del producte, $D_{ij}G=f'(g)\,D_ig\,D_jg+f(g)\,D_{ij}g$.
[5] A $(0,1)$ tenim $g=0$, $f(0)=1$ i $f'(0)=-\frac18$, així que $JG(0,1)=(2\ \ -3)$ i $HG(0,1)=-\frac18\begin{pmatrix}4&-6\\-6&9\end{pmatrix}+\begin{pmatrix}3/4&5/4\\5/4&5/4\end{pmatrix}=\begin{pmatrix}1/4&2\\2&1/8\end{pmatrix}$.
[6] El polinomi de grau 2 de $G$ és doncs $2x-3(y-1)+\frac12\left(\frac14x^2+2x(y-1)+\frac18(y-1)^2\right)=2x-3(y-1)+\frac18x^2+x(y-1)+\frac{1}{16}(y-1)^2$.
[7] Sumant les dues parts: $P_2(x,y)=\log2+\left(\frac12+2\right)x+(1-3)(y-1)+\left(\frac58+\frac18\right)x^2+x(y-1)+\frac{1}{16}(y-1)^2=\log2+\frac52x-2(y-1)+\frac34x^2+x(y-1)+\frac{1}{16}(y-1)^2$.


## t5-5a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Trobeu i classifiqueu tots els punts crítics de les funcions següents:

(a) $f(x,y)=x^4+y^4-2y^2+4xy-2x^2$;
RESULTAT CORRECTE: Punts crítics: $(0,0)$, $(\sqrt2,-\sqrt2)$ i $(-\sqrt2,\sqrt2)$.
Els punts $(\sqrt2,-\sqrt2)$ i $(-\sqrt2,\sqrt2)$ són mínims locals estrictes (hessiana definida positiva); de fet són mínims absoluts, amb $f=-8$.
L'origen $(0,0)$ és un punt de sella: la hessiana hi és degenerada, però $f(x,0)=x^4-2x^2<0$ per $0<|x|<\sqrt2$ i $f(x,x)=2x^4>0$ per $x\neq0$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [punts_critics] Trobar els punts crítics  (teoria: T5.22)
     objectiu: Trobar tots els punts on s'anul·len les dues derivades parcials de $f$.
     idea: Plantejar el sistema $f_x=0$, $f_y=0$. Combinar les dues equacions per eliminar els termes lineals i obtenir una relació senzilla entre $x$ i $y$; després substituir.
     detall: $f_x=4x^3-4x+4y$, $f_y=4y^3-4y+4x$. Sumant les dues equacions: $4(x^3+y^3)=0$, i com que $x^3+y^3=(x+y)(x^2-xy+y^2)$ i el segon factor només s'anul·la a l'origen, queda $y=-x$. Substituint a $f_x=0$: $4x^3-8x=0$, és a dir $x=0$ o $x=\pm\sqrt2$. Punts crítics: $(0,0)$, $(\sqrt2,-\sqrt2)$, $(-\sqrt2,\sqrt2)$.
  2. [hessiana] Calcular la hessiana als punts crítics  (teoria: T5.32, T5.6)
     objectiu: Obtenir la matriu hessiana de $f$ i avaluar-la a cada punt crític.
     idea: $f$ és polinòmica, per tant $\mathcal{C}^\infty$ i les derivades creuades coincideixen. Calcular les derivades segones i substituir cada punt.
     detall: $Hf(x,y)=\begin{pmatrix}12x^2-4&4\\4&12y^2-4\end{pmatrix}$.
A $(\pm\sqrt2,\mp\sqrt2)$: $Hf=\begin{pmatrix}20&4\\4&20\end{pmatrix}$, amb $\det=384>0$ i $\mathrm{tr}=40>0$.
A $(0,0)$: $Hf=\begin{pmatrix}-4&4\\4&-4\end{pmatrix}$, amb $\det=0$ i $\mathrm{tr}=-8$.
  3. [classificar_no_degenerats] Classificar on la hessiana decideix  (teoria: T5.33, T5.30)
     objectiu: Decidir el caràcter dels punts crítics on la hessiana no és degenerada.
     idea: Aplicar les condicions suficients d'extrem; en dues variables el signe de la forma hessiana es llegeix del determinant i de la traça.
     detall: A $(\pm\sqrt2,\mp\sqrt2)$: $\det>0$ i $\mathrm{tr}>0$, la hessiana és definida positiva, per tant són mínims locals estrictes. Hi val $f=4+4-4-8-4=-8$; com que $f\to+\infty$ quan $\|(x,y)\|\to\infty$ (dominen els termes de grau 4), $f$ assoleix un mínim absolut, que ha de ser en un punt crític: aquests dos punts són mínims absoluts.
  4. [origen] Estudiar l'origen (cas degenerat)  (teoria: T5.25)
     objectiu: Decidir el caràcter de l'origen, on el criteri de la hessiana no decideix.
     idea: Tornar a la definició: comparar el signe de $f(x,y)-f(0,0)$ restringint $f$ a diverses rectes que passen per l'origen.
     detall: $f(0,0)=0$. Sobre l'eix $y=0$: $f(x,0)=x^4-2x^2=x^2(x^2-2)<0$ per $0<|x|<\sqrt2$. Sobre la diagonal $y=x$: $f(x,x)=2x^4>0$ per $x\neq0$. Tota bola centrada a l'origen conté punts amb $f<0$ i punts amb $f>0$: l'origen és un punt de sella.
ERRORS COMUNS:
  - [perd_solucions] En resoldre l'equació en $x$ divideix per $x$ i perd la solució $x=0$ (o bé no justifica que $x^3+y^3=0$ implica $y=-x$).
  - [degenerat_conclou] Amb $\det Hf(0,0)=0$ conclou que l'origen és un màxim (perquè la traça és negativa) o que «no és res» sense justificar-ho.
  - [nomes_una_direccio] Estudia l'origen només sobre una recta (per exemple $y=0$) i en dedueix que és un màxim local.

TEORIA DEL CURS QUE FA SERVIR:
[T5.21] Definició 21 (Tema 5) — Extrems locals (diverses variables)
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció. Diem que un punt $\mathbf{a}\in\Omega$ és un

(i) màxim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\leqslant f(\mathbf{a})$;

(ii) mínim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\geqslant f(\mathbf{a})$;

(iii) màxim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})<f(\mathbf{a})$;

(iv) mínim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})>f(\mathbf{a})$.

[T5.22] Definició 22 (Tema 5) — Punt crític
$\mathbf{a}\in\Omega$ és un punt crític de $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si $f$ és diferenciable en $\mathbf{a}$ i $Df(\mathbf{a})=0$.

[T5.25] Definició 25 (Tema 5) — Punt de sella
Un punt $\mathbf{a}\in\Omega$ és un punt de sella d'una funció diferenciable $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si és un punt crític de $f$ i per a tot $\epsilon>0$ existeixen $\mathbf{x},\mathbf{y}\in B(\mathbf{a},\epsilon)$ tals que $f(\mathbf{x})<f(\mathbf{a})<f(\mathbf{y})$.

[T5.32] Definició 32 (Tema 5) — Matriu hessiana
Sigui $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$. La matriu (o la forma quadràtica) hessiana de $f$ en un punt $\mathbf{a}\in\Omega$ és $Hf(\mathbf{a})$ (o $q_{Hf(\mathbf{a})}$), on
$$Hf(\mathbf{a})=\begin{pmatrix}D_{1,1}f(\mathbf{a})&\cdots&D_{1,n}f(\mathbf{a})\\\vdots&&\vdots\\D_{n,1}f(\mathbf{a})&\cdots&D_{n,n}f(\mathbf{a})\end{pmatrix}.$$

[T5.6] Teorema 6 (Tema 5) — Teorema de Schwarz
(Schwarz). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$ i $D_iD_jf$ i $D_jD_if$ existeixen en $\Omega$. Si $D_iD_jf$ i $D_jD_if$ són contínues en un entorn d'$\mathbf{a}\in\Omega$, aleshores
$$D_iD_jf(\mathbf{a})=D_jD_if(\mathbf{a}).$$

[T5.33] Teorema 33 (Tema 5) — Condicions suficients d'extrem
(condicions suficients). Sigui $\Omega\subseteq\mathbb{R}^n$ un obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$, i $\mathbf{a}\in\Omega$ un punt crític de $f$. Aleshores,

(i) $q_{Hf(\mathbf{a})}$ és definida positiva $\Rightarrow$ $\mathbf{a}$ és un mínim local estricte de $f$.

(ii) $q_{Hf(\mathbf{a})}$ és definida negativa $\Rightarrow$ $\mathbf{a}$ és un màxim local estricte de $f$.

(iii) $q_{Hf(\mathbf{a})}$ és indefinida $\Rightarrow$ $\mathbf{a}$ és un punt de sella de $f$.

(iv) $\mathbf{a}$ és un mínim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida positiva.

(v) $\mathbf{a}$ és un màxim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida negativa.

[T5.30] Observació 30 (Tema 5) — Valors propis en dues variables
En dues variables, si $M=\begin{pmatrix}m_{11}&m_{12}\\m_{21}&m_{22}\end{pmatrix}$, aleshores els valors propis de $M$ són
$$\lambda_\pm=\frac12\left(\mathrm{tr}M\pm\sqrt{(\mathrm{tr}M)^2-4\,\mathrm{det}M}\right),$$
on $\mathrm{tr}M=m_{11}+m_{22}$ és la traça de $M$ i $\mathrm{det}M=m_{11}m_{22}-m_{12}m_{21}=m_{11}m_{22}-m_{12}^2$ és el seu determinant. En concret, el discriminant sempre és positiu o zero:
$$(\mathrm{tr}M)^2-4\,\mathrm{det}M=(m_{11}+m_{22})^2-4(m_{11}m_{22}-m_{12}^2)=(m_{11}-m_{22})^2+4m_{12}^2\geq0.$$
Fixem-nos que:

- Si $\det M<0$, aleshores $\lambda_+>0$ i $\lambda_-<0$. En particular, $\lambda_+$ i $\lambda_-$ tenen signes diferents i, per tant, la forma quadràtica $q_M$ és indefinida.
- Si $\det M>0$, aleshores $\mathrm{sgn}(\lambda_\pm)=\mathrm{sgn}(\mathrm{tr}M)$. En particular, si $\mathrm{tr}M>0$, $q_M$ és definida positiva, i si $\mathrm{tr}M<0$, $q_M$ és definida negativa.
- Si $\det M=0$, aleshores $\lambda_-=0$ i $\lambda_+=\mathrm{tr}M$. En aquest cas, si $\mathrm{tr}M>0$, $q_M$ és semidefinida positiva, i si $\mathrm{tr}M<0$, $q_M$ és semidefinida negativa. Si, a més, $\mathrm{tr}M=0$, ambdós valors propis són zero (cas degenerat).
</solucio_de_referencia>

### Document a revisar

[1] Les derivades parcials són $f_x=4x^3-4x+4y$ i $f_y=4y^3-4y+4x$. Sumant les equacions $f_x=0$ i $f_y=0$ obtenim $4(x^3+y^3)=0$; com que $x^3+y^3=(x+y)(x^2-xy+y^2)$ i el segon factor només s'anul·la a l'origen, en tots els casos $y=-x$.
[2] Substituint $y=-x$ a $f_x=0$: $4x^3-8x=4x(x^2-2)=0$, d'on $x=0$ o $x=\pm\sqrt2$. Els punts crítics són $(0,0)$, $(\sqrt2,-\sqrt2)$ i $(-\sqrt2,\sqrt2)$.
[3] La hessiana és $Hf(x,y)=\begin{pmatrix}12x^2-4&4\\4&12y^2-4\end{pmatrix}$. A $(\pm\sqrt2,\mp\sqrt2)$ val $\begin{pmatrix}20&4\\4&20\end{pmatrix}$, amb determinant $384>0$ i traça $40>0$.
[4] Per tant la hessiana és definida positiva a $(\sqrt2,-\sqrt2)$ i a $(-\sqrt2,\sqrt2)$, i aquests dos punts són mínims locals estrictes, amb $f=4+4-4-8-4=-8$.
[5] A més, com que $f$ és contínua a $\mathbb{R}^2$, pel teorema de Weierstrass té un mínim absolut, que ha de ser en un punt crític perquè $\mathbb{R}^2$ és obert. Com que $f(0,0)=0>-8$, aquests dos punts són mínims absoluts.
[6] A l'origen, $Hf(0,0)=\begin{pmatrix}-4&4\\4&-4\end{pmatrix}$ té determinant $0$, de manera que el criteri de la hessiana no decideix i cal estudiar $f$ directament.
[7] Sobre l'eix $y=0$, $f(x,0)=x^4-2x^2=x^2(x^2-2)<0$ per a $0<|x|<\sqrt2$; sobre la diagonal $y=x$, $f(x,x)=2x^4+4x^2>0$ per a $x\neq0$. Com que $f(0,0)=0$, tota bola centrada a l'origen conté punts amb $f<0$ i amb $f>0$: l'origen és un punt de sella.


## t5-6:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Estudieu, en funció de $k$, el caràcter dels punts crítics de la funció $f(x,y)=\frac{1}{2}(x^2+y^2)+kxy$.
RESULTAT CORRECTE: - Si $k\neq\pm1$, l'únic punt crític és $(0,0)$. Si $|k|<1$ és un mínim local estricte (de fet, mínim absolut, $f\geq0$); si $|k|>1$ és un punt de sella.
- Si $k=1$, $f=\frac12(x+y)^2$ i els punts crítics són tots els de la recta $y=-x$; si $k=-1$, $f=\frac12(x-y)^2$ i els punts crítics són tots els de la recta $y=x$. En tots dos casos cada punt crític és un mínim local (i absolut) no estricte, amb $f=0$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [punts_critics] Trobar els punts crítics segons $k$  (teoria: T5.22)
     objectiu: Trobar els punts crítics de $f$, distingint els valors de $k$ per als quals el conjunt de punts crítics canvia.
     idea: El sistema $f_x=0$, $f_y=0$ és lineal i homogeni en $(x,y)$: té solució única si i només si el determinant de la matriu del sistema és no nul.
     detall: $f_x=x+ky$, $f_y=kx+y$. El determinant del sistema és $1-k^2$. Si $k\neq\pm1$, l'única solució és $(0,0)$. Si $k=1$, les dues equacions són $x+y=0$: tots els punts de la recta $y=-x$ són crítics. Si $k=-1$, queda $x-y=0$: tots els punts de la recta $y=x$ són crítics.
  2. [hessiana] Calcular la hessiana  (teoria: T5.32)
     objectiu: Obtenir la matriu hessiana de $f$ i el seu determinant i traça.
     idea: $f$ és polinòmica de grau 2, de manera que la hessiana és constant.
     detall: $Hf(x,y)=\begin{pmatrix}1&k\\k&1\end{pmatrix}$ a tot punt, amb $\det Hf=1-k^2$ i $\mathrm{tr}\,Hf=2>0$.
  3. [classificar_no_degenerat] Classificar l'origen quan $k\neq\pm1$  (teoria: T5.33, T5.30)
     objectiu: Decidir el caràcter de l'origen en els casos en què la hessiana no és degenerada.
     idea: Aplicar les condicions suficients d'extrem; en dues variables el signe de la forma hessiana es llegeix del signe del determinant i de la traça.
     detall: Si $|k|<1$: $\det=1-k^2>0$ i $\mathrm{tr}=2>0$, la hessiana és definida positiva, i l'origen és un mínim local estricte (de fet absolut: $f$ és la mateixa forma quadràtica, que és $\geq0$).
Si $|k|>1$: $\det<0$, la hessiana és indefinida i l'origen és un punt de sella (per exemple, $f(t,t)=(1+k)t^2$ i $f(t,-t)=(1-k)t^2$ tenen signes oposats).
  4. [casos_degenerats] Estudiar els casos $k=\pm1$  (teoria: T5.21)
     objectiu: Decidir el caràcter dels punts crítics quan $k=1$ i quan $k=-1$, on el criteri de la hessiana no decideix.
     idea: Mirar l'expressió de $f$ per a aquests valors concrets de $k$: es pot escriure de manera que el seu signe sigui evident, i comparar directament amb el valor de $f$ als punts crítics.
     detall: Si $k=1$: $f=\frac12(x^2+2xy+y^2)=\frac12(x+y)^2\geq0$, i val $0$ exactament a la recta $y=-x$. Cada punt crític té $f=0\leq f(x,y)$ per a tot $(x,y)$: és un mínim local (i absolut), però no estricte, perquè a qualsevol bola hi ha altres punts de la recta amb el mateix valor.
Si $k=-1$: $f=\frac12(x-y)^2$, i el mateix raonament sobre la recta $y=x$.
ERRORS COMUNS:
  - [oblida_cas_degenerat] Afirma que l'únic punt crític és sempre l'origen, sense adonar-se que per a $k=\pm1$ el sistema té infinites solucions.
  - [hessiana_degenerada_conclou] Per a $k=\pm1$ (determinant zero) conclou que no hi ha extrem, o aplica el criteri de la hessiana com si decidís.
  - [estricte_vs_no_estricte] Per a $k=\pm1$ diu que els punts crítics són mínims locals estrictes.

TEORIA DEL CURS QUE FA SERVIR:
[T5.21] Definició 21 (Tema 5) — Extrems locals (diverses variables)
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció. Diem que un punt $\mathbf{a}\in\Omega$ és un

(i) màxim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\leqslant f(\mathbf{a})$;

(ii) mínim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\geqslant f(\mathbf{a})$;

(iii) màxim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})<f(\mathbf{a})$;

(iv) mínim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})>f(\mathbf{a})$.

[T5.22] Definició 22 (Tema 5) — Punt crític
$\mathbf{a}\in\Omega$ és un punt crític de $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si $f$ és diferenciable en $\mathbf{a}$ i $Df(\mathbf{a})=0$.

[T5.32] Definició 32 (Tema 5) — Matriu hessiana
Sigui $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$. La matriu (o la forma quadràtica) hessiana de $f$ en un punt $\mathbf{a}\in\Omega$ és $Hf(\mathbf{a})$ (o $q_{Hf(\mathbf{a})}$), on
$$Hf(\mathbf{a})=\begin{pmatrix}D_{1,1}f(\mathbf{a})&\cdots&D_{1,n}f(\mathbf{a})\\\vdots&&\vdots\\D_{n,1}f(\mathbf{a})&\cdots&D_{n,n}f(\mathbf{a})\end{pmatrix}.$$

[T5.33] Teorema 33 (Tema 5) — Condicions suficients d'extrem
(condicions suficients). Sigui $\Omega\subseteq\mathbb{R}^n$ un obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$, i $\mathbf{a}\in\Omega$ un punt crític de $f$. Aleshores,

(i) $q_{Hf(\mathbf{a})}$ és definida positiva $\Rightarrow$ $\mathbf{a}$ és un mínim local estricte de $f$.

(ii) $q_{Hf(\mathbf{a})}$ és definida negativa $\Rightarrow$ $\mathbf{a}$ és un màxim local estricte de $f$.

(iii) $q_{Hf(\mathbf{a})}$ és indefinida $\Rightarrow$ $\mathbf{a}$ és un punt de sella de $f$.

(iv) $\mathbf{a}$ és un mínim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida positiva.

(v) $\mathbf{a}$ és un màxim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida negativa.

[T5.30] Observació 30 (Tema 5) — Valors propis en dues variables
En dues variables, si $M=\begin{pmatrix}m_{11}&m_{12}\\m_{21}&m_{22}\end{pmatrix}$, aleshores els valors propis de $M$ són
$$\lambda_\pm=\frac12\left(\mathrm{tr}M\pm\sqrt{(\mathrm{tr}M)^2-4\,\mathrm{det}M}\right),$$
on $\mathrm{tr}M=m_{11}+m_{22}$ és la traça de $M$ i $\mathrm{det}M=m_{11}m_{22}-m_{12}m_{21}=m_{11}m_{22}-m_{12}^2$ és el seu determinant. En concret, el discriminant sempre és positiu o zero:
$$(\mathrm{tr}M)^2-4\,\mathrm{det}M=(m_{11}+m_{22})^2-4(m_{11}m_{22}-m_{12}^2)=(m_{11}-m_{22})^2+4m_{12}^2\geq0.$$
Fixem-nos que:

- Si $\det M<0$, aleshores $\lambda_+>0$ i $\lambda_-<0$. En particular, $\lambda_+$ i $\lambda_-$ tenen signes diferents i, per tant, la forma quadràtica $q_M$ és indefinida.
- Si $\det M>0$, aleshores $\mathrm{sgn}(\lambda_\pm)=\mathrm{sgn}(\mathrm{tr}M)$. En particular, si $\mathrm{tr}M>0$, $q_M$ és definida positiva, i si $\mathrm{tr}M<0$, $q_M$ és definida negativa.
- Si $\det M=0$, aleshores $\lambda_-=0$ i $\lambda_+=\mathrm{tr}M$. En aquest cas, si $\mathrm{tr}M>0$, $q_M$ és semidefinida positiva, i si $\mathrm{tr}M<0$, $q_M$ és semidefinida negativa. Si, a més, $\mathrm{tr}M=0$, ambdós valors propis són zero (cas degenerat).
</solucio_de_referencia>

### Document a revisar

[1] Les derivades parcials són $f_x=x+ky$ i $f_y=kx+y$. Els punts crítics són les solucions d'un sistema lineal homogeni de determinant $1-k^2$.
[2] Si $k\neq\pm1$, el determinant no és zero i l'única solució és $(0,0)$. Si $k=1$, les dues equacions són $x+y=0$ i tots els punts de la recta $y=-x$ són crítics; si $k=-1$, queda $x-y=0$ i són crítics tots els punts de la recta $y=x$.
[3] La hessiana és constant: $Hf=\begin{pmatrix}1&k\\k&1\end{pmatrix}$, amb $\det Hf=1-k^2$ i $\mathrm{tr}\,Hf=2>0$.
[4] Si $|k|<1$, $\det Hf>0$ i $\mathrm{tr}\,Hf>0$, de manera que la hessiana és definida positiva i l'origen és un mínim local estricte; de fet és absolut, perquè $f$ és la forma quadràtica $\frac12(x,y)\,Hf\,(x,y)^T$, que és $\geq0$.
[5] Si $k>1$, $\det Hf<0$, la hessiana és indefinida i l'origen és un punt de sella: $f(t,t)=(1+k)t^2>0$ i $f(t,-t)=(1-k)t^2<0$ per a $t\neq0$. Si $k<-1$, en canvi, $f(t,t)=(1+k)t^2<0$ per a $t\neq0$, i l'origen és un màxim local.
[6] Si $k=1$, $f=\frac12(x+y)^2\geq0$ i val $0$ exactament sobre la recta $y=-x$. Per tant cada punt crític és un mínim local estricte, ja que $f>0$ a tots els punts fora de la recta.
[7] Si $k=-1$, $f=\frac12(x-y)^2$, i el mateix raonament s'aplica als punts de la recta $y=x$.


## t5-11:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Calculeu el polinomi de Taylor de grau $\leqslant3$ de la funció $f(x,y)=(x-1+\sin^2y)\log(x-y)$ en el punt $(1,0)$. És $(1,0)$ un extrem local de $f(x,y)$?
RESULTAT CORRECTE: Amb $u=x-1$: $P_3(x,y)=u^2-uy-\frac12u^3+u^2y+\frac12uy^2-y^3$, és a dir,
$P_3(x,y)=(x-1)^2-(x-1)y-\frac12(x-1)^3+(x-1)^2y+\frac12(x-1)y^2-y^3$.
El punt $(1,0)$ és crític (no hi ha termes de grau $1$), però la hessiana $Hf(1,0)=\begin{pmatrix}2&-1\\-1&0\end{pmatrix}$ té determinant $-1<0$: és indefinida i $(1,0)$ és un punt de sella, no un extrem local.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [desenvolupar_factors] Desenvolupar cada factor  (teoria: T5.16, T5.17)
     objectiu: Obtenir els desenvolupaments de Taylor fins a grau $3$ de cadascun dels dos factors de $f$ al voltant de $(1,0)$.
     idea: Canviar a la variable $u=x-1$ (centre a l'origen) i usar desenvolupaments coneguts d'una variable ($\log(1+z)$, $\sin y$) substituint-hi l'expressió adequada; la unicitat del polinomi de Taylor garanteix que el resultat és el polinomi de Taylor.
     detall: Amb $u=x-1$ tenim $x-y=1+(u-y)$ i, posant $z=u-y$ a $\log(1+z)=z-\frac{z^2}{2}+\frac{z^3}{3}+O_4(z)$:
$\log(x-y)=(u-y)-\frac12(u-y)^2+\frac13(u-y)^3+O_4(u,y)$.
D'altra banda $\sin y=y+O_3(y)$, de manera que $\sin^2y=y^2+O_4(y)$ i el primer factor és $u+y^2+O_4(u,y)$.
  2. [producte] Multiplicar i truncar  (teoria: T5.16, T5.17)
     objectiu: Obtenir $P_3$ multiplicant els desenvolupaments i quedant-se amb els monomis de grau $\leq 3$.
     idea: El primer factor no té terme constant, així que del segon factor només calen els termes de grau $\leq 2$; tots els productes de grau $\geq 4$ van al residu.
     detall: $(u+y^2)\left((u-y)-\frac12(u-y)^2\right)=u^2-uy-\frac12u(u^2-2uy+y^2)+uy^2-y^3+O_4$
$=u^2-uy-\frac12u^3+u^2y+\frac12uy^2-y^3+O_4(u,y)$.
Per tant $P_3(x,y)=(x-1)^2-(x-1)y-\frac12(x-1)^3+(x-1)^2y+\frac12(x-1)y^2-y^3$ (i $f(1,0)=0$).
  3. [hessiana] Punt crític i hessiana  (teoria: T5.14, T5.22, T5.32)
     objectiu: Comprovar si $(1,0)$ és un punt crític i obtenir la matriu hessiana de $f$ en $(1,0)$ a partir del polinomi.
     idea: Els termes de grau $1$ de $P_3$ són $Df(1,0)$; la part de grau $2$ és $\frac12$ de la forma quadràtica hessiana, i en podem llegir les derivades segones.
     detall: $P_3$ no té termes de grau $1$, per tant $Df(1,0)=(0\ \ 0)$ i $(1,0)$ és crític.
La part quadràtica és $u^2-uy=\frac12\left(2u^2-2uy+0\cdot y^2\right)$, d'on $f_{xx}(1,0)=2$, $f_{xy}(1,0)=-1$, $f_{yy}(1,0)=0$:
$Hf(1,0)=\begin{pmatrix}2&-1\\-1&0\end{pmatrix}$.
  4. [classificar] Classificar el punt  (teoria: T5.30, T5.33, T5.25)
     objectiu: Decidir el caràcter del punt crític $(1,0)$.
     idea: Estudiar el signe de la forma quadràtica hessiana (en dues variables, el signe del determinant i de la traça) i aplicar les condicions suficients de segon ordre.
     detall: $\det Hf(1,0)=2\cdot0-(-1)^2=-1<0$, per tant els valors propis tenen signes oposats i la forma és indefinida. Com que $f$ és $\mathcal{C}^2$ en un entorn de $(1,0)$ (on $x-y>0$), $(1,0)$ és un punt de sella i no és extrem local.
Comprovació directa: $f(x,0)=(x-1)\log x>0$ per $x\neq1$ proper a $1$, mentre que $f(1,y)=\sin^2y\,\log(1-y)<0$ per $y>0$ petit.
ERRORS COMUNS:
  - [sin2_grau1] Desenvolupa $\sin^2y$ com si fos $y$ (o hi posa un terme $-y^3/3$), confonent $\sin^2y$ amb $\sin y$.
  - [truncar_malament] Multiplica els desenvolupaments i oblida termes creuats de grau $3$ (per exemple els de $u\cdot(u-y)^2$ o $y^2\cdot(u-y)$), o en manté de grau $4$.
  - [oblida_punt_critic] Classifica el punt amb la hessiana sense comprovar abans que és crític, o creu que el grau $3$ del polinomi decideix el caràcter.
  - [determinant_signe] Amb $f_{yy}=0$ creu que la hessiana és semidefinida o que el criteri no decideix, sense calcular el determinant.

TEORIA DEL CURS QUE FA SERVIR:
[T5.14] Teorema 14 (Tema 5) — Teorema de Taylor (diverses variables)
(de Taylor). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^{r+1}(\Omega)$, i $\mathbf{a}\in\Omega$. Per a tot $\mathbf{x}\in\Omega$ amb $[\mathbf{a},\mathbf{x}]\subseteq\Omega$, existeix $\xi_\mathbf{x}\in(\mathbf{a},\mathbf{x})$ tal que $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$, on

(i) El polinomi
$$\begin{aligned}P_r(\mathbf{x})={}&f(\mathbf{a})+\sum_{i=1}^{n}D_if(\mathbf{a})(x_i-a_i)+\frac{1}{2!}\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_i)(x_j-a_j)+\cdots\\
&\cdots+\frac{1}{r!}\sum_{i_1,\ldots,i_r=1}^{n}D_{i_1,\ldots,i_r}f(\mathbf{a})(x_{i_1}-a_{i_1})\cdots(x_{i_r}-a_{i_r})\end{aligned}$$
s'anomena el polinomi de Taylor de grau $r$ de la funció $f$ en el punt $\mathbf{a}$,

(ii) El residu de grau $r$ de la funció $f$ en el punt $\mathbf{a}$ és
$$R_{r+1}(\mathbf{x})=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})(x_{i_1}-a_{i_1})\cdots(x_{i_{r+1}}-a_{i_{r+1}}).$$
A més, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$

[T5.21] Definició 21 (Tema 5) — Extrems locals (diverses variables)
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció. Diem que un punt $\mathbf{a}\in\Omega$ és un

(i) màxim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\leqslant f(\mathbf{a})$;

(ii) mínim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\geqslant f(\mathbf{a})$;

(iii) màxim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})<f(\mathbf{a})$;

(iv) mínim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})>f(\mathbf{a})$.

[T5.16] Observació 16 (Tema 5) — Unicitat del polinomi de Taylor
Per a una funció $f\in\mathcal{C}^{r+1}(\Omega)$, el seu polinomi de Taylor de grau $r$, $P_r(\mathbf{x})$, és l'únic polinomi de grau $\leqslant r$ que compleix $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-P_r(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$

[T5.17] Exemple 17 (Tema 5) — Càlcul de polinomis de Taylor
Exemples de càlcul de polinomis de Taylor.

A nivell pràctic, donat que el polinomi de Taylor és únic, ens dóna llibertat per calcular-lo de formes diverses sempre que ens assegurem que $\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-P_r(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0$.

Vegem-ne alguns exemples:

1. Calculem el desenvolupament fins a ordre $3$ de la funció $f(x,y)=\mathrm{e}^x\sin(xy)$ a l'origen.

   Per a fer-ho usarem els corresponents desenvolupaments de Taylor de les funcions d'una variable $\mathrm{e}^x$ i $\sin(z)$, substituïrem $z=xy$ i calcularem els termes del seu producte fins a grau $3$. La unicitat del polinomi de Taylor ens assegura que el resultat que obtinguem serà el mateix que calcular el polinomi de Taylor de $f(x,y)$ fins a grau $3$ a través de la seva fórmula (vegeu el Teorema 14). En efecte
   $$\mathrm{e}^x=1+x+\frac{x^2}{2}+\frac{x^3}{3!}+S_4(x),\quad\text{amb }\frac{S_4(x)}{x^3}\to0\quad\text{quan }x\to0.$$
   De manera anàloga,
   $$\sin(z)=z-\frac{z^3}{3!}+T_4(z),\quad\text{amb }\frac{T_4(z)}{z^3}\to0\quad\text{quan }z\to0$$
   i, per tant, fent $z=xy$,
   $$\sin(xy)=xy+W_4(x,y),\quad\text{amb}\quad\frac{W_4(x,y)}{\|(x,y)\|^3}\to0\ \text{ quan }\|(x,y)\|\to0.$$
   Multiplicant ambdues expressions per a $\mathrm{e}^x$ i $\sin(xy)$ s'obté que
   $$f(x,y)=\mathrm{e}^x\,\sin(xy)=\left(1+x+\frac{x^2}{2}+\frac{x^3}{3!}+S_4(x)\right)(xy+W_4(x,y))=xy+x^2y+R_4(x,y),$$
   amb $\dfrac{R_4(x,y)}{\|(x,y)\|^3}\to0$ quan $\|(x,y)\|\to0$.

2. Calculem el polinomi de Taylor de la funció $f(x,y)=\sin x\ \cos y$ de grau $5$ a l'origen.

   Una manera usual de simplificar la notació del residu és denotar $R(x,y)=O_{r+1}(x,y)$ per a indicar que $R(x,y)$ té tots els seus monomis de grau $\geq r+1$. Noteu que, aleshores,
   $$\lim_{(x,y)\to(0,0)}\frac{R(x,y)}{\|(x,y)\|^r}=0\Leftrightarrow R(x,y)=O_{r+1}(x,y).$$
   Aquesta notació s'estèn de manera similar a qualsevol dimensió, $x\in\mathbb{R}^n$.

   Tenint en compte aquest fet i els desenvolupaments de $\sin(x)$ i de $\cos(y)$, podem escriure
   $$\begin{aligned}f(x,y)&=\sin(x)\cos(y)=\left(x-\frac{x^3}{3!}+\frac{x^5}{5!}+O_7(x)\right)\left(1-\frac{y^2}{2}+\frac{y^4}{4!}+O_6(y)\right)\\
   &=x-\frac{xy^2}{2}+\frac{xy^4}{4!}-\frac{x^3}{3!}+\left(\frac{x^3}{3!}\right)\left(\frac{y^2}{2!}\right)+\frac{x^5}{5!}+O_7(x,y)\\
   &=x-\frac{x^3}{3!}-\frac{xy^2}{2}+\frac{xy^4}{4!}+\frac{x^3y^2}{3!2!}+\frac{x^5}{5!}+O_7(x,y)\end{aligned}$$
   Per tant, el polinomi de grau $5$ de $f(x,y)$ a l'origen és
   $$P_5(x,y)=x-\frac{x^3}{3!}-\frac{xy^2}{2}+\frac{xy^4}{4!}+\frac{x^3y^2}{3!2!}+\frac{x^5}{5!}.$$

3. Calculem el polinomi de grau $3$ de $f(x,y)=\mathrm{e}^{x+\sin y}$ a l'origen. Per a fer-ho usarem, primer, que $\mathrm{e}^{x+\sin y}=\mathrm{e}^x\mathrm{e}^{\sin y}$; segon, per a calcular el polinomi de Taylor de $\mathrm{e}^{\sin y}$ al $(0,0)$,
   $$P_{\exp(\sin y)}(y)=P_{\exp(x)}(x)\circ P_{\sin y}(y)$$
   on $P_{\exp(x)}$ i $P_{\sin y}$ denoten, respectivament, els polinomis de Taylor de les funcions $\exp(x)$ i $\sin y$ i, a més, tenim en compte que $P_{\sin y}(0)=0$. Així, del fet que
   $$\mathrm{e}^{\sin y}=1+\sin y+\frac{\sin^2y}{2!}+\frac{\sin^3y}{3!}+\cdots,$$
   es deriva que
   $$\begin{aligned}P_{\exp(\sin y)}(y)&=1+\left(y-\frac{y^3}{3!}+O_4(y)\right)+\frac{1}{2!}\left(y-\frac{y^3}{3!}+O_4(y)\right)^2+\frac{1}{3!}\left(y+O(y^2)\right)^3+O_4(y)\\
   &=1+\left(y-\frac{y^3}{3!}\right)+\frac{1}{2!}\left(y^2\right)+\frac{1}{3!}\left(y^3\right)+O_4(y)\\
   &=1+y+\frac{y^2}{2!}+O_4(y).\end{aligned}$$
   Així, per a obtenir el polinomi de grau $3$ de $f(x,y)$, fem
   $$\begin{aligned}f(x,y)&=\left(1+x+\frac{x^2}{2!}+\frac{x^3}{3!}+O_4(x)\right)\left(1+y+\frac{y^2}{2!}+O_4(y)\right)\\
   &=\left(1+y+\frac{y^2}{2!}\right)+x\left(1+y+\frac{y^2}{2!}\right)+\frac{x^2}{2!}(1+y)+\frac{x^3}{3!}+O_4(x,y)\\
   &=1+x+y+\frac12x^2+x\,y+\frac12y^2+\frac16x^3+\frac12x^2\,y+\frac12x\,y^2+O_4(x,y).\end{aligned}$$
   Així, doncs, $P_3(x,y)=1+x+y+\frac12x^2+x\,y+\frac12y^2+\frac16x^3+\frac12x^2\,y+\frac12x\,y^2.$

[T5.22] Definició 22 (Tema 5) — Punt crític
$\mathbf{a}\in\Omega$ és un punt crític de $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si $f$ és diferenciable en $\mathbf{a}$ i $Df(\mathbf{a})=0$.

[T5.32] Definició 32 (Tema 5) — Matriu hessiana
Sigui $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$. La matriu (o la forma quadràtica) hessiana de $f$ en un punt $\mathbf{a}\in\Omega$ és $Hf(\mathbf{a})$ (o $q_{Hf(\mathbf{a})}$), on
$$Hf(\mathbf{a})=\begin{pmatrix}D_{1,1}f(\mathbf{a})&\cdots&D_{1,n}f(\mathbf{a})\\\vdots&&\vdots\\D_{n,1}f(\mathbf{a})&\cdots&D_{n,n}f(\mathbf{a})\end{pmatrix}.$$

[T5.30] Observació 30 (Tema 5) — Valors propis en dues variables
En dues variables, si $M=\begin{pmatrix}m_{11}&m_{12}\\m_{21}&m_{22}\end{pmatrix}$, aleshores els valors propis de $M$ són
$$\lambda_\pm=\frac12\left(\mathrm{tr}M\pm\sqrt{(\mathrm{tr}M)^2-4\,\mathrm{det}M}\right),$$
on $\mathrm{tr}M=m_{11}+m_{22}$ és la traça de $M$ i $\mathrm{det}M=m_{11}m_{22}-m_{12}m_{21}=m_{11}m_{22}-m_{12}^2$ és el seu determinant. En concret, el discriminant sempre és positiu o zero:
$$(\mathrm{tr}M)^2-4\,\mathrm{det}M=(m_{11}+m_{22})^2-4(m_{11}m_{22}-m_{12}^2)=(m_{11}-m_{22})^2+4m_{12}^2\geq0.$$
Fixem-nos que:

- Si $\det M<0$, aleshores $\lambda_+>0$ i $\lambda_-<0$. En particular, $\lambda_+$ i $\lambda_-$ tenen signes diferents i, per tant, la forma quadràtica $q_M$ és indefinida.
- Si $\det M>0$, aleshores $\mathrm{sgn}(\lambda_\pm)=\mathrm{sgn}(\mathrm{tr}M)$. En particular, si $\mathrm{tr}M>0$, $q_M$ és definida positiva, i si $\mathrm{tr}M<0$, $q_M$ és definida negativa.
- Si $\det M=0$, aleshores $\lambda_-=0$ i $\lambda_+=\mathrm{tr}M$. En aquest cas, si $\mathrm{tr}M>0$, $q_M$ és semidefinida positiva, i si $\mathrm{tr}M<0$, $q_M$ és semidefinida negativa. Si, a més, $\mathrm{tr}M=0$, ambdós valors propis són zero (cas degenerat).

[T5.33] Teorema 33 (Tema 5) — Condicions suficients d'extrem
(condicions suficients). Sigui $\Omega\subseteq\mathbb{R}^n$ un obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$, i $\mathbf{a}\in\Omega$ un punt crític de $f$. Aleshores,

(i) $q_{Hf(\mathbf{a})}$ és definida positiva $\Rightarrow$ $\mathbf{a}$ és un mínim local estricte de $f$.

(ii) $q_{Hf(\mathbf{a})}$ és definida negativa $\Rightarrow$ $\mathbf{a}$ és un màxim local estricte de $f$.

(iii) $q_{Hf(\mathbf{a})}$ és indefinida $\Rightarrow$ $\mathbf{a}$ és un punt de sella de $f$.

(iv) $\mathbf{a}$ és un mínim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida positiva.

(v) $\mathbf{a}$ és un màxim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida negativa.

[T5.25] Definició 25 (Tema 5) — Punt de sella
Un punt $\mathbf{a}\in\Omega$ és un punt de sella d'una funció diferenciable $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si és un punt crític de $f$ i per a tot $\epsilon>0$ existeixen $\mathbf{x},\mathbf{y}\in B(\mathbf{a},\epsilon)$ tals que $f(\mathbf{x})<f(\mathbf{a})<f(\mathbf{y})$.
</solucio_de_referencia>

### Document a revisar

[1] Posem $u=x-1$. Aleshores $x-y=1+(u-y)$ i, posant $z=u-y$ a $\log(1+z)=z-\frac{z^2}{2}+\frac{z^3}{3}+O_4(z)$, obtenim $\log(x-y)=(u-y)-\frac12(u-y)^2+\frac13(u-y)^3+O_4(u,y)$.
[2] D'altra banda, $\sin y=y+O_3(y)$, de manera que $\sin^2y=y^2+O_4(y)$ i el primer factor és $u+y^2+O_4(u,y)$.
[3] Com que el primer factor no té terme constant, del logaritme només calen els termes fins a grau $2$: cal truncar a grau $3$ el producte $(u+y^2)\left((u-y)-\frac12(u-y)^2\right)$.
[4] Multiplicant: $u(u-y)=u^2-uy$, $-\frac12u(u-y)^2=-\frac12u^3+\frac12u^2y-\frac12uy^2$ i $y^2(u-y)=uy^2-y^3$; el producte de $y^2$ per $-\frac12(u-y)^2$ és de grau $4$ i el descartem.
[5] Per tant, amb $f(1,0)=0$, $P_3(x,y)=(x-1)^2-(x-1)y-\frac12(x-1)^3+\frac12(x-1)^2y+\frac12(x-1)y^2-y^3$.
[6] $P_3$ no té termes de grau $1$, així que $Df(1,0)=(0\ \ 0)$ i $(1,0)$ és un punt crític. Comparant la part quadràtica $u^2-uy$ amb $\frac12\left(f_{xx}u^2+2f_{xy}uy+f_{yy}y^2\right)$, llegim $f_{xx}(1,0)=2$, $f_{xy}(1,0)=-2$ i $f_{yy}(1,0)=0$.
[7] Llavors $Hf(1,0)=\begin{pmatrix}2&-2\\-2&0\end{pmatrix}$ té determinant $-4<0$: és indefinida i, com que $f$ és $\mathcal{C}^2$ en un entorn de $(1,0)$ (on $x-y>0$), el punt $(1,0)$ és un punt de sella i no és un extrem local.


## t5-14:dificil

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $\varphi:\mathbb{R}\to\mathbb{R}$ una funció derivable i tal que $a<b$ en són els únics zeros, complint a més $\varphi'(a)>0$ i $\varphi'(b)<0$. Considerem la funció $f(x,y)=\int_x^y\varphi(t)\,dt$. Calculeu els punts crítics de $f$, discutiu-ne el caràcter i interpreteu els resultats obtinguts.
RESULTAT CORRECTE: $\nabla f(x,y)=(-\varphi(x),\varphi(y))$; punts crítics: $(a,a)$, $(a,b)$, $(b,a)$, $(b,b)$.
$\varphi<0$ a $(-\infty,a)$, $\varphi>0$ a $(a,b)$, $\varphi<0$ a $(b,+\infty)$. Amb $\Phi'=\varphi$, $f(x,y)=\Phi(y)-\Phi(x)$, i $\Phi$ té un mínim local estricte a $a$ i un màxim local estricte a $b$. Per tant:
$(a,b)$ és màxim local estricte, amb $f(a,b)=\int_a^b\varphi>0$; $(b,a)$ és mínim local estricte, amb $f(b,a)=-\int_a^b\varphi<0$; $(a,a)$ i $(b,b)$ són punts de sella (amb $f=0$).
Interpretació: entre els intervals d'integració propers, el que dona més àrea és exactament el tram $[a,b]$ on $\varphi>0$ (afegir o treure trossos on $\varphi<0$, o treure trossos on $\varphi>0$, fa disminuir la integral); el mínim és el mateix interval recorregut al revés. A la diagonal $f(x,x)=0$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [punts_critics] Gradient i punts crítics  (teoria: T3.2, T3.18, T5.22)
     objectiu: Calcular les derivades parcials de $f$, justificar que és diferenciable i trobar-ne els punts crítics.
     idea: Pel teorema fonamental del càlcul (una variable; $\varphi$ és contínua perquè és derivable), derivar la integral respecte del límit superior i de l'inferior. Parcials contínues impliquen diferenciabilitat.
     detall: $\frac{\partial f}{\partial x}(x,y)=-\varphi(x)$, $\frac{\partial f}{\partial y}(x,y)=\varphi(y)$, contínues, de manera que $f$ és diferenciable (de fet $\mathcal{C}^1$).
$\nabla f=0\iff\varphi(x)=\varphi(y)=0\iff x,y\in\{a,b\}$: punts crítics $(a,a)$, $(a,b)$, $(b,a)$, $(b,b)$.
  2. [signe_phi] Signe de φ  (teoria: T2.24, T5.9)
     objectiu: Determinar el signe de $\varphi$ a cadascun dels intervals en què $a$ i $b$ divideixen la recta.
     idea: El signe de $\varphi'$ en un zero diu el signe de $\varphi$ just a cada costat; entre zeros consecutius, una funció contínua sense zeros no canvia de signe (valor intermedi).
     detall: $\varphi'(a)=\lim_{t\to a}\frac{\varphi(t)}{t-a}>0$: $\varphi(t)$ té el signe de $t-a$ prop de $a$. Igualment $\varphi'(b)<0$: $\varphi(t)$ té el signe contrari de $t-b$ prop de $b$. Pel teorema del valor intermedi, el signe és constant a cada interval: $\varphi<0$ a $(-\infty,a)$, $\varphi>0$ a $(a,b)$, $\varphi<0$ a $(b,+\infty)$.
Amb $\Phi(s)=\int_a^s\varphi$: $\Phi$ decreix, creix, decreix; $a$ és mínim local estricte i $b$ màxim local estricte de $\Phi$.
  3. [classificar] Caràcter dels punts crítics  (teoria: T5.21, T5.25)
     objectiu: Decidir el caràcter de cadascun dels quatre punts crítics.
     idea: Com que $f(x,y)=\Phi(y)-\Phi(x)$ separa variables, l'increment de $f$ és la diferència de dos increments d'una variable; combinar el caràcter de $a$ i $b$ per a $\Phi$ en cada coordenada.
     detall: $f(x,y)-f(x_0,y_0)=[\Phi(y)-\Phi(y_0)]-[\Phi(x)-\Phi(x_0)]$.
$(a,b)$: per $(x,y)$ proper, $\Phi(y)\leq\Phi(b)$ i $\Phi(x)\geq\Phi(a)$, amb igualtat només si $y=b$ i $x=a$ respectivament; si $(x,y)\neq(a,b)$ alguna de les dues és estricta i $f(x,y)<f(a,b)$: màxim local estricte.
$(b,a)$: tot al revés, mínim local estricte.
$(a,a)$: $f(a,y)-f(a,a)=\Phi(y)-\Phi(a)>0$ per $y\neq a$ proper, i $f(x,a)-f(a,a)=-(\Phi(x)-\Phi(a))<0$: punt de sella. $(b,b)$: anàlogament, sella.
(Si $\varphi\in\mathcal{C}^1$, ho confirma la hessiana $Hf=\mathrm{diag}(-\varphi'(x),\varphi'(y))$.)
  4. [interpretar] Interpretar
     objectiu: Explicar en termes d'àrees per què els punts crítics tenen aquest caràcter.
     idea: $f(x,y)$ és l'àrea amb signe sota $\varphi$ entre $x$ i $y$; pensar què passa en moure lleugerament els extrems de l'interval d'integració.
     detall: $f(a,b)=\int_a^b\varphi>0$ és l'àrea de tot el tram on $\varphi$ és positiva: moure $a$ o $b$ cap a fora afegeix àrea negativa i cap a dins en treu de positiva, així que la integral decreix. $f(b,a)=-f(a,b)$ és el mateix interval recorregut al revés (mínim). A la diagonal $f(x,x)=0$, i prop de $(a,a)$ o $(b,b)$ la integral sobre un interval petit pot tenir qualsevol signe segons cap a on el posem: sella.
ERRORS COMUNS:
  - [signe_derivada_inferior] Oblida el signe menys en derivar respecte del límit inferior ($\partial f/\partial x=\varphi(x)$).
  - [hessiana_sense_c2] Aplica el criteri de la hessiana assumint $f\in\mathcal{C}^2$, quan només sabem que $\varphi$ és derivable ($\varphi'$ podria no ser contínua).
  - [signe_phi_sense_justificar] Afirma el signe de $\varphi$ entre zeros sense justificar per què no canvia (o confon el signe de $\varphi$ amb el de $\varphi'$).
  - [oblida_punts_diagonal] Només troba $(a,b)$ i $(b,a)$, oblidant $(a,a)$ i $(b,b)$.

TEORIA DEL CURS QUE FA SERVIR:
[T5.21] Definició 21 (Tema 5) — Extrems locals (diverses variables)
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció. Diem que un punt $\mathbf{a}\in\Omega$ és un

(i) màxim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\leqslant f(\mathbf{a})$;

(ii) mínim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\geqslant f(\mathbf{a})$;

(iii) màxim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})<f(\mathbf{a})$;

(iv) mínim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})>f(\mathbf{a})$.

[T5.22] Definició 22 (Tema 5) — Punt crític
$\mathbf{a}\in\Omega$ és un punt crític de $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si $f$ és diferenciable en $\mathbf{a}$ i $Df(\mathbf{a})=0$.

[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

[T2.24] Teorema 24 (Tema 2) — Teorema del valor intermedi
(del valor intermedi). Sigui $f:\Omega\subseteq M\to\mathbb{R}$ contínua, $K\subseteq\Omega$ connex, i $x,y\in K$. Aleshores, per a tota $c\in\mathbb{R}$ tal que $f(x)<c<f(y)$, $\exists\xi\in K$ tal que $f(\xi)=c$.

[T5.9] Definició 9 (Tema 5) — Extrems locals (una variable)
Sigui $\Omega\subseteq\mathbb{R}$ obert i $f:\Omega\to\mathbb{R}$ una funció. Diem que un punt $a\in\Omega$ és un

(i) màxim local de $f$ si $\exists\,\epsilon>0$ t.q. $\forall x\in(a-\epsilon,a+\epsilon)\subseteq\Omega$, $f(x)\leqslant f(a)$;

(ii) mínim local de $f$ si $\exists\,\epsilon>0$ t.q. $\forall x\in(a-\epsilon,a+\epsilon)\subseteq\Omega$, $f(x)\geqslant f(a)$;

(iii) màxim local estricte de $f$ si $\exists\,\epsilon>0\ \forall\, a\neq x\in(a-\epsilon,a+\epsilon)\subseteq\Omega$, $f(x)<f(a)$;

(iv) mínim local estricte de $f$ si $\exists\,\epsilon>0\ \forall\, a\neq x\in(a-\epsilon,a+\epsilon)\subseteq\Omega$, $f(x)>f(a)$.

[T5.25] Definició 25 (Tema 5) — Punt de sella
Un punt $\mathbf{a}\in\Omega$ és un punt de sella d'una funció diferenciable $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si és un punt crític de $f$ i per a tot $\epsilon>0$ existeixen $\mathbf{x},\mathbf{y}\in B(\mathbf{a},\epsilon)$ tals que $f(\mathbf{x})<f(\mathbf{a})<f(\mathbf{y})$.
</solucio_de_referencia>

### Document a revisar

[1] Com que $\varphi$ és derivable, és contínua. Posem $\Phi(s)=\int_a^s\varphi(t)\,dt$; pel teorema fonamental del càlcul $\Phi'=\varphi$, i $f(x,y)=\Phi(y)-\Phi(x)$.
[2] Així $\frac{\partial f}{\partial x}(x,y)=-\varphi(x)$ i $\frac{\partial f}{\partial y}(x,y)=\varphi(y)$, que són contínues, i $f$ és de classe $\mathcal{C}^1$. Els punts crítics són els que compleixen $\varphi(x)=\varphi(y)=0$: $(a,a)$, $(a,b)$, $(b,a)$ i $(b,b)$.
[3] Com que $\varphi'(a)>0$, $\varphi$ és creixent en un entorn de $a$ i, com que $\varphi(a)=0$, prop de $a$ el signe de $\varphi(t)$ és el de $t-a$. Anàlogament, de $\varphi'(b)<0$ es dedueix que prop de $b$ el signe de $\varphi(t)$ és el contrari del de $t-b$.
[4] Com que $\varphi$ és contínua i no s'anul·la a $(-\infty,a)$, a $(a,b)$ ni a $(b,+\infty)$, pel teorema de Bolzano té signe constant a cada interval: $\varphi<0$ a $(-\infty,a)$, $\varphi>0$ a $(a,b)$ i $\varphi<0$ a $(b,+\infty)$. Per tant $\Phi$ té un mínim local estricte a $a$ i un màxim local estricte a $b$.
[5] Al punt $(a,b)$: per a $(x,y)$ proper, $\Phi(y)\leq\Phi(b)$ i $\Phi(x)\geq\Phi(a)$, amb igualtat només si $y=b$ i $x=a$ respectivament. Per tant $f(x,y)-f(a,b)=[\Phi(y)-\Phi(b)]-[\Phi(x)-\Phi(a)]<0$ si $(x,y)\neq(a,b)$: és un màxim local estricte.
[6] Al punt $(b,a)$ les desigualtats s'inverteixen, i és un mínim local estricte, amb $f(b,a)=-\int_a^b\varphi<0$.
[7] Al punt $(a,a)$: $f(a,y)-f(a,a)=\Phi(y)-\Phi(a)>0$ per a $y\neq a$ proper, de manera que hi ha punts arbitràriament a prop on $f$ supera $f(a,a)=0$, i per tant $(a,a)$ és un punt de sella. Anàlogament, $(b,b)$ és un punt de sella.
[8] Interpretació: $f(a,b)=\int_a^b\varphi>0$ és l'àrea de tot el tram on $\varphi$ és positiva; desplaçar un extrem de l'interval afegeix àrea negativa o en treu de positiva, i la integral disminueix. De fet, $f(a,b)$ és el màxim absolut de $f$, perquè cap interval no pot acumular més àrea positiva que $[a,b]$. El mínim local $(b,a)$ és el mateix interval recorregut al revés, i a la diagonal $f(x,x)=0$.


## t6-4c:facil

### Referència

<solucio_de_referencia>
ENUNCIAT: Determineu els extrems absoluts de les funcions $f$ següents sobre els recintes $K$ que s'especifiquen:

(c) $f(x,y)=x^2+y^2-xy+y+x$, $\quad K=\{(x,y)\in\mathbb{R}^2\mid x+y\geqslant-3,\ x\leqslant y,\ y\leqslant0\}$.
RESULTAT CORRECTE: Màxim absolut $6$, assolit en $(-3,0)$.
Mínim absolut $-1$, assolit en $(-1,-1)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [recinte] Descriure el recinte  (teoria: T2.18, T1.34, T2.23)
     objectiu: Descriure $K$ (quina figura és, els seus vèrtexs) i justificar que hi ha extrems absoluts.
     idea: Intersecar dos a dos les rectes que el delimiten; un conjunt definit per desigualtats no estrictes de funcions contínues és tancat.
     detall: $K$ és el triangle de vèrtexs $(0,0)$ (de $x=y$, $y=0$), $(-3,0)$ (de $x+y=-3$, $y=0$) i $\left(-\frac32,-\frac32\right)$ (de $x+y=-3$, $x=y$). És tancat i fitat, per tant compacte, i $f$ és contínua: Weierstrass garanteix màxim i mínim absoluts.
  2. [interior] Punts crítics  (teoria: T5.23, T5.22)
     objectiu: Trobar els punts crítics de $f$ i situar-los respecte de $K$.
     idea: Resoldre el sistema lineal $\nabla f=0$ i comprovar a quina part de $K$ (interior o frontera) cau.
     detall: $f_x=2x-y+1=0$, $f_y=2y-x+1=0$ donen $x=y=-1$. El punt $(-1,-1)$ és de $K$ però és a la frontera (compleix $x=y$), no a l'interior: a l'interior no hi ha punts crítics. Igualment és candidat, amb $f(-1,-1)=-1$.
  3. [costats] Els tres costats  (teoria: T6.1)
     objectiu: Trobar els candidats a extrem sobre cadascun dels tres costats del triangle.
     idea: Parametritzar cada costat amb una variable (substituint l'equació de la recta) i estudiar la funció d'una variable a l'interval corresponent.
     detall: $y=0$, $x\in[-3,0]$: $f=x^2+x$, crític $x=-\frac12$ amb valor $-\frac14$; extrems $f(0,0)=0$, $f(-3,0)=6$.
$y=x$, $x\in[-\frac32,0]$: $f=x^2+2x$, crític $x=-1$ amb valor $-1$; extrem $f\left(-\frac32,-\frac32\right)=-\frac34$.
$y=-3-x$, $x\in[-3,-\frac32]$: $f=3x^2+9x+6$, amb $f'=6x+9=0$ només a $x=-\frac32$, que és l'extrem de l'interval (vèrtex $\left(-\frac32,-\frac32\right)$, valor $-\frac34$); a l'altre extrem, $f(-3,0)=6$.
  4. [comparar] Comparar valors  (teoria: T2.23)
     objectiu: Decidir el màxim i el mínim absoluts.
     idea: Comparar tots els valors dels candidats.
     detall: Valors: $0,6,-\frac14,-1,-\frac34$. Màxim absolut $6$ en $(-3,0)$; mínim absolut $-1$ en $(-1,-1)$.
ERRORS COMUNS:
  - [critic_interior] Afirma que $(-1,-1)$ és un punt interior de $K$, o el descarta per ser a la frontera.
  - [triangle_malament] Identifica malament el triangle (per exemple pren el costat $x\ge y$) i treballa amb vèrtexs equivocats.
  - [oblida_vertexs] Oblida avaluar els vèrtexs del triangle.

TEORIA DEL CURS QUE FA SERVIR:
[T1.24] Definició 24 (Tema 1) — Compacte i seqüencialment compacte
Sigui $(M,d)$ espai mètric, $A\subseteq M$.

i) $A$ és _compacte_ si tot recobriment per oberts de $A$ admet un subrecobriment finit, és a dir: si $A\subseteq\bigcup_{i\in I}U_i$, amb $U_i$ obert, aleshores existeixen $i_1,\ldots,i_k\in I$ tals que $A\subseteq\bigcup_{j=1}^k U_{i_j}$.

ii) $A$ és _seqüencialment compacte_ si tota successió $(x_n)_{n\in\mathbb{N}}\subseteq A$ admet una subsuccessió (una parcial) convergent a un punt de $A$.

[T2.18] Corol·lari 18 (Tema 2) — Conjunts definits per desigualtats
Siguin $f,g:\mathbb{R}^n\longrightarrow\mathbb{R}$, funcions contínues. Llavors:

(i) $A=\{x\in\mathbb{R}^n:f(x)>g(x)\}$ és un conjunt obert.

(ii) $B=\{x\in\mathbb{R}^n:f(x)\geq g(x)\}$ és un conjunt tancat.

[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.

[T2.23] Teorema 23 (Tema 2) — Teorema de Weierstrass
(Weierstrass). Sigui $f:\Omega\subseteq M\to\mathbb{R}$ contínua i $K\subseteq\Omega$ compacte. Llavors $f(K)$ és fitat i $\exists x_0,x_1\in K$ t.q. $f(x_0)=\min_{x\in K}f(x)$ i $f(x_1)=\max_{x\in K}f(x)$.

[T5.23] Proposició 23 (Tema 5) — Els extrems són punts crítics
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció diferenciable en $\mathbf{a}\in\Omega$. Si $\mathbf{a}$ és un extrem (és a dir, un màxim o un mínim) local de $f$, llavors $\mathbf{a}$ és un punt crític de $f$.

[T5.22] Definició 22 (Tema 5) — Punt crític
$\mathbf{a}\in\Omega$ és un punt crític de $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si $f$ és diferenciable en $\mathbf{a}$ i $Df(\mathbf{a})=0$.

[T6.1] Exemple 1 (Tema 6) — Exemple inicial d'extrems condicionats
Exemple inicial d'extrems condicionats i de varietat diferenciable.

Considerem la funció $f(x,y)=x^2+y^2$, amb $(x,y)\in\mathbb{R}^2$, i suposem que la volem maximitzar/minimitzar sobre una corba $M\subset\mathbb{R}^2$. Distingim dos casos:

- $M$ no està fitada, com ara una recta $ax+by=c$.
- $M$ és compacta, com ara una circumferència $x^2+y^2=2x$.

En el cas de la recta, si suposem, per exemple, que $b\neq 0$ (si $b=0$, canviem els papers de $x$ i $y$), podem aïllar $y=(-c-ax)/b$ i substituir a $f(x,y)$. Així
$$H(x):=f(x,y)|_M=x^2+\frac{(-c-a\,x)^2}{b^2}=\left(1+\frac{a^2}{b^2}\right)x^2+\frac{2ac}{b^2}x+\frac{c^2}{b^2}.$$
Com que $H$ és un polinomi, si volem trobar els candidats a extrems locals, fem
$$H'(x)=0\Leftrightarrow x=\frac{-ac}{a^2+b^2}.$$
Clarament, el punt trobat és un mínim local ja que $H''(x)>0$ per a tot $x\in\mathbb{R}$; a més, $H$ no té màxims locals ja que és una paràbola i $\displaystyle\lim_{x\to\pm\infty}H(x)=+\infty$.

També podem calcular
$$\begin{aligned}H\left(\frac{-ac}{a^2+b^2}\right)&=\frac{a^2+b^2}{b^2}\left(\frac{-ac}{a^2+b^2}\right)^2+\frac{2ac}{b^2}\left(\frac{-ac}{a^2+b^2}\right)+\frac{c^2}{b^2}\\&=\frac{a^2c^2}{b^2(a^2+b^2)}-\frac{2a^2c^2}{b^2(a^2+b^2)}+\frac{c^2(a^2+b^2)}{b^2(a^2+b^2)}=\frac{c^2}{a^2+b^2}.\end{aligned}$$

Representem gràficament la situació, dibuixant les corbes de nivell de $f(x,y)$ i la recta.

En la figura, hem triat $a=3$, $b=-1$ i $c=2$, amb la qual cosa el mínim (local) val $\frac{c^2}{a^2+b^2}=\frac{2}{5}$ i s'ateny al punt $(x,y)=\left(\frac{-ac}{a^2+b^2},(-c-a\frac{-ac}{a^2+b^2})/b\right)=\left(\frac{-ac}{a^2+b^2},\frac{-bc}{a^2+b^2}\right)=\left(-\frac35,\frac15\right)$. S'hi mostren (en vermell) les corbes de nivell $k\in\{\frac15,\frac25,\frac35,\frac45,1\}$ i la recta (en negre). Observem que just en el mínim local de $f$ sobre la recta, $\left(-\frac35,\frac15\right)$ hi ha una tangència. Veurem a continuació que això no és cap casualitat.

[Figura: corbes de nivell circulars de $f$ (en vermell) centrades a l'origen i la recta $3x-y=2$ (en negre), tangent a una corba de nivell en $(-3/5,1/5)$.]

Imaginem-nos que en el gràfic anterior la recta representa el traçat d'una trajectòria sobre les corbes de nivell d'un mapa. És clar que la tangència indica la mínima cota (si el valor de les corbes de nivell és creixent des del centre cap enfora) ja que no tallarà corbes de nivell més baix.

La condició de tangència és equivalent al fet que els vectors gradients $\nabla f$ i $\nabla\Phi$, amb $\Phi(x,y)=ax+by+c$, siguin paral·lels. Deixem com a exercici veure que imposant aquest paral·lelisme obtenim la mateixa solució.

En el cas de la circumferència donada per $x^2+y^2+2x=0$ (en negre a la gràfica de la dreta), resulta ser tangent a les corbes de nivell de $f(x,y)$ en els punts $(0,0)$ i $(2,0)$. De fet, ho podíem haver vist a cop d'ull ja que $x^2+y^2+2x=0$ equival a $(x-1)^2+y^2=1$ i és evident que el mínim de $x^2+y^2$ (distància a l'origen al quadrat) es pren a $(0,0)$ i el màxim es pren a $(2,0)$. A més, ambdós són extrems absoluts, que sabem que han d'existir ja que estem maximitzant/minimitzant una funció sobre un compacte.

[Figura: corbes de nivell circulars de $f$ (en vermell) i la circumferència $(x-1)^2+y^2=1$ (en negre).]

Una altra manera de resoldre aquest darrer exemple seria parametritzant la circumferència $x^2+y^2+2x=0$ per $\rho(t)=(x(t),y(t))=(1+\cos t,\sin t)$ i substituint a $f(x)$:
$$F(t):=f(x(t),y(t))=(1+\cos t)^2+\sin^2t=2+2\cos t,\qquad t\in[0,2\pi].$$
És immediat veure que $F'(t)=0$ per a $t\in(0,2\pi)$ si i només si $t=\pi$; a més, $F''(\pi)>0$. Com que $[0,2\pi]$ és compacte, existeixen els extrems absoluts: el mínim absolut $F=0$ es pren en $t=\pi$, és a dir, per a $(x,y)=(0,0)$, i el màxim absolut s'ateny en els extrems de l'interval: $F(0)=F(2\pi)=4$, és a dir, per a $(x,y)=(2,0)$.

Afegirem una tercera situació a aquest exemple: el cas que vulguem trobar els extrems absoluts en un domini del pla delimitat per diverses corbes. Prenem, per exemple,
$$D=\left\{(x,y)\in\mathbb{R}^2\ \middle|\ x^2+y^2-x\leq\frac34,\ y\geq x-\frac32\right\}.$$
Representem el domini $D$ (regió blava) conjuntament amb les corbes de nivell de $f(x,y)$ (en vermell). Intencionadament, hem marcat algunes corbes de nivell amb un traç més gruixut.

[Figura: domini $D$ (regió blava) limitat per la circumferència $x^2+y^2-x=3/4$ i la recta $y=x-3/2$, amb les corbes de nivell de $f$ en vermell.]

Fixem-nos que $D$ és un domini compacte i, per tant, la funció $f$, contínua arreu, hi prendrà un màxim absolut i un mínim absolut.

D'altra banda, les corbes que delimiten el domini, definides com a solucions de $x^2+y^2-x=\frac34$ i de $y=x-\frac32$, es tallen en els punts $(1/2,-1)$ i $(3/2,0)$ (cal substituir $y=x-\frac32$ en l'equació de la circumferència i resoldre).

Els extrems absoluts es podran prendre, o bé en l'interior de $D$, o bé damunt la circumferència $x^2+y^2-x=\frac34$ (sempre i quan estigui fent de frontera), o bé sobre el segment $\{(x,y)\mid y=x-3/2,\ x\in[1/2,3/2]\}$. Els estudiem un per un:

(i) Un extrem absolut en l'obert $\mathrm{int}(D)$ ha de ser, al mateix temps, extrem relatiu. Per tant, resolem $\nabla f(x,y)=(0,0)$ i obtenim que $(0,0)$ és un extrem relatiu (de fet, un mínim perquè $\lambda=2$ és un vap de la matriu hessiana de multiplicitat 2) i, per tant, un candidat a mínim absolut. (Nota: En aquest exemple, és evident que és mínim absolut ja que $f(x,y)=x^2+y^2>f(0,0)=0$ per a tot $(x,y)\in\mathbb{R}^2\setminus\{(0,0)\}$.)

(ii) Per a estudiar $f(x,y)$ sobre $x^2+y^2-x=\frac34$, ho podem fer de tres maneres:

- Substituint $y^2=\dfrac34+x-x^2$ en $f(x,y)=x^2+y^2$ i buscant els extrems absoluts de
$$F(x):=f(x,y)|_{y^2=\frac34+x-x^2},\qquad\text{per a }x\in[-1/2,3/2].$$
Observem que, en realitat, per a $(x,y)=(-1/2,0)$ i per a $(x,y)=(3/2,0)$, no podem posar $y$ en funció de $x$ ja que no es compleix la condició $\Phi_y=y\neq0$ del teorema de la funció implícita. Hauríem de fer-ho per a
$$y=\pm\sqrt{\frac34+x-x^2},\qquad x\in(-1/2,3/2),$$
i analitzar a posteriori quin valor pren la funció $f$ en $(x,y)=(-1/2,0)$ i $(x,y)=(3/2,0)$.
A efectes pràctics, com que només tenim un terme $y^2$, podem tractar els dos casos de cop:
$$F(x):=f(x,y)|_{y^2=\frac34+x-x^2}=x+\frac34$$
que, de manera òbvia, es veu que és creixent per a $x\in(-1/2,3/2)$. Així, doncs, el mínim es pren en $x=-1/2$ i el màxim en $x=3/2$, que corresponen als punts $P_1:=(-1/2,0)$ i $P_2:=(3/2,0)$, respectivament.
- Parametritzant el tros de circumferència com $\rho(t)=\{(\frac12+\cos t,\sin t),\ t\in[0,3\pi/2]\}$ i considerant
$$G(t):=f(x(t),y(t))=\left(\frac12+\cos t\right)^2+\sin^2t=\cos t+\frac54.$$
Clarament, els extrems absoluts de $G$ en $t\in[0,3\pi/2]$ es prenen per a $t=\pi$ (mínim) i per a $t=0$ (màxim), que corresponen als punts $P_1$ i $P_2$, respectivament (com no podria ser d'altra manera).
Com que estem cercant extrems absoluts en un interval tancat, hem de considerar també que els extrems de l'interval són candidats a ser-ho. En el cas de la parametrització, això ens obligaria a explorar el punt corresponent a $t=3\pi/2$, és a dir, $P_3:=(1/2,-1)$.
- Imposant que
$$\nabla f(x,y)=\lambda\nabla\Phi(x,y),$$
on $\Phi(x,y)=x^2+y^2-x-\frac34$, és a dir,
$$(2x,2y)=\lambda(2x-1,2y).$$
De la segona equació treiem que $\lambda=1$ o $y=0$. Si $\lambda=1$, la primera equació no té solució. Per tant, ens quedem només amb $y=0$ i, de $\Phi=0$ obtenim que $x^2-x-\frac34=0$, que té per solucions $x=-1/2$ i $x=3/2$, com ja havíem obtingut per altres mètodes. Tot i que ja no és rellevant, observem, que per a $x=-1/2$, s'obté $\lambda=1/2$, per a $x=3/2$, s'obté $\lambda=3/2$.

(iii) Per a estudiar $f(x,y)$ sobre la recta $y=x-\frac32$, per a $x\in[1/2,3/2]$, també es pot fer de diverses maneres, però ho farem només substituint per no fer l'estudi tan repetitiu:
$$H(x):=f(x,y)|_{y=x-\frac32}=2x^2-3x+9/4,$$
que no té solucions reals. Per tant, només pot prendre extrems absoluts en $x=1/2$ i en $x=3/2$, que corresponen, respectivament, als punts $P_2$ i $P_3$ ja definits anteriorment.

Malgrat tot, és interessant en aquest cas veure que el plantejament
$$\nabla f(x,y)=\lambda\nabla\Phi(x,y),$$
on $\Phi(x,y)=y-x+3/2$, ens duu a
$$(2x,2y)=\lambda(-1,1),$$
és a dir, o bé $\lambda=x=y=0$, que no és vàlida perquè $\Phi(0,0)\neq0$, o bé $x=-y=-\lambda/2$. Per a aquesta darrera opció, imposant que $\Phi(x,y)=0$, obtenim que $\lambda=-3$ i, per tant, $x=3/4$ i $y=-3/4$. No és un candidat a extrem absolut, però l'anomenem $P_4:=(3/4,-3/4)$ i li dedicarem un comentari al final.

Per a acabar l'exemple, avaluem $f(x,y)$ en tots els punts candidats:
$$f(0,0)=0;\ f(P_1)=1/4;\ f(P_2)=9/4;\ f(P_3)=5/4.$$
Per tant, el mínim absolut de $f$ s'ateny en $(0,0)$ i el màxim absolut, en $(3/2,0)$, com és ben evident a la figura ja que representen els contactes dins $D$ amb les corbes de nivell més baix i més alt, respectivament.

Fixem-nos que el punt $P_4$ representa un punt de sella condicionat perquè, per a tot $\epsilon>0$, existeixen punts $(x_1,y_1)$ i $(x_2,y_2)$ en $D\cap B(P_4,\epsilon)$ tals que $f(x_1,y_1)<f(P_4)<f(x_2,y_2)$.
</solucio_de_referencia>

### Document a revisar

[1] El recinte $K$ és el triangle de vèrtexs $(0,0)$ (intersecció de $x=y$ i $y=0$), $(-3,0)$ (de $x+y=-3$ i $y=0$) i $\left(-\frac32,-\frac32\right)$ (de $x+y=-3$ i $x=y$). És tancat i fitat, per tant compacte, i $f$ és contínua: pel teorema de Weierstrass, $f$ té màxim i mínim absoluts a $K$.
[2] Punts crítics: $f_x=2x-y+1=0$ i $f_y=2y-x+1=0$ donen $x=y=-1$. El punt $(-1,-1)$ compleix $x=y$, de manera que és a la frontera de $K$ i no a l'interior; igualment el guardem com a candidat, amb $f(-1,-1)=-1$.
[3] Costat $y=0$, $x\in[-3,0]$: $f=x^2+x$, amb derivada nul·la a $x=-\frac12$ i valor $f\left(-\frac12,0\right)=-\frac34$; als extrems, $f(0,0)=0$ i $f(-3,0)=6$.
[4] Costat $y=x$, $x\in\left[-\frac32,0\right]$: $f=x^2+2x$, amb derivada nul·la a $x=-1$ (el punt $(-1,-1)$ d'abans) i valor $-1$; al vèrtex, $f\left(-\frac32,-\frac32\right)=-\frac34$.
[5] Costat $y=-3-x$, $x\in\left[-3,-\frac32\right]$: $f=3x^2+9x+6$, amb $f'=6x+9$, que només s'anul·la a $x=-\frac32$, extrem de l'interval; els valors als extrems ja els tenim: $-\frac34$ i $6$.
[6] Comparant tots els valors obtinguts ($0$, $6$, $-\frac34$, $-1$ i $-\frac34$), el màxim absolut és $6$, assolit a $(-3,0)$, i el mínim absolut és $-1$, assolit a $(-1,-1)$.


## t6-3f:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Determineu els extrems absoluts de $f$ quan les variables estan sotmeses als lligams que s'indiquen. (Intenteu resoldre l'exercici sense fer servir multiplicadors de Lagrange.)

(f) $f(x,y,z)=x+y+z$, $\quad x^2-y^2=1$, $\quad 2x+z=1$.
RESULTAT CORRECTE: No té extrems absoluts. Sobre el lligam, $z=1-2x$ i $f=1-x+y$; a la branca $x\geq1$ ($x=\cosh t$, $y=\sinh t$) $f=1-e^{-t}$ pren tots els valors de $(-\infty,1)$, i a la branca $x\leq-1$ ($x=-\cosh t$, $y=\sinh t$) $f=1+e^{t}$ pren tots els valors de $(1,+\infty)$. Per tant $f$ no és fitada ni superiorment ni inferiorment.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [eliminar_z] Eliminar una variable
     objectiu: Reduir el problema a una funció de dues variables sobre una corba plana.
     idea: El lligam lineal permet aïllar una variable i substituir-la a $f$.
     detall: $z=1-2x$, i $f=x+y+1-2x=1-x+y$ sobre la hipèrbola $x^2-y^2=1$ del pla $XY$.
  2. [parametritzar] Parametritzar la hipèrbola
     objectiu: Escriure la funció obtinguda en termes d'un paràmetre de la corba.
     idea: La hipèrbola té dues branques; cadascuna es parametritza amb funcions hiperbòliques.
     detall: Branca dreta: $x=\cosh t$, $y=\sinh t$, $f=1-\cosh t+\sinh t=1-e^{-t}$. Branca esquerra: $x=-\cosh t$, $y=\sinh t$, $f=1+\cosh t+\sinh t=1+e^{t}$ ($t\in\mathbb{R}$).
  3. [concloure] Estudiar el recorregut
     objectiu: Determinar si $f$ és fitada sobre el lligam i si assoleix algun valor extrem.
     idea: Mirar els límits de cada expressió quan el paràmetre tendeix a $\pm\infty$.
     detall: $1-e^{-t}\to-\infty$ quan $t\to-\infty$, i $1+e^{t}\to+\infty$ quan $t\to+\infty$. Així $f$ no és fitada ni per dalt ni per baix sobre el lligam: no hi ha màxim ni mínim absoluts (de fet, cada expressió és estrictament monòtona i tampoc no hi ha extrems locals).
ERRORS COMUNS:
  - [una_sola_branca] Només considera la branca $x\geq1$ i conclou que el suprem és $1$ o que hi ha un màxim.
  - [lagrange_sense_compacitat] Busca punts crítics (o aplica Lagrange) i en dona algun com a extrem absolut sense comprovar existència.
  - [oblida_z] Substitueix malament $z$ (p. ex. $z=2x-1$) o oblida que $f$ depèn de $z$.

TEORIA DEL CURS QUE FA SERVIR:
[T6.12] Definició 12 (Tema 6) — Extrems condicionats
Siguin $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geq1$, $D\subseteq\mathbb{R}^n$ un obert tal que $M\subseteq D$ i $f\colon D\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(D)$. Diem que un punt $\mathbf{a}\in M$ és un màxim local de $f$ condicionat a $M$ si $\mathbf{a}$ és un màxim local de $f|_M$; és a dir, si existeix un obert $G$ tal que $\mathbf{a}\in G$ i $f(\mathbf{x})\leq f(\mathbf{a})$ per a tot $x\in M\cap G$.

Definim mínim condicionat i màxim i mínim estrictes condicionats d'una manera semblant, canviant $\leq$ per la desigualtat que pertoqui. Per ser punt de sella condicionat, cal que, per a tot obert $G$ tal que $\mathbf{a}\in G$, existeixin $\mathbf{x},\mathbf{y}\in M\cap G$ tals que $f(\mathbf{x})<f(\mathbf{a})$ i $f(\mathbf{y})>f(\mathbf{a})$.
</solucio_de_referencia>

### Document a revisar

[1] Del segon lligam, $z=1-2x$. Substituint, sobre el conjunt de lligams $f=x+y+1-2x=1-x+y$, i el problema es redueix a estudiar $g(x,y)=1-x+y$ sobre la hipèrbola $x^2-y^2=1$ del pla $XY$.
[2] La hipèrbola té dues branques. La branca dreta ($x\geq1$) es parametritza per $x=\cosh t$, $y=\sinh t$, amb $t\in[0,+\infty)$, i hi tenim $g=1-\cosh t+\sinh t=1-e^{-t}$.
[3] La branca esquerra ($x\leq-1$) es parametritza per $x=-\cosh t$, $y=\sinh t$, amb $t\in\mathbb{R}$, i hi tenim $g=1+\cosh t+\sinh t=1+e^{t}$.
[4] A la branca dreta, $1-e^{-t}$ és estrictament creixent per a $t\geq0$: val $0$ a $t=0$ i tendeix a $1$ quan $t\to+\infty$, sense assolir-lo.
[5] A la branca esquerra, $1+e^{t}$ és estrictament creixent, tendeix a $+\infty$ quan $t\to+\infty$ i pren tots els valors de $(2,+\infty)$.
[6] Per tant $f$ no és fitada superiorment sobre els lligams i no té màxim absolut. En canvi, a la branca dreta $g\geq0$, amb igualtat a $t=0$, i a l'esquerra $g>2$, de manera que el mínim absolut és $0$, assolit al punt $(1,0,-1)$.


## t6-6:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Trobeu la distància entre les corbes d'equació $x+y=4$ i $x^2+4y^2=4$.
RESULTAT CORRECTE: $d=\dfrac{4-\sqrt5}{\sqrt2}=\dfrac{4\sqrt2-\sqrt{10}}{2}\approx1.25$, assolida entre el punt $\left(\frac{4}{\sqrt5},\frac{1}{\sqrt5}\right)$ de l'el·lipse i el punt $\left(\frac{4}{\sqrt5}+\frac{4-\sqrt5}{2},\frac{1}{\sqrt5}+\frac{4-\sqrt5}{2}\right)$ de la recta.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [no_es_tallen] Les corbes no es tallen  (teoria: T1.34, T2.23)
     objectiu: Comprovar si les dues corbes es tallen i escollir una funció a minimitzar.
     idea: Si es tallessin la distància seria $0$. Per a un punt fix de l'el·lipse, la distància a la recta té una fórmula tancada.
     detall: La distància d'un punt $(x,y)$ a la recta $x+y=4$ és $\frac{|x+y-4|}{\sqrt2}$. La distància entre les corbes és el mínim d'aquesta funció sobre l'el·lipse $E$, que és compacta (tancada i fitada), així que el mínim existeix. Veurem que $x+y<4$ a tota $E$, de manera que les corbes no es tallen i cal maximitzar $x+y$ sobre $E$.
  2. [maxim_suma] Extrems de $x+y$ sobre l'el·lipse  (teoria: T6.2, T6.17, T2.23)
     objectiu: Trobar el màxim de $x+y$ sobre l'el·lipse.
     idea: Extrems condicionats d'una funció lineal sobre una corba compacta: Lagrange (o parametritzar l'el·lipse).
     detall: L'el·lipse és una 1-varietat compacta: $\nabla\Phi=(2x,8y)\neq0$ a $E$. Lagrange: $\nabla(x+y)=(1,1)=\lambda(2x,8y)$ dona $x=4y$; amb $x^2+4y^2=4$: $20y^2=4$, $y=\pm\frac{1}{\sqrt5}$, $x=\pm\frac{4}{\sqrt5}$. Valors $x+y=\pm\sqrt5$. Màxim $\sqrt5<4$, en $\left(\frac{4}{\sqrt5},\frac{1}{\sqrt5}\right)$.
(Parametritzant $(2\cos t,\sin t)$: $2\cos t+\sin t\le\sqrt5$.)
  3. [distancia] Calcular la distància
     objectiu: Obtenir la distància i els punts on s'assoleix.
     idea: Substituir el màxim trobat a la fórmula de distància punt-recta; el punt de la recta és el peu de la perpendicular.
     detall: $d=\frac{4-\sqrt5}{\sqrt2}=\frac{4\sqrt2-\sqrt{10}}{2}\approx1.25$. El punt de la recta és $\left(\frac{4}{\sqrt5},\frac{1}{\sqrt5}\right)+\frac{4-\sqrt5}{2}(1,1)$.
ERRORS COMUNS:
  - [interseccio] No comprova si les corbes es tallen (o creu que es tallen) i dona distància $0$ o un resultat sense sentit.
  - [lagrange_una_sola] Aplica Lagrange a la distància de l'origen a la recta o al centre de l'el·lipse, en lloc de la distància entre punts de les dues corbes.
  - [valor_absolut] Agafa el mínim de $x+y$ en comptes del màxim (perd el valor absolut de la fórmula punt-recta).

TEORIA DEL CURS QUE FA SERVIR:
[T1.5] Definició 5 (Tema 1) — Distància
Sigui $M$ un conjunt. Una funció $d(\cdot,\cdot):M\times M\longrightarrow\mathbb{R}$ es diu que és una _distància_ si per a tot $x,y,z\in M$, es compleixen:

i) $d(x,y)\geq 0$; $d(x,y)=0\iff x=y$.

ii) $d(x,y)=d(y,x)$ (simètrica).

iii) $d(x,y)\leq d(x,z)+d(z,y)$ (desigualtat triangular).

Direm en aquest cas que $(M,d)$ és un _espai mètric_.

[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.

[T2.23] Teorema 23 (Tema 2) — Teorema de Weierstrass
(Weierstrass). Sigui $f:\Omega\subseteq M\to\mathbb{R}$ contínua i $K\subseteq\Omega$ compacte. Llavors $f(K)$ és fitat i $\exists x_0,x_1\in K$ t.q. $f(x_0)=\min_{x\in K}f(x)$ i $f(x_1)=\max_{x\in K}f(x)$.

[T6.2] Definició 2 (Tema 6) — Varietat en forma implícita
Una $m$-varietat de classe $r$ a $\mathbb{R}^n$ és un subconjunt no buit $M\subseteq\mathbb{R}^n$ tal que per a tot $\mathbf{a}\in M$ existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i una funció $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$ amb $\mathrm{rang}\left(D\Phi(\mathbf{x})\right)=n-m$ per a tot $\mathbf{x}\in G$, tals que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.

En aquest context, es diu que $M$ és la $m$-varietat associada a $\Phi$; per reforçar aquesta relació amb $\Phi$, de vegades la denotarem amb $M_\Phi$.

$M$ també s'acostuma a anomenar (sub)varietat (diferenciable, $\mathcal{C}^r$ o de classe $r$) de dimensió $m$ en $\mathbb{R}^n$.

[T6.17] Corol·lari 17 (Tema 6) — Teorema dels multiplicadors de Lagrange
(Teorema dels multiplicadors de Lagrange). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ de classe $\mathcal{C}^r$, $M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(G)$. Si $\mathbf{a}\in M_\Phi$ és un extrem local de $f$ condicionat a $M_\Phi$, aleshores existeixen uns valors únics $\lambda_1,\ldots,\lambda_{n-m}\in\mathbb{R}$ tals que $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in G\times\mathbb{R}^{n-m}$ és un punt crític de $L$, és a dir, $(\mathbf{a},\boldsymbol{\lambda})$ és solució del sistema de $2n-m$ equacions
$$\begin{cases}\nabla f(\mathbf{a})-\lambda_1\nabla\Phi_1(\mathbf{a})-\cdots-\lambda_{n-m}\nabla\Phi_{n-m}(\mathbf{a})&=\mathbf{0},\\\Phi(\mathbf{a})&=\mathbf{0}.\end{cases}$$
</solucio_de_referencia>

### Document a revisar

[1] La distància d'un punt $(x,y)$ a la recta $x+y=4$ és $\frac{|x+y-4|}{2}$. La distància entre les dues corbes és el mínim d'aquesta funció sobre l'el·lipse $E:\ x^2+4y^2=4$.
[2] L'el·lipse és tancada i fitada, per tant compacta, i la funció és contínua: pel teorema de Weierstrass el mínim existeix.
[3] Busquem els extrems de $x+y$ sobre $E$. Com que $\nabla(x^2+4y^2)=(2x,8y)\neq(0,0)$ a $E$, podem aplicar Lagrange: $(1,1)=\lambda(2x,8y)$ dona $2\lambda x=8\lambda y=1$, de manera que $\lambda\neq0$ i $x=4y$.
[4] Substituint a l'equació de l'el·lipse: $16y^2+4y^2=4$, és a dir $y^2=\frac15$, $y=\pm\frac{1}{\sqrt5}$ i $x=\pm\frac{4}{\sqrt5}$ (amb el mateix signe). Els valors de $x+y$ són $\pm\frac{5}{\sqrt5}=\pm\sqrt5$.
[5] Per tant, sobre $E$, $-\sqrt5\leq x+y\leq\sqrt5<4$: tots els punts de l'el·lipse compleixen $x+y-4<0$, i les corbes no es tallen.
[6] Així $|x+y-4|=4-(x+y)$, que és mínim quan $x+y$ és mínim, és a dir al punt $\left(-\frac{4}{\sqrt5},-\frac{1}{\sqrt5}\right)$, on $x+y=-\sqrt5$.
[7] La distància entre les corbes és $d=\frac{|-\sqrt5-4|}{2}=\frac{4+\sqrt5}{2}\approx3.12$.


## t6-8:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Trobeu els extrems absoluts de $f(x,y)=x-x^2-y^2$ en el disc $\{(x,y)\mid x^2+y^2<1\}$.
RESULTAT CORRECTE: Màxim absolut $\frac14$, assolit en $\left(\frac12,0\right)$.
No hi ha mínim absolut: $f>-2$ al disc obert i $\inf f=-2$ (quan $(x,y)\to(-1,0)$), però no s'assoleix.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [critics] Punts crítics  (teoria: T5.23, T5.22)
     objectiu: Trobar els punts crítics de $f$ al disc obert.
     idea: El disc és obert: un extrem absolut hi ha de ser extrem local, per tant punt crític.
     detall: $f_x=1-2x=0$, $f_y=-2y=0$: únic punt crític $\left(\frac12,0\right)$, que és del disc, amb $f=\frac14$.
  2. [maxim] És màxim absolut  (teoria: T5.33)
     objectiu: Decidir si el punt crític és un extrem absolut.
     idea: Completar quadrats per escriure $f$ com una constant menys una suma de quadrats (o mirar la hessiana i la concavitat).
     detall: $f=\frac14-\left(x-\frac12\right)^2-y^2\le\frac14$, amb igualtat només a $\left(\frac12,0\right)$: és el màxim absolut, de valor $\frac14$. (La hessiana $\begin{pmatrix}-2&0\\0&-2\end{pmatrix}$ és definida negativa.)
  3. [minim] El mínim  (teoria: T5.23, T5.22)
     objectiu: Decidir si $f$ té mínim absolut al disc obert.
     idea: Recordar quina condició ha de complir un extrem absolut d'una funció diferenciable en un obert i contrastar-la amb els punts crítics trobats. Per descriure bé la situació, estudiar els valors de $f$ prop de la circumferència: quin és l'ínfim i si s'assoleix.
     detall: Un mínim absolut al disc obert seria un mínim local i, per tant, un punt crític; l'únic punt crític és $\left(\frac12,0\right)$, que és el màxim estricte, de manera que $f$ no té mínim absolut. Per entendre-ho: a la circumferència $x^2+y^2=1$ seria $f=x-1$, amb mínim $-2$ a $(-1,0)$, que no és del disc. Al disc, $f=x-(x^2+y^2)>x-1>-2$ (perquè $x^2+y^2<1$ i $x>-1$), i $f(x,0)\to-2$ quan $x\to-1^+$. Per tant $\inf f=-2$ però no s'assoleix: no hi ha mínim absolut.
ERRORS COMUNS:
  - [weierstrass_obert] Aplica Weierstrass al disc obert com si fos compacte i busca el mínim a la frontera.
  - [minim_a_frontera] Dona com a mínim $-2$ en $(-1,0)$.
  - [local_vs_absolut] Classifica $\left(\frac12,0\right)$ com a màxim local i no justifica que sigui absolut.

TEORIA DEL CURS QUE FA SERVIR:
[T1.11] Definició 11 (Tema 1) — Boles, oberts i tancats
Sigui $(M,d)$ un espai mètric i sigui $x\in M$ un element. Aleshores, es defineix:

i) _Bola oberta_ de centre $x$ i radi $r>0$: $B_r(x)=B(x,r)=\{y\in M\mid d(x,y)<r\}$.

ii) _Bola tancada_ de centre $x$ i radi $r>0$: $\overline{B}_r(x)=\overline{B}(x,r)=\{y\in M\mid d(x,y)\leq r\}$.

iii) $A$ és un _conjunt obert_ de $M\Leftrightarrow A\subseteq M$ i per a tot $x\in A$ existeix $r>0$ tal que $B_r(x)\subseteq A$.

iv) $A$ és un _conjunt tancat_ de $M\Leftrightarrow A^c=M\setminus A$, el seu complementari a $M$, és obert.

Noteu que sempre $x\in B(x,r)$ i $x\in\overline{B}(x,r)$.

[T5.23] Proposició 23 (Tema 5) — Els extrems són punts crítics
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció diferenciable en $\mathbf{a}\in\Omega$. Si $\mathbf{a}$ és un extrem (és a dir, un màxim o un mínim) local de $f$, llavors $\mathbf{a}$ és un punt crític de $f$.

[T5.22] Definició 22 (Tema 5) — Punt crític
$\mathbf{a}\in\Omega$ és un punt crític de $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si $f$ és diferenciable en $\mathbf{a}$ i $Df(\mathbf{a})=0$.

[T5.33] Teorema 33 (Tema 5) — Condicions suficients d'extrem
(condicions suficients). Sigui $\Omega\subseteq\mathbb{R}^n$ un obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$, i $\mathbf{a}\in\Omega$ un punt crític de $f$. Aleshores,

(i) $q_{Hf(\mathbf{a})}$ és definida positiva $\Rightarrow$ $\mathbf{a}$ és un mínim local estricte de $f$.

(ii) $q_{Hf(\mathbf{a})}$ és definida negativa $\Rightarrow$ $\mathbf{a}$ és un màxim local estricte de $f$.

(iii) $q_{Hf(\mathbf{a})}$ és indefinida $\Rightarrow$ $\mathbf{a}$ és un punt de sella de $f$.

(iv) $\mathbf{a}$ és un mínim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida positiva.

(v) $\mathbf{a}$ és un màxim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida negativa.
</solucio_de_referencia>

### Document a revisar

[1] Les derivades $f_x=1-2x$ i $f_y=-2y$ s'anul·len només a $\left(\frac12,0\right)$, que és del disc perquè $\frac14<1$; hi val $f\left(\frac12,0\right)=\frac12-\frac14=\frac14$.
[2] Completant quadrats, $f(x,y)=\frac14-\left(x-\frac12\right)^2-y^2\leq\frac14$, amb igualtat només a $\left(\frac12,0\right)$. Per tant el màxim absolut és $\frac14$, assolit a $\left(\frac12,0\right)$.
[3] Per al mínim, observem que el disc és obert, de manera que no s'hi pot aplicar el teorema de Weierstrass i, per tant, $f$ no hi té mínim absolut.
[4] Ho podem confirmar: si $f$ tingués un mínim absolut en un punt del disc, com que el disc és obert, seria un mínim local i, per tant, un punt crític. L'únic punt crític és $\left(\frac12,0\right)$, que és el màxim estricte, així que no hi ha mínim absolut.
[5] Per veure què passa, fitem $f$: al disc, $x^2+y^2<1$, de manera que $f=x-(x^2+y^2)<x-1$, i com que $x>-1$, obtenim $f>-2$.
[6] A més, $f(x,0)=x-x^2\to-2$ quan $x\to-1^+$, de manera que $\inf f=-2$, però aquest valor no s'assoleix al disc.


## t6-10b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considereu la funció $f\colon\mathbb{R}^2\to\mathbb{R}$ definida per $f(x,y)=\sin(x+y)+\cos(x-y)$.

(b) Calculeu els extrems absoluts de $f$ en el quadrat $[\pi/2,\pi]\times[\pi/2,\pi]$.
RESULTAT CORRECTE: Màxim absolut $1$, assolit en $\left(\frac{\pi}{2},\frac{\pi}{2}\right)$ i en $(\pi,\pi)$.
Mínim absolut $-1$, assolit en $\left(\frac{\pi}{2},\pi\right)$ i en $\left(\pi,\frac{\pi}{2}\right)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [interior] Punts crítics a l'interior  (teoria: T5.23, T2.23)
     objectiu: Usant l'apartat (a), trobar els punts crítics de $f$ a l'interior del quadrat i el valor de $f$ en ells.
     idea: Mirar quins valors poden prendre $x+y$ i $x-y$ dins el quadrat i quins punts crítics de (a) hi cauen.
     detall: Al quadrat, $x+y\in[\pi,2\pi]$ i $x-y\in[-\frac{\pi}{2},\frac{\pi}{2}]$. L'únic punt crític interior és $x+y=\frac{3\pi}{2}$, $x-y=0$: $\left(\frac{3\pi}{4},\frac{3\pi}{4}\right)$, un punt de sella amb $f=0$. Com que el quadrat és compacte, els extrems absoluts existeixen (Weierstrass) i han de ser a la frontera.
  2. [costats] Els quatre costats  (teoria: T6.1)
     objectiu: Estudiar $f$ sobre cadascun dels quatre costats del quadrat.
     idea: A cada costat una variable és constant: simplificar amb fórmules trigonomètriques i estudiar la monotonia de la funció d'una variable resultant.
     detall: $x=\frac{\pi}{2}$: $f=\cos y+\sin y$, derivada $\cos y-\sin y<0$ a $(\frac{\pi}{2},\pi)$: decreix de $1$ a $-1$.
$x=\pi$: $f=-\sin y-\cos y$: creix de $-1$ (a $y=\frac{\pi}{2}$) a $1$ (a $y=\pi$).
$y=\frac{\pi}{2}$: $f=\cos x+\sin x$: decreix de $1$ a $-1$.
$y=\pi$: $f=-\sin x-\cos x$: creix de $-1$ a $1$.
Els extrems de cada costat són als vèrtexs: $f\left(\frac{\pi}{2},\frac{\pi}{2}\right)=f(\pi,\pi)=1$ i $f\left(\frac{\pi}{2},\pi\right)=f\left(\pi,\frac{\pi}{2}\right)=-1$.
  3. [concloure] Concloure
     objectiu: Donar el màxim i el mínim absoluts i on s'assoleixen.
     idea: Comparar els valors de tots els candidats.
     detall: Candidats: $0$ (punt de sella interior), $1$ i $-1$ als vèrtexs. Màxim absolut $1$ en $\left(\frac{\pi}{2},\frac{\pi}{2}\right)$ i $(\pi,\pi)$; mínim absolut $-1$ en $\left(\frac{\pi}{2},\pi\right)$ i $\left(\pi,\frac{\pi}{2}\right)$.
ERRORS COMUNS:
  - [critics_fora] Pren com a candidats punts crítics de (a) que no són dins el quadrat, com $\left(\frac{\pi}{4},\frac{\pi}{4}\right)$.
  - [sella_com_extrem] Inclou el punt interior com a extrem, o creu que l'absència de màxims locals interiors vol dir que no hi ha màxim absolut.
  - [un_sol_vertex] Troba només un dels dos punts on s'assoleix cada extrem.

TEORIA DEL CURS QUE FA SERVIR:
[T1.24] Definició 24 (Tema 1) — Compacte i seqüencialment compacte
Sigui $(M,d)$ espai mètric, $A\subseteq M$.

i) $A$ és _compacte_ si tot recobriment per oberts de $A$ admet un subrecobriment finit, és a dir: si $A\subseteq\bigcup_{i\in I}U_i$, amb $U_i$ obert, aleshores existeixen $i_1,\ldots,i_k\in I$ tals que $A\subseteq\bigcup_{j=1}^k U_{i_j}$.

ii) $A$ és _seqüencialment compacte_ si tota successió $(x_n)_{n\in\mathbb{N}}\subseteq A$ admet una subsuccessió (una parcial) convergent a un punt de $A$.

[T5.23] Proposició 23 (Tema 5) — Els extrems són punts crítics
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció diferenciable en $\mathbf{a}\in\Omega$. Si $\mathbf{a}$ és un extrem (és a dir, un màxim o un mínim) local de $f$, llavors $\mathbf{a}$ és un punt crític de $f$.

[T2.23] Teorema 23 (Tema 2) — Teorema de Weierstrass
(Weierstrass). Sigui $f:\Omega\subseteq M\to\mathbb{R}$ contínua i $K\subseteq\Omega$ compacte. Llavors $f(K)$ és fitat i $\exists x_0,x_1\in K$ t.q. $f(x_0)=\min_{x\in K}f(x)$ i $f(x_1)=\max_{x\in K}f(x)$.

[T6.1] Exemple 1 (Tema 6) — Exemple inicial d'extrems condicionats
Exemple inicial d'extrems condicionats i de varietat diferenciable.

Considerem la funció $f(x,y)=x^2+y^2$, amb $(x,y)\in\mathbb{R}^2$, i suposem que la volem maximitzar/minimitzar sobre una corba $M\subset\mathbb{R}^2$. Distingim dos casos:

- $M$ no està fitada, com ara una recta $ax+by=c$.
- $M$ és compacta, com ara una circumferència $x^2+y^2=2x$.

En el cas de la recta, si suposem, per exemple, que $b\neq 0$ (si $b=0$, canviem els papers de $x$ i $y$), podem aïllar $y=(-c-ax)/b$ i substituir a $f(x,y)$. Així
$$H(x):=f(x,y)|_M=x^2+\frac{(-c-a\,x)^2}{b^2}=\left(1+\frac{a^2}{b^2}\right)x^2+\frac{2ac}{b^2}x+\frac{c^2}{b^2}.$$
Com que $H$ és un polinomi, si volem trobar els candidats a extrems locals, fem
$$H'(x)=0\Leftrightarrow x=\frac{-ac}{a^2+b^2}.$$
Clarament, el punt trobat és un mínim local ja que $H''(x)>0$ per a tot $x\in\mathbb{R}$; a més, $H$ no té màxims locals ja que és una paràbola i $\displaystyle\lim_{x\to\pm\infty}H(x)=+\infty$.

També podem calcular
$$\begin{aligned}H\left(\frac{-ac}{a^2+b^2}\right)&=\frac{a^2+b^2}{b^2}\left(\frac{-ac}{a^2+b^2}\right)^2+\frac{2ac}{b^2}\left(\frac{-ac}{a^2+b^2}\right)+\frac{c^2}{b^2}\\&=\frac{a^2c^2}{b^2(a^2+b^2)}-\frac{2a^2c^2}{b^2(a^2+b^2)}+\frac{c^2(a^2+b^2)}{b^2(a^2+b^2)}=\frac{c^2}{a^2+b^2}.\end{aligned}$$

Representem gràficament la situació, dibuixant les corbes de nivell de $f(x,y)$ i la recta.

En la figura, hem triat $a=3$, $b=-1$ i $c=2$, amb la qual cosa el mínim (local) val $\frac{c^2}{a^2+b^2}=\frac{2}{5}$ i s'ateny al punt $(x,y)=\left(\frac{-ac}{a^2+b^2},(-c-a\frac{-ac}{a^2+b^2})/b\right)=\left(\frac{-ac}{a^2+b^2},\frac{-bc}{a^2+b^2}\right)=\left(-\frac35,\frac15\right)$. S'hi mostren (en vermell) les corbes de nivell $k\in\{\frac15,\frac25,\frac35,\frac45,1\}$ i la recta (en negre). Observem que just en el mínim local de $f$ sobre la recta, $\left(-\frac35,\frac15\right)$ hi ha una tangència. Veurem a continuació que això no és cap casualitat.

[Figura: corbes de nivell circulars de $f$ (en vermell) centrades a l'origen i la recta $3x-y=2$ (en negre), tangent a una corba de nivell en $(-3/5,1/5)$.]

Imaginem-nos que en el gràfic anterior la recta representa el traçat d'una trajectòria sobre les corbes de nivell d'un mapa. És clar que la tangència indica la mínima cota (si el valor de les corbes de nivell és creixent des del centre cap enfora) ja que no tallarà corbes de nivell més baix.

La condició de tangència és equivalent al fet que els vectors gradients $\nabla f$ i $\nabla\Phi$, amb $\Phi(x,y)=ax+by+c$, siguin paral·lels. Deixem com a exercici veure que imposant aquest paral·lelisme obtenim la mateixa solució.

En el cas de la circumferència donada per $x^2+y^2+2x=0$ (en negre a la gràfica de la dreta), resulta ser tangent a les corbes de nivell de $f(x,y)$ en els punts $(0,0)$ i $(2,0)$. De fet, ho podíem haver vist a cop d'ull ja que $x^2+y^2+2x=0$ equival a $(x-1)^2+y^2=1$ i és evident que el mínim de $x^2+y^2$ (distància a l'origen al quadrat) es pren a $(0,0)$ i el màxim es pren a $(2,0)$. A més, ambdós són extrems absoluts, que sabem que han d'existir ja que estem maximitzant/minimitzant una funció sobre un compacte.

[Figura: corbes de nivell circulars de $f$ (en vermell) i la circumferència $(x-1)^2+y^2=1$ (en negre).]

Una altra manera de resoldre aquest darrer exemple seria parametritzant la circumferència $x^2+y^2+2x=0$ per $\rho(t)=(x(t),y(t))=(1+\cos t,\sin t)$ i substituint a $f(x)$:
$$F(t):=f(x(t),y(t))=(1+\cos t)^2+\sin^2t=2+2\cos t,\qquad t\in[0,2\pi].$$
És immediat veure que $F'(t)=0$ per a $t\in(0,2\pi)$ si i només si $t=\pi$; a més, $F''(\pi)>0$. Com que $[0,2\pi]$ és compacte, existeixen els extrems absoluts: el mínim absolut $F=0$ es pren en $t=\pi$, és a dir, per a $(x,y)=(0,0)$, i el màxim absolut s'ateny en els extrems de l'interval: $F(0)=F(2\pi)=4$, és a dir, per a $(x,y)=(2,0)$.

Afegirem una tercera situació a aquest exemple: el cas que vulguem trobar els extrems absoluts en un domini del pla delimitat per diverses corbes. Prenem, per exemple,
$$D=\left\{(x,y)\in\mathbb{R}^2\ \middle|\ x^2+y^2-x\leq\frac34,\ y\geq x-\frac32\right\}.$$
Representem el domini $D$ (regió blava) conjuntament amb les corbes de nivell de $f(x,y)$ (en vermell). Intencionadament, hem marcat algunes corbes de nivell amb un traç més gruixut.

[Figura: domini $D$ (regió blava) limitat per la circumferència $x^2+y^2-x=3/4$ i la recta $y=x-3/2$, amb les corbes de nivell de $f$ en vermell.]

Fixem-nos que $D$ és un domini compacte i, per tant, la funció $f$, contínua arreu, hi prendrà un màxim absolut i un mínim absolut.

D'altra banda, les corbes que delimiten el domini, definides com a solucions de $x^2+y^2-x=\frac34$ i de $y=x-\frac32$, es tallen en els punts $(1/2,-1)$ i $(3/2,0)$ (cal substituir $y=x-\frac32$ en l'equació de la circumferència i resoldre).

Els extrems absoluts es podran prendre, o bé en l'interior de $D$, o bé damunt la circumferència $x^2+y^2-x=\frac34$ (sempre i quan estigui fent de frontera), o bé sobre el segment $\{(x,y)\mid y=x-3/2,\ x\in[1/2,3/2]\}$. Els estudiem un per un:

(i) Un extrem absolut en l'obert $\mathrm{int}(D)$ ha de ser, al mateix temps, extrem relatiu. Per tant, resolem $\nabla f(x,y)=(0,0)$ i obtenim que $(0,0)$ és un extrem relatiu (de fet, un mínim perquè $\lambda=2$ és un vap de la matriu hessiana de multiplicitat 2) i, per tant, un candidat a mínim absolut. (Nota: En aquest exemple, és evident que és mínim absolut ja que $f(x,y)=x^2+y^2>f(0,0)=0$ per a tot $(x,y)\in\mathbb{R}^2\setminus\{(0,0)\}$.)

(ii) Per a estudiar $f(x,y)$ sobre $x^2+y^2-x=\frac34$, ho podem fer de tres maneres:

- Substituint $y^2=\dfrac34+x-x^2$ en $f(x,y)=x^2+y^2$ i buscant els extrems absoluts de
$$F(x):=f(x,y)|_{y^2=\frac34+x-x^2},\qquad\text{per a }x\in[-1/2,3/2].$$
Observem que, en realitat, per a $(x,y)=(-1/2,0)$ i per a $(x,y)=(3/2,0)$, no podem posar $y$ en funció de $x$ ja que no es compleix la condició $\Phi_y=y\neq0$ del teorema de la funció implícita. Hauríem de fer-ho per a
$$y=\pm\sqrt{\frac34+x-x^2},\qquad x\in(-1/2,3/2),$$
i analitzar a posteriori quin valor pren la funció $f$ en $(x,y)=(-1/2,0)$ i $(x,y)=(3/2,0)$.
A efectes pràctics, com que només tenim un terme $y^2$, podem tractar els dos casos de cop:
$$F(x):=f(x,y)|_{y^2=\frac34+x-x^2}=x+\frac34$$
que, de manera òbvia, es veu que és creixent per a $x\in(-1/2,3/2)$. Així, doncs, el mínim es pren en $x=-1/2$ i el màxim en $x=3/2$, que corresponen als punts $P_1:=(-1/2,0)$ i $P_2:=(3/2,0)$, respectivament.
- Parametritzant el tros de circumferència com $\rho(t)=\{(\frac12+\cos t,\sin t),\ t\in[0,3\pi/2]\}$ i considerant
$$G(t):=f(x(t),y(t))=\left(\frac12+\cos t\right)^2+\sin^2t=\cos t+\frac54.$$
Clarament, els extrems absoluts de $G$ en $t\in[0,3\pi/2]$ es prenen per a $t=\pi$ (mínim) i per a $t=0$ (màxim), que corresponen als punts $P_1$ i $P_2$, respectivament (com no podria ser d'altra manera).
Com que estem cercant extrems absoluts en un interval tancat, hem de considerar també que els extrems de l'interval són candidats a ser-ho. En el cas de la parametrització, això ens obligaria a explorar el punt corresponent a $t=3\pi/2$, és a dir, $P_3:=(1/2,-1)$.
- Imposant que
$$\nabla f(x,y)=\lambda\nabla\Phi(x,y),$$
on $\Phi(x,y)=x^2+y^2-x-\frac34$, és a dir,
$$(2x,2y)=\lambda(2x-1,2y).$$
De la segona equació treiem que $\lambda=1$ o $y=0$. Si $\lambda=1$, la primera equació no té solució. Per tant, ens quedem només amb $y=0$ i, de $\Phi=0$ obtenim que $x^2-x-\frac34=0$, que té per solucions $x=-1/2$ i $x=3/2$, com ja havíem obtingut per altres mètodes. Tot i que ja no és rellevant, observem, que per a $x=-1/2$, s'obté $\lambda=1/2$, per a $x=3/2$, s'obté $\lambda=3/2$.

(iii) Per a estudiar $f(x,y)$ sobre la recta $y=x-\frac32$, per a $x\in[1/2,3/2]$, també es pot fer de diverses maneres, però ho farem només substituint per no fer l'estudi tan repetitiu:
$$H(x):=f(x,y)|_{y=x-\frac32}=2x^2-3x+9/4,$$
que no té solucions reals. Per tant, només pot prendre extrems absoluts en $x=1/2$ i en $x=3/2$, que corresponen, respectivament, als punts $P_2$ i $P_3$ ja definits anteriorment.

Malgrat tot, és interessant en aquest cas veure que el plantejament
$$\nabla f(x,y)=\lambda\nabla\Phi(x,y),$$
on $\Phi(x,y)=y-x+3/2$, ens duu a
$$(2x,2y)=\lambda(-1,1),$$
és a dir, o bé $\lambda=x=y=0$, que no és vàlida perquè $\Phi(0,0)\neq0$, o bé $x=-y=-\lambda/2$. Per a aquesta darrera opció, imposant que $\Phi(x,y)=0$, obtenim que $\lambda=-3$ i, per tant, $x=3/4$ i $y=-3/4$. No és un candidat a extrem absolut, però l'anomenem $P_4:=(3/4,-3/4)$ i li dedicarem un comentari al final.

Per a acabar l'exemple, avaluem $f(x,y)$ en tots els punts candidats:
$$f(0,0)=0;\ f(P_1)=1/4;\ f(P_2)=9/4;\ f(P_3)=5/4.$$
Per tant, el mínim absolut de $f$ s'ateny en $(0,0)$ i el màxim absolut, en $(3/2,0)$, com és ben evident a la figura ja que representen els contactes dins $D$ amb les corbes de nivell més baix i més alt, respectivament.

Fixem-nos que el punt $P_4$ representa un punt de sella condicionat perquè, per a tot $\epsilon>0$, existeixen punts $(x_1,y_1)$ i $(x_2,y_2)$ en $D\cap B(P_4,\epsilon)$ tals que $f(x_1,y_1)<f(P_4)<f(x_2,y_2)$.
</solucio_de_referencia>

### Document a revisar

[1] El quadrat $Q=[\pi/2,\pi]\times[\pi/2,\pi]$ és tancat i fitat, per tant compacte, i $f$ és contínua, així que pel teorema de Weierstrass $f$ té màxim i mínim absoluts a $Q$.
[2] Punts crítics: $f_x=\cos(x+y)-\sin(x-y)$ i $f_y=\cos(x+y)+\sin(x-y)$ s'anul·len si $\cos(x+y)=0$ i $\sin(x-y)=0$. A $Q$, $x+y\in[\pi,2\pi]$ i $x-y\in\left[-\frac{\pi}{2},\frac{\pi}{2}\right]$, i l'única possibilitat és $x+y=\frac{3\pi}{2}$, $x-y=0$: el punt interior $\left(\frac{3\pi}{4},\frac{3\pi}{4}\right)$, amb $f=\sin\frac{3\pi}{2}+\cos0=0$.
[3] La hessiana en aquest punt és $\begin{pmatrix}0&2\\2&0\end{pmatrix}$; com que la traça és $0$, el criteri de la hessiana no decideix el seu caràcter, però és igualment un candidat amb $f=0$.
[4] Costat $x=\frac{\pi}{2}$: $f=\sin\left(\frac{\pi}{2}+y\right)+\cos\left(\frac{\pi}{2}-y\right)=\cos y+\sin y$, amb derivada $\cos y-\sin y<0$ a $\left(\frac{\pi}{2},\pi\right)$: decreix de $1$ a $-1$. Costat $x=\pi$: $f=\sin(\pi+y)+\cos(\pi-y)=-\sin y-\cos y$, que creix de $-1$ a $1$.
[5] Per la simetria $f(x,y)=f(y,x)$, el costat $y=\frac{\pi}{2}$ es comporta com el costat $x=\pi$, i el costat $y=\pi$ com el costat $x=\frac{\pi}{2}$.
[6] Per tant, a la frontera els valors extrems són als vèrtexs: $f\left(\frac{\pi}{2},\frac{\pi}{2}\right)=f(\pi,\pi)=1$ i $f\left(\frac{\pi}{2},\pi\right)=f\left(\pi,\frac{\pi}{2}\right)=-1$.
[7] Comparant els candidats ($0$ a l'interior i $\pm1$ a la frontera), el màxim absolut és $1$, assolit a $\left(\frac{\pi}{2},\frac{\pi}{2}\right)$ i a $(\pi,\pi)$, i el mínim absolut és $-1$, assolit a $\left(\frac{\pi}{2},\pi\right)$ i a $\left(\pi,\frac{\pi}{2}\right)$.


## t6-13:dificil

### Referència

<solucio_de_referencia>
ENUNCIAT: Calculeu el màxim volum d'un paral·lelepípede de cares paral·leles als plans coordenats, inscrit dins l'el·lipsoide d'equació $\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}=1$, amb $a,b,c\in\mathbb{R}^+$.
RESULTAT CORRECTE: $V_{\max}=\dfrac{8abc}{3\sqrt3}=\dfrac{8\sqrt3}{9}abc$, per al paral·lelepípede de vèrtexs $\left(\pm\frac{a}{\sqrt3},\pm\frac{b}{\sqrt3},\pm\frac{c}{\sqrt3}\right)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [plantejament] Plantejar el problema  (teoria: T1.34, T2.23, T6.2, T6.12)
     objectiu: Escriure el volum com una funció a maximitzar sobre l'el·lipsoide i justificar que el màxim existeix.
     idea: Per simetria, el paral·lelepípede està centrat a l'origen i queda determinat pel vèrtex del primer octant. Restringir-se a la part de l'el·lipsoide amb coordenades no negatives, que és compacta.
     detall: Si els vuit vèrtexs són a l'el·lipsoide, dos vèrtexs que només difereixen en $x$ compleixen $x_1^2=x_2^2$, així que el paral·lelepípede és $[-x,x]\times[-y,y]\times[-z,z]$ i $V=8xyz$ amb $(x,y,z)$ a l'el·lipsoide, $x,y,z\ge0$. Aquest conjunt $S^+$ és compacte i $V$ és contínua: hi ha màxim. Com que $V=0$ quan alguna coordenada és $0$ i $V>0$ en altres punts, el màxim és en un punt amb $x,y,z>0$; com que aquests punts formen un obert de l'el·lipsoide, és un màxim local de $V$ condicionat a l'el·lipsoide, que és una 2-varietat ($\nabla\Phi=\left(\frac{2x}{a^2},\frac{2y}{b^2},\frac{2z}{c^2}\right)\neq0$ sobre ell).
  2. [lagrange] Sistema de Lagrange  (teoria: T6.17)
     objectiu: Escriure les equacions de Lagrange i obtenir una relació entre les coordenades.
     idea: Multiplicar cada equació per la variable corresponent: els tres membres esquerres es tornen iguals.
     detall: $8yz=\lambda\frac{2x}{a^2}$, $8xz=\lambda\frac{2y}{b^2}$, $8xy=\lambda\frac{2z}{c^2}$. Multiplicant per $x$, $y$, $z$ respectivament: $8xyz=2\lambda\frac{x^2}{a^2}=2\lambda\frac{y^2}{b^2}=2\lambda\frac{z^2}{c^2}$. Com que $xyz>0$, $\lambda\neq0$ i $\frac{x^2}{a^2}=\frac{y^2}{b^2}=\frac{z^2}{c^2}$.
  3. [resoldre] Resoldre i calcular el volum
     objectiu: Trobar el vèrtex òptim i el volum màxim.
     idea: Substituir la relació obtinguda a l'equació de l'el·lipsoide.
     detall: Cada quocient val $\frac13$: $x=\frac{a}{\sqrt3}$, $y=\frac{b}{\sqrt3}$, $z=\frac{c}{\sqrt3}$. És l'únic candidat amb $x,y,z>0$, per tant és el màxim: $V=8\frac{abc}{3\sqrt3}=\frac{8abc}{3\sqrt3}=\frac{8\sqrt3}{9}abc$.
ERRORS COMUNS:
  - [volum_xyz] Pren com a volum $xyz$ en lloc de $8xyz$ (confon el vèrtex amb les arestes).
  - [sense_existencia] Troba el punt crític de Lagrange i afirma que és el màxim sense cap argument d'existència.
  - [dividir_lambda] Divideix les equacions sense justificar que $x,y,z,\lambda\neq0$.

TEORIA DEL CURS QUE FA SERVIR:
[T6.12] Definició 12 (Tema 6) — Extrems condicionats
Siguin $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geq1$, $D\subseteq\mathbb{R}^n$ un obert tal que $M\subseteq D$ i $f\colon D\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(D)$. Diem que un punt $\mathbf{a}\in M$ és un màxim local de $f$ condicionat a $M$ si $\mathbf{a}$ és un màxim local de $f|_M$; és a dir, si existeix un obert $G$ tal que $\mathbf{a}\in G$ i $f(\mathbf{x})\leq f(\mathbf{a})$ per a tot $x\in M\cap G$.

Definim mínim condicionat i màxim i mínim estrictes condicionats d'una manera semblant, canviant $\leq$ per la desigualtat que pertoqui. Per ser punt de sella condicionat, cal que, per a tot obert $G$ tal que $\mathbf{a}\in G$, existeixin $\mathbf{x},\mathbf{y}\in M\cap G$ tals que $f(\mathbf{x})<f(\mathbf{a})$ i $f(\mathbf{y})>f(\mathbf{a})$.

[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.

[T2.23] Teorema 23 (Tema 2) — Teorema de Weierstrass
(Weierstrass). Sigui $f:\Omega\subseteq M\to\mathbb{R}$ contínua i $K\subseteq\Omega$ compacte. Llavors $f(K)$ és fitat i $\exists x_0,x_1\in K$ t.q. $f(x_0)=\min_{x\in K}f(x)$ i $f(x_1)=\max_{x\in K}f(x)$.

[T6.2] Definició 2 (Tema 6) — Varietat en forma implícita
Una $m$-varietat de classe $r$ a $\mathbb{R}^n$ és un subconjunt no buit $M\subseteq\mathbb{R}^n$ tal que per a tot $\mathbf{a}\in M$ existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i una funció $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$ amb $\mathrm{rang}\left(D\Phi(\mathbf{x})\right)=n-m$ per a tot $\mathbf{x}\in G$, tals que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.

En aquest context, es diu que $M$ és la $m$-varietat associada a $\Phi$; per reforçar aquesta relació amb $\Phi$, de vegades la denotarem amb $M_\Phi$.

$M$ també s'acostuma a anomenar (sub)varietat (diferenciable, $\mathcal{C}^r$ o de classe $r$) de dimensió $m$ en $\mathbb{R}^n$.

[T6.17] Corol·lari 17 (Tema 6) — Teorema dels multiplicadors de Lagrange
(Teorema dels multiplicadors de Lagrange). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ de classe $\mathcal{C}^r$, $M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(G)$. Si $\mathbf{a}\in M_\Phi$ és un extrem local de $f$ condicionat a $M_\Phi$, aleshores existeixen uns valors únics $\lambda_1,\ldots,\lambda_{n-m}\in\mathbb{R}$ tals que $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in G\times\mathbb{R}^{n-m}$ és un punt crític de $L$, és a dir, $(\mathbf{a},\boldsymbol{\lambda})$ és solució del sistema de $2n-m$ equacions
$$\begin{cases}\nabla f(\mathbf{a})-\lambda_1\nabla\Phi_1(\mathbf{a})-\cdots-\lambda_{n-m}\nabla\Phi_{n-m}(\mathbf{a})&=\mathbf{0},\\\Phi(\mathbf{a})&=\mathbf{0}.\end{cases}$$
</solucio_de_referencia>

### Document a revisar

[1] Un paral·lelepípede de cares paral·leles als plans coordenats inscrit a l'el·lipsoide té els vuit vèrtexs sobre l'el·lipsoide. Dos vèrtexs que només difereixen en la coordenada $x$ compleixen $x_1^2=x_2^2$, i per tant $x_2=-x_1$; igual amb $y$ i $z$. Així el paral·lelepípede és $[-x,x]\times[-y,y]\times[-z,z]$ i el seu volum és $V=8xyz$, amb $(x,y,z)$ a l'el·lipsoide i $x,y,z>0$.
[2] El conjunt $S^+$ dels punts de l'el·lipsoide amb $x,y,z>0$ és fitat i $V$ hi és contínua, de manera que, pel teorema de Weierstrass, $V$ assoleix un màxim a $S^+$.
[3] El conjunt $S^+$ és un obert de l'el·lipsoide, que és una 2-varietat perquè $\nabla\Phi=\left(\frac{2x}{a^2},\frac{2y}{b^2},\frac{2z}{c^2}\right)\neq(0,0,0)$ sobre ell; per tant el màxim és un extrem local de $V$ condicionat a l'el·lipsoide i podem aplicar Lagrange.
[4] Les equacions de Lagrange són $8yz=\lambda\frac{2x}{a^2}$, $8xz=\lambda\frac{2y}{b^2}$ i $8xy=\lambda\frac{2z}{c^2}$. Multiplicant-les per $x$, $y$ i $z$ respectivament: $8xyz=2\lambda\frac{x^2}{a^2}=2\lambda\frac{y^2}{b^2}=2\lambda\frac{z^2}{c^2}$.
[5] Com que $\nabla\Phi\neq0$, el multiplicador $\lambda$ no és nul i podem dividir per $2\lambda$: $\frac{x^2}{a^2}=\frac{y^2}{b^2}=\frac{z^2}{c^2}$. Com que la seva suma és $1$, cadascun val $\frac13$: $x=\frac{a}{\sqrt3}$, $y=\frac{b}{\sqrt3}$, $z=\frac{c}{\sqrt3}$.
[6] És l'únic candidat de $S^+$, i la hessiana de $V=8xyz$ en aquest punt és definida negativa, de manera que és el màxim: $V_{\max}=8\cdot\frac{abc}{3\sqrt3}=\frac{8abc}{3\sqrt3}=\frac{8\sqrt3}{9}abc$.

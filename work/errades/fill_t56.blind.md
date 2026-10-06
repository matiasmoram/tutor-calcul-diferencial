## t5-1a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Trobeu els polinomis de Taylor de grau $\leq k$, centrats a $p$, de les funcions següents:

(a) $f(x,y,z)=xyz$, $k\in\mathbb{N}$, $p=(1,-1,0)$;
RESULTAT CORRECTE: Amb $u=x-1$, $v=y+1$, $w=z$ es té $xyz=-w-uw+vw+uvw$. Per tant:
$P_0=0$; $P_1=-z$; $P_2=-z-(x-1)z+(y+1)z$; i per a tot $k\geq 3$, $P_k=-z-(x-1)z+(y+1)z+(x-1)(y+1)z=xyz$ (el residu és idènticament nul).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [canvi_variables] Escriure $f$ en potències dels increments  (teoria: T5.16)
     objectiu: Expressar $f$ com un polinomi en les variables $x-1$, $y+1$ i $z$, que mesuren el desplaçament respecte de $p$.
     idea: Com que $f$ ja és un polinomi, n'hi ha prou de posar $x=1+u$, $y=-1+v$, $z=w$ i desenvolupar el producte. Per la unicitat del polinomi de Taylor, el polinomi que s'obté, agrupat per graus en $(u,v,w)$, ja dona tots els $P_k$. (Alternativament: calcular les derivades parcials de $f$ a $p$ i aplicar la fórmula de Taylor.)
     detall: $xyz=(1+u)(-1+v)\,w=(-1+v-u+uv)\,w=-w-uw+vw+uvw$, amb $u=x-1$, $v=y+1$, $w=z$. Equivalentment, amb derivades: $D_3f(p)=xy|_p=-1$, $D_{13}f(p)=y|_p=-1$, $D_{23}f(p)=x|_p=1$, $D_{123}f(p)=1$, i totes les altres derivades a $p$ són nul·les.
  2. [agrupar_graus] Separar per graus  (teoria: T5.12, T5.14)
     objectiu: Identificar les parts homogènies de cada grau del polinomi obtingut.
     idea: El polinomi de Taylor de grau $\leq k$ és la suma de les parts homogènies de grau $0,1,\dots,k$ en els increments.
     detall: Grau $0$: $0$ (perquè $f(p)=0$). Grau $1$: $-z$. Grau $2$: $-(x-1)z+(y+1)z$. Grau $3$: $(x-1)(y+1)z$. No hi ha termes de grau $\geq 4$.
  3. [concloure] Escriure $P_k$ per a cada $k$  (teoria: T5.14)
     objectiu: Donar $P_k$ per a tots els valors de $k\in\mathbb{N}$.
     idea: Distingir casos segons si $k$ és més petit o no que el grau total de $f$.
     detall: $P_0=0$, $P_1=-z$, $P_2=-z-(x-1)z+(y+1)z$, i per a $k\geq 3$ el polinomi de Taylor és tot el polinomi: $P_k=xyz$, perquè totes les derivades d'ordre $\geq 4$ són nul·les i el residu és $0$.
ERRORS COMUNS:
  - [centrat_origen] Escriu el polinomi en potències de $x,y,z$ (centrat a l'origen) en lloc de potències de $x-1$, $y+1$, $z$; per exemple conclou que $P_1=0$ o $P_2=0$.
  - [signe_canvi] S'equivoca de signe en el canvi de variable (per exemple $y=1+v$).
  - [graus_superiors] Creu que per a $k$ gran apareixen termes nous, o no reconeix que per a $k\geq 3$ el polinomi coincideix amb $f$.

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

[T5.16] Observació 16 (Tema 5) — Unicitat del polinomi de Taylor
Per a una funció $f\in\mathcal{C}^{r+1}(\Omega)$, el seu polinomi de Taylor de grau $r$, $P_r(\mathbf{x})$, és l'únic polinomi de grau $\leqslant r$ que compleix $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-P_r(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$

[T5.12] Definició 12 (Tema 5) — Multiíndex, monomi i homogeneïtat
- Per a polinomis de diverses variables, escriurem
  $$p(\mathbf{x})=\sum_{m=0}^{r}\ \sum_{\substack{\alpha_1,\ldots,\alpha_n\\ \alpha_1+\cdots+\alpha_n=m}}a_{\alpha_1,\ldots,\alpha_n}\,x_1^{\alpha_1}\ldots x_n^{\alpha_n}.$$
  Per fer la notació més compacta, definim el multiíndex $\alpha=(\alpha_1,\ldots,\alpha_n)\in\mathbb{N}^n$ de manera que $\mathbf{x}^\alpha=x_1^{\alpha_1}\ldots x_n^{\alpha_n}$, on $\mathbf{x}=(x_1,\ldots,x_n)$. Llavors, un polinomi de grau $r$ en $n$ variables s'escriu com
  $$p(x)=\sum_{m=0}^{r}\ \sum_{|\alpha|=m}a_\alpha\,\mathbf{x}^\alpha,$$
  on $|\alpha|=\alpha_1+\cdots+\alpha_n$ s'anomena el grau d'$\alpha$.
- Cada element $\mathbf{x}^\alpha$ s'anomena monomi. (Nota: En alguns textos, la definició de monomi conté el coeficient: $a_\alpha\,\mathbf{x}^\alpha$.) Observem que hi ha $n^r$ monomis de grau $r$ si suposem que $x_ix_j$ i $x_jx_i$, per a tot $i,j$, no són el mateix monomi.
- El factorial d'un multiíndex es defineix com $\alpha!=\alpha_1!\ldots\alpha_n!$
- Una funció de $n$ variables és homogènia de grau $r$ si existeix un $r\in\mathbb{N}$ tal que
  $$f(\lambda\,\mathbf{x})=\lambda^r\,f(\mathbf{x});$$
  fixem-nos que els polinomis homogenis ho compleixen clarament.
</solucio_de_referencia>

### Document a revisar

[1] Fem el canvi $u=x-1$, $v=y+1$, $w=z$, que mesura el desplaçament respecte de $p=(1,-1,0)$: així $x=1+u$, $y=-1+v$ i $z=w$.
[2] Com que $f$ és un polinomi, desenvolupem el producte: $xyz=(1+u)(-1+v)\,w=(-1+v-u+uv)\,w=-w-uw+vw+uvw$. Per la unicitat del polinomi de Taylor, n'hi ha prou d'agrupar aquesta expressió per graus en $(u,v,w)$.
[3] Com a comprovació, amb derivades: $D_3f(p)=xy|_p=-1$, $D_{13}f(p)=y|_p=-1$, $D_{23}f(p)=x|_p=1$ i $D_{123}f(p)=1$, i totes les altres derivades de $f$ a $p$ (llevat de les obtingudes permutant aquests índexs) són nul·les, d'acord amb els coeficients obtinguts.
[4] Separant per graus: grau $0$: $0$ (perquè $f(p)=0$); grau $1$: $-z$; grau $2$: $-(x-1)z+(y+1)z$; grau $3$: $(x-1)(y+1)z$. No hi ha termes de grau $\geq4$.
[5] Per tant $P_0=0$, $P_1=-z$ i el polinomi de Taylor de grau $\leq2$ és $P_2=-(x-1)z+(y+1)z$.
[6] Per a $k\geq3$, el polinomi de Taylor és tot el polinomi: $P_k=-z-(x-1)z+(y+1)z+(x-1)(y+1)z=xyz$, ja que $f$ té grau $3$ i, per tant, totes les seves derivades d'ordre $\geq3$ són nul·les i el residu és $0$.


## t5-2:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Siguin $\varphi:\mathbb{R}\to\mathbb{R}$ una funció de classe $\mathcal{C}^3(\mathbb{R})$ i $a\in\mathbb{R}$. Calculeu el polinomi de Taylor de grau 3 centrat a l'origen de la funció $f:\mathbb{R}^m\to\mathbb{R}$ definida per $f(x_1,\cdots,x_m)=\varphi\left(e^{a\sum_{i=1}^{m}x_i}\right)$.
RESULTAT CORRECTE: Amb $S=x_1+\cdots+x_m$:
$P_3(\mathbf{x})=\varphi(1)+a\varphi'(1)\,S+\dfrac{a^2\left(\varphi'(1)+\varphi''(1)\right)}{2}S^2+\dfrac{a^3\left(\varphi'(1)+3\varphi''(1)+\varphi'''(1)\right)}{6}S^3$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [reduir_una_variable] Reduir a una funció d'una variable  (teoria: T3.21, T5.14)
     objectiu: Relacionar les derivades parcials de $f$ amb les derivades d'una funció d'una sola variable.
     idea: Posar $g(s)=\varphi(e^{as})$, de manera que $f(\mathbf{x})=g(x_1+\cdots+x_m)$, i aplicar la regla de la cadena: cada derivada parcial de la suma respecte de qualsevol $x_i$ val $1$.
     detall: $D_{i_1\cdots i_k}f(\mathbf{x})=g^{(k)}(x_1+\cdots+x_m)$ per a qualsevol tria d'índexs $i_1,\dots,i_k$ i $k\leq 3$ (en particular $f\in\mathcal{C}^3$). Al terme d'ordre $k$ de la fórmula de Taylor: $\sum_{i_1,\dots,i_k}D_{i_1\cdots i_k}f(\mathbf{0})\,x_{i_1}\cdots x_{i_k}=g^{(k)}(0)\,(x_1+\cdots+x_m)^k$.
  2. [derivades_g] Derivades de $g$ a $0$  (teoria: T3.21)
     objectiu: Calcular $g(0)$, $g'(0)$, $g''(0)$ i $g'''(0)$.
     idea: Derivar $g(s)=\varphi(e^{as})$ amb la regla de la cadena i la del producte (una variable), i avaluar a $s=0$, on $e^{as}=1$.
     detall: $g'(s)=a e^{as}\varphi'(e^{as})$; $g''(s)=a^2e^{as}\varphi'(e^{as})+a^2e^{2as}\varphi''(e^{as})$; $g'''(s)=a^3\left(e^{as}\varphi'(e^{as})+3e^{2as}\varphi''(e^{as})+e^{3as}\varphi'''(e^{as})\right)$. A $s=0$: $g(0)=\varphi(1)$, $g'(0)=a\varphi'(1)$, $g''(0)=a^2(\varphi'(1)+\varphi''(1))$, $g'''(0)=a^3(\varphi'(1)+3\varphi''(1)+\varphi'''(1))$.
  3. [muntar] Muntar el polinomi  (teoria: T5.14)
     objectiu: Escriure el polinomi de Taylor de grau $3$ de $f$ a l'origen.
     idea: Substituir els valors $g^{(k)}(0)$ al terme d'ordre $k$ de la fórmula de Taylor, amb el factor $\frac{1}{k!}$.
     detall: $P_3=\varphi(1)+a\varphi'(1)S+\frac{a^2(\varphi'(1)+\varphi''(1))}{2}S^2+\frac{a^3(\varphi'(1)+3\varphi''(1)+\varphi'''(1))}{6}S^3$, amb $S=x_1+\cdots+x_m$.
ERRORS COMUNS:
  - [sense_termes_creuats] Pensa que només hi ha derivades pures i escriu $\sum_i x_i^2$ en lloc de $\left(\sum_i x_i\right)^2$ (oblida les derivades creuades).
  - [regla_producte] En derivar $a e^{as}\varphi'(e^{as})$ oblida un dels dos factors que depenen de $s$ (per exemple obté $g''=a^2e^{2as}\varphi''$).
  - [avaluar_a_zero] Avalua $\varphi$ i les seves derivades a $0$ en lloc d'$1$.

TEORIA DEL CURS QUE FA SERVIR:
[T5.3] Definició 3 (Tema 5) — Funció de classe C^r
Direm que una funció $f:\Omega\subset\mathbb{R}^n\to\mathbb{R}^m$ és de classe $\mathcal{C}^r$ si totes les derivades fins a ordre $r$ existeixen i són contínues.

Equivalentment, $f:\Omega\subset\mathbb{R}^n\to\mathbb{R}^m$ és de classe $\mathcal{C}^r\Leftrightarrow Df$ és de classe $\mathcal{C}^{r-1}$.

[T5.14] Teorema 14 (Tema 5) — Teorema de Taylor (diverses variables)
(de Taylor). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^{r+1}(\Omega)$, i $\mathbf{a}\in\Omega$. Per a tot $\mathbf{x}\in\Omega$ amb $[\mathbf{a},\mathbf{x}]\subseteq\Omega$, existeix $\xi_\mathbf{x}\in(\mathbf{a},\mathbf{x})$ tal que $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$, on

(i) El polinomi
$$\begin{aligned}P_r(\mathbf{x})={}&f(\mathbf{a})+\sum_{i=1}^{n}D_if(\mathbf{a})(x_i-a_i)+\frac{1}{2!}\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_i)(x_j-a_j)+\cdots\\
&\cdots+\frac{1}{r!}\sum_{i_1,\ldots,i_r=1}^{n}D_{i_1,\ldots,i_r}f(\mathbf{a})(x_{i_1}-a_{i_1})\cdots(x_{i_r}-a_{i_r})\end{aligned}$$
s'anomena el polinomi de Taylor de grau $r$ de la funció $f$ en el punt $\mathbf{a}$,

(ii) El residu de grau $r$ de la funció $f$ en el punt $\mathbf{a}$ és
$$R_{r+1}(\mathbf{x})=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})(x_{i_1}-a_{i_1})\cdots(x_{i_{r+1}}-a_{i_{r+1}}).$$
A més, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$
</solucio_de_referencia>

### Document a revisar

[1] Sigui $g(s)=\varphi(e^{as})$, de manera que $f(\mathbf{x})=g(x_1+\cdots+x_m)$. Com que $\varphi$ és de classe $\mathcal{C}^3$ i $s\mapsto e^{as}$ és de classe $\mathcal{C}^\infty$, $g$ és de classe $\mathcal{C}^3$, i per tant $f$ és de classe $\mathcal{C}^\infty$.
[2] Per la regla de la cadena, com que $\partial(x_1+\cdots+x_m)/\partial x_i=1$, es té $D_if(\mathbf{x})=g'(x_1+\cdots+x_m)$, i iterant, $D_{i_1\cdots i_k}f(\mathbf{x})=g^{(k)}(x_1+\cdots+x_m)$ per a qualsevol tria d'índexs $i_1,\dots,i_k$ i $k\leq3$.
[3] Amb $S=x_1+\cdots+x_m$, el terme d'ordre $k$ de la fórmula de Taylor a l'origen és $\frac{1}{k!}\sum_{i_1,\dots,i_k}D_{i_1\cdots i_k}f(\mathbf{0})\,x_{i_1}\cdots x_{i_k}=\frac{g^{(k)}(0)}{k!}S^k$, perquè la suma de tots els productes $x_{i_1}\cdots x_{i_k}$ és $S^k$. Així, $P_3=\sum_{k=0}^{3}\frac{g^{(k)}(0)}{k!}S^k$.
[4] Derivem $g$: $g'(s)=ae^{as}\varphi'(e^{as})$ i $g''(s)=a^2e^{as}\varphi'(e^{as})+a^2e^{2as}\varphi''(e^{as})$.
[5] A $s=0$, com que $e^0=1$: $g(0)=\varphi(1)$, $g'(0)=a\varphi'(1)$ i $g''(0)=a^2\left(\varphi'(1)+\varphi''(1)\right)$.
[6] Derivant un cop més, $g'''(s)=a^3\left(e^{as}\varphi'(e^{as})+2e^{2as}\varphi''(e^{as})+e^{3as}\varphi'''(e^{as})\right)$, i per tant $g'''(0)=a^3\left(\varphi'(1)+2\varphi''(1)+\varphi'''(1)\right)$.
[7] Per tant, amb $S=x_1+\cdots+x_m$, $P_3(\mathbf{x})=\varphi(1)+a\varphi'(1)\,S+\frac{a^2\left(\varphi'(1)+\varphi''(1)\right)}{2}S^2+\frac{a^3\left(\varphi'(1)+2\varphi''(1)+\varphi'''(1)\right)}{6}S^3$.


## t5-7a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considereu la funció $f(x,y)=(y-3x^2)(y-x^2)$.

(a) Proveu que l'origen n'és l'únic punt crític, i estudieu-ne el caràcter.
RESULTAT CORRECTE: $f_x=4x(3x^2-2y)$, $f_y=2y-4x^2$ s'anul·len només a $(0,0)$. La hessiana a l'origen és $\begin{pmatrix}0&0\\0&2\end{pmatrix}$ (semidefinida, no decideix). Com que $f<0$ entre les dues paràboles $y=x^2$ i $y=3x^2$ (per exemple $f(x,2x^2)=-x^4$) i $f>0$ fora (per exemple $f(0,y)=y^2$), l'origen és un punt de sella.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [punts_critics] Trobar els punts crítics  (teoria: T5.22)
     objectiu: Veure que l'únic punt on s'anul·len les dues derivades parcials és l'origen.
     idea: Desenvolupar $f$ (o derivar el producte), resoldre l'equació més senzilla per expressar $y$ en funció de $x$ i substituir a l'altra.
     detall: $f=y^2-4x^2y+3x^4$, $f_x=-8xy+12x^3=4x(3x^2-2y)$, $f_y=2y-4x^2$. De $f_y=0$, $y=2x^2$; substituint, $f_x=4x(3x^2-4x^2)=-4x^3=0$, d'on $x=0$ i $y=0$.
  2. [hessiana] Provar el criteri de la hessiana  (teoria: T5.32, T5.33)
     objectiu: Calcular la hessiana a l'origen i veure si permet decidir el caràcter del punt crític.
     idea: Calcular les derivades segones, avaluar-les a l'origen i mirar el signe de la forma quadràtica resultant.
     detall: $f_{xx}=36x^2-8y$, $f_{xy}=-8x$, $f_{yy}=2$. A l'origen, $Hf(0,0)=\begin{pmatrix}0&0\\0&2\end{pmatrix}$: valors propis $0$ i $2$, semidefinida positiva però no definida. Les condicions suficients no decideixen (només descarten que sigui un màxim local).
  3. [estudi_directe] Estudiar el signe de $f$ a prop de l'origen  (teoria: T5.25)
     objectiu: Decidir el caràcter de l'origen comparant $f$ amb $f(0,0)$ en punts propers.
     idea: $f$ és un producte de dos factors que s'anul·len sobre dues corbes que passen per l'origen: estudiar el signe de cada factor a les regions que determinen.
     detall: $f(0,0)=0$. Els factors s'anul·len a les paràboles $y=x^2$ i $y=3x^2$. Entre elles ($x^2<y<3x^2$) un factor és positiu i l'altre negatiu: $f<0$; per exemple $f(x,2x^2)=(-x^2)(x^2)=-x^4<0$ per a $x\neq0$. Fora d'elles, $f>0$; per exemple $f(0,y)=y^2>0$ per a $y\neq0$. Tota bola centrada a l'origen conté punts de tots dos tipus: l'origen és un punt de sella.
ERRORS COMUNS:
  - [hessiana_semidefinida_minim] Com que la hessiana és semidefinida positiva, conclou que l'origen és un mínim local.
  - [nomes_rectes] Estudia $f$ només sobre rectes que passen per l'origen (on sempre té mínim) i conclou que l'origen és un mínim.
  - [perd_solucio] En resoldre el sistema divideix per $x$ i no comprova el cas $x=0$, o no justifica que no hi ha altres solucions.

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

[T5.25] Definició 25 (Tema 5) — Punt de sella
Un punt $\mathbf{a}\in\Omega$ és un punt de sella d'una funció diferenciable $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si és un punt crític de $f$ i per a tot $\epsilon>0$ existeixen $\mathbf{x},\mathbf{y}\in B(\mathbf{a},\epsilon)$ tals que $f(\mathbf{x})<f(\mathbf{a})<f(\mathbf{y})$.
</solucio_de_referencia>

### Document a revisar

[1] Desenvolupant, $f(x,y)=y^2-4x^2y+3x^4$, i les derivades parcials són $f_x=-8xy+12x^3=4x(3x^2-2y)$ i $f_y=2y-4x^2$.
[2] De $f_y=0$ obtenim $y=2x^2$, i substituint a l'altra equació, $f_x=4x(3x^2-2x^2)=4x^3=0$, d'on $x=0$ i, per tant, $y=0$. L'origen és l'únic punt crític.
[3] Derivades segones: $f_{xx}=36x^2-8y$, $f_{xy}=-8x$, $f_{yy}=2$, de manera que $Hf(0,0)=\begin{pmatrix}0&0\\0&2\end{pmatrix}$, amb valors propis $0$ i $2$: és semidefinida positiva però no definida, i el criteri de la hessiana no decideix (només descarta que l'origen sigui un màxim local).
[4] Estudiem directament el signe de $f$ a prop de l'origen, on $f(0,0)=0$. Els factors $y-3x^2$ i $y-x^2$ s'anul·len sobre les paràboles $y=3x^2$ i $y=x^2$, respectivament.
[5] Entre les dues paràboles, és a dir quan $x^2<y<3x^2$, es té $y-3x^2>0$ i $y-x^2<0$, de manera que $f<0$; per exemple, $f(x,2x^2)=(-x^2)(x^2)=-x^4<0$ per a $x\neq0$.
[6] Si $y<x^2$ o $y>3x^2$, els dos factors tenen el mateix signe i $f>0$; per exemple, $f(0,y)=y^2>0$ per a $y\neq0$.
[7] Tota bola centrada a l'origen conté punts $(x,2x^2)$ i $(0,y)$ amb $x,y\neq0$ petits, on $f<0$ i $f>0$ respectivament. Per tant l'origen no és un extrem local: és un punt de sella.


## t5-8a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Trobeu i classifiqueu tots els punts crítics de les funcions següents:

(a) $f(x,y)=(x-y)^3+(x+y)^2$;
RESULTAT CORRECTE: L'únic punt crític és $(0,0)$. La hessiana hi és $\begin{pmatrix}2&2\\2&2\end{pmatrix}$ (semidefinida positiva, no decideix). Sobre la recta $y=-x$, $f(x,-x)=8x^3$ canvia de signe: l'origen és un punt de sella.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [punts_critics] Trobar els punts crítics  (teoria: T5.22)
     objectiu: Trobar tots els punts on s'anul·len les dues derivades parcials.
     idea: Les dues derivades parcials comparteixen els mateixos termes amb signes diferents: sumar-les i restar-les dona dues equacions molt senzilles.
     detall: $f_x=3(x-y)^2+2(x+y)$, $f_y=-3(x-y)^2+2(x+y)$. Sumant: $4(x+y)=0$; restant: $6(x-y)^2=0$. Per tant $x=y$ i $x=-y$, i l'únic punt crític és $(0,0)$.
  2. [hessiana] Provar el criteri de la hessiana  (teoria: T5.32, T5.33, T5.30)
     objectiu: Calcular la hessiana a l'origen i veure si decideix.
     idea: Calcular les derivades segones, avaluar a l'origen i estudiar el signe de la forma quadràtica (determinant i traça).
     detall: $f_{xx}=6(x-y)+2$, $f_{xy}=-6(x-y)+2$, $f_{yy}=6(x-y)+2$. $Hf(0,0)=\begin{pmatrix}2&2\\2&2\end{pmatrix}$, $\det=0$, $\mathrm{tr}=4$: semidefinida positiva (valors propis $0$ i $4$). No decideix.
  3. [estudi_directe] Estudiar $f$ sobre la direcció degenerada  (teoria: T5.25)
     objectiu: Decidir el caràcter de l'origen estudiant directament el signe de $f$ a prop seu.
     idea: Restringir $f$ a la recta en la direcció del vector propi de valor propi $0$, on el terme quadràtic desapareix, i mirar el signe del que queda.
     detall: Sobre $y=-x$: $f(x,-x)=(2x)^3+0=8x^3$, positiu per a $x>0$ i negatiu per a $x<0$. Com que $f(0,0)=0$, tota bola centrada a l'origen conté punts amb $f>0$ i amb $f<0$: l'origen és un punt de sella.
ERRORS COMUNS:
  - [semidefinida_minim] Conclou que l'origen és un mínim perquè la hessiana és semidefinida positiva.
  - [direccio_equivocada] Estudia $f$ només sobre rectes com $y=0$ o $y=x$, on $f$ sembla tenir mínim, i conclou que és un mínim.

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

[T5.25] Definició 25 (Tema 5) — Punt de sella
Un punt $\mathbf{a}\in\Omega$ és un punt de sella d'una funció diferenciable $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si és un punt crític de $f$ i per a tot $\epsilon>0$ existeixen $\mathbf{x},\mathbf{y}\in B(\mathbf{a},\epsilon)$ tals que $f(\mathbf{x})<f(\mathbf{a})<f(\mathbf{y})$.
</solucio_de_referencia>

### Document a revisar

[1] Les derivades parcials són $f_x=3(x-y)^2+2(x+y)$ i $f_y=-3(x-y)^2+2(x+y)$.
[2] Sumant les equacions $f_x=0$ i $f_y=0$ obtenim $4(x+y)=0$, i restant-les, $6(x-y)^2=0$. Per tant $x=-y$ i $x=y$, i l'únic punt crític és $(0,0)$.
[3] Derivades segones: $f_{xx}=6(x-y)+2$, $f_{xy}=-6(x-y)+2$ i $f_{yy}=-6(x-y)+2$. A l'origen, $Hf(0,0)=\begin{pmatrix}2&2\\2&2\end{pmatrix}$.
[4] Com que $\det Hf(0,0)=0$ i $\mathrm{tr}\,Hf(0,0)=4$, els valors propis són $0$ i $4$: la hessiana és semidefinida positiva però no definida. El criteri no decideix, tot i que ja descarta que l'origen sigui un mínim local.
[5] Estudiem $f$ en la direcció del nucli de la hessiana, la recta $y=-x$: allà $x-y=2x$ i $x+y=0$, de manera que $f(x,-x)=(2x)^3=8x^3$.
[6] Com que $f(0,0)=0$ i $8x^3$ és positiu per a $x>0$ i negatiu per a $x<0$, tota bola centrada a l'origen conté punts amb $f>0$ i punts amb $f<0$: l'origen és un punt de sella.


## t5-9c:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem la funció $f(x,y)=(x^2+y^2+2x)\,x^3$.

(c) Useu els apartats anteriors per determinar si el punt $(0,0)$ és un extrem local de $f$.
RESULTAT CORRECTE: $(0,0)$ no és un extrem local de $f$: $f(0,0)=0$ i tota bola centrada a l'origen conté punts del semiplà $x>0$ (on $f>0$) i punts amb $x<0$ exteriors al disc (on $f<0$), per exemple $(-s,\sqrt{2s})$ amb $f=-s^5$. De fet, com que $Df(0,0)=0$, és un punt de sella.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [punts_positius] Punts propers amb $f>0$
     objectiu: Assumint els apartats (a) i (b), veure que tota bola centrada a l'origen conté punts on $f$ és més gran que $f(0,0)$.
     idea: Mirar quines regions de l'apartat (b) tenen l'origen a la seva frontera.
     detall: $f(0,0)=0$. Els punts $(t,0)$ amb $t>0$ petit són al semiplà $x>0$, on $f>0$ (per exemple $f(t,0)=t^5+2t^4>0$).
  2. [punts_negatius] Punts propers amb $f<0$
     objectiu: Veure que tota bola centrada a l'origen conté també punts on $f<0$.
     idea: La regió on $f<0$ és la part del semiplà esquerre fora del disc; com que la circumferència és tangent a l'eix vertical a l'origen, aquesta regió arriba fins a l'origen. Cal trobar una família explícita de punts en aquesta regió que tendeixin a l'origen.
     detall: Per a $s>0$ petit, el punt $(-s,\sqrt{2s})$ compleix $x^2+y^2+2x=s^2+2s-2s=s^2>0$ i $x<0$: és exterior al disc, i $f(-s,\sqrt{2s})=s^2\cdot(-s^3)=-s^5<0$. La seva distància a l'origen, $\sqrt{s^2+2s}$, tendeix a $0$.
  3. [concloure] Concloure  (teoria: T5.21, T5.25)
     objectiu: Decidir si l'origen és un extrem local de $f$.
     idea: Comparar amb la definició de màxim i mínim local: cap de les dues desigualtats es pot complir en tota una bola.
     detall: En tota bola $B((0,0),\epsilon)$ hi ha punts amb $f>f(0,0)$ i punts amb $f<f(0,0)$, de manera que l'origen no és ni màxim ni mínim local. Com que $f=2x^4+x^5+x^3y^2$ només té termes de grau $\geq4$, $Df(0,0)=0$: l'origen és un punt crític i, de fet, un punt de sella.
ERRORS COMUNS:
  - [nomes_eix_horitzontal] Mira $f$ només sobre l'eix $y=0$, on $f(x,0)=x^4(x+2)\geq0$ prop de l'origen, i conclou que l'origen és un mínim.
  - [regio_negativa_lluny] Creu que la regió on $f<0$ queda lluny de l'origen (a $x<-2$) perquè no veu que la circumferència és tangent a l'eix vertical.
  - [hessiana] Intenta usar la hessiana, que a l'origen és nul·la, i conclou que no es pot decidir (o que és un extrem).

TEORIA DEL CURS QUE FA SERVIR:
[T5.21] Definició 21 (Tema 5) — Extrems locals (diverses variables)
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció. Diem que un punt $\mathbf{a}\in\Omega$ és un

(i) màxim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\leqslant f(\mathbf{a})$;

(ii) mínim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\geqslant f(\mathbf{a})$;

(iii) màxim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})<f(\mathbf{a})$;

(iv) mínim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})>f(\mathbf{a})$.

[T5.25] Definició 25 (Tema 5) — Punt de sella
Un punt $\mathbf{a}\in\Omega$ és un punt de sella d'una funció diferenciable $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si és un punt crític de $f$ i per a tot $\epsilon>0$ existeixen $\mathbf{x},\mathbf{y}\in B(\mathbf{a},\epsilon)$ tals que $f(\mathbf{x})<f(\mathbf{a})<f(\mathbf{y})$.
</solucio_de_referencia>

### Document a revisar

[1] Tenim $f(0,0)=0$. Per l'apartat anterior, $f>0$ al semiplà $x>0$; a l'interior del disc $(x+1)^2+y^2<1$ els dos factors $x^2+y^2+2x$ i $x^3$ són negatius, de manera que $f<0$; i als punts amb $x<0$ exteriors al disc, $f<0$.
[2] Els punts $(t,0)$ amb $t>0$ són del semiplà $x>0$ i s'acosten a l'origen quan $t\to0^+$; per exemple, $f(t,0)=(t^2+2t)\,t^3=t^5+2t^4>0=f(0,0)$.
[3] La circumferència $(x+1)^2+y^2=1$ és tangent a l'eix vertical a l'origen, així que hi ha punts amb $x<0$ exteriors al disc arbitràriament a prop de l'origen. Per a $s>0$ petit, prenem $(-s,\sqrt{2s})$: $x^2+y^2+2x=s^2+2s-2s=s^2>0$ i $x=-s<0$.
[4] En aquest punt, $f(-s,\sqrt{2s})=s^2\cdot(-s)^3=-s^5<0=f(0,0)$, i la seva distància a l'origen és $\sqrt{s^2+2s}\leq\sqrt{4s^2}=2s$, que tendeix a $0$ quan $s\to0^+$.
[5] Per tant, tota bola $B((0,0),\epsilon)$ conté punts amb $f>f(0,0)$ i punts amb $f<f(0,0)$, i l'origen no és ni màxim ni mínim local de $f$.
[6] De fet, $f=2x^4+x^5+x^3y^2$ només té termes de grau $\geq4$, de manera que $Df(0,0)=0$: l'origen és un punt crític que no és extrem, és a dir, un punt de sella.


## t5-10b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considereu la funció $f(x,y)=-y^4-e^{-x^2}+2y^2\sqrt{e^x+e^{-x^2}}$.

(b) Proveu que el seu únic punt crític és $(0,0)$.

Indicació: Podeu considerar $f(0,y)$. (Indicació de l'apartat e.)
RESULTAT CORRECTE: Amb $g(x)=e^x+e^{-x^2}$: $f_y=4y\big(\sqrt{g(x)}-y^2\big)$ i $f_x=2xe^{-x^2}+y^2\dfrac{e^x-2xe^{-x^2}}{\sqrt{g(x)}}$. Si $y=0$, $f_x=2xe^{-x^2}=0$ dona $x=0$. Si $y^2=\sqrt{g(x)}$, $f_x=e^x>0$, sense solucions. L'únic punt crític és $(0,0)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [derivades] Calcular les derivades parcials  (teoria: T3.21)
     objectiu: Calcular $f_x$ i $f_y$.
     idea: Anomenar $g(x)=e^x+e^{-x^2}$ i derivar $\sqrt{g(x)}$ amb la regla de la cadena; factoritzar $f_y$.
     detall: $f_y=-4y^3+4y\sqrt{g(x)}=4y\big(\sqrt{g(x)}-y^2\big)$.
$f_x=2xe^{-x^2}+2y^2\dfrac{g'(x)}{2\sqrt{g(x)}}=2xe^{-x^2}+y^2\dfrac{e^x-2xe^{-x^2}}{\sqrt{g(x)}}$.
  2. [cas_y_zero] Cas $y=0$  (teoria: T5.22)
     objectiu: Trobar els punts crítics amb $y=0$.
     idea: Substituir $y=0$ a l'equació $f_x=0$.
     detall: $f_x(x,0)=2xe^{-x^2}=0\iff x=0$. Punt crític $(0,0)$.
  3. [cas_altre_factor] L'altre factor de $f_y$  (teoria: T5.22)
     objectiu: Veure que no hi ha punts crítics on s'anul·la l'altre factor de $f_y$.
     idea: Substituir la relació que dona aquest factor a l'expressió de $f_x$: hi ha una simplificació que deixa una expressió de signe constant.
     detall: Si $y^2=\sqrt{g(x)}$: $f_x=2xe^{-x^2}+\big(e^x-2xe^{-x^2}\big)=e^x>0$. Mai s'anul·la, per tant no hi ha punts crítics en aquest cas.
ERRORS COMUNS:
  - [divideix_per_y] Divideix $f_y=0$ per $y$ i perd el cas $y=0$, o al revés, només considera $y=0$ i oblida l'altre factor.
  - [derivada_arrel] Deriva malament $\sqrt{e^x+e^{-x^2}}$ (oblida la regla de la cadena o el signe de la derivada de $e^{-x^2}$).
  - [no_simplifica] En el segon cas s'encalla intentant resoldre una equació transcendent sense substituir la relació $y^2=\sqrt{g(x)}$.

TEORIA DEL CURS QUE FA SERVIR:
[T5.22] Definició 22 (Tema 5) — Punt crític
$\mathbf{a}\in\Omega$ és un punt crític de $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si $f$ és diferenciable en $\mathbf{a}$ i $Df(\mathbf{a})=0$.

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$
</solucio_de_referencia>

### Document a revisar

[1] Sigui $g(x)=e^x+e^{-x^2}$. Com que $g(x)>1$ per a tot $x$, l'arrel $\sqrt{g(x)}$ està ben definida i és diferenciable, i $f(x,y)=-y^4-e^{-x^2}+2y^2\sqrt{g(x)}$.
[2] Derivant respecte de $y$: $f_y=-4y^3+4y\sqrt{g(x)}=4y\big(\sqrt{g(x)}-y^2\big)$.
[3] Derivant respecte de $x$, amb $g'(x)=e^x-2xe^{-x^2}$: $f_x=2xe^{-x^2}+2y^2\frac{g'(x)}{2\sqrt{g(x)}}=2xe^{-x^2}+y^2\frac{e^x-2xe^{-x^2}}{\sqrt{g(x)}}$.
[4] Per tant $f_y=0$ si i només si $y=0$ o $y^2=\sqrt{g(x)}$, és a dir, $y=\sqrt[4]{g(x)}$.
[5] Cas $y=0$: $f_x(x,0)=2xe^{-x^2}=0$ si i només si $x=0$, perquè $e^{-x^2}>0$. Obtenim el punt crític $(0,0)$.
[6] Cas $y^2=\sqrt{g(x)}$: substituint, $f_x=2xe^{-x^2}+\sqrt{g(x)}\,\frac{e^x-2xe^{-x^2}}{\sqrt{g(x)}}=2xe^{-x^2}+e^x-2xe^{-x^2}=e^x>0$, que no s'anul·la mai: en aquest cas no hi ha punts crítics.
[7] Per tant, l'únic punt crític de $f$ és $(0,0)$.


## t5-12b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $f(x,y)=-3x^2y^2+x^3y^3$.

(b) Sense usar derivades segones, raoneu el caràcter dels punts crítics de $f(x,y)$ que es troben a la bola unitat $B(\mathbf{0},1)$.
RESULTAT CORRECTE: Els punts crítics de $B(\mathbf{0},1)$ són els punts dels eixos amb $\|(x,y)\|<1$ (la hipèrbola $xy=2$ queda fora de la bola). Tots són màxims locals no estrictes: dins de la bola $f(x,y)=(xy)^2(xy-3)\leq0=f(p)$, i $f$ és constantment $0$ sobre els eixos.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [punts_a_la_bola] Quins punts crítics hi ha a la bola
     objectiu: Sabent per l'apartat (a) que els punts crítics són els dels eixos i els de la hipèrbola $xy=2$, determinar quins són a $B(\mathbf{0},1)$.
     idea: Comparar $x^2+y^2$ amb $|xy|$ mitjançant una desigualtat elemental.
     detall: Com que $x^2+y^2\geq2|xy|$, els punts amb $xy=2$ compleixen $x^2+y^2\geq4$: cap és a la bola. Els punts crítics de la bola són els dels eixos: $(x,0)$ amb $|x|<1$ i $(0,y)$ amb $|y|<1$, on $f$ val $0$.
  2. [reescriure] Reescriure f en funció de xy
     objectiu: Escriure $f$ d'una manera que en faci evident el signe.
     idea: $f$ només depèn del producte $t=xy$: factoritzar com a polinomi en $t$.
     detall: Amb $t=xy$, $f(x,y)=-3t^2+t^3=t^2(t-3)$.
  3. [signe_i_caracter] Signe a la bola i conclusió  (teoria: T5.21)
     objectiu: Comparar $f$ en un entorn de cada punt crític de la bola amb el valor de $f$ en aquest punt, i deduir-ne el caràcter.
     idea: Fitar $|xy|$ dins de la bola per saber el signe de cada factor, i aplicar la definició d'extrem local (la bola és oberta, així que conté un entorn de cada punt seu).
     detall: A $B(\mathbf{0},1)$, $|xy|\leq\frac12(x^2+y^2)<\frac12$, de manera que $t-3<0$ i $f=t^2(t-3)\leq0$, amb igualtat si i només si $t=0$. Per a $p$ a un eix de la bola, $f(p)=0$, i prenent $\epsilon$ amb $B(p,\epsilon)\subseteq B(\mathbf{0},1)$ es té $f(x,y)\leq f(p)$ a $B(p,\epsilon)$: $p$ és màxim local. No és estricte perquè $f=0$ en tots els punts de l'eix propers a $p$.
ERRORS COMUNS:
  - [hipèrbola_dins] Inclou (o no descarta raonadament) punts de $xy=2$ dins la bola.
  - [estricte] Afirma que són extrems estrictes, oblidant que els punts crítics no són aïllats.
  - [usa_hessiana] Intenta usar la hessiana (prohibit per l'enunciat; a més, als eixos és semidefinida i no decideix).
  - [signe_sense_fita] Afirma $f\leq0$ sense justificar per què $xy-3<0$, o ho conclou al pla sencer.

TEORIA DEL CURS QUE FA SERVIR:
[T5.21] Definició 21 (Tema 5) — Extrems locals (diverses variables)
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció. Diem que un punt $\mathbf{a}\in\Omega$ és un

(i) màxim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\leqslant f(\mathbf{a})$;

(ii) mínim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\geqslant f(\mathbf{a})$;

(iii) màxim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})<f(\mathbf{a})$;

(iv) mínim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})>f(\mathbf{a})$.

[T5.22] Definició 22 (Tema 5) — Punt crític
$\mathbf{a}\in\Omega$ és un punt crític de $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si $f$ és diferenciable en $\mathbf{a}$ i $Df(\mathbf{a})=0$.
</solucio_de_referencia>

### Document a revisar

[1] Per l'apartat anterior, $f_x=3xy^2(xy-2)$ i $f_y=3x^2y(xy-2)$, i els punts crítics de $f$ són els dels eixos ($xy=0$) i els de la hipèrbola $xy=2$.
[2] Si $xy=2$, aleshores $|x|\geq2$ o $|y|\geq2$, de manera que $x^2+y^2\geq4>1$ i cap punt de la hipèrbola és a la bola. Els punts crítics de $B(\mathbf{0},1)$ són, doncs, $(x,0)$ amb $|x|<1$ i $(0,y)$ amb $|y|<1$, on $f$ val $0$.
[3] Escrivim $f$ en funció de $t=xy$: $f(x,y)=-3t^2+t^3=t^2(t-3)$.
[4] A la bola, $|xy|\leq\frac12(x^2+y^2)<\frac12$, així que $t-3<0$ i $f=t^2(t-3)\leq0$, amb igualtat si i només si $t=xy=0$.
[5] Sigui $p$ un punt d'un eix dins la bola, on $f(p)=0$. Com que la bola és oberta, existeix $\epsilon>0$ amb $B(p,\epsilon)\subseteq B(\mathbf{0},1)$, i es té $f(x,y)\leq0=f(p)$ per a tot $(x,y)\in B(p,\epsilon)$: $p$ és un màxim local.
[6] Aquests màxims no són estrictes, perquè $f=0$ en tots els punts de l'eix propers a $p$; l'única excepció és l'origen, que és un màxim local estricte.


## t5-13a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem la funció $f(x,y)=e^{x-y}\left(\cos(x+1)-\sin(y+1)-1\right)$ i el punt $p=(-1,-1)$.

(a) Calculeu el polinomi de Taylor de grau $\leqslant3$ de $f$ en $p$.
RESULTAT CORRECTE: Amb $u=x+1$, $v=y+1$:
$P_3=-v-\frac12u^2-uv+v^2-\frac12u^3+uv^2-\frac13v^3$, és a dir,
$P_3(x,y)=-(y+1)-\frac12(x+1)^2-(x+1)(y+1)+(y+1)^2-\frac12(x+1)^3+(x+1)(y+1)^2-\frac13(y+1)^3$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [canvi_i_factors] Centrar i desenvolupar els factors  (teoria: T5.16, T5.17)
     objectiu: Escriure $f$ en variables centrades en $p$ i desenvolupar cada factor fins a grau $3$.
     idea: Amb $u=x+1$, $v=y+1$ s'observa que $x-y=u-v$; usar els desenvolupaments d'una variable de l'exponencial, el cosinus i el sinus, justificats per la unicitat del polinomi de Taylor.
     detall: $f=e^{u-v}\left(\cos u-\sin v-1\right)$.
$\cos u-1-\sin v=-v-\frac12u^2+\frac16v^3+O_4(u,v)$ i $e^{u-v}=1+(u-v)+\frac12(u-v)^2+O_3(u,v)$.
  2. [producte] Multiplicar per graus  (teoria: T5.16)
     objectiu: Obtenir els termes de grau $1$, $2$ i $3$ del producte.
     idea: El segon factor no té terme constant: el terme de grau $k$ del producte combina el de grau $j\geq1$ del segon factor amb el de grau $k-j$ de l'exponencial.
     detall: Grau 1: $-v$. Grau 2: $-\frac12u^2+(u-v)(-v)=-\frac12u^2-uv+v^2$.
Grau 3: $\frac16v^3+(u-v)\left(-\frac12u^2\right)+\frac12(u-v)^2(-v)=-\frac12u^3+uv^2-\frac13v^3$.
$P_3=-v-\frac12u^2-uv+v^2-\frac12u^3+uv^2-\frac13v^3$, amb $u=x+1$, $v=y+1$ (i $f(p)=0$).
ERRORS COMUNS:
  - [no_centrar] Desenvolupa $\cos(x+1)$ i $\sin(y+1)$ en potències de $x$ i $y$ (al voltant de l'origen) en lloc de $x+1$ i $y+1$.
  - [exponencial_mal_centrada] Escriu $e^{x-y}$ com $e^{u-v}$ multiplicat per una constant incorrecta, o desenvolupa $e^{x-y}$ al voltant de $0$ en $x,y$.
  - [oblida_creuats] Oblida termes de grau $3$ que provenen de $(u-v)^2\cdot(-v)$ o de $(u-v)\cdot(-\frac12u^2)$.

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
</solucio_de_referencia>

### Document a revisar

[1] Centrem a $p$ amb $u=x+1$, $v=y+1$. Llavors $x-y=u-v$ i $f=e^{u-v}\left(\cos u-\sin v-1\right)$, amb $f(p)=e^0(1-0-1)=0$.
[2] Desenvolupem els factors: $\cos u-1-\sin v=-v-\frac12u^2+\frac16v^3+O_4(u,v)$ i, com que aquest factor no té terme constant, de l'exponencial n'hi ha prou amb $e^{u-v}=1+(u-v)+\frac12(u-v)^2+O_3(u,v)$.
[3] Multiplicant i agrupant per graus: el grau $1$ és $-v$, i el grau $2$ és $-\frac12u^2+(u-v)(-v)=-\frac12u^2-uv-v^2$.
[4] El grau $3$ és $\frac16v^3+(u-v)\left(-\frac12u^2\right)+(u-v)^2(-v)=\frac16v^3-\frac12u^3+\frac12u^2v-u^2v+2uv^2-v^3=-\frac12u^3-\frac12u^2v+2uv^2-\frac56v^3$.
[5] Per tant, $P_3=-v-\frac12u^2-uv-v^2-\frac12u^3-\frac12u^2v+2uv^2-\frac56v^3$, és a dir, $P_3(x,y)=-(y+1)-\frac12(x+1)^2-(x+1)(y+1)-(y+1)^2-\frac12(x+1)^3-\frac12(x+1)^2(y+1)+2(x+1)(y+1)^2-\frac56(y+1)^3$.


## t5-15a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Repetiu el problema anterior amb les altres tres variants possibles:

(a) $\varphi'(a)<0$ i $\varphi'(b)>0$;
RESULTAT CORRECTE: Punts crítics: $(a,a)$, $(a,b)$, $(b,a)$, $(b,b)$. Ara $\varphi>0$ a $(-\infty,a)$, $\varphi<0$ a $(a,b)$, $\varphi>0$ a $(b,+\infty)$; $\Phi$ (primitiva de $\varphi$) té màxim local estricte a $a$ i mínim local estricte a $b$.
$(a,b)$ és mínim local estricte, amb $f(a,b)=\int_a^b\varphi<0$; $(b,a)$ és màxim local estricte, amb $f(b,a)=\int_a^b|\varphi|>0$; $(a,a)$ i $(b,b)$ són punts de sella.
Interpretació: $[a,b]$ és ara el tram on $\varphi<0$; integrant-lo d'esquerra a dreta s'obté l'àrea més negativa possible a prop, i al revés la més positiva.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [punts_critics] Punts crítics  (teoria: T3.18, T5.22)
     objectiu: Amb $f(x,y)=\int_x^y\varphi(t)\,dt$ com al problema 14 i les noves hipòtesis, trobar els punts crítics de $f$.
     idea: El gradient no depèn dels signes de $\varphi'$: és el mateix càlcul del problema anterior (teorema fonamental del càlcul).
     detall: $\nabla f=(-\varphi(x),\varphi(y))$, que s'anul·la exactament a $(a,a)$, $(a,b)$, $(b,a)$, $(b,b)$; $f$ és diferenciable perquè les parcials són contínues.
  2. [signe_phi] Signe de φ  (teoria: T2.24, T5.9)
     objectiu: Determinar el signe de $\varphi$ a cada interval determinat per $a$ i $b$, i el caràcter de $a$ i $b$ per a una primitiva $\Phi$ de $\varphi$.
     idea: El signe de $\varphi'$ en cada zero fixa el signe de $\varphi$ a cada costat; el valor intermedi el propaga fins al zero següent.
     detall: $\varphi'(a)<0$: $\varphi>0$ just a l'esquerra de $a$ i $\varphi<0$ just a la dreta; $\varphi'(b)>0$: $\varphi<0$ just a l'esquerra de $b$ i $\varphi>0$ a la dreta. Per valor intermedi: $\varphi>0$ a $(-\infty,a)$, $\varphi<0$ a $(a,b)$, $\varphi>0$ a $(b,+\infty)$ (coherent). Per tant $\Phi$ creix, decreix, creix: $a$ és màxim local estricte i $b$ mínim local estricte de $\Phi$.
  3. [classificar] Caràcter dels punts crítics  (teoria: T5.21, T5.25)
     objectiu: Decidir el caràcter dels quatre punts crítics.
     idea: Escriure $f(x,y)=\Phi(y)-\Phi(x)$ i combinar el caràcter de $a$ i $b$ per a $\Phi$ a cada coordenada, com al problema 14.
     detall: $(a,b)$: per $(x,y)$ proper, $\Phi(y)\geq\Phi(b)$ i $\Phi(x)\leq\Phi(a)$, amb igualtat només si $y=b$ i $x=a$ respectivament; així $f(x,y)>f(a,b)$ si $(x,y)\neq(a,b)$: mínim local estricte. $(b,a)$: màxim local estricte. $(a,a)$: $f(a,y)-f(a,a)=\Phi(y)-\Phi(a)<0$ i $f(x,a)-f(a,a)=\Phi(a)-\Phi(x)>0$: sella; $(b,b)$ igual, sella.
  4. [interpretar] Interpretar
     objectiu: Interpretar els resultats en termes d'àrees.
     idea: Identificar on $\varphi$ és positiva i negativa i pensar quin interval d'integració proper maximitza o minimitza l'àrea amb signe.
     detall: $[a,b]$ és el tram on $\varphi<0$: $\int_a^b\varphi$ és l'àrea més negativa que es pot aconseguir movent poc els extrems, i $\int_b^a\varphi=\int_a^b|\varphi|$ la més positiva. A la diagonal $f=0$ i els punts $(a,a)$, $(b,b)$ són selles.
ERRORS COMUNS:
  - [copia_resultat_anterior] Copia la classificació del problema 14 sense refer el signe de $\varphi$.
  - [signe_derivada_inferior] Oblida el signe menys de $\partial f/\partial x$ i inverteix el caràcter en la coordenada $x$.

TEORIA DEL CURS QUE FA SERVIR:
[T5.21] Definició 21 (Tema 5) — Extrems locals (diverses variables)
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció. Diem que un punt $\mathbf{a}\in\Omega$ és un

(i) màxim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\leqslant f(\mathbf{a})$;

(ii) mínim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\geqslant f(\mathbf{a})$;

(iii) màxim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})<f(\mathbf{a})$;

(iv) mínim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})>f(\mathbf{a})$.

[T5.22] Definició 22 (Tema 5) — Punt crític
$\mathbf{a}\in\Omega$ és un punt crític de $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si $f$ és diferenciable en $\mathbf{a}$ i $Df(\mathbf{a})=0$.

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

[1] Com que $\varphi$ és derivable, és contínua, i pel teorema fonamental del càlcul $\frac{\partial f}{\partial x}(x,y)=-\varphi(x)$ i $\frac{\partial f}{\partial y}(x,y)=\varphi(y)$. Com que existeixen les derivades parcials en tot punt, $f$ és diferenciable.
[2] Els punts crítics són les solucions de $\varphi(x)=0$ i $\varphi(y)=0$, és a dir, $(a,a)$, $(a,b)$, $(b,a)$ i $(b,b)$.
[3] Com que $\varphi(a)=0$ i $\varphi'(a)<0$, $\varphi>0$ just a l'esquerra de $a$ i $\varphi<0$ just a la dreta; com que $\varphi'(b)>0$, $\varphi<0$ just a l'esquerra de $b$ i $\varphi>0$ just a la dreta. Com que $a$ i $b$ són els únics zeros, pel teorema de Bolzano $\varphi>0$ a $(-\infty,a)$, $\varphi<0$ a $(a,b)$ i $\varphi>0$ a $(b,+\infty)$.
[4] Sigui $\Phi$ una primitiva de $\varphi$, de manera que $f(x,y)=\Phi(y)-\Phi(x)$. $\Phi$ és estrictament creixent a $(-\infty,a]$, estrictament decreixent a $[a,b]$ i estrictament creixent a $[b,+\infty)$: $a$ és un màxim local estricte de $\Phi$ i $b$ un mínim local estricte.
[5] Punt $(a,b)$: per a $(x,y)$ proper, $\Phi(y)\geq\Phi(b)$ i $\Phi(x)\leq\Phi(a)$, amb igualtat només si $y=b$ i $x=a$ respectivament; per tant $f(x,y)>f(a,b)$ si $(x,y)\neq(a,b)$, i $(a,b)$ és un mínim local estricte, amb $f(a,b)=\int_a^b\varphi<0$. Anàlogament, $(b,a)$ és un màxim local estricte, amb $f(b,a)=\int_a^b|\varphi|>0$.
[6] Punt $(a,a)$: per a $y\neq a$ proper a $a$, $f(a,y)-f(a,a)=\Phi(y)-\Phi(a)>0$, i per a $x\neq a$ proper a $a$, $f(x,a)-f(a,a)=\Phi(a)-\Phi(x)<0$. Així $f$ pren valors més grans i més petits que $f(a,a)=0$ a prop de $(a,a)$: és un punt de sella. El mateix raonament amb $b$ mostra que $(b,b)$ també és un punt de sella.
[7] Interpretació: $[a,b]$ és el tram on $\varphi<0$. Integrant-lo d'esquerra a dreta, $\int_a^b\varphi$ és l'àrea més negativa que es pot aconseguir movent poc els extrems d'integració, i integrant-lo al revés s'obté la més positiva; a la diagonal, $f=0$.


## t6-1a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Doneu una parametrització de classe $\mathcal{C}^1$ de les corbes següents:

(a) Una el·lipse centrada a l'origen, de semieixos $a,b>0$, recorreguda dos cops en sentit horari.
RESULTAT CORRECTE: Per exemple, $\gamma(t)=(a\cos t,\,-b\sin t)$, $t\in[0,4\pi]$ (o bé $\gamma(t)=(a\cos 2t,\,-b\sin 2t)$, $t\in[0,2\pi]$). És $\mathcal{C}^\infty$ i $\gamma'(t)=(-a\sin t,\,-b\cos t)\neq(0,0)$ per a tot $t$. Qualsevol altra parametrització regular que recorri l'el·lipse $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$ dues vegades en sentit horari també és correcta.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [una_volta] Parametritzar l'el·lipse una vegada
     objectiu: Donar una parametrització que recorri l'el·lipse una sola vegada, sense preocupar-se encara pel sentit.
     idea: Escriure l'equació de l'el·lipse i adaptar-hi la parametrització de la circumferència unitat amb cosinus i sinus, escalant cada coordenada pel semieix corresponent.
     detall: L'el·lipse és $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$. Com que $\cos^2t+\sin^2t=1$, la corba $(a\cos t,\,b\sin t)$, $t\in[0,2\pi]$, la recorre una vegada, començant a $(a,0)$.
  2. [sentit] Ajustar el sentit
     objectiu: Determinar en quin sentit es recorre la corba anterior i, si cal, canviar-lo perquè sigui horari.
     idea: Mirar el vector velocitat en un punt concret (per exemple a $(a,0)$): cap a on es mou el punt? Per invertir el sentit n'hi ha prou de canviar el signe d'una de les coordenades (o substituir $t$ per $-t$).
     detall: A $t=0$, $(a\cos t,b\sin t)$ passa per $(a,0)$ amb velocitat $(0,b)$, cap amunt: sentit antihorari. Canviant $t\mapsto -t$ s'obté $(a\cos t,\,-b\sin t)$, amb velocitat $(0,-b)$ a $(a,0)$: sentit horari.
  3. [dos_cops] Recórrer-la dos cops
     objectiu: Aconseguir que la corba doni exactament dues voltes.
     idea: O bé s'allarga l'interval de paràmetre, o bé es multiplica el paràmetre per una constant dins de les funcions trigonomètriques.
     detall: Prenent $t\in[0,4\pi]$ (o bé $\gamma(t)=(a\cos 2t,-b\sin 2t)$ amb $t\in[0,2\pi]$) el punt dona dues voltes completes.
  4. [regularitat] Comprovar que és $\mathcal{C}^1$ i regular  (teoria: T6.3)
     objectiu: Justificar que la parametrització obtinguda és de classe $\mathcal{C}^1$ i té vector velocitat no nul.
     idea: Les components són funcions trigonomètriques; cal mirar si $\gamma'(t)$ s'anul·la mai (rang de $D\gamma$ igual a $1$).
     detall: $\gamma'(t)=(-a\sin t,\,-b\cos t)$; com que $\sin t$ i $\cos t$ no s'anul·len simultàniament i $a,b>0$, $\gamma'(t)\neq(0,0)$ per a tot $t$, és a dir, $\mathrm{rang}\,D\gamma(t)=1$.
ERRORS COMUNS:
  - [sentit_antihorari] Dona $(a\cos t,b\sin t)$ sense adonar-se que es recorre en sentit antihorari.
  - [una_sola_volta] Usa l'interval $[0,2\pi]$ amb $\cos t$, $\sin t$, de manera que només dona una volta.
  - [semieixos_intercanviats] Posa el semieix $a$ a la coordenada $y$ i el $b$ a la $x$ (o no especifica quin és quin) sense dir-ho.

TEORIA DEL CURS QUE FA SERVIR:
[T6.5] Definició 5 (Tema 6) — Equacions definidores i parametrització
En el context de les definicions 2 i 3:

- La funció $\Phi$ conté les condicions o equacions definidores de la varietat $M$. Podem dir que defineix la varietat de manera implícita.
- La funció $\rho$ és una parametrització de la varietat $M$.
- El conjunt $\rho^{-1}(M)$ s'anomena carta local associada a la varietat $M$.

[T6.3] Definició 3 (Tema 6) — Varietat en forma paramètrica
Una $m$-varietat de classe $r$ a $\mathbb{R}^n$ és un subconjunt no buit $M\subseteq\mathbb{R}^n$ tal que per a tot $\mathbf{a}\in M$ existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, un obert $\Omega\subseteq\mathbb{R}^m$ i una funció $\rho\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^n$, $\rho\in\mathcal{C}^r(\Omega)$ amb $\mathrm{rang}\left(D\rho(\mathbf{u})\right)=m$ per a tot $\mathbf{u}\in\Omega$, tals que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiu (és un homeomorfisme).
</solucio_de_referencia>

### Document a revisar

[1] L'el·lipse és $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$. Com que $\cos^2t+\sin^2t=1$, la corba $(a\cos t,\,b\sin t)$, $t\in[0,2\pi]$, la recorre una vegada començant a $(a,0)$.
[2] A $t=0$ aquesta corba passa per $(a,0)$ amb velocitat $(0,b)$, cap amunt: la recorre en sentit antihorari. Canviant $t$ per $-t$ obtenim $(a\cos t,\,-b\sin t)$, que passa per $(a,0)$ amb velocitat $(0,-b)$: sentit horari.
[3] Per fer dues voltes prenem $t\in[0,4\pi]$; alternativament, $(a\cos 2t,\,-b\sin 2t)$ amb $t\in[0,\pi]$ també dona dues voltes.
[4] La parametrització $\gamma(t)=(a\cos t,\,-b\sin t)$ és de classe $\mathcal{C}^\infty$, amb $\gamma'(t)=(a\sin t,\,-b\cos t)$.
[5] Com que $\sin t$ i $\cos t$ no s'anul·len simultàniament i $a,b>0$, $\gamma'(t)\neq(0,0)$ per a tot $t$, és a dir, $\mathrm{rang}\,D\gamma(t)=1$: la parametrització és regular.
[6] Per tant, $\gamma(t)=(a\cos t,\,-b\sin t)$, $t\in[0,4\pi]$, és una parametrització $\mathcal{C}^1$ regular de l'el·lipse recorreguda dos cops en sentit horari.


## t6-2e:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Doneu una parametrització de classe $\mathcal{C}^1$ de les superfícies següents:

(e) Un el·lipsoide de semieixos $a,b,c>0$, centrat a l'origen.
RESULTAT CORRECTE: $\varphi(u,v)=(a\cos u\cos v,\ b\sin u\cos v,\ c\sin v)$, $(u,v)\in[0,2\pi]\times[-\pi/2,\pi/2]$; és $\mathcal{C}^\infty$ i regular (rang $2$) quan $\cos v\neq0$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [equacio] Equació de l'el·lipsoide
     objectiu: Escriure l'equació de l'el·lipsoide i relacionar-la amb una superfície coneguda.
     idea: Un canvi d'escala independent a cada eix converteix l'esfera unitat en l'el·lipsoide.
     detall: $\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}=1$; si $(X,Y,Z)$ és a l'esfera unitat, $(aX,bY,cZ)$ és a l'el·lipsoide.
  2. [parametritzar] Parametritzar  (teoria: T6.6)
     objectiu: Donar la parametrització i el seu domini.
     idea: Aplicar el canvi d'escala a la parametrització de l'esfera unitat amb dos angles.
     detall: $\varphi(u,v)=(a\cos u\cos v,\ b\sin u\cos v,\ c\sin v)$, $(u,v)\in[0,2\pi]\times[-\pi/2,\pi/2]$.
  3. [rang] Estudiar el rang  (teoria: T6.3)
     objectiu: Determinar on la parametrització és regular.
     idea: $D\varphi$ és la de l'esfera unitat multiplicada a l'esquerra per una matriu diagonal invertible.
     detall: $D\varphi=\mathrm{diag}(a,b,c)\begin{pmatrix}-\sin u\cos v&-\cos u\sin v\\\cos u\cos v&-\sin u\sin v\\0&\cos v\end{pmatrix}$, de rang $2$ si i només si $\cos v\neq0$.
ERRORS COMUNS:
  - [semieixos_mal_posats] Posa els semieixos en coordenades equivocades o els eleva al quadrat.
  - [domini_angles] Pren els dos angles a $[0,2\pi]$ i recobreix la superfície dues vegades.

TEORIA DEL CURS QUE FA SERVIR:
[T6.5] Definició 5 (Tema 6) — Equacions definidores i parametrització
En el context de les definicions 2 i 3:

- La funció $\Phi$ conté les condicions o equacions definidores de la varietat $M$. Podem dir que defineix la varietat de manera implícita.
- La funció $\rho$ és una parametrització de la varietat $M$.
- El conjunt $\rho^{-1}(M)$ s'anomena carta local associada a la varietat $M$.

[T6.6] Exemple 6 (Tema 6) — Esfera com a varietat
Considerem una esfera de radi $R$ centrada a l'origen com a varietat de dimensió 2 a $\mathbb{R}^3$; en la notació que hem fet servir, doncs, $n=3$ i $m=2$.

Podem descriure l'esfera a partir de l'equació definidora
$$\Phi(x,y,z)=x^2+y^2+z^2-R^2,$$
on $\Phi\colon\mathbb{R}^3\longrightarrow\mathbb{R}$, o bé amb una parametrització
$$\rho(u,v)=R\,(\cos u\,\cos v,\sin u\,\cos v,\sin v),$$
on $\rho\colon\Omega\subset\mathbb{R}^2\longrightarrow\mathbb{R}^3$, amb $\Omega=(0,2\pi)\times(-\pi/2,\pi/2)$. Veurem que es pot estendre també a $[0,2\pi]\times(-\pi/2,\pi/2)$. També seria possible prendre altres cartes locals.

Observem que $D\Phi(x,y,z)=\begin{pmatrix}2x&2y&2z\end{pmatrix}$, que té rang $n-m=1$ per a tot $(x,y,z)$ tal que $\Phi(x,y,z)=0$. En canvi,
$$D\rho(u,v)=\begin{pmatrix}-R\sin u\cos v&-R\cos u\sin v\\R\cos u\cos v&-R\sin u\sin v\\0&R\cos v\end{pmatrix},$$
i té rang 1 quan $v=\pm\pi/2$ (per això no els hem considerat al domini). Per tant, té rang $m=2$ per a tot $(u,v)\in\Omega$.

[T6.3] Definició 3 (Tema 6) — Varietat en forma paramètrica
Una $m$-varietat de classe $r$ a $\mathbb{R}^n$ és un subconjunt no buit $M\subseteq\mathbb{R}^n$ tal que per a tot $\mathbf{a}\in M$ existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, un obert $\Omega\subseteq\mathbb{R}^m$ i una funció $\rho\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^n$, $\rho\in\mathcal{C}^r(\Omega)$ amb $\mathrm{rang}\left(D\rho(\mathbf{u})\right)=m$ per a tot $\mathbf{u}\in\Omega$, tals que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiu (és un homeomorfisme).
</solucio_de_referencia>

### Document a revisar

[1] L'el·lipsoide és $\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}=1$: un punt $(x,y,z)$ hi pertany si i només si $\left(\frac xa,\frac yb,\frac zc\right)$ és de l'esfera unitat.
[2] Parametritzem l'esfera unitat amb coordenades esfèriques, $(\cos u\cos v,\ \sin u\cos v,\ \sin v)$, i escalem cada coordenada: $\varphi(u,v)=(a\cos u\cos v,\ b\sin u\cos v,\ c\sin v)$, amb $(u,v)\in[0,2\pi]\times[-\pi/2,\pi/2]$.
[3] Efectivament, $\cos^2u\cos^2v+\sin^2u\cos^2v+\sin^2v=\cos^2v+\sin^2v=1$, de manera que $\varphi$ pren valors a l'el·lipsoide i el recobreix tot; a més, $\varphi$ és de classe $\mathcal{C}^\infty$ i és injectiva en tot el domini.
[4] Les derivades parcials són $\partial_u\varphi=(-a\sin u\cos v,\ b\cos u\cos v,\ 0)$ i $\partial_v\varphi=(-a\cos u\sin v,\ b\sin u\sin v,\ c\cos v)$.
[5] Si $\cos v\neq0$, $\partial_u\varphi$ és no nul (perquè $\sin u$ i $\cos u$ no s'anul·len alhora) i té tercera component $0$, mentre que la tercera component de $\partial_v\varphi$ és $c\cos v\neq0$: són linealment independents i $D\varphi$ té rang $2$. Si $\cos v=0$, $\partial_u\varphi=0$ i el rang és $1$.
[6] Per tant, $\varphi$ és una parametrització $\mathcal{C}^\infty$ de l'el·lipsoide, regular (rang $2$) als punts amb $\cos v\neq0$, és a dir, fora dels pols $(0,0,\pm c)$.


## t6-5:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Trobeu la distància entre el punt $(0,b)$ i la paràbola $x^2-4y=0$. Resoleu el problema emprant dos mètodes diferents.
RESULTAT CORRECTE: $d=|b|$ si $b\le2$ (punt més proper $(0,0)$), i $d=2\sqrt{b-1}$ si $b\ge2$ (punts més propers $\left(\pm2\sqrt{b-2},\,b-2\right)$). Per $b=2$ les dues expressions donen $2$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [plantejament] Plantejar el problema  (teoria: T1.34, T2.23)
     objectiu: Escriure la distància com un problema d'extrems i justificar que el mínim existeix.
     idea: Minimitzar el quadrat de la distància (mateixos minimitzadors). El conjunt no és compacte: cal un argument perquè el mínim existeixi (lluny, la funció es fa gran).
     detall: Minimitzem $D(x,y)=x^2+(y-b)^2$ sobre la paràbola $P=\{x^2=4y\}$. Com que $D\to+\infty$ quan $\|(x,y)\|\to\infty$, el mínim sobre $P$ coincideix amb el mínim sobre $P\cap\overline{B}(0,R)$ per $R$ gran, que és compacte; per Weierstrass existeix.
  2. [substitucio] Mètode 1: substitució  (teoria: T6.1)
     objectiu: Reduir el problema a una variable i trobar el mínim.
     idea: Sobre la paràbola, $x^2$ s'expressa en funció de $y$; el problema queda en una variable amb una restricció de signe sobre $y$.
     detall: Amb $x^2=4y$, $y\ge0$: $g(y)=4y+(y-b)^2=y^2+(4-2b)y+b^2$. És una paràbola en $y$ amb vèrtex a $y=b-2$.
Si $b\ge2$, el vèrtex és admissible: $g(b-2)=4(b-2)+4=4b-4$, als punts $\left(\pm2\sqrt{b-2},b-2\right)$.
Si $b<2$, $g$ és creixent a $[0,\infty)$ i el mínim és $g(0)=b^2$, al punt $(0,0)$.
  3. [lagrange] Mètode 2: multiplicadors de Lagrange  (teoria: T6.2, T6.17)
     objectiu: Obtenir els mateixos candidats amb el mètode de Lagrange.
     idea: Comprovar que la paràbola és una 1-varietat ($\nabla\Phi\ne0$) i resoldre $\nabla D=\lambda\nabla\Phi$, $\Phi=0$, separant casos segons quin factor s'anul·la.
     detall: $\Phi=x^2-4y$, $\nabla\Phi=(2x,-4)\neq0$. Sistema: $2x=2\lambda x$, $2(y-b)=-4\lambda$, $x^2=4y$.
De la primera, $x=0$ o $\lambda=1$. Si $x=0$: $y=0$, $D=b^2$. Si $\lambda=1$: $y=b-2$, i cal $x^2=4(b-2)\ge0$, és a dir $b\ge2$; llavors $D=4b-4$.
Per $b\ge2$, $b^2-(4b-4)=(b-2)^2\ge0$, de manera que el mínim és $4b-4$; per $b<2$ només hi ha el candidat $(0,0)$.
  4. [conclusio] Concloure
     objectiu: Donar la distància en funció de $b$.
     idea: Prendre l'arrel del mínim de $D$ en cada cas.
     detall: $d=|b|$ si $b\le2$ i $d=2\sqrt{b-1}$ si $b\ge2$ (les dues coincideixen a $b=2$).
ERRORS COMUNS:
  - [oblida_cas] Dona només $d=2\sqrt{b-1}$ per a tot $b$, sense veure que per $b<2$ el punt $y=b-2$ no és de la paràbola (o surt una arrel negativa).
  - [oblida_x0] A Lagrange divideix per $x$ a la primera equació i perd el cas $x=0$.
  - [sense_existencia] Pren el candidat de Lagrange com a mínim sense justificar que el mínim existeix (la paràbola no és compacta).

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

[T6.2] Definició 2 (Tema 6) — Varietat en forma implícita
Una $m$-varietat de classe $r$ a $\mathbb{R}^n$ és un subconjunt no buit $M\subseteq\mathbb{R}^n$ tal que per a tot $\mathbf{a}\in M$ existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i una funció $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$ amb $\mathrm{rang}\left(D\Phi(\mathbf{x})\right)=n-m$ per a tot $\mathbf{x}\in G$, tals que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.

En aquest context, es diu que $M$ és la $m$-varietat associada a $\Phi$; per reforçar aquesta relació amb $\Phi$, de vegades la denotarem amb $M_\Phi$.

$M$ també s'acostuma a anomenar (sub)varietat (diferenciable, $\mathcal{C}^r$ o de classe $r$) de dimensió $m$ en $\mathbb{R}^n$.

[T6.17] Corol·lari 17 (Tema 6) — Teorema dels multiplicadors de Lagrange
(Teorema dels multiplicadors de Lagrange). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ de classe $\mathcal{C}^r$, $M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(G)$. Si $\mathbf{a}\in M_\Phi$ és un extrem local de $f$ condicionat a $M_\Phi$, aleshores existeixen uns valors únics $\lambda_1,\ldots,\lambda_{n-m}\in\mathbb{R}$ tals que $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in G\times\mathbb{R}^{n-m}$ és un punt crític de $L$, és a dir, $(\mathbf{a},\boldsymbol{\lambda})$ és solució del sistema de $2n-m$ equacions
$$\begin{cases}\nabla f(\mathbf{a})-\lambda_1\nabla\Phi_1(\mathbf{a})-\cdots-\lambda_{n-m}\nabla\Phi_{n-m}(\mathbf{a})&=\mathbf{0},\\\Phi(\mathbf{a})&=\mathbf{0}.\end{cases}$$
</solucio_de_referencia>

### Document a revisar

[1] Minimitzem el quadrat de la distància, $D(x,y)=x^2+(y-b)^2$, sobre la paràbola $P=\{x^2=4y\}$. Com que $P$ és un tancat de $\mathbb{R}^2$, és compacte, i pel teorema de Weierstrass $D$ hi assoleix el mínim.
[2] Mètode 1 (substitució): sobre $P$, $x^2=4y$ amb $y\geq0$, i $D=g(y)=4y+(y-b)^2=y^2+(4-2b)y+b^2$, una paràbola en $y$ amb vèrtex a $y=b-2$.
[3] Si $b\geq2$, el vèrtex és admissible i el mínim és $g(b-2)=4(b-2)+4=4b-4$, assolit als punts $\left(\pm2\sqrt{b-2},\,b-2\right)$. Si $b<2$, el vèrtex és a $y<0$, $g$ és creixent a $[0,+\infty)$ i el mínim és $g(0)=b^2$, al punt $(0,0)$.
[4] Mètode 2 (multiplicadors de Lagrange): amb $\Phi=x^2-4y$, $\nabla\Phi=(2x,-4)\neq0$, i el sistema és $2x=2\lambda x$, $2(y-b)=-4\lambda$, $x^2=4y$.
[5] De la primera equació, $x=0$ o $\lambda=1$. Si $x=0$, aleshores $y=0$ i $D=b^2$. Si $\lambda=1$, aleshores $y=b-2$, i cal $x^2=4(b-2)\geq0$, és a dir, $b\geq2$; llavors $D=4b-4$.
[6] Per a $b\geq2$, $b^2-(4b-4)=(b-2)^2\geq0$, de manera que el mínim és $4b-4$; per a $b<2$ l'únic candidat és $(0,0)$, que és, doncs, el mínim.
[7] En conclusió, la distància és $d=b$ si $b\leq2$ i $d=2\sqrt{b-1}$ si $b\geq2$; les dues expressions coincideixen a $b=2$.


## t6-7:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Trobeu els vèrtexs i semieixos de l'el·lipse obtinguda intersecant el pla d'equació $x+y+z=0$ amb l'el·lipsoide d'equació $x^2/4+y^2+z^2=1$.
RESULTAT CORRECTE: Semieix major $\sqrt2$, amb vèrtexs $\pm\left(-\frac{2}{\sqrt3},\frac{1}{\sqrt3},\frac{1}{\sqrt3}\right)$.
Semieix menor $1$, amb vèrtexs $\pm\left(0,\frac{1}{\sqrt2},-\frac{1}{\sqrt2}\right)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [plantejament] Plantejar com a extrems condicionats  (teoria: T6.2, T1.34, T2.23)
     objectiu: Traduir "vèrtexs i semieixos" a un problema d'extrems condicionats.
     idea: Trobar el centre de l'el·lipse per simetria; els vèrtexs són els punts de la corba a distància màxima i mínima del centre. Cal comprovar que la corba és una 1-varietat compacta.
     detall: La corba $C$ és simètrica respecte de l'origen ($\mathbf{x}\in C\Rightarrow-\mathbf{x}\in C$), així que el centre és $(0,0,0)$. Maximitzem i minimitzem $f=x^2+y^2+z^2$ sobre $C=\{\Phi_1=\frac{x^2}{4}+y^2+z^2-1=0,\ \Phi_2=x+y+z=0\}$.
$\nabla\Phi_1=(\frac x2,2y,2z)$ i $\nabla\Phi_2=(1,1,1)$ només són paral·lels si $\frac x2=2y=2z$, i amb $x+y+z=0$ això dona l'origen, que no és de $C$: rang $2$ a tot $C$. $C$ és compacta, així que hi ha màxim i mínim.
  2. [sistema] Sistema de Lagrange  (teoria: T6.17)
     objectiu: Escriure el sistema de Lagrange i reduir-lo a casos.
     idea: Restar les equacions corresponents a $y$ i a $z$ per eliminar el segon multiplicador.
     detall: $2x=\lambda\frac{x}{2}+\mu$, $2y=2\lambda y+\mu$, $2z=2\lambda z+\mu$. Restant les dues últimes: $2(1-\lambda)(y-z)=0$, és a dir, $y=z$ o $\lambda=1$.
  3. [casos] Resoldre els casos  (teoria: T6.17)
     objectiu: Trobar tots els punts crítics condicionats i el valor de $f$ en ells.
     idea: En cada cas, usar les dues equacions de lligam per determinar el punt.
     detall: Si $y=z$: $x=-2y$ i $\frac{4y^2}{4}+2y^2=3y^2=1$, $y=\pm\frac{1}{\sqrt3}$: punts $\pm\left(-\frac{2}{\sqrt3},\frac{1}{\sqrt3},\frac{1}{\sqrt3}\right)$ amb $f=2$.
Si $\lambda=1$: la segona equació dona $\mu=0$, la primera $2x=\frac x2$, és a dir $x=0$; llavors $z=-y$ i $2y^2=1$: punts $\pm\left(0,\frac{1}{\sqrt2},-\frac{1}{\sqrt2}\right)$ amb $f=1$.
  4. [conclusio] Vèrtexs i semieixos
     objectiu: Donar els semieixos i els vèrtexs de l'el·lipse.
     idea: Els semieixos són les arrels dels valors màxim i mínim de $f$.
     detall: Semieix major $\sqrt2$, vèrtexs $\pm\left(-\frac{2}{\sqrt3},\frac{1}{\sqrt3},\frac{1}{\sqrt3}\right)$; semieix menor $1$, vèrtexs $\pm\left(0,\frac{1}{\sqrt2},-\frac{1}{\sqrt2}\right)$. (Les dues direccions són ortogonals, com ha de ser.)
ERRORS COMUNS:
  - [un_sol_lligam] Fa Lagrange amb una sola restricció (només l'el·lipsoide o només el pla).
  - [centre] Busca extrems de la distància sense saber quin és el centre de l'el·lipse, o pren com a semieixos els de l'el·lipsoide.
  - [perd_cas] Divideix per $1-\lambda$ o per $y-z$ i perd una família de solucions.

TEORIA DEL CURS QUE FA SERVIR:
[T6.2] Definició 2 (Tema 6) — Varietat en forma implícita
Una $m$-varietat de classe $r$ a $\mathbb{R}^n$ és un subconjunt no buit $M\subseteq\mathbb{R}^n$ tal que per a tot $\mathbf{a}\in M$ existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i una funció $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$ amb $\mathrm{rang}\left(D\Phi(\mathbf{x})\right)=n-m$ per a tot $\mathbf{x}\in G$, tals que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.

En aquest context, es diu que $M$ és la $m$-varietat associada a $\Phi$; per reforçar aquesta relació amb $\Phi$, de vegades la denotarem amb $M_\Phi$.

$M$ també s'acostuma a anomenar (sub)varietat (diferenciable, $\mathcal{C}^r$ o de classe $r$) de dimensió $m$ en $\mathbb{R}^n$.

[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.

[T2.23] Teorema 23 (Tema 2) — Teorema de Weierstrass
(Weierstrass). Sigui $f:\Omega\subseteq M\to\mathbb{R}$ contínua i $K\subseteq\Omega$ compacte. Llavors $f(K)$ és fitat i $\exists x_0,x_1\in K$ t.q. $f(x_0)=\min_{x\in K}f(x)$ i $f(x_1)=\max_{x\in K}f(x)$.

[T6.17] Corol·lari 17 (Tema 6) — Teorema dels multiplicadors de Lagrange
(Teorema dels multiplicadors de Lagrange). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ de classe $\mathcal{C}^r$, $M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(G)$. Si $\mathbf{a}\in M_\Phi$ és un extrem local de $f$ condicionat a $M_\Phi$, aleshores existeixen uns valors únics $\lambda_1,\ldots,\lambda_{n-m}\in\mathbb{R}$ tals que $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in G\times\mathbb{R}^{n-m}$ és un punt crític de $L$, és a dir, $(\mathbf{a},\boldsymbol{\lambda})$ és solució del sistema de $2n-m$ equacions
$$\begin{cases}\nabla f(\mathbf{a})-\lambda_1\nabla\Phi_1(\mathbf{a})-\cdots-\lambda_{n-m}\nabla\Phi_{n-m}(\mathbf{a})&=\mathbf{0},\\\Phi(\mathbf{a})&=\mathbf{0}.\end{cases}$$
</solucio_de_referencia>

### Document a revisar

[1] La corba $C$ és simètrica respecte de l'origen ($\mathbf{x}\in C\Rightarrow-\mathbf{x}\in C$), així que el centre de l'el·lipse és l'origen. Els vèrtexs són els punts de $C$ més llunyans i més propers al centre: busquem els extrems de $f=x^2+y^2+z^2$ sobre $C=\{\Phi_1=\frac{x^2}{4}+y^2+z^2-1=0,\ \Phi_2=x+y+z=0\}$.
[2] $\nabla\Phi_1=(\frac x2,2y,2z)$ i $\nabla\Phi_2=(1,1,1)$ només són paral·lels si $\frac x2=2y=2z$, i amb $x+y+z=0$ això dona l'origen, que no és de $C$: el rang és $2$ a tot $C$. A més, $C$ és tancada, perquè és intersecció de dos tancats, i per tant compacta: $f$ hi té màxim i mínim.
[3] Sistema de Lagrange: $2x=\lambda\frac x2+\mu$, $2y=2\lambda y+\mu$, $2z=2\lambda z+\mu$. Restant les dues últimes, $2(1-\lambda)(y-z)=0$, és a dir, $y=z$ o $\lambda=1$.
[4] Si $y=z$, el pla dona $x=-2y$, i l'el·lipsoide, $\frac{4y^2}{4}+y^2+y^2=3y^2=1$, $y=\pm\frac{1}{\sqrt3}$: punts $\pm\left(-\frac{2}{\sqrt3},\frac{1}{\sqrt3},\frac{1}{\sqrt3}\right)$, amb $f=\frac43+\frac13+\frac13=2$.
[5] Si $\lambda=1$, la segona equació dona $\mu=0$ i la primera, $2x=\frac x2$, és a dir, $x=0$; llavors $z=-y$ i $2y^2=1$: punts $\pm\left(0,\frac{1}{\sqrt2},-\frac{1}{\sqrt2}\right)$, amb $f=1$.
[6] Com que $f$ és el quadrat de la distància al centre, el semieix major és $2$, amb vèrtexs $\pm\left(-\frac{2}{\sqrt3},\frac{1}{\sqrt3},\frac{1}{\sqrt3}\right)$, i el semieix menor és $1$, amb vèrtexs $\pm\left(0,\frac{1}{\sqrt2},-\frac{1}{\sqrt2}\right)$. Les dues direccions són ortogonals, com ha de ser.


## t6-9:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Calculeu els extrems absoluts de $f(x,y)=\log\left(8xy-x^2+1\right)$ sobre el compacte
$$K=\{(x,y)\in\mathbb{R}^2\mid x>0,\ xy\leqslant8,\ 1\leqslant y\leqslant x^2\}.$$
RESULTAT CORRECTE: Màxim absolut $\log61$, assolit en $(2,4)$.
Mínim absolut $\log1=0$, assolit en $(8,1)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [recinte] Descriure $K$  (teoria: T1.34)
     objectiu: Descriure el recinte $K$: vèrtexs i corbes que el delimiten.
     idea: Intersecar dos a dos les corbes $y=1$, $y=x^2$, $xy=8$; observar quins valors pot prendre $x$.
     detall: De $1\le y\le x^2$ i $x>0$ surt $x\ge1$, i de $xy\le8$, $y\ge1$ surt $x\le8$. Vèrtexs: $(1,1)$ ($y=1$, $y=x^2$), $(2,4)$ ($y=x^2$, $xy=8$) i $(8,1)$ ($xy=8$, $y=1$). La frontera és formada pel segment $y=1$, $x\in[1,8]$, l'arc de paràbola $y=x^2$, $x\in[1,2]$, i l'arc d'hipèrbola $y=\frac8x$, $x\in[2,8]$.
  2. [reduir] Eliminar el logaritme  (teoria: T2.23)
     objectiu: Simplificar la funció a estudiar i comprovar que $f$ està ben definida a $K$.
     idea: El logaritme és estrictament creixent: els extrems de $f$ són als mateixos punts que els de l'argument, sempre que aquest sigui positiu a $K$.
     detall: Sigui $g=8xy-x^2+1$. A $K$: $8xy\ge8x\ge x^2$ (perquè $1\le x\le8$), per tant $g\ge1>0$ i $f=\log g$ és contínua a $K$. Per Weierstrass hi ha extrems, i són als mateixos punts que els de $g$.
  3. [interior] Interior  (teoria: T5.23)
     objectiu: Trobar els punts crítics de $g$ a l'interior de $K$.
     idea: Mirar si les dues derivades parcials poden anul·lar-se simultàniament a $K$.
     detall: $g_y=8x\neq0$ a $K$ ($x\ge1$): no hi ha punts crítics a l'interior.
  4. [frontera] Els tres trossos de frontera  (teoria: T6.1)
     objectiu: Estudiar $g$ sobre cadascun dels tres trossos de la frontera.
     idea: Substituir l'equació de cada corba i estudiar una funció d'una variable a l'interval corresponent (monotonia o punts crítics).
     detall: $y=1$, $x\in[1,8]$: $g=8x-x^2+1$, crític $x=4$ amb $g=17$; $g(1)=8$, $g(8)=1$.
$y=x^2$, $x\in[1,2]$: $g=8x^3-x^2+1$, $g'=24x^2-2x>0$: creixent, de $8$ a $61$.
$y=\frac8x$, $x\in[2,8]$: $g=65-x^2$, decreixent, de $61$ a $1$.
  5. [comparar] Concloure
     objectiu: Donar el màxim i el mínim absoluts de $f$.
     idea: Comparar els valors de $g$ i aplicar el logaritme.
     detall: $\max g=61$ en $(2,4)$ i $\min g=1$ en $(8,1)$. Per tant $\max f=\log61$ i $\min f=\log1=0$.
ERRORS COMUNS:
  - [log_sense_justificar] Treu el logaritme sense comprovar que l'argument és positiu, o creu que canvia la posició dels extrems.
  - [vertexs_malament] Calcula malament on es tallen les corbes (per exemple no troba $(2,4)$) o oblida que $x\ge1$.
  - [oblida_extrems_interval] Als trossos de frontera només busca on s'anul·la la derivada i oblida els vèrtexs, que són precisament on hi ha el màxim i el mínim.

TEORIA DEL CURS QUE FA SERVIR:
[T1.24] Definició 24 (Tema 1) — Compacte i seqüencialment compacte
Sigui $(M,d)$ espai mètric, $A\subseteq M$.

i) $A$ és _compacte_ si tot recobriment per oberts de $A$ admet un subrecobriment finit, és a dir: si $A\subseteq\bigcup_{i\in I}U_i$, amb $U_i$ obert, aleshores existeixen $i_1,\ldots,i_k\in I$ tals que $A\subseteq\bigcup_{j=1}^k U_{i_j}$.

ii) $A$ és _seqüencialment compacte_ si tota successió $(x_n)_{n\in\mathbb{N}}\subseteq A$ admet una subsuccessió (una parcial) convergent a un punt de $A$.

[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.

[T2.23] Teorema 23 (Tema 2) — Teorema de Weierstrass
(Weierstrass). Sigui $f:\Omega\subseteq M\to\mathbb{R}$ contínua i $K\subseteq\Omega$ compacte. Llavors $f(K)$ és fitat i $\exists x_0,x_1\in K$ t.q. $f(x_0)=\min_{x\in K}f(x)$ i $f(x_1)=\max_{x\in K}f(x)$.

[T5.23] Proposició 23 (Tema 5) — Els extrems són punts crítics
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció diferenciable en $\mathbf{a}\in\Omega$. Si $\mathbf{a}$ és un extrem (és a dir, un màxim o un mínim) local de $f$, llavors $\mathbf{a}$ és un punt crític de $f$.

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

[1] De $1\leq y\leq x^2$ i $x>0$ surt $x\geq1$, i de $xy\leq8$ amb $y\geq1$ surt $x\leq8$. Els vèrtexs de $K$ són $(1,1)$ (on $y=1$ talla $y=x^2$), $(2,4)$ (on $y=x^2$ talla $xy=8$) i $(8,1)$ (on $xy=8$ talla $y=1$).
[2] La frontera de $K$ és formada pel segment $y=1$, $x\in[1,8]$, l'arc de paràbola $y=x^2$, $x\in[1,2]$, i l'arc d'hipèrbola $y=\frac8x$, $x\in[2,8]$.
[3] Sigui $g=8xy-x^2+1$. A $K$ es té $8xy\geq8x$ (perquè $y\geq1$) i $8x\geq x^2$ (perquè $x\geq1$), així que $g\geq1>0$ i $f=\log g$ és contínua a $K$. Per Weierstrass hi ha extrems absoluts i, com que $\log$ és estrictament creixent, s'assoleixen als mateixos punts que els de $g$.
[4] A l'interior de $K$, $g_y=8x\neq0$ (perquè $x\geq1$), així que no hi ha punts crítics.
[5] Sobre $y=1$, $x\in[1,8]$: $g=8x-x^2+1$, amb punt crític $x=4$ i $g(4)=25$; als extrems, $g(1)=8$ i $g(8)=1$.
[6] Sobre $y=x^2$, $x\in[1,2]$: $g=8x^3-x^2+1$ i $g'=24x^2-2x=2x(12x-1)>0$, de manera que $g$ és creixent, de $g(1)=8$ a $g(2)=61$.
[7] Sobre $y=\frac8x$, $x\in[2,8]$: $g=64-x^2+1=65-x^2$, decreixent, de $g(2)=61$ a $g(8)=1$.
[8] Per tant $\max g=61$, a $(2,4)$, i $\min g=1$, a $(8,1)$: el màxim absolut de $f$ és $\log61$, assolit a $(2,4)$, i el mínim absolut és $\log1=0$, assolit a $(8,1)$.


## t6-11:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Trobeu els extrems absoluts de la funció $f(x,y)=x^3-3xy^2$ sobre la circumferència de radi 1 centrada a l'origen (la superfície $z=f(x,y)$ s'anomena *cadira del mico*).
RESULTAT CORRECTE: Màxim absolut $1$, assolit en $(1,0)$, $\left(-\frac12,\frac{\sqrt3}{2}\right)$ i $\left(-\frac12,-\frac{\sqrt3}{2}\right)$.
Mínim absolut $-1$, assolit en $(-1,0)$, $\left(\frac12,\frac{\sqrt3}{2}\right)$ i $\left(\frac12,-\frac{\sqrt3}{2}\right)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [existencia_param] Existència i parametrització  (teoria: T1.34, T2.23, T6.1)
     objectiu: Justificar que hi ha extrems absoluts i reduir el problema a una variable.
     idea: La circumferència és compacta. Parametritzar-la amb l'angle i simplificar $f$ amb fórmules trigonomètriques (angle triple).
     detall: La circumferència és tancada i fitada i $f$ és contínua: hi ha extrems absoluts. Amb $(x,y)=(\cos t,\sin t)$, $t\in[0,2\pi]$:
$f=\cos^3t-3\cos t\sin^2t=\cos3t$.
  2. [extrems] Extrems de la funció d'una variable
     objectiu: Trobar el màxim i el mínim de la funció d'una variable i els angles on s'assoleixen.
     idea: Els valors extrems de la funció trigonomètrica obtinguda són coneguts; buscar tots els angles de $[0,2\pi)$ on s'assoleixen.
     detall: $\cos3t=1\iff t\in\{0,\frac{2\pi}{3},\frac{4\pi}{3}\}$ i $\cos3t=-1\iff t\in\{\frac{\pi}{3},\pi,\frac{5\pi}{3}\}$.
  3. [punts] Tornar als punts del pla
     objectiu: Escriure els punts de la circumferència on s'assoleixen els extrems.
     idea: Substituir els angles a la parametrització.
     detall: Màxim $1$ en $(1,0)$, $\left(-\frac12,\pm\frac{\sqrt3}{2}\right)$; mínim $-1$ en $(-1,0)$, $\left(\frac12,\pm\frac{\sqrt3}{2}\right)$.
ERRORS COMUNS:
  - [nomes_eixos] Troba només $(1,0)$ i $(-1,0)$ i oblida els altres quatre punts.
  - [lagrange_casos] Amb Lagrange, divideix per $x$ o per $y$ i perd solucions del sistema $3x^2-3y^2=2\lambda x$, $-6xy=2\lambda y$.
  - [punts_critics_lliures] Busca els punts crítics lliures de $f$ (només l'origen) i conclou que no hi ha extrems.

TEORIA DEL CURS QUE FA SERVIR:
[T6.12] Definició 12 (Tema 6) — Extrems condicionats
Siguin $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geq1$, $D\subseteq\mathbb{R}^n$ un obert tal que $M\subseteq D$ i $f\colon D\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(D)$. Diem que un punt $\mathbf{a}\in M$ és un màxim local de $f$ condicionat a $M$ si $\mathbf{a}$ és un màxim local de $f|_M$; és a dir, si existeix un obert $G$ tal que $\mathbf{a}\in G$ i $f(\mathbf{x})\leq f(\mathbf{a})$ per a tot $x\in M\cap G$.

Definim mínim condicionat i màxim i mínim estrictes condicionats d'una manera semblant, canviant $\leq$ per la desigualtat que pertoqui. Per ser punt de sella condicionat, cal que, per a tot obert $G$ tal que $\mathbf{a}\in G$, existeixin $\mathbf{x},\mathbf{y}\in M\cap G$ tals que $f(\mathbf{x})<f(\mathbf{a})$ i $f(\mathbf{y})>f(\mathbf{a})$.

[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.

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

[1] La circumferència unitat és tancada i fitada i $f$ és contínua, així que hi ha extrems absoluts. La parametritzem amb $(x,y)=(\cos t,\sin t)$, $t\in[0,2\pi]$.
[2] Sobre la circumferència, $f=\cos^3t-3\cos t\sin^2t=\cos^3t-3\cos t(1-\cos^2t)=4\cos^3t-3\cos t=\cos3t$.
[3] Per tant $f$ pren valors a $[-1,1]$ sobre la circumferència, i $\cos3t=1$ si i només si $t\in\{0,\frac{2\pi}{3},\frac{4\pi}{3}\}$ (o $t=2\pi$, que dona el mateix punt que $t=0$), mentre que $\cos3t=-1$ si i només si $t\in\{\frac{\pi}{3},\pi,\frac{5\pi}{3}\}$.
[4] Els punts de màxim són $(\cos0,\sin0)=(1,0)$, $\left(\cos\frac{2\pi}{3},\sin\frac{2\pi}{3}\right)=\left(-\frac{\sqrt3}{2},\frac12\right)$ i $\left(\cos\frac{4\pi}{3},\sin\frac{4\pi}{3}\right)=\left(-\frac12,-\frac{\sqrt3}{2}\right)$, on $f=1$.
[5] Els punts de mínim, corresponents a $t=\frac{\pi}{3},\pi,\frac{5\pi}{3}$, són $\left(\frac12,\frac{\sqrt3}{2}\right)$, $(-1,0)$ i $\left(\frac12,-\frac{\sqrt3}{2}\right)$, on $f=-1$.
[6] Així, el màxim absolut de $f$ sobre la circumferència és $1$ i el mínim absolut és $-1$, cadascun assolit en tres punts. A més, $(1,0)$ és també un màxim local de $f$ a $\mathbb{R}^2$.


## t6-12:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem la funció $f(x,y,z)=x^4+y^2/4+z^2-x^2y-2z+1$ i el conjunt $M=\{(x,y,z)\in\mathbb{R}^3\mid2x^2+y^2+z^3-5xz-2=0\}$. Proveu que en el punt $p=(1,2,1)$ s'assoleix un mínim local de la restricció de $f$ a $M$. Es tracta d'un mínim absolut de la restricció de $f$ a $M$?
RESULTAT CORRECTE: $p$ és un mínim local estricte de $f|_M$: $\nabla f(p)=\mathbf{0}$ (multiplicador $\lambda=0$) i la forma hessiana $q_{Hf(p)}$, que a $\mathbb{R}^3$ és només semidefinida positiva, és definida positiva sobre $T_M(p)=\{v_1-4v_2+2v_3=0\}$.
Sí, és un mínim absolut: $f=\left(x^2-\frac y2\right)^2+(z-1)^2\ge0=f(p)$ a tot $\mathbb{R}^3$, i en particular a $M$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [varietat] $M$ és varietat prop de $p$  (teoria: T6.2)
     objectiu: Comprovar que $p\in M$ i que $M$ és una varietat diferenciable en un entorn de $p$.
     idea: Calcular $\Phi(p)$ i el gradient de l'equació definidora $\Phi$ en $p$; si no s'anul·la, per continuïtat té rang màxim en un entorn.
     detall: $\Phi(p)=2+4+1-5-2=0$. $\nabla\Phi=(4x-5z,\ 2y,\ 3z^2-5x)$, $\nabla\Phi(p)=(-1,4,-2)\neq0$. Per continuïtat $\nabla\Phi\neq0$ en un obert $G\ni p$, i $M\cap G$ és una 2-varietat $\mathcal{C}^\infty$.
  2. [lagrange] Punt crític de la funció de Lagrange  (teoria: T6.16, T6.17)
     objectiu: Comprovar que $p$ satisfà la condició necessària de Lagrange i trobar el multiplicador.
     idea: Calcular $\nabla f(p)$ i comparar-lo amb $\nabla\Phi(p)$.
     detall: $\nabla f=(4x^3-2xy,\ \frac y2-x^2,\ 2z-2)$, $\nabla f(p)=(0,0,0)=0\cdot\nabla\Phi(p)$. Per tant $(p,\lambda)$ amb $\lambda=0$ és punt crític de $L=f-\lambda\Phi$, i $F=L(\cdot,0)=f$.
  3. [hessiana] Hessiana de $F$  (teoria: T5.32, T5.33)
     objectiu: Calcular la matriu hessiana de la funció $F$ del criteri de segon ordre en $p$ i veure què diu el criteri lliure.
     idea: Amb el multiplicador trobat, $F$ coincideix amb $f$. Calcular les derivades segones i mirar el signe de la forma a tot $\mathbb{R}^3$.
     detall: $HF(p)=Hf(p)=\begin{pmatrix}8&-2&0\\-2&\frac12&0\\0&0&2\end{pmatrix}$. El menor $2\times2$ té determinant $4-4=0$: la forma és semidefinida positiva (s'anul·la en la direcció $(1,4,0)$), així que el criteri d'extrems lliures no decideix.
  4. [tangent] Restringir a l'espai tangent  (teoria: T6.10, T6.19)
     objectiu: Estudiar el signe de la forma quadràtica hessiana sobre $T_M(p)$ i concloure el caràcter local de $p$.
     idea: L'espai tangent és el nucli de $D\Phi(p)$. Escriure la forma com a suma de quadrats i veure si pot anul·lar-se en un vector tangent no nul.
     detall: $T_M(p)=\ker D\Phi(p)=\{v\mid -v_1+4v_2-2v_3=0\}$. $q(v)=8v_1^2-4v_1v_2+\frac12v_2^2+2v_3^2=\frac12(4v_1-v_2)^2+2v_3^2\ge0$, i $q(v)=0$ només si $v_3=0$, $v_2=4v_1$; llavors la condició tangent dona $-v_1+16v_1=0$, $v=0$. Per tant $q$ és definida positiva sobre $T_M(p)$ i, pel teorema de condicions suficients, $p$ és un mínim local estricte de $f|_M$.
  5. [absolut] És mínim absolut?
     objectiu: Decidir si $p$ és un mínim absolut de $f|_M$.
     idea: Calcular $f(p)$ i intentar reescriure $f$ completant quadrats (fixeu-vos en els termes $x^4$, $-x^2y$, $\frac{y^2}{4}$).
     detall: $f(p)=1+1+1-2-2+1=0$ i $f=\left(x^2-\frac y2\right)^2+(z-1)^2\ge0$ a tot $\mathbb{R}^3$. Per tant $f(q)\ge f(p)$ per a tot $q\in M$: sí, és un mínim absolut de $f|_M$.
ERRORS COMUNS:
  - [criteri_lliure] Usa la hessiana a tot $\mathbb{R}^3$, veu que és semidefinida i conclou que no es pot decidir (o que no és mínim).
  - [tangent_malament] Pren com a espai tangent el generat per $\nabla\Phi(p)$ en lloc del seu ortogonal.
  - [oblida_varietat] No comprova que $p\in M$ ni que $\nabla\Phi(p)\neq0$, condicions necessàries per aplicar els teoremes.
  - [local_implica_absolut] Afirma que és absolut perquè és l'únic punt crític trobat, o que no ho és perquè $M$ no és compacte, sense cap argument.

TEORIA DEL CURS QUE FA SERVIR:
[T6.12] Definició 12 (Tema 6) — Extrems condicionats
Siguin $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geq1$, $D\subseteq\mathbb{R}^n$ un obert tal que $M\subseteq D$ i $f\colon D\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(D)$. Diem que un punt $\mathbf{a}\in M$ és un màxim local de $f$ condicionat a $M$ si $\mathbf{a}$ és un màxim local de $f|_M$; és a dir, si existeix un obert $G$ tal que $\mathbf{a}\in G$ i $f(\mathbf{x})\leq f(\mathbf{a})$ per a tot $x\in M\cap G$.

Definim mínim condicionat i màxim i mínim estrictes condicionats d'una manera semblant, canviant $\leq$ per la desigualtat que pertoqui. Per ser punt de sella condicionat, cal que, per a tot obert $G$ tal que $\mathbf{a}\in G$, existeixin $\mathbf{x},\mathbf{y}\in M\cap G$ tals que $f(\mathbf{x})<f(\mathbf{a})$ i $f(\mathbf{y})>f(\mathbf{a})$.

[T6.2] Definició 2 (Tema 6) — Varietat en forma implícita
Una $m$-varietat de classe $r$ a $\mathbb{R}^n$ és un subconjunt no buit $M\subseteq\mathbb{R}^n$ tal que per a tot $\mathbf{a}\in M$ existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i una funció $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$ amb $\mathrm{rang}\left(D\Phi(\mathbf{x})\right)=n-m$ per a tot $\mathbf{x}\in G$, tals que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.

En aquest context, es diu que $M$ és la $m$-varietat associada a $\Phi$; per reforçar aquesta relació amb $\Phi$, de vegades la denotarem amb $M_\Phi$.

$M$ també s'acostuma a anomenar (sub)varietat (diferenciable, $\mathcal{C}^r$ o de classe $r$) de dimensió $m$ en $\mathbb{R}^n$.

[T6.16] Definició 16 (Tema 6) — Funció de Lagrange
Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ com en la proposició 13, $M_\Phi\neq\emptyset$ la varietat associada a $\Phi$, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(G)$. La funció de Lagrange associada a $\Phi$ i $f$ és una funció $L\colon G\times\mathbb{R}^{n-m}\to\mathbb{R}$, definida com
$$L(\mathbf{x},\boldsymbol{\lambda})=f(\mathbf{x})-\lambda_1\Phi_1(\mathbf{x})-\cdots-\lambda_{n-m}\Phi_{n-m}(\mathbf{x}),$$
on $\mathbf{x}=(x_1,\ldots,x_n)\in G$ i $\boldsymbol{\lambda}=(\lambda_1,\ldots,\lambda_{n-m})\in\mathbb{R}^{n-m}$.

[T6.17] Corol·lari 17 (Tema 6) — Teorema dels multiplicadors de Lagrange
(Teorema dels multiplicadors de Lagrange). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ de classe $\mathcal{C}^r$, $M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(G)$. Si $\mathbf{a}\in M_\Phi$ és un extrem local de $f$ condicionat a $M_\Phi$, aleshores existeixen uns valors únics $\lambda_1,\ldots,\lambda_{n-m}\in\mathbb{R}$ tals que $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in G\times\mathbb{R}^{n-m}$ és un punt crític de $L$, és a dir, $(\mathbf{a},\boldsymbol{\lambda})$ és solució del sistema de $2n-m$ equacions
$$\begin{cases}\nabla f(\mathbf{a})-\lambda_1\nabla\Phi_1(\mathbf{a})-\cdots-\lambda_{n-m}\nabla\Phi_{n-m}(\mathbf{a})&=\mathbf{0},\\\Phi(\mathbf{a})&=\mathbf{0}.\end{cases}$$

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

[T6.10] Teorema 10 (Tema 6) — Càlcul dels espais tangent i normal
Siguin $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geqslant1$, $\Phi$ i $G$ com a la definició 2, en un entorn del punt $\mathbf{a}\in M$, i $\rho$ i $\Omega$ com a la definició 3. És a dir,

- existeixen oberts $G\in\mathbb{R}^n$ i $\Omega\in\mathbb{R}^m$, amb $\mathbf{a}\in G$;
- existeix una funció $\Phi\colon G\longrightarrow\mathbb{R}^{n-m}\in\mathcal{C}^r(G)$, amb $\mathrm{rang}\,D\Phi(\mathbf{x})=n-m$ per a tot $x\in G$ tal que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=0\}$.
- existeix una funció $\rho\colon\Omega\longrightarrow\mathbb{R}^n\in\mathcal{C}^r(\Omega)$, amb $\mathrm{rang}\,D\rho(\mathbf{u})=m$ per a tot $\mathbf{u}\in\Omega$ tal que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiva; en particular, existeix un únic $\mathbf{b}\in\Omega$ tal que $\rho(\mathbf{b})=\mathbf{a}$.

Aleshores,

(i) $T_M(\mathbf{a})=\ker\left(D\Phi(\mathbf{a})\right)=\langle\text{columnes de }D\rho(\mathbf{b})\rangle$;

(ii) $N_M(\mathbf{a})=\langle\text{files de }D\Phi(\mathbf{a})\rangle=\langle\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})\rangle$.

En particular, $T_M(\mathbf{a})$ i $N_M(\mathbf{a})$ són subespais vectorials de $\mathbb{R}^n$ de dimensions $\dim\left(T_M(\mathbf{a})\right)=m$ i $\dim\left(N_M(\mathbf{a})\right)=n-m$, respectivament.

[T6.19] Teorema 19 (Tema 6) — Condicions suficients d'extrem condicionat
(condicions suficients). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ com en el corol·lari 17, amb $r\geq2$, $M=M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^2(G)$. Sigui $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in M\times\mathbb{R}^{n-m}$ un punt crític de la funció de Lagrange $L$; considerem la subfunció $F\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ donada per $F(\mathbf{x})=L(\mathbf{x},\lambda_1,\ldots,\lambda_{n-m})$. Llavors,

(i) $q_{HF(\mathbf{a})}$ és definida negativa ($\ominus$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un màxim local estricte de $f$ condicionat a $M$;

(ii) $q_{HF(\mathbf{a})}$ és definida positiva ($\oplus$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un mínim local estricte de $f$ condicionat a $M$;

(iii) $q_{HF(\mathbf{a})}$ és indefinida ($\odot$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un punt de sella de $f$ condicionat a $M$;

(iv) $\mathbf{a}$ és un màxim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida negativa ($\underline{\ominus}$) sobre $T_M(\mathbf{a})$;

(v) $\mathbf{a}$ és un mínim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida positiva ($\underline{\oplus}$) sobre $T_M(\mathbf{a})$.
</solucio_de_referencia>

### Document a revisar

[1] Sigui $\Phi=2x^2+y^2+z^3-5xz-2$. Comprovem que $p\in M$: $\Phi(p)=2+4+1-5-2=0$. A més, $\nabla\Phi=(4x-5z,\ 2y,\ 3z^2-5x)$ i $\nabla\Phi(p)=(-1,4,-2)\neq0$; per continuïtat $\nabla\Phi\neq0$ en un obert $G\ni p$, i $M\cap G$ és una 2-varietat de classe $\mathcal{C}^\infty$.
[2] $\nabla f=(4x^3-2xy,\ \frac y2-x^2,\ 2z-2)$, i $\nabla f(p)=(0,0,0)=0\cdot\nabla\Phi(p)$. Per tant $(p,0)$ és un punt crític de la funció de Lagrange $L=f-\lambda\Phi$, i $F=L(\cdot,0)=f$.
[3] $HF(p)=Hf(p)=\begin{pmatrix}8&-2&0\\-2&\frac12&0\\0&0&2\end{pmatrix}$. El menor $2\times2$ superior té determinant $4-4=0$, i la forma és semidefinida positiva: s'anul·la en la direcció $(4,1,0)$. El criteri d'extrems lliures no decideix.
[4] L'espai tangent és $T_M(p)=\ker D\Phi(p)=\{v\in\mathbb{R}^3\mid -v_1+4v_2-2v_3=0\}$.
[5] La forma quadràtica és $q(v)=8v_1^2-4v_1v_2+\frac12v_2^2+2v_3^2=\frac12(4v_1-v_2)^2+2v_3^2\geq0$, i $q(v)=0$ si i només si $v_3=0$ i $v_2=4v_1$.
[6] Com que $q$ és semidefinida positiva a tot $\mathbb{R}^3$, la seva restricció a $T_M(p)$ és definida positiva, i pel teorema de condicions suficients $p$ és un mínim local estricte de $f|_M$.
[7] És un mínim absolut? Sí: $f(p)=1+1+1-2-2+1=0$ i $f=\left(x^2-\frac y2\right)^2+(z-1)^2\geq0$ a tot $\mathbb{R}^3$, de manera que $f(\mathbf{x})\geq f(p)$ per a tot $\mathbf{x}\in M$.


## t6-14:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem el conjunt $D=\{(x,y)\in\mathbb{R}^2\mid x^2+y^2-2x\leqslant0,\ x\geqslant1\}$ i la funció $f\colon\mathbb{R}^2\to\mathbb{R}$ definida per $f(x,y)=x^4+x^2y^2+2xy^2+12y^2$. Trobeu, si existeixen, els punts de $D$ on $f$ assoleix valors màxim i mínim.
RESULTAT CORRECTE: Existeixen (D és compacte). Mínim $1$, assolit només en $(1,0)$. Màxim $18$, assolit en $\left(\frac32,\frac{\sqrt3}{2}\right)$ i $\left(\frac32,-\frac{\sqrt3}{2}\right)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [recinte] El recinte  (teoria: T2.18, T1.34, T2.23)
     objectiu: Descriure $D$ i justificar l'existència d'extrems.
     idea: Completar quadrats a la primera desigualtat; un conjunt definit per desigualtats no estrictes de funcions contínues és tancat.
     detall: $x^2+y^2-2x\le0\iff(x-1)^2+y^2\le1$: $D$ és el semidisc dret del disc de centre $(1,0)$ i radi $1$, amb $x\in[1,2]$. És tancat i fitat, per tant compacte, i $f$ és contínua: pel teorema de Weierstrass hi ha màxim i mínim.
  2. [interior] Punts crítics interiors  (teoria: T5.23)
     objectiu: Trobar els punts crítics de $f$ a l'interior de $D$.
     idea: Factoritzar $f_y$; usar la informació que en surt a $f_x=0$.
     detall: $f_y=2y(x^2+2x+12)$, i $x^2+2x+12>0$, per tant $y=0$; llavors $f_x=4x^3+2xy^2+2y^2=4x^3=0$ dona $x=0\notin D$. No hi ha punts crítics a $D$.
  3. [minim] El mínim
     objectiu: Trobar el mínim de $f$ a $D$.
     idea: Agrupar els termes amb $y^2$ i observar el signe del seu coeficient a $D$.
     detall: $f=x^4+y^2(x^2+2x+12)\ge x^4\ge1$ a $D$ (on $x\ge1$), amb igualtat només si $y=0$ i $x=1$. Mínim $f(1,0)=1$.
  4. [frontera] La frontera  (teoria: T6.1)
     objectiu: Estudiar $f$ sobre el segment $x=1$ i sobre l'arc de circumferència.
     idea: Sobre l'arc, substituir $y^2$ en funció de $x$ (només hi apareix $y^2$) i estudiar una funció d'una variable a $[1,2]$.
     detall: Segment $x=1$, $y\in[-1,1]$: $f=1+15y^2$, entre $1$ i $16$.
Arc $y^2=2x-x^2$, $x\in[1,2]$: $f=x^4+(2x-x^2)(x^2+2x+12)=-8x^2+24x$. Derivada $-16x+24=0$ a $x=\frac32$, valor $18$; als extrems, $16$ (en $(1,\pm1)$) i $16$ (en $(2,0)$). Per $x=\frac32$, $y^2=\frac34$.
  5. [concloure] Concloure
     objectiu: Donar els punts de màxim i de mínim.
     idea: Comparar tots els valors.
     detall: Mínim $1$ en $(1,0)$; màxim $18$ en $\left(\frac32,\pm\frac{\sqrt3}{2}\right)$.
ERRORS COMUNS:
  - [disc_sencer] Treballa amb tot el disc oblidant la condició $x\ge1$, o confon el centre del disc.
  - [substitucio_arrel] Aïlla $y=\sqrt{2x-x^2}$ i oblida la meitat inferior de l'arc, perdent un dels punts de màxim.
  - [oblida_segment] Estudia només l'arc i oblida el segment $x=1$ (o al revés).

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

[1] $x^2+y^2-2x\leq0$ equival a $(x-1)^2+y^2\leq1$, així que $D$ és la meitat dreta del disc de centre $(1,0)$ i radi $1$, amb $x\in[1,2]$. És tancat i fitat, per tant compacte, i $f$ és contínua: pel teorema de Weierstrass, $f$ hi assoleix màxim i mínim.
[2] Punts crítics: $f_y=2y(x^2+2x+12)$ i $x^2+2x+12=(x+1)^2+11>0$, així que $y=0$; llavors $f_x=4x^3+2xy^2+2y^2=4x^3=0$ dona $x=0$, que no és de $D$. No hi ha punts crítics a $D$.
[3] Mínim: a $D$, $f=x^4+y^2(x^2+2x+12)\geq x^4\geq1$, perquè $x\geq1$, amb igualtat només si $y=0$ i $x=1$. El mínim és $f(1,0)=1$.
[4] Frontera, segment $x=1$, $y\in[-1,1]$: $f=1+y^2+2y^2+12y^2=1+14y^2$, que pren valors entre $1$ i $15$.
[5] Arc $y^2=2x-x^2$, $x\in[1,2]$ (amb les dues meitats, $y\geq0$ i $y\leq0$): $f=x^4+(2x-x^2)(x^2+2x+12)=-8x^2+24x$.
[6] La derivada $-16x+24$ s'anul·la a $x=\frac32$, on $f=-18+36=18$ i $y^2=3-\frac94=\frac34$; als extrems de l'arc, $f(1,\pm1)=16$ i $f(2,0)=16$.
[7] Comparant tots els candidats, el mínim absolut és $1$, assolit a $(1,0)$, i el màxim absolut és $18$, assolit a $\left(\frac32,\frac{\sqrt3}{2}\right)$.


## t6-15b:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem la funció donada per $f(x,y,z)=(x+1)^2+(y-1)^2+2z$ i el conjunt $A=\{(x,y,z)\in\mathbb{R}^3\mid z\geqslant x^2+y^2,\ z\leqslant2y-2x+1\}$.

(b) Justifiqueu l'existència d'extrems absoluts de $f$ en $A$ i calculeu-los.
RESULTAT CORRECTE: Existeixen perquè $A$ és compacte (tancat per (a) i fitat) i $f$ és contínua.
Mínim absolut $\frac43$, en $\left(-\frac13,\frac13,\frac29\right)$.
Màxim absolut $13+4\sqrt6$, en $\left(-1-\frac{\sqrt6}{2},\ 1+\frac{\sqrt6}{2},\ 5+2\sqrt6\right)$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [existencia] Existència  (teoria: T1.34, T2.23)
     objectiu: Usant l'apartat (a), justificar que $f$ té extrems absoluts a $A$.
     idea: Falta veure que $A$ és fitat: combinar les dues desigualtats per eliminar $z$ i obtenir una fita per a $(x,y)$, i després per a $z$.
     detall: De $x^2+y^2\le z\le2y-2x+1$ surt $x^2+2x+y^2-2y\le1$, és a dir, $(x+1)^2+(y-1)^2\le3$: $(x,y)$ és al disc $\Delta$ de centre $(-1,1)$ i radi $\sqrt3$. Llavors $0\le z\le2y-2x+1$, que és fitat sobre $\Delta$. $A$ és tancat i fitat, per tant compacte (i no buit: $(0,0,0)\in A$); $f$ és contínua, i per Weierstrass hi ha extrems absoluts.
  2. [interior] Interior  (teoria: T5.23)
     objectiu: Decidir si hi pot haver extrems a l'interior de $A$.
     idea: A l'interior (obert) un extrem hauria de ser punt crític de $f$.
     detall: $\nabla f=(2(x+1),\ 2(y-1),\ 2)\neq0$: no hi ha punts crítics, i els extrems són a la frontera (al paraboloide $z=x^2+y^2$ o al pla $z=2y-2x+1$).
  3. [reduir] Reduir a dues variables
     objectiu: Per a cada $(x,y)$ fix, decidir a quin $z$ de $A$ la funció és mínima i a quin és màxima, i reduir el problema a funcions de $(x,y)$ sobre un disc.
     idea: $f$ depèn de $z$ de manera creixent. (Alternativament: estudiar cada tros de frontera amb Lagrange, inclosa la corba intersecció.)
     detall: Com que $f$ és creixent en $z$, per a $(x,y)\in\Delta$ el mínim és al paraboloide i el màxim al pla:
$\min_A f=\min_\Delta g$, $g=f(x,y,x^2+y^2)=3x^2+2x+3y^2-2y+2$;
$\max_A f=\max_\Delta h$, $h=f(x,y,2y-2x+1)=(x-1)^2+(y+1)^2+2$.
  4. [minim] El mínim
     objectiu: Trobar el mínim absolut de $f$ a $A$ i on s'assoleix.
     idea: Completar quadrats a la funció de dues variables obtinguda i comprovar que el punt on s'anul·len els quadrats és del disc.
     detall: $g=3\left(x+\frac13\right)^2+3\left(y-\frac13\right)^2+\frac43$, mínim $\frac43$ en $\left(-\frac13,\frac13\right)$, que és de $\Delta$ ($\frac49+\frac49\le3$). El punt de $A$ és $\left(-\frac13,\frac13,\frac29\right)$, amb $f=\frac49+\frac49+\frac49=\frac43$.
  5. [maxim] El màxim
     objectiu: Trobar el màxim absolut de $f$ a $A$ i on s'assoleix.
     idea: La funció de dues variables per al màxim és una distància al quadrat a un punt fix (més una constant): el seu màxim sobre el disc és al punt del disc més allunyat d'aquest punt fix.
     detall: $h-2$ és el quadrat de la distància a $(1,-1)$. La distància de $(1,-1)$ al centre $(-1,1)$ és $2\sqrt2$, i el punt més llunyà del disc és $(-1,1)+\sqrt3\frac{(-1,1)}{\sqrt2}=\left(-1-\frac{\sqrt6}{2},1+\frac{\sqrt6}{2}\right)$, a distància $2\sqrt2+\sqrt3$. Màxim: $(2\sqrt2+\sqrt3)^2+2=13+4\sqrt6$, amb $z=2y-2x+1=5+2\sqrt6$ (que també és $x^2+y^2$: el punt és a la corba intersecció).
ERRORS COMUNS:
  - [no_fitat] Afirma que $A$ és compacte sense demostrar que és fitat (o creu que un paraboloide sempre dona un conjunt no fitat).
  - [oblida_corba] Estudiant trossos de frontera per separat, oblida la corba intersecció del paraboloide i el pla, on hi ha el màxim.
  - [critic_fora] Al pla, troba el punt crític $(1,-1)$ de la funció restringida i el pren com a candidat sense comprovar que és fora del disc.

TEORIA DEL CURS QUE FA SERVIR:
[T1.24] Definició 24 (Tema 1) — Compacte i seqüencialment compacte
Sigui $(M,d)$ espai mètric, $A\subseteq M$.

i) $A$ és _compacte_ si tot recobriment per oberts de $A$ admet un subrecobriment finit, és a dir: si $A\subseteq\bigcup_{i\in I}U_i$, amb $U_i$ obert, aleshores existeixen $i_1,\ldots,i_k\in I$ tals que $A\subseteq\bigcup_{j=1}^k U_{i_j}$.

ii) $A$ és _seqüencialment compacte_ si tota successió $(x_n)_{n\in\mathbb{N}}\subseteq A$ admet una subsuccessió (una parcial) convergent a un punt de $A$.

[T1.34] Teorema 34 (Tema 1) — Teorema de Heine-Borel
(Heine-Borel.) Sigui $A\subseteq\mathbb{R}^n$, amb $n>1$. Aleshores, $A$ és compacte $\Leftrightarrow$ $A$ és tancat i fitat.

[T2.23] Teorema 23 (Tema 2) — Teorema de Weierstrass
(Weierstrass). Sigui $f:\Omega\subseteq M\to\mathbb{R}$ contínua i $K\subseteq\Omega$ compacte. Llavors $f(K)$ és fitat i $\exists x_0,x_1\in K$ t.q. $f(x_0)=\min_{x\in K}f(x)$ i $f(x_1)=\max_{x\in K}f(x)$.

[T5.23] Proposició 23 (Tema 5) — Els extrems són punts crítics
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció diferenciable en $\mathbf{a}\in\Omega$. Si $\mathbf{a}$ és un extrem (és a dir, un màxim o un mínim) local de $f$, llavors $\mathbf{a}$ és un punt crític de $f$.
</solucio_de_referencia>

### Document a revisar

[1] Si $(x,y,z)\in A$, de $x^2+y^2\leq z\leq2y-2x+1$ surt $x^2+2x+y^2-2y\leq1$, és a dir, $(x+1)^2+(y-1)^2\leq3$: $(x,y)$ és al disc tancat $\Delta$ de centre $(-1,1)$ i radi $\sqrt3$.
[2] Llavors $0\leq z\leq2y-2x+1$, que és fitat sobre $\Delta$, i $A$ és fitat. També és tancat, perquè el defineixen desigualtats no estrictes entre funcions contínues, i no és buit, perquè $(0,0,0)\in A$. Per tant $A$ és compacte i, com que $f$ és contínua, pel teorema de Weierstrass hi assoleix màxim i mínim absoluts.
[3] $\nabla f=(2(x+1),\ 2(y-1),\ 2)\neq0$, així que $f$ no té punts crítics a l'interior de $A$ i els extrems són a la frontera.
[4] Com que $f$ és creixent en $z$, per a cada $(x,y)\in\Delta$ el mínim de $f$ s'assoleix al paraboloide $z=x^2+y^2$ i el màxim al pla $z=2y-2x+1$. Per tant $\min_Af=\min_\Delta g$ amb $g=f(x,y,x^2+y^2)=3x^2+2x+3y^2-2y+2$, i $\max_Af=\max_\Delta h$ amb $h=f(x,y,2y-2x+1)=(x-1)^2+(y+1)^2+2$.
[5] $g=3\left(x+\frac13\right)^2+3\left(y-\frac13\right)^2+\frac43$, amb mínim $\frac43$ a $\left(-\frac13,\frac13\right)$, que és de $\Delta$ perquè $\frac49+\frac49\leq3$. El mínim absolut de $f$ a $A$ és $\frac43$, assolit al punt $\left(-\frac13,\frac13,\frac23\right)$.
[6] $h-2$ és el quadrat de la distància de $(x,y)$ a $(1,-1)$. Aquest punt és a distància $2\sqrt2$ del centre $(-1,1)$, i el punt de $\Delta$ més llunyà de $(1,-1)$ és $(-1,1)+\sqrt3\,\frac{(-1,1)}{\sqrt2}=\left(-1-\frac{\sqrt6}{2},\ 1+\frac{\sqrt6}{2}\right)$, a distància $2\sqrt2+\sqrt3$.
[7] El màxim absolut és $(2\sqrt2+\sqrt3)^2+2=11+2\sqrt6+2=13+2\sqrt6$, assolit al punt $\left(-1-\frac{\sqrt6}{2},\ 1+\frac{\sqrt6}{2},\ 5+2\sqrt6\right)$, on $z=2y-2x+1=5+2\sqrt6$.

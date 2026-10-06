## T4.4:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.4] Proposició 4 (Tema 4) — Fitacions de f i injectivitat local
Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^m$ una funció, i $a\in\Omega$.

(i) Si $f$ és diferenciable en $a$, llavors per a tot $\varepsilon>0$, existeix $\delta>0$ tal que per a tot $x\in B(a,\delta)\subseteq\Omega$, es compleix que $\|f(x)-f(a)\|\leqslant\big(\|Df(a)\|+\varepsilon\big)\|x-a\|$.

(ii) Si $f\in\mathcal{C}^1(\Omega)$, llavors per a tot $\varepsilon>0$ existeix $\delta>0$ tal que per a tot $x,y\in B(a,\delta)\subseteq\Omega$, es compleix que $\|f(x)-f(y)\|\leqslant\big(\|Df(a)\|+\varepsilon\big)\|x-y\|$.

(iii) Si $n=m$, $f\in\mathcal{C}^1(\Omega)$, i $\det Jf(a)\neq 0$, llavors per a tot $\varepsilon>0$ existeix $\delta>0$ tal que per a tot $x,y\in B(a,\delta)\subseteq\Omega$, es compleix que $\|f(x)-f(y)\|\geqslant(c-\varepsilon)\|x-y\|$, on $c=1/\|(Df(a))^{-1}\|$. (En particular, $f$ és localment injectiva.)
Demostració: (i) Com que $f$ és diferenciable en $a$, per a tot $\varepsilon>0$, existeix $\delta>0$ de manera que per a qualsevol $x\in B(a,\delta)\subseteq\Omega$ es compleix que
$$\|f(x)-f(a)-Df(a)(x-a)\|\leq\varepsilon\,\|x-a\|.$$
Aleshores,
$$\begin{aligned}\|f(x)-f(a)\|&=\|f(x)-f(a)-Df(a)(x-a)+Df(a)(x-a)\|\\ &\leq\|f(x)-f(a)-Df(a)(x-a)\|+\|Df(a)(x-a)\|\\ &\leq(\varepsilon+\|Df(a)\|)\,\|x-a\|,\end{aligned}$$
on, al darrer pas, hem fet servir la definició de normes de matrius i vectors consistents.

(ii) Com que $f$ és de classe $\mathcal{C}^1$, sabem que totes les derivades parcials són contínues i, per tant, la diferencial $Df:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ i la seva norma (matricial) $\|Df\|:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}$ també són contínues.
Aleshores, per a tot $\varepsilon>0$, existeix $\delta>0$ tal que $z\in B(a,\delta)\subseteq\Omega$ es compleix que
$$\|Df(z)\|-\|Df(a)\|<\varepsilon;\ \text{ és a dir, }\ \|Df(z)\|<\|Df(a)\|+\varepsilon.$$
Considerem ara dos punts $x,y\in B(a,\delta)$. En virtut del teorema del valor mitjà per a camps vectorials diferenciables (resultat 76 del resum de teoria), prenent $u=f(x)-f(y)$, sabem que existeix $z\in[x,y]$ tal que
$$\langle f(x)-f(y),f(x)-f(y)\rangle=\langle f(x)-f(y),Df(z)\,(x-y)\rangle;$$
Ara bé, per una banda,
$$\langle f(x)-f(y),f(x)-f(y)\rangle=\|f(x)-f(y)\|^2,$$
i, per l'altra, aplicant primer la desigualtat de Cauchy-Schwarz i després la consistència entre norma de matrius i vectors,
$$\begin{aligned}\langle f(x)-f(y),Df(z)\,(x-y)\rangle&\leq\|f(x)-f(y)\|\,\|Df(z)\,(x-y)\|\\ &\leq\|f(x)-f(y)\|\,\|Df(z)\|\,\|x-y\|.\end{aligned}$$
Ajuntant-ho tot, tenim que
$$\|f(x)-f(y)\|^2\leq\|f(x)-f(y)\|\,\|Df(z)\|\,\|(x-y)\|\leq\|f(x)-f(y)\|\,(\|Df(a)\|+\varepsilon)\,\|x-y\|,$$
i, per tant,
$$\|f(x)-f(y)\|\leq(\|Df(a)\|+\varepsilon)\,\|x-y\|.$$

(iii) Considerem la funció $h:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$ definida per $h(x)=f(x)-Df(a)(x-a)$. Observem que és de classe $\mathcal{C}^1$ per ser composició de funcions de classe $\mathcal{C}^1$ i, a més, $Dh(x)=Df(x)-Df(a)$; en particular, $Dh(a)=0$.

Com que és de classe $\mathcal{C}^1$, per l'apartat (ii) sabem que per a tot $\varepsilon>0$ existeix $\delta>0$ tal que per a tot $x,y\in B(a,\delta)\subseteq\Omega$, es compleix que $\|h(x)-h(y)\|\leqslant\big(\|Dh(a)\|+\varepsilon\big)\|x-y\|=\varepsilon\,\|x-y\|$.

D'altra banda, per definició de $h$,
$$\|h(x)-h(y)\|=\|f(x)-Df(a)(x-a)-f(y)+Df(a)(y-a)\|=\|f(x)-f(y)-Df(a)(x-y)\|;$$
és a dir, obtenim la desigualtat
$$\|f(x)-f(y)-Df(a)(x-y)\|\leq\varepsilon\,\|x-y\|.$$

Ara usarem que $\|A-B\|\geq\|A\|-\|B\|$ (Nota: A l'exercici 5(b) de la llista de problemes del tema 1 es demostra una propietat equivalent per a distàncies.) per tal de fitar inferiorment $\|f(x)-f(y)\|$:
$$\begin{aligned}\|f(x)-f(y)\|&=\|f(x)-f(y)-Df(a)(x-y)+Df(a)(x-y)\|\\ &\geq\|Df(a)(x-y)\|-\|f(x)-f(y)-Df(a)(x-y)\|\\ &\geq(c-\varepsilon)\,\|x-y\|,\end{aligned}$$
si demostrem que $\|Df(a)(x-y)\|\geq c\|x-y\|$, on $c:=\dfrac{1}{\|(Df(a))^{-1}\|}$. Per demostrar aquesta desigualtat usarem la hipòtesi que $\det Jf(a)\neq 0$, que ens asssegura que
$$(Df(a))^{-1}\,Df(a)=\mathrm{Id}.$$
Llavors,
$$\|x-y\|=\|(Df(a))^{-1}\,Df(a)\,(x-y)\|\leq\|(Df(a))^{-1}\|\,\|Df(a)\,(x-y)\|,$$
i, en conseqüència,
$$\frac{1}{\|(Df(a))^{-1}\|}\|x-y\|\leq\|Df(a)\,(x-y)\|.$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^m$ una funció i $a\in\Omega$. (i) Si $f$ és diferenciable en $a$, llavors per a tot $\varepsilon>0$ existeix $\delta>0$ tal que per a tot $x,y\in B(a,\delta)\subseteq\Omega$ es compleix $\|f(x)-f(y)\|\leq\big(\|Df(a)\|+\varepsilon\big)\|x-y\|$.
[2] (enunciat) (ii) Si $f\in\mathcal{C}^1(\Omega)$, llavors per a tot $\varepsilon>0$ existeix $\delta>0$ tal que per a tot $x,y\in B(a,\delta)\subseteq\Omega$ es compleix $\|f(x)-f(y)\|\leq\big(\|Df(a)\|+\varepsilon\big)\|x-y\|$.
[3] (enunciat) (iii) Si $n=m$, $f\in\mathcal{C}^1(\Omega)$ i $\det Jf(a)\neq 0$, llavors per a tot $\varepsilon>0$ existeix $\delta>0$ tal que per a tot $x,y\in B(a,\delta)\subseteq\Omega$ es compleix $\|f(x)-f(y)\|\geq(c-\varepsilon)\|x-y\|$, on $c=1/\|(Df(a))^{-1}\|$. (En particular, $f$ és localment injectiva.)
[4] (demostració) (i) Com que $f$ és diferenciable en $a$, donat $\varepsilon>0$ existeix $\delta>0$ tal que $\|f(x)-f(a)-Df(a)(x-a)\|\leq\varepsilon\|x-a\|$ per a tot $x\in B(a,\delta)\subseteq\Omega$. Per la desigualtat triangular i la consistència entre normes de matrius i vectors, $\|f(x)-f(a)\|\leq\|f(x)-f(a)-Df(a)(x-a)\|+\|Df(a)(x-a)\|\leq(\varepsilon+\|Df(a)\|)\|x-a\|$.
[5] (demostració) (ii) Com que $f\in\mathcal{C}^1(\Omega)$, la diferencial $Df$ i la seva norma $\|Df\|$ són contínues en $\Omega$. Per tant, donat $\varepsilon>0$, existeix $\delta>0$ tal que $\|Df(z)\|<\|Df(a)\|+\varepsilon$ per a tot $z\in B(a,\delta)\subseteq\Omega$.
[6] (demostració) Siguin $x,y\in B(a,\delta)$. Pel teorema del valor mitjà per a camps vectorials, aplicat amb $u=f(x)-f(y)$, existeix $z\in[x,y]\subseteq B(a,\delta)$ tal que $\langle f(x)-f(y),f(x)-f(y)\rangle=\langle f(x)-f(y),Df(z)(x-y)\rangle$, és a dir, $\|f(x)-f(y)\|^2=\langle f(x)-f(y),Df(z)(x-y)\rangle$.
[7] (demostració) Per la desigualtat de Cauchy-Schwarz i la consistència de normes, $\|f(x)-f(y)\|^2\leq\|f(x)-f(y)\|\,\|Df(z)\|\,\|x-y\|\leq\|f(x)-f(y)\|\big(\|Df(a)\|+\varepsilon\big)\|x-y\|$. Dividint per $\|f(x)-f(y)\|$ (si és nul, la desigualtat és immediata), obtenim $\|f(x)-f(y)\|\leq\big(\|Df(a)\|+\varepsilon\big)\|x-y\|$.
[8] (demostració) (iii) Sigui $h(x)=f(x)-Df(a)(x-a)$, que és de classe $\mathcal{C}^1$ amb $Dh(x)=Df(x)-Df(a)$; en particular, $Dh(a)=0$. Per l'apartat (ii) aplicat a $h$, donat $\varepsilon>0$ existeix $\delta>0$ tal que $\|h(x)-h(y)\|\leq\varepsilon\|x-y\|$ per a tot $x,y\in B(a,\delta)\subseteq\Omega$, és a dir, $\|f(x)-f(y)-Df(a)(x-y)\|\leq\varepsilon\|x-y\|$.
[9] (demostració) Usant que $\|A-B\|\geq\|A\|-\|B\|$, tenim $\|f(x)-f(y)\|\geq\|Df(a)(x-y)\|-\|f(x)-f(y)-Df(a)(x-y)\|\geq\|Df(a)(x-y)\|-\varepsilon\|x-y\|$. N'hi ha prou, doncs, de veure que $\|Df(a)(x-y)\|\geq c\|x-y\|$.
[10] (demostració) Com que $\det Jf(a)\neq 0$, existeix $(Df(a))^{-1}$ i $\|x-y\|=\|(Df(a))^{-1}Df(a)(x-y)\|\geq\|(Df(a))^{-1}\|\,\|Df(a)(x-y)\|$, d'on $c\|x-y\|\leq\|Df(a)(x-y)\|$. Per tant, $\|f(x)-f(y)\|\geq(c-\varepsilon)\|x-y\|$ per a tot $x,y\in B(a,\delta)$.


## T4.8:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.8] Corol·lari 8 (Tema 4) — Teorema de l'aplicació oberta
Teorema de l'aplicació oberta. Sigui $f:U\subseteq\mathbb{R}^n\to V\subseteq\mathbb{R}^n$ una funció $\mathcal{C}^1(U)$ tal que $\det Jf(a)\neq 0$ per a tot $a\in U$. Aleshores, per a tot obert $B\subseteq U$, $f(B)$ és també un obert.
Demostració: Pel teorema de la funció inversa, $f^{-1}:V\longrightarrow U$ està ben definida i és contínua. Considerem ara un obert $B\subseteq U$. Per la continuïtat de $f^{-1}$, existeix un obert $B'$ tal que $(f^{-1})^{-1}(B)=B'\cap V$. Ara bé, d'una banda, com que $B\subseteq U$, aleshores $B'\subseteq V$, i, de l'altra, $(f^{-1})^{-1}(B)=f(B)$. Per tant, hem vist que $f(B)=B'\subseteq V$. (Nota: Una demostració alternativa: Prenem $x_0\in B$. Per demostrar que $f(B)$ és obert, és suficient provar que existeix un entorn obert de $f(x_0)$ contingut en $f(B)$. Com que $\det Jf(a)\neq 0$, el TFI ens garanteix que existeixen entorns prou petits $U'\in\mathcal{E}_{\mathbf{x_0}}$ i $V'\in\mathcal{E}_{\mathbf{f(x_0)}}$ tals que $f|_{U'}$ és bijectiva, diferenciable i amb inversa diferenciable. Això implica que $V'$ és obert.)

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:U\subseteq\mathbb{R}^n\to V\subseteq\mathbb{R}^n$ una funció $\mathcal{C}^1(U)$, amb $U$ obert, tal que $\det Jf(a)\neq 0$ per a tot $a\in U$.
[2] (enunciat) Aleshores, per a tot obert $B\subseteq U$, $f(B)$ és també un obert i $f|_B:B\to f(B)$ és bijectiva.
[3] (demostració) Sigui $B\subseteq U$ un obert, i siguin $y_0\in f(B)$ i $x_0\in B$ amb $f(x_0)=y_0$.
[4] (demostració) La restricció de $f$ a l'obert $B$ és de classe $\mathcal{C}^1$ i $\det Jf(x_0)\neq 0$. Pel teorema de la funció inversa aplicat a $f|_B$ en $x_0$, existeixen entorns oberts $U'\in\mathcal{E}_{x_0}$, amb $U'\subseteq B$, i $V'=f(U')\in\mathcal{E}_{f(x_0)}$ tals que $f|_{U'}:U'\to V'$ és bijectiva, diferenciable i amb inversa diferenciable.
[5] (demostració) En particular, $V'$ és un obert que conté $y_0=f(x_0)$ i, com que $U'\subseteq B$, $V'=f(U')\subseteq f(B)$.
[6] (demostració) Per tant, $f(B)$ conté un obert no buit, $V'$, i en conseqüència $f(B)$ és obert.


## T4.5:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.
Demostració: Sabem que $f\in\mathcal{C}^1$ (de fet, és $\mathcal{C}^r$). Així doncs, la funció *determinant*,
$$\begin{array}{ccccc}\Omega\subseteq\mathbb{R}^n&\longrightarrow&\mathbb{R}^{n^2}&\longrightarrow&\mathbb{R}\\ x&\longmapsto&Df(x)&\longmapsto&\det Df(x),\end{array}$$
és contínua. Per tant, existeix $\delta_1>0$ tal que per a tot $z\in B(a,\delta_1)$, $\det Df(z)\neq 0$. Aplicant l'apartat iii de la proposició 4, sabem que per a tot $\varepsilon>0$, existeix $\delta_2>0$ tal que per a tot $x,y\in B(a,\delta_2)\subseteq\Omega$, $\|f(x)-f(y)\|\geq(c-\varepsilon)\|x-y\|$. En particular, si prenem $\varepsilon=c/2$, llavors
$$\|f(x)-f(y)\|\geq c/2\,\|x-y\|.$$
Finalment, considerem $\delta=\min\{\delta_1,\delta_2\}$ i $U=B(a,\delta)\subseteq\Omega$.

(i) Per a tot $z\in U$, $\det Df(z)\neq 0$ ja que $z\in U=B(a,\delta)\subseteq B(a,\delta_1)$.
De l'anterior desigualtat, se'n desprèn que si, donats $x,y\in U$, tenim que $f(x)=f(y)$, aleshores $x=y$. Per tant, $f|_U:U\longrightarrow\mathbb{R}^n$ és injectiva.

(ii) Volem veure ara que $V=f(U)$ és un obert de $\mathbb{R}^n$. Per tant, donat $y_0\in V$, hem de trobar $\delta$ tal que $B(y_0,\delta)\subseteq V$.

Com que ja hem vist que $f|_U$ és injectiva, aleshores existeix un únic $x_0\in U$ tal que $f(x_0)=y_0$. Prenem ara $\eta>0$ tal que $B(x_0,\eta)=:U_0\subseteq U$ i que $\overline{U_0}\subseteq U$.

La frontera de $U_0$ ($\mathrm{Fr}(U_0)$) és tancada i fitada i, per tant, compacta. Com que $f$ és contínua, $f(\mathrm{Fr}(U_0))$ també és compacte i, a més, no conté $y_0$ (per injectivitat).

Definim ara $\sigma=\min_{x\in\mathrm{Fr}(U_0)}||y_0-f(x)||>0$ i considerem l'obert $V_0=B(y_0,\sigma/2)$. Si veiem que $V_0\subseteq V$, ja haurem demostrat el que volíem. Així, doncs, prenem $y\in V_0$ i volem trobar $z\in U$ tal que $f(z)=y$ (fixem-nos que amb això, haurem provat que $y\in f(U)=V$ i, en conseqüència, que $V_0\subseteq V$).

Fixat $y\in V_0$, considerem la funció
$$\begin{array}{rcl}\varphi:\Omega&\longrightarrow&\mathbb{R}\\ x&\longmapsto&\|f(x)-y\|,\end{array}$$
que és contínua, i $z:=\arg\min\{\varphi(x)\mid x\in\overline{U_0}\}$, que existeix pel teorema de Weiertrass atès que $\varphi$ és contínua i $\overline{U_0}$ és compacte.

Tenim que $\varphi(x_0)=\|f(x_0)-y\|=\|y_0-y\|<\sigma/2$ ja que $y\in V_0=B(y_0,\sigma/2)$. Per tant, com que $z=\arg\min\{\varphi(x)\mid x\in\overline{U_0}\}$, aleshores, $\varphi(z)\leq\varphi(x)<\sigma/2$. En canvi, per a tot $x\in\mathrm{Fr}(U_0)$, $\varphi(x)=\|f(x)-y\|\geq\|f(x)-y_0\|-\|y_0-y\|>\sigma/2$ perquè $\|f(x)-y\|\geq\sigma$ i $\|y_0-y\|<\sigma/2$. Per tant, el mínim no està a $\mathrm{Fr}(U_0)$ sinó en un punt $z\in U_0$.

Vegem ara que $f(z)=y$.
Com que $\varphi(z)$ és el valor mínim de $\varphi$ sobre $\overline{U_0}$, aleshores $\varphi(z)^2$ també serà el valor mínim de $\varphi(x)^2$ que es podrà atènyer a $\overline{U_0}$, on
$$\varphi(z)^2=\|f(z)-y\|^2=\sum_{k=1}^{n}(f_k(z)-y_k)^2.$$
Llavors, per a tot $i=1,\ldots,n$, i donat que hem vist que $z\in U_0$ (obert),
$$0=\frac{\partial(\varphi^2)}{\partial x_i}(z)=2\sum_{k=1}^{n}(f_k(z)-y_k)\frac{\partial f_k}{\partial x_i}(z)=2\,(f_1(z)-y_1,\ldots,f_n(z)-y_n)\begin{pmatrix}\dfrac{\partial f_1}{\partial x_i}\\ \vdots\\ \dfrac{\partial f_n}{\partial x_i}\end{pmatrix}_{(z)}.$$
Agrupant per a tot $i=1,\ldots,n$, tenim que
$$(f_1(x)-y_1,\ldots,f_n(x)-y_n)\,Jf(z)=(0,\ldots,0).$$
Com que $\det Jf(z)\neq 0$, deduïm que $(f_1(x)-y_1,\ldots,f_n(x)-y_n)=(0,\ldots,0)$ (de fet, és la solució única d'una sistema lineal compatible homogeni) i, per tant, que $f(z)=y$.
En conclusió, $y\in V$ perquè és imatge de $z\in U$ i hem demostrat que $V_0\subseteq V$ perquè $y$ era un punt qualsevol de l'obert $V_0$.

(iii) Comencem veient que $f^{-1}\in\mathcal{C}^1$ i que $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$. Prenem $y_0\in V$ i ens proposem de demostrar que, donat $\varepsilon>0$, existeix $\delta>0$ tal que per a tot $y$ que satisfaci $\|y-y_0\|<\delta$ es compleix que
$$\|f^{-1}(y)-f^{-1}(y_0)-\big(Df(f^{-1}(y_0))\big)^{-1}(y-y_0)\|<\varepsilon\,\|y-y_0\|.$$
Considerem
$$c=\frac{1}{\|(Df(a))^{-1}\|},\qquad c_1=\frac{1}{\|(Df(f^{-1}(y_0)))^{-1}\|}=\frac{1}{\|(Df(x_0))^{-1}\|},\quad\text{amb }y_0=f(x_0).$$
En aquest punt, fem una sèrie d'observacions:

(a) El terme que volem fitar es pot escriure com
$$f^{-1}(y)-f^{-1}(y_0)-\big(Df(f^{-1}(y_0))\big)^{-1}(y-y_0)=x-x_0-\big(Df(x_0)\big)^{-1}(f(x)-f(x_0)).$$
Per tant, si multipliquem ambdues bandes de la igualtat per $Df(x_0)$, tenim que
$$\begin{aligned}&Df(x_0)\Big(f^{-1}(y)-f^{-1}(y_0)-\big(Df(f^{-1}(y_0))\big)^{-1}(y-y_0)\Big)\\ &\qquad=Df(x_0)(x-x_0)-(f(x)-f(x_0)).\end{aligned}\tag{1}$$

(b) Per a tot vector $u\in\mathbb{R}^n$ es té que
$$\|u\|=\|\big(Df(x_0)\big)^{-1}Df(x_0)u\|\leq\|\big(Df(x_0)\big)^{-1}\|\,\|Df(x_0)u\|,$$
i per tant,
$$c_1\,\|u\|=\frac{1}{\|(Df(x_0))^{-1}\|}\|u\|\leq\|Df(x_0)u\|.$$
Si ho apliquem a la igualtat (1), tenim que
$$\begin{aligned}&c_1\,\|f^{-1}(y)-f^{-1}(y_0)-\big(Df(f^{-1}(y_0))\big)^{-1}(y-y_0)\|\\ &\qquad\leq\|Df(x_0)(x-x_0)-(f(x)-f(x_0))\|.\end{aligned}\tag{2}$$

(c) Com que $f$ és diferenciable en $x_0$, per a tot $\varepsilon>0$, existeix un obert $U_3$, amb $x_0\in U_3\subseteq U$, tal que per a tot $x\in U_3$,
$$\|f(x)-f(x_0)-Df(x_0)\,(x-x_0)\|<\frac{\varepsilon\,c\,c_1}{2}\|x-x_0\|.$$

(d) Tal com hem deduït a la demostració de l'apartat (i), per a tot $x\in U$ (en particular, $x\in U_3$),
$$\|f(x)-f(x_0)\|\geq c/2\,\|x-x_0\|,$$
és a dir, per a tot $y\in V_3=f(U_3)\subseteq f(U)=V$,
$$\|y-y_0\|\geq c/2\,\|f^{-1}(y)-f^{-1}(y_0)\|=c/2\,\|x-x_0\|.$$

Tornem ara a l'expressió que volíem fitar i li apliquem els punts anteriors (observació (b) al primer pas, observació (c) al segon pas, observació (d) al tercer pas):
$$\begin{aligned}\|f^{-1}(y)-f^{-1}(y_0)-\big(Df(x_0)\big)^{-1}(y-y_0)\|&\leq\frac{1}{c_1}\|Df(x_0)(x-x_0)-(f(x)-f(x_0))\|\\ &\leq\frac{1}{c_1}\frac{\varepsilon\,c\,c_1}{2}\,\|x-x_0\|\\ &\leq\frac{1}{c_1}\frac{\varepsilon\,c\,c_1}{2}\frac{2}{c}\|y-y_0\|=\varepsilon\,\|y-y_0\|.\end{aligned}$$
Per tant, hem demostrat que $f^{-1}$ és diferenciable i que per a tot $y\in V$,
$$Df^{-1}(y)=\big(Df(f^{-1}(y))\big)^{-1}.$$
Notem que, estrictament, hauríem de redefinir $U:=U_3$ i $V:=V_3$ perquè és en aquests conjunts que hem acabat demostrant totes les propietats.

Ara ens queda veure que si $f\in\mathcal{C}^r(\Omega)$, aleshores $f^{-1}\in\mathcal{C}^r(V)$.

En primer lloc, hem de veure que $f^{-1}\in\mathcal{C}^1(V)$. En efecte, observem d'una banda que, per ser diferenciable, $f^{-1}$ també és contínua, i, de l'altra, que, donat que $f\in\mathcal{C}^1(U)$, $Df$ (vista com una funció de $\mathbb{R}^n$ a $\mathbb{R}^{nm}$ que té per components les derivades parcials de $f$) és contínua en $U$. Per tant, $Df(f^{-1}(y))$ és contínua. La seva matriu inversa existeix gràcies a l'apartat (i) i, a més, les seves components són combinacions lineals de les components de $Df(f^{-1}(y))$. En conclusió, les components de $Df^{-1}(y)=\big(Df(f^{-1}(y))\big)^{-1}$ són totes contínues i, per tant, $f^{-1}\in\mathcal{C}^1(V)$.

Finalment, demostrem que aquest raonament s'estén fins a classe $\mathcal{C}^r$. En efecte, si $f\in\mathcal{C}^r$, aleshores $f^{-1}\in\mathcal{C}^{r-1}$ i $Df\in\mathcal{C}^{r-1}$. Per tant, $Df(f^{-1}(y))$ és de classe $\mathcal{C}^{r-1}$. La seva matriu inversa existeix gràcies a l'apartat (i) i, a més, les seves components són combinacions lineals de les components de $Df(f^{-1}(y))$. En conclusió, les components de $Df^{-1}(y)=\big(Df(f^{-1}(y))\big)^{-1}$ són de classe $\mathcal{C}^{r-1}$ i, per tant, $f^{-1}\in\mathcal{C}^r(V)$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, $r\geq 1$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que:
[2] (enunciat) (i) $f|_U:U\to\mathbb{R}^n$ és injectiva i $\det\big(Jf(z)\big)\neq 0$ per a tot $z\in U$; (ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;
[3] (enunciat) (iii) la inversa $f^{-1}:V\to U$ és de classe $\mathcal{C}^r(V)$ i, per a tot $y_0\in V$, $Df^{-1}(y_0)=\big(Df(y_0)\big)^{-1}$.
[4] (demostració) Com que $f\in\mathcal{C}^1$, la funció $x\mapsto\det Df(x)$ és contínua i, per tant, existeix $\delta_1>0$ tal que $\det Df(z)\neq 0$ per a tot $z\in B(a,\delta_1)$. Per l'apartat (iii) de la proposició 4 amb $\varepsilon=c/2$, on $c=1/\|(Df(a))^{-1}\|$, existeix $\delta_2>0$ tal que $\|f(x)-f(y)\|\geq\frac{c}{2}\|x-y\|$ per a tot $x,y\in B(a,\delta_2)\subseteq\Omega$. Prenem $\delta=\min\{\delta_1,\delta_2\}$ i $U=B(a,\delta)$.
[5] (demostració) (i) Si $z\in U$, aleshores $z\in B(a,\delta_1)$ i, per tant, $\det Df(z)\neq 0$. A més, si $x,y\in U$ compleixen $f(x)=f(y)$, la desigualtat anterior dona $\frac{c}{2}\|x-y\|\leq 0$, és a dir, $x=y$; per tant, $f|_U$ és injectiva.
[6] (demostració) (ii) Sigui $y_0\in V$ i sigui $x_0\in U$ l'únic punt amb $f(x_0)=y_0$. Prenem $\eta>0$ tal que $U_0=B(x_0,\eta)$ compleixi $\overline{U_0}\subseteq U$. La frontera $\mathrm{Fr}(U_0)$ és compacta; per tant, també ho és $f(\mathrm{Fr}(U_0))$, que no conté $y_0$ per la injectivitat de $f|_U$. Així, $\sigma=\min_{x\in\mathrm{Fr}(U_0)}\|y_0-f(x)\|>0$.
[7] (demostració) Vegem que $V_0=B(y_0,\sigma/2)\subseteq V$. Fixat $y\in V_0$, la funció $\varphi(x)=\|f(x)-y\|$ és contínua i, pel teorema de Weierstrass, assoleix el mínim sobre el compacte $\overline{U_0}$ en un punt $z$.
[8] (demostració) D'una banda, $\varphi(z)\leq\varphi(x_0)=\|y_0-y\|<\sigma/2$. De l'altra, per a tot $x\in\mathrm{Fr}(U_0)$, $\varphi(x)=\|f(x)-y\|\geq\|f(x)-y_0\|-\|y_0-y\|>\sigma-\sigma/2=\sigma/2$. Per tant, el mínim no és a la frontera, i $z\in U_0$, que és obert.
[9] (demostració) Aleshores $\varphi^2=\sum_{k=1}^n(f_k-y_k)^2$ també assoleix el mínim sobre $\overline{U_0}$ en $z$, que és un punt interior, i per a $i=1,\ldots,n$ es té $0=\frac{\partial(\varphi^2)}{\partial x_i}(z)=2\sum_{k=1}^n(f_k(z)-y_k)\frac{\partial f_k}{\partial x_i}(z)$, és a dir, $(f(z)-y)^{T}Jf(z)=0$. Com que $z\in U$, $\det Jf(z)\neq 0$, i per tant $f(z)=y$. Així, $y\in f(U)=V$, i $V_0\subseteq V$.
[10] (demostració) (iii) Sigui $y_0\in V$, $x_0=f^{-1}(y_0)$, $c_1=1/\|(Df(x_0))^{-1}\|$ i, per a $y\in V$, $x=f^{-1}(y)$. Per a tot $u\in\mathbb{R}^n$, $\|u\|=\|(Df(x_0))^{-1}Df(x_0)u\|\leq\|(Df(x_0))^{-1}\|\,\|Df(x_0)u\|$, és a dir, $c_1\|u\|\leq\|Df(x_0)u\|$. Aplicat a $u=f^{-1}(y)-f^{-1}(y_0)-(Df(x_0))^{-1}(y-y_0)$, per al qual $Df(x_0)u=Df(x_0)(x-x_0)-(f(x)-f(x_0))$, obtenim $c_1\|u\|\leq\|f(x)-f(x_0)-Df(x_0)(x-x_0)\|$.
[11] (demostració) Donat $\varepsilon>0$, per la diferenciabilitat de $f$ en $x_0$ existeix un obert $U_3$, amb $x_0\in U_3\subseteq U$, tal que $\|f(x)-f(x_0)-Df(x_0)(x-x_0)\|\leq\frac{\varepsilon c c_1}{2}\|x-x_0\|$ per a tot $x\in U_3$. D'altra banda, per la desigualtat de l'inici de la demostració, $\|y-y_0\|\geq\frac{c}{2}\|x-x_0\|$ per a tot $x\in U$; en particular, $f^{-1}$ és contínua i, si $y$ és prou a prop de $y_0$, $x=f^{-1}(y)\in U_3$.
[12] (demostració) Combinant-ho, per a $y$ prou a prop de $y_0$, $\|u\|\leq\frac{1}{c_1}\cdot\frac{\varepsilon c c_1}{2}\|x-x_0\|\leq\frac{\varepsilon c}{2}\cdot\frac{2}{c}\|y-y_0\|=\varepsilon\|y-y_0\|$. Per tant, $f^{-1}$ és diferenciable en $y_0$ i $Df^{-1}(y_0)=(Df(x_0))^{-1}=\big(Df(f^{-1}(y_0))\big)^{-1}$.
[13] (demostració) Finalment, $Df^{-1}(y)=\big(Df(f^{-1}(y))\big)^{-1}$ per a tot $y\in V$. Com que $f^{-1}$ i $Df$ són contínues, $Df(f^{-1}(y))$ és contínua, i les components de la seva inversa (que existeix per (i)) són quocients de polinomis en les seves components amb denominador $\det Df(f^{-1}(y))\neq 0$; per tant, $f^{-1}\in\mathcal{C}^1(V)$. Iterant, si $f^{-1}\in\mathcal{C}^k(V)$ amb $k<r$, aleshores $Df(f^{-1}(y))$ i la seva inversa són de classe $\mathcal{C}^k$, és a dir, $f^{-1}\in\mathcal{C}^{k+1}(V)$; així arribem a $f^{-1}\in\mathcal{C}^r(V)$.


## T4.5:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.
Demostració: Sabem que $f\in\mathcal{C}^1$ (de fet, és $\mathcal{C}^r$). Així doncs, la funció *determinant*,
$$\begin{array}{ccccc}\Omega\subseteq\mathbb{R}^n&\longrightarrow&\mathbb{R}^{n^2}&\longrightarrow&\mathbb{R}\\ x&\longmapsto&Df(x)&\longmapsto&\det Df(x),\end{array}$$
és contínua. Per tant, existeix $\delta_1>0$ tal que per a tot $z\in B(a,\delta_1)$, $\det Df(z)\neq 0$. Aplicant l'apartat iii de la proposició 4, sabem que per a tot $\varepsilon>0$, existeix $\delta_2>0$ tal que per a tot $x,y\in B(a,\delta_2)\subseteq\Omega$, $\|f(x)-f(y)\|\geq(c-\varepsilon)\|x-y\|$. En particular, si prenem $\varepsilon=c/2$, llavors
$$\|f(x)-f(y)\|\geq c/2\,\|x-y\|.$$
Finalment, considerem $\delta=\min\{\delta_1,\delta_2\}$ i $U=B(a,\delta)\subseteq\Omega$.

(i) Per a tot $z\in U$, $\det Df(z)\neq 0$ ja que $z\in U=B(a,\delta)\subseteq B(a,\delta_1)$.
De l'anterior desigualtat, se'n desprèn que si, donats $x,y\in U$, tenim que $f(x)=f(y)$, aleshores $x=y$. Per tant, $f|_U:U\longrightarrow\mathbb{R}^n$ és injectiva.

(ii) Volem veure ara que $V=f(U)$ és un obert de $\mathbb{R}^n$. Per tant, donat $y_0\in V$, hem de trobar $\delta$ tal que $B(y_0,\delta)\subseteq V$.

Com que ja hem vist que $f|_U$ és injectiva, aleshores existeix un únic $x_0\in U$ tal que $f(x_0)=y_0$. Prenem ara $\eta>0$ tal que $B(x_0,\eta)=:U_0\subseteq U$ i que $\overline{U_0}\subseteq U$.

La frontera de $U_0$ ($\mathrm{Fr}(U_0)$) és tancada i fitada i, per tant, compacta. Com que $f$ és contínua, $f(\mathrm{Fr}(U_0))$ també és compacte i, a més, no conté $y_0$ (per injectivitat).

Definim ara $\sigma=\min_{x\in\mathrm{Fr}(U_0)}||y_0-f(x)||>0$ i considerem l'obert $V_0=B(y_0,\sigma/2)$. Si veiem que $V_0\subseteq V$, ja haurem demostrat el que volíem. Així, doncs, prenem $y\in V_0$ i volem trobar $z\in U$ tal que $f(z)=y$ (fixem-nos que amb això, haurem provat que $y\in f(U)=V$ i, en conseqüència, que $V_0\subseteq V$).

Fixat $y\in V_0$, considerem la funció
$$\begin{array}{rcl}\varphi:\Omega&\longrightarrow&\mathbb{R}\\ x&\longmapsto&\|f(x)-y\|,\end{array}$$
que és contínua, i $z:=\arg\min\{\varphi(x)\mid x\in\overline{U_0}\}$, que existeix pel teorema de Weiertrass atès que $\varphi$ és contínua i $\overline{U_0}$ és compacte.

Tenim que $\varphi(x_0)=\|f(x_0)-y\|=\|y_0-y\|<\sigma/2$ ja que $y\in V_0=B(y_0,\sigma/2)$. Per tant, com que $z=\arg\min\{\varphi(x)\mid x\in\overline{U_0}\}$, aleshores, $\varphi(z)\leq\varphi(x)<\sigma/2$. En canvi, per a tot $x\in\mathrm{Fr}(U_0)$, $\varphi(x)=\|f(x)-y\|\geq\|f(x)-y_0\|-\|y_0-y\|>\sigma/2$ perquè $\|f(x)-y\|\geq\sigma$ i $\|y_0-y\|<\sigma/2$. Per tant, el mínim no està a $\mathrm{Fr}(U_0)$ sinó en un punt $z\in U_0$.

Vegem ara que $f(z)=y$.
Com que $\varphi(z)$ és el valor mínim de $\varphi$ sobre $\overline{U_0}$, aleshores $\varphi(z)^2$ també serà el valor mínim de $\varphi(x)^2$ que es podrà atènyer a $\overline{U_0}$, on
$$\varphi(z)^2=\|f(z)-y\|^2=\sum_{k=1}^{n}(f_k(z)-y_k)^2.$$
Llavors, per a tot $i=1,\ldots,n$, i donat que hem vist que $z\in U_0$ (obert),
$$0=\frac{\partial(\varphi^2)}{\partial x_i}(z)=2\sum_{k=1}^{n}(f_k(z)-y_k)\frac{\partial f_k}{\partial x_i}(z)=2\,(f_1(z)-y_1,\ldots,f_n(z)-y_n)\begin{pmatrix}\dfrac{\partial f_1}{\partial x_i}\\ \vdots\\ \dfrac{\partial f_n}{\partial x_i}\end{pmatrix}_{(z)}.$$
Agrupant per a tot $i=1,\ldots,n$, tenim que
$$(f_1(x)-y_1,\ldots,f_n(x)-y_n)\,Jf(z)=(0,\ldots,0).$$
Com que $\det Jf(z)\neq 0$, deduïm que $(f_1(x)-y_1,\ldots,f_n(x)-y_n)=(0,\ldots,0)$ (de fet, és la solució única d'una sistema lineal compatible homogeni) i, per tant, que $f(z)=y$.
En conclusió, $y\in V$ perquè és imatge de $z\in U$ i hem demostrat que $V_0\subseteq V$ perquè $y$ era un punt qualsevol de l'obert $V_0$.

(iii) Comencem veient que $f^{-1}\in\mathcal{C}^1$ i que $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$. Prenem $y_0\in V$ i ens proposem de demostrar que, donat $\varepsilon>0$, existeix $\delta>0$ tal que per a tot $y$ que satisfaci $\|y-y_0\|<\delta$ es compleix que
$$\|f^{-1}(y)-f^{-1}(y_0)-\big(Df(f^{-1}(y_0))\big)^{-1}(y-y_0)\|<\varepsilon\,\|y-y_0\|.$$
Considerem
$$c=\frac{1}{\|(Df(a))^{-1}\|},\qquad c_1=\frac{1}{\|(Df(f^{-1}(y_0)))^{-1}\|}=\frac{1}{\|(Df(x_0))^{-1}\|},\quad\text{amb }y_0=f(x_0).$$
En aquest punt, fem una sèrie d'observacions:

(a) El terme que volem fitar es pot escriure com
$$f^{-1}(y)-f^{-1}(y_0)-\big(Df(f^{-1}(y_0))\big)^{-1}(y-y_0)=x-x_0-\big(Df(x_0)\big)^{-1}(f(x)-f(x_0)).$$
Per tant, si multipliquem ambdues bandes de la igualtat per $Df(x_0)$, tenim que
$$\begin{aligned}&Df(x_0)\Big(f^{-1}(y)-f^{-1}(y_0)-\big(Df(f^{-1}(y_0))\big)^{-1}(y-y_0)\Big)\\ &\qquad=Df(x_0)(x-x_0)-(f(x)-f(x_0)).\end{aligned}\tag{1}$$

(b) Per a tot vector $u\in\mathbb{R}^n$ es té que
$$\|u\|=\|\big(Df(x_0)\big)^{-1}Df(x_0)u\|\leq\|\big(Df(x_0)\big)^{-1}\|\,\|Df(x_0)u\|,$$
i per tant,
$$c_1\,\|u\|=\frac{1}{\|(Df(x_0))^{-1}\|}\|u\|\leq\|Df(x_0)u\|.$$
Si ho apliquem a la igualtat (1), tenim que
$$\begin{aligned}&c_1\,\|f^{-1}(y)-f^{-1}(y_0)-\big(Df(f^{-1}(y_0))\big)^{-1}(y-y_0)\|\\ &\qquad\leq\|Df(x_0)(x-x_0)-(f(x)-f(x_0))\|.\end{aligned}\tag{2}$$

(c) Com que $f$ és diferenciable en $x_0$, per a tot $\varepsilon>0$, existeix un obert $U_3$, amb $x_0\in U_3\subseteq U$, tal que per a tot $x\in U_3$,
$$\|f(x)-f(x_0)-Df(x_0)\,(x-x_0)\|<\frac{\varepsilon\,c\,c_1}{2}\|x-x_0\|.$$

(d) Tal com hem deduït a la demostració de l'apartat (i), per a tot $x\in U$ (en particular, $x\in U_3$),
$$\|f(x)-f(x_0)\|\geq c/2\,\|x-x_0\|,$$
és a dir, per a tot $y\in V_3=f(U_3)\subseteq f(U)=V$,
$$\|y-y_0\|\geq c/2\,\|f^{-1}(y)-f^{-1}(y_0)\|=c/2\,\|x-x_0\|.$$

Tornem ara a l'expressió que volíem fitar i li apliquem els punts anteriors (observació (b) al primer pas, observació (c) al segon pas, observació (d) al tercer pas):
$$\begin{aligned}\|f^{-1}(y)-f^{-1}(y_0)-\big(Df(x_0)\big)^{-1}(y-y_0)\|&\leq\frac{1}{c_1}\|Df(x_0)(x-x_0)-(f(x)-f(x_0))\|\\ &\leq\frac{1}{c_1}\frac{\varepsilon\,c\,c_1}{2}\,\|x-x_0\|\\ &\leq\frac{1}{c_1}\frac{\varepsilon\,c\,c_1}{2}\frac{2}{c}\|y-y_0\|=\varepsilon\,\|y-y_0\|.\end{aligned}$$
Per tant, hem demostrat que $f^{-1}$ és diferenciable i que per a tot $y\in V$,
$$Df^{-1}(y)=\big(Df(f^{-1}(y))\big)^{-1}.$$
Notem que, estrictament, hauríem de redefinir $U:=U_3$ i $V:=V_3$ perquè és en aquests conjunts que hem acabat demostrant totes les propietats.

Ara ens queda veure que si $f\in\mathcal{C}^r(\Omega)$, aleshores $f^{-1}\in\mathcal{C}^r(V)$.

En primer lloc, hem de veure que $f^{-1}\in\mathcal{C}^1(V)$. En efecte, observem d'una banda que, per ser diferenciable, $f^{-1}$ també és contínua, i, de l'altra, que, donat que $f\in\mathcal{C}^1(U)$, $Df$ (vista com una funció de $\mathbb{R}^n$ a $\mathbb{R}^{nm}$ que té per components les derivades parcials de $f$) és contínua en $U$. Per tant, $Df(f^{-1}(y))$ és contínua. La seva matriu inversa existeix gràcies a l'apartat (i) i, a més, les seves components són combinacions lineals de les components de $Df(f^{-1}(y))$. En conclusió, les components de $Df^{-1}(y)=\big(Df(f^{-1}(y))\big)^{-1}$ són totes contínues i, per tant, $f^{-1}\in\mathcal{C}^1(V)$.

Finalment, demostrem que aquest raonament s'estén fins a classe $\mathcal{C}^r$. En efecte, si $f\in\mathcal{C}^r$, aleshores $f^{-1}\in\mathcal{C}^{r-1}$ i $Df\in\mathcal{C}^{r-1}$. Per tant, $Df(f^{-1}(y))$ és de classe $\mathcal{C}^{r-1}$. La seva matriu inversa existeix gràcies a l'apartat (i) i, a més, les seves components són combinacions lineals de les components de $Df(f^{-1}(y))$. En conclusió, les components de $Df^{-1}(y)=\big(Df(f^{-1}(y))\big)^{-1}$ són de classe $\mathcal{C}^{r-1}$ i, per tant, $f^{-1}\in\mathcal{C}^r(V)$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, $r\geq 1$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que:
[2] (enunciat) (i) $f|_U:U\to\mathbb{R}^n$ és injectiva i $\det\big(Jf(z)\big)\neq 0$ per a tot $z\in U$; (ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert, i també ho és $f(\Omega)$;
[3] (enunciat) (iii) la inversa $f^{-1}:V\to U$ és de classe $\mathcal{C}^r(V)$ i, per a tot $y_0\in V$, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.
[4] (demostració) Com que $f\in\mathcal{C}^1$, la funció $x\mapsto\det Df(x)$ és contínua i, per tant, existeix $\delta_1>0$ tal que $\det Df(z)\neq 0$ per a tot $z\in B(a,\delta_1)$. Per l'apartat (iii) de la proposició 4 amb $\varepsilon=c/2$, on $c=1/\|(Df(a))^{-1}\|$, existeix $\delta_2>0$ tal que $\|f(x)-f(y)\|\geq\frac{c}{2}\|x-y\|$ per a tot $x,y\in B(a,\delta_2)\subseteq\Omega$. Prenem $\delta=\min\{\delta_1,\delta_2\}$ i $U=B(a,\delta)$.
[5] (demostració) (i) Si $z\in U$, aleshores $z\in B(a,\delta_1)$ i, per tant, $\det Df(z)\neq 0$. A més, si $x,y\in U$ compleixen $f(x)=f(y)$, la desigualtat anterior dona $\frac{c}{2}\|x-y\|\leq 0$, és a dir, $x=y$; per tant, $f|_U$ és injectiva.
[6] (demostració) (ii) Sigui $y_0\in V$ i sigui $x_0\in U$ l'únic punt amb $f(x_0)=y_0$. Prenem $\eta>0$ tal que $U_0=B(x_0,\eta)$ compleixi $\overline{U_0}\subseteq U$. La frontera $\mathrm{Fr}(U_0)$ és compacta; per tant, també ho és $f(\mathrm{Fr}(U_0))$, que no conté $y_0$ per la injectivitat de $f|_U$. Així, $\sigma=\min_{x\in\mathrm{Fr}(U_0)}\|y_0-f(x)\|>0$.
[7] (demostració) Vegem que $V_0=B(y_0,\sigma/2)\subseteq V$. Fixat $y\in V_0$, la funció $\varphi(x)=\|f(x)-y\|$ és contínua i, pel teorema de Weierstrass, assoleix el mínim sobre el compacte $\overline{U_0}$ en un punt $z$.
[8] (demostració) D'una banda, $\varphi(z)\leq\varphi(x_0)=\|y_0-y\|<\sigma/2$. De l'altra, per a tot $x\in\mathrm{Fr}(U_0)$, $\varphi(x)=\|f(x)-y\|\geq\|f(x)-y_0\|+\|y_0-y\|>\sigma/2$. Per tant, el mínim no és a la frontera, i $z\in U_0$, que és obert.
[9] (demostració) Aleshores $\varphi^2=\sum_{k=1}^n(f_k-y_k)^2$ també assoleix el mínim sobre $\overline{U_0}$ en $z$, que és un punt interior, i per a $i=1,\ldots,n$ es té $0=\frac{\partial(\varphi^2)}{\partial x_i}(z)=2\sum_{k=1}^n(f_k(z)-y_k)\frac{\partial f_k}{\partial x_i}(z)$, és a dir, $(f(z)-y)^{T}Jf(z)=0$. Com que $z\in U$, $\det Jf(z)\neq 0$, i per tant $f(z)=y$. Així, $y\in f(U)=V$, i $V_0\subseteq V$.
[10] (demostració) (iii) Sigui $y_0\in V$, $x_0=f^{-1}(y_0)$, $c_1=1/\|(Df(x_0))^{-1}\|$ i, per a $y\in V$, $x=f^{-1}(y)$. Per a tot $u\in\mathbb{R}^n$, $\|u\|=\|(Df(x_0))^{-1}Df(x_0)u\|\leq\|(Df(x_0))^{-1}\|\,\|Df(x_0)u\|$, és a dir, $c_1\|u\|\leq\|Df(x_0)u\|$. Aplicat a $u=f^{-1}(y)-f^{-1}(y_0)-(Df(x_0))^{-1}(y-y_0)$, per al qual $Df(x_0)u=Df(x_0)(x-x_0)-(f(x)-f(x_0))$, obtenim $c_1\|u\|\leq\|f(x)-f(x_0)-Df(x_0)(x-x_0)\|$.
[11] (demostració) Donat $\varepsilon>0$, per la diferenciabilitat de $f$ en $x_0$ existeix un obert $U_3$, amb $x_0\in U_3\subseteq U$, tal que $\|f(x)-f(x_0)-Df(x_0)(x-x_0)\|\leq\frac{\varepsilon c c_1}{2}\|x-x_0\|$ per a tot $x\in U_3$. D'altra banda, per la desigualtat de l'inici de la demostració, $\|y-y_0\|\geq\frac{c}{2}\|x-x_0\|$ per a tot $x\in U$; en particular, $f^{-1}$ és contínua i, si $y$ és prou a prop de $y_0$, $x=f^{-1}(y)\in U_3$.
[12] (demostració) Combinant-ho, per a $y$ prou a prop de $y_0$, $\|u\|\leq\frac{1}{c_1}\cdot\frac{\varepsilon c c_1}{2}\|x-x_0\|\leq\frac{\varepsilon c}{2}\cdot\frac{2}{c}\|y-y_0\|=\varepsilon\|y-y_0\|$. Per tant, $f^{-1}$ és diferenciable en $y_0$ i $Df^{-1}(y_0)=(Df(x_0))^{-1}=\big(Df(f^{-1}(y_0))\big)^{-1}$.
[13] (demostració) Finalment, $Df^{-1}(y)=\big(Df(f^{-1}(y))\big)^{-1}$ per a tot $y\in V$. Com que $f^{-1}$ i $Df$ són contínues, $Df(f^{-1}(y))$ és contínua, i les components de la seva inversa (que existeix per (i)) són quocients de polinomis en les seves components amb denominador $\det Df(f^{-1}(y))\neq 0$; per tant, $f^{-1}\in\mathcal{C}^1(V)$. Iterant, si $f^{-1}\in\mathcal{C}^k(V)$ amb $k<r$, aleshores $Df(f^{-1}(y))$ i la seva inversa són de classe $\mathcal{C}^k$, és a dir, $f^{-1}\in\mathcal{C}^{k+1}(V)$; així arribem a $f^{-1}\in\mathcal{C}^r(V)$.


## T4.5:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.
Demostració: Sabem que $f\in\mathcal{C}^1$ (de fet, és $\mathcal{C}^r$). Així doncs, la funció *determinant*,
$$\begin{array}{ccccc}\Omega\subseteq\mathbb{R}^n&\longrightarrow&\mathbb{R}^{n^2}&\longrightarrow&\mathbb{R}\\ x&\longmapsto&Df(x)&\longmapsto&\det Df(x),\end{array}$$
és contínua. Per tant, existeix $\delta_1>0$ tal que per a tot $z\in B(a,\delta_1)$, $\det Df(z)\neq 0$. Aplicant l'apartat iii de la proposició 4, sabem que per a tot $\varepsilon>0$, existeix $\delta_2>0$ tal que per a tot $x,y\in B(a,\delta_2)\subseteq\Omega$, $\|f(x)-f(y)\|\geq(c-\varepsilon)\|x-y\|$. En particular, si prenem $\varepsilon=c/2$, llavors
$$\|f(x)-f(y)\|\geq c/2\,\|x-y\|.$$
Finalment, considerem $\delta=\min\{\delta_1,\delta_2\}$ i $U=B(a,\delta)\subseteq\Omega$.

(i) Per a tot $z\in U$, $\det Df(z)\neq 0$ ja que $z\in U=B(a,\delta)\subseteq B(a,\delta_1)$.
De l'anterior desigualtat, se'n desprèn que si, donats $x,y\in U$, tenim que $f(x)=f(y)$, aleshores $x=y$. Per tant, $f|_U:U\longrightarrow\mathbb{R}^n$ és injectiva.

(ii) Volem veure ara que $V=f(U)$ és un obert de $\mathbb{R}^n$. Per tant, donat $y_0\in V$, hem de trobar $\delta$ tal que $B(y_0,\delta)\subseteq V$.

Com que ja hem vist que $f|_U$ és injectiva, aleshores existeix un únic $x_0\in U$ tal que $f(x_0)=y_0$. Prenem ara $\eta>0$ tal que $B(x_0,\eta)=:U_0\subseteq U$ i que $\overline{U_0}\subseteq U$.

La frontera de $U_0$ ($\mathrm{Fr}(U_0)$) és tancada i fitada i, per tant, compacta. Com que $f$ és contínua, $f(\mathrm{Fr}(U_0))$ també és compacte i, a més, no conté $y_0$ (per injectivitat).

Definim ara $\sigma=\min_{x\in\mathrm{Fr}(U_0)}||y_0-f(x)||>0$ i considerem l'obert $V_0=B(y_0,\sigma/2)$. Si veiem que $V_0\subseteq V$, ja haurem demostrat el que volíem. Així, doncs, prenem $y\in V_0$ i volem trobar $z\in U$ tal que $f(z)=y$ (fixem-nos que amb això, haurem provat que $y\in f(U)=V$ i, en conseqüència, que $V_0\subseteq V$).

Fixat $y\in V_0$, considerem la funció
$$\begin{array}{rcl}\varphi:\Omega&\longrightarrow&\mathbb{R}\\ x&\longmapsto&\|f(x)-y\|,\end{array}$$
que és contínua, i $z:=\arg\min\{\varphi(x)\mid x\in\overline{U_0}\}$, que existeix pel teorema de Weiertrass atès que $\varphi$ és contínua i $\overline{U_0}$ és compacte.

Tenim que $\varphi(x_0)=\|f(x_0)-y\|=\|y_0-y\|<\sigma/2$ ja que $y\in V_0=B(y_0,\sigma/2)$. Per tant, com que $z=\arg\min\{\varphi(x)\mid x\in\overline{U_0}\}$, aleshores, $\varphi(z)\leq\varphi(x)<\sigma/2$. En canvi, per a tot $x\in\mathrm{Fr}(U_0)$, $\varphi(x)=\|f(x)-y\|\geq\|f(x)-y_0\|-\|y_0-y\|>\sigma/2$ perquè $\|f(x)-y\|\geq\sigma$ i $\|y_0-y\|<\sigma/2$. Per tant, el mínim no està a $\mathrm{Fr}(U_0)$ sinó en un punt $z\in U_0$.

Vegem ara que $f(z)=y$.
Com que $\varphi(z)$ és el valor mínim de $\varphi$ sobre $\overline{U_0}$, aleshores $\varphi(z)^2$ també serà el valor mínim de $\varphi(x)^2$ que es podrà atènyer a $\overline{U_0}$, on
$$\varphi(z)^2=\|f(z)-y\|^2=\sum_{k=1}^{n}(f_k(z)-y_k)^2.$$
Llavors, per a tot $i=1,\ldots,n$, i donat que hem vist que $z\in U_0$ (obert),
$$0=\frac{\partial(\varphi^2)}{\partial x_i}(z)=2\sum_{k=1}^{n}(f_k(z)-y_k)\frac{\partial f_k}{\partial x_i}(z)=2\,(f_1(z)-y_1,\ldots,f_n(z)-y_n)\begin{pmatrix}\dfrac{\partial f_1}{\partial x_i}\\ \vdots\\ \dfrac{\partial f_n}{\partial x_i}\end{pmatrix}_{(z)}.$$
Agrupant per a tot $i=1,\ldots,n$, tenim que
$$(f_1(x)-y_1,\ldots,f_n(x)-y_n)\,Jf(z)=(0,\ldots,0).$$
Com que $\det Jf(z)\neq 0$, deduïm que $(f_1(x)-y_1,\ldots,f_n(x)-y_n)=(0,\ldots,0)$ (de fet, és la solució única d'una sistema lineal compatible homogeni) i, per tant, que $f(z)=y$.
En conclusió, $y\in V$ perquè és imatge de $z\in U$ i hem demostrat que $V_0\subseteq V$ perquè $y$ era un punt qualsevol de l'obert $V_0$.

(iii) Comencem veient que $f^{-1}\in\mathcal{C}^1$ i que $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$. Prenem $y_0\in V$ i ens proposem de demostrar que, donat $\varepsilon>0$, existeix $\delta>0$ tal que per a tot $y$ que satisfaci $\|y-y_0\|<\delta$ es compleix que
$$\|f^{-1}(y)-f^{-1}(y_0)-\big(Df(f^{-1}(y_0))\big)^{-1}(y-y_0)\|<\varepsilon\,\|y-y_0\|.$$
Considerem
$$c=\frac{1}{\|(Df(a))^{-1}\|},\qquad c_1=\frac{1}{\|(Df(f^{-1}(y_0)))^{-1}\|}=\frac{1}{\|(Df(x_0))^{-1}\|},\quad\text{amb }y_0=f(x_0).$$
En aquest punt, fem una sèrie d'observacions:

(a) El terme que volem fitar es pot escriure com
$$f^{-1}(y)-f^{-1}(y_0)-\big(Df(f^{-1}(y_0))\big)^{-1}(y-y_0)=x-x_0-\big(Df(x_0)\big)^{-1}(f(x)-f(x_0)).$$
Per tant, si multipliquem ambdues bandes de la igualtat per $Df(x_0)$, tenim que
$$\begin{aligned}&Df(x_0)\Big(f^{-1}(y)-f^{-1}(y_0)-\big(Df(f^{-1}(y_0))\big)^{-1}(y-y_0)\Big)\\ &\qquad=Df(x_0)(x-x_0)-(f(x)-f(x_0)).\end{aligned}\tag{1}$$

(b) Per a tot vector $u\in\mathbb{R}^n$ es té que
$$\|u\|=\|\big(Df(x_0)\big)^{-1}Df(x_0)u\|\leq\|\big(Df(x_0)\big)^{-1}\|\,\|Df(x_0)u\|,$$
i per tant,
$$c_1\,\|u\|=\frac{1}{\|(Df(x_0))^{-1}\|}\|u\|\leq\|Df(x_0)u\|.$$
Si ho apliquem a la igualtat (1), tenim que
$$\begin{aligned}&c_1\,\|f^{-1}(y)-f^{-1}(y_0)-\big(Df(f^{-1}(y_0))\big)^{-1}(y-y_0)\|\\ &\qquad\leq\|Df(x_0)(x-x_0)-(f(x)-f(x_0))\|.\end{aligned}\tag{2}$$

(c) Com que $f$ és diferenciable en $x_0$, per a tot $\varepsilon>0$, existeix un obert $U_3$, amb $x_0\in U_3\subseteq U$, tal que per a tot $x\in U_3$,
$$\|f(x)-f(x_0)-Df(x_0)\,(x-x_0)\|<\frac{\varepsilon\,c\,c_1}{2}\|x-x_0\|.$$

(d) Tal com hem deduït a la demostració de l'apartat (i), per a tot $x\in U$ (en particular, $x\in U_3$),
$$\|f(x)-f(x_0)\|\geq c/2\,\|x-x_0\|,$$
és a dir, per a tot $y\in V_3=f(U_3)\subseteq f(U)=V$,
$$\|y-y_0\|\geq c/2\,\|f^{-1}(y)-f^{-1}(y_0)\|=c/2\,\|x-x_0\|.$$

Tornem ara a l'expressió que volíem fitar i li apliquem els punts anteriors (observació (b) al primer pas, observació (c) al segon pas, observació (d) al tercer pas):
$$\begin{aligned}\|f^{-1}(y)-f^{-1}(y_0)-\big(Df(x_0)\big)^{-1}(y-y_0)\|&\leq\frac{1}{c_1}\|Df(x_0)(x-x_0)-(f(x)-f(x_0))\|\\ &\leq\frac{1}{c_1}\frac{\varepsilon\,c\,c_1}{2}\,\|x-x_0\|\\ &\leq\frac{1}{c_1}\frac{\varepsilon\,c\,c_1}{2}\frac{2}{c}\|y-y_0\|=\varepsilon\,\|y-y_0\|.\end{aligned}$$
Per tant, hem demostrat que $f^{-1}$ és diferenciable i que per a tot $y\in V$,
$$Df^{-1}(y)=\big(Df(f^{-1}(y))\big)^{-1}.$$
Notem que, estrictament, hauríem de redefinir $U:=U_3$ i $V:=V_3$ perquè és en aquests conjunts que hem acabat demostrant totes les propietats.

Ara ens queda veure que si $f\in\mathcal{C}^r(\Omega)$, aleshores $f^{-1}\in\mathcal{C}^r(V)$.

En primer lloc, hem de veure que $f^{-1}\in\mathcal{C}^1(V)$. En efecte, observem d'una banda que, per ser diferenciable, $f^{-1}$ també és contínua, i, de l'altra, que, donat que $f\in\mathcal{C}^1(U)$, $Df$ (vista com una funció de $\mathbb{R}^n$ a $\mathbb{R}^{nm}$ que té per components les derivades parcials de $f$) és contínua en $U$. Per tant, $Df(f^{-1}(y))$ és contínua. La seva matriu inversa existeix gràcies a l'apartat (i) i, a més, les seves components són combinacions lineals de les components de $Df(f^{-1}(y))$. En conclusió, les components de $Df^{-1}(y)=\big(Df(f^{-1}(y))\big)^{-1}$ són totes contínues i, per tant, $f^{-1}\in\mathcal{C}^1(V)$.

Finalment, demostrem que aquest raonament s'estén fins a classe $\mathcal{C}^r$. En efecte, si $f\in\mathcal{C}^r$, aleshores $f^{-1}\in\mathcal{C}^{r-1}$ i $Df\in\mathcal{C}^{r-1}$. Per tant, $Df(f^{-1}(y))$ és de classe $\mathcal{C}^{r-1}$. La seva matriu inversa existeix gràcies a l'apartat (i) i, a més, les seves components són combinacions lineals de les components de $Df(f^{-1}(y))$. En conclusió, les components de $Df^{-1}(y)=\big(Df(f^{-1}(y))\big)^{-1}$ són de classe $\mathcal{C}^{r-1}$ i, per tant, $f^{-1}\in\mathcal{C}^r(V)$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, $r\geq 1$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors, per a tot $U\in\mathcal{E}_a$ amb $U\subseteq\Omega$, es compleix:
[2] (enunciat) (i) $f|_U:U\to\mathbb{R}^n$ és injectiva i $\det\big(Jf(z)\big)\neq 0$ per a tot $z\in U$; (ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;
[3] (enunciat) (iii) la inversa $f^{-1}:V\to U$ és de classe $\mathcal{C}^r(V)$ i, per a tot $y_0\in V$, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.
[4] (demostració) Com que $f\in\mathcal{C}^1$, la funció $x\mapsto\det Df(x)$ és contínua i, per tant, existeix $\delta_1>0$ tal que $\det Df(z)\neq 0$ per a tot $z\in B(a,\delta_1)$. Per l'apartat (iii) de la proposició 4 amb $\varepsilon=c/2$, on $c=1/\|(Df(a))^{-1}\|$, existeix $\delta_2>0$ tal que $\|f(x)-f(y)\|\geq\frac{c}{2}\|x-y\|$ per a tot $x,y\in B(a,\delta_2)\subseteq\Omega$. Prenem $\delta=\min\{\delta_1,\delta_2\}$ i $U=B(a,\delta)$.
[5] (demostració) (i) Si $z\in U$, aleshores $z\in B(a,\delta_1)$ i, per tant, $\det Df(z)\neq 0$. A més, si $x,y\in U$ compleixen $f(x)=f(y)$, la desigualtat anterior dona $\frac{c}{2}\|x-y\|\leq 0$, és a dir, $x=y$; per tant, $f|_U$ és injectiva.
[6] (demostració) (ii) Sigui $y_0\in V$ i sigui $x_0\in U$ l'únic punt amb $f(x_0)=y_0$. Prenem $\eta>0$ tal que $U_0=B(x_0,\eta)$ compleixi $\overline{U_0}\subseteq U$. La frontera $\mathrm{Fr}(U_0)$ és compacta; per tant, també ho és $f(\mathrm{Fr}(U_0))$, que no conté $y_0$ per la injectivitat de $f|_U$. Així, $\sigma=\min_{x\in\mathrm{Fr}(U_0)}\|y_0-f(x)\|>0$.
[7] (demostració) Vegem que $V_0=B(y_0,\sigma/2)\subseteq V$. Fixat $y\in V_0$, la funció $\varphi(x)=\|f(x)-y\|$ és contínua i, pel teorema de Weierstrass, assoleix el mínim sobre el compacte $\overline{U_0}$ en un punt $z$.
[8] (demostració) D'una banda, $\varphi(z)\leq\varphi(x_0)=\|y_0-y\|<\sigma/2$. De l'altra, per a tot $x\in\mathrm{Fr}(U_0)$, $\varphi(x)=\|f(x)-y\|\geq\|f(x)-y_0\|-\|y_0-y\|>\sigma-\sigma/2=\sigma/2$. Per tant, el mínim no és a la frontera, i $z\in U_0$, que és obert.
[9] (demostració) Aleshores $\varphi^2=\sum_{k=1}^n(f_k-y_k)^2$ també assoleix el mínim sobre $\overline{U_0}$ en $z$, que és un punt interior, i per a $i=1,\ldots,n$ es té $0=\frac{\partial(\varphi^2)}{\partial x_i}(z)=2\sum_{k=1}^n(f_k(z)-y_k)\frac{\partial f_k}{\partial x_i}(z)$, és a dir, $(f(z)-y)^{T}Jf(z)=0$. Com que $\det Jf(x_0)\neq 0$, aquest sistema lineal només té la solució nul·la, i per tant $f(z)=y$. Així, $y\in f(U)=V$, i $V_0\subseteq V$.
[10] (demostració) (iii) Sigui $y_0\in V$, $x_0=f^{-1}(y_0)$, $c_1=1/\|(Df(x_0))^{-1}\|$ i, per a $y\in V$, $x=f^{-1}(y)$. Per a tot $u\in\mathbb{R}^n$, $\|u\|=\|(Df(x_0))^{-1}Df(x_0)u\|\leq\|(Df(x_0))^{-1}\|\,\|Df(x_0)u\|$, és a dir, $c_1\|u\|\leq\|Df(x_0)u\|$. Aplicat a $u=f^{-1}(y)-f^{-1}(y_0)-(Df(x_0))^{-1}(y-y_0)$, per al qual $Df(x_0)u=Df(x_0)(x-x_0)-(f(x)-f(x_0))$, obtenim $c_1\|u\|\leq\|f(x)-f(x_0)-Df(x_0)(x-x_0)\|$.
[11] (demostració) Donat $\varepsilon>0$, per la diferenciabilitat de $f$ en $x_0$ existeix un obert $U_3$, amb $x_0\in U_3\subseteq U$, tal que $\|f(x)-f(x_0)-Df(x_0)(x-x_0)\|\leq\frac{\varepsilon c c_1}{2}\|x-x_0\|$ per a tot $x\in U_3$. D'altra banda, per la desigualtat de l'inici de la demostració, $\|x-x_0\|\geq\frac{c}{2}\|y-y_0\|$ per a tot $x\in U$; en particular, $f^{-1}$ és contínua i, si $y$ és prou a prop de $y_0$, $x=f^{-1}(y)\in U_3$.
[12] (demostració) Combinant-ho, per a $y$ prou a prop de $y_0$, $\|u\|\leq\frac{1}{c_1}\cdot\frac{\varepsilon c c_1}{2}\|x-x_0\|\leq\frac{\varepsilon c}{2}\cdot\frac{2}{c}\|y-y_0\|=\varepsilon\|y-y_0\|$. Per tant, $f^{-1}$ és diferenciable en $y_0$ i $Df^{-1}(y_0)=(Df(x_0))^{-1}=\big(Df(f^{-1}(y_0))\big)^{-1}$.
[13] (demostració) Finalment, $Df^{-1}(y)=\big(Df(f^{-1}(y))\big)^{-1}$ per a tot $y\in V$. Com que $f^{-1}$ i $Df$ són contínues, $Df(f^{-1}(y))$ és contínua, i les components de la seva inversa (que existeix per (i)) són quocients de polinomis en les seves components amb denominador $\det Df(f^{-1}(y))\neq 0$; per tant, $f^{-1}\in\mathcal{C}^1(V)$. Iterant, si $f^{-1}\in\mathcal{C}^k(V)$ amb $k<r$, aleshores $Df(f^{-1}(y))$ i la seva inversa són de classe $\mathcal{C}^k$, és a dir, $f^{-1}\in\mathcal{C}^{k+1}(V)$; així arribem a $f^{-1}\in\mathcal{C}^r(V)$.


## T4.13:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]
Demostració: (i) Considerem la funció
$$\begin{aligned}f:G\subseteq\mathbb{R}^{n+m}&\longrightarrow\mathbb{R}^{n+m}\\ (x,y)&\longmapsto(x,\Phi(x,y)),\quad(x,y)=(x_1,\ldots,x_n,y_1,\ldots,y_m).\end{aligned}$$
Clarament, $f\in\mathcal{C}^r(G)$ i $f(a,b)=(a,0)$, i el determinant de la seva matriu jacobiana en $(a,b)$ no s'anul·la; en efecte,
$$\det(Jf(a,b))=\begin{vmatrix}1&0&\ldots&0&0&\ldots&0\\ 0&\ddots&\ddots&\vdots&\vdots&\ldots&0\\ \vdots&\ddots&\ddots&0&\vdots&\ldots&0\\ 0&\ddots&0&1&0&\ldots&0\\ \frac{\partial\Phi_1}{\partial x_1}&\ldots&\ldots&\frac{\partial\Phi_1}{\partial x_n}&\frac{\partial\Phi_1}{\partial y_1}&\ldots&\frac{\partial\Phi_1}{\partial y_m}\\ \vdots&\vdots&\vdots&\vdots&\vdots&\vdots&\vdots\\ \frac{\partial\Phi_m}{\partial x_1}&\ldots&\ldots&\frac{\partial\Phi_m}{\partial x_n}&\frac{\partial\Phi_m}{\partial y_1}&\ldots&\frac{\partial\Phi_m}{\partial y_m}\end{vmatrix}=\begin{vmatrix}\frac{\partial\Phi_1}{\partial y_1}&\ldots&\frac{\partial\Phi_1}{\partial y_m}\\ \vdots&\vdots&\vdots\\ \frac{\partial\Phi_m}{\partial y_1}&\ldots&\frac{\partial\Phi_m}{\partial y_m}\end{vmatrix}\neq 0.$$
Per tant, hi podem aplicar el teorema de la funció inversa, que ens assegura que existeix un obert $U\subseteq G$ tal que $(a,b)\in U$ i:

(a) $f|_U:U\to\mathbb{R}^{n+m}$ és injectiva, $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$ i, a més, com que $\det Jf(z)=1\cdot\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}$, tenim que $\det\Big(\dfrac{\partial\Phi_i}{\partial y_j}(z)\Big)_{i,j=1,\ldots,m}\neq 0$ per a tot $z\in U$;

(b) $V=f(U)\subseteq\mathbb{R}^{n+m}$ és obert;

(c) existeix la inversa $f^{-1}:V\to U$, $f^{-1}\in\mathcal{C}^r(V)$;

A més, observem que $f^{-1}$ és de la forma $f^{-1}(u,v)=(u,h(u,v))\in U$, on $(u,v)\in V$.

(ii) Definim l'obert $\Omega\subset\mathbb{R}^n$ i la funció $\varphi:\Omega\longrightarrow\mathbb{R}^m$ de la següent manera:
$$\Omega=\{x\in\mathbb{R}^n:(x,0,\overset{(m)}{\ldots},0)\in V\};\qquad\begin{aligned}\varphi:\Omega\subset\mathbb{R}^n&\longrightarrow\mathbb{R}^m\\ u&\longmapsto h(u,0).\end{aligned}$$
Vegem que el conjunt $\Omega$ és obert. Prenem $x_0\in\Omega$, és a dir, $(x_0,0)\in V$, que és obert. Per tant, existeix $\varepsilon>0$ tal que $B((x_0,0),\varepsilon)\subseteq V\subseteq\mathbb{R}^{n+m}$. Demostrarem que $B(x_0,\varepsilon)\subseteq\Omega\subseteq\mathbb{R}^n$: si prenem $x\in B(x_0,\varepsilon)$, tenim que $d(x,x_0)<\varepsilon$ i, per tant, $d((x,0,\ldots,0)),(x_0,0,\ldots,0))=d(x,x_0)<\varepsilon$. Això ens diu que $(x,0)\in B((x_0,0),\varepsilon)\subset V$, que implica que $x\in\Omega$ per construcció de $\Omega$.

D'altra banda, $\varphi$ està ben definida i és de classe $\mathcal{C}^r$. En efecte, donat $u\in\Omega$, $(u,0)\in V$ i, per tant, $\varphi(u)=h(u,0)$ està ben definit. De manera similar, $f^{-1}(u,0)=(u,h(u,0))=(u,\varphi(u))$; és a dir, $\varphi$ és una component de $f^{-1}$, i per tant també és de classe $\mathcal{C}^r$.

En aquest punt, fem una observació que ens serà útil en les demostracions dels passos restants del teorema, així com en els teoremes del rang.

[Aquí les notes intercalen l'Observació 14, que és l'ítem T4.14 i la seva demostració.]

Per acabar la demostració de l'apartat (ii) del teorema de la funció implícita, ho apliquem a $(a,b)\in U$ tal que $\Phi(a,b)=0$. Per l'observació i usant la definició de $\varphi$, obtenim
$$b=h(a,\Phi(a,b))=h(a,0)=\varphi(a).$$

(iii) Hem de veure que $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$.

$\subseteq$ Prenem $(x,y)\in U$ amb $\Phi(x,y)=0$.
Primer de tot, ens assegurem que $x\in\Omega$: en efecte, com que $f(x,y)=(x,\Phi(x,y))=(x,0)\in V$, aleshores $x\in\Omega$ per definició d'$\Omega$, justament.
D'altra banda, per la primera igualtat de l'observació 14 i la definició de $\varphi$,
$$y=h(x,\Phi(x,y))=h(x,0)=\varphi(x);$$
per tant $(x,y)=(x,\varphi(x))\in\{(u,\varphi(u))\mid u\in\Omega\}$.

$\supseteq$ Prenem $(u,\varphi(u))$ amb $u\in\Omega$. Primer de tot, ens assegurem que $(u,\varphi(u))\in U$: en efecte, per definició d'$\Omega$, $(u,0)\in V$, com que $f^{-1}(u,0)=(u,h(u,0))=(u,\varphi(u))$ i $f^{-1}:V\to U$, llavors $(u,\varphi(u))\in U$.
D'altra banda, usant la definició de $\varphi$ i la segona igualtat de l'observació 14,
$$\Phi(u,\varphi(u))=\Phi(u,h(u,0))=0.$$

RESULTATS DELS APUNTS QUE CITA:
[T4.14] Observació 14 (Tema 4) — Igualtats entre h i Φ
Siguin $(x,y)\in U$ i $(u,v)\in V$, amb $x,u\in\mathbb{R}^n$ i $y,v\in\mathbb{R}^m$. Llavors, es compleixen les igualtats
$$y=h(x,\Phi(x,y));\qquad\Phi(u,h(u,v))=v.$$
</apunts>

### Document a revisar

[1] (enunciat) Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$.
[2] (enunciat) Aleshores existeixen dos oberts $U$ i $\Omega$, amb $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G$, i una funció $\varphi:\Omega\to\mathbb{R}^m$ tals que: (i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ per a tot $z\in U$; (ii) $\varphi\in\mathcal{C}^\infty(\Omega)$ i $\varphi(a)=b$;
[3] (enunciat) (iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.
[4] (demostració) (i) Considerem $f:G\to\mathbb{R}^{n+m}$, $f(x,y)=(x,\Phi(x,y))$. Clarament $f\in\mathcal{C}^r(G)$ i $f(a,b)=(a,0)$. La matriu $Jf$ és triangular inferior per blocs, amb blocs diagonals $\mathrm{Id}_n$ i $\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}$; per tant, $\det Jf(a,b)=\det\big(\partial\Phi_i/\partial y_j(a,b)\big)\neq 0$.
[5] (demostració) Pel teorema de la funció inversa, existeix un obert $U\subseteq G$ amb $(a,b)\in U$ tal que $f|_U$ és injectiva i $\det Jf(z)\neq 0$ per a tot $z\in U$, $V=f(U)$ és obert i $f^{-1}:V\to U$ és de classe $\mathcal{C}^r(V)$. Com que $\det Jf(z)=\det\big(\partial\Phi_i/\partial y_j(z)\big)$, això demostra (i).
[6] (demostració) (ii) Com que $f$ conserva les $n$ primeres coordenades, $f^{-1}$ és de la forma $f^{-1}(u,v)=(u,h(u,v))$ per a $(u,v)\in V$. Definim $\Omega=\{x\in\mathbb{R}^n:(x,0)\in V\}$ i $\varphi:\Omega\to\mathbb{R}^m$, $\varphi(u)=h(u,0)$. Observem que $a\in\Omega$, ja que $(a,0)=f(a,b)\in V$.
[7] (demostració) $\Omega$ és obert: si $x_0\in\Omega$, aleshores $(x_0,0)\in V$, que és obert, i existeix $\varepsilon>0$ amb $B((x_0,0),\varepsilon)\subseteq V$. Si $\|x-x_0\|<\varepsilon$, aleshores $\|(x,0)-(x_0,0)\|=\|x-x_0\|<\varepsilon$, de manera que $(x,0)\in V$, és a dir, $x\in\Omega$.
[8] (demostració) $\varphi$ està ben definida, perquè $(u,0)\in V$ per a tot $u\in\Omega$; i com que $f^{-1}(u,0)=(u,h(u,0))=(u,\varphi(u))$, $\varphi$ és una component de $f^{-1}$, i per tant $\varphi\in\mathcal{C}^r(\Omega)$.
[9] (demostració) Per la bijectivitat de $f:U\to V$, per a $(x,y)\in U$ i $(u,v)\in V$ es té $(x,y)=f^{-1}(f(x,y))=(x,h(x,\Phi(x,y)))$ i $(u,v)=f(f^{-1}(u,v))=(u,\Phi(u,h(u,v)))$; és a dir, $y=h(x,\Phi(x,y))$ i $\Phi(u,h(u,v))=v$. En particular, $b=h(a,\Phi(a,b))=h(a,0)=\varphi(a)$, i queda demostrat (ii).
[10] (demostració) (iii) $\subseteq$: sigui $(x,y)\in U$ amb $\Phi(x,y)=0$. Aleshores $f(x,y)=(x,0)\in V$, és a dir, $x\in\Omega$, i per la primera de les igualtats anteriors, $y=h(x,\Phi(x,y))=h(x,0)=\varphi(x)$.
[11] (demostració) $\supseteq$: sigui $u\in\Omega$. Aleshores $(u,0)\in V$ i $(u,\varphi(u))=f^{-1}(u,0)\in U$, ja que $f^{-1}:V\to U$; a més, per la segona igualtat, $\Phi(u,\varphi(u))=\Phi(u,h(u,0))=0$.


## T4.13:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]
Demostració: (i) Considerem la funció
$$\begin{aligned}f:G\subseteq\mathbb{R}^{n+m}&\longrightarrow\mathbb{R}^{n+m}\\ (x,y)&\longmapsto(x,\Phi(x,y)),\quad(x,y)=(x_1,\ldots,x_n,y_1,\ldots,y_m).\end{aligned}$$
Clarament, $f\in\mathcal{C}^r(G)$ i $f(a,b)=(a,0)$, i el determinant de la seva matriu jacobiana en $(a,b)$ no s'anul·la; en efecte,
$$\det(Jf(a,b))=\begin{vmatrix}1&0&\ldots&0&0&\ldots&0\\ 0&\ddots&\ddots&\vdots&\vdots&\ldots&0\\ \vdots&\ddots&\ddots&0&\vdots&\ldots&0\\ 0&\ddots&0&1&0&\ldots&0\\ \frac{\partial\Phi_1}{\partial x_1}&\ldots&\ldots&\frac{\partial\Phi_1}{\partial x_n}&\frac{\partial\Phi_1}{\partial y_1}&\ldots&\frac{\partial\Phi_1}{\partial y_m}\\ \vdots&\vdots&\vdots&\vdots&\vdots&\vdots&\vdots\\ \frac{\partial\Phi_m}{\partial x_1}&\ldots&\ldots&\frac{\partial\Phi_m}{\partial x_n}&\frac{\partial\Phi_m}{\partial y_1}&\ldots&\frac{\partial\Phi_m}{\partial y_m}\end{vmatrix}=\begin{vmatrix}\frac{\partial\Phi_1}{\partial y_1}&\ldots&\frac{\partial\Phi_1}{\partial y_m}\\ \vdots&\vdots&\vdots\\ \frac{\partial\Phi_m}{\partial y_1}&\ldots&\frac{\partial\Phi_m}{\partial y_m}\end{vmatrix}\neq 0.$$
Per tant, hi podem aplicar el teorema de la funció inversa, que ens assegura que existeix un obert $U\subseteq G$ tal que $(a,b)\in U$ i:

(a) $f|_U:U\to\mathbb{R}^{n+m}$ és injectiva, $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$ i, a més, com que $\det Jf(z)=1\cdot\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}$, tenim que $\det\Big(\dfrac{\partial\Phi_i}{\partial y_j}(z)\Big)_{i,j=1,\ldots,m}\neq 0$ per a tot $z\in U$;

(b) $V=f(U)\subseteq\mathbb{R}^{n+m}$ és obert;

(c) existeix la inversa $f^{-1}:V\to U$, $f^{-1}\in\mathcal{C}^r(V)$;

A més, observem que $f^{-1}$ és de la forma $f^{-1}(u,v)=(u,h(u,v))\in U$, on $(u,v)\in V$.

(ii) Definim l'obert $\Omega\subset\mathbb{R}^n$ i la funció $\varphi:\Omega\longrightarrow\mathbb{R}^m$ de la següent manera:
$$\Omega=\{x\in\mathbb{R}^n:(x,0,\overset{(m)}{\ldots},0)\in V\};\qquad\begin{aligned}\varphi:\Omega\subset\mathbb{R}^n&\longrightarrow\mathbb{R}^m\\ u&\longmapsto h(u,0).\end{aligned}$$
Vegem que el conjunt $\Omega$ és obert. Prenem $x_0\in\Omega$, és a dir, $(x_0,0)\in V$, que és obert. Per tant, existeix $\varepsilon>0$ tal que $B((x_0,0),\varepsilon)\subseteq V\subseteq\mathbb{R}^{n+m}$. Demostrarem que $B(x_0,\varepsilon)\subseteq\Omega\subseteq\mathbb{R}^n$: si prenem $x\in B(x_0,\varepsilon)$, tenim que $d(x,x_0)<\varepsilon$ i, per tant, $d((x,0,\ldots,0)),(x_0,0,\ldots,0))=d(x,x_0)<\varepsilon$. Això ens diu que $(x,0)\in B((x_0,0),\varepsilon)\subset V$, que implica que $x\in\Omega$ per construcció de $\Omega$.

D'altra banda, $\varphi$ està ben definida i és de classe $\mathcal{C}^r$. En efecte, donat $u\in\Omega$, $(u,0)\in V$ i, per tant, $\varphi(u)=h(u,0)$ està ben definit. De manera similar, $f^{-1}(u,0)=(u,h(u,0))=(u,\varphi(u))$; és a dir, $\varphi$ és una component de $f^{-1}$, i per tant també és de classe $\mathcal{C}^r$.

En aquest punt, fem una observació que ens serà útil en les demostracions dels passos restants del teorema, així com en els teoremes del rang.

[Aquí les notes intercalen l'Observació 14, que és l'ítem T4.14 i la seva demostració.]

Per acabar la demostració de l'apartat (ii) del teorema de la funció implícita, ho apliquem a $(a,b)\in U$ tal que $\Phi(a,b)=0$. Per l'observació i usant la definició de $\varphi$, obtenim
$$b=h(a,\Phi(a,b))=h(a,0)=\varphi(a).$$

(iii) Hem de veure que $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$.

$\subseteq$ Prenem $(x,y)\in U$ amb $\Phi(x,y)=0$.
Primer de tot, ens assegurem que $x\in\Omega$: en efecte, com que $f(x,y)=(x,\Phi(x,y))=(x,0)\in V$, aleshores $x\in\Omega$ per definició d'$\Omega$, justament.
D'altra banda, per la primera igualtat de l'observació 14 i la definició de $\varphi$,
$$y=h(x,\Phi(x,y))=h(x,0)=\varphi(x);$$
per tant $(x,y)=(x,\varphi(x))\in\{(u,\varphi(u))\mid u\in\Omega\}$.

$\supseteq$ Prenem $(u,\varphi(u))$ amb $u\in\Omega$. Primer de tot, ens assegurem que $(u,\varphi(u))\in U$: en efecte, per definició d'$\Omega$, $(u,0)\in V$, com que $f^{-1}(u,0)=(u,h(u,0))=(u,\varphi(u))$ i $f^{-1}:V\to U$, llavors $(u,\varphi(u))\in U$.
D'altra banda, usant la definició de $\varphi$ i la segona igualtat de l'observació 14,
$$\Phi(u,\varphi(u))=\Phi(u,h(u,0))=0.$$

RESULTATS DELS APUNTS QUE CITA:
[T4.14] Observació 14 (Tema 4) — Igualtats entre h i Φ
Siguin $(x,y)\in U$ i $(u,v)\in V$, amb $x,u\in\mathbb{R}^n$ i $y,v\in\mathbb{R}^m$. Llavors, es compleixen les igualtats
$$y=h(x,\Phi(x,y));\qquad\Phi(u,h(u,v))=v.$$
</apunts>

### Document a revisar

[1] (enunciat) Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$.
[2] (enunciat) Aleshores existeixen dos oberts $U$ i $\Omega$, amb $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G$, i una funció $\varphi:\Omega\to\mathbb{R}^m$ tals que: (i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ per a tot $z\in G$; (ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;
[3] (enunciat) (iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.
[4] (demostració) (i) Considerem $f:G\to\mathbb{R}^{n+m}$, $f(x,y)=(x,\Phi(x,y))$. Clarament $f\in\mathcal{C}^r(G)$ i $f(a,b)=(a,0)$. La matriu $Jf$ és triangular inferior per blocs, amb blocs diagonals $\mathrm{Id}_n$ i $\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}$; per tant, $\det Jf(a,b)=\det\big(\partial\Phi_i/\partial y_j(a,b)\big)\neq 0$.
[5] (demostració) Pel teorema de la funció inversa, existeix un obert $U\subseteq G$ amb $(a,b)\in U$ tal que $f|_U$ és injectiva i $\det Jf(z)\neq 0$ per a tot $z\in U$, $V=f(U)$ és obert i $f^{-1}:V\to U$ és de classe $\mathcal{C}^r(V)$. Com que $\det Jf(z)=\det\big(\partial\Phi_i/\partial x_j(z)\big)$, això demostra (i).
[6] (demostració) (ii) Com que $f$ conserva les $n$ primeres coordenades, $f^{-1}$ és de la forma $f^{-1}(u,v)=(u,h(u,v))$ per a $(u,v)\in V$. Definim $\Omega=\{x\in\mathbb{R}^n:(x,0)\in V\}$ i $\varphi:\Omega\to\mathbb{R}^m$, $\varphi(u)=h(u,0)$. Observem que $a\in\Omega$, ja que $(a,0)=f(a,b)\in V$.
[7] (demostració) $\Omega$ és obert: si $x_0\in\Omega$, aleshores $(x_0,0)\in V$, que és obert, i existeix $\varepsilon>0$ amb $B((x_0,0),\varepsilon)\subseteq V$. Si $\|x-x_0\|<\varepsilon$, aleshores $\|(x,0)-(x_0,0)\|=\|x-x_0\|<\varepsilon$, de manera que $(x,0)\in V$, és a dir, $x\in\Omega$.
[8] (demostració) $\varphi$ està ben definida, perquè $(u,0)\in V$ per a tot $u\in\Omega$; i com que $f^{-1}(u,0)=(u,h(u,0))=(u,\varphi(u))$, $\varphi$ és una component de $f^{-1}$, i per tant $\varphi\in\mathcal{C}^r(\Omega)$.
[9] (demostració) Per la bijectivitat de $f:U\to V$, per a $(x,y)\in U$ i $(u,v)\in V$ es té $(x,y)=f^{-1}(f(x,y))=(x,h(x,\Phi(x,y)))$ i $(u,v)=f(f^{-1}(u,v))=(u,\Phi(u,h(u,v)))$; és a dir, $y=h(x,\Phi(x,y))$ i $\Phi(u,h(u,v))=v$. En particular, $b=h(a,\Phi(a,b))=h(a,0)=\varphi(a)$, i queda demostrat (ii).
[10] (demostració) (iii) $\subseteq$: sigui $(x,y)\in U$ amb $\Phi(x,y)=0$. Aleshores $f(x,y)=(x,0)\in V$, és a dir, $x\in\Omega$, i per la primera de les igualtats anteriors, $y=h(x,\Phi(x,y))=h(x,0)=\varphi(x)$.
[11] (demostració) $\supseteq$: sigui $u\in\Omega$. Aleshores $(u,0)\in V$ i $(u,\varphi(u))=f^{-1}(u,0)\in U$, ja que $f^{-1}:V\to U$; a més, per la segona igualtat, $\Phi(u,\varphi(u))=\Phi(u,h(u,0))=0$.


## T4.13:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]
Demostració: (i) Considerem la funció
$$\begin{aligned}f:G\subseteq\mathbb{R}^{n+m}&\longrightarrow\mathbb{R}^{n+m}\\ (x,y)&\longmapsto(x,\Phi(x,y)),\quad(x,y)=(x_1,\ldots,x_n,y_1,\ldots,y_m).\end{aligned}$$
Clarament, $f\in\mathcal{C}^r(G)$ i $f(a,b)=(a,0)$, i el determinant de la seva matriu jacobiana en $(a,b)$ no s'anul·la; en efecte,
$$\det(Jf(a,b))=\begin{vmatrix}1&0&\ldots&0&0&\ldots&0\\ 0&\ddots&\ddots&\vdots&\vdots&\ldots&0\\ \vdots&\ddots&\ddots&0&\vdots&\ldots&0\\ 0&\ddots&0&1&0&\ldots&0\\ \frac{\partial\Phi_1}{\partial x_1}&\ldots&\ldots&\frac{\partial\Phi_1}{\partial x_n}&\frac{\partial\Phi_1}{\partial y_1}&\ldots&\frac{\partial\Phi_1}{\partial y_m}\\ \vdots&\vdots&\vdots&\vdots&\vdots&\vdots&\vdots\\ \frac{\partial\Phi_m}{\partial x_1}&\ldots&\ldots&\frac{\partial\Phi_m}{\partial x_n}&\frac{\partial\Phi_m}{\partial y_1}&\ldots&\frac{\partial\Phi_m}{\partial y_m}\end{vmatrix}=\begin{vmatrix}\frac{\partial\Phi_1}{\partial y_1}&\ldots&\frac{\partial\Phi_1}{\partial y_m}\\ \vdots&\vdots&\vdots\\ \frac{\partial\Phi_m}{\partial y_1}&\ldots&\frac{\partial\Phi_m}{\partial y_m}\end{vmatrix}\neq 0.$$
Per tant, hi podem aplicar el teorema de la funció inversa, que ens assegura que existeix un obert $U\subseteq G$ tal que $(a,b)\in U$ i:

(a) $f|_U:U\to\mathbb{R}^{n+m}$ és injectiva, $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$ i, a més, com que $\det Jf(z)=1\cdot\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}$, tenim que $\det\Big(\dfrac{\partial\Phi_i}{\partial y_j}(z)\Big)_{i,j=1,\ldots,m}\neq 0$ per a tot $z\in U$;

(b) $V=f(U)\subseteq\mathbb{R}^{n+m}$ és obert;

(c) existeix la inversa $f^{-1}:V\to U$, $f^{-1}\in\mathcal{C}^r(V)$;

A més, observem que $f^{-1}$ és de la forma $f^{-1}(u,v)=(u,h(u,v))\in U$, on $(u,v)\in V$.

(ii) Definim l'obert $\Omega\subset\mathbb{R}^n$ i la funció $\varphi:\Omega\longrightarrow\mathbb{R}^m$ de la següent manera:
$$\Omega=\{x\in\mathbb{R}^n:(x,0,\overset{(m)}{\ldots},0)\in V\};\qquad\begin{aligned}\varphi:\Omega\subset\mathbb{R}^n&\longrightarrow\mathbb{R}^m\\ u&\longmapsto h(u,0).\end{aligned}$$
Vegem que el conjunt $\Omega$ és obert. Prenem $x_0\in\Omega$, és a dir, $(x_0,0)\in V$, que és obert. Per tant, existeix $\varepsilon>0$ tal que $B((x_0,0),\varepsilon)\subseteq V\subseteq\mathbb{R}^{n+m}$. Demostrarem que $B(x_0,\varepsilon)\subseteq\Omega\subseteq\mathbb{R}^n$: si prenem $x\in B(x_0,\varepsilon)$, tenim que $d(x,x_0)<\varepsilon$ i, per tant, $d((x,0,\ldots,0)),(x_0,0,\ldots,0))=d(x,x_0)<\varepsilon$. Això ens diu que $(x,0)\in B((x_0,0),\varepsilon)\subset V$, que implica que $x\in\Omega$ per construcció de $\Omega$.

D'altra banda, $\varphi$ està ben definida i és de classe $\mathcal{C}^r$. En efecte, donat $u\in\Omega$, $(u,0)\in V$ i, per tant, $\varphi(u)=h(u,0)$ està ben definit. De manera similar, $f^{-1}(u,0)=(u,h(u,0))=(u,\varphi(u))$; és a dir, $\varphi$ és una component de $f^{-1}$, i per tant també és de classe $\mathcal{C}^r$.

En aquest punt, fem una observació que ens serà útil en les demostracions dels passos restants del teorema, així com en els teoremes del rang.

[Aquí les notes intercalen l'Observació 14, que és l'ítem T4.14 i la seva demostració.]

Per acabar la demostració de l'apartat (ii) del teorema de la funció implícita, ho apliquem a $(a,b)\in U$ tal que $\Phi(a,b)=0$. Per l'observació i usant la definició de $\varphi$, obtenim
$$b=h(a,\Phi(a,b))=h(a,0)=\varphi(a).$$

(iii) Hem de veure que $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$.

$\subseteq$ Prenem $(x,y)\in U$ amb $\Phi(x,y)=0$.
Primer de tot, ens assegurem que $x\in\Omega$: en efecte, com que $f(x,y)=(x,\Phi(x,y))=(x,0)\in V$, aleshores $x\in\Omega$ per definició d'$\Omega$, justament.
D'altra banda, per la primera igualtat de l'observació 14 i la definició de $\varphi$,
$$y=h(x,\Phi(x,y))=h(x,0)=\varphi(x);$$
per tant $(x,y)=(x,\varphi(x))\in\{(u,\varphi(u))\mid u\in\Omega\}$.

$\supseteq$ Prenem $(u,\varphi(u))$ amb $u\in\Omega$. Primer de tot, ens assegurem que $(u,\varphi(u))\in U$: en efecte, per definició d'$\Omega$, $(u,0)\in V$, com que $f^{-1}(u,0)=(u,h(u,0))=(u,\varphi(u))$ i $f^{-1}:V\to U$, llavors $(u,\varphi(u))\in U$.
D'altra banda, usant la definició de $\varphi$ i la segona igualtat de l'observació 14,
$$\Phi(u,\varphi(u))=\Phi(u,h(u,0))=0.$$

RESULTATS DELS APUNTS QUE CITA:
[T4.14] Observació 14 (Tema 4) — Igualtats entre h i Φ
Siguin $(x,y)\in U$ i $(u,v)\in V$, amb $x,u\in\mathbb{R}^n$ i $y,v\in\mathbb{R}^m$. Llavors, es compleixen les igualtats
$$y=h(x,\Phi(x,y));\qquad\Phi(u,h(u,v))=v.$$
</apunts>

### Document a revisar

[1] (enunciat) Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$.
[2] (enunciat) Aleshores existeixen dos oberts $U$ i $\Omega$, amb $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G$, i una funció $\varphi:\Omega\to\mathbb{R}^m$ tals que: (i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ per a tot $z\in U$; (ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;
[3] (enunciat) (iii) $\{(x,y)\in G\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.
[4] (demostració) (i) Considerem $f:G\to\mathbb{R}^{n+m}$, $f(x,y)=(x,\Phi(x,y))$. Clarament $f\in\mathcal{C}^r(G)$ i $f(a,b)=(a,0)$. La matriu $Jf$ és triangular inferior per blocs, amb blocs diagonals $\mathrm{Id}_n$ i $\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}$; per tant, $\det Jf(a,b)=\det\big(\partial\Phi_i/\partial y_j(a,b)\big)\neq 0$.
[5] (demostració) Pel teorema de la funció inversa, existeix un obert $U\subseteq G$ amb $(a,b)\in U$ tal que $f|_U$ és injectiva i $\det Jf(z)\neq 0$ per a tot $z\in U$, $V=f(U)$ és obert i $f^{-1}:V\to U$ és de classe $\mathcal{C}^r(V)$. Com que $\det Jf(z)=\det\big(\partial\Phi_i/\partial y_j(z)\big)$, això demostra (i).
[6] (demostració) (ii) Com que $f$ conserva les $n$ primeres coordenades, $f^{-1}$ és de la forma $f^{-1}(u,v)=(u,h(u,v))$ per a $(u,v)\in V$. Definim $\Omega=\{x\in\mathbb{R}^n:(x,0)\in V\}$ i $\varphi:\Omega\to\mathbb{R}^m$, $\varphi(u)=h(u,0)$. Observem que $a\in\Omega$, ja que $(a,0)=f(a,b)\in V$.
[7] (demostració) $\Omega$ és obert: si $x_0\in\Omega$, aleshores $(x_0,0)\in V$, que és obert, i existeix $\varepsilon>0$ amb $B((x_0,0),\varepsilon)\subseteq V$. Si $\|x-x_0\|<\varepsilon$, aleshores $\|(x,0)-(x_0,0)\|=\|x-x_0\|<\varepsilon$, de manera que $(x,0)\in V$, és a dir, $x\in\Omega$.
[8] (demostració) $\varphi$ està ben definida, perquè $(u,0)\in V$ per a tot $u\in\Omega$; i com que $f^{-1}(u,0)=(u,h(u,0))=(u,\varphi(u))$, $\varphi$ és una component de $f^{-1}$, i per tant $\varphi\in\mathcal{C}^r(\Omega)$.
[9] (demostració) Per la bijectivitat de $f:U\to V$, per a $(x,y)\in U$ i $(u,v)\in V$ es té $(x,y)=f^{-1}(f(x,y))=(x,h(x,\Phi(x,y)))$ i $(u,v)=f(f^{-1}(u,v))=(u,\Phi(u,h(u,v)))$; és a dir, $y=h(x,\Phi(x,y))$ i $\Phi(u,h(u,v))=v$. En particular, $b=h(a,\Phi(a,b))=h(a,0)=\varphi(a)$, i queda demostrat (ii).
[10] (demostració) (iii) $\subseteq$: sigui $(x,y)\in U$ amb $\Phi(x,y)=0$. Aleshores $f(x,y)=(x,0)\in V$, és a dir, $x\in\Omega$, i, com que $\Phi(x,y)=0=\Phi(x,\varphi(x))$, la injectivitat de $\Phi$ dona $y=\varphi(x)$.
[11] (demostració) $\supseteq$: sigui $u\in\Omega$. Aleshores $(u,\varphi(u))\in U$, ja que $\Omega\times\mathbb{R}^m\subseteq U$; a més, per la segona igualtat, $\Phi(u,\varphi(u))=\Phi(u,h(u,0))=0$.


## T4.18:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.18] Teorema 18 (Tema 4) — Teorema de redreçament del domini
(de redreçament del domini). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi$ una funció $\mathcal{C}^r(G)$, $\Phi:G\subset\mathbb{R}^{n+m}\to\mathbb{R}^m$, i $(a,b)\in G$ tals que $\mathrm{rang}\big(D\Phi(a,b)\big)=m$. Llavors, existeixen oberts $U,V\subset\mathbb{R}^{n+m}$, amb $(a,b)\in U\subseteq G$, i un $\mathcal{C}^r$-difeomorfisme $g:V\to U$ tals que $\Phi\circ g:V\to U\to\mathbb{R}^k$ és la projecció $\tilde\Phi(u,v)=v$.
Demostració: Seguint la notació habitual del teorema de la funció implícita, suposem que
$$\det\left(\frac{\partial\Phi_j}{\partial y_j}\right)_{i,j=1,\ldots,m}(a,b)\neq 0.$$
Fixem-nos que $\mathrm{rang}\big(D\Phi(a,b)\big)=m$ ens diu que hi ha *algun* menor amb aquesta propietat, però no té perquè ser aquest. Nosaltres farem aquesta suposició i al final de la demostració veurem que, si en realitat són unes altres variables que ho satisfan, aplicant una matriu de permutacions s'aconsegueix igualment el resultat.

A partir d'aquí, apliquem arguments idèntics als de la demostració del teorema de la funció implícita. Construïm la mateixa funció $f(x,y)=(x,\Phi(x,y))$ i, per tant, existeixen $U$ i $V$ oberts, i una correspondència bijectiva entre ells. De fet, el $\mathcal{C}^r$-difeomorfisme $g$ que busquem és precisament $g(u,v)=f^{-1}(u,v)=(u,h(u,v))$, calcant la notació de la demostració del teorema de la funció implícita. Llavors, aplicant la composició i la segona igualtat de l'observació 14, tenim
$$(\Phi\circ g)(u,v)=\Phi(u,h(u,v))=v,$$
tal com volíem demostrar.

Si, en lloc de
$$\det\left(\frac{\partial\Phi_j}{\partial z_j}\right)_{i,j}(a,b)\neq 0,\ \text{ amb }i=1,\ldots,m;\ j=n+1,\ldots,n+m,$$
adoptant la notació $z=(x,y)$, tenim que
$$\det\left(\frac{\partial\Phi_j}{\partial z_{k_j}}\right)_{i,j}(a,b)\neq 0,$$
amb $i=1,\ldots,m$, $k_j\in\{1,\ldots,n+m\}$ per a $j=1,\ldots,m$, amb $k_j\neq k_{j'}$ si $j\neq j'$, aleshores considerem la matriu de permutació $p$ que passa el conjunt $\{k_1,\ldots,k_m\}$ al conjunt al conjunt $\{n+1,\ldots,n+m\}$ (Nota: Per exemple, si $n=2$, $m=3$ i les variable tals que el menor corresponent té rang 3 són $z_1$, $z_2$ i $z_4$, aleshores la matriu diferencial de la permutació $p$ seria
$$Dp=\begin{pmatrix}0&0&1&0&0\\ 0&0&0&1&0\\ 1&0&0&0&0\\ 0&0&0&0&1\\ 0&1&0&0&0\end{pmatrix},$$
de manera que $D\Phi\,Dp$ tindria com a darreres 3 columnes les columnes 1, 2 i 4 de $D\Phi$.), llavors podem aplicar l'anterior demostració a $\Phi\circ p$ i trobem un difeomorfisme $g$ tal que $((\Phi\circ p)\circ g)(u,v)=v$. Per tant, la funció $p\circ g$ és el $\mathcal{C}^r$-difeomorfisme que cerquem per a aconseguir que $(\Phi\circ(p\circ g))(u,v)=v$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$ una funció $\mathcal{C}^r(G)$, i $(a,b)\in G$ tal que $D\Phi(a,b)\neq 0$.
[2] (enunciat) Llavors existeixen oberts $U,V\subseteq\mathbb{R}^{n+m}$, amb $(a,b)\in U\subseteq G$, i un $\mathcal{C}^r$-difeomorfisme $g:V\to U$ tals que $\Phi\circ g:V\to\mathbb{R}^m$ és la projecció $(\Phi\circ g)(u,v)=v$.
[3] (demostració) Suposem primer que $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. La hipòtesi sobre el rang només assegura que hi ha algun menor d'ordre $m$ no nul, no necessàriament el de les variables $y$; el cas general el tractarem al final.
[4] (demostració) Com a la demostració del teorema de la funció implícita, considerem $f(x,y)=(x,\Phi(x,y))$, que és de classe $\mathcal{C}^r(G)$ i compleix $\det Jf(a,b)=\det\big(\partial\Phi_i/\partial y_j(a,b)\big)\neq 0$. Pel teorema de la funció inversa, existeix un obert $U\subseteq G$ amb $(a,b)\in U$ tal que $V=f(U)$ és obert, $f:U\to V$ és bijectiva i $f^{-1}:V\to U$ és de classe $\mathcal{C}^r$.
[5] (demostració) Prenem $g=f^{-1}:V\to U$, que és de la forma $g(u,v)=(u,h(u,v))$. És un $\mathcal{C}^r$-difeomorfisme: és bijectiva, de classe $\mathcal{C}^r$, i la seva inversa $f$ també és de classe $\mathcal{C}^r$.
[6] (demostració) Per la segona igualtat de l'observació 14, $\Phi(u,h(u,v))=v$ per a tot $(u,v)\in V$; per tant, $(\Phi\circ g)(u,v)=\Phi(u,h(u,v))=v$, tal com volíem.
[7] (demostració) En el cas general, escrivint $z=(x,y)$, hi ha índexs diferents $k_1,\ldots,k_m\in\{1,\ldots,n+m\}$ tals que $\det\big(\partial\Phi_i/\partial z_{k_j}(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Sigui $p$ la permutació de coordenades de $\mathbb{R}^{n+m}$ tal que les darreres $m$ columnes de $D(\Phi\circ p)=D\Phi\,Dp$ són les columnes $k_1,\ldots,k_m$ de $D\Phi$.
[8] (demostració) Aplicant el cas anterior a $\Phi\circ p$, definida a l'obert $p^{-1}(G)$, en el punt $p^{-1}(a,b)$, obtenim un $\mathcal{C}^r$-difeomorfisme $g$ amb $((\Phi\circ p)\circ g)(u,v)=v$. Com que $p$ és lineal i invertible, $p\circ g$ és un $\mathcal{C}^r$-difeomorfisme, la seva imatge conté $(a,b)$, i $(\Phi\circ(p\circ g))(u,v)=v$.


## T4.18:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.18] Teorema 18 (Tema 4) — Teorema de redreçament del domini
(de redreçament del domini). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi$ una funció $\mathcal{C}^r(G)$, $\Phi:G\subset\mathbb{R}^{n+m}\to\mathbb{R}^m$, i $(a,b)\in G$ tals que $\mathrm{rang}\big(D\Phi(a,b)\big)=m$. Llavors, existeixen oberts $U,V\subset\mathbb{R}^{n+m}$, amb $(a,b)\in U\subseteq G$, i un $\mathcal{C}^r$-difeomorfisme $g:V\to U$ tals que $\Phi\circ g:V\to U\to\mathbb{R}^k$ és la projecció $\tilde\Phi(u,v)=v$.
Demostració: Seguint la notació habitual del teorema de la funció implícita, suposem que
$$\det\left(\frac{\partial\Phi_j}{\partial y_j}\right)_{i,j=1,\ldots,m}(a,b)\neq 0.$$
Fixem-nos que $\mathrm{rang}\big(D\Phi(a,b)\big)=m$ ens diu que hi ha *algun* menor amb aquesta propietat, però no té perquè ser aquest. Nosaltres farem aquesta suposició i al final de la demostració veurem que, si en realitat són unes altres variables que ho satisfan, aplicant una matriu de permutacions s'aconsegueix igualment el resultat.

A partir d'aquí, apliquem arguments idèntics als de la demostració del teorema de la funció implícita. Construïm la mateixa funció $f(x,y)=(x,\Phi(x,y))$ i, per tant, existeixen $U$ i $V$ oberts, i una correspondència bijectiva entre ells. De fet, el $\mathcal{C}^r$-difeomorfisme $g$ que busquem és precisament $g(u,v)=f^{-1}(u,v)=(u,h(u,v))$, calcant la notació de la demostració del teorema de la funció implícita. Llavors, aplicant la composició i la segona igualtat de l'observació 14, tenim
$$(\Phi\circ g)(u,v)=\Phi(u,h(u,v))=v,$$
tal com volíem demostrar.

Si, en lloc de
$$\det\left(\frac{\partial\Phi_j}{\partial z_j}\right)_{i,j}(a,b)\neq 0,\ \text{ amb }i=1,\ldots,m;\ j=n+1,\ldots,n+m,$$
adoptant la notació $z=(x,y)$, tenim que
$$\det\left(\frac{\partial\Phi_j}{\partial z_{k_j}}\right)_{i,j}(a,b)\neq 0,$$
amb $i=1,\ldots,m$, $k_j\in\{1,\ldots,n+m\}$ per a $j=1,\ldots,m$, amb $k_j\neq k_{j'}$ si $j\neq j'$, aleshores considerem la matriu de permutació $p$ que passa el conjunt $\{k_1,\ldots,k_m\}$ al conjunt al conjunt $\{n+1,\ldots,n+m\}$ (Nota: Per exemple, si $n=2$, $m=3$ i les variable tals que el menor corresponent té rang 3 són $z_1$, $z_2$ i $z_4$, aleshores la matriu diferencial de la permutació $p$ seria
$$Dp=\begin{pmatrix}0&0&1&0&0\\ 0&0&0&1&0\\ 1&0&0&0&0\\ 0&0&0&0&1\\ 0&1&0&0&0\end{pmatrix},$$
de manera que $D\Phi\,Dp$ tindria com a darreres 3 columnes les columnes 1, 2 i 4 de $D\Phi$.), llavors podem aplicar l'anterior demostració a $\Phi\circ p$ i trobem un difeomorfisme $g$ tal que $((\Phi\circ p)\circ g)(u,v)=v$. Per tant, la funció $p\circ g$ és el $\mathcal{C}^r$-difeomorfisme que cerquem per a aconseguir que $(\Phi\circ(p\circ g))(u,v)=v$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$ una funció $\mathcal{C}^r(G)$, i $(a,b)\in G$ tal que $\mathrm{rang}\big(D\Phi(a,b)\big)=m$.
[2] (enunciat) Llavors existeixen oberts $U,V\subseteq\mathbb{R}^{n+m}$, amb $(a,b)\in U\subseteq G$, i un $\mathcal{C}^r$-difeomorfisme lineal $g:V\to U$ tals que $\Phi\circ g:V\to\mathbb{R}^m$ és la projecció $(\Phi\circ g)(u,v)=v$.
[3] (demostració) Suposem primer que $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. La hipòtesi sobre el rang només assegura que hi ha algun menor d'ordre $m$ no nul, no necessàriament el de les variables $y$; el cas general el tractarem al final.
[4] (demostració) Com a la demostració del teorema de la funció implícita, considerem $f(x,y)=(x,\Phi(x,y))$, que és de classe $\mathcal{C}^r(G)$ i compleix $\det Jf(a,b)=\det\big(\partial\Phi_i/\partial y_j(a,b)\big)\neq 0$. Pel teorema de la funció inversa, existeix un obert $U\subseteq G$ amb $(a,b)\in U$ tal que $V=f(U)$ és obert, $f:U\to V$ és bijectiva i $f^{-1}:V\to U$ és de classe $\mathcal{C}^r$.
[5] (demostració) Prenem $g=f^{-1}:V\to U$, que és de la forma $g(u,v)=(u,h(u,v))$. És un $\mathcal{C}^r$-difeomorfisme: és bijectiva, de classe $\mathcal{C}^r$, i la seva inversa $f$ també és de classe $\mathcal{C}^r$.
[6] (demostració) Per la segona igualtat de l'observació 14, $\Phi(u,h(u,v))=v$ per a tot $(u,v)\in V$; per tant, $(\Phi\circ g)(u,v)=\Phi(u,h(u,v))=v$, tal com volíem.
[7] (demostració) En el cas general, escrivint $z=(x,y)$, hi ha índexs diferents $k_1,\ldots,k_m\in\{1,\ldots,n+m\}$ tals que $\det\big(\partial\Phi_i/\partial z_{k_j}(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Sigui $p$ la permutació de coordenades de $\mathbb{R}^{n+m}$ tal que les darreres $m$ columnes de $D(\Phi\circ p)=D\Phi\,Dp$ són les columnes $k_1,\ldots,k_m$ de $D\Phi$.
[8] (demostració) Aplicant el cas anterior a $\Phi\circ p$, definida a l'obert $p^{-1}(G)$, en el punt $p^{-1}(a,b)$, obtenim un $\mathcal{C}^r$-difeomorfisme $g$ amb $((\Phi\circ p)\circ g)(u,v)=v$. Com que $p$ és lineal i invertible, $g\circ p$ és un $\mathcal{C}^r$-difeomorfisme, la seva imatge conté $(a,b)$, i $(\Phi\circ(g\circ p))(u,v)=v$.


## T4.18:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.18] Teorema 18 (Tema 4) — Teorema de redreçament del domini
(de redreçament del domini). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi$ una funció $\mathcal{C}^r(G)$, $\Phi:G\subset\mathbb{R}^{n+m}\to\mathbb{R}^m$, i $(a,b)\in G$ tals que $\mathrm{rang}\big(D\Phi(a,b)\big)=m$. Llavors, existeixen oberts $U,V\subset\mathbb{R}^{n+m}$, amb $(a,b)\in U\subseteq G$, i un $\mathcal{C}^r$-difeomorfisme $g:V\to U$ tals que $\Phi\circ g:V\to U\to\mathbb{R}^k$ és la projecció $\tilde\Phi(u,v)=v$.
Demostració: Seguint la notació habitual del teorema de la funció implícita, suposem que
$$\det\left(\frac{\partial\Phi_j}{\partial y_j}\right)_{i,j=1,\ldots,m}(a,b)\neq 0.$$
Fixem-nos que $\mathrm{rang}\big(D\Phi(a,b)\big)=m$ ens diu que hi ha *algun* menor amb aquesta propietat, però no té perquè ser aquest. Nosaltres farem aquesta suposició i al final de la demostració veurem que, si en realitat són unes altres variables que ho satisfan, aplicant una matriu de permutacions s'aconsegueix igualment el resultat.

A partir d'aquí, apliquem arguments idèntics als de la demostració del teorema de la funció implícita. Construïm la mateixa funció $f(x,y)=(x,\Phi(x,y))$ i, per tant, existeixen $U$ i $V$ oberts, i una correspondència bijectiva entre ells. De fet, el $\mathcal{C}^r$-difeomorfisme $g$ que busquem és precisament $g(u,v)=f^{-1}(u,v)=(u,h(u,v))$, calcant la notació de la demostració del teorema de la funció implícita. Llavors, aplicant la composició i la segona igualtat de l'observació 14, tenim
$$(\Phi\circ g)(u,v)=\Phi(u,h(u,v))=v,$$
tal com volíem demostrar.

Si, en lloc de
$$\det\left(\frac{\partial\Phi_j}{\partial z_j}\right)_{i,j}(a,b)\neq 0,\ \text{ amb }i=1,\ldots,m;\ j=n+1,\ldots,n+m,$$
adoptant la notació $z=(x,y)$, tenim que
$$\det\left(\frac{\partial\Phi_j}{\partial z_{k_j}}\right)_{i,j}(a,b)\neq 0,$$
amb $i=1,\ldots,m$, $k_j\in\{1,\ldots,n+m\}$ per a $j=1,\ldots,m$, amb $k_j\neq k_{j'}$ si $j\neq j'$, aleshores considerem la matriu de permutació $p$ que passa el conjunt $\{k_1,\ldots,k_m\}$ al conjunt al conjunt $\{n+1,\ldots,n+m\}$ (Nota: Per exemple, si $n=2$, $m=3$ i les variable tals que el menor corresponent té rang 3 són $z_1$, $z_2$ i $z_4$, aleshores la matriu diferencial de la permutació $p$ seria
$$Dp=\begin{pmatrix}0&0&1&0&0\\ 0&0&0&1&0\\ 1&0&0&0&0\\ 0&0&0&0&1\\ 0&1&0&0&0\end{pmatrix},$$
de manera que $D\Phi\,Dp$ tindria com a darreres 3 columnes les columnes 1, 2 i 4 de $D\Phi$.), llavors podem aplicar l'anterior demostració a $\Phi\circ p$ i trobem un difeomorfisme $g$ tal que $((\Phi\circ p)\circ g)(u,v)=v$. Per tant, la funció $p\circ g$ és el $\mathcal{C}^r$-difeomorfisme que cerquem per a aconseguir que $(\Phi\circ(p\circ g))(u,v)=v$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$ una funció $\mathcal{C}^r(G)$, i $(a,b)\in G$ tal que $\mathrm{rang}\big(D\Phi(a,b)\big)=m$.
[2] (enunciat) Llavors, per a tot obert $U$ amb $(a,b)\in U\subseteq G$, existeixen un obert $V\subseteq\mathbb{R}^{n+m}$ i un $\mathcal{C}^r$-difeomorfisme $g:V\to U$ tals que $\Phi\circ g:V\to\mathbb{R}^m$ és la projecció $(\Phi\circ g)(u,v)=v$.
[3] (demostració) Suposem primer que $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. La hipòtesi sobre el rang només assegura que hi ha algun menor d'ordre $m$ no nul, no necessàriament el de les variables $y$; el cas general el tractarem al final.
[4] (demostració) Com a la demostració del teorema de la funció implícita, considerem $f(x,y)=(x,\Phi(x,y))$, que és de classe $\mathcal{C}^r(G)$ i compleix $\det Jf(a,b)=\det\big(\partial\Phi_i/\partial y_j(a,b)\big)\neq 0$. Pel teorema de la funció inversa, existeix un obert $U\subseteq G$ amb $(a,b)\in U$ tal que $V=f(U)$ és obert, $f:U\to V$ és bijectiva i $f^{-1}:V\to U$ és de classe $\mathcal{C}^r$.
[5] (demostració) Prenem $g=f^{-1}:V\to U$, que és de la forma $g(u,v)=(u,h(u,v))$. És un $\mathcal{C}^r$-difeomorfisme perquè és bijectiva i de classe $\mathcal{C}^r$, i tota bijecció de classe $\mathcal{C}^r$ entre oberts és un $\mathcal{C}^r$-difeomorfisme.
[6] (demostració) Per la segona igualtat de l'observació 14, $\Phi(u,h(u,v))=v$ per a tot $(u,v)\in V$; per tant, $(\Phi\circ g)(u,v)=\Phi(u,h(u,v))=v$, tal com volíem.
[7] (demostració) En el cas general, escrivint $z=(x,y)$, hi ha índexs diferents $k_1,\ldots,k_m\in\{1,\ldots,n+m\}$ tals que $\det\big(\partial\Phi_i/\partial z_{k_j}(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Sigui $p$ la permutació de coordenades de $\mathbb{R}^{n+m}$ tal que les darreres $m$ columnes de $D(\Phi\circ p)=Dp\,D\Phi$ són les columnes $k_1,\ldots,k_m$ de $D\Phi$.
[8] (demostració) Aplicant el cas anterior a $\Phi\circ p$, definida a l'obert $p^{-1}(G)$, en el punt $p^{-1}(a,b)$, obtenim un $\mathcal{C}^r$-difeomorfisme $g$ amb $((\Phi\circ p)\circ g)(u,v)=v$. Com que $p$ és lineal i invertible, $p\circ g$ és un $\mathcal{C}^r$-difeomorfisme, la seva imatge conté $(a,b)$, i $(\Phi\circ(p\circ g))(u,v)=v$.


## T4.20:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.20] Teorema 20 (Tema 4) — Teorema de redreçament de la imatge
(de redreçament de la imatge). Sigui $G\subset\mathbb{R}^m$ obert, $\Phi:G\subset\mathbb{R}^m\to\mathbb{R}^{n+m}$ una funció $\mathcal{C}^r(G)$, i $b\in G$ tal que $\mathrm{rang}\big(D\Phi(b)\big)=m$. Llavors, existeixen oberts $U,V\subset\mathbb{R}^{n+m}$, amb $\Phi(b)\in V$, un $\mathcal{C}^r$-difeomorfisme $h:V\to U$, i un obert $U'\subset G\subseteq\mathbb{R}^m$ amb $b\in U'$, tals que $h\circ\Phi:U'\to V\to\mathbb{R}^{n+m}$ és $y\mapsto(0,y)$.
Demostració: Dividim la funció $\Phi$ en dues components $\Phi_1$ i $\Phi_2$, $\Phi_1:G\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^n$ i $\Phi_2:G\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^m$, de manera que
$$\begin{array}{rcl}\Phi\quad G\subseteq\mathbb{R}^m&\longrightarrow&\mathbb{R}^n\times\mathbb{R}^m=\mathbb{R}^{n+m}\\ y&\longmapsto&(\Phi_1(y),\Phi_2(y))\,.\end{array}$$
Com en el teorema 20, suposem que
$$\det\left(\frac{\partial\Phi_2}{\partial y}\right)(b)\neq 0,$$
i ja aplicarem una permutació al final si aquesta condició es compleix per a un altre subconjunt de $m$ variables en lloc de $(y_1,\ldots,y_m)$.

Considerem ara la funció
$$\begin{array}{rcl}f\quad\mathbb{R}^n\times G\subseteq\mathbb{R}^{n+m}&\longrightarrow&\mathbb{R}^{n+m}\\ (x,y)&\longmapsto&(x+\Phi_1(y),\Phi_2(y))\,.\end{array}$$
En particular, $f(0,b)=\Phi(b)$.
Clarament, $f\in\mathcal{C}^r(\mathbb{R}^n\times G)$ perquè és la suma de la identitat en $\mathbb{R}^n$ amb $\Phi\in\mathcal{C}^r(G)$, i es pot veure que
$$\det Df(0,b)=\det\left(\frac{\partial\Phi_2}{\partial y}\right)(b)\neq 0,$$
de manera anàloga al pas (i) de la demostració del teorema de la funció implícita. Per tant, continuant amb l'analogia, podem aplicar el teorema de la funció inversa a $f$: existeixen uns oberts $U,V\subseteq\mathbb{R}^n\times G$ tals que $f:U\to V$ és bijectiva i la inversa $f^{-1}=V\to U$ és bijectiva i de classe $\mathcal{C}^r$. Com en el cas del teorema de redreçament del domini, $f^{-1}$ serà el $\mathcal{C}^r$-difeomorfisme que cerquem, és a dir, definim
$$h=f^{-1}.$$
Prenem ara
$$U'=\{y\in\mathbb{R}^m\mid(0,y)\in U\}.$$
Com que $U\subseteq\mathbb{R}^n\times G$, és evident que $U\subseteq G$. Amàlogament a la demostració de l'apartat (ii) del teorema de la funció implícita, podem veure que $U'$ és obert.

Considerem ara $(h\circ\Phi)(y)$, amb $y\in U'$. Volem veure que està ben definit per a tot $y\in U'$ i, d'altra banda, que compleix la conclusió del teorema, és a dir, que $(h\circ\Phi)(y)=(0,y)$.

- Si $y\in U'$, aleshores per definició $(0,y)\in U$ i $f(0,y)\in V$ està ben definit. Ara bé, per definició de $f$, $f(0,y)=(\Phi_1(y),\Phi_2(y))=\Phi(y)\in V$ i podem composar doncs, amb $h$.
- D'altra banda, per definició de $h=f^{-1}$ i tornant a fer servir la definició de $f$, obtenim
$$(0,y)=f^{-1}(f(0,y))=h(\Phi(y)).$$

Com en el teorema del redreçament, si la condició del rang la complissin altres variables, podríem considerar una permutació $p$ de manera que $p\circ h\circ\Phi(y)=(0,y)$ i, per tant, $p\circ h$ seria el $\mathcal{C}^r$-difeomorfisme que buscàvem.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $G\subseteq\mathbb{R}^m$ obert, $\Phi:G\to\mathbb{R}^{n+m}$ una funció $\mathcal{C}^r(G)$, i $b\in G$ tal que $\mathrm{rang}\big(D\Phi(b)\big)=m$.
[2] (enunciat) Llavors existeixen oberts $U,V\subseteq\mathbb{R}^{n+m}$, amb $\Phi(b)\in V$, un $\mathcal{C}^r$-difeomorfisme $h:V\to U$ i un obert $U'\subseteq G$ amb $b\in U'$, tals que $(h\circ\Phi)(y)=(0,y)$ per a tot $y\in G$.
[3] (demostració) Escrivim $\Phi=(\Phi_1,\Phi_2)$, amb $\Phi_1:G\to\mathbb{R}^n$ i $\Phi_2:G\to\mathbb{R}^m$. Suposem que $\det\big(\partial\Phi_2/\partial y\big)(b)\neq 0$; si el menor d'ordre $m$ no nul de $D\Phi(b)$ correspon a unes altres $m$ components de $\Phi$, aplicarem una permutació al final.
[4] (demostració) Considerem $f:\mathbb{R}^n\times G\to\mathbb{R}^{n+m}$, $f(x,y)=(x+\Phi_1(y),\Phi_2(y))$, que és de classe $\mathcal{C}^r$ i compleix $f(0,b)=\Phi(b)$. La seva jacobiana és $\begin{pmatrix}\mathrm{Id}_n&D\Phi_1(y)\\ 0&D\Phi_2(y)\end{pmatrix}$, i per tant $\det Df(0,b)=\det\big(\partial\Phi_2/\partial y\big)(b)\neq 0$.
[5] (demostració) Pel teorema de la funció inversa, existeixen oberts $U\subseteq\mathbb{R}^n\times G$, amb $(0,b)\in U$, i $V=f(U)\subseteq\mathbb{R}^{n+m}$, amb $\Phi(b)=f(0,b)\in V$, tals que $f:U\to V$ és bijectiva i la seva inversa és de classe $\mathcal{C}^r$. Definim $h=f^{-1}:V\to U$, que és un $\mathcal{C}^r$-difeomorfisme.
[6] (demostració) Prenem $U'=\{y\in\mathbb{R}^m\mid(0,y)\in U\}$. Com que $U\subseteq\mathbb{R}^n\times G$, tenim $U'\subseteq G$, i $b\in U'$ perquè $(0,b)\in U$. Com a l'apartat (ii) del teorema de la funció implícita, $U'$ és obert.
[7] (demostració) Si $y\in U'$, aleshores $(0,y)\in U$ i, per definició de $f$, $f(0,y)=(\Phi_1(y),\Phi_2(y))=\Phi(y)\in V$; per tant, $h\circ\Phi$ està ben definida en $U'$.
[8] (demostració) A més, per a tot $y\in U'$, $(h\circ\Phi)(y)=f^{-1}(f(0,y))=(0,y)$.
[9] (demostració) Si el menor no nul correspon a unes altres components, prenem una permutació $p$ de les coordenades de $\mathbb{R}^{n+m}$ tal que $p\circ\Phi$ compleix la suposició anterior; obtenim un $\mathcal{C}^r$-difeomorfisme $h$ amb $(h\circ p\circ\Phi)(y)=(0,y)$, i aleshores $h\circ p$ és el $\mathcal{C}^r$-difeomorfisme buscat.


## T4.20:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.20] Teorema 20 (Tema 4) — Teorema de redreçament de la imatge
(de redreçament de la imatge). Sigui $G\subset\mathbb{R}^m$ obert, $\Phi:G\subset\mathbb{R}^m\to\mathbb{R}^{n+m}$ una funció $\mathcal{C}^r(G)$, i $b\in G$ tal que $\mathrm{rang}\big(D\Phi(b)\big)=m$. Llavors, existeixen oberts $U,V\subset\mathbb{R}^{n+m}$, amb $\Phi(b)\in V$, un $\mathcal{C}^r$-difeomorfisme $h:V\to U$, i un obert $U'\subset G\subseteq\mathbb{R}^m$ amb $b\in U'$, tals que $h\circ\Phi:U'\to V\to\mathbb{R}^{n+m}$ és $y\mapsto(0,y)$.
Demostració: Dividim la funció $\Phi$ en dues components $\Phi_1$ i $\Phi_2$, $\Phi_1:G\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^n$ i $\Phi_2:G\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^m$, de manera que
$$\begin{array}{rcl}\Phi\quad G\subseteq\mathbb{R}^m&\longrightarrow&\mathbb{R}^n\times\mathbb{R}^m=\mathbb{R}^{n+m}\\ y&\longmapsto&(\Phi_1(y),\Phi_2(y))\,.\end{array}$$
Com en el teorema 20, suposem que
$$\det\left(\frac{\partial\Phi_2}{\partial y}\right)(b)\neq 0,$$
i ja aplicarem una permutació al final si aquesta condició es compleix per a un altre subconjunt de $m$ variables en lloc de $(y_1,\ldots,y_m)$.

Considerem ara la funció
$$\begin{array}{rcl}f\quad\mathbb{R}^n\times G\subseteq\mathbb{R}^{n+m}&\longrightarrow&\mathbb{R}^{n+m}\\ (x,y)&\longmapsto&(x+\Phi_1(y),\Phi_2(y))\,.\end{array}$$
En particular, $f(0,b)=\Phi(b)$.
Clarament, $f\in\mathcal{C}^r(\mathbb{R}^n\times G)$ perquè és la suma de la identitat en $\mathbb{R}^n$ amb $\Phi\in\mathcal{C}^r(G)$, i es pot veure que
$$\det Df(0,b)=\det\left(\frac{\partial\Phi_2}{\partial y}\right)(b)\neq 0,$$
de manera anàloga al pas (i) de la demostració del teorema de la funció implícita. Per tant, continuant amb l'analogia, podem aplicar el teorema de la funció inversa a $f$: existeixen uns oberts $U,V\subseteq\mathbb{R}^n\times G$ tals que $f:U\to V$ és bijectiva i la inversa $f^{-1}=V\to U$ és bijectiva i de classe $\mathcal{C}^r$. Com en el cas del teorema de redreçament del domini, $f^{-1}$ serà el $\mathcal{C}^r$-difeomorfisme que cerquem, és a dir, definim
$$h=f^{-1}.$$
Prenem ara
$$U'=\{y\in\mathbb{R}^m\mid(0,y)\in U\}.$$
Com que $U\subseteq\mathbb{R}^n\times G$, és evident que $U\subseteq G$. Amàlogament a la demostració de l'apartat (ii) del teorema de la funció implícita, podem veure que $U'$ és obert.

Considerem ara $(h\circ\Phi)(y)$, amb $y\in U'$. Volem veure que està ben definit per a tot $y\in U'$ i, d'altra banda, que compleix la conclusió del teorema, és a dir, que $(h\circ\Phi)(y)=(0,y)$.

- Si $y\in U'$, aleshores per definició $(0,y)\in U$ i $f(0,y)\in V$ està ben definit. Ara bé, per definició de $f$, $f(0,y)=(\Phi_1(y),\Phi_2(y))=\Phi(y)\in V$ i podem composar doncs, amb $h$.
- D'altra banda, per definició de $h=f^{-1}$ i tornant a fer servir la definició de $f$, obtenim
$$(0,y)=f^{-1}(f(0,y))=h(\Phi(y)).$$

Com en el teorema del redreçament, si la condició del rang la complissin altres variables, podríem considerar una permutació $p$ de manera que $p\circ h\circ\Phi(y)=(0,y)$ i, per tant, $p\circ h$ seria el $\mathcal{C}^r$-difeomorfisme que buscàvem.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $G\subseteq\mathbb{R}^m$ obert, $\Phi:G\to\mathbb{R}^{n+m}$ una funció $\mathcal{C}^r(G)$, i $b\in G$ tal que $\mathrm{rang}\big(D\Phi(b)\big)=m$.
[2] (enunciat) Llavors existeixen oberts $U,V\subseteq\mathbb{R}^{n+m}$, amb $\Phi(b)\in V$, un $\mathcal{C}^r$-difeomorfisme $h:V\to U$ i un obert $U'\subseteq G$ amb $b\in U'$ i $\Phi(U')=V$, tals que $(h\circ\Phi)(y)=(0,y)$ per a tot $y\in U'$.
[3] (demostració) Escrivim $\Phi=(\Phi_1,\Phi_2)$, amb $\Phi_1:G\to\mathbb{R}^n$ i $\Phi_2:G\to\mathbb{R}^m$. Suposem que $\det\big(\partial\Phi_2/\partial y\big)(b)\neq 0$; si el menor d'ordre $m$ no nul de $D\Phi(b)$ correspon a unes altres $m$ components de $\Phi$, aplicarem una permutació al final.
[4] (demostració) Considerem $f:\mathbb{R}^n\times G\to\mathbb{R}^{n+m}$, $f(x,y)=(x+\Phi_1(y),\Phi_2(y))$, que és de classe $\mathcal{C}^r$ i compleix $f(0,b)=\Phi(b)$. La seva jacobiana és $\begin{pmatrix}\mathrm{Id}_n&D\Phi_1(y)\\ 0&D\Phi_2(y)\end{pmatrix}$, i per tant $\det Df(0,b)=\det\big(\partial\Phi_2/\partial y\big)(b)\neq 0$.
[5] (demostració) Pel teorema de la funció inversa, existeixen oberts $U\subseteq\mathbb{R}^n\times G$, amb $(0,b)\in U$, i $V=f(U)\subseteq\mathbb{R}^{n+m}$, amb $\Phi(b)=f(0,b)\in V$, tals que $f:U\to V$ és bijectiva i la seva inversa és de classe $\mathcal{C}^r$. Definim $h=f^{-1}:V\to U$, que és un $\mathcal{C}^r$-difeomorfisme.
[6] (demostració) Prenem $U'=\{y\in\mathbb{R}^m\mid(0,y)\in U\}$. Com que $U\subseteq\mathbb{R}^n\times G$, tenim $U'\subseteq G$, i $b\in U'$ perquè $(0,b)\in U$. Com a l'apartat (ii) del teorema de la funció implícita, $U'$ és obert.
[7] (demostració) Si $y\in U'$, aleshores $(0,y)\in U$ i, per definició de $f$, $f(0,y)=(\Phi_1(y),\Phi_2(y))=\Phi(y)\in V$; per tant, $h\circ\Phi$ està ben definida en $U'$.
[8] (demostració) A més, per a tot $y\in U'$, com que $\Phi(y)=f^{-1}(0,y)$, tenim $(h\circ\Phi)(y)=h(f^{-1}(0,y))=(0,y)$.
[9] (demostració) Si el menor no nul correspon a unes altres components, prenem una permutació $p$ de les coordenades de $\mathbb{R}^{n+m}$ tal que $p\circ\Phi$ compleix la suposició anterior; obtenim un $\mathcal{C}^r$-difeomorfisme $h$ amb $(h\circ p\circ\Phi)(y)=(0,y)$, i aleshores $h\circ p$ és el $\mathcal{C}^r$-difeomorfisme buscat.


## T4.20:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T4.20] Teorema 20 (Tema 4) — Teorema de redreçament de la imatge
(de redreçament de la imatge). Sigui $G\subset\mathbb{R}^m$ obert, $\Phi:G\subset\mathbb{R}^m\to\mathbb{R}^{n+m}$ una funció $\mathcal{C}^r(G)$, i $b\in G$ tal que $\mathrm{rang}\big(D\Phi(b)\big)=m$. Llavors, existeixen oberts $U,V\subset\mathbb{R}^{n+m}$, amb $\Phi(b)\in V$, un $\mathcal{C}^r$-difeomorfisme $h:V\to U$, i un obert $U'\subset G\subseteq\mathbb{R}^m$ amb $b\in U'$, tals que $h\circ\Phi:U'\to V\to\mathbb{R}^{n+m}$ és $y\mapsto(0,y)$.
Demostració: Dividim la funció $\Phi$ en dues components $\Phi_1$ i $\Phi_2$, $\Phi_1:G\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^n$ i $\Phi_2:G\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^m$, de manera que
$$\begin{array}{rcl}\Phi\quad G\subseteq\mathbb{R}^m&\longrightarrow&\mathbb{R}^n\times\mathbb{R}^m=\mathbb{R}^{n+m}\\ y&\longmapsto&(\Phi_1(y),\Phi_2(y))\,.\end{array}$$
Com en el teorema 20, suposem que
$$\det\left(\frac{\partial\Phi_2}{\partial y}\right)(b)\neq 0,$$
i ja aplicarem una permutació al final si aquesta condició es compleix per a un altre subconjunt de $m$ variables en lloc de $(y_1,\ldots,y_m)$.

Considerem ara la funció
$$\begin{array}{rcl}f\quad\mathbb{R}^n\times G\subseteq\mathbb{R}^{n+m}&\longrightarrow&\mathbb{R}^{n+m}\\ (x,y)&\longmapsto&(x+\Phi_1(y),\Phi_2(y))\,.\end{array}$$
En particular, $f(0,b)=\Phi(b)$.
Clarament, $f\in\mathcal{C}^r(\mathbb{R}^n\times G)$ perquè és la suma de la identitat en $\mathbb{R}^n$ amb $\Phi\in\mathcal{C}^r(G)$, i es pot veure que
$$\det Df(0,b)=\det\left(\frac{\partial\Phi_2}{\partial y}\right)(b)\neq 0,$$
de manera anàloga al pas (i) de la demostració del teorema de la funció implícita. Per tant, continuant amb l'analogia, podem aplicar el teorema de la funció inversa a $f$: existeixen uns oberts $U,V\subseteq\mathbb{R}^n\times G$ tals que $f:U\to V$ és bijectiva i la inversa $f^{-1}=V\to U$ és bijectiva i de classe $\mathcal{C}^r$. Com en el cas del teorema de redreçament del domini, $f^{-1}$ serà el $\mathcal{C}^r$-difeomorfisme que cerquem, és a dir, definim
$$h=f^{-1}.$$
Prenem ara
$$U'=\{y\in\mathbb{R}^m\mid(0,y)\in U\}.$$
Com que $U\subseteq\mathbb{R}^n\times G$, és evident que $U\subseteq G$. Amàlogament a la demostració de l'apartat (ii) del teorema de la funció implícita, podem veure que $U'$ és obert.

Considerem ara $(h\circ\Phi)(y)$, amb $y\in U'$. Volem veure que està ben definit per a tot $y\in U'$ i, d'altra banda, que compleix la conclusió del teorema, és a dir, que $(h\circ\Phi)(y)=(0,y)$.

- Si $y\in U'$, aleshores per definició $(0,y)\in U$ i $f(0,y)\in V$ està ben definit. Ara bé, per definició de $f$, $f(0,y)=(\Phi_1(y),\Phi_2(y))=\Phi(y)\in V$ i podem composar doncs, amb $h$.
- D'altra banda, per definició de $h=f^{-1}$ i tornant a fer servir la definició de $f$, obtenim
$$(0,y)=f^{-1}(f(0,y))=h(\Phi(y)).$$

Com en el teorema del redreçament, si la condició del rang la complissin altres variables, podríem considerar una permutació $p$ de manera que $p\circ h\circ\Phi(y)=(0,y)$ i, per tant, $p\circ h$ seria el $\mathcal{C}^r$-difeomorfisme que buscàvem.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $G\subseteq\mathbb{R}^m$ obert, $\Phi:G\to\mathbb{R}^{n+m}$ una funció $\mathcal{C}^r(G)$, i $b\in G$ tal que $\mathrm{rang}\big(D\Phi(b)\big)=m$.
[2] (enunciat) Llavors existeixen oberts $U,V\subseteq\mathbb{R}^{n+m}$, amb $\Phi(b)\in V$, un $\mathcal{C}^{r+1}$-difeomorfisme $h:V\to U$ i un obert $U'\subseteq G$ amb $b\in U'$, tals que $(h\circ\Phi)(y)=(0,y)$ per a tot $y\in U'$.
[3] (demostració) Escrivim $\Phi=(\Phi_1,\Phi_2)$, amb $\Phi_1:G\to\mathbb{R}^n$ i $\Phi_2:G\to\mathbb{R}^m$. Suposem que $\det\big(\partial\Phi_2/\partial y\big)(b)\neq 0$; si el menor d'ordre $m$ no nul de $D\Phi(b)$ correspon a unes altres $m$ components de $\Phi$, aplicarem una permutació al final.
[4] (demostració) Considerem $f:\mathbb{R}^n\times G\to\mathbb{R}^{n+m}$, $f(x,y)=(x+\Phi_1(y),\Phi_2(y))$, que és de classe $\mathcal{C}^r$ i compleix $f(0,b)=\Phi(b)$. La seva jacobiana és $\begin{pmatrix}\mathrm{Id}_n&0\\ D\Phi_1(y)&D\Phi_2(y)\end{pmatrix}$, i per tant $\det Df(0,b)=\det\big(\partial\Phi_2/\partial y\big)(b)\neq 0$.
[5] (demostració) Pel teorema de la funció inversa, existeixen oberts $U\subseteq\mathbb{R}^n\times G$, amb $(0,b)\in U$, i $V=f(U)\subseteq\mathbb{R}^{n+m}$, amb $\Phi(b)=f(0,b)\in V$, tals que $f:U\to V$ és bijectiva i la seva inversa és de classe $\mathcal{C}^r$. Definim $h=f^{-1}:V\to U$, que és un $\mathcal{C}^r$-difeomorfisme.
[6] (demostració) Prenem $U'=\{y\in\mathbb{R}^m\mid(0,y)\in U\}$. Com que $U\subseteq\mathbb{R}^n\times G$, tenim $U'\subseteq G$, i $b\in U'$ perquè $(0,b)\in U$. A més, $U'$ és obert perquè és la projecció de l'obert $U$ sobre les darreres $m$ coordenades.
[7] (demostració) Si $y\in U'$, aleshores $(0,y)\in U$ i, per definició de $f$, $f(0,y)=(\Phi_1(y),\Phi_2(y))=\Phi(y)\in V$; per tant, $h\circ\Phi$ està ben definida en $U'$.
[8] (demostració) A més, per a tot $y\in U'$, $(h\circ\Phi)(y)=f^{-1}(f(0,y))=(0,y)$.
[9] (demostració) Si el menor no nul correspon a unes altres components, prenem una permutació $p$ de les coordenades de $\mathbb{R}^{n+m}$ tal que $p\circ\Phi$ compleix la suposició anterior; obtenim un $\mathcal{C}^r$-difeomorfisme $h$ amb $(h\circ p\circ\Phi)(y)=(0,y)$, i aleshores $h\circ p$ és el $\mathcal{C}^r$-difeomorfisme buscat.

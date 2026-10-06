## T5.13:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.13] Lema 13 (Tema 5) — Límit d'un polinomi i grau dels monomis
Sigui $P(\mathbf{x})\neq0$ un polinomi, $\mathbf{x}=(x_1,\ldots,x_n)$. Llavors, $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}\dfrac{P(\mathbf{x})}{\|\mathbf{x}\|^r}=0$ si, i només si, tots els monomis de $P$ són de grau $\geqslant r+1$.
Demostració: $\Longleftarrow$ Suposem que $P(\mathbf{x})=\sum_{|\alpha|\geq r+1}a_\alpha\,\mathbf{x}^\alpha$. Aleshores, per a cada $\alpha$, existeix $\beta=\beta(\alpha)$ tal que $|\beta|\geq0$ i
$$\mathbf{x}^\alpha=x_{i_1}\ldots x_{i_{r+1}}\,\mathbf{x}^\beta,$$
atès que $\alpha$ té almenys $r+1$ factors.

Llavors,
$$\begin{aligned}
\left|\frac{P(\mathbf{x})}{\|\mathbf{x}\|^r}\right| &= \left|\sum_{|\alpha|\geq r+1}a_\alpha\,\frac{x_{i_1}\ldots x_{i_{r+1}}\,\mathbf{x}^\beta}{\|\mathbf{x}\|^r}\right|\\
&\leq\sum_{|\alpha|\geq r+1}|a_\alpha|\,\frac{|x_{i_1}|}{\|\mathbf{x}\|}\ldots\frac{|x_{i_r}|}{\|\mathbf{x}\|}\,|x_{i_{r+1}}|\,|\mathbf{x}^\beta|.
\end{aligned}$$
Com que $|a_\alpha|$ és una constant per a cada $\alpha$, els factors $\dfrac{|x_{i_j}|}{\|\mathbf{x}\|}$ estan fitats per a tot $j=0,\ldots,r$, el factor $|x_{i_{r+1}}|$ tendeix a zero quan $\mathbf{x}\to0$ i $|\mathbf{x}^\beta|\to0$ si $|\beta|>0$, aleshores $\left|\dfrac{P(\mathbf{x})}{\|\mathbf{x}\|^r}\right|$ també tendeix a zero, tal com volíem demostrar.

$\Longrightarrow$ Suposem ara que $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}\frac{P(\mathbf{x})}{\|\mathbf{x}\|^r}=0$ i volem demostrar que tots els monomis de $P$ són de grau $\geqslant r+1$.

Ho demostrarem per inducció en $r$.

Per a $r=0$, hem de veure que si $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}P(\mathbf{x})=0$, aleshores tots els monomis de $P$ són de grau $\geqslant1$. Com que $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}P(\mathbf{x})=P(0)$, per continuïtat, tenim que $P(0)=0$ i, per tant, el polinomi $P$ no té termes de grau zero.

Ara, suposem-ho cert fins a $r=m$ i ho volem demostrar per a $r=m+1$. Sabem, doncs, que si $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}\frac{P(\mathbf{x})}{\|\mathbf{x}\|^m}=0$, aleshores tots els monomis de $P$ són de grau $\geq m+1$.

Suposem ara que $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}\frac{P(\mathbf{x})}{\|\mathbf{x}\|^{m+1}}=0$. En particular, tenim que $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}\frac{P(\mathbf{x})}{\|\mathbf{x}\|^m}=0$ ja que $\dfrac{P(\mathbf{x})}{\|\mathbf{x}\|^{m+1}}=\dfrac{P(\mathbf{x})}{\|\mathbf{x}\|^m}\dfrac{1}{\|\mathbf{x}\|}$ i el darrer terme tendeix a infinit quan $\mathbf{x}$ tendeix a $0$. Per tant, tots els monomis de $P$ són de grau $\geq m+1$;$\ldots$ però volem demostrar que tots els monomis de $P$ són de grau $\geq m+2$. Ho farem per reducció a l'absurd.

Suposem, doncs, que $P$ té monomis de grau $m+1$, i separem $P$ en dos termes segons el grau dels seus monomis: $P(\mathbf{x})=P_{m+1}(\mathbf{x})+P_{\geq m+2}(\mathbf{x})$, on $P_{m+1}$ conté els termes de grau exactament $m+1$ i la resta, de grau superior, els posem a $P_{\geq m+2}$. Per hipòtesi, $P_{m+1}\not\equiv0$ i, per tant, existeix almenys un vector $\mathbf{v}\in\mathbb{R}^n$ tal que $P(\mathbf{v})\neq0$; a més, $P(t\,\mathbf{v})=t^{m+1}\,P(\mathbf{v})$, per a tot $t\in\mathbb{R}$.

Finalment, tenim per una banda que $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}\frac{P(t\mathbf{v})}{\|t\mathbf{v}\|^{m+1}}=0$, per hipòtesi. Però, per altra banda,
$$\lim_{\mathbf{x}\to\mathbf{0}}\frac{P(t\mathbf{v})}{\|t\mathbf{v}\|^{m+1}}=\lim_{t\to0}\frac{t^{m+1}}{|t|^{m+1}}\frac{P_{m+1}(\mathbf{v})}{\|\mathbf{v}\|^{m+1}}+\lim_{t\to0}\frac{P_{\geq m+2}(t\mathbf{v})}{\|t\mathbf{v}\|^{m+1}}\neq0$$
ja que $\displaystyle\lim_{t\to0}\frac{P_{m+1}(\mathbf{v})}{\|\mathbf{v}\|^{m+1}}\neq0$ i $\displaystyle\lim_{t\to0}\frac{P_{\geq m+2}(t\mathbf{v})}{\|t\mathbf{v}\|^{m+1}}=0$ per la implicació contrària del lema, ja demostrada anteriorment. Hem arribat, doncs, a contradicció i, per tant, queda demostrat que $P$ ha de tenir tots els monomis de grau $\geq m+2$.

NOTA: Amb tot rigor, cal prendre només un límit lateral, $\displaystyle\lim_{t\to0^+}$ o $\displaystyle\lim_{t\to0^-}$, per tal que $\displaystyle\lim_{t\to0}\frac{t^{m+1}}{|t|^{m+1}}$ existeixi.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $P(\mathbf{x})\neq0$ un polinomi, $\mathbf{x}=(x_1,\ldots,x_n)$, i $r\geq0$ un enter. Llavors $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}\frac{P(\mathbf{x})}{\|\mathbf{x}\|^r}=0$ si, i només si, tots els monomis de $P$ són de grau $\geqslant r+1$; i, en aquest cas, de fet, $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}\frac{P(\mathbf{x})}{\|\mathbf{x}\|^{r+1}}=0$.
[2] (demostració) $\Longleftarrow$ Suposem que $P(\mathbf{x})=\sum_{|\alpha|\geq r+1}a_\alpha\,\mathbf{x}^\alpha$. Com que cada monomi té almenys $r+1$ factors, per a cada $\alpha$ existeix $\beta=\beta(\alpha)$, amb $|\beta|\geq0$, tal que $\mathbf{x}^\alpha=x_{i_1}\cdots x_{i_{r+1}}\,\mathbf{x}^\beta$.
[3] (demostració) Per la desigualtat triangular, $\displaystyle\left|\frac{P(\mathbf{x})}{\|\mathbf{x}\|^r}\right|\leq\sum_{|\alpha|\geq r+1}|a_\alpha|\,\frac{|x_{i_1}|}{\|\mathbf{x}\|}\cdots\frac{|x_{i_r}|}{\|\mathbf{x}\|}\,|x_{i_{r+1}}|\,|\mathbf{x}^\beta|$.
[4] (demostració) Cada factor $\frac{|x_{i_j}|}{\|\mathbf{x}\|}$ està fitat per $1$, el factor $|x_{i_{r+1}}|$ tendeix a $0$ quan $\mathbf{x}\to\mathbf{0}$ i $|\mathbf{x}^\beta|$ val $1$ si $|\beta|=0$ i tendeix a $0$ si $|\beta|>0$. Com que la suma és finita, $\frac{P(\mathbf{x})}{\|\mathbf{x}\|^r}$ tendeix a $0$.
[5] (demostració) $\Longrightarrow$ Ho demostrem per inducció en $r$. Per a $r=0$: com que $P$ és continu, $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}P(\mathbf{x})=P(\mathbf{0})$, i per tant $P(\mathbf{0})=0$; és a dir, $P$ no té terme de grau zero i tots els seus monomis són de grau $\geq1$.
[6] (demostració) Suposem el resultat cert per a $r=m$, i que $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}\frac{P(\mathbf{x})}{\|\mathbf{x}\|^{m+1}}=0$. Com que $\frac{P(\mathbf{x})}{\|\mathbf{x}\|^m}=\frac{P(\mathbf{x})}{\|\mathbf{x}\|^{m+1}}\,\|\mathbf{x}\|$ i tots dos factors tendeixen a $0$, també $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}\frac{P(\mathbf{x})}{\|\mathbf{x}\|^m}=0$, i per hipòtesi d'inducció tots els monomis de $P$ són de grau $\geq m+1$.
[7] (demostració) Volem veure que són de grau $\geq m+2$, i ho fem per reducció a l'absurd. Suposem que $P$ té monomis de grau $m+1$ i escrivim $P=P_{m+1}+P_{\geq m+2}$, on $P_{m+1}\not\equiv0$ conté els monomis de grau exactament $m+1$ i $P_{\geq m+2}$ la resta.
[8] (demostració) Com que $P_{m+1}\not\equiv0$, per a tot $\mathbf{v}\neq\mathbf{0}$ es té $P_{m+1}(\mathbf{v})\neq0$; en fixem un. Com que $P_{m+1}$ és homogeni de grau $m+1$, $P_{m+1}(t\mathbf{v})=t^{m+1}P_{m+1}(\mathbf{v})$ per a tot $t\in\mathbb{R}$.
[9] (demostració) Restringim el límit a la semirecta $\mathbf{x}=t\mathbf{v}$, $t\to0^+$: per a $t>0$, $\displaystyle\frac{P(t\mathbf{v})}{\|t\mathbf{v}\|^{m+1}}=\frac{P_{m+1}(\mathbf{v})}{\|\mathbf{v}\|^{m+1}}+\frac{P_{\geq m+2}(t\mathbf{v})}{\|t\mathbf{v}\|^{m+1}}$. El segon terme tendeix a $0$ per la implicació $\Longleftarrow$ ja demostrada (o perquè és nul, si $P_{\geq m+2}\equiv0$).
[10] (demostració) Per tant, el límit al llarg d'aquesta semirecta és $\frac{P_{m+1}(\mathbf{v})}{\|\mathbf{v}\|^{m+1}}\neq0$, en contradicció amb la hipòtesi. Així, tots els monomis de $P$ són de grau $\geq m+2$.


## T5.15:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.15] Corol·lari 15 (Tema 5) — Taylor amb hipòtesi C^r
Si $f\in\mathcal{C}^r(\Omega)$ i $\mathbf{a}\in\Omega$, aleshores $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-P_r(x)}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$

Abans de demostrar-lo, observem que si apliquéssim estrictament el teorema de Taylor tal com l'hem enunciat, per obtenir el resultat del corol·lari 15, usaríem que
$$\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-P_r(x)}{\|\mathbf{x}-\mathbf{a}\|^r}=\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0,$$
i, per tant, necessitaríem suposar que $f\in\mathcal{C}^{\mathbf{r+1}}(\Omega)$. Així, doncs, el corol·lari 15 posa de manifest que l'exigència d'un ordre més de derivació es deu al fet que volem donar una expressió detallada del residu, i aquesta implica derivades d'ordre $r+1$; essencialment, però, només cal imposar $f\in\mathcal{C}^r(\Omega)$ per assegurar que $R_{r+1}(\mathbf{x})=o(\|\mathbf{x}-\mathbf{a}\|^r)$.
Demostració: Ho demostrem per a $f\in\mathcal{C}^2(\Omega)$; es generalitza fàcilment a ordre $r$.

Sabem que existeix $\xi_\mathbf{x}\in(\mathbf{a},\mathbf{x})$ tal que $f(\mathbf{x})-P_1(\mathbf{x})=R_2(\mathbf{x})$, amb $R_2(\mathbf{x})=\frac12\sum_{i,j=1}^{n}D_{ij}f(\xi_\mathbf{x})(x_i-a_i)(x_j-a_j)$. Fixades $\mathbf{x}=(x_1,\ldots,x_n)$ i $\mathbf{a}=(a_1,\ldots,a_n)$, denotem
$$T_2(\cdot):=\frac12\sum_{i,j=1}^{n}D_{ij}f(\cdot)(x_i-a_i)(x_j-a_j);$$
Observem que, en aquesta notació, $P_2(\mathbf{x})=P_1(\mathbf{x})+T_2(\mathbf{a})$ i $R_2(\mathbf{x})=T_2(\xi_\mathbf{x})$. Per tant,
$$f(\mathbf{x})-P_2(\mathbf{x})=f(\mathbf{x})-P_1(\mathbf{x})-T_2(\mathbf{a})=R_2(\mathbf{x})-T_2(\mathbf{a})=T_2(\xi_\mathbf{x})-T_2(\mathbf{a}).$$
Dividint per $\|\mathbf{x}-\mathbf{a}\|^2$ i prenent límits, arribem a
$$\begin{aligned}\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-P_2(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^2}&=\lim_{\mathbf{x}\to\mathbf{a}}\frac{T_2(\xi_\mathbf{x})-T_2(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}\\
&=\frac12\lim_{\mathbf{x}\to\mathbf{a}}\frac{\sum_{i,j=1}^{n}D_{ij}f(\xi_\mathbf{x})(x_i-a_i)(x_j-a_j)-\sum_{i,j=1}^{n}D_{ij}f(\mathbf{a})(x_i-a_i)(x_j-a_j)}{\|\mathbf{x}-\mathbf{a}\|^2}\\
&=\frac12\lim_{\mathbf{x}\to\mathbf{a}}\sum_{i,j=1}^{n}\left(D_{ij}f(\xi_\mathbf{x})-D_{i,j}f(\mathbf{a})\right)\frac{x_i-a_i}{\|\mathbf{x}-\mathbf{a}\|}\frac{x_j-a_j}{\|\mathbf{x}-\mathbf{a}\|}.\end{aligned}$$
Ara bé, d'una banda, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\left(D_{ij}f(\xi_\mathbf{x})-D_{i,j}f(\mathbf{a})\right)=0$ perquè $f\in\mathcal{C}^2(\Omega)$ i $\xi_\mathbf{x}$ tendeix a $\mathbf{a}$; de l'altra, els factors $\dfrac{|x_i-a_i|}{\|\mathbf{x}-\mathbf{a}\|}$ estan fitats per $1$, amb la qual cosa obtenim el resultat que volíem.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $r\geq1$, $f\in\mathcal{C}^r(\Omega)$ i $\mathbf{a}\in\Omega$. Aleshores $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-P_{r-1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0$, on $P_k$ denota el polinomi de Taylor de grau $k$ de $f$ en $\mathbf{a}$.
[2] (demostració) Ho demostrem per a $r=2$, és a dir, per a $f\in\mathcal{C}^2(\Omega)$; el cas general és anàleg. Prenem $\rho>0$ amb $B(\mathbf{a},\rho)\subseteq\Omega$, de manera que, per a $\mathbf{x}\in B(\mathbf{a},\rho)$, el segment $[\mathbf{a},\mathbf{x}]$ és dins de $\Omega$.
[3] (demostració) Pel teorema de Taylor d'ordre $1$ (que només necessita $f\in\mathcal{C}^2(\Omega)$), existeix $\xi_\mathbf{x}\in(\mathbf{a},\mathbf{x})$ tal que $f(\mathbf{x})-P_1(\mathbf{x})=R_2(\mathbf{x})=\frac12\sum_{i,j=1}^{n}D_{ij}f(\xi_\mathbf{x})(x_i-a_i)(x_j-a_j)$.
[4] (demostració) Fixats $\mathbf{x}$ i $\mathbf{a}$, denotem $T_2(\mathbf{y}):=\frac12\sum_{i,j=1}^{n}D_{ij}f(\mathbf{y})(x_i-a_i)(x_j-a_j)$. Aleshores $P_2(\mathbf{x})=P_1(\mathbf{x})+T_2(\mathbf{a})$ i $R_2(\mathbf{x})=T_2(\xi_\mathbf{x})$, de manera que $f(\mathbf{x})-P_2(\mathbf{x})=T_2(\xi_\mathbf{x})-T_2(\mathbf{a})$.
[5] (demostració) Dividint per $\|\mathbf{x}-\mathbf{a}\|^2$ obtenim $\displaystyle\frac{f(\mathbf{x})-P_2(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^2}=\frac12\sum_{i,j=1}^{n}\big(D_{ij}f(\xi_\mathbf{x})-D_{ij}f(\mathbf{a})\big)\frac{x_i-a_i}{\|\mathbf{x}-\mathbf{a}\|}\,\frac{x_j-a_j}{\|\mathbf{x}-\mathbf{a}\|}$.
[6] (demostració) Quan $\mathbf{x}\to\mathbf{a}$, també $\xi_\mathbf{x}\to\mathbf{a}$, ja que $\|\xi_\mathbf{x}-\mathbf{a}\|\leq\|\mathbf{x}-\mathbf{a}\|$; com que les derivades $D_{ij}f$ són contínues ($f\in\mathcal{C}^2(\Omega)$), $D_{ij}f(\xi_\mathbf{x})-D_{ij}f(\mathbf{a})\to0$.
[7] (demostració) D'altra banda, cada factor $\frac{x_i-a_i}{\|\mathbf{x}-\mathbf{a}\|}$ tendeix a $0$ quan $\mathbf{x}\to\mathbf{a}$, ja que el seu numerador tendeix a $0$.
[8] (demostració) Per tant, cadascun dels $n^2$ sumands tendeix a $0$, i $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-P_2(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^2}=0$, que és el que volíem.


## T5.19:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.19] Corol·lari 19 (Tema 5) — Criteri d'analiticitat
Si $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és $\mathcal{C}^\infty(\Omega)$ i existeix $M>0$ tal que $|D_{i_1,\ldots,i_r}f(\mathbf{x})|\leqslant M^r$ per a tot $r\in\mathbb{N}$ i $\mathbf{x}\in\Omega$, llavors $f$ és analítica.
Demostració: Per hipòtesi, sabem que $f\in\mathcal{C}^r,\forall r\in\mathbb{N}$. Per tant, $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})=Q_0(\mathbf{x})+\cdots+Q_r(\mathbf{x})+R_{r+1}(\mathbf{x})$, on els polinomis $Q_k$, per a $k=0,\ldots,r$, són homogenis, i
$$|R_{r+1}(x)|=\left|\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1\ldots i_{r+1}}f(\xi_x)(x_{i_1}-a_{i_1})\ldots(x_{i_{r+1}}-a_{i_{r+1}})\right|.$$
Aplicant la desigualtat triangular i després la fita de les derivades parcials de $f$, tenim que
$$|R_{r+1}(\mathbf{x})|\leq\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}M^{r+1}\|\mathbf{x}-\mathbf{a}\|^{r+1}=\frac{1}{(r+1)!}M^{r+1}\|\mathbf{x}-\mathbf{a}\|^{r+1}n^{r+1},$$
que tendeix a zero quan $r$ tendeix a infinit perquè la sèrie $\sum_{r=0}^{\infty}\dfrac{(M\,\|\mathbf{x}-\mathbf{a}\|\,n)^{r+1}}{(r+1)!}$ convergeix a $\exp(M\,\|\mathbf{x}-\mathbf{a}\|\,n)$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ de classe $\mathcal{C}^\infty(\Omega)$. Si per a cada $r\in\mathbb{N}$ existeix $M>0$ tal que $|D_{i_1,\ldots,i_r}f(\mathbf{x})|\leqslant M^r$ per a tot $\mathbf{x}\in\Omega$ i tots els índexs $i_1,\ldots,i_r$, llavors $f$ és analítica.
[2] (demostració) Sigui $\mathbf{a}\in\Omega$ i $\mathbf{x}$ amb $[\mathbf{a},\mathbf{x}]\subseteq\Omega$. Com que $f\in\mathcal{C}^{r+1}(\Omega)$ per a tot $r\in\mathbb{N}$, el teorema de Taylor dona, per a cada $r$, $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})=Q_0(\mathbf{x})+\cdots+Q_r(\mathbf{x})+R_{r+1}(\mathbf{x})$, on cada $Q_k$ és un polinomi homogeni de grau $k$ en $\mathbf{x}-\mathbf{a}$.
[3] (demostració) El residu és $R_{r+1}(\mathbf{x})=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1\ldots i_{r+1}}f(\xi_\mathbf{x})(x_{i_1}-a_{i_1})\cdots(x_{i_{r+1}}-a_{i_{r+1}})$, amb $\xi_\mathbf{x}\in(\mathbf{a},\mathbf{x})$.
[4] (demostració) Per la desigualtat triangular, la fita de les derivades parcials i $|x_i-a_i|\leq\|\mathbf{x}-\mathbf{a}\|$, cada sumand de $R_{r+1}(\mathbf{x})$ té valor absolut com a molt $\frac{1}{(r+1)!}M^{r+1}\|\mathbf{x}-\mathbf{a}\|^{r+1}$. Com que la suma té $(r+1)\,n$ sumands, $|R_{r+1}(\mathbf{x})|\leq\frac{(r+1)\,n}{(r+1)!}\big(M\|\mathbf{x}-\mathbf{a}\|\big)^{r+1}$, que tendeix a $0$ quan $r\to\infty$, perquè $\frac{c^k}{k!}\to0$ per a tot $c\geq0$.
[5] (demostració) Per tant, $f(\mathbf{x})=\lim_{r\to\infty}P_r(\mathbf{x})=\sum_{k=0}^{\infty}Q_k(\mathbf{x})$: la sèrie de Taylor de $f$ en $\mathbf{a}$ convergeix a $f(\mathbf{x})$ per a tot $\mathbf{x}$ amb $[\mathbf{a},\mathbf{x}]\subseteq\Omega$, en particular en una bola centrada en $\mathbf{a}$, i $f$ és analítica.


## T5.23:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.23] Proposició 23 (Tema 5) — Els extrems són punts crítics
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció diferenciable en $\mathbf{a}\in\Omega$. Si $\mathbf{a}$ és un extrem (és a dir, un màxim o un mínim) local de $f$, llavors $\mathbf{a}$ és un punt crític de $f$.
Demostració: Sigui $f:\Omega\to\mathbb{R}$ una funció diferenciable i $\mathbf{a}\in\Omega$ un extrem local. Aleshores, per a cada $i=1,\ldots,n$, i $\epsilon$ suficientment petit, podem considerar la funció
$$\begin{array}{cccc}g_i:&(a_i-\epsilon,a_i+\epsilon)&\longrightarrow&\mathbb{R}\\&x&\longmapsto&f(a_1,\ldots,a_{i-1},x,a_{i+1},\ldots,a_n),\end{array}$$
que és derivable i $g_i'(a_i)=\dfrac{\partial f}{\partial x_i}(\mathbf{a})$. Com que $g$ ha de tenir un extrem local en $x=a_i$, és a dir, $g_i'(a_i)=0$ ja que un extrem local ho ha de ser en totes les direccions, deduïm que $\dfrac{\partial f}{\partial x_i}(\mathbf{a})=0$ per a tot $i=1,\ldots,n$, i per tant, $Df(\mathbf{a})=(0\ \ldots\ 0)$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció diferenciable en $\mathbf{a}\in\Omega$. Aleshores $\mathbf{a}$ és un extrem (és a dir, un màxim o un mínim) local de $f$ si, i només si, $\mathbf{a}$ és un punt crític de $f$.
[2] (demostració) Suposem que $\mathbf{a}$ és un extrem local; per exemple, un màxim local (el cas del mínim és anàleg, o s'obté aplicant el raonament a $-f$). Existeix $\epsilon>0$ tal que $B(\mathbf{a},\epsilon)\subseteq\Omega$ i $f(\mathbf{x})\leq f(\mathbf{a})$ per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)$.
[3] (demostració) Per a cada $i=1,\ldots,n$ considerem $g_i:(a_i-\epsilon,a_i+\epsilon)\to\mathbb{R}$, $g_i(x)=f(a_1,\ldots,a_{i-1},x,a_{i+1},\ldots,a_n)$. Com que $f$ és diferenciable en $\mathbf{a}$, $g_i$ és derivable en $a_i$ i $g_i'(a_i)=\frac{\partial f}{\partial x_i}(\mathbf{a})$.
[4] (demostració) A més, $g_i(x)\leq g_i(a_i)$ per a tot $x\in(a_i-\epsilon,a_i+\epsilon)$: $g_i$ té un màxim local en $a_i$, ja que un extrem local de $f$ ho és també en cada direcció.
[5] (demostració) Per tant, el quocient $\frac{g_i(x)-g_i(a_i)}{x-a_i}$ és $\leq0$ si $x>a_i$ i és $\leq0$ si $x<a_i$. Prenent límits laterals en $a_i$, obtenim $g_i'(a_i)\leq0$ i $g_i'(a_i)\geq0$, és a dir, $g_i'(a_i)=0$.
[6] (demostració) Així, $\frac{\partial f}{\partial x_i}(\mathbf{a})=0$ per a tot $i=1,\ldots,n$ i, per tant, $Df(\mathbf{a})=(0\ \ldots\ 0)$: $\mathbf{a}$ és un punt crític de $f$.


## T5.28:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.28] Lema 28 (Tema 5) — Fites d'una forma definida positiva
Si $q_M:\mathbb{R}^n\to\mathbb{R}$ és una forma quadràtica definida positiva llavors existeixen constants $0<c\leqslant C<\infty$ tals que $c\|\mathbf{u}\|^2\leqslant q_M(\mathbf{u})\leqslant C\|\mathbf{u}\|^2$, $\forall\,\mathbf{u}\in\mathbb{R}^n$.
Demostració: Considerem el conjunt de vectors de norma 1: $S:=\{\mathbf{u}\in\mathbb{R}^n:\ \|\mathbf{u}\|=1\}$. Com que $S$ és compacte és a dir, tancat i fitat, pel teorema de Weierstrass, existeixen $\mathbf{u}_1,\mathbf{u}_2\in S$ tals que $c=q_M(\mathbf{u}_1)$ i $C=q_M(\mathbf{u}_2)$ compleixen que
$$c\leq q_M(\mathbf{u})\leq C,\qquad\forall\,\mathbf{u}\in S.$$
En general, si $\|\mathbf{u}\|\neq0$, considerem $\dfrac{\mathbf{u}}{\|\mathbf{u}\|}$ i li apliquem les desigualtats anteriors, tenim que $c\leq q_M\left(\dfrac{u}{\|\mathbf{u}\|}\right)\leq C$; per les propietats de les formes quadràtiques, $c\leq\dfrac{1}{\|\mathbf{u}\|^2}q_M(\mathbf{u})\leq C$, i, per tant, $c\,\|\mathbf{u}\|^2\leq q_M(\mathbf{u})\leq C\,\|\mathbf{u}\|^2$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Si $q_M:\mathbb{R}^n\to\mathbb{R}$ és una forma quadràtica semidefinida positiva, llavors existeixen constants $0<c\leqslant C<\infty$ tals que $c\|\mathbf{u}\|^2\leqslant q_M(\mathbf{u})\leqslant C\|\mathbf{u}\|^2$ per a tot $\mathbf{u}\in\mathbb{R}^n$.
[2] (demostració) Considerem el conjunt dels vectors de norma $1$, $S:=\{\mathbf{u}\in\mathbb{R}^n:\ \|\mathbf{u}\|=1\}$, que és compacte, és a dir, tancat i fitat.
[3] (demostració) La funció $q_M(\mathbf{u})=\mathbf{u}^TM\mathbf{u}$ és contínua, ja que és lineal en $\mathbf{u}$. Pel teorema de Weierstrass, existeixen $\mathbf{u}_1,\mathbf{u}_2\in S$ tals que $c:=q_M(\mathbf{u}_1)\leq q_M(\mathbf{u})\leq q_M(\mathbf{u}_2)=:C$ per a tot $\mathbf{u}\in S$; com que $\mathbf{u}_1\neq\mathbf{0}$ i $q_M$ és definida positiva, $c>0$.
[4] (demostració) Si $\mathbf{u}\neq\mathbf{0}$, el vector $\frac{\mathbf{u}}{\|\mathbf{u}\|}$ és de $S$, i per tant $c\leq q_M\left(\frac{\mathbf{u}}{\|\mathbf{u}\|}\right)\leq C$. Com que $q_M(\lambda\mathbf{u})=\lambda^2q_M(\mathbf{u})$, això és $c\leq\frac{q_M(\mathbf{u})}{\|\mathbf{u}\|^2}\leq C$, és a dir, $c\|\mathbf{u}\|^2\leq q_M(\mathbf{u})\leq C\|\mathbf{u}\|^2$.
[5] (demostració) Si $\mathbf{u}=\mathbf{0}$, els tres membres valen $0$ i les desigualtats també es compleixen.


## T5.6:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.6] Teorema 6 (Tema 5) — Teorema de Schwarz
(Schwarz). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$ i $D_iD_jf$ i $D_jD_if$ existeixen en $\Omega$. Si $D_iD_jf$ i $D_jD_if$ són contínues en un entorn d'$\mathbf{a}\in\Omega$, aleshores
$$D_iD_jf(\mathbf{a})=D_jD_if(\mathbf{a}).$$
Demostració: Farem la demostració per a $n=2$ i $m=1$, però es pot generalitzar fàcilment.

Prenem $h$ i $k$ no nuls tals que el rectangle $R(h,k)$ amb vèrtexs a $(a,b)$, $(a+h,b)$, $(a+h,b+k)$ i $(a,b+k)$ estigui contingut en $\Omega$.

Considerem l'expressió
$$\Delta(h,k)=f(a+h,b+k)-f(a+h,b)-f(a,b+k)+f(a,b),$$
que expressarem tant en termes de $D_{21}f$ com en termes de $D_{12}f$.

Considerem una nova funció $G(x)=f(x,b+k)-f(x,b)$, $x\in(a,a+h)$. Clarament,
$$\Delta(h,k)=G(a+h)-G(a)=h\,G'(\xi_x),$$
aplicant el teorema del valor mitjà per a una variable real, on $\xi_x\in(a,a+h)$. Com que $G'(x)=D_1f(x,b+k)-D_1f(x,b)$, tenim que
$$\Delta(h,k)=h\,\left(D_1f(\xi_x,b+k)-D_1f(\xi_x,b)\right).$$
Ara tornem a aplicar el teorema del valor mitjà al terme de la dreta i obtenim que
$$\Delta(h,k)=h\,k\,D_{12}f(\xi_x,\xi_y),\qquad \xi_y\in(b,b+k). \tag{1}$$
És clar que $(\xi_x,\xi_y)\in R(h,k)$.

Considerem ara una funció $H(y)=f(a+h,y)-f(a,y)$, amb $y\in(b,b+k)$. Repetint els mateixos raonaments usats per a $G$, arribem a la conclusió que existeixen $(\eta_x,\eta_y)\in R(h,k)$ tals que
$$\Delta(h,k)=h\,k\,D_{21}f(\eta_x,\eta_y). \tag{2}$$
Igualant (1) i (2), tenim que $D_{12}f(\xi_x,\xi_y)=D_{21}f(\eta_x,\eta_y)$, i prenent ara el límit per a $(h,k)\to(0,0)$, i tenint en compte la hipòtesi de continuïtat de les dues derivades segones, arribem a la conclusió desitjada.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Schwarz) Sigui $\Omega\subseteq\mathbb{R}^n$ obert i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$, $D_iD_jf$ i $D_jD_if$ existeixen en $\Omega$.
[2] (enunciat) Si $D_iD_jf$ i $D_jD_if$ són contínues en un entorn d'$\mathbf{a}\in\Omega$, aleshores $D_iD_jf=D_jD_if$ en tot $\Omega$.
[3] (demostració) Ho demostrem per a $n=2$, $m=1$ i $\mathbf{a}=(a,b)$; el cas general és anàleg. Prenem $h,k$ no nuls tals que el rectangle $R(h,k)$ de vèrtexs $(a,b)$, $(a+h,b)$, $(a+h,b+k)$ i $(a,b+k)$ sigui dins de $\Omega$, i considerem $\Delta(h,k)=f(a+h,b+k)-f(a+h,b)-f(a,b+k)+f(a,b)$.
[4] (demostració) Sigui $G(x)=f(x,b+k)-f(x,b)$, de manera que $\Delta(h,k)=G(a+h)-G(a)$. Com que $D_1f$ existeix en $\Omega$, $G$ és derivable (i, per tant, contínua) entre $a$ i $a+h$, amb $G'(x)=D_1f(x,b+k)-D_1f(x,b)$.
[5] (demostració) Pel teorema del valor mitjà, existeix $\xi_x\in(a,a+h)$ tal que $\Delta(h,k)=h\,G'(\xi_x)=h\big(D_1f(\xi_x,b+k)-D_1f(\xi_x,b)\big)$.
[6] (demostració) Fixat $\xi_x$, apliquem de nou el teorema del valor mitjà a la funció $y\mapsto D_1f(\xi_x,y)$, que és derivable amb derivada $D_2D_1f(\xi_x,y)$: existeix $\xi_y\in(b,b+k)$ tal que $\Delta(h,k)=h\,k\,D_2D_1f(\xi_x,\xi_y)$ (1), amb $(\xi_x,\xi_y)\in R(h,k)$.
[7] (demostració) Anàlogament, amb $H(y)=f(a+h,y)-f(a,y)$ tenim $\Delta(h,k)=H(b+k)-H(b)$; aplicant el teorema del valor mitjà primer en $y$ i després en $x$, obtenim $(\eta_x,\eta_y)\in R(h,k)$ tal que $\Delta(h,k)=h\,k\,D_1D_2f(\eta_x,\eta_y)$ (2).
[8] (demostració) Igualant (1) i (2) i dividint per $hk\neq0$, obtenim $D_2D_1f(\xi_x,\xi_y)=D_1D_2f(\eta_x,\eta_y)$. Quan $(h,k)\to(0,0)$, tots dos punts tendeixen a $(a,b)$, ja que són de $R(h,k)$, i per la continuïtat de $D_2D_1f$ i $D_1D_2f$ en un entorn de $(a,b)$ concloem que $D_2D_1f(a,b)=D_1D_2f(a,b)$.


## T5.6:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.6] Teorema 6 (Tema 5) — Teorema de Schwarz
(Schwarz). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$ i $D_iD_jf$ i $D_jD_if$ existeixen en $\Omega$. Si $D_iD_jf$ i $D_jD_if$ són contínues en un entorn d'$\mathbf{a}\in\Omega$, aleshores
$$D_iD_jf(\mathbf{a})=D_jD_if(\mathbf{a}).$$
Demostració: Farem la demostració per a $n=2$ i $m=1$, però es pot generalitzar fàcilment.

Prenem $h$ i $k$ no nuls tals que el rectangle $R(h,k)$ amb vèrtexs a $(a,b)$, $(a+h,b)$, $(a+h,b+k)$ i $(a,b+k)$ estigui contingut en $\Omega$.

Considerem l'expressió
$$\Delta(h,k)=f(a+h,b+k)-f(a+h,b)-f(a,b+k)+f(a,b),$$
que expressarem tant en termes de $D_{21}f$ com en termes de $D_{12}f$.

Considerem una nova funció $G(x)=f(x,b+k)-f(x,b)$, $x\in(a,a+h)$. Clarament,
$$\Delta(h,k)=G(a+h)-G(a)=h\,G'(\xi_x),$$
aplicant el teorema del valor mitjà per a una variable real, on $\xi_x\in(a,a+h)$. Com que $G'(x)=D_1f(x,b+k)-D_1f(x,b)$, tenim que
$$\Delta(h,k)=h\,\left(D_1f(\xi_x,b+k)-D_1f(\xi_x,b)\right).$$
Ara tornem a aplicar el teorema del valor mitjà al terme de la dreta i obtenim que
$$\Delta(h,k)=h\,k\,D_{12}f(\xi_x,\xi_y),\qquad \xi_y\in(b,b+k). \tag{1}$$
És clar que $(\xi_x,\xi_y)\in R(h,k)$.

Considerem ara una funció $H(y)=f(a+h,y)-f(a,y)$, amb $y\in(b,b+k)$. Repetint els mateixos raonaments usats per a $G$, arribem a la conclusió que existeixen $(\eta_x,\eta_y)\in R(h,k)$ tals que
$$\Delta(h,k)=h\,k\,D_{21}f(\eta_x,\eta_y). \tag{2}$$
Igualant (1) i (2), tenim que $D_{12}f(\xi_x,\xi_y)=D_{21}f(\eta_x,\eta_y)$, i prenent ara el límit per a $(h,k)\to(0,0)$, i tenint en compte la hipòtesi de continuïtat de les dues derivades segones, arribem a la conclusió desitjada.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Schwarz) Sigui $\Omega\subseteq\mathbb{R}^n$ obert i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$, $D_iD_jf$ i $D_jD_if$ existeixen en $\Omega$.
[2] (enunciat) Aleshores, per a tot $\mathbf{a}\in\Omega$, $D_iD_jf(\mathbf{a})=D_jD_if(\mathbf{a})$.
[3] (demostració) Ho demostrem per a $n=2$, $m=1$ i $\mathbf{a}=(a,b)$; el cas general és anàleg. Prenem $h,k$ no nuls tals que el rectangle $R(h,k)$ de vèrtexs $(a,b)$, $(a+h,b)$, $(a+h,b+k)$ i $(a,b+k)$ sigui dins de $\Omega$, i considerem $\Delta(h,k)=f(a+h,b+k)-f(a+h,b)-f(a,b+k)+f(a,b)$.
[4] (demostració) Sigui $G(x)=f(x,b+k)-f(x,b)$, de manera que $\Delta(h,k)=G(a+h)-G(a)$. Com que $D_1f$ existeix en $\Omega$, $G$ és derivable (i, per tant, contínua) entre $a$ i $a+h$, amb $G'(x)=D_1f(x,b+k)-D_1f(x,b)$.
[5] (demostració) Pel teorema del valor mitjà, existeix $\xi_x\in(a,a+h)$ tal que $\Delta(h,k)=h\,G'(\xi_x)=h\big(D_1f(\xi_x,b+k)-D_1f(\xi_x,b)\big)$.
[6] (demostració) Fixat $\xi_x$, apliquem de nou el teorema del valor mitjà a la funció $y\mapsto D_1f(\xi_x,y)$, que és derivable amb derivada $D_2D_1f(\xi_x,y)$: existeix $\xi_y\in(b,b+k)$ tal que $\Delta(h,k)=h\,k\,D_2D_1f(\xi_x,\xi_y)$ (1), amb $(\xi_x,\xi_y)\in R(h,k)$.
[7] (demostració) Anàlogament, amb $H(y)=f(a+h,y)-f(a,y)$ tenim $\Delta(h,k)=H(b+k)-H(b)$; aplicant el teorema del valor mitjà primer en $y$ i després en $x$, obtenim $(\eta_x,\eta_y)\in R(h,k)$ tal que $\Delta(h,k)=h\,k\,D_1D_2f(\eta_x,\eta_y)$ (2).
[8] (demostració) Igualant (1) i (2) i dividint per $hk\neq0$, obtenim $D_2D_1f(\xi_x,\xi_y)=D_1D_2f(\eta_x,\eta_y)$. Quan $(h,k)\to(0,0)$, tots dos punts tendeixen a $(a,b)$, ja que són de $R(h,k)$, i per la continuïtat de $D_1f$ i $D_2f$ en un entorn de $(a,b)$ concloem que $D_2D_1f(a,b)=D_1D_2f(a,b)$.


## T5.6:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.6] Teorema 6 (Tema 5) — Teorema de Schwarz
(Schwarz). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$ i $D_iD_jf$ i $D_jD_if$ existeixen en $\Omega$. Si $D_iD_jf$ i $D_jD_if$ són contínues en un entorn d'$\mathbf{a}\in\Omega$, aleshores
$$D_iD_jf(\mathbf{a})=D_jD_if(\mathbf{a}).$$
Demostració: Farem la demostració per a $n=2$ i $m=1$, però es pot generalitzar fàcilment.

Prenem $h$ i $k$ no nuls tals que el rectangle $R(h,k)$ amb vèrtexs a $(a,b)$, $(a+h,b)$, $(a+h,b+k)$ i $(a,b+k)$ estigui contingut en $\Omega$.

Considerem l'expressió
$$\Delta(h,k)=f(a+h,b+k)-f(a+h,b)-f(a,b+k)+f(a,b),$$
que expressarem tant en termes de $D_{21}f$ com en termes de $D_{12}f$.

Considerem una nova funció $G(x)=f(x,b+k)-f(x,b)$, $x\in(a,a+h)$. Clarament,
$$\Delta(h,k)=G(a+h)-G(a)=h\,G'(\xi_x),$$
aplicant el teorema del valor mitjà per a una variable real, on $\xi_x\in(a,a+h)$. Com que $G'(x)=D_1f(x,b+k)-D_1f(x,b)$, tenim que
$$\Delta(h,k)=h\,\left(D_1f(\xi_x,b+k)-D_1f(\xi_x,b)\right).$$
Ara tornem a aplicar el teorema del valor mitjà al terme de la dreta i obtenim que
$$\Delta(h,k)=h\,k\,D_{12}f(\xi_x,\xi_y),\qquad \xi_y\in(b,b+k). \tag{1}$$
És clar que $(\xi_x,\xi_y)\in R(h,k)$.

Considerem ara una funció $H(y)=f(a+h,y)-f(a,y)$, amb $y\in(b,b+k)$. Repetint els mateixos raonaments usats per a $G$, arribem a la conclusió que existeixen $(\eta_x,\eta_y)\in R(h,k)$ tals que
$$\Delta(h,k)=h\,k\,D_{21}f(\eta_x,\eta_y). \tag{2}$$
Igualant (1) i (2), tenim que $D_{12}f(\xi_x,\xi_y)=D_{21}f(\eta_x,\eta_y)$, i prenent ara el límit per a $(h,k)\to(0,0)$, i tenint en compte la hipòtesi de continuïtat de les dues derivades segones, arribem a la conclusió desitjada.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Schwarz) Sigui $\Omega\subseteq\mathbb{R}^n$ obert i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$, $D_iD_jf$ i $D_jD_if$ existeixen en $\Omega$.
[2] (enunciat) Si $D_iD_jf$ i $D_jD_if$ són contínues en $\Omega\setminus\{\mathbf{a}\}$, on $\mathbf{a}\in\Omega$, aleshores $D_iD_jf(\mathbf{a})=D_jD_if(\mathbf{a})$.
[3] (demostració) Ho demostrem per a $n=2$, $m=1$ i $\mathbf{a}=(a,b)$; el cas general és anàleg. Prenem $h,k$ no nuls tals que el rectangle $R(h,k)$ de vèrtexs $(a,b)$, $(a+h,b)$, $(a+h,b+k)$ i $(a,b+k)$ sigui dins de $\Omega$, i considerem $\Delta(h,k)=f(a+h,b+k)-f(a+h,b)-f(a,b+k)+f(a,b)$.
[4] (demostració) Sigui $G(x)=f(x,b+k)-f(x,b)$, de manera que $\Delta(h,k)=G(a+h)-G(a)$. Com que $D_1f$ existeix en $\Omega$, $G$ és derivable (i, per tant, contínua) entre $a$ i $a+h$, amb $G'(x)=D_1f(x,b+k)-D_1f(x,b)$.
[5] (demostració) Pel teorema del valor mitjà, per a tot $\xi_x\in(a,a+h)$ es té $\Delta(h,k)=h\,G'(\xi_x)=h\big(D_1f(\xi_x,b+k)-D_1f(\xi_x,b)\big)$.
[6] (demostració) Fixat $\xi_x$, apliquem de nou el teorema del valor mitjà a la funció $y\mapsto D_1f(\xi_x,y)$, que és derivable amb derivada $D_2D_1f(\xi_x,y)$: existeix $\xi_y\in(b,b+k)$ tal que $\Delta(h,k)=h\,k\,D_2D_1f(\xi_x,\xi_y)$ (1), amb $(\xi_x,\xi_y)\in R(h,k)$.
[7] (demostració) Anàlogament, amb $H(y)=f(a+h,y)-f(a,y)$ tenim $\Delta(h,k)=H(b+k)-H(b)$; aplicant el teorema del valor mitjà primer en $y$ i després en $x$, obtenim $(\eta_x,\eta_y)\in R(h,k)$ tal que $\Delta(h,k)=h\,k\,D_1D_2f(\eta_x,\eta_y)$ (2).
[8] (demostració) Igualant (1) i (2) i dividint per $hk\neq0$, obtenim $D_2D_1f(\xi_x,\xi_y)=D_1D_2f(\eta_x,\eta_y)$. Fem ara tendir $h\to0$, amb $k$ fix: tots dos punts tendeixen a $(a,b)$, ja que són de $R(h,k)$, i per la continuïtat de $D_2D_1f$ i $D_1D_2f$ en un entorn de $(a,b)$ concloem que $D_2D_1f(a,b)=D_1D_2f(a,b)$.


## T5.14:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.14] Teorema 14 (Tema 5) — Teorema de Taylor (diverses variables)
(de Taylor). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^{r+1}(\Omega)$, i $\mathbf{a}\in\Omega$. Per a tot $\mathbf{x}\in\Omega$ amb $[\mathbf{a},\mathbf{x}]\subseteq\Omega$, existeix $\xi_\mathbf{x}\in(\mathbf{a},\mathbf{x})$ tal que $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$, on

(i) El polinomi
$$\begin{aligned}P_r(\mathbf{x})={}&f(\mathbf{a})+\sum_{i=1}^{n}D_if(\mathbf{a})(x_i-a_i)+\frac{1}{2!}\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_i)(x_j-a_j)+\cdots\\
&\cdots+\frac{1}{r!}\sum_{i_1,\ldots,i_r=1}^{n}D_{i_1,\ldots,i_r}f(\mathbf{a})(x_{i_1}-a_{i_1})\cdots(x_{i_r}-a_{i_r})\end{aligned}$$
s'anomena el polinomi de Taylor de grau $r$ de la funció $f$ en el punt $\mathbf{a}$,

(ii) El residu de grau $r$ de la funció $f$ en el punt $\mathbf{a}$ és
$$R_{r+1}(\mathbf{x})=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})(x_{i_1}-a_{i_1})\cdots(x_{i_{r+1}}-a_{i_{r+1}}).$$
A més, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$
Demostració: Construïm la següent funció $F(t)=f(h(t))$ a $\mathbb{R}$:
$$\begin{array}{ccccc}[0,1]\subset\mathbb{R}&\longrightarrow&\Omega\subseteq\mathbb{R}^n&\longrightarrow&\mathbb{R}\\ t&\longmapsto&\mathbf{a}+t(\mathbf{x}-\mathbf{a})&\longmapsto&f(\mathbf{a}+t(\mathbf{x}-\mathbf{a}))\end{array}$$
Observem que $F(1)=f(\mathbf{x})$ i $F(0)=f(\mathbf{a})$; d'altra banda, com que $f\in\mathcal{C}^{r+1}(\Omega)$ i $h$ és una funció lineal, $F(t)=f(h(t))$ és una funció de classe $r+1$ en algun obert $U$ tal que $[0,1]\subset U$. Si apliquem la fórmula de Taylor per a funcions d'una variable a $F(t)$, tenim que $F(t)=\sum_{k=0}^{r}\dfrac{F^{(k)}(0)}{k!}t^k+\dfrac{F^{(r+1)}(t_x)}{(r+1)!}t^{r+1}$, amb $t_x\in(0,t)$. Aplicant-la a $t=1$,
$$F(1)=\sum_{k=0}^{r}\frac{F^{(k)}(0)}{k!}+\frac{F^{(r+1)}(\tau)}{(r+1)!},\qquad\tau\in(0,1).$$
Ens basarem en aquest desenvolupament per a demostrar la fórmula de Taylor per al camp escalar $f$. D'entrada, doncs, caldrà calcular la funció $F$ i les seves derivades en $t=0$. Ja hem vist que $F(0)=f(\mathbf{a})$. Veurem que
$$F^{(k)}(t)=\sum_{i_1,\ldots,i_k=1}^{n}D_{i_1,\ldots,i_k}f(h(t))\,(x_{i_1}-a_{i_1})\ldots(x_{i_k}-a_{i_k}),\qquad\text{per a }k\leq r+1. \tag{3}$$
Fixem-nos que, per a $t=0$,
$$F^{(k)}(0)=\sum_{i_1,\ldots,i_k=1}^{n}D_{i_1,\ldots,i_k}f(\mathbf{a})\,(x_{i_1}-a_{i_1})\ldots(x_{i_k}-a_{i_k}),$$
que coincideix amb el terme d'ordre $k$ del polinomi $P_r$.

Per a $r=1$, clarament, per la regla de la cadena, es compleix la igualtat (3):
$$F'(t)=\sum_{i=1}^{n}D_if(h(t))\,h_i'(t)=\sum_{i=1}^{n}D_if(h(t))\,(x_i-a_i).$$
Suposem ara que la fórmula (3) és cert per a $k\leq m$ i demostrem que és certa per a $k=m+1$:
$$\begin{aligned}F^{(m+1)}(t)&=\frac{d}{dt}F^{(m)}(t)=\frac{d}{dt}\sum_{i_1,\ldots,i_m=1}^{n}D_{i_1,\ldots,i_m}f(h(t))\,(x_{i_1}-a_{i_1})\ldots(x_{i_m}-a_{i_m})\\
&=\sum_{j=1}^{n}D_j\left(\sum_{i_1,\ldots,i_m=1}^{n}D_{i_1,\ldots,i_m}f(h(t))\,(x_{i_1}-a_{i_1})\ldots(x_{i_m}-a_{i_m})\right)h_j'(t)\\
&=\sum_{i_1,\ldots,i_m=1}^{n}D_{i_1,\ldots,i_{m+1}}f(h(t))\,(x_{i_1}-a_{i_1})\ldots(x_{i_{m+1}}-a_{i_{m+1}}),\end{aligned}$$
prenent $j=i_{m+1}$. Per tant, hem demostrat (3) per inducció; aplicant-la fins a $k=r$, es demostra que $\sum_{k=0}^{r}\dfrac{F^{(k)}(0)}{k!}$ és exactament el polinomi $P_r(\mathbf{x})$ de l'enunciat.

Pel que fa al residu $R_{r+1}(\mathbf{x})$, atenent a la fórmula de Taylor de $F$,
$$R_{r+1}(\mathbf{x})=\frac{F^{(r+1)}(\tau)}{(r+1)!}=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(h(\tau))\,(x_{i_1}-a_{i_1})\ldots(x_{i_{r+1}}-a_{i_{r+1}}),$$
que, prenent $\xi_x=h(\tau)\in(\mathbf{a},\mathbf{x})$, coincideix amb la fórmula de l'enunciat.

Finalment,
$$\begin{aligned}\frac{|R_{r+1}(\mathbf{x})|}{\|\mathbf{x}-\mathbf{a}\|^r}&=\frac{1}{(r+1)!}\frac{1}{\|\mathbf{x}-\mathbf{a}\|^r}\left|\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})\,(x_{i_1}-a_{i_1})\ldots(x_{i_{r+1}}-a_{i_{r+1}})\right|\\
&\leq\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}\left|D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})\right|\frac{|x_{i_1}-a_{i_1}|}{\|\mathbf{x}-\mathbf{a}\|}\ldots\frac{|x_{i_r}-a_{i_r}|}{\|\mathbf{x}-\mathbf{a}\|}\,|x_{i_{r+1}}-a_{i_{r+1}}|.\end{aligned}$$
Analitzant els termes de la fórmula que hem obtingut, observem que:

- $\left|D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})\right|$ tendeix a $\left|D_{i_1,\ldots,i_{r+1}}f(\mathbf{a})\right|$ quan $\mathbf{x}$ tendeix a $\mathbf{a}$.
- Per a tot $i=1,\ldots,n$, $\dfrac{|x_i-a_i|}{\|\mathbf{x}-\mathbf{a}\|}\leq1$.
- El terme $|x_{i_{r+1}}-a_{i_{r+1}}|$ tendeix a $0$ quan $\mathbf{x}$ tendeix a $\mathbf{a}$.

Per tant,
$$\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(x)}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}$ de classe $\mathcal{C}^{r+1}(\Omega)$ i $\mathbf{a}\in\Omega$. Per a tot $\mathbf{x}\in\Omega$ amb $[\mathbf{a},\mathbf{x}]\subseteq\Omega$, prenent el punt mitjà $\xi_\mathbf{x}=\frac{\mathbf{a}+\mathbf{x}}{2}$ es té $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$, on $P_r(\mathbf{x})=f(\mathbf{a})+\sum_{i=1}^{n}D_if(\mathbf{a})(x_i-a_i)+\cdots+\frac{1}{r!}\sum_{i_1,\ldots,i_r=1}^{n}D_{i_1,\ldots,i_r}f(\mathbf{a})(x_{i_1}-a_{i_1})\cdots(x_{i_r}-a_{i_r})$ és el polinomi de Taylor de grau $r$ de $f$ en $\mathbf{a}$.
[2] (enunciat) El residu és $R_{r+1}(\mathbf{x})=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})(x_{i_1}-a_{i_1})\cdots(x_{i_{r+1}}-a_{i_{r+1}})$.
[3] (enunciat) A més, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0$.
[4] (demostració) Sigui $h(t)=\mathbf{a}+t(\mathbf{x}-\mathbf{a})$ i $F(t)=f(h(t))$. Com que $[\mathbf{a},\mathbf{x}]\subseteq\Omega$ i $\Omega$ és obert, $F$ està definida i és de classe $\mathcal{C}^{r+1}$ en un obert $U\supseteq[0,1]$ (composició de $f$ amb $h$, que és afí), i $F(0)=f(\mathbf{a})$, $F(1)=f(\mathbf{x})$.
[5] (demostració) Per la fórmula de Taylor en una variable aplicada a $F$ en $[0,1]$, existeix $\tau\in(0,1)$ tal que $F(1)=\sum_{k=0}^{r}\frac{F^{(k)}(0)}{k!}+\frac{F^{(r+1)}(\tau)}{(r+1)!}$.
[6] (demostració) Veurem que, per a $k\leq r+1$, $F^{(k)}(t)=\sum_{i_1,\ldots,i_k=1}^{n}D_{i_1,\ldots,i_k}f(h(t))(x_{i_1}-a_{i_1})\cdots(x_{i_k}-a_{i_k})$ (3). Per a $k=1$ és la regla de la cadena: $F'(t)=\sum_{i=1}^{n}D_if(h(t))\,h_i'(t)=\sum_{i=1}^{n}D_if(h(t))(x_i-a_i)$.
[7] (demostració) Si (3) és cert per a $k=m\leq r$, derivant amb la regla de la cadena cada terme $D_{i_1,\ldots,i_m}f(h(t))$ obtenim $\sum_{j=1}^{n}D_{i_1,\ldots,i_m,j}f(h(t))(x_j-a_j)$; prenent $j=i_{m+1}$, resulta (3) per a $k=m+1$. Per inducció, (3) val per a tot $k\leq r+1$.
[8] (demostració) En $t=0$, $\frac{F^{(k)}(0)}{k!}$ és exactament el terme d'ordre $k$ de $P_r$, de manera que $\sum_{k=0}^{r}\frac{F^{(k)}(0)}{k!}=P_r(\mathbf{x})$; i $\frac{F^{(r+1)}(\tau)}{(r+1)!}=R_{r+1}(\mathbf{x})$ prenent $\xi_\mathbf{x}=h(\tau)\in(\mathbf{a},\mathbf{x})$. Això demostra que $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$.
[9] (demostració) Finalment, si $B(\mathbf{a},\rho)\subseteq\Omega$, per a $\mathbf{x}\in B(\mathbf{a},\rho)$ el segment $[\mathbf{a},\mathbf{x}]$ és dins de $\Omega$ i, per la desigualtat triangular, $\frac{|R_{r+1}(\mathbf{x})|}{\|\mathbf{x}-\mathbf{a}\|^r}\leq\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}|D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})|\frac{|x_{i_1}-a_{i_1}|}{\|\mathbf{x}-\mathbf{a}\|}\cdots\frac{|x_{i_r}-a_{i_r}|}{\|\mathbf{x}-\mathbf{a}\|}|x_{i_{r+1}}-a_{i_{r+1}}|$.
[10] (demostració) Quan $\mathbf{x}\to\mathbf{a}$, $|D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})|\to|D_{i_1,\ldots,i_{r+1}}f(\mathbf{a})|$, perquè $\xi_\mathbf{x}\to\mathbf{a}$ i les derivades d'ordre $r+1$ de $f$ són contínues; cada quocient $\frac{|x_i-a_i|}{\|\mathbf{x}-\mathbf{a}\|}$ és $\leq1$, i $|x_{i_{r+1}}-a_{i_{r+1}}|\to0$. Per tant, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0$.


## T5.14:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.14] Teorema 14 (Tema 5) — Teorema de Taylor (diverses variables)
(de Taylor). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^{r+1}(\Omega)$, i $\mathbf{a}\in\Omega$. Per a tot $\mathbf{x}\in\Omega$ amb $[\mathbf{a},\mathbf{x}]\subseteq\Omega$, existeix $\xi_\mathbf{x}\in(\mathbf{a},\mathbf{x})$ tal que $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$, on

(i) El polinomi
$$\begin{aligned}P_r(\mathbf{x})={}&f(\mathbf{a})+\sum_{i=1}^{n}D_if(\mathbf{a})(x_i-a_i)+\frac{1}{2!}\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_i)(x_j-a_j)+\cdots\\
&\cdots+\frac{1}{r!}\sum_{i_1,\ldots,i_r=1}^{n}D_{i_1,\ldots,i_r}f(\mathbf{a})(x_{i_1}-a_{i_1})\cdots(x_{i_r}-a_{i_r})\end{aligned}$$
s'anomena el polinomi de Taylor de grau $r$ de la funció $f$ en el punt $\mathbf{a}$,

(ii) El residu de grau $r$ de la funció $f$ en el punt $\mathbf{a}$ és
$$R_{r+1}(\mathbf{x})=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})(x_{i_1}-a_{i_1})\cdots(x_{i_{r+1}}-a_{i_{r+1}}).$$
A més, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$
Demostració: Construïm la següent funció $F(t)=f(h(t))$ a $\mathbb{R}$:
$$\begin{array}{ccccc}[0,1]\subset\mathbb{R}&\longrightarrow&\Omega\subseteq\mathbb{R}^n&\longrightarrow&\mathbb{R}\\ t&\longmapsto&\mathbf{a}+t(\mathbf{x}-\mathbf{a})&\longmapsto&f(\mathbf{a}+t(\mathbf{x}-\mathbf{a}))\end{array}$$
Observem que $F(1)=f(\mathbf{x})$ i $F(0)=f(\mathbf{a})$; d'altra banda, com que $f\in\mathcal{C}^{r+1}(\Omega)$ i $h$ és una funció lineal, $F(t)=f(h(t))$ és una funció de classe $r+1$ en algun obert $U$ tal que $[0,1]\subset U$. Si apliquem la fórmula de Taylor per a funcions d'una variable a $F(t)$, tenim que $F(t)=\sum_{k=0}^{r}\dfrac{F^{(k)}(0)}{k!}t^k+\dfrac{F^{(r+1)}(t_x)}{(r+1)!}t^{r+1}$, amb $t_x\in(0,t)$. Aplicant-la a $t=1$,
$$F(1)=\sum_{k=0}^{r}\frac{F^{(k)}(0)}{k!}+\frac{F^{(r+1)}(\tau)}{(r+1)!},\qquad\tau\in(0,1).$$
Ens basarem en aquest desenvolupament per a demostrar la fórmula de Taylor per al camp escalar $f$. D'entrada, doncs, caldrà calcular la funció $F$ i les seves derivades en $t=0$. Ja hem vist que $F(0)=f(\mathbf{a})$. Veurem que
$$F^{(k)}(t)=\sum_{i_1,\ldots,i_k=1}^{n}D_{i_1,\ldots,i_k}f(h(t))\,(x_{i_1}-a_{i_1})\ldots(x_{i_k}-a_{i_k}),\qquad\text{per a }k\leq r+1. \tag{3}$$
Fixem-nos que, per a $t=0$,
$$F^{(k)}(0)=\sum_{i_1,\ldots,i_k=1}^{n}D_{i_1,\ldots,i_k}f(\mathbf{a})\,(x_{i_1}-a_{i_1})\ldots(x_{i_k}-a_{i_k}),$$
que coincideix amb el terme d'ordre $k$ del polinomi $P_r$.

Per a $r=1$, clarament, per la regla de la cadena, es compleix la igualtat (3):
$$F'(t)=\sum_{i=1}^{n}D_if(h(t))\,h_i'(t)=\sum_{i=1}^{n}D_if(h(t))\,(x_i-a_i).$$
Suposem ara que la fórmula (3) és cert per a $k\leq m$ i demostrem que és certa per a $k=m+1$:
$$\begin{aligned}F^{(m+1)}(t)&=\frac{d}{dt}F^{(m)}(t)=\frac{d}{dt}\sum_{i_1,\ldots,i_m=1}^{n}D_{i_1,\ldots,i_m}f(h(t))\,(x_{i_1}-a_{i_1})\ldots(x_{i_m}-a_{i_m})\\
&=\sum_{j=1}^{n}D_j\left(\sum_{i_1,\ldots,i_m=1}^{n}D_{i_1,\ldots,i_m}f(h(t))\,(x_{i_1}-a_{i_1})\ldots(x_{i_m}-a_{i_m})\right)h_j'(t)\\
&=\sum_{i_1,\ldots,i_m=1}^{n}D_{i_1,\ldots,i_{m+1}}f(h(t))\,(x_{i_1}-a_{i_1})\ldots(x_{i_{m+1}}-a_{i_{m+1}}),\end{aligned}$$
prenent $j=i_{m+1}$. Per tant, hem demostrat (3) per inducció; aplicant-la fins a $k=r$, es demostra que $\sum_{k=0}^{r}\dfrac{F^{(k)}(0)}{k!}$ és exactament el polinomi $P_r(\mathbf{x})$ de l'enunciat.

Pel que fa al residu $R_{r+1}(\mathbf{x})$, atenent a la fórmula de Taylor de $F$,
$$R_{r+1}(\mathbf{x})=\frac{F^{(r+1)}(\tau)}{(r+1)!}=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(h(\tau))\,(x_{i_1}-a_{i_1})\ldots(x_{i_{r+1}}-a_{i_{r+1}}),$$
que, prenent $\xi_x=h(\tau)\in(\mathbf{a},\mathbf{x})$, coincideix amb la fórmula de l'enunciat.

Finalment,
$$\begin{aligned}\frac{|R_{r+1}(\mathbf{x})|}{\|\mathbf{x}-\mathbf{a}\|^r}&=\frac{1}{(r+1)!}\frac{1}{\|\mathbf{x}-\mathbf{a}\|^r}\left|\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})\,(x_{i_1}-a_{i_1})\ldots(x_{i_{r+1}}-a_{i_{r+1}})\right|\\
&\leq\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}\left|D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})\right|\frac{|x_{i_1}-a_{i_1}|}{\|\mathbf{x}-\mathbf{a}\|}\ldots\frac{|x_{i_r}-a_{i_r}|}{\|\mathbf{x}-\mathbf{a}\|}\,|x_{i_{r+1}}-a_{i_{r+1}}|.\end{aligned}$$
Analitzant els termes de la fórmula que hem obtingut, observem que:

- $\left|D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})\right|$ tendeix a $\left|D_{i_1,\ldots,i_{r+1}}f(\mathbf{a})\right|$ quan $\mathbf{x}$ tendeix a $\mathbf{a}$.
- Per a tot $i=1,\ldots,n$, $\dfrac{|x_i-a_i|}{\|\mathbf{x}-\mathbf{a}\|}\leq1$.
- El terme $|x_{i_{r+1}}-a_{i_{r+1}}|$ tendeix a $0$ quan $\mathbf{x}$ tendeix a $\mathbf{a}$.

Per tant,
$$\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(x)}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}$ de classe $\mathcal{C}^{r+1}(\Omega)$ i $\mathbf{a}\in\Omega$. Per a tot $\mathbf{x}\in\Omega$ amb $[\mathbf{a},\mathbf{x}]\subseteq\Omega$, existeix $\xi_\mathbf{x}\in(\mathbf{a},\mathbf{x})$ tal que $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$, on $P_r(\mathbf{x})=f(\mathbf{a})+\sum_{i=1}^{n}D_if(\mathbf{a})(x_i-a_i)+\cdots+\frac{1}{r!}\sum_{i_1,\ldots,i_r=1}^{n}D_{i_1,\ldots,i_r}f(\mathbf{a})(x_{i_1}-a_{i_1})\cdots(x_{i_r}-a_{i_r})$ és el polinomi de Taylor de grau $r$ de $f$ en $\mathbf{a}$.
[2] (enunciat) El residu és $R_{r+1}(\mathbf{x})=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})(x_{i_1}-a_{i_1})\cdots(x_{i_{r+1}}-a_{i_{r+1}})$.
[3] (enunciat) A més, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^{r+1}}=0$.
[4] (demostració) Sigui $h(t)=\mathbf{a}+t(\mathbf{x}-\mathbf{a})$ i $F(t)=f(h(t))$. Com que $[\mathbf{a},\mathbf{x}]\subseteq\Omega$ i $\Omega$ és obert, $F$ està definida i és de classe $\mathcal{C}^{r+1}$ en un obert $U\supseteq[0,1]$ (composició de $f$ amb $h$, que és afí), i $F(0)=f(\mathbf{a})$, $F(1)=f(\mathbf{x})$.
[5] (demostració) Per la fórmula de Taylor en una variable aplicada a $F$ en $[0,1]$, existeix $\tau\in(0,1)$ tal que $F(1)=\sum_{k=0}^{r}\frac{F^{(k)}(0)}{k!}+\frac{F^{(r+1)}(\tau)}{(r+1)!}$.
[6] (demostració) Veurem que, per a $k\leq r+1$, $F^{(k)}(t)=\sum_{i_1,\ldots,i_k=1}^{n}D_{i_1,\ldots,i_k}f(h(t))(x_{i_1}-a_{i_1})\cdots(x_{i_k}-a_{i_k})$ (3). Per a $k=1$ és la regla de la cadena: $F'(t)=\sum_{i=1}^{n}D_if(h(t))\,h_i'(t)=\sum_{i=1}^{n}D_if(h(t))\,x_i$, que és (3) per a $k=1$.
[7] (demostració) Si (3) és cert per a $k=m\leq r$, derivant amb la regla de la cadena cada terme $D_{i_1,\ldots,i_m}f(h(t))$ obtenim $\sum_{j=1}^{n}D_{i_1,\ldots,i_m,j}f(h(t))(x_j-a_j)$; prenent $j=i_{m+1}$, resulta (3) per a $k=m+1$. Per inducció, (3) val per a tot $k\leq r+1$.
[8] (demostració) En $t=0$, $\frac{F^{(k)}(0)}{k!}$ és exactament el terme d'ordre $k$ de $P_r$, de manera que $\sum_{k=0}^{r}\frac{F^{(k)}(0)}{k!}=P_r(\mathbf{x})$; i $\frac{F^{(r+1)}(\tau)}{(r+1)!}=R_{r+1}(\mathbf{x})$ prenent $\xi_\mathbf{x}=h(\tau)\in(\mathbf{a},\mathbf{x})$. Això demostra que $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$.
[9] (demostració) Finalment, si $B(\mathbf{a},\rho)\subseteq\Omega$, per a $\mathbf{x}\in B(\mathbf{a},\rho)$ el segment $[\mathbf{a},\mathbf{x}]$ és dins de $\Omega$ i, per la desigualtat triangular, $\frac{|R_{r+1}(\mathbf{x})|}{\|\mathbf{x}-\mathbf{a}\|^r}\leq\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}|D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})|\frac{|x_{i_1}-a_{i_1}|}{\|\mathbf{x}-\mathbf{a}\|}\cdots\frac{|x_{i_r}-a_{i_r}|}{\|\mathbf{x}-\mathbf{a}\|}|x_{i_{r+1}}-a_{i_{r+1}}|$.
[10] (demostració) Quan $\mathbf{x}\to\mathbf{a}$, $|D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})|\to|D_{i_1,\ldots,i_{r+1}}f(\mathbf{a})|$, perquè $\xi_\mathbf{x}\to\mathbf{a}$ i les derivades d'ordre $r+1$ de $f$ són contínues; cada quocient $\frac{|x_i-a_i|}{\|\mathbf{x}-\mathbf{a}\|}$ és $\leq1$, i $|x_{i_{r+1}}-a_{i_{r+1}}|\to0$. Per tant, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0$.


## T5.14:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.14] Teorema 14 (Tema 5) — Teorema de Taylor (diverses variables)
(de Taylor). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^{r+1}(\Omega)$, i $\mathbf{a}\in\Omega$. Per a tot $\mathbf{x}\in\Omega$ amb $[\mathbf{a},\mathbf{x}]\subseteq\Omega$, existeix $\xi_\mathbf{x}\in(\mathbf{a},\mathbf{x})$ tal que $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$, on

(i) El polinomi
$$\begin{aligned}P_r(\mathbf{x})={}&f(\mathbf{a})+\sum_{i=1}^{n}D_if(\mathbf{a})(x_i-a_i)+\frac{1}{2!}\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_i)(x_j-a_j)+\cdots\\
&\cdots+\frac{1}{r!}\sum_{i_1,\ldots,i_r=1}^{n}D_{i_1,\ldots,i_r}f(\mathbf{a})(x_{i_1}-a_{i_1})\cdots(x_{i_r}-a_{i_r})\end{aligned}$$
s'anomena el polinomi de Taylor de grau $r$ de la funció $f$ en el punt $\mathbf{a}$,

(ii) El residu de grau $r$ de la funció $f$ en el punt $\mathbf{a}$ és
$$R_{r+1}(\mathbf{x})=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})(x_{i_1}-a_{i_1})\cdots(x_{i_{r+1}}-a_{i_{r+1}}).$$
A més, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$
Demostració: Construïm la següent funció $F(t)=f(h(t))$ a $\mathbb{R}$:
$$\begin{array}{ccccc}[0,1]\subset\mathbb{R}&\longrightarrow&\Omega\subseteq\mathbb{R}^n&\longrightarrow&\mathbb{R}\\ t&\longmapsto&\mathbf{a}+t(\mathbf{x}-\mathbf{a})&\longmapsto&f(\mathbf{a}+t(\mathbf{x}-\mathbf{a}))\end{array}$$
Observem que $F(1)=f(\mathbf{x})$ i $F(0)=f(\mathbf{a})$; d'altra banda, com que $f\in\mathcal{C}^{r+1}(\Omega)$ i $h$ és una funció lineal, $F(t)=f(h(t))$ és una funció de classe $r+1$ en algun obert $U$ tal que $[0,1]\subset U$. Si apliquem la fórmula de Taylor per a funcions d'una variable a $F(t)$, tenim que $F(t)=\sum_{k=0}^{r}\dfrac{F^{(k)}(0)}{k!}t^k+\dfrac{F^{(r+1)}(t_x)}{(r+1)!}t^{r+1}$, amb $t_x\in(0,t)$. Aplicant-la a $t=1$,
$$F(1)=\sum_{k=0}^{r}\frac{F^{(k)}(0)}{k!}+\frac{F^{(r+1)}(\tau)}{(r+1)!},\qquad\tau\in(0,1).$$
Ens basarem en aquest desenvolupament per a demostrar la fórmula de Taylor per al camp escalar $f$. D'entrada, doncs, caldrà calcular la funció $F$ i les seves derivades en $t=0$. Ja hem vist que $F(0)=f(\mathbf{a})$. Veurem que
$$F^{(k)}(t)=\sum_{i_1,\ldots,i_k=1}^{n}D_{i_1,\ldots,i_k}f(h(t))\,(x_{i_1}-a_{i_1})\ldots(x_{i_k}-a_{i_k}),\qquad\text{per a }k\leq r+1. \tag{3}$$
Fixem-nos que, per a $t=0$,
$$F^{(k)}(0)=\sum_{i_1,\ldots,i_k=1}^{n}D_{i_1,\ldots,i_k}f(\mathbf{a})\,(x_{i_1}-a_{i_1})\ldots(x_{i_k}-a_{i_k}),$$
que coincideix amb el terme d'ordre $k$ del polinomi $P_r$.

Per a $r=1$, clarament, per la regla de la cadena, es compleix la igualtat (3):
$$F'(t)=\sum_{i=1}^{n}D_if(h(t))\,h_i'(t)=\sum_{i=1}^{n}D_if(h(t))\,(x_i-a_i).$$
Suposem ara que la fórmula (3) és cert per a $k\leq m$ i demostrem que és certa per a $k=m+1$:
$$\begin{aligned}F^{(m+1)}(t)&=\frac{d}{dt}F^{(m)}(t)=\frac{d}{dt}\sum_{i_1,\ldots,i_m=1}^{n}D_{i_1,\ldots,i_m}f(h(t))\,(x_{i_1}-a_{i_1})\ldots(x_{i_m}-a_{i_m})\\
&=\sum_{j=1}^{n}D_j\left(\sum_{i_1,\ldots,i_m=1}^{n}D_{i_1,\ldots,i_m}f(h(t))\,(x_{i_1}-a_{i_1})\ldots(x_{i_m}-a_{i_m})\right)h_j'(t)\\
&=\sum_{i_1,\ldots,i_m=1}^{n}D_{i_1,\ldots,i_{m+1}}f(h(t))\,(x_{i_1}-a_{i_1})\ldots(x_{i_{m+1}}-a_{i_{m+1}}),\end{aligned}$$
prenent $j=i_{m+1}$. Per tant, hem demostrat (3) per inducció; aplicant-la fins a $k=r$, es demostra que $\sum_{k=0}^{r}\dfrac{F^{(k)}(0)}{k!}$ és exactament el polinomi $P_r(\mathbf{x})$ de l'enunciat.

Pel que fa al residu $R_{r+1}(\mathbf{x})$, atenent a la fórmula de Taylor de $F$,
$$R_{r+1}(\mathbf{x})=\frac{F^{(r+1)}(\tau)}{(r+1)!}=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(h(\tau))\,(x_{i_1}-a_{i_1})\ldots(x_{i_{r+1}}-a_{i_{r+1}}),$$
que, prenent $\xi_x=h(\tau)\in(\mathbf{a},\mathbf{x})$, coincideix amb la fórmula de l'enunciat.

Finalment,
$$\begin{aligned}\frac{|R_{r+1}(\mathbf{x})|}{\|\mathbf{x}-\mathbf{a}\|^r}&=\frac{1}{(r+1)!}\frac{1}{\|\mathbf{x}-\mathbf{a}\|^r}\left|\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})\,(x_{i_1}-a_{i_1})\ldots(x_{i_{r+1}}-a_{i_{r+1}})\right|\\
&\leq\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}\left|D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})\right|\frac{|x_{i_1}-a_{i_1}|}{\|\mathbf{x}-\mathbf{a}\|}\ldots\frac{|x_{i_r}-a_{i_r}|}{\|\mathbf{x}-\mathbf{a}\|}\,|x_{i_{r+1}}-a_{i_{r+1}}|.\end{aligned}$$
Analitzant els termes de la fórmula que hem obtingut, observem que:

- $\left|D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})\right|$ tendeix a $\left|D_{i_1,\ldots,i_{r+1}}f(\mathbf{a})\right|$ quan $\mathbf{x}$ tendeix a $\mathbf{a}$.
- Per a tot $i=1,\ldots,n$, $\dfrac{|x_i-a_i|}{\|\mathbf{x}-\mathbf{a}\|}\leq1$.
- El terme $|x_{i_{r+1}}-a_{i_{r+1}}|$ tendeix a $0$ quan $\mathbf{x}$ tendeix a $\mathbf{a}$.

Per tant,
$$\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(x)}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}$ de classe $\mathcal{C}^{r+1}(\Omega)$ i $\mathbf{a}\in\Omega$. Per a tot $\mathbf{x}\in\Omega$ amb $[\mathbf{a},\mathbf{x}]\subseteq\Omega$, per a tot $\xi_\mathbf{x}\in(\mathbf{a},\mathbf{x})$ es té $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$, on $P_r(\mathbf{x})=f(\mathbf{a})+\sum_{i=1}^{n}D_if(\mathbf{a})(x_i-a_i)+\cdots+\frac{1}{r!}\sum_{i_1,\ldots,i_r=1}^{n}D_{i_1,\ldots,i_r}f(\mathbf{a})(x_{i_1}-a_{i_1})\cdots(x_{i_r}-a_{i_r})$ és el polinomi de Taylor de grau $r$ de $f$ en $\mathbf{a}$.
[2] (enunciat) El residu és $R_{r+1}(\mathbf{x})=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})(x_{i_1}-a_{i_1})\cdots(x_{i_{r+1}}-a_{i_{r+1}})$.
[3] (enunciat) A més, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0$.
[4] (demostració) Sigui $h(t)=\mathbf{a}+t(\mathbf{x}-\mathbf{a})$ i $F(t)=f(h(t))$. Com que $[\mathbf{a},\mathbf{x}]\subseteq\Omega$ i $\Omega$ és obert, $F$ està definida i és de classe $\mathcal{C}^{r+1}$ en un obert $U\supseteq[0,1]$ (composició de $f$ amb $h$, que és afí), i $F(0)=f(\mathbf{a})$, $F(1)=f(\mathbf{x})$.
[5] (demostració) Per la fórmula de Taylor en una variable aplicada a $F$ en $[0,1]$, existeix $\tau\in(0,1)$ tal que $F(1)=\sum_{k=0}^{r}\frac{F^{(k)}(0)}{k!}+\frac{F^{(r+1)}(\tau)}{(r+1)!}$.
[6] (demostració) Veurem que, per a $k\leq r+1$, $F^{(k)}(t)=\sum_{i_1,\ldots,i_k=1}^{n}D_{i_1,\ldots,i_k}f(h(t))(x_{i_1}-a_{i_1})\cdots(x_{i_k}-a_{i_k})$ (3). Per a $k=1$ és la regla de la cadena: $F'(t)=\sum_{i=1}^{n}D_if(h(t))\,h_i'(t)=\sum_{i=1}^{n}D_if(h(t))(x_i-a_i)$.
[7] (demostració) Si (3) és cert per a $k=m$, derivant amb la regla de la cadena cada terme $D_{i_1,\ldots,i_m}f(h(t))$ obtenim $\sum_{j=1}^{n}D_{i_1,\ldots,i_m,j}f(h(t))(x_j-a_j)$; prenent $j=i_{m+1}$, resulta (3) per a $k=m+1$. Per inducció, (3) val per a tot $k\in\mathbb{N}$.
[8] (demostració) En $t=0$, $\frac{F^{(k)}(0)}{k!}$ és exactament el terme d'ordre $k$ de $P_r$, de manera que $\sum_{k=0}^{r}\frac{F^{(k)}(0)}{k!}=P_r(\mathbf{x})$; i $\frac{F^{(r+1)}(\tau)}{(r+1)!}=R_{r+1}(\mathbf{x})$ prenent $\xi_\mathbf{x}=h(\tau)\in(\mathbf{a},\mathbf{x})$. Això demostra que $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$.
[9] (demostració) Finalment, si $B(\mathbf{a},\rho)\subseteq\Omega$, per a $\mathbf{x}\in B(\mathbf{a},\rho)$ el segment $[\mathbf{a},\mathbf{x}]$ és dins de $\Omega$ i, per la desigualtat triangular, $\frac{|R_{r+1}(\mathbf{x})|}{\|\mathbf{x}-\mathbf{a}\|^r}\leq\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}|D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})|\frac{|x_{i_1}-a_{i_1}|}{\|\mathbf{x}-\mathbf{a}\|}\cdots\frac{|x_{i_r}-a_{i_r}|}{\|\mathbf{x}-\mathbf{a}\|}|x_{i_{r+1}}-a_{i_{r+1}}|$.
[10] (demostració) Quan $\mathbf{x}\to\mathbf{a}$, $|D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})|\to|D_{i_1,\ldots,i_{r+1}}f(\mathbf{a})|$, perquè $\xi_\mathbf{x}\to\mathbf{a}$ i les derivades d'ordre $r$ de $f$ són contínues; cada quocient $\frac{|x_i-a_i|}{\|\mathbf{x}-\mathbf{a}\|}$ és $\leq1$, i $|x_{i_{r+1}}-a_{i_{r+1}}|\to0$. Per tant, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0$.


## T5.33:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.33] Teorema 33 (Tema 5) — Condicions suficients d'extrem
(condicions suficients). Sigui $\Omega\subseteq\mathbb{R}^n$ un obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$, i $\mathbf{a}\in\Omega$ un punt crític de $f$. Aleshores,

(i) $q_{Hf(\mathbf{a})}$ és definida positiva $\Rightarrow$ $\mathbf{a}$ és un mínim local estricte de $f$.

(ii) $q_{Hf(\mathbf{a})}$ és definida negativa $\Rightarrow$ $\mathbf{a}$ és un màxim local estricte de $f$.

(iii) $q_{Hf(\mathbf{a})}$ és indefinida $\Rightarrow$ $\mathbf{a}$ és un punt de sella de $f$.

(iv) $\mathbf{a}$ és un mínim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida positiva.

(v) $\mathbf{a}$ és un màxim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida negativa.
Demostració: (i) Pel corol·lari 15 i aplicant la condició de punt crític, sabem que
$$\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-f(\mathbf{a})-\frac12\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_j)(x_j-a_j)}{\|\mathbf{x}-\mathbf{a}\|^2}=0.$$
Apliquem la definició de límit. Per tant, per a tot $\epsilon>0$, existeix $\delta>0$ tal que si $\|\mathbf{x}-\mathbf{a}\|<\delta$ i $x\in\Omega\setminus\{\mathbf{a}\}$, aleshores
$$\frac{1}{\|\mathbf{x}-\mathbf{a}\|^2}\left|f(\mathbf{x})-f(\mathbf{a})-\frac12\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_i)(x_j-a_j)\right|<\epsilon.$$
Reescrivim-ho:
$$\left|\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}-\frac12\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})\frac{x_i-a_i}{\|\mathbf{x}-\mathbf{a}\|}\frac{x_j-a_j}{\|\mathbf{x}-\mathbf{a}\|}\right|<\epsilon,$$
és a dir,
$$-\epsilon+\frac12\left(\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}\right)^THf(\mathbf{a})\left(\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}\right)<\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}<\epsilon+\frac12\left(\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}\right)^THf(\mathbf{a})\left(\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}\right).$$
Pel lema 28, sabem que existeixen $c,C\geq0$ tals que
$$c\,\|\mathbf{u}\|^2\leq\mathbf{u}^T\,Hf(\mathbf{a})\,\mathbf{u}\leq C\,\|\mathbf{u}\|^2,\qquad\forall\mathbf{u}.$$
Com que $\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}$ té norma 1, de la darrera cadena de desigualtats, deduïm que
$$-\epsilon+\frac{c}{2}<\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}<\epsilon+\frac{C}{2},$$
o, equivalentment,
$$f(\mathbf{a})+\left(-\epsilon+\frac{c}{2}\right)\|\mathbf{x}-\mathbf{a}\|^2<f(\mathbf{x})<f(\mathbf{a})+\left(\epsilon+\frac{C}{2}\right)\|\mathbf{x}-\mathbf{a}\|^2,$$
Prenent $\epsilon<c/2$, s'obté que $f(\mathbf{x})>f(\mathbf{a})$ per a tot $\mathbf{x}\in B(\mathbf{a},\delta)\cap\Omega\setminus\{\mathbf{a}\}$.

(ii) Si $Hf(\mathbf{a})$ és definida negativa, considerem la funció $g=-f$. Evidentment, $\mathbf{a}$ és punt crític de $g$ i $Hg(\mathbf{a})$ és definida positiva. Aplicant l'apartat anterior, tenim que $\mathbf{a}$ és un mínim local estricte de $g$ i, per tant, és màxim local estricte de $f$.

(iii) Quan $Hf(\mathbf{a})$ és indefinida, per dir que és punt de sella, hem de saber distingir alguna direcció en què es prengui un màxim i alguna direcció en què es prengui un mínim. D'entrada, però, sabem que han d'existir direccions $\mathbf{u}$ i $\mathbf{v}$ tals que $\mathbf{u}^T\,Hf(\mathbf{a})\,\mathbf{u}>0$ i $\mathbf{v}^T\,Hf(\mathbf{a})\,\mathbf{v}<0$; a més, podem prendre, sense pèrdua de generalitat, $\|\mathbf{u}\|=\|\mathbf{v}\|=1$.

Prenem, per exemple, $\mathbf{u}$ i ens restringim en aquesta direcció del domini considerant $\mathbf{x}=\mathbf{a}+t\,\mathbf{u}$. Sabem que
$$\lim_{\mathbf{x}\to\mathbf{a}}\frac{1}{\|\mathbf{x}-\mathbf{a}\|^2}\left(f(\mathbf{x})-f(\mathbf{a})-\frac12(\mathbf{x}-\mathbf{a})^T\,Hf(\mathbf{a})\,(\mathbf{x}-\mathbf{a})\right)=0.$$
Per tant,
$$\lim_{t\to0}\frac{1}{t^2}\left(f(\mathbf{a}+t\,\mathbf{u})-f(a)-\frac12(t\mathbf{u})^T\,Hf(\mathbf{a})\,(t\mathbf{u})\right)=0,$$
que es pot reescriure com
$$\lim_{t\to0}\frac{f(\mathbf{a}+t\,\mathbf{u})-f(\mathbf{a})}{t^2}=\lim_{t\to0}\frac12\mathbf{u}^T\,Hf(\mathbf{a})\,\mathbf{u}>0.$$
Per tant, existeix un $\delta>0$ tal que si $|t|<\delta$, aleshores $f(\mathbf{a}+t\,\mathbf{u})>f(\mathbf{a})$. Així doncs, $\mathbf{a}$ és un mínim local restringit a la recta $\mathbf{x}=\mathbf{a}+t\,\mathbf{u}$.

Un raonament anàleg per al vector $\mathbf{v}$ ens diu que $\mathbf{a}$ és un màxim local restringit a la recta $\mathbf{x}=\mathbf{a}+t\,\mathbf{v}$.

(iv) Si $Hf(\mathbf{a})$ no fos semidefinida positiva, existiria un vector $\mathbf{v}$ tal que $\mathbf{v}^T\,Hf(\mathbf{a})\,\mathbf{v}<0$. Per l'apartat anterior, sabem que això implicaria que $\mathbf{a}$ és un màxim local restringit a la recta $\mathbf{x}=\mathbf{a}+t\,\mathbf{v}$, fet que contradeix la hipòtesi que $\mathbf{a}$ sigui un mínim local.

(v) Anàleg a (iv).

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $\Omega\subseteq\mathbb{R}^n$ un obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$ i $\mathbf{a}\in\Omega$ un punt crític de $f$. Aleshores: (i) si $q_{Hf(\mathbf{a})}$ és definida positiva, $\mathbf{a}$ és un mínim local estricte de $f$; (ii) si $q_{Hf(\mathbf{a})}$ és definida negativa, $\mathbf{a}$ és un màxim local estricte de $f$; (iii) si $q_{Hf(\mathbf{a})}$ és indefinida, $\mathbf{a}$ és un punt de sella de $f$.
[2] (enunciat) (iv) Si $q_{Hf(\mathbf{a})}$ és semidefinida positiva, $\mathbf{a}$ és un mínim local de $f$; (v) si $\mathbf{a}$ és un màxim local de $f$, $q_{Hf(\mathbf{a})}$ és semidefinida negativa.
[3] (demostració) (i) Pel corol·lari 15 amb $r=2$ i com que $Df(\mathbf{a})=0$ (punt crític), $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-f(\mathbf{a})-\frac12(\mathbf{x}-\mathbf{a})^THf(\mathbf{a})(\mathbf{x}-\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}=0$.
[4] (demostració) Per la definició de límit, per a tot $\epsilon>0$ existeix $\delta>0$ tal que, si $\mathbf{x}\in\Omega$ i $0<\|\mathbf{x}-\mathbf{a}\|<\delta$, aleshores, posant $\mathbf{u}_\mathbf{x}=\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}$, es té $\left|\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}-\frac12\mathbf{u}_\mathbf{x}^THf(\mathbf{a})\mathbf{u}_\mathbf{x}\right|<\epsilon$.
[5] (demostració) Pel lema 28, existeixen $0<c\leq C$ tals que $c\|\mathbf{u}\|^2\leq\mathbf{u}^THf(\mathbf{a})\mathbf{u}\leq C\|\mathbf{u}\|^2$ per a tot $\mathbf{u}$. Com que $\|\mathbf{u}_\mathbf{x}\|=1$, obtenim $-\epsilon+\frac c2<\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}<\epsilon+\frac C2$.
[6] (demostració) Prenent $\epsilon<c/2$, el membre de l'esquerra és positiu i, per tant, $f(\mathbf{x})>f(\mathbf{a})$ per a tot $\mathbf{x}\in B(\mathbf{a},\delta)\cap\Omega\setminus\{\mathbf{a}\}$: $\mathbf{a}$ és un mínim local estricte.
[7] (demostració) (ii) Si $Hf(\mathbf{a})$ és definida negativa, sigui $g=-f$: $\mathbf{a}$ és punt crític de $g$ i $Hg(\mathbf{a})=-Hf(\mathbf{a})$ és definida positiva. Per (i), $\mathbf{a}$ és un mínim local estricte de $g$, és a dir, un màxim local estricte de $f$.
[8] (demostració) (iii) Si $Hf(\mathbf{a})$ és indefinida, existeixen $\mathbf{u},\mathbf{v}$ de norma $1$ amb $\mathbf{u}^THf(\mathbf{a})\mathbf{u}>0$ i $\mathbf{v}^THf(\mathbf{a})\mathbf{v}<0$. Restringint el límit del principi de (i) a la recta $\mathbf{x}=\mathbf{a}+t\mathbf{u}$, on $\|\mathbf{x}-\mathbf{a}\|=|t|$, obtenim $\displaystyle\lim_{t\to0}\frac{f(\mathbf{a}+t\mathbf{u})-f(\mathbf{a})}{t^2}=\frac12\mathbf{u}^THf(\mathbf{a})\mathbf{u}>0$.
[9] (demostració) Per tant, existeix $\delta>0$ tal que $f(\mathbf{a}+t\mathbf{u})>f(\mathbf{a})$ si $0<|t|<\delta$: restringida a la recta $\mathbf{a}+t\mathbf{u}$, $f$ té un mínim local estricte en $\mathbf{a}$. Anàlogament, restringida a la recta $\mathbf{a}+t\mathbf{v}$, té un màxim local estricte en $\mathbf{a}$; així, $\mathbf{a}$ no és extrem local i és un punt de sella.
[10] (demostració) (iv) Si $Hf(\mathbf{a})$ no fos semidefinida positiva, existiria $\mathbf{v}$ amb $\mathbf{v}^THf(\mathbf{a})\mathbf{v}<0$. Pel raonament de (iii), $f(\mathbf{a}+t\mathbf{v})<f(\mathbf{a})$ per a $t\neq0$ prou petit, en contradicció amb que $\mathbf{a}$ sigui un mínim local. (v) És anàleg a (iv), aplicat a $-f$.


## T5.33:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.33] Teorema 33 (Tema 5) — Condicions suficients d'extrem
(condicions suficients). Sigui $\Omega\subseteq\mathbb{R}^n$ un obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$, i $\mathbf{a}\in\Omega$ un punt crític de $f$. Aleshores,

(i) $q_{Hf(\mathbf{a})}$ és definida positiva $\Rightarrow$ $\mathbf{a}$ és un mínim local estricte de $f$.

(ii) $q_{Hf(\mathbf{a})}$ és definida negativa $\Rightarrow$ $\mathbf{a}$ és un màxim local estricte de $f$.

(iii) $q_{Hf(\mathbf{a})}$ és indefinida $\Rightarrow$ $\mathbf{a}$ és un punt de sella de $f$.

(iv) $\mathbf{a}$ és un mínim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida positiva.

(v) $\mathbf{a}$ és un màxim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida negativa.
Demostració: (i) Pel corol·lari 15 i aplicant la condició de punt crític, sabem que
$$\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-f(\mathbf{a})-\frac12\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_j)(x_j-a_j)}{\|\mathbf{x}-\mathbf{a}\|^2}=0.$$
Apliquem la definició de límit. Per tant, per a tot $\epsilon>0$, existeix $\delta>0$ tal que si $\|\mathbf{x}-\mathbf{a}\|<\delta$ i $x\in\Omega\setminus\{\mathbf{a}\}$, aleshores
$$\frac{1}{\|\mathbf{x}-\mathbf{a}\|^2}\left|f(\mathbf{x})-f(\mathbf{a})-\frac12\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_i)(x_j-a_j)\right|<\epsilon.$$
Reescrivim-ho:
$$\left|\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}-\frac12\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})\frac{x_i-a_i}{\|\mathbf{x}-\mathbf{a}\|}\frac{x_j-a_j}{\|\mathbf{x}-\mathbf{a}\|}\right|<\epsilon,$$
és a dir,
$$-\epsilon+\frac12\left(\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}\right)^THf(\mathbf{a})\left(\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}\right)<\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}<\epsilon+\frac12\left(\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}\right)^THf(\mathbf{a})\left(\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}\right).$$
Pel lema 28, sabem que existeixen $c,C\geq0$ tals que
$$c\,\|\mathbf{u}\|^2\leq\mathbf{u}^T\,Hf(\mathbf{a})\,\mathbf{u}\leq C\,\|\mathbf{u}\|^2,\qquad\forall\mathbf{u}.$$
Com que $\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}$ té norma 1, de la darrera cadena de desigualtats, deduïm que
$$-\epsilon+\frac{c}{2}<\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}<\epsilon+\frac{C}{2},$$
o, equivalentment,
$$f(\mathbf{a})+\left(-\epsilon+\frac{c}{2}\right)\|\mathbf{x}-\mathbf{a}\|^2<f(\mathbf{x})<f(\mathbf{a})+\left(\epsilon+\frac{C}{2}\right)\|\mathbf{x}-\mathbf{a}\|^2,$$
Prenent $\epsilon<c/2$, s'obté que $f(\mathbf{x})>f(\mathbf{a})$ per a tot $\mathbf{x}\in B(\mathbf{a},\delta)\cap\Omega\setminus\{\mathbf{a}\}$.

(ii) Si $Hf(\mathbf{a})$ és definida negativa, considerem la funció $g=-f$. Evidentment, $\mathbf{a}$ és punt crític de $g$ i $Hg(\mathbf{a})$ és definida positiva. Aplicant l'apartat anterior, tenim que $\mathbf{a}$ és un mínim local estricte de $g$ i, per tant, és màxim local estricte de $f$.

(iii) Quan $Hf(\mathbf{a})$ és indefinida, per dir que és punt de sella, hem de saber distingir alguna direcció en què es prengui un màxim i alguna direcció en què es prengui un mínim. D'entrada, però, sabem que han d'existir direccions $\mathbf{u}$ i $\mathbf{v}$ tals que $\mathbf{u}^T\,Hf(\mathbf{a})\,\mathbf{u}>0$ i $\mathbf{v}^T\,Hf(\mathbf{a})\,\mathbf{v}<0$; a més, podem prendre, sense pèrdua de generalitat, $\|\mathbf{u}\|=\|\mathbf{v}\|=1$.

Prenem, per exemple, $\mathbf{u}$ i ens restringim en aquesta direcció del domini considerant $\mathbf{x}=\mathbf{a}+t\,\mathbf{u}$. Sabem que
$$\lim_{\mathbf{x}\to\mathbf{a}}\frac{1}{\|\mathbf{x}-\mathbf{a}\|^2}\left(f(\mathbf{x})-f(\mathbf{a})-\frac12(\mathbf{x}-\mathbf{a})^T\,Hf(\mathbf{a})\,(\mathbf{x}-\mathbf{a})\right)=0.$$
Per tant,
$$\lim_{t\to0}\frac{1}{t^2}\left(f(\mathbf{a}+t\,\mathbf{u})-f(a)-\frac12(t\mathbf{u})^T\,Hf(\mathbf{a})\,(t\mathbf{u})\right)=0,$$
que es pot reescriure com
$$\lim_{t\to0}\frac{f(\mathbf{a}+t\,\mathbf{u})-f(\mathbf{a})}{t^2}=\lim_{t\to0}\frac12\mathbf{u}^T\,Hf(\mathbf{a})\,\mathbf{u}>0.$$
Per tant, existeix un $\delta>0$ tal que si $|t|<\delta$, aleshores $f(\mathbf{a}+t\,\mathbf{u})>f(\mathbf{a})$. Així doncs, $\mathbf{a}$ és un mínim local restringit a la recta $\mathbf{x}=\mathbf{a}+t\,\mathbf{u}$.

Un raonament anàleg per al vector $\mathbf{v}$ ens diu que $\mathbf{a}$ és un màxim local restringit a la recta $\mathbf{x}=\mathbf{a}+t\,\mathbf{v}$.

(iv) Si $Hf(\mathbf{a})$ no fos semidefinida positiva, existiria un vector $\mathbf{v}$ tal que $\mathbf{v}^T\,Hf(\mathbf{a})\,\mathbf{v}<0$. Per l'apartat anterior, sabem que això implicaria que $\mathbf{a}$ és un màxim local restringit a la recta $\mathbf{x}=\mathbf{a}+t\,\mathbf{v}$, fet que contradeix la hipòtesi que $\mathbf{a}$ sigui un mínim local.

(v) Anàleg a (iv).

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $\Omega\subseteq\mathbb{R}^n$ un obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$ i $\mathbf{a}\in\Omega$ un punt crític de $f$. Aleshores: (i) si $q_{Hf(\mathbf{a})}$ és definida positiva, $\mathbf{a}$ és un mínim absolut estricte de $f$ en $\Omega$; (ii) si $q_{Hf(\mathbf{a})}$ és definida negativa, $\mathbf{a}$ és un màxim local estricte de $f$; (iii) si $q_{Hf(\mathbf{a})}$ és indefinida, $\mathbf{a}$ és un punt de sella de $f$.
[2] (enunciat) (iv) Si $\mathbf{a}$ és un mínim local de $f$, $q_{Hf(\mathbf{a})}$ és semidefinida positiva; (v) si $\mathbf{a}$ és un màxim local de $f$, $q_{Hf(\mathbf{a})}$ és semidefinida negativa.
[3] (demostració) (i) Pel corol·lari 15 amb $r=2$ i com que $Df(\mathbf{a})=0$ (punt crític), $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-f(\mathbf{a})-\frac12(\mathbf{x}-\mathbf{a})^THf(\mathbf{a})(\mathbf{x}-\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}=0$.
[4] (demostració) Per la definició de límit, per a tot $\epsilon>0$ existeix $\delta>0$ tal que, si $\mathbf{x}\in\Omega$ i $0<\|\mathbf{x}-\mathbf{a}\|<\delta$, aleshores, posant $\mathbf{u}_\mathbf{x}=\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}$, es té $\left|\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}-\frac12\mathbf{u}_\mathbf{x}^THf(\mathbf{a})\mathbf{u}_\mathbf{x}\right|<\epsilon$.
[5] (demostració) Pel lema 28, existeixen $0<c\leq C$ tals que $c\|\mathbf{u}\|^2\leq\mathbf{u}^THf(\mathbf{a})\mathbf{u}\leq C\|\mathbf{u}\|^2$ per a tot $\mathbf{u}$. Com que $\|\mathbf{u}_\mathbf{x}\|=1$, obtenim $-\epsilon+\frac c2<\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}<\epsilon+\frac C2$.
[6] (demostració) Prenent $\epsilon<C/2$, el membre de l'esquerra és positiu i, per tant, $f(\mathbf{x})>f(\mathbf{a})$ per a tot $\mathbf{x}\in B(\mathbf{a},\delta)\cap\Omega\setminus\{\mathbf{a}\}$: $\mathbf{a}$ és un mínim local estricte.
[7] (demostració) (ii) Si $Hf(\mathbf{a})$ és definida negativa, sigui $g=-f$: $\mathbf{a}$ és punt crític de $g$ i $Hg(\mathbf{a})=-Hf(\mathbf{a})$ és definida positiva. Per (i), $\mathbf{a}$ és un mínim local estricte de $g$, és a dir, un màxim local estricte de $f$.
[8] (demostració) (iii) Si $Hf(\mathbf{a})$ és indefinida, existeixen $\mathbf{u},\mathbf{v}$ de norma $1$ amb $\mathbf{u}^THf(\mathbf{a})\mathbf{u}>0$ i $\mathbf{v}^THf(\mathbf{a})\mathbf{v}<0$. Restringint el límit del principi de (i) a la recta $\mathbf{x}=\mathbf{a}+t\mathbf{u}$, on $\|\mathbf{x}-\mathbf{a}\|=|t|$, obtenim $\displaystyle\lim_{t\to0}\frac{f(\mathbf{a}+t\mathbf{u})-f(\mathbf{a})}{t^2}=\frac12\mathbf{u}^THf(\mathbf{a})\mathbf{u}>0$.
[9] (demostració) Per tant, existeix $\delta>0$ tal que $f(\mathbf{a}+t\mathbf{u})>f(\mathbf{a})$ si $0<|t|<\delta$: restringida a la recta $\mathbf{a}+t\mathbf{u}$, $f$ té un mínim local estricte en $\mathbf{a}$. Anàlogament, restringida a la recta $\mathbf{a}+t\mathbf{v}$, té un màxim local estricte en $\mathbf{a}$; així, $\mathbf{a}$ no és extrem local i és un punt de sella.
[10] (demostració) (iv) Si $Hf(\mathbf{a})$ no fos semidefinida positiva, existiria $\mathbf{v}$ amb $\mathbf{v}^THf(\mathbf{a})\mathbf{v}<0$. Pel raonament de (iii), $f(\mathbf{a}+t\mathbf{v})<f(\mathbf{a})$ per a $t\neq0$ prou petit, en contradicció amb que $\mathbf{a}$ sigui un mínim local. (v) És anàleg a (iv), aplicat a $-f$.


## T5.33:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T5.33] Teorema 33 (Tema 5) — Condicions suficients d'extrem
(condicions suficients). Sigui $\Omega\subseteq\mathbb{R}^n$ un obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$, i $\mathbf{a}\in\Omega$ un punt crític de $f$. Aleshores,

(i) $q_{Hf(\mathbf{a})}$ és definida positiva $\Rightarrow$ $\mathbf{a}$ és un mínim local estricte de $f$.

(ii) $q_{Hf(\mathbf{a})}$ és definida negativa $\Rightarrow$ $\mathbf{a}$ és un màxim local estricte de $f$.

(iii) $q_{Hf(\mathbf{a})}$ és indefinida $\Rightarrow$ $\mathbf{a}$ és un punt de sella de $f$.

(iv) $\mathbf{a}$ és un mínim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida positiva.

(v) $\mathbf{a}$ és un màxim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida negativa.
Demostració: (i) Pel corol·lari 15 i aplicant la condició de punt crític, sabem que
$$\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-f(\mathbf{a})-\frac12\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_j)(x_j-a_j)}{\|\mathbf{x}-\mathbf{a}\|^2}=0.$$
Apliquem la definició de límit. Per tant, per a tot $\epsilon>0$, existeix $\delta>0$ tal que si $\|\mathbf{x}-\mathbf{a}\|<\delta$ i $x\in\Omega\setminus\{\mathbf{a}\}$, aleshores
$$\frac{1}{\|\mathbf{x}-\mathbf{a}\|^2}\left|f(\mathbf{x})-f(\mathbf{a})-\frac12\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_i)(x_j-a_j)\right|<\epsilon.$$
Reescrivim-ho:
$$\left|\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}-\frac12\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})\frac{x_i-a_i}{\|\mathbf{x}-\mathbf{a}\|}\frac{x_j-a_j}{\|\mathbf{x}-\mathbf{a}\|}\right|<\epsilon,$$
és a dir,
$$-\epsilon+\frac12\left(\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}\right)^THf(\mathbf{a})\left(\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}\right)<\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}<\epsilon+\frac12\left(\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}\right)^THf(\mathbf{a})\left(\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}\right).$$
Pel lema 28, sabem que existeixen $c,C\geq0$ tals que
$$c\,\|\mathbf{u}\|^2\leq\mathbf{u}^T\,Hf(\mathbf{a})\,\mathbf{u}\leq C\,\|\mathbf{u}\|^2,\qquad\forall\mathbf{u}.$$
Com que $\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}$ té norma 1, de la darrera cadena de desigualtats, deduïm que
$$-\epsilon+\frac{c}{2}<\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}<\epsilon+\frac{C}{2},$$
o, equivalentment,
$$f(\mathbf{a})+\left(-\epsilon+\frac{c}{2}\right)\|\mathbf{x}-\mathbf{a}\|^2<f(\mathbf{x})<f(\mathbf{a})+\left(\epsilon+\frac{C}{2}\right)\|\mathbf{x}-\mathbf{a}\|^2,$$
Prenent $\epsilon<c/2$, s'obté que $f(\mathbf{x})>f(\mathbf{a})$ per a tot $\mathbf{x}\in B(\mathbf{a},\delta)\cap\Omega\setminus\{\mathbf{a}\}$.

(ii) Si $Hf(\mathbf{a})$ és definida negativa, considerem la funció $g=-f$. Evidentment, $\mathbf{a}$ és punt crític de $g$ i $Hg(\mathbf{a})$ és definida positiva. Aplicant l'apartat anterior, tenim que $\mathbf{a}$ és un mínim local estricte de $g$ i, per tant, és màxim local estricte de $f$.

(iii) Quan $Hf(\mathbf{a})$ és indefinida, per dir que és punt de sella, hem de saber distingir alguna direcció en què es prengui un màxim i alguna direcció en què es prengui un mínim. D'entrada, però, sabem que han d'existir direccions $\mathbf{u}$ i $\mathbf{v}$ tals que $\mathbf{u}^T\,Hf(\mathbf{a})\,\mathbf{u}>0$ i $\mathbf{v}^T\,Hf(\mathbf{a})\,\mathbf{v}<0$; a més, podem prendre, sense pèrdua de generalitat, $\|\mathbf{u}\|=\|\mathbf{v}\|=1$.

Prenem, per exemple, $\mathbf{u}$ i ens restringim en aquesta direcció del domini considerant $\mathbf{x}=\mathbf{a}+t\,\mathbf{u}$. Sabem que
$$\lim_{\mathbf{x}\to\mathbf{a}}\frac{1}{\|\mathbf{x}-\mathbf{a}\|^2}\left(f(\mathbf{x})-f(\mathbf{a})-\frac12(\mathbf{x}-\mathbf{a})^T\,Hf(\mathbf{a})\,(\mathbf{x}-\mathbf{a})\right)=0.$$
Per tant,
$$\lim_{t\to0}\frac{1}{t^2}\left(f(\mathbf{a}+t\,\mathbf{u})-f(a)-\frac12(t\mathbf{u})^T\,Hf(\mathbf{a})\,(t\mathbf{u})\right)=0,$$
que es pot reescriure com
$$\lim_{t\to0}\frac{f(\mathbf{a}+t\,\mathbf{u})-f(\mathbf{a})}{t^2}=\lim_{t\to0}\frac12\mathbf{u}^T\,Hf(\mathbf{a})\,\mathbf{u}>0.$$
Per tant, existeix un $\delta>0$ tal que si $|t|<\delta$, aleshores $f(\mathbf{a}+t\,\mathbf{u})>f(\mathbf{a})$. Així doncs, $\mathbf{a}$ és un mínim local restringit a la recta $\mathbf{x}=\mathbf{a}+t\,\mathbf{u}$.

Un raonament anàleg per al vector $\mathbf{v}$ ens diu que $\mathbf{a}$ és un màxim local restringit a la recta $\mathbf{x}=\mathbf{a}+t\,\mathbf{v}$.

(iv) Si $Hf(\mathbf{a})$ no fos semidefinida positiva, existiria un vector $\mathbf{v}$ tal que $\mathbf{v}^T\,Hf(\mathbf{a})\,\mathbf{v}<0$. Per l'apartat anterior, sabem que això implicaria que $\mathbf{a}$ és un màxim local restringit a la recta $\mathbf{x}=\mathbf{a}+t\,\mathbf{v}$, fet que contradeix la hipòtesi que $\mathbf{a}$ sigui un mínim local.

(v) Anàleg a (iv).

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $\Omega\subseteq\mathbb{R}^n$ un obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$ i $\mathbf{a}\in\Omega$ un punt crític de $f$. Aleshores: (i) si $q_{Hf(\mathbf{a})}$ és definida positiva, $\mathbf{a}$ és un mínim local estricte de $f$; (ii) si $q_{Hf(\mathbf{a})}$ és definida negativa, $\mathbf{a}$ és un màxim local estricte de $f$; (iii) si $q_{Hf(\mathbf{a})}$ és indefinida, $\mathbf{a}$ és un punt de sella de $f$.
[2] (enunciat) (iv) Si $\mathbf{a}$ és un mínim local estricte de $f$, $q_{Hf(\mathbf{a})}$ és definida positiva; (v) si $\mathbf{a}$ és un màxim local de $f$, $q_{Hf(\mathbf{a})}$ és semidefinida negativa.
[3] (demostració) (i) Pel teorema de Taylor (teorema 14) amb $r=2$ i com que $Df(\mathbf{a})=0$ (punt crític), $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-f(\mathbf{a})-\frac12(\mathbf{x}-\mathbf{a})^THf(\mathbf{a})(\mathbf{x}-\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}=0$.
[4] (demostració) Per la definició de límit, per a tot $\epsilon>0$ existeix $\delta>0$ tal que, si $\mathbf{x}\in\Omega$ i $0<\|\mathbf{x}-\mathbf{a}\|<\delta$, aleshores, posant $\mathbf{u}_\mathbf{x}=\frac{\mathbf{x}-\mathbf{a}}{\|\mathbf{x}-\mathbf{a}\|}$, es té $\left|\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}-\frac12\mathbf{u}_\mathbf{x}^THf(\mathbf{a})\mathbf{u}_\mathbf{x}\right|<\epsilon$.
[5] (demostració) Pel lema 28, existeixen $0<c\leq C$ tals que $c\|\mathbf{u}\|^2\leq\mathbf{u}^THf(\mathbf{a})\mathbf{u}\leq C\|\mathbf{u}\|^2$ per a tot $\mathbf{u}$. Com que $\|\mathbf{u}_\mathbf{x}\|=1$, obtenim $-\epsilon+\frac c2<\frac{f(\mathbf{x})-f(\mathbf{a})}{\|\mathbf{x}-\mathbf{a}\|^2}<\epsilon+\frac C2$.
[6] (demostració) Prenent $\epsilon<c/2$, el membre de l'esquerra és positiu i, per tant, $f(\mathbf{x})>f(\mathbf{a})$ per a tot $\mathbf{x}\in B(\mathbf{a},\delta)\cap\Omega\setminus\{\mathbf{a}\}$: $\mathbf{a}$ és un mínim local estricte.
[7] (demostració) (ii) Si $Hf(\mathbf{a})$ és definida negativa, sigui $g=-f$: $\mathbf{a}$ és punt crític de $g$ i $Hg(\mathbf{a})=-Hf(\mathbf{a})$ és definida positiva. Per (i), $\mathbf{a}$ és un mínim local estricte de $g$, és a dir, un màxim local estricte de $f$.
[8] (demostració) (iii) Si $Hf(\mathbf{a})$ és indefinida, existeixen $\mathbf{u},\mathbf{v}$ de norma $1$ amb $\mathbf{u}^THf(\mathbf{a})\mathbf{u}>0$ i $\mathbf{v}^THf(\mathbf{a})\mathbf{v}<0$. Restringint el límit del principi de (i) a la recta $\mathbf{x}=\mathbf{a}+t\mathbf{u}$, on $\|\mathbf{x}-\mathbf{a}\|=|t|$, obtenim $\displaystyle\lim_{t\to0}\frac{f(\mathbf{a}+t\mathbf{u})-f(\mathbf{a})}{t^2}=\frac12\mathbf{u}^THf(\mathbf{a})\mathbf{u}>0$.
[9] (demostració) Per tant, existeix $\delta>0$ tal que $f(\mathbf{a}+t\mathbf{u})>f(\mathbf{a})$ si $0<|t|<\delta$: restringida a la recta $\mathbf{a}+t\mathbf{u}$, $f$ té un mínim local estricte en $\mathbf{a}$. Anàlogament, restringida a la recta $\mathbf{a}+t\mathbf{v}$, té un màxim local estricte en $\mathbf{a}$; així, $\mathbf{a}$ no és extrem local i és un punt de sella.
[10] (demostració) (iv) Si $Hf(\mathbf{a})$ no fos semidefinida positiva, per a tot $\mathbf{v}\neq\mathbf{0}$ tindríem $\mathbf{v}^THf(\mathbf{a})\mathbf{v}<0$. Pel raonament de (iii), $f(\mathbf{a}+t\mathbf{v})<f(\mathbf{a})$ per a $t\neq0$ prou petit, en contradicció amb que $\mathbf{a}$ sigui un mínim local. (v) És anàleg a (iv), aplicat a $-f$.

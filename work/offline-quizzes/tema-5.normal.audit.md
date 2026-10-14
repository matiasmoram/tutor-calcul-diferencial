# audit

## Instructions

Ets un revisor exigent de Càlcul Diferencial. Revises les solucions d'un qüestionari "Cert o fals" abans que el vegin els alumnes.
Per a cada afirmació comprova:
- "resolucio_correcta": la resolució és matemàticament correcta i completa (cada desigualtat, cada límit, cada hipòtesi). Per a una falsa, el contraexemple compleix TOTES les hipòtesis de l'afirmació i NO la conclusió. Per a una certa, la demostració no té forats.
- "teoria_correcta": els ítems citats existeixen als apunts i s'apliquen amb les seves hipòtesis (true si no se'n cita cap).
- "pista_neutra": la pista no revela el veredicte ni el contraexemple.
- "problemes": si algun dels anteriors és fals, explica exactament què falla; altrament "".
No inventis errors: una redacció millorable no és un error.

## Notes

<apunts tema="5" titol="Fórmula de Taylor, extrems locals">
[T5.1] Definició 1 (Tema 5) — Derivades parcials r-èsimes
Denotem les derivades parcials $r$-èsimes com $\dfrac{\partial^r f}{\partial x_{i_1}\cdots\partial x_{i_r}}(p)$. També farem servir la notació abreujada $D_{i_r}\ldots D_{i_1}f$ o $D_{i_1\cdots i_r}f$, i la notació $f_{i_1\ldots i_r}$. Fixem-nos que l'ordre dels subíndexos canvia segons la notació.

[T5.2] Observació 2 (Tema 5) — Diferencial d'ordre r
(Explicació.) Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ diferenciable en tot $\Omega$. Interpretem la diferencial com una aplicació $Df:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^{nm}$. Anàlogament, la diferencial d'ordre $r$ de $f$ és una aplicació $D^rf:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^{n^r m}$ (si existeix).

[T5.3] Definició 3 (Tema 5) — Funció de classe C^r
Direm que una funció $f:\Omega\subset\mathbb{R}^n\to\mathbb{R}^m$ és de classe $\mathcal{C}^r$ si totes les derivades fins a ordre $r$ existeixen i són contínues.

Equivalentment, $f:\Omega\subset\mathbb{R}^n\to\mathbb{R}^m$ és de classe $\mathcal{C}^r\Leftrightarrow Df$ és de classe $\mathcal{C}^{r-1}$.

[T5.4] Exemple 4 (Tema 5) — Derivades segones d'una funció de R^3
Calculem les derivades d'ordre 2 de la funció $f:\mathbb{R}^3\longrightarrow\mathbb{R}$ donada per
$$f(x,y,z)=(1+x^2+2y^2)e^z.$$
$$\frac{\partial f}{\partial x}=2x\,e^z,\quad \frac{\partial f}{\partial y}=4y\,e^z,\quad \frac{\partial f}{\partial z}=(1+x^2+2y^2)\,e^z.$$
$$\begin{aligned}
&\frac{\partial^2 f}{\partial x^2}=f_{xx}=2\,e^z, & \frac{\partial^2 f}{\partial x\partial y}=f_{xy}=0, & & \frac{\partial^2 f}{\partial x\partial z}=f_{xz}=2x\,e^z;\\
&\frac{\partial^2 f}{\partial y\partial x}=f_{yx}=0, & \frac{\partial^2 f}{\partial y^2}=f_{yy}=4\,e^z, & & \frac{\partial^2 f}{\partial y\partial z}=f_{yz}=4y\,e^z;\\
&\frac{\partial^2 f}{\partial z\partial x}=f_{zx}=2x\,e^z, & \frac{\partial^2 f}{\partial z\partial y}=f_{zy}=4y\,e^z, & & \frac{\partial^2 f}{\partial z^2}=f_{zz}=(1+x^2+2y^2)\,e^z.
\end{aligned}$$

[T5.x1] Apunts del Tema 5, §5.2 — Motivació del teorema de Schwarz
Un resultat fonamental de derivades parcials $r$-èsimes posa en relació les derivades creuades. Per motivar-lo, vegem primer aquest exemple.

[T5.5] Exemple 5 (Tema 5) — Derivades creuades diferents
Hi ha funcions $f:\Omega\subset\mathbb{R}^2\to\mathbb{R}$ i $p\in\Omega$ tals que $\dfrac{\partial^2 f}{\partial y\partial x}(p)\neq\dfrac{\partial f}{\partial x\partial y}(p)$.

Considerem la següent funció $f:\mathbb{R}^2\longrightarrow\mathbb{R}$:
$$f(x,y)=\begin{cases}\dfrac{xy(x^2-y^2)}{x^2+y^2} & \text{si } (x,y)\neq(0,0),\\[2mm] 0 & \text{si } (x,y)=(0,0).\end{cases}$$

[T5.6] Teorema 6 (Tema 5) — Teorema de Schwarz
(Schwarz). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$ i $D_iD_jf$ i $D_jD_if$ existeixen en $\Omega$. Si $D_iD_jf$ i $D_jD_if$ són contínues en un entorn d'$\mathbf{a}\in\Omega$, aleshores
$$D_iD_jf(\mathbf{a})=D_jD_if(\mathbf{a}).$$

[T5.x2] Apunts del Tema 5, §5.2 — Versió més forta de Schwarz
Modificant el raonament anterior, es pot demostrar una versió més forta del teorema:

[T5.7] Teorema 7 (Tema 5) — Schwarz, versió forta
(Schwarz, versió forta). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$ i $D_jD_if$ existeixen en $\Omega$. Si, a més, $D_jD_if$ és contínua en $\Omega$, aleshores $D_iD_jf(\mathbf{a})$ també existeix i $D_iD_jf(\mathbf{a})=D_jD_if(\mathbf{a})$.

[T5.8] Teorema 8 (Tema 5) — Teorema de Taylor (una variable)
(de Taylor). Sigui $\Omega\subseteq\mathbb{R}$ obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^{r+1}(\Omega)$, i $a\in\Omega$. Per a tot $x\in\Omega$ amb $[a,x]\subseteq\Omega$ (Nota: Fem servir la notació d'intervals a $\mathbb{R}^n$ introduïda al tema 3, de manera que, a $\mathbb{R}$, $[a,x]$ pot ser tant $[a,x]$, si $x\geq a$, com $[x,a]$, si $x\leq a$.), existeix $\xi_x\in(a,x)$ tal que $f(x)=P_r(x)+R_{r+1}(x)$, on

(i) $P_r(x)=f(a)+f'(a)(x-a)+\dfrac{1}{2!}f''(a)(x-a)^2+\cdots+\dfrac{1}{r!}f^{(r)}(a)(x-a)^r$ s'anomena el polinomi de Taylor de grau $r$ de la funció $f$ en el punt $a$, i

(ii) $R_{r+1}(x)=\dfrac{1}{(r+1)!}f^{(r+1)}(\xi_x)(x-a)^{r+1}$ s'anomena el residu de grau $r$ de la funció $f$ en el punt $a$. A més,
$$\lim_{x\to a}\frac{R_{r+1}(x)}{(x-a)^r}=0.$$

[T5.x3] Apunts del Tema 5, §5.3 — Interpretació i unicitat del polinomi de Taylor
Una interpretació alternativa del rol de polinomi de Taylor és que $P_r(x)$ interpola els valors de $f(a),f'(a),\ldots,f^{(n)}(a)$, de manera que és una bona aproximació de la funció $f$ en un entorn del punt $a$.

Una conseqüència de la propietat $\lim_{x\to a}\frac{f(x)-P_r(x)}{(x-a)^r}=0$ és que el polinomi $P_r(x)$ és l'únic polinomi de grau menor o igual que $r$ que la compleix. En efecte, si existís un polinomi de grau menor o igual que $r$, $Q_r(x)=\sum_{i=0}^r q_i\,(x-a)^i$ tal que $\lim_{x\to a}\frac{f(x)-Q_r(x)}{(x-a)^r}=0$, aleshores
$$\lim_{x\to a}\frac{f(x)-P_r(x)}{(x-a)^r}=\lim_{x\to a}\frac{f(x)-Q_r(x)}{(x-a)^r}=0,$$
és a dir,
$$\lim_{x\to a}\frac{P_r(x)-Q_r(x)}{(x-a)^r}=0,$$
i, per tant, caldria que $P_r(x)-Q_r(x)=\sum_{i>r}\alpha_i\,(x-a)^i$ per a $\alpha_i\in\mathbb{R}$, fet que contradiu les hipòtesis de sortida, o bé que $P_r(x)\equiv Q_r(x)$.

[T5.9] Definició 9 (Tema 5) — Extrems locals (una variable)
Sigui $\Omega\subseteq\mathbb{R}$ obert i $f:\Omega\to\mathbb{R}$ una funció. Diem que un punt $a\in\Omega$ és un

(i) màxim local de $f$ si $\exists\,\epsilon>0$ t.q. $\forall x\in(a-\epsilon,a+\epsilon)\subseteq\Omega$, $f(x)\leqslant f(a)$;

(ii) mínim local de $f$ si $\exists\,\epsilon>0$ t.q. $\forall x\in(a-\epsilon,a+\epsilon)\subseteq\Omega$, $f(x)\geqslant f(a)$;

(iii) màxim local estricte de $f$ si $\exists\,\epsilon>0\ \forall\, a\neq x\in(a-\epsilon,a+\epsilon)\subseteq\Omega$, $f(x)<f(a)$;

(iv) mínim local estricte de $f$ si $\exists\,\epsilon>0\ \forall\, a\neq x\in(a-\epsilon,a+\epsilon)\subseteq\Omega$, $f(x)>f(a)$.

[T5.x4] Apunts del Tema 5, §5.3 — Propietats conegudes
Recordem ara algunes propietats conegudes.

[T5.10] Proposició 10 (Tema 5) — Condició necessària d'extrem (una variable)
Sigui $\Omega\subseteq\mathbb{R}$ obert i $f:\Omega\to\mathbb{R}$ una funció derivable en $a\in\Omega$. Si $a$ és un extrem ($\equiv$ màxim o mínim) local de $f$ llavors $f'(a)=0$. El recíproc no és cert.

[T5.11] Teorema 11 (Tema 5) — Criteri de la derivada r-èsima
Sigui $\Omega\subseteq\mathbb{R}$ obert i $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^r(\Omega)$. Si un punt $a\in\Omega$ compleix $f'(a)=f''(a)=\cdots=f^{(r-1)}(a)=0$, llavors

(i) $f^{(r)}(a)<0$ i $r$ parell $\Rightarrow$ $a$ és un màxim local estricte de $f$;

(ii) $f^{(r)}(a)>0$ i $r$ parell $\Rightarrow$ $a$ és un mínim local estricte de $f$;

(iii) $f^{(r)}(a)<0$ i $r$ senar $\Rightarrow$ $f$ és estrictament decreixent en $a$;

(iv) $f^{(r)}(a)>0$ i $r$ senar $\Rightarrow$ $f$ és estrictament creixent en $a$.

[T5.x5] Apunts del Tema 5, §5.4 — Notació multinomial (motivació)
En aquesta secció establim la notació multinomial, que ens és útil per a poder escriure de manera més compacta expressions que impliquin polinomis en diverses variables. Si el nombre de variables és relativament petit, la notació habitual és encara prou "sostenible". Per exemple, un polinomi de grau $r$ en dues variables es pot escriure com
$$p(x,y)=\sum_{m=0}^{r}\sum_{i=0}^{m}a_{i,m-i}x^i\,y^{m-i},$$
agrupat per polinomis homogenis de grau $m$.

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

[T5.13] Lema 13 (Tema 5) — Límit d'un polinomi i grau dels monomis
Sigui $P(\mathbf{x})\neq0$ un polinomi, $\mathbf{x}=(x_1,\ldots,x_n)$. Llavors, $\displaystyle\lim_{\mathbf{x}\to\mathbf{0}}\dfrac{P(\mathbf{x})}{\|\mathbf{x}\|^r}=0$ si, i només si, tots els monomis de $P$ són de grau $\geqslant r+1$.

[T5.14] Teorema 14 (Tema 5) — Teorema de Taylor (diverses variables)
(de Taylor). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^{r+1}(\Omega)$, i $\mathbf{a}\in\Omega$. Per a tot $\mathbf{x}\in\Omega$ amb $[\mathbf{a},\mathbf{x}]\subseteq\Omega$, existeix $\xi_\mathbf{x}\in(\mathbf{a},\mathbf{x})$ tal que $f(\mathbf{x})=P_r(\mathbf{x})+R_{r+1}(\mathbf{x})$, on

(i) El polinomi
$$\begin{aligned}P_r(\mathbf{x})={}&f(\mathbf{a})+\sum_{i=1}^{n}D_if(\mathbf{a})(x_i-a_i)+\frac{1}{2!}\sum_{i,j=1}^{n}D_{i,j}f(\mathbf{a})(x_i-a_i)(x_j-a_j)+\cdots\\
&\cdots+\frac{1}{r!}\sum_{i_1,\ldots,i_r=1}^{n}D_{i_1,\ldots,i_r}f(\mathbf{a})(x_{i_1}-a_{i_1})\cdots(x_{i_r}-a_{i_r})\end{aligned}$$
s'anomena el polinomi de Taylor de grau $r$ de la funció $f$ en el punt $\mathbf{a}$,

(ii) El residu de grau $r$ de la funció $f$ en el punt $\mathbf{a}$ és
$$R_{r+1}(\mathbf{x})=\frac{1}{(r+1)!}\sum_{i_1,\ldots,i_{r+1}=1}^{n}D_{i_1,\ldots,i_{r+1}}f(\xi_\mathbf{x})(x_{i_1}-a_{i_1})\cdots(x_{i_{r+1}}-a_{i_{r+1}}).$$
A més, $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$

[T5.15] Corol·lari 15 (Tema 5) — Taylor amb hipòtesi C^r
Si $f\in\mathcal{C}^r(\Omega)$ i $\mathbf{a}\in\Omega$, aleshores $\displaystyle\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-P_r(x)}{\|\mathbf{x}-\mathbf{a}\|^r}=0.$

Abans de demostrar-lo, observem que si apliquéssim estrictament el teorema de Taylor tal com l'hem enunciat, per obtenir el resultat del corol·lari 15, usaríem que
$$\lim_{\mathbf{x}\to\mathbf{a}}\frac{f(\mathbf{x})-P_r(x)}{\|\mathbf{x}-\mathbf{a}\|^r}=\lim_{\mathbf{x}\to\mathbf{a}}\frac{R_{r+1}(\mathbf{x})}{\|\mathbf{x}-\mathbf{a}\|^r}=0,$$
i, per tant, necessitaríem suposar que $f\in\mathcal{C}^{\mathbf{r+1}}(\Omega)$. Així, doncs, el corol·lari 15 posa de manifest que l'exigència d'un ordre més de derivació es deu al fet que volem donar una expressió detallada del residu, i aquesta implica derivades d'ordre $r+1$; essencialment, però, només cal imposar $f\in\mathcal{C}^r(\Omega)$ per assegurar que $R_{r+1}(\mathbf{x})=o(\|\mathbf{x}-\mathbf{a}\|^r)$.

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

[T5.18] Definició 18 (Tema 5) — Funció analítica
Una funció $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és analítica si, per a cada $\mathbf{a}\in\Omega$ existeix $\epsilon>0$ i una successió de polinomis homogenis $Q_m(\mathbf{x})$ de grau $m\in\mathbb{N}$, tals que $f(\mathbf{x})=\sum_{m=1}^{\infty}Q_m(\mathbf{x}-\mathbf{a})$, per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$.

[T5.19] Corol·lari 19 (Tema 5) — Criteri d'analiticitat
Si $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és $\mathcal{C}^\infty(\Omega)$ i existeix $M>0$ tal que $|D_{i_1,\ldots,i_r}f(\mathbf{x})|\leqslant M^r$ per a tot $r\in\mathbb{N}$ i $\mathbf{x}\in\Omega$, llavors $f$ és analítica.

[T5.20] Observació 20 (Tema 5) — Jerarquia de regularitat
(Explicació.) Analítica $\Rightarrow\mathcal{C}^\infty\Rightarrow\cdots\Rightarrow\mathcal{C}^{r+1}\Rightarrow\mathcal{C}^r\Rightarrow\cdots\Rightarrow\mathcal{C}^1\Rightarrow\mathcal{C}^0$. Cap recíproc és cert. Les funcions analítiques juguen un paper molt important en l'anàlisi matemàtica actual.

[T5.21] Definició 21 (Tema 5) — Extrems locals (diverses variables)
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció. Diem que un punt $\mathbf{a}\in\Omega$ és un

(i) màxim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\leqslant f(\mathbf{a})$;

(ii) mínim local de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\subseteq\Omega$, $f(\mathbf{x})\geqslant f(\mathbf{a})$;

(iii) màxim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})<f(\mathbf{a})$;

(iv) mínim local estricte de $f$ si existeix $\epsilon>0$ tal que per a tot $\mathbf{x}\in B(\mathbf{a},\epsilon)\backslash\{\mathbf{a}\}\subseteq\Omega$, $f(\mathbf{x})>f(\mathbf{a})$.

[T5.22] Definició 22 (Tema 5) — Punt crític
$\mathbf{a}\in\Omega$ és un punt crític de $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si $f$ és diferenciable en $\mathbf{a}$ i $Df(\mathbf{a})=0$.

[T5.23] Proposició 23 (Tema 5) — Els extrems són punts crítics
Sigui $\Omega\subseteq\mathbb{R}^n$ un obert i $f:\Omega\to\mathbb{R}$ una funció diferenciable en $\mathbf{a}\in\Omega$. Si $\mathbf{a}$ és un extrem (és a dir, un màxim o un mínim) local de $f$, llavors $\mathbf{a}$ és un punt crític de $f$.

[T5.24] Exemple 24 (Tema 5) — Punt crític que no és extrem
Considerem $f(x,y)=x\,y$. En $\mathbf{a}=(0,0)$, tenim que $Df(\mathbf{a})=(y\ \ x)|_\mathbf{a}=(0\ \ 0)$. Per tant, atenent a la definició $\mathbf{a}$ és un punt crític. No obstant, si $xy>0$, és a dir, si $\mathbf{x}$ pertany al primer o al tercer quadrant llevat dels eixos, $f(\mathbf{x})>f(\mathbf{a})$, mentre que per als punts del segon i quart quadrant es compleix que $f(\mathbf{x})<f(\mathbf{a})$.

Aquest exemple posa en evidència que en diverses variables hi ha punts crítics que no són extrems locals i, per tant, que el recíproc de la proposició 23 és fals.

[T5.25] Definició 25 (Tema 5) — Punt de sella
Un punt $\mathbf{a}\in\Omega$ és un punt de sella d'una funció diferenciable $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ si és un punt crític de $f$ i per a tot $\epsilon>0$ existeixen $\mathbf{x},\mathbf{y}\in B(\mathbf{a},\epsilon)$ tals que $f(\mathbf{x})<f(\mathbf{a})<f(\mathbf{y})$.

[T5.x6] Apunts del Tema 5, §5.7 — Introducció a formes quadràtiques
Amb l'objectiu de fer aquestes notes més autocontingudes, fem un recordatori de definicions i resultats de formes quadràtiques.

[T5.26] Definició 26 (Tema 5) — Forma quadràtica
Una forma quadràtica és una aplicació de la forma
$$\begin{array}{cccc}q_M:&\mathbb{R}^n&\longrightarrow&\mathbb{R}\\&\mathbf{u}&\longmapsto&\mathbf{u}^TM\mathbf{u},\end{array}$$
on $M$ és una matriu $n\times n$ simètrica.

Observem que $q_M$ és una funció $\mathcal{C}^\infty$ i compleix que $q_M(\mathbf{0})=0$ i $q_M(\lambda\mathbf{u})=\lambda^2q_M(\mathbf{u})$.

[T5.27] Definició 27 (Tema 5) — Signe d'una forma quadràtica
Diem que una forma quadràtica $q_M:\mathbb{R}^n\to\mathbb{R}$ és

(i) definida positiva ($\oplus$) si $q_M(\mathbf{u})>0$, per a tot $\mathbf{u}\in\mathbb{R}^n\setminus\{\mathbf{0}\}$;

(ii) definida negativa ($\ominus$) si $q_M(\mathbf{u})<0$, per a tot $\mathbf{u}\in\mathbb{R}^n\setminus\{\mathbf{0}\}$;

(iii) indefinida ($\odot$) si existeixen $\mathbf{u},\mathbf{v}\in\mathbb{R}^n$ tals que $q_M(\mathbf{u})>0$ i $q_M(\mathbf{v})<0$;

(iv) semidefinida positiva ($\underline{\oplus}$) si $q_M(\mathbf{u})\geqslant0$, per a tot $\mathbf{u}\in\mathbb{R}^n$;

(v) semidefinida negativa ($\underline{\ominus}$) si $q_M(\mathbf{u})\leqslant0$, per a tot $\mathbf{u}\in\mathbb{R}^n$.

[T5.x7] Apunts del Tema 5, §5.7 — Resultat útil per a la demostració final
El següent resultat ens serà útil a la demostració del resultat final d'aquest capítol.

[T5.28] Lema 28 (Tema 5) — Fites d'una forma definida positiva
Si $q_M:\mathbb{R}^n\to\mathbb{R}$ és una forma quadràtica definida positiva llavors existeixen constants $0<c\leqslant C<\infty$ tals que $c\|\mathbf{u}\|^2\leqslant q_M(\mathbf{u})\leqslant C\|\mathbf{u}\|^2$, $\forall\,\mathbf{u}\in\mathbb{R}^n$.

[T5.x8] Apunts del Tema 5, §5.7 — Forma quadràtica i valors propis
El següent resultat estableix la relació entre el caràcter d'una forma quadràtica i els valors propis de la seva matriu associada.

[T5.29] Teorema 29 (Tema 5) — Teorema dels valors propis
(dels valors propis). Sigui $M$ una matriu simètrica $n\times n$ i siguin $\lambda_1,\ldots,\lambda_n$ els seus valors propis (reals, possiblement múltiples). Llavors, la forma quadràtica $q_M$ és:

(i) definida positiva $\Leftrightarrow\lambda_1,\ldots,\lambda_n>0$;

(ii) definida negativa $\Leftrightarrow\lambda_1,\ldots,\lambda_n<0$;

(iii) indefinida $\Leftrightarrow\exists\,i,j$ tals que $\lambda_i>0$ i $\lambda_j<0$;

(iv) semidefinida positiva $\Leftrightarrow\lambda_1,\ldots,\lambda_n\geqslant0$;

(v) semidefinida negativa $\Leftrightarrow\lambda_1,\ldots,\lambda_n\leqslant0$.

[T5.30] Observació 30 (Tema 5) — Valors propis en dues variables
En dues variables, si $M=\begin{pmatrix}m_{11}&m_{12}\\m_{21}&m_{22}\end{pmatrix}$, aleshores els valors propis de $M$ són
$$\lambda_\pm=\frac12\left(\mathrm{tr}M\pm\sqrt{(\mathrm{tr}M)^2-4\,\mathrm{det}M}\right),$$
on $\mathrm{tr}M=m_{11}+m_{22}$ és la traça de $M$ i $\mathrm{det}M=m_{11}m_{22}-m_{12}m_{21}=m_{11}m_{22}-m_{12}^2$ és el seu determinant. En concret, el discriminant sempre és positiu o zero:
$$(\mathrm{tr}M)^2-4\,\mathrm{det}M=(m_{11}+m_{22})^2-4(m_{11}m_{22}-m_{12}^2)=(m_{11}-m_{22})^2+4m_{12}^2\geq0.$$
Fixem-nos que:

- Si $\det M<0$, aleshores $\lambda_+>0$ i $\lambda_-<0$. En particular, $\lambda_+$ i $\lambda_-$ tenen signes diferents i, per tant, la forma quadràtica $q_M$ és indefinida.
- Si $\det M>0$, aleshores $\mathrm{sgn}(\lambda_\pm)=\mathrm{sgn}(\mathrm{tr}M)$. En particular, si $\mathrm{tr}M>0$, $q_M$ és definida positiva, i si $\mathrm{tr}M<0$, $q_M$ és definida negativa.
- Si $\det M=0$, aleshores $\lambda_-=0$ i $\lambda_+=\mathrm{tr}M$. En aquest cas, si $\mathrm{tr}M>0$, $q_M$ és semidefinida positiva, i si $\mathrm{tr}M<0$, $q_M$ és semidefinida negativa. Si, a més, $\mathrm{tr}M=0$, ambdós valors propis són zero (cas degenerat).

[T5.x9] Apunts del Tema 5, §5.7 — Més dimensions: Sylvester
En més dimensions, en alguns casos, ens serà útil el següent resultat:

[T5.31] Teorema 31 (Tema 5) — Teorema de Sylvester
(de Sylvester). Sigui $M$ una matriu simètrica $n\times n$ i $\Delta_1,\ldots,\Delta_n$ els seus menors principals. Aleshores

(i) $\Delta_i>0$ per a $i=1,\ldots,n\quad\Leftrightarrow\quad q_M$ és definida positiva.

(ii) $(-1)^i\Delta_i>0$ per a $i=1,\ldots,n\quad\Leftrightarrow\quad q_M$ és definida negativa.

[T5.32] Definició 32 (Tema 5) — Matriu hessiana
Sigui $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$. La matriu (o la forma quadràtica) hessiana de $f$ en un punt $\mathbf{a}\in\Omega$ és $Hf(\mathbf{a})$ (o $q_{Hf(\mathbf{a})}$), on
$$Hf(\mathbf{a})=\begin{pmatrix}D_{1,1}f(\mathbf{a})&\cdots&D_{1,n}f(\mathbf{a})\\\vdots&&\vdots\\D_{n,1}f(\mathbf{a})&\cdots&D_{n,n}f(\mathbf{a})\end{pmatrix}.$$

[T5.x10] Apunts del Tema 5, §5.8 — Aplicació de les formes quadràtiques
Prenent la matriu $M=Hf(\mathbf{a})$, els resultats enunciats en el context de les formes quadràtiques ens serviran per a la classificació de punts crítics en camps escalars. El següent resultat ens proporciona condicions suficients per fer-ho.

[T5.33] Teorema 33 (Tema 5) — Condicions suficients d'extrem
(condicions suficients). Sigui $\Omega\subseteq\mathbb{R}^n$ un obert, $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^2(\Omega)$, i $\mathbf{a}\in\Omega$ un punt crític de $f$. Aleshores,

(i) $q_{Hf(\mathbf{a})}$ és definida positiva $\Rightarrow$ $\mathbf{a}$ és un mínim local estricte de $f$.

(ii) $q_{Hf(\mathbf{a})}$ és definida negativa $\Rightarrow$ $\mathbf{a}$ és un màxim local estricte de $f$.

(iii) $q_{Hf(\mathbf{a})}$ és indefinida $\Rightarrow$ $\mathbf{a}$ és un punt de sella de $f$.

(iv) $\mathbf{a}$ és un mínim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida positiva.

(v) $\mathbf{a}$ és un màxim local de $f$ $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és semidefinida negativa.

[T5.34] Observació 34 (Tema 5) — Implicacions i recíprocs falsos
$q_{Hf(\mathbf{a})}\ \oplus\ \Rightarrow$ $\mathbf{a}$ és un mínim local estricte $\Rightarrow$ $\mathbf{a}$ és un mínim local $\Rightarrow$ $q_{Hf(\mathbf{a})}$ és $\underline{\oplus}$, i els tres recíprocs són falsos.

[T5.35] Exemple 35 (Tema 5) — Classificació de punts crítics
Exemples de càlcul i classificació de punts crítics.

1. Calculeu els punts crítics de $f(x,y)=1+\mathrm{e}^{-x^2}\cos y$ i, si és possible, classifiqueu-los.

   Trobem en primer lloc els punts crítics:
   $$f_x(x,y)=-2x\mathrm{e}^{-x^2}\cos y=0,\qquad f_y(x,y)=-\mathrm{e}^{-x^2}\sin y=0.$$
   De la segona equació es deriva que $\sin y=0\Rightarrow y=k\pi$, amb $k\in\mathbb{Z}$. Substituint a la primera:
   $$f_x(x,k\pi)=-2x\mathrm{e}^{-x^2}(-1)^k=0\Rightarrow x=0.$$
   Per tant, els punts crítics de $f$ són tots els punts del tipus $(x,y)=(0,k\pi)$, amb $k\in\mathbb{Z}$.

   Calculem ara la seva matriu hessiana per a determinar, si és possible, el seu caràcter. Del fet que $f\in\mathcal{C}^2(\mathbb{R}^2)$ (en realitat, $f\in\mathcal{C}^\infty(\mathbb{R}^2)$) es dedueix que $f_{xy}=f_{yx}$. Així doncs, calculant, tenim
   $$f_{xx}=(-2+4x^2)\mathrm{e}^{-x^2}\cos y,\qquad f_{xy}=2x\mathrm{e}^{-x^2}\sin y,\qquad f_{yy}=-\mathrm{e}^{-x^2}\cos y,$$
   d'on, avaluant als punts crítics, s'obté per a $k\in\mathbb{Z}$,
   $$Hf(0,k\pi)=\begin{pmatrix}2(-1)^{k+1}&0\\0&(-1)^{k+1}\end{pmatrix}.$$
   Si considerem $k=2m$ parell, aleshores
   $$Hf(0,2m\pi)=\begin{pmatrix}2(-1)^{2m+1}&0\\0&(-1)^{2m+1}\end{pmatrix}$$
   és una matriu definida negativa (els seus vaps són tots dos negatius). En conseqüència, els punts de la forma $(0,2m\pi)$, amb $m\in\mathbb{Z}$, són màxims relatius de $f$. De manera anàloga es pot veure que els punts de la forma $(0,2m+1\pi)$, amb $m\in\mathbb{Z}$, són mínims relatius.

2. En els següents exemples, el càlcul de la matriu hessiana no decideix: a) $f(x,y)=(x-y)^3$, b) $f(x,y)=(x-y)^4$, c) $f(x,y)=(x^2+y^2)^2$.

   Comencem per l'últim. En el cas c) observeu que $f_x=4x(x^2+y^2)$ i $f_y=4y(x^2+y^2)$ s'anul·len si i només si $x=y=0$. La matriu hessiana al punt $(0,0)$ és la matriu de zeros (Nota: noteu que el polinomi de Taylor de grau 2 de $f$ al $(0,0)$ és idènticament nul) i, per tant, el criteri del teorema 33 no ens diu res. Tot i això, observeu que $f(x,y)>f(0,0)$ per a tot $(x,y)\in\mathbb{R}^2\setminus\{(0,0)\}$. És a dir, $f$ té un mínim absolut al punt $(0,0)$.

   Procedint de manera anàloga, en el cas a) tenim: $f_x=3(x-y)^2$ i $f_y=-3(x-y)^2$, que són nul·les si i només si $x=y$. Si calculem la matriu hessiana, s'obté
   $$Hf(x,y)=\begin{pmatrix}6(x-y)&-6(x-y)\\-6(x-y)&6(x-y)\end{pmatrix}\Rightarrow Hf(x,x)=\begin{pmatrix}0&0\\0&0\end{pmatrix},$$
   que no decideix. El cas b) és totalment anàleg al cas a).
</apunts>

## Statements

<questionari>
[1] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^2$. Si $(0,0)$ és un mínim local estricte de $f$, aleshores la forma quadràtica $q_{Hf(0,0)}$ és definida positiva.
    veredicte declarat: fals
    contraexemple: $f(x,y)=x^4+y^4$: $(0,0)$ és mínim local estricte però $Hf(0,0)$ és la matriu nul·la, que no és definida positiva.
    resolució: Prenem $f(x,y)=x^4+y^4$, que és $\mathcal{C}^\infty$. Per a tot $(x,y)\neq(0,0)$ es té $f(x,y)>0=f(0,0)$, de manera que $(0,0)$ és un mínim local estricte (de fet absolut). Ara bé, $f_{xx}=12x^2$, $f_{yy}=12y^2$, $f_{xy}=0$, i per tant $Hf(0,0)$ és la matriu nul·la: $q_{Hf(0,0)}(\mathbf{u})=0$ per a tot $\mathbf{u}$, que no és definida positiva. El teorema només dona que un mínim local té hessiana semidefinida positiva; el recíproc de «definida positiva $\Rightarrow$ mínim estricte» és fals.
    pista: La condició «hessiana definida positiva» és suficient per a un mínim estricte; és també necessària? Penseu en funcions que creixen més lentament que $\|\mathbf{x}\|^2$ a prop de l'origen.
    teoria citada: T5.33, T5.34, T5.27
[2] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^\infty$ tal que, per a cada vector $\mathbf{v}\in\mathbb{R}^2\setminus\{\mathbf{0}\}$, la funció $g_{\mathbf{v}}(t)=f(t\mathbf{v})$ té un mínim local estricte a $t=0$. Aleshores $(0,0)$ és un mínim local de $f$.
    veredicte declarat: fals
    contraexemple: $f(x,y)=(y-x^2)(y-2x^2)$: té mínim estricte sobre cada recta per l'origen, però sobre la paràbola $y=\frac{3}{2}x^2$ val $-\frac{x^4}{4}<0$.
    resolució: Sigui $f(x,y)=(y-x^2)(y-2x^2)=y^2-3x^2y+2x^4$, polinomi i per tant $\mathcal{C}^\infty$. Sobre $\mathbf{v}=(1,m)$: $g(t)=m^2t^2-3mt^3+2t^4$; si $m\neq0$, $g'(0)=0$ i $g''(0)=2m^2>0$, mínim local estricte; si $m=0$, $g(t)=2t^4$, mínim estricte. Sobre $\mathbf{v}=(0,1)$: $g(t)=t^2$, mínim estricte. Els múltiples d'aquests vectors donen el mateix (reparametrització lineal). En canvi, sobre la paràbola $y=\frac{3}{2}x^2$, que passa per l'origen, $f(x,\frac{3}{2}x^2)=\frac{x^2}{2}\cdot\left(-\frac{x^2}{2}\right)=-\frac{x^4}{4}<0=f(0,0)$ per a $x\neq0$. Així, tota bola centrada a l'origen conté punts on $f<f(0,0)$, i $(0,0)$ no és mínim local.
    pista: Ser mínim local demana controlar $f$ en tota una bola. Les rectes per l'origen exhaureixen tots els camins que arriben a l'origen? On és negatiu un producte de dos factors?
    teoria citada: T5.21, T5.11
[3] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^2$ i $\mathbf{a}$ un punt crític de $f$. Si $\dfrac{\partial^2 f}{\partial x^2}(\mathbf{a})\cdot\dfrac{\partial^2 f}{\partial y^2}(\mathbf{a})<0$, aleshores $\mathbf{a}$ és un punt de sella de $f$.
    veredicte declarat: cert
    resolució: Com que $f\in\mathcal{C}^2$, pel teorema de Schwarz $f_{xy}(\mathbf{a})=f_{yx}(\mathbf{a})$ i la hessiana és simètrica. El seu determinant és $\det Hf(\mathbf{a})=f_{xx}(\mathbf{a})f_{yy}(\mathbf{a})-f_{xy}(\mathbf{a})^2<0$, ja que el primer terme és negatiu i el segon no positiu. Si $\det M<0$, els valors propis tenen signes oposats i $q_{Hf(\mathbf{a})}$ és indefinida. Per les condicions suficients, un punt crític amb hessiana indefinida és un punt de sella. (També es veu directament: $q(1,0)=f_{xx}(\mathbf{a})$ i $q(0,1)=f_{yy}(\mathbf{a})$ tenen signes oposats.)
    pista: Què podeu dir del signe del determinant de la hessiana, sense conèixer la derivada creuada? I què vol dir això per als valors propis?
    teoria citada: T5.6, T5.30, T5.33, T5.25
[4] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ contínua tal que totes les derivades parcials primeres i segones de $f$ existeixen en tot punt de $\mathbb{R}^2$. Aleshores $\dfrac{\partial^2 f}{\partial x\partial y}(0,0)=\dfrac{\partial^2 f}{\partial y\partial x}(0,0)$.
    veredicte declarat: fals
    contraexemple: $f(x,y)=\frac{xy(x^2-y^2)}{x^2+y^2}$, $f(0,0)=0$: les dues derivades creuades a l'origen valen $-1$ i $1$.
    resolució: Sigui $f(x,y)=\frac{xy(x^2-y^2)}{x^2+y^2}$ si $(x,y)\neq(0,0)$ i $f(0,0)=0$. És contínua ($|f|\leq|xy|$) i fora de l'origen és un quocient de polinomis, amb totes les derivades. A l'origen: $f_x(0,y)=\lim_{h\to0}\frac{f(h,y)}{h}=\lim_{h\to0}\frac{y(h^2-y^2)}{h^2+y^2}=-y$ (també per a $y=0$, ja que $f(h,0)=0$), i $f_y(x,0)=\lim_{k\to0}\frac{f(x,k)}{k}=x$. Com que $f(x,0)=f(0,y)=0$, $f_{xx}(0,0)=f_{yy}(0,0)=0$. Derivant $f_x(0,y)=-y$ respecte de $y$ s'obté $-1$, i derivant $f_y(x,0)=x$ respecte de $x$ s'obté $1$. Així les dues derivades creuades existeixen però són diferents a l'origen. Falla la hipòtesi de Schwarz: les derivades creuades no són contínues a $(0,0)$.
    pista: Quina hipòtesi exigeix el teorema de Schwarz a més de l'existència de les derivades creuades? Hi ha algun exemple dels apunts on aquesta hipòtesi no es compleixi?
    teoria citada: T5.5, T5.6, T5.7
[5] Sigui $f(x,y)=\mathrm{e}^x\sin(xy)$. Aleshores $\dfrac{\partial^3 f}{\partial x^2\partial y}(0,0)=2$.
    veredicte declarat: cert
    resolució: La funció és $\mathcal{C}^\infty$, i per Schwarz totes les derivades terceres amb dues $x$ i una $y$ coincideixen; en direm $f_{xxy}$. Pels desenvolupaments d'una variable, $\mathrm{e}^x\sin(xy)=xy+x^2y+R_4(x,y)$ amb $R_4/\|(x,y)\|^3\to0$; per la unicitat del polinomi de Taylor, $P_3(x,y)=xy+x^2y$. A la fórmula de Taylor, el terme de grau 3 és $\frac{1}{3!}\sum_{i,j,k}D_{ijk}f(0,0)\,x_ix_jx_k$, i el monomi $x^2y$ hi apareix $3$ vegades (ordres $xxy$, $xyx$, $yxx$), de manera que el seu coeficient és $\frac{3}{3!}f_{xxy}(0,0)=\frac12 f_{xxy}(0,0)$. Igualant a $1$, $f_{xxy}(0,0)=2$.
    pista: Cal derivar tres vegades? Quina relació hi ha entre els coeficients del polinomi de Taylor i les derivades a l'origen, i com el podeu obtenir sense derivar?
    teoria citada: T5.14, T5.16, T5.17, T5.6
[6] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^\infty$ amb un únic punt crític $\mathbf{a}$. Si $\mathbf{a}$ és un mínim local estricte de $f$, aleshores $f(\mathbf{x})\geq f(\mathbf{a})$ per a tot $\mathbf{x}\in\mathbb{R}^2$.
    veredicte declarat: fals
    contraexemple: $f(x,y)=x^2+y^2(1+x)^3$: l'únic punt crític és $(0,0)$, mínim local estricte, però $f(-2,y)=4-y^2$ no està fitada inferiorment.
    resolució: Sigui $f(x,y)=x^2+y^2(1+x)^3$, polinomi. $f_x=2x+3y^2(1+x)^2$, $f_y=2y(1+x)^3$. De $f_y=0$: $y=0$ o $x=-1$. Si $y=0$, $f_x=2x=0$ dona $x=0$. Si $x=-1$, $f_x=-2\neq0$. Per tant $(0,0)$ és l'únic punt crític. $Hf(0,0)=\begin{pmatrix}2&0\\0&2\end{pmatrix}$ és definida positiva, i $(0,0)$ és mínim local estricte. Però $f(-2,y)=4-y^2$, i per exemple $f(-2,3)=-5<0=f(0,0)$. En una variable l'afirmació és certa (entre un mínim i un punt més baix hi hauria un màxim, que seria un altre punt crític), però en dues variables es pot «sortir» de la vall sense passar per cap altre punt crític.
    pista: En una variable, per què un únic punt crític que és mínim local ha de ser absolut? Quin pas d'aquest argument depèn de ser a la recta real?
    teoria citada: T5.21, T5.22, T5.33
[7] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ contínua. Si $(0,0)$ és un mínim local estricte de $f$, aleshores les derivades parcials $\dfrac{\partial f}{\partial x}(0,0)$ i $\dfrac{\partial f}{\partial y}(0,0)$ existeixen i valen $0$.
    veredicte declarat: fals
    contraexemple: $f(x,y)=\sqrt{x^2+y^2}$: mínim local estricte a l'origen, però $\frac{f(h,0)}{h}=\frac{|h|}{h}$ no té límit.
    resolució: Sigui $f(x,y)=\sqrt{x^2+y^2}$, contínua. Per a $(x,y)\neq(0,0)$, $f(x,y)>0=f(0,0)$: mínim local estricte. Però $\frac{f(h,0)-f(0,0)}{h}=\frac{|h|}{h}$ val $1$ si $h>0$ i $-1$ si $h<0$, i no té límit quan $h\to0$; per tant $\frac{\partial f}{\partial x}(0,0)$ no existeix (anàlogament per a $y$). La proposició «els extrems són punts crítics» exigeix que $f$ sigui diferenciable al punt.
    pista: Quines hipòtesis té la proposició que relaciona extrems i punts crítics? Penseu en la gràfica d'un con.
    teoria citada: T5.23, T5.22, T5.10
[8] Sigui $f:\mathbb{R}\to\mathbb{R}$ de classe $\mathcal{C}^\infty$ tal que $f^{(k)}(0)=0$ per a tot $k\geq0$. Aleshores existeix $\epsilon>0$ tal que $f(x)=0$ per a tot $x\in(-\epsilon,\epsilon)$.
    veredicte declarat: fals
    contraexemple: $f(x)=\mathrm{e}^{-1/x^2}$ si $x\neq0$, $f(0)=0$: totes les derivades a l'origen són nul·les, però $f(x)>0$ per a $x\neq0$.
    resolució: Sigui $f(x)=\mathrm{e}^{-1/x^2}$ per a $x\neq0$ i $f(0)=0$. Per inducció, per a $x\neq0$, $f^{(k)}(x)=Q_k(1/x)\,\mathrm{e}^{-1/x^2}$ amb $Q_k$ polinomi, i com que $\mathrm{e}^{-1/x^2}/x^m\to0$ quan $x\to0$ per a tot $m$, s'obté (amb el quocient incremental) $f^{(k)}(0)=0$ per a tot $k$ i que cada $f^{(k)}$ és contínua: $f\in\mathcal{C}^\infty$. Tots els polinomis de Taylor a $0$ són nuls, però $f(x)>0$ per a tot $x\neq0$, i per tant $f$ no s'anul·la en cap entorn de $0$. És un exemple de funció $\mathcal{C}^\infty$ no analítica.
    pista: El residu de Taylor tendeix a zero més ràpid que $(x-a)^r$, però això diu que el residu sigui zero? Quina és la diferència entre $\mathcal{C}^\infty$ i analítica?
    teoria citada: T5.8, T5.18, T5.20
[9] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^2$ i $\mathbf{a}$ un punt crític de $f$ tal que $q_{Hf(\mathbf{a})}$ és semidefinida positiva i $Hf(\mathbf{a})$ no és la matriu nul·la. Aleshores $\mathbf{a}$ és un mínim local de $f$.
    veredicte declarat: fals
    contraexemple: $f(x,y)=x^2+y^3$ a $(0,0)$: $Hf(0,0)=\mathrm{diag}(2,0)$, però $f(0,y)=y^3<0$ per a $y<0$.
    resolució: Sigui $f(x,y)=x^2+y^3$. $f_x=2x$, $f_y=3y^2$ s'anul·len a $(0,0)$: punt crític. $f_{xx}=2$, $f_{xy}=0$, $f_{yy}=6y$, de manera que $Hf(0,0)=\begin{pmatrix}2&0\\0&0\end{pmatrix}$, amb valors propis $2$ i $0$: semidefinida positiva i no nul·la. Però $f(0,-t)=-t^3<0=f(0,0)$ per a tot $t>0$, de manera que tota bola centrada a l'origen conté punts amb $f<f(0,0)$: no és mínim local. Quan la hessiana és degenerada, la direcció del nucli queda governada pels termes d'ordre superior.
    pista: La semidefinició positiva és necessària per a un mínim; és també suficient? Què passa en la direcció on la forma quadràtica s'anul·la?
    teoria citada: T5.33, T5.34, T5.30
[10] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^2$ i $\mathbf{a}$ un punt crític de $f$ amb $q_{Hf(\mathbf{a})}$ definida positiva. Aleshores existeix $\epsilon>0$ tal que $\mathbf{a}$ és l'únic punt crític de $f$ a la bola $B(\mathbf{a},\epsilon)$.
    veredicte declarat: cert
    resolució: El gradient $\nabla f$ és de classe $\mathcal{C}^1$, per tant diferenciable a $\mathbf{a}$ amb diferencial $Hf(\mathbf{a})$: $\nabla f(\mathbf{x})=Hf(\mathbf{a})(\mathbf{x}-\mathbf{a})+\mathbf{r}(\mathbf{x})$ amb $\|\mathbf{r}(\mathbf{x})\|/\|\mathbf{x}-\mathbf{a}\|\to0$ (hem usat $\nabla f(\mathbf{a})=\mathbf{0}$). Com que $Hf(\mathbf{a})$ és simètrica amb valors propis $\lambda_1,\lambda_2>0$, si $\lambda=\min(\lambda_1,\lambda_2)$ es té $\|Hf(\mathbf{a})\mathbf{u}\|\geq\lambda\|\mathbf{u}\|$ (base ortonormal de vectors propis). Triem $\epsilon>0$ amb $\|\mathbf{r}(\mathbf{x})\|\leq\frac{\lambda}{2}\|\mathbf{x}-\mathbf{a}\|$ a $B(\mathbf{a},\epsilon)$. Aleshores, per a $\mathbf{x}\neq\mathbf{a}$ de la bola, $\|\nabla f(\mathbf{x})\|\geq\frac{\lambda}{2}\|\mathbf{x}-\mathbf{a}\|>0$, i $\mathbf{x}$ no és crític.
    pista: Quina aproximació lineal té el gradient a prop de $\mathbf{a}$? Si una matriu simètrica té tots els valors propis positius, pot enviar un vector no nul a $\mathbf{0}$?
    teoria citada: T5.29, T5.32, T5.33
[11] Si $f:\mathbb{R}^2\to\mathbb{R}$ és de classe $\mathcal{C}^3$, aleshores entre les $8$ derivades parcials terceres $D_{i}D_{j}D_{k}f$ ($i,j,k\in\{1,2\}$) n'hi ha com a molt $4$ de diferents.
    veredicte declarat: cert
    resolució: Com que $f\in\mathcal{C}^3$, $f$ i les seves derivades primeres són $\mathcal{C}^2$ i s'hi pot aplicar el teorema de Schwarz. Per exemple, $D_1D_2D_1f=D_1(D_2D_1f)=D_1(D_1D_2f)=D_1D_1D_2f$ (Schwarz per a $f$), i $D_2D_1(D_1f)=D_1D_2(D_1f)$ (Schwarz per a $D_1f$). Repetint, qualsevol derivada tercera és igual a la que s'obté reordenant els índexs, i per tant només depèn de quantes vegades es deriva respecte de $x$: $0,1,2$ o $3$. Això dona com a molt $4$ funcions diferents: $f_{xxx},f_{xxy},f_{xyy},f_{yyy}$ (i en general són diferents, p. ex. per a $x^3+x^2y+2xy^2+3y^3$ valen $6,2,4,18$).
    pista: Si es pot canviar l'ordre de dues derivacions consecutives, de què depèn realment una derivada tercera? Quants monomis de grau 3 hi ha en dues variables?
    teoria citada: T5.6, T5.1, T5.12
</questionari>

## Output

Write tema-5.normal.audit.json following this schema:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "revisions"
  ],
  "properties": {
    "revisions": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "num",
          "problemes",
          "resolucio_correcta",
          "teoria_correcta",
          "pista_neutra"
        ],
        "properties": {
          "num": {
            "type": "integer"
          },
          "problemes": {
            "type": "string"
          },
          "resolucio_correcta": {
            "type": "boolean"
          },
          "teoria_correcta": {
            "type": "boolean"
          },
          "pista_neutra": {
            "type": "boolean"
          }
        }
      }
    }
  }
}
```

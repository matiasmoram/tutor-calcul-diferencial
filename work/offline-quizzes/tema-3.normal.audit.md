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

<apunts tema="3" titol="Diferenciabilitat">
[T3.1] Definició 1 (Tema 3) — Derivada direccional
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $a\in\mathring{\Omega}$, i $u\in\mathbb{R}^n\setminus\{0\}$. Es defineix la derivada direccional de $f$ en el punt $a$ segons la direcció i sentit del vector $u$ com
$$D_uf(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t},\tag{1}$$
si aquest límit existeix. (Nota: De fet, si definim $g(t)=f(a+tu)$, la funció $f$ restringida a la recta $\{a+tu\mid t\in\mathbb{R}\}$, aleshores $D_uf(a)=g'(0)$.)

[T3.x1] Apunts del Tema 3, §3.1 — Recordatori: derivada en una variable
Recordeu que per a una funció $f:\Omega\subseteq\mathbb{R}\to\mathbb{R}$, que $f$ sigui derivable a $a\in\mathring{\Omega}$ és equivalent a que existeixi
$$f'(a)=\lim_{h\to0}\frac{f(a+h)-f(a)}{h}=\lim_{x\to a}\frac{f(x)-f(a)}{x-a}.$$
En el cas particular que el vector $u$ sigui algun vector de la base canònica, és a dir, $u=e_i=(0,0,\ldots,\overset{(i)}{1},0,\ldots,0)$ aquestes derivades direccionals reben un nom especial.

[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T3.3] Exemple 3 (Tema 3) — Càlcul de derivades parcials
(i) Sigui $f:\mathbb{R}^2\to\mathbb{R}$, definida per $f(x,y)=x^2+y^2$. Aleshores, es té que
$$\frac{\partial f}{\partial x}(x,y)=2x,\qquad \frac{\partial f}{\partial y}(x,y)=2y.$$
(ii) Si considerem $f:\mathbb{R}^2\to\mathbb{R}$, definida per $f(x,y)=x^2\sin(3y)$, llavors
$$\frac{\partial f}{\partial x}(x,y)=2x\sin(3y),\qquad \frac{\partial f}{\partial y}(x,y)=3x^2\cos(3y).$$

[T3.4] Exercici 4 (Tema 3) — Funció simètrica i derivades parcials
Sigui $f:\mathbb{R}^2\to\mathbb{R}$ tal que $f(x,y)=f(y,x)$, és a dir $f$ és simètrica respecte de la involució $x\leftrightarrow y$. Demostreu que
$$\frac{\partial f}{\partial y}(x_0,y_0)=\frac{\partial f}{\partial x}(y_0,x_0).$$

[T3.5] Observació 5 (Tema 3) — Homogeneïtat en la direcció
És fàcil comprovar que $D_{\lambda u}f(a)=\lambda D_uf(a)$. Això fa que si es vol "comparar" els diferents valors de les derivades direccionals en un punt $a$ fixat, el vector $u$ es consideri unitari.

[T3.x2] Apunts del Tema 3, §3.1 — Figura de la derivada direccional
[Figura: Superfície gràfica d'un camp escalar $f:\mathbb{R}^2\to\mathbb{R}$ tallada per un pla vertical que conté la direcció $u$ des del punt $a=(a_1,a_2)$ del pla $XY$; la corba intersecció (en vermell) i la seva recta tangent (en negre) al punt de la gràfica sobre $a$.]
Figura 1: Representació gràfica de la derivada direccional a un punt $a=(a_1,a_2)$ d'un camp escalar $f:\mathbb{R}^2\to\mathbb{R}$.

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

[T3.7] Observació 7 (Tema 3) — Derivada direccional de camps vectorials
En el cas que $f:\mathbb{R}^n\to\mathbb{R}^m$, amb $f=(f_1,f_2,\ldots,f_m)$, si $a\in\mathbb{R}^n$ i $u\in\mathbb{R}^n\setminus\{0\}$, aleshores $D_uf(a)=(D_uf_1(a),D_uf_2(a),\ldots,D_uf_m(a))$.

[T3.x3] Apunts del Tema 3, §3.1 — Recordatori: aplicacions lineals
Recordeu que $\mathcal{L}(\mathbb{R}^n,\mathbb{R}^m)$ denota el conjunt de les aplicacions lineals de $\mathbb{R}^n$ a $\mathbb{R}^m$. Si $g\in\mathcal{L}(\mathbb{R}^n,\mathbb{R}^m)$ i denotem per $A\in\mathcal{M}_{m\times n}$ la matriu associada a $g$ en les bases $\{u\}$, $\{v\}$ de $\mathbb{R}^n$ i $\mathbb{R}^m$, respectivament, aleshores $\forall x\in\mathbb{R}^n$ es té que $g(x)=Ax$.

[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$

[T3.x4] Apunts del Tema 3, §3.1 — Reformulació epsilon-delta i aproximació afí
És a dir, en altres paraules, si $\forall\varepsilon>0$ $\exists\delta=\delta(\varepsilon)>0$ tal que si $x\in\Omega$ amb $\|x-a\|<\delta$ aleshores $\|f(x)-(f(a)+Df(a)(x-a))\|\leq\varepsilon\|x-a\|$.

Per tant, si $f$ és diferenciable al punt $a$, per a valors d'$x$ propers a $a$ la funció $f(x)$ es pot aproximar per la funció afí $f(a)+Df(a)(x-a)$.

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

[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$

[T3.11] Observació 11 (Tema 3) — Derivada direccional via derivades parcials
Observeu que si $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és diferenciable en $a\in\mathring{\Omega}$ aleshores, si $u=\lambda_1e_1+\lambda_2e_2+\cdots+\lambda_ne_n$ llavors
$$D_uf(a)=\sum_{j=1}^n\lambda_j\frac{\partial f}{\partial x_j}(a).$$

[T3.12] Exemple 12 (Tema 3) — Diferenciabilitat de x^2+y^2 a (1,2)
La funció $f:\mathbb{R}^2\to\mathbb{R}$, definida per $f(x,y)=x^2+y^2$ és diferenciable al punt $a=(1,2)$.

[T3.13] Proposició 13 (Tema 3) — Direcció de màxim creixement i gradient
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciable en un punt $a\in\mathring{\Omega}$. Aleshores:

(i) $\displaystyle\max_{\|u\|=1}\{D_uf(a)\}=\|\nabla f(a)\|$ i aquest valor s'obté per a $u=\dfrac{\nabla f(a)}{\|\nabla f(a)\|}$.

(ii) De manera anàloga, $\displaystyle\min_{\|u\|=1}\{D_uf(a)\}=-\|\nabla f(a)\|$ i aquest valor s'obté per al vector $u=-\dfrac{\nabla f(a)}{\|\nabla f(a)\|}$.

(iii) Considerem el cas $n=2$. Sigui $\gamma=\{x\in\mathbb{R}^2\mid f(x,y)=f(a_1,a_2)\}$ la corba de nivell (al pla $(x,y)$) d'alçada $f(a_1,a_2)$. Aleshores, el vector gradient de $f$ al punt $(a_1,a_2)$, $\nabla f(a_1,a_2)$, és ortogonal a la corba $\gamma$ en el punt $(a_1,a_2)$.

[T3.x5] Apunts del Tema 3, §3.1 — Resum: direcció de màxim decreixement
En resum, la direcció donada pel vector $\nabla f(a)\in\mathbb{R}^n\setminus\{0\}$ determina la direcció i sentits de màxim/mínim decreixement de la funció $f$ en el punt $(a,f(a))$.

[T3.14] Proposició 14 (Tema 3) — Diferenciable implica contínua i Lipschitz
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $a\in\mathring{\Omega}$. Si $f$ és diferenciable al punt $a$, aleshores:

(i) $f$ és contínua al punt $a$.

(ii) $f$ és localment Lipschitz en $a$. (Nota: De fet, és més precís dir que és localment puntualment Lipschitz en $a$; és a dir que existeix $\delta>0$ i $M>0$ tal que $d(f8x),f(x))<M\,d(x,a)$ per a tota $x\in B(a,\delta)$. [transcripció literal de la nota; sembla un error tipogràfic de l'original])

[T3.15] Observació 15 (Tema 3) — Contínua no implica diferenciable
El recíproc és fals, és a dir, $f$ contínua en $a$ no implica que $f$ sigui diferenciable al punt $a$. Contraexemple: $f(x,y)=|x|+|y|$ és contínua al punt $(0,0)$ però en canvi no és diferenciable en $(0,0)$. En efecte, vegem que no existeix una de les seves derivades parcials i, per tant, no tindrem la seva diferenciabilitat:
$$\frac{\partial f}{\partial x}(0,0)=\lim_{t\to0}\frac{f(t,0)-f(0,0)}{t}=\lim_{t\to0}\frac{|t|}{t},$$
que no existeix ja que els seus límits laterals a $0$ són diferents.

[T3.16] Observació 16 (Tema 3) — Derivades parcials sense direccionals
L'existència de les derivades parcials en un punt $x=a$ no implica l'existència de totes les derivades direccionals $D_uf(a)$ en aquell punt. Per exemple, considereu $f:\mathbb{R}^2\to\mathbb{R}$ definida per
$$f(x,y)=\begin{cases}\dfrac{x^2y}{(x^2+y^2)^{5/4}} & \text{si } (x,y)\neq(0,0)\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$
Aquesta funció és contínua al $(0,0)$: observeu que en polars s'escriu
$$f(r\cos\theta,r\sin\theta)=\sqrt{r}\cos^2\theta\sin\theta$$
i satisfà les inequacions
$$0\leq\left|\sqrt{r}\cos^2\theta\sin\theta\right|\leq\sqrt{r}$$
per a tot $r\geq0$. Aplicant el lema del sandwich, si $r\to0$, la funció $\left|\sqrt{r}\cos^2\theta\sin\theta\right|$ tendeix també a $0$ uniformement amb $r$. Per tant, el seu límit al $(0,0)$ és $0$, coincideix amb $f(0,0)$.

D'altra banda, existeixen les dues derivades parcials a l'origen:
$$\begin{aligned}\frac{\partial f}{\partial x}(0,0)&=\lim_{t\to0}\frac{f(t,0)-f(0,0)}{t}=\lim_{t\to0}\frac{0}{t}=0,\\\frac{\partial f}{\partial y}(0,0)&=\lim_{t\to0}\frac{f(0,t)-f(0,0)}{t}=\lim_{t\to0}\frac{0}{t}=0.\end{aligned}$$
En canvi no existeix cap altra derivada direccional: en efecte, prenem $u=(u_1,u_2)$, amb $\|u\|=1$ i tal que $u_1,u_2$ són diferents de $0$. Aleshores,
$$\begin{aligned}D_uf(0,0)&=\lim_{t\to0}\frac{f(tu_1,tu_2)-f(0,0)}{t}=\lim_{t\to0}\frac{1}{t}\frac{(tu_1)^2tu_2}{\left((tu_1)^2+(tu_2)^2\right)^{5/4}}\\&=\lim_{t\to0}\frac{t^2u_1^2u_2}{(t^2)^{5/4}(u_1^2+u_2^2)^{5/4}}=\lim_{t\to0}\frac{u_1^2u_2}{\sqrt{|t|}(u_1^2+u_2^2)^{5/4}}=\infty.\end{aligned}$$

[T3.17] Observació 17 (Tema 3) — Direccionals sense diferenciabilitat
Fins i tot l'existència de totes les derivades direccionals en un punt no implica la diferenciabilitat en aquell punt. Un exemple clàssic és aquest:
$$f(x,y)=\begin{cases}\dfrac{x^2y}{x^2+y^2} & \text{si } (x,y)\neq(0,0)\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

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

[T3.20] Definició 20 (Tema 3) — Funció de classe C^1
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $\Omega$ obert. Direm que $f$ és de classe $\mathcal{C}^1(\Omega)$ si $f$ és diferenciable a $\Omega$ i, per a tot punt $a\in\Omega$, existeixen totes les derivades parcials de $f$ al punt $a$ i hi són contínues. De manera anàloga a definicions anteriors, direm que $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $f=(f_1,f_2,\ldots,f_m)$, és de classe $\mathcal{C}^1(\Omega)$ si $f_i\in\mathcal{C}^1(\Omega)$, per a tot $i=1,2,\ldots,m$.

[T3.x6] Apunts del Tema 3, §3.1 — Mapa d'implicacions
La Figura 3 conté el mapa d'implicacions dels darrers resultats. Recordeu que les implicacions recíproques són falses.

[Figura: Mapa d'implicacions. "Existeixen $\frac{\partial f_i}{\partial x_j}(\cdot)$ en un entorn de $a$ i són contínues en $a$" implica (fletxa 73) "$f$ és diferenciable en $a$"; "$f$ és diferenciable en $a$" implica (fletxa 70) "existeix $D_uf(a)$, $\forall u\neq0$" i (fletxa 72) "$f$ és contínua en $a$"; "existeix $D_uf(a)$, $\forall u\neq0$" implica (fletxa 67) "existeix $\frac{\partial f}{\partial x_i}(a)$, $\forall i=1,\ldots,k$".]
Figura 3: Mapa d'implicacions: diferenciabilitat, existència de derivades direccionals i/o parcials, continuïtat, etc.

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

[T3.23] Proposició 23 (Tema 3) — Àlgebra de funcions diferenciables
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciables en $a\in\mathring{\Omega}$ i sigui $\lambda\in\mathbb{R}$. Llavors,

(i) $f+g$ és diferenciable en $a$ i $D(f+g)(a)=Df(a)+Dg(a)$.

(ii) $\lambda f$ és diferenciable en $a$ i $D(\lambda f)(a)=\lambda Df(a)$.

(iii) $fg$ és diferenciable en $a$ i $J(fg)(a)=g(a)Jf(a)+f(a)Jg(a)$.

(iv) $\dfrac{f}{g}$ és diferenciable en $a$ si $g(a)\neq0$. A més
$$J\left(\frac{f}{g}\right)(a)=\frac{g(a)Jf(a)-f(a)Jg(a)}{g(a)^2}.$$

[T3.x7] Apunts del Tema 3, §3.3 — Introducció al teorema del valor mitjà
Abans d'enunciar-lo, introduïm la següent definició, que generalitza el concepte d'interval a la recta real.

[T3.24] Definició 24 (Tema 3) — Segment obert i tancat
Donats $a,b\in\mathbb{R}^n$, definim el segment obert $(a,b)$ i el segment tancat $[a,b]$ com
$$(a,b)=\{(1-\mu)a+\mu b\mid0<\mu<1\};\qquad[a,b]=\{(1-\mu)a+\mu b\mid0\leq\mu\leq1\}.$$

[T3.25] Teorema 25 (Tema 3) — Teorema del valor mitjà
(Teorema del valor mitjà). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, diferenciable en un obert $\Omega\subseteq\mathbb{R}^n$. Sigui $u\in\mathbb{R}^m$. Aleshores, per a tot $a,b\in\Omega$ tals que $[a,b]\subseteq\Omega$ existeix $\xi\in(a,b)$ tal que
$$\langle u,f(b)-f(a)\rangle=\langle u,Jf(\xi)(b-a)\rangle.$$

[T3.26] Corol·lari 26 (Tema 3) — Teorema del valor mitjà (cas m=1)
(Cas $m=1$). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciable en un obert $\Omega\subseteq\mathbb{R}^n$. Aleshores, $\forall a,b\in\Omega$ tal que $[a,b]\subseteq\Omega$ existeix un $\xi\in[a,b]$ tal que $f(b)-f(a)=\langle\nabla f(\xi),b-a\rangle$.

[T3.27] Definició 27 (Tema 3) — Conjunt convex i pre-convex
(i) Direm que un conjunt $\Omega\subseteq\mathbb{R}^n$ és convex si $\forall a,b\in\Omega$ es té que $[a,b]\subseteq\Omega$.

(ii) Direm que $\Omega\subseteq\mathbb{R}^n$ és pre-convex si $\forall a,b\in\Omega$ existeixen $z_0=a,z_1,z_2,\ldots,z_r=b\in\Omega$ tals que $[z_0,z_1]\cup[z_1,z_2]\cup\ldots\cup[z_{r-1},z_r]$ està inclòs a $\Omega$. És a dir, existeix un conjunt concatenat de segments, tots ells inclosos a $\Omega$, de manera que connecten $a$ amb $b$.

[T3.28] Corol·lari 28 (Tema 3) — Jacobiana nul·la implica funció constant
Sigui $f:\mathbb{R}^n\to\mathbb{R}^m$ diferenciable en un obert pre-convex $\Omega\subseteq\mathbb{R}^n$. Aleshores, si $Jf(a)=0$ per a tot $a\in\Omega$, llavors $f$ és constant a $\Omega$.

[T3.29] Observació 29 (Tema 3) — Necessitat de la pre-convexitat
La hipòtesi que $\Omega$ sigui pre-convexa és necessària. En efecte, sigui $\Omega=\Omega_1\cup\Omega_2$, on $\Omega_1$ i $\Omega_2$ són dos oberts disconnexos de $\mathbb{R}^n$. Podem definir la funció $f:\mathbb{R}^n\to\mathbb{R}$ que valgui $1$ sobre $\Omega_1$ i $2$ sobre $\Omega_2$. Aquesta funció satisfà que $Jf(a)=\nabla f(a)=0$ per a tot $a\in\Omega$ i, en canvi, $f$ no és constant a $\Omega$.

[T3.30] Observació 30 (Tema 3) — Pre-convex implica connex
$\Omega$ pre-convex $\Rightarrow$ $\Omega$ connex (si $\Omega$ és disconnex, aleshores $\Omega$ és no pre-convex).

[T3.31] Definició 31 (Tema 3) — Classes C^r de funcions
Direm que $f\in\mathcal{C}^0(\Omega)\Leftrightarrow f$ és contínua a $\Omega$.

$f\in\mathcal{C}^1(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ a tot punt de $\Omega$ i totes són contínues (per tant, en particular, $f$ és diferenciable i contínua).

$f\in\mathcal{C}^2(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ d'ordre $2$:
$$\frac{\partial^2f}{\partial x_i\partial x_j}=\frac{\partial}{\partial x_j}\left(\frac{\partial f}{\partial x_i}\right),$$
a tot punt de $\Omega$ i són contínues.

En general, per a $r\geq1$, es diu que $f\in\mathcal{C}^r(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials d'ordre $r$ a $\Omega$ i totes són contínues. Clarament, $f\in\mathcal{C}^{r+1}(\Omega)\Rightarrow f\in\mathcal{C}^r(\Omega)$.

Direm que $f\in\mathcal{C}^\infty(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials a qualsevol ordre de $f$ a $\Omega$ i totes són contínues.

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

[T3.x9] Apunts del Tema 3, §3.4 — Introducció a la regla de Leibniz
En aquesta secció parlarem, molt breument, de funcions definides via integrals. Per posar-ne un exemple, suposeu que tenim $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}$ integrable i que definim, associada a ella, la següent funció $F:\mathbb{R}\to\mathbb{R}$,
$$F(y)=\int_a^bf(x,y)\,dx,$$
on $a<b$ són nombres reals. Què en podem dir? És derivable, és a dir, existeix $F'(y)$? Si ho és, quant val?

[T3.32] Teorema 32 (Tema 3) — Regla de Leibniz
(Regla de Leibniz). Sigui $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^1(\Omega)$, amb $\Omega$ obert. Siguin $a,b,c,d\in\mathbb{R}$ tals que $[a,b]\times[c,d]\subseteq\Omega$ i considereu $u,v:(c,d)\to[a,b]$ dues funcions derivables. Llavors,

(i) La funció
$$F(y)=\int_a^bf(x,y)\,dx$$
és derivable a l'interval $(c,d)$ i $F'(y)=\displaystyle\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$.

(ii) La funció
$$G(y)=\int_{u(y)}^{v(y)}f(x,y)\,dx$$
és derivable a l'interval $(c,d)$ i la seva derivada val
$$G'(y)=f(v(y),y)v'(y)-f(u(y),y)u'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx.$$

[T3.33] Exemple 33 (Tema 3) — Leibniz amb cos(mu x)
Considerem la funció $f:\mathbb{R}^2\to\mathbb{R}$ definida per $f(x,\mu)=\cos(\mu x)$. Les seves derivades parcials
$$\frac{\partial f}{\partial x}(x,\mu)=-\mu\sin(\mu x),\qquad\frac{\partial f}{\partial\mu}(x,\mu)=-x\sin(\mu x),$$
són contínues a tot $\mathbb{R}^2$ i, per tant, $f\in\mathcal{C}^1(\mathbb{R}^2)$. Definim, associada a $f$, la funció $F:\mathbb{R}\to\mathbb{R}$
$$F(\mu)=\int_0^bf(x,\mu)\,dx=\int_0^b\cos(\mu x)\,dx,$$
on $b\in\mathbb{R}$ és una constant. Calculem $F'(\mu)$ directament i usant la regla de Leibniz. En efecte, per a $\mu\neq0$, integrant respecte a $x$ tenim
$$F(\mu)=\int_0^b\cos(\mu x)\,dx=\frac{1}{\mu}\left[\sin(\mu x)\right]_0^b=\frac{1}{\mu}\sin(\mu b)\Rightarrow F'(\mu)=\frac{-1}{\mu^2}\sin(\mu b)+\frac{b}{\mu}\cos(\mu b).$$
De l'altra banda, usant Leibniz, tenim que
$$F'(\mu)=\int_0^b\frac{\partial}{\partial\mu}\left(\cos(\mu x)\right)\,dx=-\int_0^bx\sin(\mu x)\,dx.$$
Per tant, comparant amb l'anterior expressió es dedueix que
$$\int_0^bx\sin(\mu x)\,dx=\frac{-1}{\mu^2}\sin(\mu b)+\frac{b}{\mu}\cos(\mu b).$$
Observem que podríem haver obtingut aquesta darrera igualtat integrant per parts.

[T3.34] Exemple 34 (Tema 3) — Fórmula recurrent amb Leibniz
Sovint la regla de Leibniz es fa servir per a obtenir fórmules recurrents per al càlcul de determinades integrals. Per exemple, per a $n\in\mathbb{N}$ i $f:\mathbb{R}\to\mathbb{R}$ contínua, definim la següent successió de funcions
$$F_n(x)=\int_0^x\frac{(x-y)^n}{n!}f(y)\,dy.$$
Busquem una fórmula recurrent per al càlcul de $F_n$ en funció de $f$. Per a simplificar la notació, denotem
$$g(x,y)=\frac{(x-y)^n}{n!}f(y),$$
de manera que $F_n(x)=\displaystyle\int_0^xg(x,y)\,dy$. Calculem $F_n'(x)$ usant la regla de Leibniz:
$$F_n'(x)=\int_0^x\frac{\partial g}{\partial x}(x,y)\,dy+g(x,x)\frac{\partial x}{\partial x}-g(x,0)\frac{\partial0}{\partial x}=\int_0^x\frac{\partial g}{\partial x}(x,y)\,dy,$$
ja que $g(x,x)=0$. A més,
$$F_n'(x)=\int_0^x\frac{\partial g}{\partial x}(x,y)\,dy=\int_0^x\frac{n(x-y)^{n-1}}{n!}f(y)\,dy=\int_0^x\frac{(x-y)^{n-1}}{(n-1)!}f(y)\,dy=F_{n-1}(x).$$
Per tant, tenint en compte que $F_0(x)=\displaystyle\int_0^xf(y)\,dy$, la resta d'elements de la successió s'obtenen a partir de la recurrència
$$F_1(x)=\int_0^xF_0(s)\,ds,\quad F_2(x)=\int_0^xF_1(s)\,ds,\quad\ldots,\quad F_n(x)=\int_0^xF_{n-1}(s)\,ds.$$
</apunts>

## Statements

<questionari>
[1] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ i $a\in\mathbb{R}^2$. Si $u,v\in\mathbb{R}^2$ són vectors no nuls amb $u+v\neq0$ i existeixen $D_uf(a)$ i $D_vf(a)$, aleshores existeix $D_{u+v}f(a)$ i $D_{u+v}f(a)=D_uf(a)+D_vf(a)$.
    veredicte declarat: fals
    contraexemple: $f(x,y)=\frac{x^3}{x^2+y^2}$ si $(x,y)\neq(0,0)$, $f(0,0)=0$, a $a=(0,0)$ amb $u=(1,0)$, $v=(0,1)$: $D_uf(0,0)=1$, $D_vf(0,0)=0$, però $D_{(1,1)}f(0,0)=\frac{1}{2}\neq1$.
    resolució: Prenem $f(x,y)=\frac{x^3}{x^2+y^2}$ si $(x,y)\neq(0,0)$ i $f(0,0)=0$, $a=(0,0)$, $u=(1,0)$, $v=(0,1)$, de manera que $u+v=(1,1)\neq0$. Tenim $D_uf(0,0)=\lim_{t\to0}\frac{f(t,0)}{t}=\lim_{t\to0}\frac{t^3/t^2}{t}=1$ i $D_vf(0,0)=\lim_{t\to0}\frac{f(0,t)}{t}=\lim_{t\to0}\frac{0}{t}=0$, així que les hipòtesis es compleixen. En canvi $D_{(1,1)}f(0,0)=\lim_{t\to0}\frac{f(t,t)}{t}=\lim_{t\to0}\frac{t^3/(2t^2)}{t}=\frac{1}{2}$, que existeix però és diferent de $D_uf(0,0)+D_vf(0,0)=1$. La fórmula $D_uf(a)=\langle\nabla f(a),u\rangle$, que fa lineal $u\mapsto D_uf(a)$, només està garantida si $f$ és diferenciable a $a$ (Proposició 9); aquí $f$ no ho és.
    pista: Quin resultat dels apunts dona la fórmula $D_uf(a)=\langle\nabla f(a),u\rangle$, i quina hipòtesi demana?
    teoria citada: T3.1, T3.5, T3.9, T3.17
[2] Sigui $f:\mathbb{R}^2\to\mathbb{R}$. Si existeixen totes les derivades direccionals $D_uf(0,0)$, $u\neq0$, i existeix $w\in\mathbb{R}^2$ tal que $D_uf(0,0)=\langle w,u\rangle$ per a tot $u\neq0$, aleshores $f$ és contínua a $(0,0)$.
    veredicte declarat: fals
    contraexemple: $f(x,y)=\frac{x^3y}{x^6+y^2}$ si $(x,y)\neq(0,0)$, $f(0,0)=0$: totes les derivades direccionals a l'origen valen $0=\langle(0,0),u\rangle$, però sobre $y=x^3$ la funció val $\frac{1}{2}$.
    resolució: Sigui $f(x,y)=\frac{x^3y}{x^6+y^2}$ si $(x,y)\neq(0,0)$ i $f(0,0)=0$. Donat $u=(u_1,u_2)\neq0$: si $u_2=0$, $f(tu_1,0)=0$ i $D_uf(0,0)=0$; si $u_2\neq0$, $\frac{f(tu_1,tu_2)}{t}=\frac{t^4u_1^3u_2}{t\,(t^6u_1^6+t^2u_2^2)}=\frac{t\,u_1^3u_2}{t^4u_1^6+u_2^2}\to0$. Per tant $D_uf(0,0)=0=\langle w,u\rangle$ amb $w=(0,0)$, i les hipòtesis es compleixen. Però sobre la corba $y=x^3$, $f(x,x^3)=\frac{x^6}{2x^6}=\frac{1}{2}$ per a $x\neq0$, de manera que $\lim_{x\to0}f(x,x^3)=\frac{1}{2}\neq0=f(0,0)$ i $f$ no és contínua a l'origen. Les derivades direccionals només miren rectes per l'origen, i la fórmula lineal no substitueix la condició de diferenciabilitat (3).
    pista: Les derivades direccionals depenen només del comportament de $f$ sobre rectes per l'origen; què passa si t'hi acostes per una corba?
    teoria citada: T3.1, T3.6, T3.8, T3.14
[3] Si $f:\mathbb{R}^2\to\mathbb{R}$ és diferenciable a tot punt de $\mathbb{R}^2$, aleshores la derivada parcial $\frac{\partial f}{\partial x}$ és contínua a tot $\mathbb{R}^2$.
    veredicte declarat: fals
    contraexemple: $f(x,y)=x^2\sin\frac{1}{x}$ si $x\neq0$, $f(0,y)=0$: és diferenciable a tot $\mathbb{R}^2$, però $\frac{\partial f}{\partial x}=2x\sin\frac{1}{x}-\cos\frac{1}{x}$ (per $x\neq0$) no té límit quan $x\to0$.
    resolució: Sigui $f(x,y)=x^2\sin\frac{1}{x}$ si $x\neq0$ i $f(0,y)=0$. Als punts amb $x\neq0$, $\frac{\partial f}{\partial x}=2x\sin\frac{1}{x}-\cos\frac{1}{x}$ i $\frac{\partial f}{\partial y}=0$ són contínues en un entorn, així que $f$ hi és diferenciable (Teorema 18). Als punts $(0,y_0)$: $\frac{\partial f}{\partial x}(0,y_0)=\lim_{t\to0}\frac{t^2\sin(1/t)}{t}=0$, $\frac{\partial f}{\partial y}(0,y_0)=0$, i $|f(x,y)-f(0,y_0)-0|\leq x^2\leq\|(x,y)-(0,y_0)\|^2$, de manera que el quocient de (3) és $\leq\|(x,y)-(0,y_0)\|\to0$: $f$ és diferenciable amb $Df(0,y_0)=0$. Així $f$ és diferenciable a tot $\mathbb{R}^2$. Però sobre l'eix $y=0$, $\frac{\partial f}{\partial x}(x,0)=2x\sin\frac{1}{x}-\cos\frac{1}{x}$: el primer terme tendeix a $0$ i $\cos\frac{1}{x}$ no té límit, de manera que $\frac{\partial f}{\partial x}$ no és contínua a $(0,0)$.
    pista: Recorda l'exemple d'una variable $x^2\sin\frac{1}{x}$: és derivable a $0$? La seva derivada hi és contínua?
    teoria citada: T3.8, T3.18, T3.19, T3.20
[4] Siguin $f:\mathbb{R}^2\to\mathbb{R}^2$ i $g:\mathbb{R}^2\to\mathbb{R}$, i $a\in\mathbb{R}^2$. Si $f$ és diferenciable a $a$ i $g\circ f$ és diferenciable a $a$, aleshores $g$ és diferenciable a $f(a)$.
    veredicte declarat: fals
    contraexemple: $f(x,y)=(x^3,y^3)$, $g(u,v)=\sqrt[3]{u}+\sqrt[3]{v}$, $a=(0,0)$: $g\circ f(x,y)=x+y$ és diferenciable, però $\frac{\partial g}{\partial u}(0,0)$ no existeix.
    resolució: Prenem $f(x,y)=(x^3,y^3)$, polinòmica i per tant diferenciable a $a=(0,0)$, i $g(u,v)=\sqrt[3]{u}+\sqrt[3]{v}$ (arrel cúbica real). Aleshores $(g\circ f)(x,y)=\sqrt[3]{x^3}+\sqrt[3]{y^3}=x+y$, lineal i diferenciable a tot arreu. Però a $f(a)=(0,0)$: $\frac{\partial g}{\partial u}(0,0)=\lim_{t\to0}\frac{\sqrt[3]{t}}{t}=\lim_{t\to0}t^{-2/3}=+\infty$, de manera que no existeix aquesta derivada parcial i $g$ no és diferenciable a $(0,0)$ (Proposició 9). La regla de la cadena només va en un sentit: $f$ pot «aplanar» la singularitat de $g$ ($Jf(0,0)=0$).
    pista: Si $Jf(a)$ és la matriu nul·la, què et diu la composició sobre el comportament de $g$ a prop de $f(a)$?
    teoria citada: T3.2, T3.9, T3.21
[5] Sigui $f:\mathbb{R}\to\mathbb{R}^2$ derivable a tot $\mathbb{R}$. Aleshores, per a tot $a<b$ existeix $c\in(a,b)$ tal que $f(b)-f(a)=f'(c)\,(b-a)$.
    veredicte declarat: fals
    contraexemple: $f(t)=(\cos t,\sin t)$ a $[0,2\pi]$: $f(2\pi)-f(0)=(0,0)$, però $\|f'(c)\|=1$ per a tot $c$.
    resolució: Sigui $f(t)=(\cos t,\sin t)$, derivable a tot $\mathbb{R}$ amb $f'(t)=(-\sin t,\cos t)$. Prenem $a=0$, $b=2\pi$: $f(2\pi)-f(0)=(1,0)-(1,0)=(0,0)$. La igualtat demanaria $f'(c)\cdot2\pi=(0,0)$, és a dir $f'(c)=(0,0)$, però $\|f'(c)\|^2=\sin^2c+\cos^2c=1$ per a tot $c$. Per tant no existeix cap $c$. El Teorema 25 només assegura la igualtat després de projectar sobre un vector $u$ fix, $\langle u,f(b)-f(a)\rangle=\langle u,Jf(\xi)(b-a)\rangle$, amb un $\xi$ que depèn de $u$: cada component té el seu propi punt intermedi.
    pista: Aplica el teorema d'una variable a cada component per separat: el punt intermedi que obtens és el mateix per a les dues?
    teoria citada: T3.25
[6] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ contínua i $F(y)=\int_0^1f(x,y)\,dx$. Aleshores $F$ és derivable a tot $\mathbb{R}$.
    veredicte declarat: fals
    contraexemple: $f(x,y)=|y|$: és contínua, però $F(y)=\int_0^1|y|\,dx=|y|$ no és derivable a $y=0$.
    resolució: Prenem $f(x,y)=|y|$, contínua a $\mathbb{R}^2$. Aleshores $F(y)=\int_0^1|y|\,dx=|y|$. A $y=0$, $\frac{F(t)-F(0)}{t}=\frac{|t|}{t}$ té límit $1$ per la dreta i $-1$ per l'esquerra, així que $F'(0)$ no existeix. La regla de Leibniz (Teorema 32) demana $f\in\mathcal{C}^1$; la continuïtat de $f$ només dona la continuïtat de $F$, no la derivabilitat.
    pista: Quina hipòtesi demana la regla de Leibniz sobre $f$? Què passa si $f$ no depèn de $x$?
    teoria citada: T3.32, T3.15
[7] Sigui $\Omega=\mathbb{R}^2\setminus\{(0,0)\}$ i $f:\Omega\to\mathbb{R}$ diferenciable a $\Omega$ amb $\nabla f(p)=(0,0)$ per a tot $p\in\Omega$. Aleshores $f$ és constant a $\Omega$.
    veredicte declarat: cert
    resolució: $\Omega$ és obert. Vegem que és pre-convex. Siguin $a,b\in\Omega$. Si $(0,0)\notin[a,b]$, ja està. Si $(0,0)\in[a,b]$, aleshores $a$, $b$ i l'origen són sobre una mateixa recta $r$. Prenem $c\notin r$. El segment $[a,c]$ no conté l'origen: si el contingués, $c$ seria sobre la recta que passa per $a$ i l'origen, que és $r$. Igualment $[c,b]$ no conté l'origen. Així $[a,c]\cup[c,b]\subseteq\Omega$ i $\Omega$ és pre-convex. Com que $Jf(p)=\nabla f(p)=0$ a tot $\Omega$, el Corol·lari 28 dona que $f$ és constant a $\Omega$. (Treure un punt no desconnecta el pla, a diferència de treure una recta.)
    pista: Quina hipòtesi geomètrica sobre $\Omega$ demana el resultat que relaciona jacobiana nul·la i funció constant? La compleix el pla sense un punt?
    teoria citada: T3.27, T3.28, T3.29
[8] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ diferenciable a $a\in\mathbb{R}^2$. Aleshores existeix un vector unitari $u\in\mathbb{R}^2$ tal que $D_uf(a)=0$.
    veredicte declarat: cert
    resolució: Com que $f$ és diferenciable a $a$, per la Proposició 9 tenim $D_uf(a)=\langle\nabla f(a),u\rangle$ per a tot $u\neq0$. Si $\nabla f(a)=(p,q)\neq(0,0)$, prenem $u=\frac{(-q,p)}{\sqrt{p^2+q^2}}$, unitari i ortogonal a $\nabla f(a)$, i aleshores $D_uf(a)=\frac{-pq+qp}{\sqrt{p^2+q^2}}=0$. Si $\nabla f(a)=(0,0)$, qualsevol $u$ unitari serveix. (És la direcció tangent a la corba de nivell, Proposició 13.)
    pista: Com s'expressa $D_uf(a)$ en termes del gradient quan $f$ és diferenciable? Quins vectors anul·len aquesta expressió?
    teoria citada: T3.9, T3.13
[9] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ diferenciable a $(0,0)$ amb $D_{(1,1)}f(0,0)=3$ i $D_{(1,-1)}f(0,0)=1$. Aleshores $\frac{\partial f}{\partial x}(0,0)=2$.
    veredicte declarat: cert
    resolució: Per diferenciabilitat (Observació 11), $D_{(1,1)}f(0,0)=\frac{\partial f}{\partial x}(0,0)+\frac{\partial f}{\partial y}(0,0)=3$ i $D_{(1,-1)}f(0,0)=\frac{\partial f}{\partial x}(0,0)-\frac{\partial f}{\partial y}(0,0)=1$. Sumant, $2\frac{\partial f}{\partial x}(0,0)=4$, és a dir $\frac{\partial f}{\partial x}(0,0)=2$ (i $\frac{\partial f}{\partial y}(0,0)=1$). Observeu que els vectors no són unitaris, però la fórmula $D_uf(a)=\langle\nabla f(a),u\rangle$ val per a tot $u\neq0$.
    pista: Escriu cada dada com una combinació de les derivades parcials. Quin sistema obtens?
    teoria citada: T3.9, T3.11, T3.5
[10] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ tal que $\frac{\partial f}{\partial x}$ i $\frac{\partial f}{\partial y}$ existeixen a tot punt de $\mathbb{R}^2$ i existeix $M>0$ amb $\left|\frac{\partial f}{\partial x}(p)\right|\leq M$ i $\left|\frac{\partial f}{\partial y}(p)\right|\leq M$ per a tot $p\in\mathbb{R}^2$. Aleshores $f$ és contínua a $\mathbb{R}^2$.
    veredicte declarat: cert
    resolució: Sigui $(x_0,y_0)\in\mathbb{R}^2$. Escrivim $|f(x,y)-f(x_0,y_0)|\leq|f(x,y)-f(x_0,y)|+|f(x_0,y)-f(x_0,y_0)|$. La funció d'una variable $t\mapsto f(t,y)$ és derivable a tot $\mathbb{R}$ amb derivada $\frac{\partial f}{\partial x}(t,y)$; pel teorema del valor mitjà d'una variable, $|f(x,y)-f(x_0,y)|\leq M|x-x_0|$. Anàlogament, $t\mapsto f(x_0,t)$ dona $|f(x_0,y)-f(x_0,y_0)|\leq M|y-y_0|$. Per tant $|f(x,y)-f(x_0,y_0)|\leq M(|x-x_0|+|y-y_0|)\to0$ quan $(x,y)\to(x_0,y_0)$, i $f$ és contínua a $(x_0,y_0)$. La clau és que les parcials existeixen a tot arreu (no només en un punt, com a l'Observació 16) i estan fitades.
    pista: Pots anar de $(x_0,y_0)$ a $(x,y)$ movent primer una sola coordenada i després l'altra? Què et diu sobre cada tram una derivada fitada?
    teoria citada: T3.2, T3.16
[11] Siguin $f,g:\mathbb{R}^2\to\mathbb{R}$ i $a\in\mathbb{R}^2$. Si $f$ és diferenciable a $a$ amb $f(a)=0$ i $g$ és contínua a $a$, aleshores el producte $fg$ és diferenciable a $a$.
    veredicte declarat: cert
    resolució: Proposem $L=g(a)Df(a)$. Com que $f(a)=0$, $(fg)(a)=0$ i $(fg)(x)-0-g(a)Df(a)(x-a)=f(x)\,(g(x)-g(a))+g(a)\,(f(x)-f(a)-Df(a)(x-a))$. Dividint per $\|x-a\|$: el segon terme tendeix a $0$ per la diferenciabilitat de $f$. Per al primer, per la Proposició 14 existeixen $\delta,M>0$ amb $|f(x)|=|f(x)-f(a)|\leq M\|x-a\|$ si $\|x-a\|<\delta$; per tant $\frac{|f(x)|\,|g(x)-g(a)|}{\|x-a\|}\leq M|g(x)-g(a)|\to0$ per la continuïtat de $g$. Així $fg$ és diferenciable a $a$ amb $D(fg)(a)=g(a)Df(a)$. Per exemple, $x\,|y|$ és diferenciable a l'origen tot i que $|y|$ no ho és.
    pista: Quina hauria de ser la diferencial del producte si imites la regla del producte? Quina mida té $f(x)$ quan $x$ és a prop de $a$?
    teoria citada: T3.8, T3.14, T3.23
</questionari>

## Output

Write tema-3.normal.audit.json following this schema:

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

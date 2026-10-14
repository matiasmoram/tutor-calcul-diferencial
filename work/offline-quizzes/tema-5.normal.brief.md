# Writer brief: tema-5, normal (8 statements in the quiz)

## Instructions

Ets un professor de Càlcul Diferencial (FME-UPC, primer curs de grau) que prepara un qüestionari "Cert o fals" en català.
Cada afirmació és un enunciat matemàtic general; l'alumne l'haurà de DEMOSTRAR si és cert o REFUTAR amb un CONTRAEXEMPLE si és fals.
Model: «Si existeixen els dos límits iterats a $(0,0)$ i són iguals, aleshores existeix el límit doble» (fals: $\frac{xy}{x^2+y^2}$).

Requisits de cada afirmació:
- Autocontinguda i ben plantejada: fixa el domini i l'espai ($f:\mathbb{R}^2\to\mathbb{R}$, $A\subseteq\mathbb{R}^n$...), sense ambigüitats ni convencions implícites. Ha de tenir un valor de veritat clar amb les definicions dels apunts.
- Conceptualment interessant: el tipus d'enunciat que un alumne es creuria (un recíproc, un teorema sense una hipòtesi, una conclusió massa forta, quantificadors canviats, informació parcial presa per suficient, una propietat d'una variable que falla en diverses), o un fet cert que costa de veure.
- Variada: conceptes diferents del tema i tipus de trampa diferents; cap afirmació no pot ser una variant trivial d'una altra.
- Les falses han de tenir un contraexemple EXPLÍCIT i senzill (funció donada per una fórmula, conjunt concret), el més estàndard possible. Les certes, una demostració curta (com a molt 8 línies) a partir dels apunts.
- Fórmules en LaTeX entre $...$ (mai $$). Català correcte.

Camps:
- "enunciat": l'afirmació, sense dir si és certa ni donar cap pista.
- "veredicte": "cert" o "fals". "trampa": el tipus d'enunciat.
- "concepte": el concepte en 2-5 paraules (es mostra a l'alumne: no pot revelar el veredicte), p. ex. "Límits iterats".
- "contraexemple": per a les falses, el contraexemple (la funció o el conjunt i què hi falla, breu). Per a les certes, "".
- "resolucio": la resolució completa i rigorosa: per a les falses, comprova que el contraexemple compleix les hipòtesis i no la conclusió; per a les certes, la demostració.
- "idees_clau": 1-4 punts que una resposta correcta ha de contenir (rúbrica per corregir), p. ex. "els dos iterats valen 0", "sobre $y=mx$ el límit depèn de $m$".
- "pista": una pregunta socràtica que ajudi a pensar-hi SENSE revelar el veredicte (no diguis "cert", "fals" ni "contraexemple").
- "teoria": els ítems dels apunts que fa servir la resolució (pot ser buida).
- "comprovacions": per a les falses, TOTS els càlculs concrets del contraexemple que es puguin comprovar amb sympy (límits sobre camins, límits que no existeixen, derivades, igualtats), d'1 a 4; si el contraexemple no té cap càlcul comprovable (p. ex. topologia), []. Per a les certes, normalment []. Es comproven automàticament: una comprovació falsa fa descartar l'afirmació.

Sintaxi de les comprovacions (sympy, cap altra cosa):
- Operadors: + - * / ** (o ^), parèntesis. Multiplicació SEMPRE explícita: 2*x, x*y.
- Variables: x y z t m n k a b c r s u v w h p q (reals). Funcions: sin cos tan exp log sqrt Abs atan asin acos sinh cosh tanh sign Max Min floor cbrt diff limit; constants pi E oo.
- "limit": `expressio` ha de dependre d'UNA variable que tendeix al punt (els paràmetres com m poden quedar lliures); per a un camí, substitueix-lo: f(x,y)=x*y/(x**2+y**2) sobre y=m*x és "x*(m*x)/(x**2+(m*x)**2)", variable "x", punt "0", valor "m/(1+m**2)".
- "no_limit": el límit (d'una variable) no existeix: expressio "sin(1/y)", variable "y", punt "0", valor "".
- "igualtat": expressio i valor són iguals com a funcions: expressio "diff(x**2*y, x)", valor "2*x*y" (variable "", punt "").
- No escriguis funcions definides a trossos: comprova cada tros sobre la regió on s'aplica.


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

## Request

Cobreix el Tema 5 de manera variada.
Dificultat normal: cal pensar el paper de cada hipòtesi; contraexemples coneguts però no immediats.

Escriu EXACTAMENT 11 afirmacions noves, de les quals entre 5 i 7 falses.

## Output

A JSON file: {"font": "tema-5", "dificultat": "normal", "autor": "<your model>", "afirmacions": [...]}, each statement following this schema:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "afirmacions"
  ],
  "properties": {
    "afirmacions": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "enunciat",
          "veredicte",
          "trampa",
          "concepte",
          "contraexemple",
          "resolucio",
          "idees_clau",
          "pista",
          "teoria",
          "comprovacions"
        ],
        "properties": {
          "enunciat": {
            "type": "string"
          },
          "veredicte": {
            "type": "string",
            "enum": [
              "cert",
              "fals"
            ]
          },
          "trampa": {
            "type": "string",
            "enum": [
              "reciproc",
              "hipotesi_eliminada",
              "conclusio_mes_forta",
              "quantificadors",
              "informacio_parcial",
              "generalitzacio",
              "cert_resultat",
              "cert_demostracio"
            ]
          },
          "concepte": {
            "type": "string"
          },
          "contraexemple": {
            "type": "string"
          },
          "resolucio": {
            "type": "string"
          },
          "idees_clau": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "pista": {
            "type": "string"
          },
          "teoria": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "T1.1",
                "T1.2",
                "T1.3",
                "T1.4",
                "T1.5",
                "T1.6",
                "T1.7",
                "T1.8",
                "T1.9",
                "T1.10",
                "T1.11",
                "T1.12",
                "T1.13",
                "T1.14",
                "T1.15",
                "T1.16",
                "T1.17",
                "T1.18",
                "T1.19",
                "T1.20",
                "T1.21",
                "T1.22",
                "T1.23",
                "T1.24",
                "T1.25",
                "T1.26",
                "T1.27",
                "T1.28",
                "T1.29",
                "T1.30",
                "T1.31",
                "T1.32",
                "T1.33",
                "T1.34",
                "T1.35",
                "T1.36",
                "T1.37",
                "T2.1",
                "T2.2",
                "T2.3",
                "T2.4",
                "T2.5",
                "T2.6",
                "T2.7",
                "T2.8",
                "T2.9",
                "T2.10",
                "T2.11",
                "T2.12",
                "T2.13",
                "T2.14",
                "T2.15",
                "T2.16",
                "T2.17",
                "T2.18",
                "T2.19",
                "T2.20",
                "T2.21",
                "T2.22",
                "T2.23",
                "T2.24",
                "T2.25",
                "T2.26",
                "T2.27",
                "T2.28",
                "T2.29",
                "T2.30",
                "T2.31",
                "T2.32",
                "T2.33",
                "T2.34",
                "T2.35",
                "T2.36",
                "T2.37",
                "T2.38",
                "T2.39",
                "T2.40",
                "T3.1",
                "T3.2",
                "T3.3",
                "T3.4",
                "T3.5",
                "T3.6",
                "T3.7",
                "T3.8",
                "T3.9",
                "T3.10",
                "T3.11",
                "T3.12",
                "T3.13",
                "T3.14",
                "T3.15",
                "T3.16",
                "T3.17",
                "T3.18",
                "T3.19",
                "T3.20",
                "T3.21",
                "T3.22",
                "T3.23",
                "T3.24",
                "T3.25",
                "T3.26",
                "T3.27",
                "T3.28",
                "T3.29",
                "T3.30",
                "T3.31",
                "T3.32",
                "T3.33",
                "T3.34",
                "T4.1",
                "T4.2",
                "T4.3",
                "T4.4",
                "T4.5",
                "T4.6",
                "T4.7",
                "T4.8",
                "T4.9",
                "T4.10",
                "T4.11",
                "T4.12",
                "T4.13",
                "T4.14",
                "T4.15",
                "T4.16",
                "T4.17",
                "T4.18",
                "T4.19",
                "T4.20",
                "T4.21",
                "T5.1",
                "T5.2",
                "T5.3",
                "T5.4",
                "T5.5",
                "T5.6",
                "T5.7",
                "T5.8",
                "T5.9",
                "T5.10",
                "T5.11",
                "T5.12",
                "T5.13",
                "T5.14",
                "T5.15",
                "T5.16",
                "T5.17",
                "T5.18",
                "T5.19",
                "T5.20",
                "T5.21",
                "T5.22",
                "T5.23",
                "T5.24",
                "T5.25",
                "T5.26",
                "T5.27",
                "T5.28",
                "T5.29",
                "T5.30",
                "T5.31",
                "T5.32",
                "T5.33",
                "T5.34",
                "T5.35"
              ]
            }
          },
          "comprovacions": {
            "type": "array",
            "items": {
              "type": "object",
              "additionalProperties": false,
              "required": [
                "descripcio",
                "tipus",
                "expressio",
                "variable",
                "punt",
                "costat",
                "valor"
              ],
              "properties": {
                "descripcio": {
                  "type": "string",
                  "description": "Què es comprova, en català (p. ex. 'límit sobre la recta y=mx')."
                },
                "tipus": {
                  "type": "string",
                  "enum": [
                    "limit",
                    "no_limit",
                    "igualtat"
                  ]
                },
                "expressio": {
                  "type": "string",
                  "description": "Sintaxi sympy, una sola variable lliure per als límits (substitueix el camí)."
                },
                "variable": {
                  "type": "string",
                  "description": "Variable del límit; '' per a igualtat."
                },
                "punt": {
                  "type": "string",
                  "description": "Punt del límit (p. ex. '0', 'oo'); '' per a igualtat."
                },
                "costat": {
                  "type": "string",
                  "enum": [
                    "ambdos",
                    "dreta",
                    "esquerra"
                  ]
                },
                "valor": {
                  "type": "string",
                  "description": "Valor esperat (límit o costat dret de la igualtat); '' per a no_limit."
                }
              }
            }
          }
        }
      }
    }
  }
}
```

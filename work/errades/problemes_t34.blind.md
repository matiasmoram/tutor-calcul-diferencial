## t3-7:dificil

### Referència

<solucio_de_referencia>
ENUNCIAT: Estudieu la continuïtat i la diferenciabilitat de la funció
$$f(x,y)=\begin{cases}\dfrac{x|y|}{\sqrt{x^2+y^2}} & \text{si } (x,y)\neq(0,0)\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$
RESULTAT CORRECTE: $f$ és contínua a tot $\mathbb{R}^2$. És diferenciable exactament a $\{(x,y): y\neq0\}$: no és diferenciable en cap punt de l'eix $y=0$. Als punts $(x_0,0)$, $x_0\neq0$, no existeix $\partial f/\partial y$; a l'origen les parcials valen $0$ però $\dfrac{f(x,y)}{\|(x,y)\|}=\dfrac{x|y|}{x^2+y^2}$ no tendeix a $0$ (per exemple val $\pm\frac12$ sobre $y=x$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [continuitat_fora] Continuïtat fora de l'origen  (teoria: T2.19, T2.20)
     objectiu: Justificar la continuïtat als punts $(x,y)\neq(0,0)$.
     idea: Fora de l'origen $f$ és una combinació (productes, quocients, composicions) de funcions contínues amb denominador no nul.
     detall: $x$, $|y|$ i $\sqrt{x^2+y^2}$ són contínues i el denominador no s'anul·la a $\mathbb{R}^2\setminus\{(0,0)\}$, per tant $f$ hi és contínua.
  2. [continuitat_origen] Continuïtat a l'origen  (teoria: T2.14)
     objectiu: Decidir si $\lim_{(x,y)\to(0,0)}f(x,y)=0$.
     idea: Fita el mòdul del quocient: compara un dels factors del numerador amb el denominador.
     detall: $|x|\le\sqrt{x^2+y^2}$, per tant $|f(x,y)|\le|y|\to0$. Per sandvitx el límit és $0=f(0,0)$: $f$ és contínua a l'origen, i doncs a tot $\mathbb{R}^2$.
  3. [diferenciable_fora_eix] Diferenciabilitat on y no és zero  (teoria: T3.18)
     objectiu: Estudiar la diferenciabilitat als punts amb $y\neq0$.
     idea: En un entorn d'un punt amb $y\neq0$, el valor absolut té un signe fix: estudia la regularitat de les parcials allà.
     detall: A l'obert $\{y>0\}$ (resp. $\{y<0\}$), $f=\pm\dfrac{xy}{\sqrt{x^2+y^2}}$, amb parcials contínues (quocients de funcions $\mathcal C^1$, denominador no nul). Per la condició suficient, $f$ és diferenciable a tot punt amb $y\neq0$.
  4. [eix_sense_origen] Punts de l'eix fora de l'origen  (teoria: T3.2, T3.9)
     objectiu: Estudiar la diferenciabilitat als punts $(x_0,0)$ amb $x_0\neq0$.
     idea: Si fos diferenciable, existirien totes les parcials. Calcula la parcial respecte de $y$ amb la definició i mira els límits laterals.
     detall: $\dfrac{f(x_0,t)-f(x_0,0)}{t}=\dfrac{x_0|t|}{t\sqrt{x_0^2+t^2}}\to\pm\dfrac{x_0}{|x_0|}$ quan $t\to0^\pm$: els laterals són $\pm1$ (amb signe de $x_0$), no existeix $\partial f/\partial y(x_0,0)$. Per tant no és diferenciable.
  5. [origen] Diferenciabilitat a l'origen  (teoria: T3.8, T3.9, T2.10)
     objectiu: Decidir si $f$ és diferenciable a $(0,0)$.
     idea: Calcula les parcials a l'origen per obtenir l'única candidata a diferencial i estudia el límit de la definició amb aquesta candidata.
     detall: $f(t,0)=f(0,t)=0$, així $\nabla f(0,0)=(0,0)$ i la candidata és $Df(0,0)=0$. Cal $\dfrac{f(x,y)}{\sqrt{x^2+y^2}}=\dfrac{x|y|}{x^2+y^2}\to0$, però sobre $y=x$ val $\dfrac{x|x|}{2x^2}=\pm\dfrac12$. No és diferenciable a l'origen. (Equivalentment: $D_uf(0,0)=u_1|u_2|$ per a $u$ unitari, que no és lineal en $u$.)
ERRORS COMUNS:
  - [parcials_implica_diferenciable] A l'origen calcula que les parcials existeixen (i valen $0$) i conclou que és diferenciable.
  - [oblida_eix] Només estudia l'origen i diu que fora és diferenciable "per ser composició de funcions diferenciables", oblidant que $|y|$ no és derivable a $y=0$.
  - [camins_rectes_continuitat] Conclou la continuïtat a l'origen només provant rectes.

TEORIA DEL CURS QUE FA SERVIR:
[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$

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

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

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

[T2.10] Proposició 10 (Tema 2) — Límit per camins
Límit per camins. Si $F:D\subseteq\mathbb{R}^2\longrightarrow\mathbb{R}^m$ i $(a,b)\in D'$ tal que $\displaystyle\exists\lim_{(x,y)\to(a,b)}F(x,y)=L$, llavors per a tota funció real i contínua $g$ definida en un entorn d'$a$, tal que $g(a)=b$, es compleix que
$$\lim_{x\to a}F(x,g(x))=L.$$
</solucio_de_referencia>

### Document a revisar

[1] Fora de l'origen, les funcions $x$, $|y|$ i $\sqrt{x^2+y^2}$ són contínues i el denominador no s'anul·la a $\mathbb{R}^2\setminus\{(0,0)\}$, de manera que $f$ hi és contínua.
[2] A l'origen, sobre les rectes $y=mx$ tenim $f(x,mx)=\dfrac{x\,|m|\,|x|}{|x|\sqrt{1+m^2}}=\dfrac{|m|\,x}{\sqrt{1+m^2}}\to0$, i sobre l'eix $x=0$ la funció val $0$. Per tant el límit a l'origen és $0=f(0,0)$ i $f$ és contínua a tot $\mathbb{R}^2$.
[3] A l'obert $\{y>0\}$ tenim $f=\dfrac{xy}{\sqrt{x^2+y^2}}$, amb $\dfrac{\partial f}{\partial x}=\dfrac{y^3}{(x^2+y^2)^{3/2}}$ i $\dfrac{\partial f}{\partial y}=\dfrac{x^3}{(x^2+y^2)^{3/2}}$; a l'obert $\{y<0\}$ són les mateixes amb el signe canviat. Com que les dues derivades parcials existeixen a tot punt d'aquests oberts, $f$ és diferenciable a tot punt amb $y\neq0$.
[4] En un punt $(x_0,0)$ amb $x_0\neq0$: $\dfrac{f(x_0,t)-f(x_0,0)}{t}=\dfrac{x_0|t|}{t\sqrt{x_0^2+t^2}}$, que tendeix a $\dfrac{x_0}{|x_0|}$ quan $t\to0^+$ i a $-\dfrac{x_0}{|x_0|}$ quan $t\to0^-$. Els límits laterals són diferents, no existeix $\dfrac{\partial f}{\partial y}(x_0,0)$ i, per tant, $f$ no és diferenciable en aquests punts.
[5] A l'origen, $f(t,0)=0$ i $f(0,t)=0$ per a tot $t$, així que $\nabla f(0,0)=(0,0)$ i l'única candidata a diferencial és l'aplicació lineal nul·la.
[6] Per a la diferenciabilitat a l'origen cal que $\dfrac{f(x,y)}{x^2+y^2}=\dfrac{x|y|}{(x^2+y^2)^{3/2}}$ tendeixi a $0$. Sobre la recta $y=x$, amb $x>0$, val $\dfrac{x^2}{2\sqrt2\,x^3}=\dfrac{1}{2\sqrt2\,x}\to+\infty$, de manera que $f$ no és diferenciable a l'origen.
[7] En resum, $f$ és contínua a tot $\mathbb{R}^2$ i és diferenciable exactament als punts amb $y\neq0$: no ho és en cap punt de l'eix $y=0$.


## t3-12:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem la funció $f(x,y)=(xy^{3/2},\ x^{3/2}-y^2)$. Justifiqueu que és diferenciable en un entorn del punt $(4,1)$, calculeu l'aproximació lineal de $f$ en el punt $(4,1)$, i useu-la per calcular una aproximació de $f(4.2,1.1)$.
RESULTAT CORRECTE: En l'obert $\{x>0,\ y>0\}$, que conté $(4,1)$, les quatre derivades parcials existeixen i són contínues, per tant $f$ hi és diferenciable. Amb $f(4,1)=(4,7)$ i $Jf(4,1)=\begin{pmatrix}1&6\\3&-2\end{pmatrix}$, l'aproximació lineal és
$L(x,y)=(4,7)+\begin{pmatrix}1&6\\3&-2\end{pmatrix}\begin{pmatrix}x-4\\y-1\end{pmatrix}=\big(4+(x-4)+6(y-1),\ 7+3(x-4)-2(y-1)\big)$,
i $f(4.2,1.1)\approx L(4.2,1.1)=(4.8,\ 7.4)$ (el valor exacte és $\approx(4.8455,\ 7.3974)$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [diferenciable] Justificar la diferenciabilitat  (teoria: T3.18, T2.20)
     objectiu: Justificar que $f$ és diferenciable en tot un entorn de $(4,1)$.
     idea: Busca un obert al voltant de $(4,1)$ on les expressions de les components siguin derivables sense problemes (atenció a les potències d'exponent $3/2$) i aplica la condició suficient de diferenciabilitat.
     detall: A l'obert $U=\{x>0,\ y>0\}\ni(4,1)$ les parcials $\frac{\partial f_1}{\partial x}=y^{3/2}$, $\frac{\partial f_1}{\partial y}=\frac32xy^{1/2}$, $\frac{\partial f_2}{\partial x}=\frac32x^{1/2}$, $\frac{\partial f_2}{\partial y}=-2y$ existeixen i són contínues (composicions i productes de funcions contínues). Per la condició suficient, $f$ és diferenciable a tot $U$.
  2. [jacobiana] Matriu jacobiana al punt  (teoria: T3.9, T3.10)
     objectiu: Calcular $f(4,1)$ i la matriu de la diferencial de $f$ a $(4,1)$.
     idea: Avalua les derivades parcials de cada component al punt: la fila $i$ correspon a la component $f_i$.
     detall: $f(4,1)=(4\cdot1,\ 8-1)=(4,7)$ i $Jf(4,1)=\begin{pmatrix}1&6\\3&-2\end{pmatrix}$ (perquè $\frac32\cdot4\cdot1=6$ i $\frac32\cdot\sqrt4=3$).
  3. [aproximacio_lineal] Escriure l'aproximació lineal  (teoria: T3.x4)
     objectiu: Escriure la funció afí que aproxima $f$ prop de $(4,1)$.
     idea: És el valor al punt més la diferencial aplicada a l'increment $(x-4,\ y-1)$.
     detall: $L(x,y)=(4,7)+\begin{pmatrix}1&6\\3&-2\end{pmatrix}\begin{pmatrix}x-4\\y-1\end{pmatrix}=\big(4+(x-4)+6(y-1),\ 7+3(x-4)-2(y-1)\big)$.
  4. [avaluar] Avaluar l'aproximació
     objectiu: Usar l'aproximació lineal per estimar $f(4.2,1.1)$.
     idea: Calcula l'increment respecte del punt base i substitueix-lo a l'aproximació lineal.
     detall: Increment $(0.2,\ 0.1)$: $L(4.2,1.1)=(4+0.2+0.6,\ 7+0.6-0.2)=(4.8,\ 7.4)$. (Valor exacte $\approx(4.8455,\ 7.3974)$.)
ERRORS COMUNS:
  - [increment_malament] Substitueix $(4.2,\ 1.1)$ directament a la matriu jacobiana en lloc de l'increment $(0.2,\ 0.1)$.
  - [jacobiana_transposada] Escriu la jacobiana transposada (posa les derivades d'una mateixa component en una columna).
  - [diferenciable_sense_justificar] Diu que és diferenciable "perquè és una funció elemental" sense mirar on són contínues les parcials (amb potències $3/2$ el domini importa).

TEORIA DEL CURS QUE FA SERVIR:
[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$

[T3.x4] Apunts del Tema 3, §3.1 — Reformulació epsilon-delta i aproximació afí
És a dir, en altres paraules, si $\forall\varepsilon>0$ $\exists\delta=\delta(\varepsilon)>0$ tal que si $x\in\Omega$ amb $\|x-a\|<\delta$ aleshores $\|f(x)-(f(a)+Df(a)(x-a))\|\leq\varepsilon\|x-a\|$.

Per tant, si $f$ és diferenciable al punt $a$, per a valors d'$x$ propers a $a$ la funció $f(x)$ es pot aproximar per la funció afí $f(a)+Df(a)(x-a)$.

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

[T2.20] Proposició 20 (Tema 2) — Àlgebra de funcions contínues
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $h:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, contínues. Llavors

(i) $f+g,\ \lambda f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $\lambda\in\mathbb{R}$, són contínues;

(ii) $hf:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ és contínua;

(iii) per a $m=1$, si $g(x)\neq0\ \forall x\in\Omega$, $f/g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(iv) $\langle f,g\rangle:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(v) $\|f\|:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua.

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
</solucio_de_referencia>

### Document a revisar

[1] Les components de $f$ són $f_1(x,y)=xy^{3/2}$ i $f_2(x,y)=x^{3/2}-y^2$. Hem de justificar la diferenciabilitat a prop de $(4,1)$, escriure l'aproximació lineal en aquest punt i avaluar-la en $(4.2,1.1)$.
[2] Les dues components són sumes i productes de potències de $x$ i de $y$, que són funcions elementals; per tant $f$ és diferenciable a tot $\mathbb{R}^2$, i en particular en un entorn de $(4,1)$.
[3] Les derivades parcials són $\frac{\partial f_1}{\partial x}=y^{3/2}$, $\frac{\partial f_1}{\partial y}=\frac32xy^{1/2}$, $\frac{\partial f_2}{\partial x}=\frac32x^{1/2}$ i $\frac{\partial f_2}{\partial y}=-2y$. Al punt, com que $\frac32\cdot4\cdot1=6$ i $\frac32\sqrt4=3$, queda $Jf(4,1)=\begin{pmatrix}1&6\\3&-2\end{pmatrix}$.
[4] A més, $f(4,1)=(4\cdot1,\ 4^{3/2}-1)=(4,7)$, i l'aproximació lineal és $L(x,y)=(4,7)+\begin{pmatrix}1&6\\3&-2\end{pmatrix}\begin{pmatrix}x-4\\y-1\end{pmatrix}=\big(4+(x-4)+6(y-1),\ 7+3(x-4)-2(y-1)\big)$.
[5] Per aproximar $f(4.2,1.1)$ apliquem la jacobiana al punt: $f(4.2,1.1)\approx(4+4.2+6\cdot1.1,\ 7+3\cdot4.2-2\cdot1.1)=(14.8,\ 17.4)$.
[6] Per tant, l'aproximació lineal dona $f(4.2,1.1)\approx(14.8,\ 17.4)$.


## t3-13:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Calculeu un valor aproximat de $\sqrt{3+e^{-0.1}\cos0.05+5\sin0.05}$.
RESULTAT CORRECTE: Amb $f(x,y)=\sqrt{3+e^x\cos y+5\sin y}$ al voltant de $(0,0)$: $f(0,0)=2$, $\nabla f(0,0)=(1/4,\ 5/4)$, i
$\sqrt{3+e^{-0.1}\cos0.05+5\sin0.05}\approx2+\frac14(-0.1)+\frac54(0.05)=2.0375$ (el valor exacte és $\approx2.0380$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [triar_funcio] Triar la funció i el punt base
     objectiu: Escriure el nombre com el valor d'una funció de diverses variables en un punt proper a un punt on la funció és fàcil d'avaluar.
     idea: Substitueix els nombres petits ($-0.1$ i $0.05$) per variables i pren com a punt base aquell on aquestes variables valen $0$.
     detall: $f(x,y)=\sqrt{3+e^x\cos y+5\sin y}$, punt base $(0,0)$, on $f(0,0)=\sqrt{3+1+0}=2$; volem $f(-0.1,\ 0.05)$.
  2. [diferenciable] Justificar la diferenciabilitat  (teoria: T3.18)
     objectiu: Veure que la funció és diferenciable al punt base, per poder-hi fer servir l'aproximació afí.
     idea: Mira si les parcials existeixen i són contínues en un entorn del punt base (l'argument de l'arrel hi ha de ser positiu).
     detall: Prop de $(0,0)$ l'argument de l'arrel és proper a $4>0$, així que $f$ és composició de funcions $\mathcal{C}^1$ amb parcials contínues; per la condició suficient, és diferenciable a $(0,0)$.
  3. [gradient] Calcular el gradient  (teoria: T3.9, T3.10)
     objectiu: Calcular les derivades parcials de $f$ al punt base.
     idea: Deriva l'arrel per la regla de la cadena d'una variable i avalua a l'origen.
     detall: $\frac{\partial f}{\partial x}=\frac{e^x\cos y}{2f}$, $\frac{\partial f}{\partial y}=\frac{-e^x\sin y+5\cos y}{2f}$; a $(0,0)$: $\nabla f(0,0)=(1/4,\ 5/4)$.
  4. [aproximar] Aproximar  (teoria: T3.x4)
     objectiu: Obtenir el valor aproximat.
     idea: Aproximació afí: valor al punt base més el gradient aplicat a l'increment.
     detall: $f(-0.1,\ 0.05)\approx2+\frac14(-0.1)+\frac54(0.05)=2-0.025+0.0625=2.0375$.
ERRORS COMUNS:
  - [punt_base_dolent] Pren un punt base on la funció no és fàcil d'avaluar o que no és proper al punt desitjat.
  - [signe_increment] Usa l'increment $+0.1$ en lloc de $-0.1$ per a la variable de l'exponencial.
  - [oblida_arrel] Aproxima només l'argument de l'arrel i oblida el factor $\frac{1}{2\sqrt{\cdot}}$ en derivar.

TEORIA DEL CURS QUE FA SERVIR:
[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

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

[T3.x4] Apunts del Tema 3, §3.1 — Reformulació epsilon-delta i aproximació afí
És a dir, en altres paraules, si $\forall\varepsilon>0$ $\exists\delta=\delta(\varepsilon)>0$ tal que si $x\in\Omega$ amb $\|x-a\|<\delta$ aleshores $\|f(x)-(f(a)+Df(a)(x-a))\|\leq\varepsilon\|x-a\|$.

Per tant, si $f$ és diferenciable al punt $a$, per a valors d'$x$ propers a $a$ la funció $f(x)$ es pot aproximar per la funció afí $f(a)+Df(a)(x-a)$.
</solucio_de_referencia>

### Document a revisar

[1] Considero $f(x,y)=\sqrt{3+e^x\cos y+5\sin y}$; el nombre que volem és $f(-0.1,\ 0.05)$. Com a punt base prenc $(0,0)$, proper al punt i on $f(0,0)=\sqrt{3+1+0}=2$.
[2] Prop de $(0,0)$ l'argument de l'arrel és proper a $4>0$ i $t\mapsto\sqrt t$ és $\mathcal{C}^1$ a $(0,+\infty)$; per tant $f$ té derivades parcials contínues en un entorn de $(0,0)$ i, per la condició suficient, és diferenciable a $(0,0)$.
[3] Derivant, $\dfrac{\partial f}{\partial x}=\dfrac{e^x\cos y}{2f}$ i $\dfrac{\partial f}{\partial y}=\dfrac{e^x\sin y+5\cos y}{2f}$.
[4] Al punt base, amb $f(0,0)=2$: $\nabla f(0,0)=\left(\dfrac{1}{4},\ \dfrac{5}{4}\right)$.
[5] L'aproximació lineal dona $f(-0.1,\ 0.05)\approx2+\frac14(0.05)+\frac54(-0.1)=2+0.0125-0.125=1.8875$.
[6] Per tant, $\sqrt{3+e^{-0.1}\cos0.05+5\sin0.05}\approx1.8875$.


## t3-16:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Calculeu tots els punts de $\mathbb{R}^2$ on la gràfica de la funció $f(x,y)=(1-\sin x)\,y+y^3$ té pla tangent paral·lel al pla $XY$. Escriviu també l'equació d'aquests plans tangents.
RESULTAT CORRECTE: $f$ és $\mathcal{C}^1$ a $\mathbb{R}^2$, així que té pla tangent a tot punt, i aquest és horitzontal si i només si $\nabla f=0$. Els punts són $\left(\frac{\pi}{2}+2k\pi,\ 0\right)$, $k\in\mathbb{Z}$, on $f=0$, i el pla tangent és en tots ells $z=0$ (el mateix pla $XY$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [diferenciable] Existència de pla tangent  (teoria: T3.18, T3.9)
     objectiu: Justificar que la gràfica té pla tangent a tot punt.
     idea: Comprova la condició suficient de diferenciabilitat.
     detall: $\frac{\partial f}{\partial x}=-y\cos x$ i $\frac{\partial f}{\partial y}=1-\sin x+3y^2$ són contínues a $\mathbb{R}^2$; $f$ és diferenciable a tot arreu i té pla tangent a cada punt.
  2. [condicio] Traduir 'paral·lel al pla XY'  (teoria: T3.9)
     objectiu: Escriure la condició perquè el pla tangent a $(a,f(a))$ sigui paral·lel al pla $XY$.
     idea: Mira l'equació del pla tangent: quan no depèn ni de $x$ ni de $y$?
     detall: El pla $z=f(a)+\frac{\partial f}{\partial x}(a)(x-a_1)+\frac{\partial f}{\partial y}(a)(y-a_2)$ és horitzontal si i només si $\nabla f(a)=(0,0)$.
  3. [resoldre] Resoldre el sistema
     objectiu: Trobar tots els punts on s'anul·len les dues derivades parcials.
     idea: Comença per l'equació que és una suma de termes de signe conegut.
     detall: $1-\sin x+3y^2=0$ amb $1-\sin x\ge0$ i $3y^2\ge0$ obliga $y=0$ i $\sin x=1$, és a dir $x=\frac{\pi}{2}+2k\pi$. Llavors $-y\cos x=0$ també es compleix. Punts: $\left(\frac{\pi}{2}+2k\pi,\ 0\right)$, $k\in\mathbb{Z}$.
  4. [plans] Equació dels plans  (teoria: T3.9)
     objectiu: Escriure l'equació del pla tangent en aquests punts.
     idea: Calcula el valor de $f$ en aquests punts.
     detall: $f\left(\frac{\pi}{2}+2k\pi,0\right)=0$, així que el pla tangent és $z=0$ en tots ells.
ERRORS COMUNS:
  - [perd_solucions] Només dona $x=\pi/2$ i oblida la periodicitat.
  - [cos_zero] De $-y\cos x=0$ afegeix punts amb $\cos x=0$ i $y\neq0$ sense comprovar l'altra equació.
  - [confon_condicio] Imposa $f=0$ en lloc de $\nabla f=0$.

TEORIA DEL CURS QUE FA SERVIR:
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

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.
</solucio_de_referencia>

### Document a revisar

[1] Les derivades parcials de $f$ són $\dfrac{\partial f}{\partial x}=y\cos x$ i $\dfrac{\partial f}{\partial y}=1-\sin x+3y^2$, contínues a tot $\mathbb{R}^2$. Per tant $f$ és diferenciable a tot arreu i la seva gràfica té pla tangent a cada punt.
[2] El pla tangent a la gràfica en $(a,f(a))$ és $z=f(a)+\frac{\partial f}{\partial x}(a)(x-a_1)+\frac{\partial f}{\partial y}(a)(y-a_2)$, i és paral·lel al pla $XY$ si i només si $\nabla f(a)=(0,0)$.
[3] Cal resoldre $y\cos x=0$ i $1-\sin x+3y^2=0$. A la segona equació, $1-\sin x\geq0$ i $3y^2\geq0$, i la suma només s'anul·la si tots dos termes són zero: $y=0$ i $\sin x=1$.
[4] De $\sin x=1$ obtenim $x=\frac{\pi}{2}$, i amb $y=0$ la primera equació també es compleix. L'únic punt és, doncs, $\left(\frac{\pi}{2},\ 0\right)$.
[5] En aquest punt $f\left(\frac{\pi}{2},0\right)=(1-1)\cdot0+0=0$ i el gradient s'anul·la, de manera que el pla tangent és $z=0$, el mateix pla $XY$.


## t3-21b:facil

### Referència

<solucio_de_referencia>
ENUNCIAT: Calculeu les derivades parcials $D_1F$, $D_2F$ de les funcions compostes següents:

(b) $F=f\circ g$, amb $f(x,y)=\dfrac{x+y}{1-xy}$, $g(u,v)=(\tan u,\tan v)$.
RESULTAT CORRECTE: On està definida ($\cos u\neq0$, $\cos v\neq0$ i $\tan u\tan v\neq1$; amb les dues primeres, la tercera equival a $\cos(u+v)\neq0$):
$D_1F(u,v)=\frac{(1+\tan^2u)(1+\tan^2v)}{(1-\tan u\tan v)^2}=\frac{1}{\cos^2(u+v)}$, i $D_2F(u,v)=\frac{1}{\cos^2(u+v)}$ igualment. (De fet $F(u,v)=\tan(u+v)$.)
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [domini] Domini i diferenciabilitat  (teoria: T3.18, T3.21)
     objectiu: Determinar on està definida $F$ i on es pot aplicar la regla de la cadena.
     idea: Cal que $g$ estigui definida i que el seu valor caigui on $f$ és diferenciable.
     detall: $g$ és $\mathcal{C}^1$ on $\cos u\neq0\neq\cos v$; $f$ és $\mathcal{C}^1$ a l'obert $xy\neq1$. Així $F$ està definida i és diferenciable (regla de la cadena) on $\cos u\neq0$, $\cos v\neq0$ i $\tan u\tan v\neq1$.
  2. [parcials_f] Parcials de f
     objectiu: Calcular $\frac{\partial f}{\partial x}$ i $\frac{\partial f}{\partial y}$.
     idea: Regla del quocient, i simplifica el numerador.
     detall: $\frac{\partial f}{\partial x}=\frac{(1-xy)+(x+y)y}{(1-xy)^2}=\frac{1+y^2}{(1-xy)^2}$, i per simetria $\frac{\partial f}{\partial y}=\frac{1+x^2}{(1-xy)^2}$.
  3. [cadena] Regla de la cadena  (teoria: T3.21, T3.22)
     objectiu: Obtenir $D_1F$ i $D_2F$.
     idea: $g$ té cada component dependent d'una sola variable; la jacobiana de $g$ és diagonal.
     detall: $D_1F=\frac{\partial f}{\partial x}(g)\cdot(1+\tan^2u)=\frac{(1+\tan^2v)(1+\tan^2u)}{(1-\tan u\tan v)^2}$, i $D_2F=\frac{(1+\tan^2u)(1+\tan^2v)}{(1-\tan u\tan v)^2}$.
  4. [simplificar] Simplificar
     objectiu: Simplificar l'expressió obtinguda.
     idea: Passa a sinus i cosinus i reconeix una fórmula d'addició.
     detall: $\frac{1}{\cos^2u\cos^2v(1-\tan u\tan v)^2}=\frac{1}{(\cos u\cos v-\sin u\sin v)^2}=\frac{1}{\cos^2(u+v)}$. Ambdues parcials valen el mateix (coherent amb $F=\tan(u+v)$).
ERRORS COMUNS:
  - [quocient_malament] Errors de signe en la regla del quocient (el denominador $1-xy$ té derivada $-y$).
  - [oblida_derivada_tan] Oblida multiplicar per la derivada de $\tan u$.
  - [domini] No esmenta on és vàlida la fórmula.

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

[1] $g$ és de classe $\mathcal{C}^1$ on $\cos u\neq0$ i $\cos v\neq0$, i $f$ és de classe $\mathcal{C}^1$ a l'obert $\{xy\neq1\}$. Per la regla de la cadena, $F=f\circ g$ és diferenciable als punts amb $\cos u\neq0$, $\cos v\neq0$ i $\tan u\tan v\neq1$.
[2] Derivant el quocient, $\dfrac{\partial f}{\partial x}=\dfrac{(1-xy)+(x+y)y}{(1-xy)^2}=\dfrac{1+y^2}{(1-xy)^2}$ i, per simetria, $\dfrac{\partial f}{\partial y}=\dfrac{1+x^2}{(1-xy)^2}$.
[3] A més, $\dfrac{d}{du}\tan u=1+\tan^2u$, i la segona component de $g$ no depèn de $u$. Per la regla de la cadena, $D_1F=\dfrac{\partial f}{\partial x}(g(u,v))\,(1+\tan^2u)=\dfrac{(1+\tan^2u)(1+\tan^2v)}{(1-\tan u\tan v)^2}$.
[4] Anàlogament, $D_2F=\dfrac{\partial f}{\partial y}(g(u,v))\,(1+\tan^2v)=\dfrac{(1+\tan^2u)(1+\tan^2v)}{(1-\tan u\tan v)^2}$.
[5] Per simplificar, usem $1+\tan^2u=\dfrac{1}{\cos^2u}$: $D_1F=\dfrac{1}{\cos^2u\cos^2v\,(1-\tan u\tan v)^2}=\dfrac{1}{(\cos u\cos v+\sin u\sin v)^2}$.
[6] Per tant, $D_1F(u,v)=D_2F(u,v)=\dfrac{1}{\cos^2(u-v)}$ a tots els punts on $F$ està definida.


## t3-22:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Calculeu, si existeix, la derivada en el punt zero de la funció $(f\circ\gamma)(t)$, on
$$f(x,y)=\begin{cases}\dfrac{x^2y}{x^2+y^2} & \text{si } (x,y)\neq(0,0),\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$
i $\gamma(t)=(t,t)$, $\forall t\in\mathbb{R}$. Raoneu si es pot obtenir el resultat aplicant la regla de la cadena.

Calculeu, si existeix, la derivada en el punt zero de la funció $(f\circ\gamma)(t)$, on
$$f(x,y)=\begin{cases}\dfrac{x^2y}{x^2+y^2} & \text{si } (x,y)\neq(0,0),\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$
i $\gamma(t)=(t,t)$, $\forall t\in\mathbb{R}$. Raoneu si es pot obtenir el resultat aplicant la regla de la cadena.
RESULTAT CORRECTE: $(f\circ\gamma)(t)=t/2$ per a tot $t$ (també a $t=0$), per tant $(f\circ\gamma)'(0)=1/2$. No es pot obtenir amb la regla de la cadena: $\frac{\partial f}{\partial x}(0,0)=\frac{\partial f}{\partial y}(0,0)=0$, de manera que la fórmula $\nabla f(0,0)\cdot\gamma'(0)$ donaria $0\neq 1/2$. La regla de la cadena no s'aplica perquè $f$ no és diferenciable a l'origen (si ho fos, $D_{(1,1)}f(0,0)$ hauria de ser $\nabla f(0,0)\cdot(1,1)=0$, i en canvi val $1/2$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [composicio] Escriure la composició
     objectiu: Obtenir una expressió explícita de $(f\circ\gamma)(t)$ per a tot $t\in\mathbb{R}$.
     idea: Substitueix $x=t$, $y=t$ a la fórmula de $f$, separant el cas $t=0$ (on $\gamma(0)$ és l'origen).
     detall: Per $t\neq0$: $(f\circ\gamma)(t)=\frac{t^2\cdot t}{t^2+t^2}=\frac{t}{2}$. Per $t=0$: $f(0,0)=0=\frac{0}{2}$. Per tant $(f\circ\gamma)(t)=t/2$ per a tot $t$.
  2. [derivada] Derivar a zero  (teoria: T3.x1)
     objectiu: Calcular $(f\circ\gamma)'(0)$, si existeix.
     idea: És una funció d'una variable: aplica la definició de derivada en una variable (o deriva l'expressió que has obtingut, vàlida a tot $\mathbb{R}$).
     detall: $(f\circ\gamma)'(0)=\lim_{t\to0}\frac{t/2-0}{t}=\frac12$. Existeix i val $1/2$.
  3. [parcials] Parcials de $f$ a l'origen  (teoria: T3.2)
     objectiu: Calcular les derivades parcials de $f$ a $(0,0)$, que és el que necessitaria la regla de la cadena.
     idea: A l'origen la funció està definida a part: usa la definició de derivada parcial com a límit, restringint $f$ als eixos.
     detall: $f(t,0)=0$ i $f(0,t)=0$ per a tot $t$, així que $\frac{\partial f}{\partial x}(0,0)=\lim_{t\to0}\frac{0-0}{t}=0$ i igualment $\frac{\partial f}{\partial y}(0,0)=0$. Per tant $\nabla f(0,0)=(0,0)$.
  4. [cadena] Per què falla la regla de la cadena  (teoria: T3.21, T3.9, T3.1)
     objectiu: Comparar el resultat amb el que donaria la regla de la cadena i explicar la diferència.
     idea: Escriu què donaria la fórmula $J(f\circ\gamma)(0)=Jf(\gamma(0))\,J\gamma(0)$ i revisa quines hipòtesis demana el teorema. Relaciona la derivada que has calculat amb una derivada direccional de $f$ a l'origen.
     detall: La fórmula donaria $\nabla f(0,0)\cdot\gamma'(0)=(0,0)\cdot(1,1)=0\neq\frac12$. No hi ha contradicció: la regla de la cadena exigeix que $f$ sigui diferenciable a $\gamma(0)=(0,0)$, i no ho és. En efecte, $(f\circ\gamma)'(0)=D_{(1,1)}f(0,0)=\frac12$, mentre que si $f$ fos diferenciable caldria $D_{(1,1)}f(0,0)=Df(0,0)(1,1)=\nabla f(0,0)\cdot(1,1)=0$. Per tant $f$ no és diferenciable a l'origen i el resultat no es pot obtenir amb la regla de la cadena.
ERRORS COMUNS:
  - [cadena_cega] Aplica la regla de la cadena sense comprovar hipòtesis i conclou que la derivada és $0$.
  - [parcials_implica_diferenciable] Creu que, com que existeixen les derivades parcials a l'origen, $f$ hi és diferenciable i la regla de la cadena s'hi pot aplicar.
  - [oblida_cas_origen] Usa la fórmula $\frac{x^2y}{x^2+y^2}$ també a l'origen o no comprova que $(f\circ\gamma)(0)=0$.

TEORIA DEL CURS QUE FA SERVIR:
[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$

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

[T3.1] Definició 1 (Tema 3) — Derivada direccional
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $a\in\mathring{\Omega}$, i $u\in\mathbb{R}^n\setminus\{0\}$. Es defineix la derivada direccional de $f$ en el punt $a$ segons la direcció i sentit del vector $u$ com
$$D_uf(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t},\tag{1}$$
si aquest límit existeix. (Nota: De fet, si definim $g(t)=f(a+tu)$, la funció $f$ restringida a la recta $\{a+tu\mid t\in\mathbb{R}\}$, aleshores $D_uf(a)=g'(0)$.)

[T3.17] Observació 17 (Tema 3) — Direccionals sense diferenciabilitat
Fins i tot l'existència de totes les derivades direccionals en un punt no implica la diferenciabilitat en aquell punt. Un exemple clàssic és aquest:
$$f(x,y)=\begin{cases}\dfrac{x^2y}{x^2+y^2} & \text{si } (x,y)\neq(0,0)\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$
</solucio_de_referencia>

### Document a revisar

[1] Per a $t\neq0$ tenim $\gamma(t)=(t,t)\neq(0,0)$, i $(f\circ\gamma)(t)=\dfrac{t^2\cdot t}{t^2+t^2}=\dfrac{t^3}{2t^2}=\dfrac{t}{2}$.
[2] Per a $t=0$, la mateixa expressió $\dfrac{t^3}{2t^2}$ avaluada en $t=0$ dona $0$, de manera que $(f\circ\gamma)(t)=\dfrac t2$ per a tot $t\in\mathbb{R}$.
[3] Aleshores $(f\circ\gamma)'(0)=\lim_{t\to0}\dfrac{t/2-0}{t}=\dfrac12$: la derivada existeix i val $\dfrac12$.
[4] Les parcials de $f$ a l'origen: $f(t,0)=0$ i $f(0,t)=0$ per a tot $t$, així que $\dfrac{\partial f}{\partial x}(0,0)=\dfrac{\partial f}{\partial y}(0,0)=0$ i $\nabla f(0,0)=(0,0)$.
[5] Si apliquéssim la regla de la cadena obtindríem $\nabla f(0,0)\cdot\gamma'(0)=(0,0)\cdot(1,1)=0$, que és diferent de $\dfrac12$.
[6] La regla de la cadena exigeix que $f$ sigui diferenciable a $\gamma(0)=(0,0)$, i aquí no ho és perquè $f$ no és contínua a l'origen: el límit de $\dfrac{x^2y}{x^2+y^2}$ quan $(x,y)\to(0,0)$ depèn del camí.
[7] Per tant $(f\circ\gamma)'(0)=\dfrac12$, i aquest resultat no es pot obtenir aplicant la regla de la cadena.


## t4-1:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Trobeu tots els punts $(x,y)\in\mathbb{R}^2$ tals que
$$\frac{\partial^2 f}{\partial x\partial y}(x,y)\neq\frac{\partial^2 f}{\partial y\partial x}(x,y)$$
on
$$f(x,y)=\begin{cases}\dfrac{xy(x^2-y^2)}{x^2+y^2} & \text{si } (x,y)\neq(0,0)\\ 0 & \text{altrament.}\end{cases}$$
RESULTAT CORRECTE: L'únic punt és l'origen $(0,0)$. Fora de l'origen $f$ és de classe $\mathcal{C}^\infty$ i les derivades creuades coincideixen pel teorema de Schwarz. A l'origen, $\frac{\partial f}{\partial x}(0,y)=-y$ i $\frac{\partial f}{\partial y}(x,0)=x$, de manera que derivar primer respecte de $x$ i després respecte de $y$ dona $-1$, mentre que derivar primer respecte de $y$ i després respecte de $x$ dona $1$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [fora_origen] Punts diferents de l'origen  (teoria: T5.6, T3.31)
     objectiu: Decidir què passa amb les derivades creuades en els punts $(x,y)\neq(0,0)$.
     idea: En l'obert $\mathbb{R}^2\setminus\{(0,0)\}$, $f$ és un quocient de polinomis amb denominador que no s'anul·la. Quin teorema garanteix la igualtat de les derivades creuades si són contínues?
     detall: A $\Omega=\mathbb{R}^2\setminus\{(0,0)\}$ (obert) $f$ és quocient de polinomis amb $x^2+y^2\neq 0$, per tant $f\in\mathcal{C}^\infty(\Omega)$; en particular les derivades segones existeixen i són contínues a $\Omega$. Pel teorema de Schwarz les dues derivades creuades coincideixen en tot punt de $\Omega$. L'únic punt candidat és $(0,0)$.
  2. [parcials_eixos] Derivades primeres sobre els eixos  (teoria: T3.2)
     objectiu: Obtenir $\frac{\partial f}{\partial x}$ sobre l'eix $x=0$ i $\frac{\partial f}{\partial y}$ sobre l'eix $y=0$ (incloent-hi l'origen).
     idea: Per derivar una segona vegada a l'origen només calen les primeres derivades al llarg d'un eix. Fora de l'origen es poden derivar amb les regles habituals; a l'origen cal la definició com a límit.
     detall: Per $(x,y)\neq(0,0)$: $\frac{\partial f}{\partial x}=\frac{y(x^4+4x^2y^2-y^4)}{(x^2+y^2)^2}$ i $\frac{\partial f}{\partial y}=\frac{x(x^4-4x^2y^2-y^4)}{(x^2+y^2)^2}$. A l'origen, $f(h,0)=f(0,k)=0$, per tant $\frac{\partial f}{\partial x}(0,0)=\frac{\partial f}{\partial y}(0,0)=0$. Així $f_x(0,y)=-y$ i $f_y(x,0)=x$ per a tot $x,y$ (també en $0$).
  3. [creuades_origen] Derivades creuades a l'origen  (teoria: T3.2, T5.1)
     objectiu: Calcular les dues derivades creuades en $(0,0)$ i comparar-les.
     idea: Derivar les funcions d'una variable obtingudes al pas anterior, respectant l'ordre de derivació de cada derivada creuada.
     detall: $\frac{\partial^2 f}{\partial x\partial y}(0,0)=\frac{\partial}{\partial y}\Big(\frac{\partial f}{\partial x}\Big)(0,0)=\frac{d}{dy}(-y)\big|_{y=0}=-1$ i $\frac{\partial^2 f}{\partial y\partial x}(0,0)=\frac{\partial}{\partial x}\Big(\frac{\partial f}{\partial y}\Big)(0,0)=\frac{d}{dx}(x)\big|_{x=0}=1$. Són diferents, per tant el conjunt demanat és $\{(0,0)\}$.
ERRORS COMUNS:
  - [regles_a_lorigen] Calcula $f_x(0,0)$ o $f_y(0,0)$ substituint $(0,0)$ a la fórmula obtinguda fora de l'origen (que no hi està definida), en lloc d'usar la definició.
  - [schwarz_arreu] Aplica el teorema de Schwarz a tot $\mathbb{R}^2$ sense comprovar la continuïtat de les derivades segones a prop de l'origen.
  - [derivar_formula_general] Per calcular la segona derivada a l'origen deriva la fórmula general de $f_x$ i hi substitueix $(0,0)$, en lloc de derivar $f_x(0,y)$ com a funció d'una variable.

TEORIA DEL CURS QUE FA SERVIR:
[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T5.1] Definició 1 (Tema 5) — Derivades parcials r-èsimes
Denotem les derivades parcials $r$-èsimes com $\dfrac{\partial^r f}{\partial x_{i_1}\cdots\partial x_{i_r}}(p)$. També farem servir la notació abreujada $D_{i_r}\ldots D_{i_1}f$ o $D_{i_1\cdots i_r}f$, i la notació $f_{i_1\ldots i_r}$. Fixem-nos que l'ordre dels subíndexos canvia segons la notació.

[T5.6] Teorema 6 (Tema 5) — Teorema de Schwarz
(Schwarz). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$ i $D_iD_jf$ i $D_jD_if$ existeixen en $\Omega$. Si $D_iD_jf$ i $D_jD_if$ són contínues en un entorn d'$\mathbf{a}\in\Omega$, aleshores
$$D_iD_jf(\mathbf{a})=D_jD_if(\mathbf{a}).$$

[T3.31] Definició 31 (Tema 3) — Classes C^r de funcions
Direm que $f\in\mathcal{C}^0(\Omega)\Leftrightarrow f$ és contínua a $\Omega$.

$f\in\mathcal{C}^1(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ a tot punt de $\Omega$ i totes són contínues (per tant, en particular, $f$ és diferenciable i contínua).

$f\in\mathcal{C}^2(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ d'ordre $2$:
$$\frac{\partial^2f}{\partial x_i\partial x_j}=\frac{\partial}{\partial x_j}\left(\frac{\partial f}{\partial x_i}\right),$$
a tot punt de $\Omega$ i són contínues.

En general, per a $r\geq1$, es diu que $f\in\mathcal{C}^r(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials d'ordre $r$ a $\Omega$ i totes són contínues. Clarament, $f\in\mathcal{C}^{r+1}(\Omega)\Rightarrow f\in\mathcal{C}^r(\Omega)$.

Direm que $f\in\mathcal{C}^\infty(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials a qualsevol ordre de $f$ a $\Omega$ i totes són contínues.

[T5.5] Exemple 5 (Tema 5) — Derivades creuades diferents
Hi ha funcions $f:\Omega\subset\mathbb{R}^2\to\mathbb{R}$ i $p\in\Omega$ tals que $\dfrac{\partial^2 f}{\partial y\partial x}(p)\neq\dfrac{\partial f}{\partial x\partial y}(p)$.

Considerem la següent funció $f:\mathbb{R}^2\longrightarrow\mathbb{R}$:
$$f(x,y)=\begin{cases}\dfrac{xy(x^2-y^2)}{x^2+y^2} & \text{si } (x,y)\neq(0,0),\\[2mm] 0 & \text{si } (x,y)=(0,0).\end{cases}$$
</solucio_de_referencia>

### Document a revisar

[1] A $\Omega=\mathbb{R}^2\setminus\{(0,0)\}$, que és obert, $f$ és un quocient de polinomis amb denominador no nul. Com que $f$ i les seves derivades primeres són contínues a $\Omega$, pel teorema de Schwarz les dues derivades creuades coincideixen a tot punt de $\Omega$. L'únic candidat és l'origen.
[2] Per a $(x,y)\neq(0,0)$: $\dfrac{\partial f}{\partial x}=\dfrac{y(x^4+4x^2y^2-y^4)}{(x^2+y^2)^2}$ i $\dfrac{\partial f}{\partial y}=\dfrac{x(x^4-4x^2y^2-y^4)}{(x^2+y^2)^2}$.
[3] A l'origen, substituint $(0,0)$ en aquestes fórmules obtenim $\dfrac{\partial f}{\partial x}(0,0)=\dfrac{\partial f}{\partial y}(0,0)=0$.
[4] Sobre l'eix $x=0$, per a $y\neq0$: $\dfrac{\partial f}{\partial x}(0,y)=\dfrac{y\cdot(-y^4)}{y^4}=-y$, i en $y=0$ també val $0=-0$; així $\dfrac{\partial f}{\partial x}(0,y)=-y$ per a tot $y$. Anàlogament, $\dfrac{\partial f}{\partial y}(x,0)=\dfrac{x\cdot x^4}{x^4}=x$ per a tot $x$.
[5] Llavors $\dfrac{\partial^2 f}{\partial x\partial y}(0,0)=\dfrac{\partial}{\partial y}\Big(\dfrac{\partial f}{\partial x}\Big)(0,0)=\dfrac{d}{dy}(-y)\Big|_{y=0}=-1$ i $\dfrac{\partial^2 f}{\partial y\partial x}(0,0)=\dfrac{\partial}{\partial x}\Big(\dfrac{\partial f}{\partial y}\Big)(0,0)=\dfrac{d}{dx}(x)\Big|_{x=0}=1$.
[6] Les dues derivades creuades a l'origen són diferents, per tant el conjunt de punts demanat és $\{(0,0)\}$.


## t4-8:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Proveu que la funció $G(x,y,z)=(x+y+z^2,\ x-y+z,\ 2x+y-z)$ admet una inversa local diferenciable al voltant del punt $(1,-1,2)$ i calculeu $DG^{-1}(4,4,-1)$. Admet $G$ inversa global?
RESULTAT CORRECTE: $G$ és de classe $\mathcal{C}^\infty$ i $\det JG(x,y,z)=3+6z$, que en $(1,-1,2)$ val $15\neq 0$. Pel teorema de la funció inversa, $G$ té inversa local de classe $\mathcal{C}^\infty$ en un entorn de $G(1,-1,2)=(4,4,-1)$, i
$$DG^{-1}(4,4,-1)=\big(JG(1,-1,2)\big)^{-1}=\begin{pmatrix}1&1&4\\ 1&-1&1\\ 2&1&-1\end{pmatrix}^{-1}=\begin{pmatrix}0&\frac13&\frac13\\ \frac15&-\frac35&\frac15\\ \frac15&\frac1{15}&-\frac2{15}\end{pmatrix}.$$
$G$ no admet inversa global: no és injectiva, per exemple $G(0,0,0)=G(0,-1,-1)=(0,0,0)$ (en general, $(x,y,z)$ i el punt amb $z'=-1-z$ corresponent tenen la mateixa imatge). A més $\det JG=0$ sobre el pla $z=-\frac12$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [punt_imatge] Situar el punt i la seva imatge
     objectiu: Relacionar el punt $(1,-1,2)$ amb el punt $(4,4,-1)$ on es demana la diferencial de la inversa.
     idea: La diferencial de la inversa s'avalua en la imatge del punt on s'inverteix: cal comprovar quin punt de l'espai de sortida correspon a $(4,4,-1)$.
     detall: $G(1,-1,2)=(1-1+4,\ 1+1+2,\ 2-1-2)=(4,4,-1)$. Per tant $(4,4,-1)$ és la imatge de $(1,-1,2)$ i $DG^{-1}(4,4,-1)$ és la diferencial de la inversa local definida al voltant de $(1,-1,2)$.
  2. [jacobiana] Jacobiana i hipòtesis del TFI  (teoria: T4.5, T3.31)
     objectiu: Comprovar que $G$ satisfà les hipòtesis del teorema de la funció inversa en $(1,-1,2)$.
     idea: $G$ és polinòmica, per tant de classe $\mathcal{C}^\infty$. Cal calcular la matriu jacobiana i veure que el seu determinant no s'anul·la en el punt.
     detall: $JG(x,y,z)=\begin{pmatrix}1&1&2z\\ 1&-1&1\\ 2&1&-1\end{pmatrix}$, i desenvolupant, $\det JG(x,y,z)=1\cdot(1-1)-1\cdot(-1-2)+2z\cdot(1+2)=3+6z$. En $(1,-1,2)$: $\det JG(1,-1,2)=15\neq 0$. Pel teorema de la funció inversa existeix un entorn $U$ de $(1,-1,2)$ tal que $G|_U$ és injectiva, $G(U)$ és obert i la inversa és de classe $\mathcal{C}^\infty$.
  3. [diferencial_inversa] Calcular la diferencial de la inversa  (teoria: T4.5)
     objectiu: Calcular $DG^{-1}(4,4,-1)$.
     idea: El teorema de la funció inversa dona la diferencial de la inversa com la inversa de la diferencial de $G$ en el punt antiimatge. Cal invertir una matriu $3\times 3$.
     detall: $DG^{-1}(4,4,-1)=\big(JG(1,-1,2)\big)^{-1}$ amb $JG(1,-1,2)=\begin{pmatrix}1&1&4\\ 1&-1&1\\ 2&1&-1\end{pmatrix}$. Per adjunts (determinant $15$):
$\big(JG(1,-1,2)\big)^{-1}=\frac{1}{15}\begin{pmatrix}0&5&5\\ 3&-9&3\\ 3&1&-2\end{pmatrix}=\begin{pmatrix}0&\frac13&\frac13\\ \frac15&-\frac35&\frac15\\ \frac15&\frac1{15}&-\frac2{15}\end{pmatrix}$.
Comprovació: multiplicant per $JG(1,-1,2)$ dona la identitat.
  4. [inversa_global] Inversa global  (teoria: T4.9)
     objectiu: Decidir si $G$ admet una inversa definida globalment.
     idea: Una inversa global requereix que $G$ sigui injectiva a tot $\mathbb{R}^3$. Proveu de resoldre $G(x,y,z)=(u,v,w)$: les dues darreres components són lineals i permeten eliminar $x$ i $y$; mireu quantes solucions té l'equació en $z$ que en resulta.
     detall: De $v+w=3x$ s'obté $x=\frac{v+w}{3}$, i de la segona component $y=x+z-v$. Substituint a la primera: $u=2x-v+z+z^2$, és a dir $z^2+z=u+v-2x$. Aquesta equació de segon grau en $z$ té en general dues solucions, $z$ i $-1-z$, que donen dues antiimatges diferents. Exemple: $G(0,0,0)=(0,0,0)$ i $G(0,-1,-1)=(0-1+1,\ 0+1-1,\ 0-1+1)=(0,0,0)$. Per tant $G$ no és injectiva i no té inversa global. (També: $\det JG=0$ al pla $z=-\frac12$, on cap inversa local pot ser diferenciable; i $G$ no és exhaustiva, ja que $z^2+z\geq-\frac14$.)
ERRORS COMUNS:
  - [punt_equivocat] Avalua la jacobiana de $G$ en $(4,4,-1)$ en lloc d'avaluar-la en l'antiimatge $(1,-1,2)$.
  - [local_implica_global] Conclou que hi ha inversa global perquè el determinant de la jacobiana no és zero en el punt (o en molts punts).
  - [inversa_mal_calculada] S'equivoca en invertir la matriu (oblida transposar la matriu d'adjunts o dividir pel determinant).

TEORIA DEL CURS QUE FA SERVIR:
[T4.9] Definició 9 (Tema 4) — Homeomorfisme i difeomorfisme
1. Una funció $f:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$ és un homeomorfisme si $f$ és bijectiva, contínua i la seva inversa $f^{-1}$ també és contínua.

2. Una funció $f:U\longrightarrow V$ entre dos oberts $U,V$ de $\mathbb{R}^n$ és un difeomorfisme (o una transformació regular) de classe $C^r$, amb $r\geq 1$, si $f$ és bijectiva, de classe $C^r$ i la seva inversa $f^{-1}$ també és de classe $C^r$.

Els homeomorfisme preserven la forma topològica, mentre que els difeomorfisme també preserven l'estructura diferenciable.

[Resum 91'] Una definició alternativa de difeomorfisme és: Una funció $f:U\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$, amb $U$ obert de $\mathbb{R}^n$, és un difeomorfisme si $f\in\mathcal{C}^1(U)$, $f$ és injectiva, i $\det\big(Jf(x)\big)\neq 0$ per a tot $x\in U$.

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

[1] Primer situem el punt: $G(1,-1,2)=(1-1+4,\ 1+1+2,\ 2-1-2)=(4,4,-1)$. Per tant $DG^{-1}(4,4,-1)$ és la diferencial de la inversa local definida al voltant de $(1,-1,2)$.
[2] $G$ és polinòmica, de classe $\mathcal{C}^\infty$, i $JG(x,y,z)=\begin{pmatrix}1&1&2z\\ 1&-1&1\\ 2&1&-1\end{pmatrix}$. Desenvolupant per la primera fila, $\det JG(x,y,z)=1\cdot(1-1)-1\cdot(-1-2)+2z\cdot(1+2)=3+6z$.
[3] En $(1,-1,2)$, $\det JG(1,-1,2)=15\neq0$. Pel teorema de la funció inversa, hi ha un entorn $U$ de $(1,-1,2)$ tal que $G|_U$ és injectiva, $G(U)$ és obert i la inversa és de classe $\mathcal{C}^\infty$, amb $DG^{-1}(4,4,-1)=\big(JG(1,-1,2)\big)^{-1}$.
[4] Amb $JG(1,-1,2)=\begin{pmatrix}1&1&4\\ 1&-1&1\\ 2&1&-1\end{pmatrix}$, calculem els adjunts i dividim pel determinant: $DG^{-1}(4,4,-1)=\frac{1}{15}\begin{pmatrix}0&3&3\\ 5&-9&1\\ 5&3&-2\end{pmatrix}$.
[5] Pel que fa a la inversa global: com que $\det JG(x,y,z)=3+6z$ s'anul·la als punts del pla $z=-\frac12$, $G$ no pot ser injectiva a $\mathbb{R}^3$, i per tant no admet inversa global.


## t4-10:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Siguin $G:\mathbb{R}^2\to\mathbb{R}^2$ definida per $G(u,v)=(u+v,\ v-u^2)$ i $T$ l'interior del triangle limitat per les rectes $u+v=2$, $u=0$, $v=0$. Determineu el recinte $S=G(T)$ i comproveu que $G:T\to S$ és un canvi de variables (o difeomorfisme).
RESULTAT CORRECTE: $S=G(T)=\{(x,y)\in\mathbb{R}^2\mid 0<x<2,\ -x^2<y<x\}$ (limitat per la recta $y=x$, la paràbola $y=-x^2$ i la recta $x=2$). $G$ és $\mathcal{C}^\infty$, $\det JG(u,v)=1+2u>0$ a $T$, i $G:T\to S$ és bijectiva amb inversa $u=\frac{-1+\sqrt{1+4(x-y)}}{2}$, $v=x-u$, de classe $\mathcal{C}^\infty$. Per tant $G:T\to S$ és un difeomorfisme.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [imatge_vores] Imatge de les vores
     objectiu: Determinar en què es transformen els tres costats del triangle.
     idea: Parametritzeu cada costat i apliqueu-hi $G$; és útil anomenar $(x,y)=G(u,v)$ i expressar la corba imatge com a relació entre $x$ i $y$.
     detall: Costat $u=0$, $0<v<2$: $(x,y)=(v,v)$, segment de $y=x$ amb $0<x<2$. Costat $v=0$, $0<u<2$: $(x,y)=(u,-u^2)$, arc de paràbola $y=-x^2$ amb $0<x<2$. Costat $u+v=2$, $0<u<2$: $x=2$, $y=2-u-u^2\in(-4,2)$, segment vertical de $(2,2)$ a $(2,-4)$. El candidat és la regió limitada per aquestes tres corbes.
  2. [invertir] Resoldre G(u,v)=(x,y)
     objectiu: Determinar exactament $S$ i veure que cada punt de $S$ té una única antiimatge a $T$.
     idea: Aïlleu $v$ de la primera equació i substituïu a la segona: queda una equació de segon grau en $u$. Traduïu les condicions $u>0$, $v>0$, $u+v<2$ en condicions sobre $(x,y)$.
     detall: $v=x-u$ i $y=x-u-u^2$, és a dir $u^2+u=x-y$. Amb $u>0$ cal $x-y>0$ i aleshores l'única arrel positiva és $u=\frac{-1+\sqrt{1+4(x-y)}}{2}$. La condició $v>0$ és $u<x$; com que $t\mapsto t^2+t$ és creixent per $t>0$, $u<x\iff x-y<x^2+x\iff y>-x^2$. La condició $u+v<2$ és $x<2$. Per tant $(x,y)\in G(T)$ si i només si $0<x<2$ i $-x^2<y<x$ (a més $x=u+v>0$; recíprocament, si $0<x<2$ i $-x^2<y<x$, la $u$ anterior compleix $u>0$, $v=x-u>0$ i $u+v=x<2$), i l'antiimatge és única: $G:T\to S$ és bijectiva amb $S=\{0<x<2,\ -x^2<y<x\}$.
  3. [jacobiana] Jacobiana
     objectiu: Comprovar que la diferencial de $G$ és invertible a tot $T$.
     idea: Calculeu $\det JG(u,v)$ i useu el signe de $u$ a $T$.
     detall: $JG(u,v)=\begin{pmatrix}1&1\\ -2u&1\end{pmatrix}$, $\det JG(u,v)=1+2u>0$ per $u>0$, en particular a tot $T$.
  4. [concloure] Concloure que és un difeomorfisme  (teoria: T4.9, T4.5, T4.8)
     objectiu: Justificar que $G:T\to S$ és un canvi de variables.
     idea: Un difeomorfisme és una bijecció $\mathcal{C}^1$ entre oberts amb inversa $\mathcal{C}^1$; equivalentment, una aplicació $\mathcal{C}^1$ injectiva amb jacobiana invertible a cada punt de l'obert.
     detall: $T$ és obert, $G$ és polinòmica ($\mathcal{C}^\infty$), injectiva a $T$ i amb $\det JG\neq 0$ a $T$. Pel teorema de la funció inversa (aplicat a cada punt), $S=G(T)$ és obert i la inversa és $\mathcal{C}^\infty$; també es veu directament de la fórmula explícita, ja que $1+4(x-y)>1$ a $S$. Per tant $G:T\to S$ és un difeomorfisme $\mathcal{C}^\infty$.
ERRORS COMUNS:
  - [imatge_triangle] Suposa que la imatge del triangle és el triangle de vèrtexs $G(0,0)$, $G(2,0)$, $G(0,2)$, com si $G$ fos lineal.
  - [sense_injectivitat] Només comprova $\det JG\neq 0$ i conclou que és un difeomorfisme, sense provar la injectivitat.
  - [arrel_equivocada] En aïllar $u$ pren l'arrel negativa o no comprova que l'arrel triada compleixi $u>0$ i $v>0$.

TEORIA DEL CURS QUE FA SERVIR:
[T4.9] Definició 9 (Tema 4) — Homeomorfisme i difeomorfisme
1. Una funció $f:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$ és un homeomorfisme si $f$ és bijectiva, contínua i la seva inversa $f^{-1}$ també és contínua.

2. Una funció $f:U\longrightarrow V$ entre dos oberts $U,V$ de $\mathbb{R}^n$ és un difeomorfisme (o una transformació regular) de classe $C^r$, amb $r\geq 1$, si $f$ és bijectiva, de classe $C^r$ i la seva inversa $f^{-1}$ també és de classe $C^r$.

Els homeomorfisme preserven la forma topològica, mentre que els difeomorfisme també preserven l'estructura diferenciable.

[Resum 91'] Una definició alternativa de difeomorfisme és: Una funció $f:U\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$, amb $U$ obert de $\mathbb{R}^n$, és un difeomorfisme si $f\in\mathcal{C}^1(U)$, $f$ és injectiva, i $\det\big(Jf(x)\big)\neq 0$ per a tot $x\in U$.

[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.

[T4.8] Corol·lari 8 (Tema 4) — Teorema de l'aplicació oberta
Teorema de l'aplicació oberta. Sigui $f:U\subseteq\mathbb{R}^n\to V\subseteq\mathbb{R}^n$ una funció $\mathcal{C}^1(U)$ tal que $\det Jf(a)\neq 0$ per a tot $a\in U$. Aleshores, per a tot obert $B\subseteq U$, $f(B)$ és també un obert.
</solucio_de_referencia>

### Document a revisar

[1] Mirem primer les vores de $T$. Costat $u=0$, $0<v<2$: $G(0,v)=(v,v)$, el segment de la recta $y=x$ amb $0<x<2$. Costat $v=0$, $0<u<2$: $G(u,0)=(u,-u^2)$, l'arc de la paràbola $y=-x^2$ amb $0<x<2$.
[2] Costat $u+v=2$, $0<u<2$: $x=u+v=2$ i $y=v-u^2=2-u-u^2$, que per a $0<u<2$ recorre l'interval $(-2,2)$; és un segment vertical sobre la recta $x=2$. La candidata a $S$ és la regió limitada per aquestes tres corbes.
[3] Resolem $G(u,v)=(x,y)$: de $u+v=x$ i $v-u^2=y$ surt $v=x-u$ i $u^2+u=x-y$. Com que volem $u>0$, cal $x-y=u^2+u>0$, i prenem l'arrel positiva $u=\dfrac{-1+\sqrt{1+4(x-y)}}{2}$.
[4] La condició $v>0$ és $u<x$; com que $t\mapsto t^2+t$ és creixent per a $t>0$, equival a $x-y<x^2+x$, és a dir $y>-x^2$. La condició $u+v<2$ és $x<2$, i $x=u+v>0$. Recíprocament, si $0<x<2$ i $-x^2<y<x$, la $u$ anterior dona el punt $(u,x-u)\in T$. Per tant $S=G(T)=\{(x,y)\mid 0<x<2,\ -x^2<y<x\}$.
[5] La jacobiana és $JG(u,v)=\begin{pmatrix}1&1\\ -2u&1\end{pmatrix}$, amb $\det JG(u,v)=1+2u>0$ per a $u>0$, i en particular a tot $T$.
[6] Com que $T$ és obert, $G$ és polinòmica (de classe $\mathcal{C}^\infty$) i $\det JG\neq0$ a tot $T$, el teorema de la funció inversa assegura que $G$ és injectiva a $T$, que $S=G(T)$ és obert i que la inversa $G^{-1}:S\to T$ és de classe $\mathcal{C}^\infty$.
[7] Per tant $G:T\to S$ és un difeomorfisme de classe $\mathcal{C}^\infty$, amb $S=\{(x,y)\mid 0<x<2,\ -x^2<y<x\}$.


## t4-16a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $f:\mathbb{R}^2\to\mathbb{R}^2$ definida per $f(u,v)=(u^3-3uv^2,\ 3u^2v-v^3)$.

(a) En quins punts existeix inversa local diferenciable?
RESULTAT CORRECTE: A tots els punts $(u,v)\neq(0,0)$: allà $\det Jf(u,v)=9(u^2+v^2)^2\neq 0$ i el TFI dona inversa local $\mathcal{C}^\infty$. A l'origen no n'hi ha: $Df(0,0)=0$, i si existís $h$ diferenciable amb $h\circ f=\mathrm{Id}$ a prop de l'origen, la regla de la cadena donaria $Dh(0,0)\,Df(0,0)=I$, impossible (a més, $f$ ni tan sols és localment injectiva a l'origen).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [jacobia] Jacobiana i determinant  (teoria: T3.10)
     objectiu: Calcular la matriu jacobiana de $f$ i el seu determinant en un punt qualsevol.
     idea: Derivar les components; el determinant es pot escriure de manera compacta com una suma de quadrats.
     detall: $Jf(u,v)=\begin{pmatrix}3u^2-3v^2&-6uv\\ 6uv&3u^2-3v^2\end{pmatrix}$, $\det Jf(u,v)=(3u^2-3v^2)^2+36u^2v^2=9(u^2+v^2)^2$.
  2. [aplicar_tfi] Punts on s'aplica el TFI  (teoria: T4.5, T3.31)
     objectiu: Decidir en quins punts el teorema de la funció inversa assegura una inversa local diferenciable.
     idea: Comprovar la regularitat de $f$ i veure on s'anul·la el determinant jacobià.
     detall: $f$ és polinòmica, $f\in\mathcal{C}^\infty(\mathbb{R}^2)$, i $9(u^2+v^2)^2=0$ només a l'origen. Per tant, a tot $(u,v)\neq(0,0)$ hi ha inversa local de classe $\mathcal{C}^\infty$.
  3. [origen] Què passa a l'origen  (teoria: T3.21)
     objectiu: Decidir si a l'origen, on el TFI no s'aplica, hi pot haver igualment una inversa local diferenciable.
     idea: Suposar que existeix i aplicar la regla de la cadena a la composició amb $f$; o bé estudiar la injectivitat de $f$ a prop de l'origen.
     detall: $Df(0,0)=0$. Si hi hagués $h$ diferenciable en $f(0,0)=(0,0)$ amb $h(f(p))=p$ per a $p$ a prop de l'origen, la regla de la cadena donaria $Dh(0,0)\,Df(0,0)=I$, però el producte és $0$: contradicció. De fet, $f$ no és ni localment injectiva: en polars $f(r\cos\theta,r\sin\theta)=(r^3\cos 3\theta,r^3\sin 3\theta)$, així que $(r,0)$ i $(r\cos\frac{2\pi}{3},r\sin\frac{2\pi}{3})$ tenen la mateixa imatge per a tot $r>0$.
ERRORS COMUNS:
  - [tfi_com_a_equivalencia] Conclou que a l'origen no hi ha inversa local només perquè el determinant s'hi anul·la, com si la condició del TFI fos necessària.
  - [determinant_mal] Calcula malament el determinant (signes de $\pm 6uv$) i obté una expressió que s'anul·la en més punts.
  - [local_vs_global] Respon sobre la inversa global (o diu que no n'hi ha enlloc perquè $f$ no és injectiva).

TEORIA DEL CURS QUE FA SERVIR:
[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.

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

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$

[T4.3] Exemple 3 (Tema 4) — Inversió global falla en dimensió superior
El teorema d'inversió global no és cert en dimensió superior.

Se'n poden construir molts exemples, però aquest és paradigmàtic: considerem el camp vectorial polinòmic
$$f(x,y)=(x^3-3xy^2,\,3x^2y-y^3),$$
que clarament està definit a tot $\mathbb{R}^2$.

La seva matriu jacobiana, que seria el concepte que millor generalitza tant la derivada d'una funció d'una variable com la matriu d'una aplicació lineal, és
$$Jf(x,y)=\begin{pmatrix}3x^2-3y^2 & -6xy\\ 6xy & 3x^2-3y^2\end{pmatrix}.$$

Observem que $\det Jf(x,y)=(3x^2-3y^2)^2+(6xy)^2=9(x^2+y^2)^2\neq 0$ excepte en $(x,y)=(0,0)$. En canvi, $f$ no és injectiva (de fet, es pot pensar com la part real i imaginària de $f(z)=z^3$, amb $z\in\mathbb{C}$), i sabem que $z^3=w$, $w\neq 0\in\mathbb{C}$, sempre té 3 arrels diferents.

Relacionat amb aquest problema, val la pena esmentar la conjectura jacobiana real, que estableix que si el determinant de la matriu jacobiana és 1 arreu, aleshores $F$ és invertible, que s'ha demostrat que no es compleix ni per a $n=2$.
</solucio_de_referencia>

### Document a revisar

[1] La jacobiana de $f$ és $Jf(u,v)=\begin{pmatrix}3u^2-3v^2&-6uv\\ 6uv&3u^2-3v^2\end{pmatrix}$.
[2] El seu determinant és $\det Jf(u,v)=(3u^2-3v^2)^2+36u^2v^2=9(u^2+v^2)^2$, que només s'anul·la a l'origen.
[3] $f$ és polinòmica, de classe $\mathcal{C}^\infty(\mathbb{R}^2)$, i a tot punt $(u,v)\neq(0,0)$ el determinant és no nul. Pel teorema de la funció inversa, a tots aquests punts hi ha inversa local de classe $\mathcal{C}^\infty$.
[4] A l'origen, en canvi, $\det Jf(0,0)=0$, i per tant, pel teorema de la funció inversa, $f$ no hi té inversa local diferenciable.
[5] De fet, $f$ ni tan sols és localment injectiva a l'origen: en polars, $f(r\cos\theta,r\sin\theta)=(r^3\cos3\theta,\ r^3\sin3\theta)$, de manera que $(r,0)$ i $\left(r\cos\frac{\pi}{3},\ r\sin\frac{\pi}{3}\right)$ tenen la mateixa imatge per a tot $r>0$.
[6] Conclusió: $f$ té inversa local diferenciable a tots els punts $(u,v)\neq(0,0)$, i no en té a l'origen.


## t4-20:facil

### Referència

<solucio_de_referencia>
ENUNCIAT: Demostreu que l'equació $x^2y+e^x+z=0$ defineix implícitament $x$ en funció de $y$ i $z$ al voltant del punt $(0,1,-1)$. Calculeu les derivades primeres i segones de $x(y,z)$ en el punt $(1,-1)$.
RESULTAT CORRECTE: Amb $F(x,y,z)=x^2y+e^x+z$ (de classe $\mathcal{C}^\infty$), $F(0,1,-1)=0$ i $\frac{\partial F}{\partial x}(0,1,-1)=1\neq 0$, el teorema de la funció implícita (amb $r=2$) dona $x=x(y,z)$ de classe $\mathcal{C}^2$ (de fet $\mathcal{C}^\infty$) en un entorn de $(1,-1)$ amb $x(1,-1)=0$. Derivades en $(1,-1)$: $x_y=0$, $x_z=-1$, $x_{yy}=0$, $x_{yz}=x_{zy}=0$, $x_{zz}=-3$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [hipotesis_tfi] Comprovar les hipòtesis del teorema de la funció implícita  (teoria: T4.13, T3.31)
     objectiu: Justificar que l'equació defineix $x$ com a funció diferenciable de $(y,z)$ prop de $(1,-1)$.
     idea: Escriure l'equació com $F(x,y,z)=0$ i comprovar les hipòtesis del teorema de la funció implícita respecte de la variable que es vol aïllar.
     detall: $F(x,y,z)=x^2y+e^x+z$ és de classe $\mathcal{C}^\infty$ i $F(0,1,-1)=0+1-1=0$. A més $\frac{\partial F}{\partial x}=2xy+e^x$, que en $(0,1,-1)$ val $e^0=1\neq 0$. Pel teorema de la funció implícita (aplicat amb $r=2$, ja que $F\in\mathcal{C}^2$) existeixen un entorn obert $\Omega$ de $(1,-1)$ i $x=x(y,z)$ de classe $\mathcal{C}^2(\Omega)$, amb $x(1,-1)=0$ i $F(x(y,z),y,z)=0$ per a tot $(y,z)\in\Omega$; a més, prop de $(0,1,-1)$ aquestes són totes les solucions. La classe $\mathcal{C}^2$ és la que cal per parlar de derivades segones (i per Schwarz).
  2. [derivades_primeres] Derivades primeres  (teoria: T4.15, T3.21)
     objectiu: Calcular $\frac{\partial x}{\partial y}(1,-1)$ i $\frac{\partial x}{\partial z}(1,-1)$.
     idea: Derivar la identitat $F(x(y,z),y,z)=0$ respecte de cada variable amb la regla de la cadena i avaluar en el punt.
     detall: Derivant respecte de $y$: $2x\,x_y\,y+x^2+e^x x_y=0$; en $(1,-1)$ (on $x=0$): $x_y=0$, és a dir $x_y(1,-1)=0$.
Derivant respecte de $z$: $2x\,x_z\,y+e^x x_z+1=0$; en el punt: $x_z(1,-1)=-1$.
  3. [derivades_segones] Derivades segones  (teoria: T3.21, T5.6)
     objectiu: Calcular $x_{yy}$, $x_{yz}$ i $x_{zz}$ en $(1,-1)$.
     idea: Tornar a derivar les identitats del pas anterior (recordant que $x$ i les seves derivades depenen de $(y,z)$) i substituir els valors ja coneguts. Com que $x$ és $\mathcal{C}^2$, les derivades creuades coincideixen.
     detall: Derivant $2x\,x_y\,y+x^2+e^xx_y=0$ respecte de $y$: $4x\,x_y+2x_y^2y+2x\,x_{yy}y+e^xx_y^2+e^xx_{yy}=0$; en el punt ($x=0$, $x_y=0$): $x_{yy}=0$.
Derivant $2x\,x_z\,y+e^xx_z+1=0$ respecte de $y$: $2x_yx_zy+2x\,x_{zy}y+2x\,x_z+e^xx_yx_z+e^xx_{zy}=0$; en el punt: $x_{zy}=0$, i per Schwarz $x_{yz}=0$.
Derivant la mateixa identitat respecte de $z$: $2x_z^2y+2x\,x_{zz}y+e^xx_z^2+e^xx_{zz}=0$; en el punt ($x_z=-1$, $y=1$): $2+1+x_{zz}=0$, per tant $x_{zz}(1,-1)=-3$.
ERRORS COMUNS:
  - [variable_equivocada] Comprova la hipòtesi del teorema amb la derivada respecte d'una variable que no és la que es vol aïllar (per exemple $\partial F/\partial z$).
  - [oblidar_dependencia] En derivar per segon cop tracta $x$ o $x_z$ com a constants i perd termes de la regla de la cadena (per exemple el terme $2x_z^2y$).
  - [punt_equivocat] Avalua en $(y,z)=(1,-1)$ però substitueix un valor de $x$ incorrecte, o confon el punt de $\mathbb{R}^3$ amb el de $\mathbb{R}^2$.

TEORIA DEL CURS QUE FA SERVIR:
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

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$

[T5.6] Teorema 6 (Tema 5) — Teorema de Schwarz
(Schwarz). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, i $f:\Omega\to\mathbb{R}^m$ una funció tal que les derivades parcials $D_if$, $D_jf$ i $D_iD_jf$ i $D_jD_if$ existeixen en $\Omega$. Si $D_iD_jf$ i $D_jD_if$ són contínues en un entorn d'$\mathbf{a}\in\Omega$, aleshores
$$D_iD_jf(\mathbf{a})=D_jD_if(\mathbf{a}).$$
</solucio_de_referencia>

### Document a revisar

[1] Sigui $F(x,y,z)=x^2y+e^x+z$, de classe $\mathcal{C}^\infty$. Tenim $F(0,1,-1)=0+1-1=0$ i $\dfrac{\partial F}{\partial x}=2xy+e^x$, que en $(0,1,-1)$ val $e^0=1\neq0$.
[2] Pel teorema de la funció implícita (aplicat amb $r=2$) existeixen un entorn obert $\Omega$ de $(1,-1)$ i una funció $x=x(y,z)$ de classe $\mathcal{C}^2(\Omega)$ amb $x(1,-1)=0$ i $F(x(y,z),y,z)=0$ per a tot $(y,z)\in\Omega$.
[3] Derivant la identitat respecte de $y$: $2x\,x_y\,y+x^2+e^xx_y=0$; en $(1,-1)$, on $x=0$, queda $x_y(1,-1)=0$.
[4] Derivant-la respecte de $z$: $2x\,x_z\,y+e^xx_z+1=0$; en el punt queda $x_z(1,-1)=1$.
[5] Derivant $2x\,x_y\,y+x^2+e^xx_y=0$ respecte de $y$: $4x\,x_y+2x_y^2y+2x\,x_{yy}y+e^xx_y^2+e^xx_{yy}=0$; en el punt ($x=0$, $x_y=0$) dona $x_{yy}(1,-1)=0$.
[6] Derivant $2x\,x_z\,y+e^xx_z+1=0$ respecte de $y$: $2x_yx_zy+2x\,x_{zy}y+2x\,x_z+e^xx_yx_z+e^xx_{zy}=0$; en el punt, $x_{zy}(1,-1)=0$, i per Schwarz $x_{yz}(1,-1)=0$.
[7] Derivant la mateixa identitat respecte de $z$: $2x_z^2y+2x\,x_{zz}y+e^xx_z^2+e^xx_{zz}=0$; en el punt, amb $x_z^2=1$ i $y=1$: $2+1+x_{zz}=0$, és a dir $x_{zz}(1,-1)=-3$.


## t4-27:dificil

### Referència

<solucio_de_referencia>
ENUNCIAT: Demostreu que la corba d'equació
$$xy=\log\left(\frac{x}{y}\right)$$
és la gràfica d'una funció $f$ de classe $\mathcal{C}^\infty$ en un entorn de $x=\sqrt{e}$. Té $f$ un extrem local en $x=\sqrt{e}$?
RESULTAT CORRECTE: Per a $x=\sqrt e$ l'únic punt de la corba és $y_0=1/\sqrt e$. Amb $F(x,y)=xy-\log x+\log y$ ($x,y>0$), $\frac{\partial F}{\partial y}(\sqrt e,1/\sqrt e)=2\sqrt e\neq0$, i el teorema de la funció implícita dona $f\in\mathcal{C}^\infty$ amb $f(\sqrt e)=1/\sqrt e$. A més $f'(\sqrt e)=0$ i $f''(\sqrt e)=-\frac{1}{2e^{3/2}}<0$: $f$ té un màxim local estricte en $x=\sqrt e$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [punt] Trobar el punt de la corba
     objectiu: Trobar quin punt $(\sqrt e,y_0)$ és a la corba.
     idea: Observar el domini (cal $x/y>0$) i provar valors que simplifiquin el logaritme; justificar la unicitat per monotonia en $y$.
     detall: Com que $x=\sqrt e>0$, cal $y>0$. L'equació és $\sqrt e\,y=\frac12-\log y$; el membre esquerre és creixent i el dret decreixent en $y$, per tant hi ha com a màxim una solució, i $y_0=\frac{1}{\sqrt e}$ ho és: $1=\frac12+\frac12$.
  2. [tfi] Aplicar el teorema de la funció implícita  (teoria: T4.13, T3.31)
     objectiu: Justificar que, prop d'aquest punt, la corba és la gràfica d'una funció $\mathcal{C}^\infty$ de $x$.
     idea: Escriure $F(x,y)=0$ en un obert on $F$ sigui $\mathcal{C}^\infty$ i comprovar la hipòtesi sobre la derivada respecte de $y$.
     detall: A l'obert $x,y>0$, $F(x,y)=xy-\log x+\log y$ és $\mathcal{C}^\infty$. $\frac{\partial F}{\partial y}=x+\frac1y$, que en el punt val $\sqrt e+\sqrt e=2\sqrt e\neq0$. Pel teorema de la funció implícita hi ha un interval obert $I\ni\sqrt e$ i $f\in\mathcal{C}^1(I)$ amb $f(\sqrt e)=1/\sqrt e$, $f>0$, $F_y(x,f(x))\neq0$ en $I$, i prop del punt la corba és exactament la gràfica de $f$. A més $f'=-\frac{F_x(x,f)}{F_y(x,f)}$; si $f\in\mathcal{C}^k$ el segon membre és $\mathcal{C}^k$, així que $f\in\mathcal{C}^{k+1}$, i per inducció $f\in\mathcal{C}^\infty(I)$ (les notes ho abreugen aplicant el teorema amb $r=\infty$).
  3. [punt_critic] Derivada primera  (teoria: T4.15, T3.21)
     objectiu: Calcular $f'(\sqrt e)$.
     idea: Derivar la identitat $F(x,f(x))=0$ respecte de $x$ i avaluar.
     detall: $f+xf'-\frac1x+\frac{f'}{f}=0$. En $x=\sqrt e$, $f=1/\sqrt e$: $\frac{1}{\sqrt e}-\frac{1}{\sqrt e}+2\sqrt e\,f'(\sqrt e)=0$, per tant $f'(\sqrt e)=0$: és un punt crític.
  4. [segona_derivada] Classificar amb la derivada segona  (teoria: T5.11)
     objectiu: Decidir si hi ha extrem local i de quin tipus.
     idea: Tornar a derivar la identitat, usar $f'(\sqrt e)=0$ per simplificar i aplicar el criteri de la derivada segona.
     detall: Derivant de nou: $2f'+xf''+\frac{1}{x^2}+\frac{f''}{f}-\frac{f'^2}{f^2}=0$. En el punt ($f'=0$): $f''(\sqrt e)\,(\sqrt e+\sqrt e)=-\frac1e$, d'on $f''(\sqrt e)=-\frac{1}{2e^{3/2}}<0$. Pel criteri de la derivada $r$-èsima amb $r=2$, $x=\sqrt e$ és un màxim local estricte de $f$.
ERRORS COMUNS:
  - [domini_log] Treballa amb $\log x-\log y$ sense comprovar que $x,y>0$, o busca solucions amb $y<0$.
  - [critic_implica_extrem] Conclou que hi ha extrem només perquè $f'(\sqrt e)=0$.
  - [termes_segona_derivada] En derivar per segon cop oblida el terme de $\log f$ (la derivada de $f'/f$) o el de $xf'$.

TEORIA DEL CURS QUE FA SERVIR:
[T3.31] Definició 31 (Tema 3) — Classes C^r de funcions
Direm que $f\in\mathcal{C}^0(\Omega)\Leftrightarrow f$ és contínua a $\Omega$.

$f\in\mathcal{C}^1(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ a tot punt de $\Omega$ i totes són contínues (per tant, en particular, $f$ és diferenciable i contínua).

$f\in\mathcal{C}^2(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials de $f$ d'ordre $2$:
$$\frac{\partial^2f}{\partial x_i\partial x_j}=\frac{\partial}{\partial x_j}\left(\frac{\partial f}{\partial x_i}\right),$$
a tot punt de $\Omega$ i són contínues.

En general, per a $r\geq1$, es diu que $f\in\mathcal{C}^r(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials d'ordre $r$ a $\Omega$ i totes són contínues. Clarament, $f\in\mathcal{C}^{r+1}(\Omega)\Rightarrow f\in\mathcal{C}^r(\Omega)$.

Direm que $f\in\mathcal{C}^\infty(\Omega)\Leftrightarrow$ existeixen totes les derivades parcials a qualsevol ordre de $f$ a $\Omega$ i totes són contínues.

[T5.9] Definició 9 (Tema 5) — Extrems locals (una variable)
Sigui $\Omega\subseteq\mathbb{R}$ obert i $f:\Omega\to\mathbb{R}$ una funció. Diem que un punt $a\in\Omega$ és un

(i) màxim local de $f$ si $\exists\,\epsilon>0$ t.q. $\forall x\in(a-\epsilon,a+\epsilon)\subseteq\Omega$, $f(x)\leqslant f(a)$;

(ii) mínim local de $f$ si $\exists\,\epsilon>0$ t.q. $\forall x\in(a-\epsilon,a+\epsilon)\subseteq\Omega$, $f(x)\geqslant f(a)$;

(iii) màxim local estricte de $f$ si $\exists\,\epsilon>0\ \forall\, a\neq x\in(a-\epsilon,a+\epsilon)\subseteq\Omega$, $f(x)<f(a)$;

(iv) mínim local estricte de $f$ si $\exists\,\epsilon>0\ \forall\, a\neq x\in(a-\epsilon,a+\epsilon)\subseteq\Omega$, $f(x)>f(a)$.

[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]

[T4.15] Observació 15 (Tema 4) — Diferencial de la funció implícita
$D\varphi(a)$ es pot calcular aplicant la regla de la cadena a l'equació $\Phi(x,\varphi(x))=0$ en un entorn de $(a,b)$:
$$\frac{\partial\Phi}{\partial x}(a,b)+\frac{\partial\Phi}{\partial y}(a,b)\cdot\frac{\partial\varphi}{\partial x}(a)=0.$$

A l'enunciat de l'observació hem mantingut la notació en derivades parcials, però cal tenir en compte que $\dfrac{\partial\varphi}{\partial x}(a)$ és simplement $D\varphi(a)$.

[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$

[T5.11] Teorema 11 (Tema 5) — Criteri de la derivada r-èsima
Sigui $\Omega\subseteq\mathbb{R}$ obert i $f:\Omega\to\mathbb{R}$ una funció $\mathcal{C}^r(\Omega)$. Si un punt $a\in\Omega$ compleix $f'(a)=f''(a)=\cdots=f^{(r-1)}(a)=0$, llavors

(i) $f^{(r)}(a)<0$ i $r$ parell $\Rightarrow$ $a$ és un màxim local estricte de $f$;

(ii) $f^{(r)}(a)>0$ i $r$ parell $\Rightarrow$ $a$ és un mínim local estricte de $f$;

(iii) $f^{(r)}(a)<0$ i $r$ senar $\Rightarrow$ $f$ és estrictament decreixent en $a$;

(iv) $f^{(r)}(a)>0$ i $r$ senar $\Rightarrow$ $f$ és estrictament creixent en $a$.
</solucio_de_referencia>

### Document a revisar

[1] Per a $x=\sqrt e>0$, l'equació demana $\frac{x}{y}>0$, és a dir $y>0$, i es pot escriure $\sqrt e\,y=\frac12-\log y$. Els dos membres són funcions creixents de $y$, i per tant hi ha com a màxim una solució; $y_0=\frac{1}{\sqrt e}$ ho és, ja que $1=\frac12+\frac12$.
[2] A l'obert $\{x>0,\ y>0\}$ considerem $F(x,y)=xy-\log x+\log y$, de classe $\mathcal{C}^\infty$, amb $F\left(\sqrt e,\frac{1}{\sqrt e}\right)=0$. Com que $\frac{\partial F}{\partial y}=x+\frac1y$ val $\sqrt e+\sqrt e=2\sqrt e\neq0$ en el punt, el teorema de la funció implícita (amb $r=\infty$) dona un interval obert $I\ni\sqrt e$ i $f\in\mathcal{C}^\infty(I)$ amb $f(\sqrt e)=\frac{1}{\sqrt e}$ tal que, prop del punt, la corba és exactament la gràfica de $f$.
[3] Derivant $xf(x)-\log x+\log f(x)=0$: $f+xf'-\frac1x+\frac{f'}{f}=0$. En $x=\sqrt e$, amb $f=\frac{1}{\sqrt e}$: $\frac{1}{\sqrt e}-\frac{1}{\sqrt e}+2\sqrt e\,f'(\sqrt e)=0$, per tant $f'(\sqrt e)=0$ i $f$ té un extrem local en $x=\sqrt e$.
[4] Per saber de quin tipus és, derivem de nou: $2f'+xf''+\frac{1}{x^2}+\frac{f''}{f}=0$.
[5] En el punt, amb $f'(\sqrt e)=0$: $f''(\sqrt e)\,(\sqrt e+\sqrt e)=-\frac1e$, d'on $f''(\sqrt e)=-\frac{1}{2e^{3/2}}<0$. Per tant $x=\sqrt e$ és un màxim local estricte de $f$.

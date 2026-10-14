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

<apunts tema="2" titol="Límits i continuïtat de funcions">
[T2.1] Definició 1 (Tema 2) — Funció entre espais mètrics
Donats dos espais mètrics $(M,d)$ i $(N,d')$, una funció $f:\Omega\subseteq M\longrightarrow N$ és una correspondència que assigna valors de $M$ a valors de $N$.

- Si $\Omega\subseteq\mathbb{R}^n$ i $N=\mathbb{R}^m$, aleshores $f$ s'anomena funció/camp vectorial:
$$\begin{aligned} f:\Omega\subseteq\mathbb{R}^n&\longrightarrow\mathbb{R}^m\\ x=(x_1,\dots,x_n)&\longmapsto(f_1(x),\dots,f_m(x)).\end{aligned}$$
- Si $\Omega\subseteq\mathbb{R}^n$ i $N=\mathbb{R}$, aleshores $f$ s'anomena funció/camp escalar:
$$\begin{aligned} f:\Omega\subseteq\mathbb{R}^n&\longrightarrow\mathbb{R}\\ x=(x_1,\dots,x_n)&\longmapsto f(x_1,\dots,x_n)=f(x).\end{aligned}$$

[T2.2] Exemple 2 (Tema 2) — Funcions de diverses variables
Funcions de diverses/múltiples variables:
$$\theta(x,y)=\arctan(y/x),\ r(x,y)=\sqrt{x^2+y^2}$$
$$f(x,y)=1/(1-\sqrt{x^2+y^2})$$
$$F(x,y)=(-y,x)$$

[T2.3] Definició 3 (Tema 2) — Conceptes bàsics de funcions
Conceptes bàsics (extensions de concepte de càlcul en una variable).

- El domini de $f$ és el subconjunt de $M$ on $f$ està definida: $\mathrm{Dom}(f)=\{x\in M \text{ tals que } \exists f(x)\}$.
- La imatge de $f$ és $\mathrm{Im}(f)=\{y\in N\mid\exists x\in M \text{ amb } f(x)=y\}\subseteq N$.
- La gràfica de $f$ és $\mathrm{Graf}(f)=\{(x,f(x))\mid x\in\mathrm{Dom}(f)\}\subseteq M\times N$.
- $f$ és injectiva $\Leftrightarrow\forall x,y\in M$, si $f(x)=f(y)$, aleshores $x=y$.
- $f$ és exhaustiva $\Leftrightarrow\forall y\in N,\exists x\in M$ tal que $f(x)=y$.
- $f$ és bijectiva $\Leftrightarrow\forall y\in N,\exists!\,x\in M$ tal que $f(x)=y$.

[T2.4] Definició 4 (Tema 2) — Conjunt de nivell
Donada una funció escalar $f$, es defineix el conjunt de nivell $k$ com
$$C_k(f)=\{x\in M\mid f(x)=k\}\subseteq M.$$

[T2.5] Exemple 5 (Tema 2) — Corbes i superfícies de nivell
Corbes i superfícies de nivell.

- $f:\mathbb{R}^2\longrightarrow\mathbb{R}$, $f(x,y)=x^2+y^2$. $\mathrm{Dom}(f)=\mathbb{R}^2$, $\mathrm{Im}(f)=[0,+\infty)$. Les corbes de nivell són
$$C_k(f)=\{x\in\mathbb{R}^2\mid x^2+y^2=k\};$$
per tant, circumferències centrades a $O=\{(0,0)\}$ de radi $\sqrt{k}$ per a $k>0$, el punt $O$ per a $k=0$ i el conjunt buit per a $k<0$.

[Figura: esquerra, corbes de nivell $1/2,1,2,3,4,5$ de la funció $f(x,y)=x^2+y^2$ en el pla $(x,y)$ (circumferències concèntriques); dreta, gràfica de la funció $f$ (paraboloide).]
Esquerra: corbes de nivell $1/2,1,2,3,4,5$ de la funció $f(x,y)=x^2+y^2$ en el pla $(x,y)$. Dreta: Gràfica de la funció $f$.

Observem que per a qualsevol funció $f(x,y)=G(x^2+y^2)$, les corbes de nivell seran les mateixes (circumferències concèntriques centrades a l'origen), però canviarà el valor en cada corba de nivell. Això, evidentment, afecta la geometria de la gràfica. Per exemple,

- Per a $f(x,y)=\sqrt{x^2+y^2}$, tenim circumferències de radi $k$ per a $k>0$ (i no pas radi $\sqrt{k}$).
- Per a $f(x,y)=\dfrac{1}{\sqrt{1-(x^2+y^2)}}$, tenim circumferències de radi $\sqrt{1-\dfrac{1}{k^2}}$ per a $k>1$. Observem que, en aquest cas, $\mathrm{Dom}(f)=\{(x,y)\in\mathbb{R}^2\mid x^2+y^2<1\}$.

- $f:\mathbb{R}^2\longrightarrow\mathbb{R}$, $f(x,y)=x^2-y^2$. $\mathrm{Dom}(f)=\mathbb{R}^2$, $\mathrm{Im}(f)=\mathbb{R}$. Les corbes de nivell són
$$C_k(f)=\{(x,y)\in\mathbb{R}^2\mid x^2-y^2=k\};$$
per tant, hipèrboles centrades a $O=\{(0,0)\}$ amb punts de tall a $(\pm\sqrt{k},0)$ per a $k>0$, i a $(0,\pm\sqrt{k})$ per a $k<0$; $C_0$ és la unió de les rectes $y=x$ i $y=-x$, que són, a més, les asímptotes per a $k\neq0$.

[Figura: esquerra, corbes de nivell (hipèrboles); dreta, gràfica de $f(x,y)=x^2-y^2$ (sella).]
Esquerra: corbes de nivell $-5,-3,-1,1/2,5/2,7/2$ de la funció $f(x,y)=x^2-y^2$ en el pla $(x,y)$. Dreta: Gràfica de la funció $f$.

- $f:\mathbb{R}^3\longrightarrow\mathbb{R}$, $f(x,y,z)=a\,x+b\,y+c\,z$. $\mathrm{Dom}(f)=\mathbb{R}^3$, $\mathrm{Im}(f)=\mathbb{R}$. Les superfícies de nivell són plans de vector normal $(a,b,c)$.

- $f:\mathbb{R}^3\longrightarrow\mathbb{R}$, $f(x,y,z)=x^2+y^2+z^2$. $\mathrm{Dom}(f)=\mathbb{R}^3$, $\mathrm{Im}(f)=[0,+\infty)$. Les superfícies de nivell són
$$C_k(f)=\{(x,y,z)\in\mathbb{R}^3\mid x^2+y^2+z^2=k\},$$
és a dir, esferes de radi $\sqrt{k}$ centrades a l'origen.

- $f:\mathbb{R}^3\longrightarrow\mathbb{R}$, $f(x,y,z)=x^2+2\,y^2$. $\mathrm{Dom}(f)=\mathbb{R}^3$, $\mathrm{Im}(f)=[0,+\infty)$. Les superfícies de nivell són
$$C_k(f)=\{(x,y,z)\in\mathbb{R}^3\mid x^2+2\,y^2=k\},$$
és a dir, cilindres el·líptics tals que per a cada secció $z=z_0$ és una el·lipse centrada a l'origen de semieixos $\sqrt{k}$ i $\sqrt{k/2}$.

[T2.6] Definició 6 (Tema 2) — Límit d'una funció
Límit d'una funció. Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $\Omega$ un domini qualsevol de $M$, $x_0\in\Omega'$, $b\in\mathbb{R}^m$, i $f:\Omega\subseteq M\longrightarrow N$ una funció. Aleshores, direm que existeix el límit de $f$ quan $x$ tendeix a $x_0$ i val $b$, $\displaystyle\lim_{x\to x_0}f(x)=b$, si es dona qualsevol de les següents condicions:

(a) $\forall\epsilon>0,\exists\delta>0$ tal que $\forall x\in\Omega$ amb $0<d(x,x_0)<\delta$, es té que $d(f(x),b)<\epsilon$.

(b) Per a tot obert $\mathcal{V}$ que conté $b$, existeix un obert $\mathcal{U}$ que conté $x_0$ tal que $f\left((\mathcal{U}\setminus\{x_0\})\cap\Omega\right)\subseteq\mathcal{V}$. (Nota: Dir que $V$ és un obert que conté $A\subseteq M$, és equivalent a dir que $V$ és un entorn obert d'$A$. En aquesta situació, un conjunt que contingui $V$, s'anomena simplement entorn. En aquest curs, considerarem sempre entorns oberts. En el cas que $A=\{x\}$, denotarem amb $\mathcal{E}_{\mathbf{x}}$ el conjunt d'entorns oberts d'$x$ (abusant del llenguatge, ja que hauria de ser $\{x\}$).)

(c) Per a tota successió $(x_n)_{n\in\mathbb{N}}$ amb $x_0\neq x_n\in\Omega$ i $\displaystyle\lim_{n\to+\infty}x_n=x_0$, es té que $\displaystyle\lim_{n\to+\infty}f(x_n)=b$.

[T2.7] Proposició 7 (Tema 2) — Equivalència de les definicions de límit
Les condicions (a), (b) i (c) de la definició 6 són equivalents.

[T2.8] Proposició 8 (Tema 2) — Unicitat del límit
Unicitat del límit. Si existeix $\displaystyle\lim_{x\to x_0}f(x)$, aquest és únic.

[T2.x1] Apunts del Tema 2, §2.2 — Convenció M=R^n, N=R^m
A partir d'ara, prendrem $M=\mathbb{R}^n$ i $N=\mathbb{R}^m$ i, molt sovint, considerarem només el cas $m=1$ ja que l'estudi de les propietats bàsiques dels camps vectorials es pot reduir a l'estudi de les seves $m$ components per separat.

En general, el càlcul de límits per a funcions de múltiples variables presenta una problemàtica nova si ho comparem amb els límits de funcions d'una variable. El següents resultats i, sobretot, els exemples que els acompanyen mostren algunes situacions que no es donaven en dimensió 1.

[T2.9] Proposició 9 (Tema 2) — Àlgebra de límits
Sigui $x_0\in\Omega'\subseteq\mathbb{R}^n$, i siguin $F_1$ i $F_2:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^m$ tals que $\displaystyle\lim_{x\to x_0}F_j(x)=L_j$, i siguin $f_1$ i $f_2:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}$ tals que $\displaystyle\lim_{x\to x_0}f_j(x)=b_j$, per a $j=1,2$; aleshores,

(i) $\displaystyle\lim_{x\to x_0}(F_1\pm F_2)(x)=L_1\pm L_2$;

(ii) $\displaystyle\lim_{x\to x_0}(\lambda F_j)(x)=\lambda L_j,\ \forall\lambda\in\mathbb{R}$;

(iii) $\displaystyle\lim_{x\to x_0}\langle F_1(x),F_2(x)\rangle=\langle L_1,L_2\rangle$; en particular, $\displaystyle\lim_{x\to x_0}\|F_j(x)\|=\|L_j\|$;

(iv) $\displaystyle\lim_{x\to x_0}(f_1\,f_2)(x)=b_1\,b_2$; $\displaystyle\lim_{x\to x_0}(f_1/f_2)(x)=b_1/b_2$, sempre que la divisió tingui sentit;

(v) $\displaystyle\lim_{x\to x_0}(f_1,f_2)(x)=(b_1,b_2)$.

[T2.x2] Apunts del Tema 2, §2.2 — Nota sobre la demostració de la Prop. 9
No demostrem la proposició 9; a la secció de continuïtat es demostraran propietats semblants.

[T2.10] Proposició 10 (Tema 2) — Límit per camins
Límit per camins. Si $F:D\subseteq\mathbb{R}^2\longrightarrow\mathbb{R}^m$ i $(a,b)\in D'$ tal que $\displaystyle\exists\lim_{(x,y)\to(a,b)}F(x,y)=L$, llavors per a tota funció real i contínua $g$ definida en un entorn d'$a$, tal que $g(a)=b$, es compleix que
$$\lim_{x\to a}F(x,g(x))=L.$$

[T2.11] Exemple 11 (Tema 2) — No existència de límit per camins
La proposició 10 es pot fer servir per demostrar la no existència de límits. Considerem, per exemple,
$$f(x,y)=\begin{cases}\dfrac{y}{y+x^2}, & y\neq-x^2,\\ \alpha, & y=-x^2,\end{cases}$$
on $\alpha$ és un nombre real qualsevol. Calculem el límit de la restricció de $f$ a un parell de corbes "distingides" que passen per l'origen:

- Sobre $y=-x^2$, $\displaystyle\lim_{x\to0}f(x,-x^2)=\alpha$, per definició.
- Sobre $y=x^2$, $\displaystyle\lim_{x\to0}f(x,x^2)=\lim_{x\to0}\frac{x^2}{x^2+x^2}=\frac{1}{2}$.

Clarament, una condició necessària perquè existeixi $\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$ és que $\alpha=1/2$. Tot i així, si calculem el límit sobre una paràbola "qualsevol" (ens en deixem alguna, però no és rellevant per a l'exercici) que passi per l'origen, $y=m\,x^2$ amb $m\in\mathbb{R}$, tenim que:
$$\lim_{x\to0}f(x,m\,x^2)=\lim_{x\to0}\frac{m\,x^2}{m\,x^2+x^2}=\frac{m}{m+1},$$
que depèn de $m$, i només coincideix amb $1/2$ si $m=1$. Per tant, podem afirmar que $\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$ no existeix.

[T2.12] Proposició 12 (Tema 2) — Límits iterats
Límits iterats. Sigui $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}^m$ i $(a,b)\in\Omega$ t.q. $(a-\eta,a+\eta)\times(b-\eta,b+\eta)\subseteq\Omega$ per a $\eta>0$. Suposem que $\lim_{(x,y)\to(a,b)}f(x,y)=L$ i $\forall x\in(a-\eta,a+\eta)\ \exists\lim_{y\to b}f(x,y)$, i $\forall y\in(b-\eta,b+\eta)\ \exists\lim_{x\to a}f(x,y)$. Llavors,
$$\lim_{x\to a}\lim_{y\to b}f(x,y)=L=\lim_{y\to b}\lim_{x\to a}f(x,y).$$

[T2.x3] Apunts del Tema 2, §2.2 — El recíproc no és cert
Observem, no obstant, que el recíproc no és cert.

[T2.13] Exemple 13 (Tema 2) — Límits iterats sense límit
Considerem la funció
$$f(x,y)=\begin{cases}\dfrac{x\,y}{x^2+y^2}, & (x,y)\neq(0,0),\\ 0, & (x,y)=(0,0).\end{cases}$$
D'entrada, $\lim_{x\to0}\lim_{y\to0}f(x,y)=\lim_{y\to0}\lim_{x\to0}f(x,y)=0$. En efecte, si fixem $y$, $\lim_{x\to0}f(x,y)=0$, tant si $y=0$ ($f(x,y)=0$) com si $y\neq0$, ja que
$$\lim_{x\to0}\frac{x\,y}{x^2+y^2}=\frac{0}{y^2}=0.$$
Per tant, $\lim_{y\to0}\lim_{x\to0}f(x,y)=0$. Per simetria, $\lim_{x\to0}\lim_{y\to0}f(x,y)=0$.
En canvi, si prenem $y=m\,x$, amb $m\in\mathbb{R}$,
$$\lim_{x\to0}\frac{x\,y}{x^2+y^2}=\lim_{x\to0}\frac{m\,x^2}{x^2+m^2\,x^2}=\frac{m}{1+m^2},$$
que depèn de $m$ i, per tant, no es compleix que existeixi $\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$.

[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T2.15] Observació 15 (Tema 2) — Punts aïllats i continuïtat
La condició de no pertinença al conjunt de punts d'acumulació pot resultar sorprenent, però es fa perquè es considera que els punts aïllats són continus amb sí mateixos. Que són punts aïllats, es desprèn de:
$$x_0\in\Omega,\ x_0\notin\Omega'\Rightarrow\exists\,\epsilon\text{ tal que }B(x_0,\epsilon)\cap\Omega=\{x_0\}.$$

[T2.16] Exemple 16 (Tema 2) — Funció amb punt aïllat
$f:\{x_0\}\cup A\longrightarrow\mathbb{R}$, amb $\{x_0\}\cap A'=\emptyset$.

[T2.17] Teorema 17 (Tema 2) — Caracteritzacions de la continuïtat
Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents:

(a) $f$ és contínua en $\Omega$;

(b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;

(c) per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$;

(d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.

[T2.18] Corol·lari 18 (Tema 2) — Conjunts definits per desigualtats
Siguin $f,g:\mathbb{R}^n\longrightarrow\mathbb{R}$, funcions contínues. Llavors:

(i) $A=\{x\in\mathbb{R}^n:f(x)>g(x)\}$ és un conjunt obert.

(ii) $B=\{x\in\mathbb{R}^n:f(x)\geq g(x)\}$ és un conjunt tancat.

[T2.x4] Apunts del Tema 2, §2.3 — Comentari sobre el corol·lari 18
Observem que, en el corol·lari 18, si les funcions només estiguessin definides en un conjunt $\Omega\subseteq\mathbb{R}^n$, només podríem afirmar que $A=U\cap\Omega$, on $U$ és un obert de $\mathbb{R}^n$. En el cas que $\Omega$ fos un obert de $\mathbb{R}^n$, aleshores $A$ també seria un obert de $\mathbb{R}^n$. Anàlogament per a $B$ canviant "obert" per "tancat".

Els següents resultats ens asseguren que, de manera genèrica, les combinacions i composicions de funcions contínues donen lloc a funcions contínues.

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

[T2.21] Proposició 21 (Tema 2) — Imatge contínua de compactes i connexos
Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $f:\Omega\subseteq M\to N$ contínua i $K\subseteq\Omega$. Aleshores,

(i) $K$ compacte $\Rightarrow f(K)$ compacte;

(ii) $K$ connex $\Rightarrow f(K)$ connex.

[T2.22] Observació 22 (Tema 2) — Recíprocs falsos de la Prop. 21
Els recíprocs dels dos apartats de la proposició 21 no són certs.

- La funció $f:\mathbb{R}\longrightarrow\mathbb{R}$, $f(x)\equiv0$, és contínua, i el conjunt $\{0\}\in\mathbb{R}$ és compacte. En canvi, $f^{-1}(\{0\})=\mathbb{R}$ NO és compacte.
- La funció $f(x):\mathbb{R}\longrightarrow\mathbb{R}$, $f(x)=x^2$, compleix que $K=f^{-1}([a,b])\subset\mathbb{R}$, amb $0<a<b$, NO és connex, però en canvi $f(K)=[a,b]$ sí que ho és.

[T2.23] Teorema 23 (Tema 2) — Teorema de Weierstrass
(Weierstrass). Sigui $f:\Omega\subseteq M\to\mathbb{R}$ contínua i $K\subseteq\Omega$ compacte. Llavors $f(K)$ és fitat i $\exists x_0,x_1\in K$ t.q. $f(x_0)=\min_{x\in K}f(x)$ i $f(x_1)=\max_{x\in K}f(x)$.

[T2.24] Teorema 24 (Tema 2) — Teorema del valor intermedi
(del valor intermedi). Sigui $f:\Omega\subseteq M\to\mathbb{R}$ contínua, $K\subseteq\Omega$ connex, i $x,y\in K$. Aleshores, per a tota $c\in\mathbb{R}$ tal que $f(x)<c<f(y)$, $\exists\xi\in K$ tal que $f(\xi)=c$.

[T2.25] Definició 25 (Tema 2) — Continuïtat uniforme
Una funció $f:\Omega\subseteq M\to N$ és uniformement contínua si $\forall\epsilon>0\ \exists\delta>0$ t.q. $\forall x,y\in\Omega$, $d(x,y)<\delta$ tenim que $d'(f(x),f(y))<\epsilon$.

[T2.26] Definició 26 (Tema 2) — Funció Lipschitz
Una funció $f:\Omega\subseteq M\to N$ és de Lipschitz si $\exists C>0$ t.q. $\forall x,y\in\Omega$, $d'(f(x),f(y))<C\,d(x,y)$.

[T2.27] Exemple 27 (Tema 2) — Aplicacions lineals són Lipschitz
Tota aplicació lineal $f:\mathbb{R}^n\to\mathbb{R}^m$ és de Lipschitz.

En efecte, considerem $f(x)=Ax$, amb $x=(x_1,\dots,x_n)^t$ i $A=(a_{i,j})_{i=1,\dots,m;j=1,\dots,n}$. Denotem amb $c_j=(a_{1,j},\dots,a_{m,j})^t$ la $j$-èsima columna de $A$ i definim la norma $\|A\|_{=}\max_j\{\|c_j\|\}$, a partir de la norma $\ell_1$ de vectors ($\|v\|_1=\sum_{j=1}^m|v_j|$). (Nota: Al final del tema es fa un repàs de normes equivalents, normes de vectors i normes de matrus. En particular, seguint la definició 36, a l'exemple 37 veurem que $\|A\|_1$ és una norma subordinada a la normal vectorial $\|v\|_1$ i que, per tant, és consistent i $\|A(x-y)\|_1\leq\|A\|_1\|x-y\|_1$. Directament, veiem, doncs, que l'aplicació lineal és Lipschitz amb $C=1$.)

Per a un parell de punts qualssevol $x,y\in\mathbb{R}^n$, ometent el subíndex $1$ de les normes, tenim que:
$$\begin{aligned}\|f(x)-f(y)\|&=\|Ax-Ay\|=\|A(x-y)\|=\Big\|A\sum_{i=1}^n(x_i-y_i)e_i\Big\|=\Big\|\sum_{i=1}^n(x_i-y_i)A\,e_i\Big\|\\&=\Big\|\sum_{i=1}^n(x_i-y_i)c_i\Big\|\leq\sum_{i=1}^n|x_i-y_i|\,\|c_i\|\leq\sum_{i=1}^n|x_i-y_i|\,\|A\|\\&\leq n\,\|x-y\|\,\|A\|=C\|x-y\|,\end{aligned}$$
amb $C=n\|A\|$ i, per tant, $f$ és Lipschitz.

[T2.28] Proposició 28 (Tema 2) — Lipschitz, uniforme i contínua
Lipschitz $\Rightarrow$ uniformement contínua $\Rightarrow$ contínua. Els recíprocs són falsos.

[T2.29] Teorema 29 (Tema 2) — Teorema de Heine-Cantor
(Heine–Cantor). Siguin $(M,d)$ i $(N,d')$ espais mètrics, i $K\subseteq M$ un conjunt compacte. Si $f:K\to N$ és una funció contínua, llavors $f$ és uniformement contínua en $K$.

[T2.x5] Apunts del Tema 2, §2.5 — Rellevància de la compacitat
Observem que la compacitat és rellevant per poder garantir l'existència d'una subsuccessió convergent. Per exemple, el teorema de Heine-Cantor no es pot aplicar a la funció $f(x)=1/x$ que hem considerat al contraexemple de la demostració de la proposició 28 perquè no està definida en un compacte.

[T2.30] Definició 30 (Tema 2) — Funció contractiva
Una funció $f:\Omega\subseteq M\to N$ és contractiva si existeix $0<k<1$ t.q. $\forall x,y\in\Omega$, $d'(f(x),f(y))\leqslant k\,d(x,y)$ (és a dir, Lipschitz amb constant $<1$).

[T2.31] Teorema 31 (Tema 2) — Teorema del punt fix
(del punt fix). Sigui $(M,d)$ un espai mètric complet, i sigui $f:M\to M$ una funció contractiva. Aleshores:

(a) $f$ té un únic punt fix $x^*$ a $M$, és a dir, existeix un únic $x^*\in M$ tal que $f(x^*)=x^*$.

(b) Per a qualsevol punt inicial $x_0\in M$ (condició inicial), la successió definida per iteració $x_{n+1}=f(x_n)$ convergeix cap a $x^*$.

Aquest teorema és fonamental en anàlisi numèrica, equacions diferencials i optimització, ja que assegura la convergència de molts mètodes iteratius.

[T2.32] Definició 32 (Tema 2) — Normes equivalents
En un espai mètric $M$, dues normes $\|\cdot\|_a$ $\|\cdot\|_b$ són equivalents si existeixen $\lambda,\mu>0$ tals que
$$\lambda\,\|\cdot\|_b\leq\|\cdot\|_a\leq\mu\,\|\cdot\|_b\qquad\forall x\in M.$$

[T2.33] Teorema 33 (Tema 2) — Equivalència de normes a R^n
A $\mathbb{R}^n$ totes les normes són equivalents.

[T2.34] Exemple 34 (Tema 2) — Normes ℓ^p a R^n
(Normes $\ell^p$ en $\mathbb{R}^n$). Per a $p\geq1$, la $p$-norma es defineix com
$$\|x\|_p=\left(\sum_{i=1}^n|x_i|^p\right)^{1/p}.$$
Per exemple,

- Si $p=1$, tenim la norma Manhattan o la norma (del) taxi:
$$\|x\|_1=|x_1|+|x_2|+\cdots+|x_n|$$
- Si $p=2$, tenim la norma euclidiana:
$$\|x\|_2=\sqrt{|x_1|^2+|x_2|^2+\cdots+|x_n|^2}$$
- Si $p=\infty$, tenim la norma del màxim:
$$\|x\|_\infty=\max_{1\leq i\leq n}|x_i|$$

Vegem ara que són equivalents.
Prenem $x\in\mathbb{R}^n$ qualsevol. Aleshores,
$$\|x\|_\infty\leq\|x\|_p\leq n^{1/p}\|x\|_\infty$$
En particular,
$$\|x\|_\infty\leq\|x\|_2\leq\sqrt{n}\|x\|_\infty,\qquad\|x\|_\infty\leq\|x\|_1\leq n\|x\|_\infty.$$

[T2.35] Exemple 35 (Tema 2) — Normes pesades
(Normes pesades). Definim
$$\|x\|_w=\sum_{i=1}^nw_i|x_i|,$$
on $w_i>0$ són uns pesos fixats. Aquestes normes també són equivalents a la norma $\|x\|_1$:
$$\min_iw_i\ \|x\|_1\leq\|x\|_w\leq\max_iw_i\ \|x\|_1$$
Tot i la diversitat de normes, en dimensió finita totes mesuren d'una manera similar, i només difereixen per factors d'escala.

Com a cas particular, en $\mathbb{R}^2$ les boles unitat són cercles si la norma és l'euclidiana, quadrats en forma de rombe si prenem la norma 1, i quadrats paral·lels als eixos si prenem la norma infinit. Però independentment de la forma, totes representen regions fitades i per això són equivalents.

[T2.36] Definició 36 (Tema 2) — Norma matricial consistent i subordinada
Direm que una norma matricial definida en un espai vectorial de matrius $\mathcal{M}_{m\times n}(\mathbb{R})$ és una norma consistent amb les normes vectorials $\|\cdot\|_a$ en $\mathbb{R}^n$ i $\|\cdot\|_b$ en $\mathbb{R}^m$ si
$$\|A\,x\|_b\leq\|A\|\,\|x\|_a,\qquad\forall x\in\mathbb{R},\forall A\in\mathcal{M}_{m\times n}(\mathbb{R}).$$
En el cas de matrius quadrades en l'espai vectorial $\mathcal{M}_{n\times n}(\mathbb{R})$, direm que la norma és multiplicativa si
$$\|A\,B\|\leq\|A\|\,\|B\|,\qquad\forall A,B\in\mathcal{M}_{n\times n}(\mathbb{R}).$$
Donada una norma vectorial $\|\cdot\|$, podem definir una norma matricial que sigui consistent amb ella com
$$\|A\|=\sup_{x\neq0}\frac{\|Ax\|}{\|x\|}=\sup_{\|x\|=1}\|Ax\|,$$
que s'anomena norma matricial subordinada a l'esmentada norma vectorial.

[T2.37] Exemple 37 (Tema 2) — Normes matricials subordinades
(Normes matricials subordinades). Sigui $A=(a_{ij})_{i,j}$ i considerem les normes vectorials $\|\cdot\|_1$, $\|\cdot\|_\infty$ i $\|\cdot\|_2$.

- $\|A\|_1=\max_{1\leq j\leq n}\sum_{i=1}^m|a_{ij}|$ és la norma subordinada a $\|\cdot\|_1$.

  En efecte, si $A\in\mathcal{M}_{m\times n}(\mathbb{R})$ i $x\in\mathbb{R}^n$,
  $$\|A\,x\|_1=\sum_{i=1}^m\left|\sum_{j=1}^na_{ij}\,x_j\right|\leq\sum_{j=1}^n|x_j|\sum_{i=1}^m|a_{ij}|\leq\left(\max_{j=1,\dots,n}\sum_{i=1}^m|a_{ij}|\right)\|x\|_1=\|A\|_1\|x\|_1.$$
- $\|A\|_\infty=\max_{1\leq i\leq m}\sum_{j=1}^n|a_{ij}|$ és la norma subordinada a $\|\cdot\|_\infty$.
- $\|A\|_2=\sqrt{\rho(A^TA)}$, on $\rho(B)$ és el radi espectral de $B$, és la norma subordinada a $\|\cdot\|_2$.

[T2.38] Observació 38 (Tema 2) — Norma d'Euclides no subordinada
No tota norma matricial prové d'una de vectorial (o sigui, és subordinada a una de vectorial). Per exemple, la norma matricial (no multiplicativa)
$$\|A\|_E=\left(\sum_{i,j}|a_{ij}|^2\right)^{1/2}$$
no està subordinada a cap norma vectorial.

[T2.39] Definició 39 (Tema 2) — Distàncies equivalents
En un espai mètric $M$, dues distàncies $d$ i $d'$ són equivalents si la funció identitat $Id:(M,d)\longrightarrow(M,d')$ és contínua, bijectiva i d'inversa contínua.

[T2.40] Definició 40 (Tema 2) — Distàncies uniformement equivalents
En un espai mètric $M$, dues distàncies $d$ i $d'$ són uniformement equivalents si la funció identitat $Id:(M,d)\longrightarrow(M,d')$ és uniformement contínua, bijectiva i d'inversa uniformement contínua.
</apunts>

## Statements

<questionari>
[1] Sigui $f:\mathbb{R}^2\to\mathbb{R}$. Si per a tota recta $r$ que passa per l'origen es compleix que el límit de $f$ restringida a $r$ quan el punt tendeix a $(0,0)$ val $0$, aleshores $\lim_{(x,y)\to(0,0)}f(x,y)=0$.
    veredicte declarat: fals
    contraexemple: $f(x,y)=\frac{x^2y}{x^4+y^2}$ si $(x,y)\neq(0,0)$, $f(0,0)=0$: sobre totes les rectes el límit és $0$, però sobre la paràbola $y=x^2$ val $\frac{1}{2}$.
    resolució: Prenem $f(x,y)=\frac{x^2y}{x^4+y^2}$ per a $(x,y)\neq(0,0)$ i $f(0,0)=0$. Sobre la recta $x=0$ tenim $f(0,y)=0$, i el límit és $0$. Sobre la recta $y=mx$ (amb $x\neq0$), $f(x,mx)=\frac{mx^3}{x^4+m^2x^2}=\frac{mx}{x^2+m^2}$, que tendeix a $0$ quan $x\to0$ (si $m=0$ la funció és idènticament $0$; si $m\neq0$ el denominador tendeix a $m^2\neq0$). Per tant la hipòtesi es compleix. En canvi, sobre la paràbola $y=x^2$, $f(x,x^2)=\frac{x^4}{2x^4}=\frac{1}{2}$ per a $x\neq0$, de manera que, per la proposició 10 (amb $g(x)=x^2$ contínua i $g(0)=0$), si existís el límit doble hauria de valer $\frac{1}{2}$, i també $0$ (pel camí $y=0$). Per la unicitat del límit, el límit doble no existeix.
    pista: Quina condició exigeix la definició de límit doble que no exigeixen els límits sobre rectes?
    teoria citada: T2.10, T2.11, T2.8
[2] Tota funció $f:[0,1]\to\mathbb{R}$ uniformement contínua és de Lipschitz.
    veredicte declarat: fals
    contraexemple: $f(x)=\sqrt{x}$ a $[0,1]$: és uniformement contínua (Heine-Cantor) però el quocient $\frac{\sqrt{x}-\sqrt{0}}{x-0}=\frac{1}{\sqrt{x}}$ no és fitat.
    resolució: Sigui $f(x)=\sqrt{x}$ a $[0,1]$. És contínua i $[0,1]$ és compacte, així que pel teorema de Heine-Cantor és uniformement contínua. Si fos de Lipschitz amb constant $C>0$, tindríem per a tot $x\in(0,1]$: $\sqrt{x}=|f(x)-f(0)|<C\,x$, és a dir, $\frac{1}{\sqrt{x}}<C$. Però $\frac{1}{\sqrt{x}}\to+\infty$ quan $x\to0^+$, contradicció. Per tant $f$ no és de Lipschitz: la implicació Lipschitz $\Rightarrow$ uniformement contínua de la proposició 28 no es pot invertir, ni tan sols en un compacte.
    pista: Què controla exactament la condició de Lipschitz que la definició de continuïtat uniforme no controla?
    teoria citada: T2.25, T2.26, T2.28, T2.29
[3] Sigui $K\subseteq\mathbb{R}^n$ un compacte no buit i $f:K\to\mathbb{R}$ una funció contínua tal que $f(x)>0$ per a tot $x\in K$. Aleshores existeix $c>0$ tal que $f(x)\geq c$ per a tot $x\in K$.
    veredicte declarat: cert
    resolució: Com que $f$ és contínua i $K$ és compacte i no buit, pel teorema de Weierstrass existeix $x_0\in K$ tal que $f(x_0)=\min_{x\in K}f(x)$. Prenem $c=f(x_0)$. Per hipòtesi $c=f(x_0)>0$, i per definició de mínim $f(x)\geq c$ per a tot $x\in K$. Observem que la compacitat és essencial: a $(0,1]$ la funció $f(x)=x$ és positiva però el seu ínfim és $0$.
    pista: Quina diferència hi ha entre l'ínfim d'un conjunt de valors i el mínim? Quin paper hi juga la compacitat del domini?
    teoria citada: T2.23
[4] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ tal que existeix $\lim_{(x,y)\to(0,0)}f(x,y)=L$. Aleshores existeixen els dos límits iterats $\lim_{x\to0}\lim_{y\to0}f(x,y)$ i $\lim_{y\to0}\lim_{x\to0}f(x,y)$, i tots dos valen $L$.
    veredicte declarat: fals
    contraexemple: $f(x,y)=x\sin(1/y)$ si $y\neq0$, $f(x,0)=0$: el límit doble és $0$, però per a $x\neq0$ no existeix $\lim_{y\to0}f(x,y)$.
    resolució: Sigui $f(x,y)=x\sin(1/y)$ si $y\neq0$ i $f(x,0)=0$. Com que $|f(x,y)|\leq|x|\leq\|(x,y)\|$, per a tot $\epsilon>0$ el valor $\delta=\epsilon$ funciona a la definició, i $\lim_{(x,y)\to(0,0)}f(x,y)=0$. En canvi, fixat $x\neq0$, $\lim_{y\to0}x\sin(1/y)$ no existeix, perquè $\sin(1/y)$ no té límit quan $y\to0$ (per exemple, sobre $y_n=\frac{1}{n\pi}$ val $0$ i sobre $y_n=\frac{1}{2n\pi+\pi/2}$ val $1$). Per tant la funció $x\mapsto\lim_{y\to0}f(x,y)$ no està definida per a cap $x\neq0$ i el límit iterat $\lim_{x\to0}\lim_{y\to0}f(x,y)$ no existeix. La proposició 12 necessita, com a hipòtesi, que existeixin els límits interiors.
    pista: Quines hipòtesis té la proposició 12 a més de l'existència del límit doble? Alguna d'elles es dedueix de l'existència del límit doble?
    teoria citada: T2.6, T2.12
[5] Si $A\subseteq\mathbb{R}^2$ és un conjunt tancat i $f:\mathbb{R}^2\to\mathbb{R}$ és contínua, aleshores $f(A)$ és un conjunt tancat de $\mathbb{R}$.
    veredicte declarat: fals
    contraexemple: $A=\{(x,y)\in\mathbb{R}^2: xy=1\}$ i $f(x,y)=x$: $A$ és tancat però $f(A)=\mathbb{R}\setminus\{0\}$ no ho és.
    resolució: Sigui $A=\{(x,y)\in\mathbb{R}^2: xy=1\}$. És tancat pel corol·lari 18, ja que $A=\{xy\geq1\}\cap\{1\geq xy\}$ i $(x,y)\mapsto xy$ és contínua. La projecció $f(x,y)=x$ és contínua (és lineal). Si $(x,y)\in A$, aleshores $x\neq0$; i per a tot $t\neq0$, $(t,1/t)\in A$ amb $f(t,1/t)=t$. Per tant $f(A)=\mathbb{R}\setminus\{0\}$, que no és tancat: $0$ és límit de la successió $\frac{1}{n}\in f(A)$ però $0\notin f(A)$. El que sí es conserva (proposició 21) és la compacitat, i $A$ no és fitat.
    pista: Quines propietats dels conjunts es conserven per imatge contínua segons els apunts? Ser tancat n'és una?
    teoria citada: T2.18, T2.21
[6] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ tal que, per a cada $x\in\mathbb{R}$, existeix $g(x)=\lim_{y\to0}f(x,y)$ i, per a cada $y\in\mathbb{R}$, existeix $h(y)=\lim_{x\to0}f(x,y)$. Si $\lim_{x\to0}g(x)=A$ i $\lim_{y\to0}h(y)=B$ amb $A\neq B$, aleshores no existeix $\lim_{(x,y)\to(0,0)}f(x,y)$.
    veredicte declarat: cert
    resolució: Suposem, per reducció a l'absurd, que existeix $\lim_{(x,y)\to(0,0)}f(x,y)=L$. Com que $f$ està definida a tot $\mathbb{R}^2$, qualsevol quadrat $(-\eta,\eta)\times(-\eta,\eta)$ és dins del domini, i per hipòtesi existeixen els límits interiors $\lim_{y\to0}f(x,y)$ i $\lim_{x\to0}f(x,y)$ per a tot $x$ i tot $y$. Aleshores la proposició 12 dona $\lim_{x\to0}\lim_{y\to0}f(x,y)=L=\lim_{y\to0}\lim_{x\to0}f(x,y)$, és a dir, $A=L=B$, en contradicció amb $A\neq B$. Per exemple, $f(x,y)=\frac{x^2-y^2}{x^2+y^2}$ (amb $f(0,0)=0$) té iterats $1$ i $-1$.
    pista: Si el límit doble existís, què diu la proposició 12 dels dos límits iterats? Es compleixen totes les seves hipòtesis?
    teoria citada: T2.12, T2.8
[7] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ tal que, per a cada $b\in\mathbb{R}$, la funció $x\mapsto f(x,b)$ és contínua a $\mathbb{R}$ i, per a cada $a\in\mathbb{R}$, la funció $y\mapsto f(a,y)$ és contínua a $\mathbb{R}$. Aleshores $f$ és contínua a $(0,0)$.
    veredicte declarat: fals
    contraexemple: $f(x,y)=\frac{x^2y^2}{x^4+y^4}$ si $(x,y)\neq(0,0)$, $f(0,0)=0$: és contínua en cada variable separadament, però sobre $y=x$ tendeix a $\frac{1}{2}\neq f(0,0)$.
    resolució: Sigui $f(x,y)=\frac{x^2y^2}{x^4+y^4}$ si $(x,y)\neq(0,0)$ i $f(0,0)=0$. Fixat $b\neq0$, $x\mapsto\frac{x^2b^2}{x^4+b^4}$ és un quocient de polinomis amb denominador $\geq b^4>0$, per tant contínua a $\mathbb{R}$. Fixat $b=0$, $f(x,0)=0$ per a tot $x$ (també per a $x=0$), que és contínua. Per simetria de $f$ en $x$ i $y$, el mateix val per a $y\mapsto f(a,y)$. En canvi, sobre la recta $y=x$, $f(x,x)=\frac{x^4}{2x^4}=\frac{1}{2}$ per a $x\neq0$; per la proposició 10, si $f$ fos contínua a $(0,0)$ caldria $\lim_{x\to0}f(x,x)=f(0,0)=0$. Per tant $f$ no és contínua a l'origen.
    pista: Les hipòtesis controlen $f$ quan ens movem paral·lelament als eixos. Què en sabem si ens acostem a l'origen per la diagonal?
    teoria citada: T2.10, T2.14
[8] Sigui $f:\mathbb{R}^2\to\mathbb{R}$ contínua tal que $f(p,q)=0$ per a tots $p,q\in\mathbb{Q}$. Aleshores $f(x,y)=0$ per a tot $(x,y)\in\mathbb{R}^2$.
    veredicte declarat: cert
    resolució: Sigui $(x,y)\in\mathbb{R}^2$. Per la densitat de $\mathbb{Q}$ a $\mathbb{R}$, existeixen successions de racionals $p_n\to x$ i $q_n\to y$ (per exemple, $p_n\in\mathbb{Q}$ amb $|p_n-x|<\frac{1}{n}$). Aleshores $(p_n,q_n)\to(x,y)$ a $\mathbb{R}^2$, ja que $\|(p_n,q_n)-(x,y)\|\leq|p_n-x|+|q_n-y|\to0$. Com que $f$ és contínua, pel teorema 17(b), $f(x,y)=\lim_{n\to\infty}f(p_n,q_n)=\lim_{n\to\infty}0=0$.
    pista: Pots aproximar qualsevol punt de $\mathbb{R}^2$ per punts de coordenades racionals? Què diu la continuïtat sobre els valors de $f$ al llarg d'una successió convergent?
    teoria citada: T2.17
[9] Sigui $f:\mathbb{R}\to\mathbb{R}$ tal que $|f(x)-f(y)|<|x-y|$ per a tots $x,y\in\mathbb{R}$ amb $x\neq y$. Aleshores $f$ té un punt fix, és a dir, existeix $x^*\in\mathbb{R}$ amb $f(x^*)=x^*$.
    veredicte declarat: fals
    contraexemple: $f(x)=\sqrt{x^2+1}$: compleix $|f(x)-f(y)|<|x-y|$ si $x\neq y$, però $\sqrt{x^2+1}=x$ no té solució. No és contractiva: no hi ha cap $k<1$ uniforme.
    resolució: Sigui $f(x)=\sqrt{x^2+1}$. Tenim $f'(x)=\frac{x}{\sqrt{x^2+1}}$ i $|f'(x)|<1$ per a tot $x$. Pel teorema del valor mitjà, si $x\neq y$ existeix $\xi$ entre ells amb $|f(x)-f(y)|=|f'(\xi)|\,|x-y|<|x-y|$, i la hipòtesi es compleix. Però si $f(x)=x$, aleshores $x\geq0$ i $x^2+1=x^2$, impossible: no hi ha punt fix. No contradiu el teorema 31 ($\mathbb{R}$ és complet) perquè $f$ no és contractiva: per a $x>0$, $\frac{f(x)-f(0)}{x-0}=\frac{\sqrt{x^2+1}-1}{x}\to1$ quan $x\to+\infty$, així que cap constant $k<1$ no serveix per a tots els parells de punts.
    pista: Quina diferència hi ha entre la condició $|f(x)-f(y)|<|x-y|$ i la definició de funció contractiva? Quina de les dues fa servir el teorema del punt fix?
    teoria citada: T2.30, T2.31
[10] Tota funció $f:(0,1)\to\mathbb{R}$ uniformement contínua és fitada.
    veredicte declarat: cert
    resolució: Prenem $\epsilon=1$ a la definició 25: existeix $\delta>0$ tal que si $x,y\in(0,1)$ i $|x-y|<\delta$, aleshores $|f(x)-f(y)|<1$. Triem $N\in\mathbb{N}$, $N\geq1$, amb $\frac{1}{N+1}<\delta$ i els punts $p_j=\frac{j}{N+1}\in(0,1)$, $j=1,\dots,N$. Tot $x\in(0,1)$ és a distància $<\delta$ d'algun $p_j$ (la distància al més proper és com a molt $\frac{1}{N+1}$, i val estrictament menys de $\delta$). Llavors $|f(x)|\leq|f(p_j)|+|f(x)-f(p_j)|<\max_{j}|f(p_j)|+1$. Per tant $f$ és fitada per $M=\max_j|f(p_j)|+1$. La continuïtat sola no basta: $f(x)=\frac{1}{x}$ és contínua i no fitada a $(0,1)$.
    pista: Què aporta la definició de continuïtat uniforme que no aporta la continuïtat punt a punt? Quin paper hi juga que el domini sigui fitat?
    teoria citada: T2.25
[11] Si $f,g:\mathbb{R}\to\mathbb{R}$ són uniformement contínues, aleshores el producte $fg$ és uniformement contínua a $\mathbb{R}$.
    veredicte declarat: fals
    contraexemple: $f(x)=g(x)=x$ són uniformement contínues, però $fg(x)=x^2$ no ho és: amb $x_n=n$ i $y_n=n+\frac{1}{n}$, $|x_n-y_n|\to0$ però $y_n^2-x_n^2\to2$.
    resolució: Les funcions $f(x)=g(x)=x$ són lineals, per tant de Lipschitz (exemple 27) i uniformement contínues (proposició 28). El producte és $h(x)=x^2$. Prenem $x_n=n$ i $y_n=n+\frac{1}{n}$. Tenim $|x_n-y_n|=\frac{1}{n}\to0$, però $h(y_n)-h(x_n)=2+\frac{1}{n^2}>2$. Si $h$ fos uniformement contínua, amb $\epsilon=2$ existiria $\delta>0$ tal que $|x-y|<\delta$ implica $|h(x)-h(y)|<2$; prenent $n$ amb $\frac{1}{n}<\delta$ obtenim una contradicció. A diferència de la continuïtat (proposició 20(ii)), la continuïtat uniforme no es conserva pel producte quan les funcions no són fitades.
    pista: A la definició de continuïtat uniforme, el $\delta$ ha de servir a tot el domini. Com influeix la mida dels valors de $f$ i $g$ en la variació del producte?
    teoria citada: T2.20, T2.25, T2.27, T2.28
</questionari>

## Output

Write tema-2.normal.audit.json following this schema:

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

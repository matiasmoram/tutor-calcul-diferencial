# Writer brief: tema-6, normal (8 statements in the quiz)

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

<apunts tema="6" titol="Varietats diferenciables i extrems condicionats">
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

[T6.x1] Apunts del Tema 6, §6.1 — Introducció a les varietats diferenciables
Al llarg d'aquest capítol generalitzarem d'una manera formal les idees que han anat apareixent en l'exemple. Comencem pel concepte de varietat diferenciable.

[T6.2] Definició 2 (Tema 6) — Varietat en forma implícita
Una $m$-varietat de classe $r$ a $\mathbb{R}^n$ és un subconjunt no buit $M\subseteq\mathbb{R}^n$ tal que per a tot $\mathbf{a}\in M$ existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i una funció $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$ amb $\mathrm{rang}\left(D\Phi(\mathbf{x})\right)=n-m$ per a tot $\mathbf{x}\in G$, tals que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.

En aquest context, es diu que $M$ és la $m$-varietat associada a $\Phi$; per reforçar aquesta relació amb $\Phi$, de vegades la denotarem amb $M_\Phi$.

$M$ també s'acostuma a anomenar (sub)varietat (diferenciable, $\mathcal{C}^r$ o de classe $r$) de dimensió $m$ en $\mathbb{R}^n$.

[T6.3] Definició 3 (Tema 6) — Varietat en forma paramètrica
Una $m$-varietat de classe $r$ a $\mathbb{R}^n$ és un subconjunt no buit $M\subseteq\mathbb{R}^n$ tal que per a tot $\mathbf{a}\in M$ existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, un obert $\Omega\subseteq\mathbb{R}^m$ i una funció $\rho\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^n$, $\rho\in\mathcal{C}^r(\Omega)$ amb $\mathrm{rang}\left(D\rho(\mathbf{u})\right)=m$ per a tot $\mathbf{u}\in\Omega$, tals que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiu (és un homeomorfisme).

[T6.4] Teorema 4 (Tema 6) — Equivalència de les definicions de varietat
Les definicions 2 i 3 són equivalents.

[Figura: quadre "Varietat $M$ de dimensió $m$ en $\mathbb{R}^n$ i de classe $\mathcal{C}^r$" amb dues caixes. DEF. 2: FORMA IMPLÍCITA: $\forall\mathbf{a}\in M$, $\exists G$ obert, $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$, tals que $\mathrm{rg}(D\Phi(\mathbf{x}))=n-m$ $\forall\mathbf{x}\in G$, $M\cap G=\{x\in G\mid\Phi(x)=0\}$. DEF. 3: FORMA PARAMÈTRICA: $\forall\mathbf{a}\in M$, $\exists G$ obert, $a\in G\subseteq\mathbb{R}^n$, $\Omega\subseteq\mathbb{R}^m$ obert, $\boldsymbol{\rho}\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^n$, $\boldsymbol{\rho}\in\mathcal{C}^r(\Omega)$, tals que $\mathrm{rg}(D\boldsymbol{\rho}(u))=m$ $\forall u\in\Omega$, $\boldsymbol{\rho}\colon\Omega\to M\cap G$ és bijectiva. (A les caixes, $n$ es marca en verd i $m$, $n-m$ en vermell.)]

[Figura: quadre "RELACIÓ AMB LA NOTACIÓ DEL TEOREMA DE LA FUNCIÓ IMPLÍCITA". Prenem $N=m$, $M=n-m$. $G$ obert, $G\subseteq\mathbb{R}^{N+M}(=\mathbb{R}^n)$, $\Phi\colon G\to\mathbb{R}^M(=\mathbb{R}^{n-m})$, $\Phi\in\mathcal{C}^r(G)$, $\mathbf{a}=(a,b)\in G$, $\Phi(a)=0$, $0\neq\det\left(\frac{\partial\Phi_i}{\partial y_j}\right)_{i,j=1\ldots M(=n-m)}$. Existeixen oberts $U\subseteq G\subseteq\mathbb{R}^{N+M}(=\mathbb{R}^n)$, $\Omega\subseteq\mathbb{R}^N(=\mathbb{R}^m)$, i una funció $\varphi\colon\Omega\to\mathbb{R}^M(=\mathbb{R}^{n-m})$ t.q. ... (iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$, on $x,u\in\mathbb{R}^N(=\mathbb{R}^m)$ i $y,\varphi(u)\in\mathbb{R}^M(=\mathbb{R}^{n-m})$; (ii) $\varphi\in\mathcal{C}^r(\Omega)$, $\varphi(a)=b$ (OBS) $\mathbf{x}=(x,y)$, $\boldsymbol{\rho}(u)=(u,\varphi(u))$.]

Esbós de la relació entre les dues definicions de varietat diferenciable via l'enunciat del teorema de la funció implícita. Fixeu-vos en la coincidència de les notacions un cop assumit que la $N$ i la $M$ del teorema de la funció implícita es corresponen a $m$ i $n-m$, respectivament, en la definició de varietat. Aquesta relació és el nucli de la demostració del teorema 4.

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

[T6.7] Exemple 7 (Tema 6) — Una no-varietat
(una no-varietat). El conjunt $M=\{(x,y)\in\mathbb{R}^2\mid x^2-y^2=0\}$ NO és una 1-varietat.

Observem primer que $\Phi(x,y)=x^2-y^2$, però $D\Phi(0,0)=(0\ 0)$ i, per tant, el seu rang no és 1 (hauria de ser 1 perquè l'espai "ambient" és $\mathbb{R}^n$ amb $n=2$ i ve definit per una sola equació, $n-m=1$). De tota manera, això no exclou la possibilitat que existís una altra funció $\tilde\Phi$ que definís el mateix conjunt, però que complís la propietat de rang 1 arreu.

Per assegurar-nos que no és una 1-varietat, usarem la segona definició de varietat (definició 3) i cercarem $\rho\colon(a,b)\subset\mathbb{R}\longrightarrow\mathbb{R}^2$ de classe $r$ tal que $\rho\colon(a,b)\longrightarrow M\cap G$ sigui bijectiva i $\rho^{-1}$ contínua.

Suposem que existís una tal funció bijectiva i que $\rho^{-1}(0,0)=c$. Llavors, prenent la unió d'intervals $\Omega=(a,c)\cup(c,b)$, tindríem que $\rho(\Omega)$ seria la unió de quatre components connexes disjuntes. Ara bé: tota funció contínua envia connexos a connexos i, per tant, no pot ser que la imatge de la unió de dos intervals disjunts doni lloc a la unió de quatre conjunts disjunts.

[T6.8] Proposició 8 (Tema 6) — Gràfica d'una funció és varietat
Sigui $G$ obert de $\mathbb{R}^m$ i $f\colon G\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^k$ una funció de classe $r$ en $G$. Aleshores, la gràfica de $f$, $\mathrm{Gr}(f)=\{(\mathbf{x},f(\mathbf{x}))\in\mathbb{R}^{m+k}:\mathbf{x}\in G\}$ és una $m$-varietat de classe $r$ a $\mathbb{R}^{m+k}$.

[T6.9] Definició 9 (Tema 6) — Vector, espai tangent i normal
Sigui $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geqslant1$, i $\mathbf{a}\in M$.

(i) Un vector $\mathbf{v}\in\mathbb{R}^n$ és tangent a $M$ en $\mathbf{a}$ si existeix $\delta>0$ i una funció $\alpha\colon(-\delta,\delta)\subset\mathbb{R}\to M$ diferenciable en $t=0$ tal que $\alpha(0)=\mathbf{a}$ i $\alpha'(0)=\mathbf{v}$. (Nota: Usem la notació $\alpha'(t)$ ja que depèn només d'una variable. De fet, $\alpha'(t)=D\alpha(t)\in\mathcal{M}_{1\times n}(\mathbb{R})$.)

(ii) El conjunt $T_M(\mathbf{a})=\{\mathbf{v}\in\mathbb{R}^n\mid\mathbf{v}\text{ és tangent a }M\text{ en }\mathbf{a}\}$ és l'espai tangent a $M$ en el punt $\mathbf{a}$. (Nota: Considerem que el vector $\mathbf{v}=0$ pertany a $T_M(\mathbf{a})$ prenent $\alpha(t)\equiv\mathbf{a}$.)

(iii) El conjunt $N_M(\mathbf{a})=\left(T_M(\mathbf{a})\right)^\perp=\{\mathbf{u}\in\mathbb{R}^n\mid\langle\mathbf{u},\mathbf{v}\rangle=0\quad\forall\mathbf{v}\in T_M(\mathbf{a})\}$ és l'espai normal a $M$ en el punt $\mathbf{a}$.

(iv) $\mathbf{a}+T_M(\mathbf{a})$ és la $m$-varietat tangent a $M$ en el punt $\mathbf{a}$.

(v) $\mathbf{a}+N_M(\mathbf{a})$ és la $(n-m)$-varietat normal a $M$ en el punt $\mathbf{a}$.

[T6.10] Teorema 10 (Tema 6) — Càlcul dels espais tangent i normal
Siguin $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geqslant1$, $\Phi$ i $G$ com a la definició 2, en un entorn del punt $\mathbf{a}\in M$, i $\rho$ i $\Omega$ com a la definició 3. És a dir,

- existeixen oberts $G\in\mathbb{R}^n$ i $\Omega\in\mathbb{R}^m$, amb $\mathbf{a}\in G$;
- existeix una funció $\Phi\colon G\longrightarrow\mathbb{R}^{n-m}\in\mathcal{C}^r(G)$, amb $\mathrm{rang}\,D\Phi(\mathbf{x})=n-m$ per a tot $x\in G$ tal que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=0\}$.
- existeix una funció $\rho\colon\Omega\longrightarrow\mathbb{R}^n\in\mathcal{C}^r(\Omega)$, amb $\mathrm{rang}\,D\rho(\mathbf{u})=m$ per a tot $\mathbf{u}\in\Omega$ tal que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiva; en particular, existeix un únic $\mathbf{b}\in\Omega$ tal que $\rho(\mathbf{b})=\mathbf{a}$.

Aleshores,

(i) $T_M(\mathbf{a})=\ker\left(D\Phi(\mathbf{a})\right)=\langle\text{columnes de }D\rho(\mathbf{b})\rangle$;

(ii) $N_M(\mathbf{a})=\langle\text{files de }D\Phi(\mathbf{a})\rangle=\langle\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})\rangle$.

En particular, $T_M(\mathbf{a})$ i $N_M(\mathbf{a})$ són subespais vectorials de $\mathbb{R}^n$ de dimensions $\dim\left(T_M(\mathbf{a})\right)=m$ i $\dim\left(N_M(\mathbf{a})\right)=n-m$, respectivament.

[T6.11] Exemple 11 (Tema 6) — Espais tangent i normal de l'esfera
Tornem al cas de l'esfera de radi $R$ centrada a l'origen, que hem estudiat a l'exemple 6, per fer-hi el càlcul d'espais i varietats tangents i normals.

Definim $M=\{(x,y,z)\mid x^2+y^2+z^2-R^2=0\}=\mathrm{Im}\rho$, on $\rho$ està definida a l'exemple 6.

Ens situarem en el punt $\mathbf{a}=(R/2,R/2,\sqrt2R/2)$. Un càlcul directe ens dona que $D\Phi(\mathbf{a})=(R\quad R\quad\sqrt2R)$. D'altra banda, $\mathbf{a}=\rho(\mathbf{b})$, on $\mathbf{b}=(\pi/4,\pi/4)$. Així,
$$D\rho(\mathbf{b})=\begin{pmatrix}-R/2&-R/2\\R/2&-R/2\\0&\sqrt2R/2\end{pmatrix}.$$
Utilitzem el teorema 10 per calcular els espais tangent i normal:
$$T_M(\mathbf{a})=\ker D\Phi(\mathbf{a})=\{\mathbf{v}\mid R/2\,v_1+R/2\,v_2+\sqrt2R\,v_3/2=0\};$$
dit d'una altra manera, l'equació del pla tangent és
$$\begin{aligned}R\,(x-R/2)+R\,(y-R/2)+\sqrt2R\,(z-\sqrt2R/2)=0&\ \Leftrightarrow\\(x-R/2)+(y-R/2)+\sqrt2\,(z-\sqrt2R/2)=0&\ \Leftrightarrow\\x+y+\sqrt2\,z=2R.&\end{aligned}$$
També el podíem haver calculat a partir de
$$\mathrm{Im}D\rho(\mathbf{b})=\langle\text{columnes de }D\rho(\mathbf{b})\rangle=\langle(-1,1,0),(-1,-1,\sqrt2)\rangle=\langle(1,1,\sqrt2)\rangle^\perp.$$
Indirectament, ja hem vist que $N_M(\mathbf{a})=\langle(1,1,\sqrt2)\rangle$, i la recta normal ve donada per
$$(x,y,z)=(R/2,R/2,\sqrt2R/2)+t\left((1,1,\sqrt2)\right).$$

[T6.12] Definició 12 (Tema 6) — Extrems condicionats
Siguin $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geq1$, $D\subseteq\mathbb{R}^n$ un obert tal que $M\subseteq D$ i $f\colon D\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(D)$. Diem que un punt $\mathbf{a}\in M$ és un màxim local de $f$ condicionat a $M$ si $\mathbf{a}$ és un màxim local de $f|_M$; és a dir, si existeix un obert $G$ tal que $\mathbf{a}\in G$ i $f(\mathbf{x})\leq f(\mathbf{a})$ per a tot $x\in M\cap G$.

Definim mínim condicionat i màxim i mínim estrictes condicionats d'una manera semblant, canviant $\leq$ per la desigualtat que pertoqui. Per ser punt de sella condicionat, cal que, per a tot obert $G$ tal que $\mathbf{a}\in G$, existeixin $\mathbf{x},\mathbf{y}\in M\cap G$ tals que $f(\mathbf{x})<f(\mathbf{a})$ i $f(\mathbf{y})>f(\mathbf{a})$.

[T6.x2] Apunts del Tema 6, §6.3 — Multiplicadors de Lagrange: motivació
En les variants que hem presentat a l'exemple 1, hem vist que el problema d'extrems condicionats de vegades es pot reduir a un problema d'extrems lliures. En aquesta secció presentem un tractament sistemàtic per mitjà dels *multiplicadors de Lagrange*.

[T6.13] Proposició 13 (Tema 6) — Condició necessària d'extrem condicionat
(condició necessària). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ una funció $\mathcal{C}^r(G)$ tal que $\mathrm{rang}\left(D\Phi(\mathbf{z})\right)=n-m$ per a tot $\mathbf{z}\in G$. Sigui $M_\Phi$ la $m$-varietat associada a la funció $\Phi$ i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(G)$. Si $\mathbf{a}\in M$ és un extrem local de $f$ condicionat a $M_\Phi$, llavors $\nabla f(\mathbf{a})\in N_M(\mathbf{a})$.

[T6.x3] Apunts del Tema 6, §6.3 — El recíproc és fals
En el següent exemple, veiem que el recíproc és fals.

[T6.14] Exemple 14 (Tema 6) — Recíproc fals: cúbica
Considerem la 1-varietat $M$ parametritzada per $\rho\colon(-1,1)\to\mathbb{R}^2$, amb $\rho(t)=(t,t^3)$. Observem que $\rho(0)=(0,0)=:\mathbf{a}$ i que $D\rho(0)=(1\ 0)$. Com que $\dim T_M(\mathbf{a})=1$, $T_M(\mathbf{a}))=\langle(1,0)\rangle$.

Considerem la projecció $f\colon\mathbb{R}^2\to\mathbb{R}$ tal que $f(x,y)=y$. Observem que $\nabla f(0,0)=(0,1)$, que és perpendicular a $(1,0)$ i, per tant, $\nabla f(0,0)\in N_M(\mathbf{a})$. En canvi, $f$ no té un extrem local condicionat a $M$ en $\mathbf{a}=(0,0)$ ja que $f|_M=f(\rho(t))=t^3$ té un punt d'inflexió en $t=0$.

[T6.15] Observació 15 (Tema 6) — Cas no condicionat ($m=n$)
Per a $m=n$ (cas no condicionat), la propietat $\nabla f(\mathbf{a})\in N_M(\mathbf{a})$ equival a $\nabla f(\mathbf{a})=\mathbf{0}$.

[T6.16] Definició 16 (Tema 6) — Funció de Lagrange
Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ com en la proposició 13, $M_\Phi\neq\emptyset$ la varietat associada a $\Phi$, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(G)$. La funció de Lagrange associada a $\Phi$ i $f$ és una funció $L\colon G\times\mathbb{R}^{n-m}\to\mathbb{R}$, definida com
$$L(\mathbf{x},\boldsymbol{\lambda})=f(\mathbf{x})-\lambda_1\Phi_1(\mathbf{x})-\cdots-\lambda_{n-m}\Phi_{n-m}(\mathbf{x}),$$
on $\mathbf{x}=(x_1,\ldots,x_n)\in G$ i $\boldsymbol{\lambda}=(\lambda_1,\ldots,\lambda_{n-m})\in\mathbb{R}^{n-m}$.

[T6.17] Corol·lari 17 (Tema 6) — Teorema dels multiplicadors de Lagrange
(Teorema dels multiplicadors de Lagrange). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ de classe $\mathcal{C}^r$, $M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(G)$. Si $\mathbf{a}\in M_\Phi$ és un extrem local de $f$ condicionat a $M_\Phi$, aleshores existeixen uns valors únics $\lambda_1,\ldots,\lambda_{n-m}\in\mathbb{R}$ tals que $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in G\times\mathbb{R}^{n-m}$ és un punt crític de $L$, és a dir, $(\mathbf{a},\boldsymbol{\lambda})$ és solució del sistema de $2n-m$ equacions
$$\begin{cases}\nabla f(\mathbf{a})-\lambda_1\nabla\Phi_1(\mathbf{a})-\cdots-\lambda_{n-m}\nabla\Phi_{n-m}(\mathbf{a})&=\mathbf{0},\\\Phi(\mathbf{a})&=\mathbf{0}.\end{cases}$$

[T6.18] Exemple 18 (Tema 6) — Extrems condicionats en compactes
Exemples de càlcul d'extrems condicionats a varietats compactes.

[T6.19] Teorema 19 (Tema 6) — Condicions suficients d'extrem condicionat
(condicions suficients). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ com en el corol·lari 17, amb $r\geq2$, $M=M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^2(G)$. Sigui $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in M\times\mathbb{R}^{n-m}$ un punt crític de la funció de Lagrange $L$; considerem la subfunció $F\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ donada per $F(\mathbf{x})=L(\mathbf{x},\lambda_1,\ldots,\lambda_{n-m})$. Llavors,

(i) $q_{HF(\mathbf{a})}$ és definida negativa ($\ominus$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un màxim local estricte de $f$ condicionat a $M$;

(ii) $q_{HF(\mathbf{a})}$ és definida positiva ($\oplus$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un mínim local estricte de $f$ condicionat a $M$;

(iii) $q_{HF(\mathbf{a})}$ és indefinida ($\odot$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un punt de sella de $f$ condicionat a $M$;

(iv) $\mathbf{a}$ és un màxim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida negativa ($\underline{\ominus}$) sobre $T_M(\mathbf{a})$;

(v) $\mathbf{a}$ és un mínim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida positiva ($\underline{\oplus}$) sobre $T_M(\mathbf{a})$.

[T6.20] Exemple 20 (Tema 6) — Extrems locals condicionats: càlcul
Exemple de càlcul d'extrems locals condicionats.

Considerem la funció $f(x,y,z)=2xy-z^2$ i la volem estudiar condicionada a la 2-varietat representada a la figura i definida per $M=\{(x,y,z)\mid x^3+y^3+\frac12z^3=2\}$.

[Figura: superfície 3D de la 2-varietat $x^3+y^3+\frac12z^3=2$ en els eixos $x$, $y$, $z$.]

Definim la funció de Lagrange
$$L(x,y,z,\lambda)=f(x,y,z)+\lambda\,\Phi(x,y,z),$$
amb $\Phi(x,y,z)=x^3+y^3+\frac12z^3-2$.

El sistema $\nabla L=0$ s'escriu com:
$$\begin{cases}\dfrac{\partial L}{\partial x}=2y+3\lambda x^2=0&(I),\\[2mm]\dfrac{\partial L}{\partial y}=2x+3\lambda y^2=0&(II),\\[2mm]\dfrac{\partial L}{\partial z}=-2z+3\lambda z^2/2=0&(III),\\[2mm]\dfrac{\partial L}{\partial\lambda}=x^3+y^3+\frac12z^3-2=0&(IV).\end{cases}$$

Observem primer que:

- De (III), obtenim que o bé $z=0$, o bé $3\lambda z=4$.
- De (I), tenim que $y=-\frac32\lambda x^2$.
- De (II), tenim que $x=-\frac32\lambda y^2$.

Si $x=0$, aleshores, per (I), $y=0$. Si tenim $z=0$ també, no es compleix (IV). Per tant, per (IV), hem de tenir $z=4^{1/3}$ i, per (III), $\lambda=\frac23\sqrt[3]{2}$. El punt crític condicionat resultant és
$$P_1:=(0,0,4^{1/3}),\text{ amb }\lambda=\frac23\sqrt[3]{2}.$$
Si $y=0$, començant per (II), arribem a la mateixa solució.

Suposem ara que $x\neq0$. Per (II), tant $\lambda\neq0$ com $y\neq0$. Dividint les igualtats derivades de (I) i (II), tenim que
$$\frac yx=\frac{x^2}{y^2}\Leftrightarrow x^3=y^3\Leftrightarrow x=y.$$
En particular, substituint a (I) o a (II), arribem a $\lambda=-2/(3x)=-2/(3y)$. Considerem ara les dues possibilitats de (III):

- Si $z=0$, de (IV), obtenim que $x^3+y^3=2x^3=2$ i, per tant, $x=y=1$ i $\lambda=-2/3$. Això dona lloc al punt crític condicionat
$$P_2:=(1,1,0),\text{ amb }\lambda=-2/3.$$
- Si $z\neq0$, aleshores $3\lambda z=4$, i
$$z=\frac{4}{3\lambda}=\frac{4}{3\left(\frac{-2}{3x}\right)}=-2x=-2y.$$
Substituint a (IV), s'obté $x=y=-1$ i, en conseqüència, $z=2$. Per tant, el punt crític condicionat resultant és
$$P_3:=(-1,-1,2),\text{ amb }\lambda=2/3.$$

Usarem ara el teorema 19 per a classificar els punts crítics condicionats. Per a cadascun d'ells, construirem la funció $F(x,y,z)=f(x,y,z)-\lambda^*\Phi(x,y,z)$, on $\lambda^*$ és el valor concret de $\lambda$ que es correspon a cada punt crític.

La matriu hessiana de $F$ és
$$HF(x,y,z)=\begin{pmatrix}6x\lambda&2&0\\2&6y\lambda&0\\0&0&-2+3z\lambda\end{pmatrix}.$$

- Punt $P_1$:
$$HF(P_1)=\begin{pmatrix}0&2&0\\2&0&0\\0&0&-2+3\,4^{1/3}\,\frac23 2^{1/3}\end{pmatrix}=\begin{pmatrix}0&2&0\\2&0&0\\0&0&2\end{pmatrix}.$$
L'hem d'estudiar a $T_M(P_1)=\ker D\Phi(P_1)=\{(v_1,v_2,v_3)\mid v_3=0\}$ ja que $D\Phi=(3x^2,3y^2,\frac32z^2)$. Per tant, sobre $T_M(P_1)$, la forma quadràtica resultant és
$$(v_1,v_2,0)\begin{pmatrix}0&2&0\\2&0&0\\0&0&2\end{pmatrix}\begin{pmatrix}v_1\\v_2\\0\end{pmatrix}=4\,v_1\,v_2,$$
que és indefinida. Per tant, es tracta d'un **punt de sella** local condicionat a la varietat $M$.

- Punt $P_2$:
$$HF(P_2)=\begin{pmatrix}-4&2&0\\2&-4&0\\0&0&-2\end{pmatrix}.$$
L'hem d'estudiar a $T_M(P_2)=\ker D\Phi(P_2)=\{(v_1,v_2,v_3)\mid v_1+v_2=0\}$. Per tant, sobre $T_M(P_2)$, la forma quadràtica resultant és
$$(v_1,-v_1,v_3)\begin{pmatrix}-4&2&0\\2&-4&0\\0&0&-2\end{pmatrix}\begin{pmatrix}v_1\\-v_1\\v_3\end{pmatrix}=-12\,v_1^2-2\,v_3^2,$$
que és definida negativa. Per tant, es tracta d'un **màxim local** condicionat a la varietat $M$.

- Punt $P_3$:
$$HF(P_3)=\begin{pmatrix}-4&2&0\\2&-4&0\\0&0&2\end{pmatrix}.$$
L'hem d'estudiar a $T_M(P_3)=\ker D\Phi(P_3)=\{(v_1,v_2,v_3)\mid v_1+v_2+2v_3=0\}$. Per tant, sobre $T_M(P_3)$, la forma quadràtica resultant és
$$(2v_1,2v_2,-v_1-v_2)\begin{pmatrix}-4&2&0\\2&-4&0\\0&0&2\end{pmatrix}\begin{pmatrix}2v_1\\2v_2\\-v_1-v_2\end{pmatrix}=-14\,v_1^2-14\,v_2^2+20\,v_1\,v_2,$$
que és definida negativa perquè equival a la forma quadràtica donada per
$$\begin{pmatrix}-14&10\\10&-14\end{pmatrix},$$
que és definida negativa. Per tant, es tracta d'un **màxim local** condicionat a la varietat $M$.

[T6.21] Exemple 21 (Tema 6) — Extrems absoluts amb desigualtats
Exemples de càlcul d'extrems absoluts condicionats a restriccions de desigualtat.

Vegeu el darrer cas de l'exemple 1.
</apunts>

## Request

Cobreix el Tema 6 de manera variada.
Dificultat normal: cal pensar el paper de cada hipòtesi; contraexemples coneguts però no immediats.

Escriu EXACTAMENT 11 afirmacions noves, de les quals entre 5 i 7 falses.

## Output

A JSON file: {"font": "tema-6", "dificultat": "normal", "autor": "<your model>", "afirmacions": [...]}, each statement following this schema:

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
                "T5.35",
                "T6.1",
                "T6.2",
                "T6.3",
                "T6.4",
                "T6.5",
                "T6.6",
                "T6.7",
                "T6.8",
                "T6.9",
                "T6.10",
                "T6.11",
                "T6.12",
                "T6.13",
                "T6.14",
                "T6.15",
                "T6.16",
                "T6.17",
                "T6.18",
                "T6.19",
                "T6.20",
                "T6.21"
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

# Writer brief: tema-4, normal (8 statements in the quiz)

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

<apunts tema="4" titol="Teoremes de les funcions diferenciables">
[T4.x1] Apunts del Tema 4, §4.1 — Motivació: problema de la inversa
Considerem el problema de trobar una funció inversa $f^{-1}$ d'una funció $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^n$, $f\in\mathcal{C}^r(\Omega)$, amb $\Omega\subseteq\mathbb{R}^n$ obert.

Un cas particular seria que $f$ fos una funció lineal, que ja coneixem prou bé. En efecte, si $A$ és la matriu de $f$ en una base qualsevol de $\mathbb{R}^n$, tenim que:

- Si $\det A\neq 0$, aleshores, l'equació $f(x)=b$ té solució única per a qualsevol $b\in\mathbb{R}^n$. Per tant, existeix $f^{-1}$ tal que $f^{-1}\circ f=\mathrm{Id}$ i podem expressar la solució del sistema com $x=A^{-1}b$, essent $A^{-1}$ la matriu de $f^{-1}$ en la mateixa base escollida.
- Si $\det A=0$, aleshores $\mathrm{Im}\,f\neq\mathbb{R}^n$, la inversa de $f$ no està definida globalment i, a més, les antiimatges d'un valor $b\in\mathrm{Im}\,f$ no són úniques ja que $f^{-1}(b)=x_b+\mathrm{Nuc}\,f$, on $x_b$ és qualsevol element que satisfaci $f(x_b)=b$.

D'aquesta observació sobre els sistemes lineals, se'n desprèn una conclusió clara: sabem determinar quan existeix la funció inversa i, a més, quan existeix està definida a tot $\mathbb{R}^n$, és a dir, és *global*.

En el món no lineal, no obstant, la situació ja no és tan diàfana. En una variable, per exemple tenim els següents resultats:

[T4.1] Proposició 1 (Tema 4) — Inversió global (una variable)
(inversió global). Sigui $f:I=(a,b)\to\mathbb{R}$ una funció $\mathcal{C}^r$, $r\geqslant 1$, i tal que $f'(c)\neq 0$, $\forall c\in(a,b)$. Llavors $f:I\to f(I)$ és bijectiva, $f^{-1}:f(I)\to I$ també és $\mathcal{C}^r$. A més,
$$(f^{-1})'(y_0)=\frac{1}{f'(f^{-1}(y_0))},\qquad \text{per a } y_0\in f(I).$$

[T4.2] Proposició 2 (Tema 4) — Inversió local (una variable)
(inversió local). Sigui $f:(a,b)\to\mathbb{R}$ una funció $\mathcal{C}^r$, $r\geqslant 1$. Si $f'(c)\neq 0$ per a un determinat $c\in(a,b)$, llavors existeixen $\varepsilon_1,\varepsilon_2,\delta>0$ tals que $f:(c-\delta,c+\delta)\to(f(c)-\varepsilon_1,f(c)+\varepsilon_2)$ és bijectiva i $f'(x)\neq 0$ $\forall x\in(c-\delta,c+\delta)$. A més, la inversa local també és $\mathcal{C}^r$.

[T4.x2] Apunts del Tema 4, §4.1 — Transició: tanmateix, però
Tanmateix, però...

[T4.3] Exemple 3 (Tema 4) — Inversió global falla en dimensió superior
El teorema d'inversió global no és cert en dimensió superior.

Se'n poden construir molts exemples, però aquest és paradigmàtic: considerem el camp vectorial polinòmic
$$f(x,y)=(x^3-3xy^2,\,3x^2y-y^3),$$
que clarament està definit a tot $\mathbb{R}^2$.

La seva matriu jacobiana, que seria el concepte que millor generalitza tant la derivada d'una funció d'una variable com la matriu d'una aplicació lineal, és
$$Jf(x,y)=\begin{pmatrix}3x^2-3y^2 & -6xy\\ 6xy & 3x^2-3y^2\end{pmatrix}.$$

Observem que $\det Jf(x,y)=(3x^2-3y^2)^2+(6xy)^2=9(x^2+y^2)^2\neq 0$ excepte en $(x,y)=(0,0)$. En canvi, $f$ no és injectiva (de fet, es pot pensar com la part real i imaginària de $f(z)=z^3$, amb $z\in\mathbb{C}$), i sabem que $z^3=w$, $w\neq 0\in\mathbb{C}$, sempre té 3 arrels diferents.

Relacionat amb aquest problema, val la pena esmentar la conjectura jacobiana real, que estableix que si el determinant de la matriu jacobiana és 1 arreu, aleshores $F$ és invertible, que s'ha demostrat que no es compleix ni per a $n=2$.

[T4.4] Proposició 4 (Tema 4) — Fitacions de f i injectivitat local
Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^m$ una funció, i $a\in\Omega$.

(i) Si $f$ és diferenciable en $a$, llavors per a tot $\varepsilon>0$, existeix $\delta>0$ tal que per a tot $x\in B(a,\delta)\subseteq\Omega$, es compleix que $\|f(x)-f(a)\|\leqslant\big(\|Df(a)\|+\varepsilon\big)\|x-a\|$.

(ii) Si $f\in\mathcal{C}^1(\Omega)$, llavors per a tot $\varepsilon>0$ existeix $\delta>0$ tal que per a tot $x,y\in B(a,\delta)\subseteq\Omega$, es compleix que $\|f(x)-f(y)\|\leqslant\big(\|Df(a)\|+\varepsilon\big)\|x-y\|$.

(iii) Si $n=m$, $f\in\mathcal{C}^1(\Omega)$, i $\det Jf(a)\neq 0$, llavors per a tot $\varepsilon>0$ existeix $\delta>0$ tal que per a tot $x,y\in B(a,\delta)\subseteq\Omega$, es compleix que $\|f(x)-f(y)\|\geqslant(c-\varepsilon)\|x-y\|$, on $c=1/\|(Df(a))^{-1}\|$. (En particular, $f$ és localment injectiva.)

[T4.x3] Apunts del Tema 4, §4.1 — Anunci del teorema de la funció inversa
Enunciem ara el teorema de la funció inversa.

[T4.5] Teorema 5 (Tema 4) — Teorema de la funció inversa
(de la funció inversa). Sigui $\Omega\subseteq\mathbb{R}^n$ obert, $f:\Omega\to\mathbb{R}^n$ una funció $\mathcal{C}^r(\Omega)$, i $a\in\Omega$ tal que $\det\big(Jf(a)\big)\neq 0$. Llavors existeix $U\in\mathcal{E}_a$, $U\subseteq\Omega$, tal que

(i) $f|_U:U\to\mathbb{R}^n$ és injectiva, i $\det\big(Jf(z)\big)\neq 0$ $\forall z\in U$;

(ii) $V=f(U)\subseteq\mathbb{R}^n$ és obert;

(iii) la inversa $f^{-1}:V\to U$ és $\mathcal{C}^r(V)$ i, a més, $Df^{-1}(y_0)=\big(Df(f^{-1}(y_0))\big)^{-1}$.

[T4.6] Exemple 6 (Tema 4) — Exemples d'ús del TFI
Exemples d'ús del teorema de la funció inversa.

1. Considerem la funció
$$\begin{aligned}f:\mathbb{R}^2&\longrightarrow\mathbb{R}^2\\ (x,y)&\longmapsto e^x\,(\cos y,\sin y).\end{aligned}$$
Fixem-nos que per la periodicitat d'ambdues components respecte $y$, $f$ és clarament no injectiva. Addicionalment, observem que les dues components de $f$ són les parts real i imaginària, respectivament, de la funció de variable complexa $e^z$, amb $z=x+i\,y$.

D'altra banda,
$$\det Jf(x,y)=\begin{vmatrix}e^x\cos y&-e^x\sin y\\ e^x\sin y&e^x\cos y\end{vmatrix}=e^{2x}\neq 0\qquad\forall(x,y)\in\mathbb{R}^2.$$
D'entrada, doncs, veiem que, malgrat que el determinant de la matriu jacobiana no s'anul·la mai, $f$ no té una inversa global.

Ara bé, pel teorema de la funció inversa, com que $f$ és de classe $C^\infty$, en qualsevol punt $(x_0,y_0)\in\mathbb{R}^2$ podrem definir localment una funció inversa que serà també de classe $C^\infty$. Ho veurem per a un cas concret, prenent $(x_0,y_0)=(0,\pi/3)$.

Un càlcul directe ens dona que $f(0,\pi/3)=(\frac12,\frac{\sqrt3}{2})$. Llavors, $f^{-1}$ existeix en un entorn de $(\frac12,\frac{\sqrt3}{2})$ i, a més,
$$Df^{-1}\big(\tfrac12,\tfrac{\sqrt3}{2}\big)=\big(Df(0,\pi/3)\big)^{-1}=\begin{pmatrix}\frac12&-\frac{\sqrt3}{2}\\ \frac{\sqrt3}{2}&\frac12\end{pmatrix}^{-1}=\begin{pmatrix}\frac12&\frac{\sqrt3}{2}\\ -\frac{\sqrt3}{2}&\frac12\end{pmatrix}.$$
Observem que en aquest cas també es pot calcular $f^{-1}$ explícitament i, per tant, fer el càlcul de la seva matriu jacobiana sense aplicar el TFI. En efecte, si ens plantegem el sistema
$$\begin{cases}e^x\cos y=u,\\ e^x\sin y=v,\end{cases}$$
podem expressar
$$\begin{cases}u^2+v^2=e^{2x},\\ \dfrac{v}{u}=\tan y;\end{cases}\qquad\Leftrightarrow\qquad\begin{cases}x=x(u,v)=\frac12\ln(u^2+v^2),\\ y=y(u,v)=\arctan v/u.\end{cases}$$
Lligat amb el fet que $f$ és periòdica (i, per tant, no injectiva en $y$), constatem que $y(u,v)$ ni tan sols és contínua per a $u=0$. Però localment, podem considerar la seva diferencial per a $u\neq 0$:
$$\begin{aligned}Df^{-1}\big(\tfrac12,\tfrac{\sqrt3}{2}\big)=\frac{\partial(x,y)}{\partial(u,v)}\big(\tfrac12,\tfrac{\sqrt3}{2}\big)&=\begin{pmatrix}\dfrac{u}{u^2+v^2}&\dfrac{v}{u^2+v^2}\\ \dfrac{-v/u^2}{1+v^2/u^2}&\dfrac{1/u}{1+v^2/u^2}\end{pmatrix}_{(\frac12,\frac{\sqrt3}{2})}\\ &=\begin{pmatrix}\dfrac{u}{u^2+v^2}&\dfrac{v}{u^2+v^2}\\ \dfrac{-v}{u^2+v^2}&\dfrac{u}{u^2+v^2}\end{pmatrix}_{(\frac12,\frac{\sqrt3}{2})}=\begin{pmatrix}\frac12&\frac{\sqrt3}{2}\\ -\frac{\sqrt3}{2}&\frac12\end{pmatrix}.\end{aligned}$$

2. Una aplicació rellevant del teorema de la funció inversa és el càlcul de solucions aproximades de sistemes no lineals. Suposem que volem resoldre $f(x)=y$ i que coneixem que $f(p)=q$ per a un valor $q$ proper a $y$. Si $f$ és diferenciable en un obert que contingui $p$, i $\det Df(p)\neq 0$, aleshores, $f^{-1}$ és diferenciable en un entorn de $q$, i
$$\lim_{y\to q}\frac{\|f^{-1}(y)-f^{-1}(q)-Df(p)^{-1}(y-q)\|}{\|y-q\|}=0.$$
Per tant, podem aproximar $f^{-1}(y)$ per $f^{-1}(q)+Df(p)^{-1}(y-q)$, és a dir,
$$x\approx p+Df(p)^{-1}(y-q),$$
que equival a trobar l'aproximació resolent el sistema
$$Df(p)\,(x-p)=y-q.$$
Apliquem-ho, per exemple, al sistema
$$\begin{cases}x_1^3x_2^2x_3+x_1^2x_2^3x_3^2+x_1&=3.1,\\ x_1^2x_2^3+x_2^3x_3^2+x_3&=2.9,\\ x_2^3x_3^3+x_1x_3+x_1&=3.2,\end{cases}$$
que podem escriure de manera abreujada com $f(x_1,x_2,x_3)=(3.1,2.9,3.2)=:y$. Observem que el sistema $f(x_1,x_2,x_3)=(3,3,3)=:q$ té la solució $p=(1,1,1)$, i que
$$Df(p)=\begin{pmatrix}6&5&3\\ 2&6&3\\ 2&3&4\end{pmatrix},\ \text{ amb }\det Df(p)=62\neq 0.$$
Per tant, una solució aproximada de $f(x_1,x_2,x_3)=y$ és $x^*$ tal que
$$\begin{pmatrix}6&5&3\\ 2&6&3\\ 2&3&4\end{pmatrix}\begin{pmatrix}x_1^*-1\\ x_2^*-1\\ x_3^*-1\end{pmatrix}=\begin{pmatrix}0.1\\ -0.1\\ 0.2\end{pmatrix};\ \text{ és a dir, }\ \begin{pmatrix}6&5&3\\ 2&6&3\\ 2&3&4\end{pmatrix}\begin{pmatrix}x_1^*\\ x_2^*\\ x_3^*\end{pmatrix}=\begin{pmatrix}14.1\\ 10.9\\ 9.2\end{pmatrix}.$$
La solució del sistema és $x^*\approx(1.0323,0.9290,1.0871)$. A partir d'aquest punt, podríem calcular una nova aproximació prenent $p=x^*$, $q=f(x^*)\approx(3.0740,2.8891,3.1846)$ i, igual que abans, $y=(3.1,2.9,3.2)$. Observem com $\|y-q\|$ s'ha reduït: de $\sqrt{0.1^2+0.1^2+0.2^2}=\sqrt{0.06}\approx 0.2449$, hem passat a $\sqrt{(3.1-3.0740)^2+(2.9-2.8891)^2+(3.2-3.1846)^2}\approx 0.0321$.

A https://atenea.upc.edu/mod/resource/view.php?id=5449143 podeu trobar els càlculs de dos iterats més d'aquesta aproximació a la solució del sistema $f(x_1,x_2,x_3)=(3.1,2.9,3.2)$,

[T4.7] Definició 7 (Tema 4) — Funció oberta
Una funció $f:U\subseteq\mathbb{R}^n\to V\subseteq\mathbb{R}^n$ es diu que és oberta si la imatge de tot obert és un obert.

[T4.8] Corol·lari 8 (Tema 4) — Teorema de l'aplicació oberta
Teorema de l'aplicació oberta. Sigui $f:U\subseteq\mathbb{R}^n\to V\subseteq\mathbb{R}^n$ una funció $\mathcal{C}^1(U)$ tal que $\det Jf(a)\neq 0$ per a tot $a\in U$. Aleshores, per a tot obert $B\subseteq U$, $f(B)$ és també un obert.

[T4.9] Definició 9 (Tema 4) — Homeomorfisme i difeomorfisme
1. Una funció $f:\Omega\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$ és un homeomorfisme si $f$ és bijectiva, contínua i la seva inversa $f^{-1}$ també és contínua.

2. Una funció $f:U\longrightarrow V$ entre dos oberts $U,V$ de $\mathbb{R}^n$ és un difeomorfisme (o una transformació regular) de classe $C^r$, amb $r\geq 1$, si $f$ és bijectiva, de classe $C^r$ i la seva inversa $f^{-1}$ també és de classe $C^r$.

Els homeomorfisme preserven la forma topològica, mentre que els difeomorfisme també preserven l'estructura diferenciable.

[Resum 91'] Una definició alternativa de difeomorfisme és: Una funció $f:U\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^n$, amb $U$ obert de $\mathbb{R}^n$, és un difeomorfisme si $f\in\mathcal{C}^1(U)$, $f$ és injectiva, i $\det\big(Jf(x)\big)\neq 0$ per a tot $x\in U$.

[T4.10] Observació 10 (Tema 4) — Inversa i composició de difeomorfismes
- L'invers d'un difeomorfisme és un difeomorfisme.
- La composició de difeomorfismes és un difeomorfisme.

[T4.11] Exemple 11 (Tema 4) — Canvis de variables
(Canvis de variables). Exemples de difeomorfismes.

Sovint ens trobem els difeomorfismes en el context de canvis de variables. En repassarem els més habituals.

1. Coordenades polars. Considerem $f:\Omega\subset\mathbb{R}^2\longrightarrow\mathbb{R}^2$, amb $\Omega=\{(r,\theta)\in\mathbb{R}^2\mid r>0,\ \theta\in(0,2\pi)\}$, tal que $f(r,\theta)=(r\cos\theta,r\sin\theta)$. Fixem-nos en la tria del domini $\Omega$, que no comprèn l'origen ni les "rectes" $\{\theta=0\}$ i $\{\theta=2\pi\}$.

La funció $f$ és injectiva i de classe $\mathcal{C}^\infty$. A més,
$$\det Jf(r,\theta)=\begin{vmatrix}\cos\theta&-r\sin\theta\\ \sin\theta&r\cos\theta\end{vmatrix}=r\neq 0\ \text{ en }\Omega.$$
Per tant, és un difeomorfisme. Una manera d'expressar (parcialment) la seva funció inversa és
$$\begin{aligned}f^{-1}:V\subset\mathbb{R}^2&\longrightarrow\mathbb{R}^2\\ (x,y)&\longmapsto\Big(\sqrt{x^2+y^2},\arccos\frac{x}{\sqrt{x^2+y^2}}\Big).\end{aligned}$$
Fixem-nos que, amb aquesta elecció, el domini de $f^{-1}$ és $V=\{(x,y)\in\mathbb{R}^2:\ y\geq 0\}\setminus\{(0,0)\}$. En canvi, la imatge de $\Omega$ per $f$ és el conjunt $W=\mathbb{R}^2\setminus\{(x,0),\ x\geq 0\}$. A més, com a inversa tenim diverses opcions, com ara $\arctan(y/x)$ o $\arcsin(y/\sqrt{x^2+y^2})$, els dominis de les quals tampoc coincideixen amb $V$. Podríem dir que la inversa existeix en el domini $V$, però cap de les funcions inverses proposades es pot aplicar en tot el domini.

Finalment, observem que si consideréssim $\Omega=\{(r,\theta)\in\mathbb{R}^2\mid r>0,\ \theta\in[0,2\pi)\}$, aleshores el conjunt imatge seria $W=\mathbb{R}^2\setminus\{(0,0)\}$, però el domini no seria obert en $\mathbb{R}^2$.

Aquesta discordància entre dominis i l'arbitrarietat en considerar funcions inverses desapareix si ens mirem les funcions com a funcions de variable complexa, però això va més enllà dels objectius d'aquesta assignatura.

2. Coordenades cilíndriques. Considerem $f:U\subset\mathbb{R}^3\longrightarrow V\subset\mathbb{R}^3$, definida com $f(r,\theta,z)=(r\cos\theta,r\sin\theta,z)$, amb $U=\{(r,\theta,z)\in\mathbb{R}^3\mid r>0,\ \theta\in(0,2\pi),\ z\in\mathbb{R}\}$ i $V=\mathbb{R}^3\setminus\{(x,0,z)\in\mathbb{R}^3\mid x\geq 0\}$.

Observem que el determinant de la matriu jacobiana tampoc s'anul·la en $U$:
$$|Jf(r,\theta)|=\begin{vmatrix}\cos\theta&-r\sin\theta&0\\ \sin\theta&r\cos\theta&0\\ 0&0&1\end{vmatrix}=r\neq 0.$$
En aquest cas, el conjunt imatge és
$$V=\mathbb{R}^3\setminus\{(x,y,z):x\geq 0,\ y=0\}.$$

3. Coordenades esfèriques. Considerem $f:U\subset\mathbb{R}^3\longrightarrow V\subset\mathbb{R}^3$, definida com $f(r,\theta,\varphi)=(r\sin\varphi\cos\theta,r\sin\varphi\sin\theta,r\cos\varphi)$, amb $U=\{(r,\theta,\varphi)\in\mathbb{R}^3\mid r>0,\ \theta\in(0,2\pi),\ \varphi\in(0,\pi)\}$ i $V=\mathbb{R}^3\setminus\big(\{(x,0,z)\in\mathbb{R}^3\mid x\geq 0\}\cup\{z=\pm1\}\big)$.

Les variables $\theta$ i $\varphi$ representen, en coordenades geogràfiques, la longitud i la colatitud, respectivament.

Observem que el determinant de la matriu jacobiana tampoc s'anul·la en $U$:
$$|Jf(r,\theta)|=\begin{vmatrix}\sin\varphi\cos\theta&-r\sin\theta\sin\varphi&r\cos\varphi\cos\theta\\ \sin\varphi\sin\theta&r\cos\theta\sin\varphi&r\cos\varphi\sin\theta\\ \cos\varphi&0&-r\sin\varphi\end{vmatrix}=-r^2\sin\varphi\neq 0.$$

[T4.12] Nota 12 (Tema 4) — Motivació del teorema de la implícita
Explicació 12 (motivació del teorema de la funció implícita). El teorema de la funció implícita es pot interpretar des de dos punts de vista diferents, l'analític i el geomètric.

Per il·lustrar la versió analítica, prenem una funció de dues variables $f(x,y)$ definida en un domini $U\subset\mathbb{R}^2$. Aleshores, diem que l'equació $f(x,y)=0$ defineix implícitament $y=\varphi(x)$ en $\Omega$ si $f(x,y)=0$ i $y=\varphi(x)$ són equivalents per a tot $(x,y)\in\Omega$.

Geomètricament, equival a dir que el conjunt $M=\{(x,y)\in\Omega:f(x,y)=0\}$ és la gràfica d'alguna funció $\varphi$, és a dir, que per a cada $x_0$ del domini, $M$ talla $\{x=x_0\}$ exactament una vegada.

El teorema de la funció implícita s'enuncia per al cas general en què $x\in\mathbb{R}^n$ i $y\in\mathbb{R}^m$ i $f:\Omega\subseteq\mathbb{R}^{n+m}\to\mathbb{R}^m$, però, per prendre consciència del problema, igual que vam fer amb el teorema de la funció inversa, començarem fixant-nos en dues situacions que ens són familiars: les funcions de la dimensió més baixa possible ($n=1$, $m=1$) i les funcions lineals amb $n+m$ variables i $m$ components.

1. Considerem l'equació d'una recta al pla $ax+by+c=0$. Sabem que si $a\neq 0$, podem posar $x$ en funció de $y$, i que si $b\neq 0$, podem posar $y$ en funció de $x$:
$$x=-(by+c)/a;\qquad y=-(ax+c)/b.$$
En aquest exemple, $f(x,y)=ax+by+c$, mentre que en un cas tindríem $\varphi(y):=-(by+c)/a$ i en l'altre, $\varphi(x):=-(ax+c)/b$. En tots dos casos, observem que si el coeficient que acompanya una variable és diferent de zero, aleshores podem posar aquella variable en funció de l'altra. Observem que
$$a=\frac{\partial f}{\partial x};\qquad b=\frac{\partial f}{\partial y}.$$
En aquest exemple, hem pogut calcular $\varphi$ de manera explícita, però veurem més endavant que no és el més habitual... i d'aquí el terme *implícita* que acompanya els resultats d'aquesta secció.

2. Considerem ara una funció no lineal senzilla: $f(x,y)=x^2+y^2-1$. Clarament, $f(x,y)=0$ és un cercle de radi 1 centrat a l'origen.

Si volem escriure una variable en funció de l'altra, per exemple, $y$ en funció de $x$ (per simetria, l'altre cas és idèntic), tenim que
$$y=\pm\sqrt{1-x^2}=:\pm\varphi(x),\ \text{ amb }x\in[-1,1].$$
D'entrada, si bé es pot escriure explícitament, ja veiem que tenim dues funcions per a cada $x$. Però si ens situem a $(-1,0)$ o a $(1,0)$ ja veiem que $\varphi(x)$ no està definida en un entorn del punt. En canvi, en qualsevol punt de la forma $(x_0,\sqrt{1-x_0^2})$, amb $x_0\in(-1,1)$, sí que, localment, podem definir $y=\varphi(x)$ tal que $\varphi(x_0)=\sqrt{1-x_0^2}$ (anàlogament per a punts de la forma $(x_0,-\sqrt{1-x_0^2})$, amb $x_0\in(-1,1)$).

Acabem observant, amb tota la intenció, que $\dfrac{\partial f}{\partial y}=2\,y$ i, per tant, que
$$\frac{\partial f}{\partial y}(\pm1,0)=0;\qquad\frac{\partial f}{\partial y}\Big(x_0,\sqrt{1-x_0^2}\Big)\neq 0,\ \text{ si }x_0\in(-1,1).$$

3. El significat del terme "implícit", el veurem plenament en funcions com
$$f(x,y)=y+x^2y+e^xy^3+x^4y^5+\sin x=0$$
en què es pot definir localment $y=\varphi(x)$ per a tot $x\in\mathbb{R}$ perquè
$$\frac{\partial f}{\partial y}(x,y)=1+x^2+3e^xy^2+5x^4y^4>0,$$
però que $y$ no es pot aïllar explícitament.

4. Considerem, per exemple, el sistema
$$\begin{cases}3x_1+x_2+x_3+x_4&=0,\\ x_1+x_2+x_3+x_4&=0.\end{cases}$$
Té rang 2 i 4 variables; per tant, és un sistema compatible indeterminat amb dos graus de llibertat, que es pot interpretar com $f(x)=0$, on $x=(x_1,x_2,x_3,x_4)$ i $f:\mathbb{R}^4\to\mathbb{R}^2$, amb $f(x)=(3x_1+x_2+x_3+x_4,\,x_1+x_2+x_3+x_4)$.

La solució del sistema és $x_1=0$ i $x_2+x_3+x_4=0$. Per tant, podem expressar $(x_1,x_j)$, per a $j=2,3,4$, en funció de les altres dues variables, però, en canvi, no podem expressar $(x_j,x_k)$ amb $j,k\in\{2,3,4\}$ en funció de $x_1$ i la variable restant. "Casualment", es dona la circumstància que
$$\left|\frac{\partial f}{\partial(x_1,x_j)}\right|=\begin{vmatrix}3&1\\ 1&1\end{vmatrix}=2\neq 0,\qquad\forall j\in\{2,3,4\},$$
$$\left|\frac{\partial f}{\partial(x_j,x_k)}\right|=\begin{vmatrix}1&1\\ 1&1\end{vmatrix}=0,\qquad\forall j,k\in\{2,3,4\}.$$
Es pot veure fàcilment que, si consideréssim, per exemple, el sistema
$$\begin{cases}3x_1+\mathbf{2}x_2+x_3+x_4&=0,\\ x_1+x_2+x_3+x_4&=0,\end{cases}$$
aleshores $(x_3,x_4)$ és l'únic parell de variables que no podríem posar simultàniament en funció de les altres dues variables.

El teorema de la funció implícita generalitza aquestes situacions. En el cas de les funcions lineals, ens dirà (cosa que ja sabem d'àlgebra lineal) que per al sistema
$$\begin{cases}a_{11}x_1+\cdots+a_{1n}x_n+b_{11}y_1+\cdots+b_{1m}y_m&=0,\\ \vdots&\vdots\\ a_{m1}x_1+\cdots+a_{mn}x_n+b_{m1}y_1+\cdots+b_{mm}y_m&=0,\end{cases}$$
si tenim que
$$\det\begin{pmatrix}b_{11}&\ldots&b_{1m}\\ \vdots&\vdots&\vdots\\ b_{m1}&\ldots&b_{mm}\end{pmatrix}\neq 0,$$
aleshores $(y_1,\ldots,y_m)$ es poden posar en funció de $(x_1,\ldots,x_n)$.

[T4.13] Teorema 13 (Tema 4) — Teorema de la funció implícita
(de la funció implícita). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi:G\to\mathbb{R}^m$, $(x,y)\mapsto\Phi(x,y)$, una funció $\mathcal{C}^r(G)$, $r\geq 1$, i $(a,b)\in G$ tal que $\Phi(a,b)=0$ i $\det\big(\partial\Phi_i/\partial y_j(a,b)\big)_{i,j=1,\ldots,m}\neq 0$. Aleshores, existeixen dos oberts $U$ i $\Omega$, tals que $a\in\Omega\subseteq\mathbb{R}^n$ i $(a,b)\in U\subseteq G\subseteq\mathbb{R}^{n+m}$, i una funció $\varphi:\Omega\to\mathbb{R}^m$, tals que

(i) $\det\big(\partial\Phi_i/\partial y_j(z)\big)_{i,j=1,\ldots,m}\neq 0$ $\forall z\in U$;

(ii) $\varphi\in\mathcal{C}^r(\Omega)$ i $\varphi(a)=b$;

(iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$; en particular, $\Phi(x,\varphi(x))=0$ per a tot $x\in\Omega$.

[Figura: Dibuix amb eixos $x$, $y$; un domini $G$ (corba de punts) que conté la corba blava $\Phi(x,y)=0$ (una el·lipse); a l'entorn del punt $(a,b)$ la corba és la gràfica $y=\varphi(x)$ (traç lila) sobre l'entorn $\Omega$ de $a$ a l'eix $x$; als dos extrems de l'el·lipse (línies vermelles verticals) $\det\big(\partial\Phi_i/\partial y_j\big)_{i,j=1,\ldots,m}=0$.]

[T4.14] Observació 14 (Tema 4) — Igualtats entre h i Φ
Siguin $(x,y)\in U$ i $(u,v)\in V$, amb $x,u\in\mathbb{R}^n$ i $y,v\in\mathbb{R}^m$. Llavors, es compleixen les igualtats
$$y=h(x,\Phi(x,y));\qquad\Phi(u,h(u,v))=v.$$

[T4.15] Observació 15 (Tema 4) — Diferencial de la funció implícita
$D\varphi(a)$ es pot calcular aplicant la regla de la cadena a l'equació $\Phi(x,\varphi(x))=0$ en un entorn de $(a,b)$:
$$\frac{\partial\Phi}{\partial x}(a,b)+\frac{\partial\Phi}{\partial y}(a,b)\cdot\frac{\partial\varphi}{\partial x}(a)=0.$$

A l'enunciat de l'observació hem mantingut la notació en derivades parcials, però cal tenir en compte que $\dfrac{\partial\varphi}{\partial x}(a)$ és simplement $D\varphi(a)$.

[T4.16] Exemple 16 (Tema 4) — Aplicació del teorema de la implícita
(aplicació del teorema funció implícita). Considerem el sistema no lineal
$$\begin{cases}x-3y^2+z&=0,\\ 4y+yz-z+w&=0,\end{cases}$$
i ens plantegem expressar $(x,y)$ en funció de $(z,w)$.

En el llenguatge del teorema de la funció implícita,
$$\Phi(x,y,z,w)=\big(x-3y^2+z,\,4y+yz-z+w\big),\ \Phi(0,0,0,0)=(0,0),$$
i volem trobar $U,\Omega$ entorns oberts de $(0,0,0,0)$ i $(0,0)$, respectivament, i una funció $\varphi:\Omega\longrightarrow\mathbb{R}^2$ tal que $(x,y)=\varphi(z,w)$. Recordem, d'altra banda, que això equival a $\Phi(x,y,z,w)=0$.

Ens plantegem, a més, calcular la diferencial de $\varphi$, en la línia de l'observació 15.

Primer de tot, calculem la jacobiana de $\Phi$:
$$D\Phi(x,y,z,w)=\begin{pmatrix}1&-6y&1&0\\ 0&4+z&y-1&1\end{pmatrix};\qquad D\Phi(0,0,0,0)=\begin{pmatrix}1&0&1&0\\ 0&4&-1&1\end{pmatrix}.$$
En particular,
$$\frac{\partial\Phi}{\partial(x,y)}=\begin{pmatrix}1&-6y\\ 0&4+z\end{pmatrix};\qquad\left|\frac{\partial\Phi}{\partial(x,y)}\right|=4+z\neq 0\ \text{ si }z\neq-4;\qquad\frac{\partial\Phi}{\partial(x,y)}(0,0,0,0)=\begin{pmatrix}1&0\\ 0&4\end{pmatrix}.$$
Per tant, podem aplicar el teorema de la implícita en $a=(0,0)$ i $\varphi$ està ben definida i és $\mathcal{C}^\infty$ en un entorn obert $\Omega$ del punt $a$. D'altra banda, seguint l'esquema
$$\begin{array}{ccccc}\Omega\subseteq\mathbb{R}^2&\xrightarrow{\ I\times\varphi\ }&U\subseteq\mathbb{R}^4&\xrightarrow{\ \Phi\ }&\mathbb{R}^2\\ (z,t)&\longmapsto&(z,t,\varphi(z,t))&\longmapsto&\Phi(z,t,\varphi(z,t))=0\\ (0,0)&\longmapsto&(0,0,0,0)&\longmapsto&0\end{array}$$
estudiat a l'observació 15, podem calcular la diferencial de $\varphi$ a partir de la igualtat
$$0=D\Phi(0,0,0,0)\,D(\varphi\times I)(0,0),$$
és a dir,
$$\begin{pmatrix}0&0\\ 0&0\end{pmatrix}=\begin{pmatrix}1&0&1&0\\ 0&4&-1&1\end{pmatrix}\begin{pmatrix}\frac{\partial x}{\partial z}&\frac{\partial x}{\partial w}\\ \frac{\partial y}{\partial z}&\frac{\partial y}{\partial w}\\ 1&0\\ 0&1\end{pmatrix}_{(0,0)}=\begin{pmatrix}1&0\\ 0&4\end{pmatrix}\begin{pmatrix}\frac{\partial x}{\partial z}&\frac{\partial x}{\partial w}\\ \frac{\partial y}{\partial z}&\frac{\partial y}{\partial w}\end{pmatrix}_{(0,0)}+\begin{pmatrix}1&0\\ -1&1\end{pmatrix}.$$
Per tant,
$$D\varphi(0,0)=\begin{pmatrix}\frac{\partial x}{\partial z}&\frac{\partial x}{\partial w}\\ \frac{\partial y}{\partial z}&\frac{\partial y}{\partial w}\end{pmatrix}_{(0,0)}=-\begin{pmatrix}1&0\\ 0&1/4\end{pmatrix}\begin{pmatrix}1&0\\ -1&1\end{pmatrix}=\begin{pmatrix}-1&0\\ 1/4&-1/4\end{pmatrix}.$$
Com a exercici de consolidació, us podeu plantejar de calcular-la en un altre punt, o de plantejar-vos quins parells de variables poden posar-se en funció de les altres dues a l'origen.

Malgrat que ja hem calculat el que volíem, fixem-nos que en aquest cas, el sistema es pot resoldre explícitament. De la segona equació tenim que $y=\dfrac{z-w}{4+z}=:\varphi_2(z,w)$ i, substituint a la primera equació, $x=3\left(\dfrac{z-w}{4+z}\right)^2-z=:\varphi_1(z,w)$. Aleshores,
$$\frac{\partial y}{\partial z}=\frac{4+w}{(4+z)^2},\ \frac{\partial y}{\partial w}=\frac{-1}{4+z};\qquad\frac{\partial x}{\partial z}=6\frac{4+w}{(4+z)^2}\frac{\partial y}{\partial z}-1,\ \frac{\partial x}{\partial w}=6\frac{4+w}{(4+z)^2}\frac{\partial y}{\partial z},$$
i, avaluant en $(z,t)=(0,0)$:
$$D\varphi(0,0)=\begin{pmatrix}-1&0\\ 1/4&-1/4\end{pmatrix}.$$

[T4.17] Nota 17 (Tema 4) — Motivació del redreçament del domini
Explicació 17. Motivació i interpretació del teorema de redreçament del domini.

Les funcions més simples entre $\mathbb{R}^{n+m}$ i $\mathbb{R}^m$ són les projeccions, és a dir, funcions $\tilde\Phi$ tals que $\tilde\Phi(u,v)=v$. En principi, la funció $\Phi$ que hem considerat al teorema de la funció implícita no té perquè ser tan simple, però si trobem un canvi de variables (és a dir, un difeomorfisme) entre oberts $V$ i $U$, $g:V\subset\mathbb{R}^{n+m}\longrightarrow U\subset\mathbb{R}^{n+m}$ tal que $\tilde\Phi(u,v):=\Phi(g(u,v))=v$, estarem "deformant" el domini de manera que ara la nova aplicació $\tilde\Phi$ es comporti com una projecció.

Geomètricament, estem dient que les corbes de nivell de $\Phi$,
$$\mathcal{C}_v=\{(u,v)\in U:\ \Phi(u,v)=v\},\ v\in\mathbb{R}^m,$$
que en principi són superfícies qualssevol de dimensió $n$ en $\mathbb{R}^{n+m}$, passarien (mitjançant $g^{-1}$) a ser hiperplans de dimensió $n$ en $\mathbb{R}^{n+m}$, horitzontals a l'hiperplà coordenat $(v_1,\ldots,v_m)=v$. Ho podem veure il·lustrat a la següent figura.

[Figura: tres panells: un domini $V\subset\mathbb{R}^{n+m}$ amb línies de nivell horitzontals (vermelles) a l'esquerra; una fletxa $g$ cap a un domini deformat $U$ amb les línies corbes; una fletxa $\Phi$ cap a un segment vertical a $\mathbb{R}^m$ amb marques.]
Idea gràfica del teorema de redreçament del domini: les corbes de nivell de $\Phi$ són superfícies regulars (ja entrarem en detall en la regularitat) qualssevol de dimensió $n$ en $\mathbb{R}^{n+m}$; gràcies al redreçament, les corbes de nivell de $\Phi\circ g$ són varietats lineals de dimensió $n$ en $\mathbb{R}^{n+m}$.

Una condició necessària per poder fer aquest redreçament és que $\mathrm{rang}\big(D\Phi\big)=m$ allà on ho vulguem aplicar. Per veure-ho, fixem-nos que, per ser $\tilde\Phi$ una projecció sobre $\mathbb{R}^m$
$$D\tilde\Phi=D(\Phi\circ g)=\left(\begin{array}{ccc|cccc}0&\ldots&0&1&0&\ldots&0\\ \vdots&\vdots&\vdots&0&1&\ddots&0\\ \vdots&\vdots&\vdots&0&\ddots&\ddots&0\\ 0&\ldots&0&0&\ddots&0&1\end{array}\right)=(0_{m,n}\mid Id_m);$$
hem posat les dimensions com a subíndexs per fer-ho més entenedor. Llavors, per la regla de la cadena:
$$D\Phi\,Dg=(0_{m,n}\mid Id_m),$$
i com que $Dg$ és una matriu $(n+m)\times(n+m)$ invertible, aleshores cal que $\mathrm{rang}\big(D\Phi\big)=m$.

A partir d'aquesta explicació, doncs, el següent enunciat emergeix de manera natural:

[T4.18] Teorema 18 (Tema 4) — Teorema de redreçament del domini
(de redreçament del domini). Sigui $G\subseteq\mathbb{R}^{n+m}$ obert, $\Phi$ una funció $\mathcal{C}^r(G)$, $\Phi:G\subset\mathbb{R}^{n+m}\to\mathbb{R}^m$, i $(a,b)\in G$ tals que $\mathrm{rang}\big(D\Phi(a,b)\big)=m$. Llavors, existeixen oberts $U,V\subset\mathbb{R}^{n+m}$, amb $(a,b)\in U\subseteq G$, i un $\mathcal{C}^r$-difeomorfisme $g:V\to U$ tals que $\Phi\circ g:V\to U\to\mathbb{R}^k$ és la projecció $\tilde\Phi(u,v)=v$.

[T4.19] Nota 19 (Tema 4) — Motivació del redreçament de la imatge
Explicació 19. Motivació i interpretació del teorema de redreçament de la imatge.

El teorema de redreçament de la imatge és una mena de dual del teorema de redreçament del domini, però en lloc de considerar les funcions més senzilles de $\mathbb{R}^{n+m}$ a $\mathbb{R}^m$ (les projeccions), ara tindrem en compte les funcions més senzilles de $\mathbb{R}^m$ a $\mathbb{R}^{n+m}$, és a dir, les inclusions:
$$h(y)=(\mathbf{0},y),\ y\in\mathbb{R}^m,\ \mathbf{0}\in\mathbb{R}^n,$$
o altres reordenacions de les variables, però sempre de manera que $n$ valors de la imatge siguin idènticament 0 per a tota $y$ del domini.

Si amb el teorema de redreçament del domini hem vist que, sota la condició de rang màxim de $\Phi$, podem pensar aquesta funció com una projecció via un canvi de variable $g$, ara veurem que sota condicions similars, podem trobar una funció $h$ tal que
$$D(h\circ\Phi)=Dh\,D\Phi=\begin{pmatrix}0&\ldots&\ldots&0\\ \vdots&\vdots&\vdots&\vdots\\ 0&\ldots&\ldots&0\\ \hline 1&0&\ldots&0\\ 0&1&\ddots&\vdots\\ \vdots&\ddots&\ddots&0\\ 0&\ldots&0&1\end{pmatrix}=\begin{pmatrix}0_{n\times m}\\ \hline Id_m\end{pmatrix}.$$
Com que $h$ és invertible, de manera similar al teorema del redreçament del domini, ja veiem que una condició necessària serà que $\mathrm{rang}\big(D\Phi\big)=m$ allà on ho vulguem aplicar.

[Figura: tres panells: un domini pla $G\subset\mathbb{R}^m$ (disc lila); una fletxa $\Phi$ cap a una superfície corba a $\mathbb{R}^{n+m}$; una fletxa $h$ cap a un disc pla a $\mathbb{R}^m$ dins l'espai.]
Idea gràfica del teorema de redreçament de la imatge. Per entendre la imatge en tres dimensions, pensem que $m=2$ i $n=1$. El domini pla ($m=2$) inicial es converteix en una superfície $S$ a $\mathbb{R}^{1+2}$ (interpertem $\Phi$ com la parametrització d'una superfície); finalment, projectant sobre $\mathbb{R}^2$, la superfícies $S$ es converteix en un domini del tipus $(y,\mathbf{0})$, amb $y\in\mathbb{R}^m$ i $\mathbf{0}\in\mathbb{R}^n$ (és a dir, si $n=1$ i $m=2$, un domini en el pla $z=0$).

[T4.20] Teorema 20 (Tema 4) — Teorema de redreçament de la imatge
(de redreçament de la imatge). Sigui $G\subset\mathbb{R}^m$ obert, $\Phi:G\subset\mathbb{R}^m\to\mathbb{R}^{n+m}$ una funció $\mathcal{C}^r(G)$, i $b\in G$ tal que $\mathrm{rang}\big(D\Phi(b)\big)=m$. Llavors, existeixen oberts $U,V\subset\mathbb{R}^{n+m}$, amb $\Phi(b)\in V$, un $\mathcal{C}^r$-difeomorfisme $h:V\to U$, i un obert $U'\subset G\subseteq\mathbb{R}^m$ amb $b\in U'$, tals que $h\circ\Phi:U'\to V\to\mathbb{R}^{n+m}$ és $y\mapsto(0,y)$.

[T4.x4] Apunts del Tema 4, §4.3 — Fusió dels dos teoremes de redreçament
Finalment, podem fusionar els dos teoremes de redreçament i afirmar que si tenim una funció $\Phi:G\subset\mathbb{R}^N\to\mathbb{R}^P$, de manera, que $\mathrm{rang}\big(D\Phi(a)\big)=m$, on $m$ és menor o igual que $N$ i que $P$, aleshores, podem redreçar $N-m$ coordenades del domini i $P-m$ coordenades de la imatge, i aconseguir dos difeomorfismes ($g$ de $\mathbb{R}^N$ i $h$ de $\mathbb{R}^P$) tals que
$$h\circ\Phi\circ g(x_1,\ldots,x_N)=(x_1,\ldots,x_m,0,\overset{(P-m)}{\ldots},0).$$

Ho enunciem formalment:

[T4.21] Teorema 21 (Tema 4) — Teorema del rang
(del rang). Siguin $G\subset\mathbb{R}^n$ obert, $\Phi:G\subset\mathbb{R}^N\to\mathbb{R}^P$ una funció $\mathcal{C}^r(G)$ i $a\in G$ tals que $\mathrm{rang}\big(D\Phi(a)\big)=m\leqslant N,P$. Llavors, existeixen dos oberts $U_1,V_1\subseteq\mathbb{R}^N$ amb $a\in U_1$, dos oberts $U_2,V_2\subseteq\mathbb{R}^P$ amb $\Phi(a)\in V_2$, i dos $\mathcal{C}^r$-difeomorfismes $g:V_1\to U_1$ i $h:V_2\to U_2$, tals que $(h\circ\Phi\circ g)(x_1,\ldots,x_N)=(x_1,\ldots,x_m,0,\ldots,0)$.

[T4.x5] Apunts del Tema 4, §4.3 — Teorema del rang des dels redreçaments
El teorema del rang es pot demostrar a partir dels dos teoremes de redreçament, prenent $n+m=N$ en el teorema 18 i $n+m=P$ en el teorema 20. La funció $\Phi$ del teorema 21, de fet, és la composició $\Phi=\Phi_I\circ\Phi_D$, si denotem per $\Phi_D$ i $\Phi_I$ les funcions $\Phi$ emprades als teoremes de redreçament del domini i de la imatge, respectivament.
</apunts>

## Request

Cobreix el Tema 4 de manera variada.
Dificultat normal: cal pensar el paper de cada hipòtesi; contraexemples coneguts però no immediats.

Escriu EXACTAMENT 11 afirmacions noves, de les quals entre 5 i 7 falses.

## Output

A JSON file: {"font": "tema-4", "dificultat": "normal", "autor": "<your model>", "afirmacions": [...]}, each statement following this schema:

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
                "T4.21"
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

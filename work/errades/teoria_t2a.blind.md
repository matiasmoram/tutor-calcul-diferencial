## T2.7:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T2.7] Proposició 7 (Tema 2) — Equivalència de les definicions de límit
Les condicions (a), (b) i (c) de la definició 6 són equivalents.
Demostració: - (a) $\Rightarrow$ (b). Prenem $\mathcal{V}\in\mathcal{E}_{\mathbf{b}}$. Aleshores, existeix $\epsilon>0$ tal que $B(b,\epsilon)\subseteq\mathcal{V}$.
  Per (a), existeix $\delta>0$ tal que $\forall x\in\Omega$ amb $0<d(x,x_0)<\delta$, es té que $d(f(x),b)<\epsilon$.
  Prenent $\mathcal{U}=B(x_0,\delta)\in\mathcal{E}_{\mathbf{x_0}}$, es dedueix que $f\left((\mathcal{U}\setminus\{x_0\})\cap\Omega\right)\subseteq\mathcal{V}$.

- (b) $\Rightarrow$ (c). Prenem una successió $(x_n)_{n\in\mathbb{N}}$ amb $x_0\neq x_n\in\Omega$ i $\displaystyle\lim_{n\to+\infty}x_n=x_0$.
  Per tant, sabem que donat $\delta>0$, existeix $n_0$ tal que $d(x_n,x_0)<\delta$ si $n\geq n_0$.
  Considerem ara un valor $\epsilon>0$ qualsevol i prenem $\mathcal{V}=B(b,\epsilon)$. Per (b), sabem que existeix un obert $\mathcal{U}$ tal que $f\left((\mathcal{U}\setminus\{x_0\})\cap\Omega\right)\subseteq\mathcal{V}$.
  Per tant, $\exists\,\delta>0$ tal que $B(x_0,\delta)\subseteq\mathcal{U}$ i, en conseqüència, existeix $n_0$ tal que $d(x_n,x_0)<\delta$ si $n\geq n_0$ i $f(x_n)\in\mathcal{V}$ (és a dir, que $d(f(x_n),b)<\epsilon$).

- (c) $\Rightarrow$ (a).
  Donat $\epsilon\geq0$, volem trobar $\delta>0$, tal que si $0<d(x,x_0)<\delta$, aleshores $d(f(x),b)<\epsilon$.
  Observem que és una mica més complicat perquè hem d'extrapolar a tot un entorn allò que li passa a una successió.
  Ho farem per reducció a l'absurd.
  Suposem que existeix un $\epsilon>0$ tal que per a qualsevol $\delta>0$ existeix $x\in\Omega$ tal que $0<d(x,x_0)<\delta$ i $d(f(x),b)\geq\epsilon$.
  Prenem ara $\delta=1/n$. Llavors, per a cada $n$, podem escollir $x_n\in\Omega$ tal que $0<d(x_n,x_0)<\delta$ i $\displaystyle\lim_{n\to+\infty}x_n=x_0$ i $d(f(x_n),b)\geq\epsilon$.
  Però això no pot ser cert perquè caldria que $\displaystyle\lim_{n\to+\infty}f(x_n)=b$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $f:\Omega\subseteq M\longrightarrow N$, $x_0\in\Omega'$ i $b\in N$. Les condicions següents són equivalents: (a) $\forall\epsilon>0,\exists\delta>0$ tal que $\forall x\in\Omega$ amb $0<d(x,x_0)<\delta$, es té que $d'(f(x),b)<\epsilon$; (b) per a tot obert $\mathcal{V}$ que conté $b$, existeix un obert $\mathcal{U}$ que conté $x_0$ tal que $f\left((\mathcal{U}\setminus\{x_0\})\cap\Omega\right)\subseteq\mathcal{V}$;
[2] (enunciat) (c) per a tota successió $(x_n)_{n\in\mathbb{N}}\subseteq\Omega$ amb $\lim_{n\to+\infty}x_n=x_0$, es té que $\lim_{n\to+\infty}f(x_n)=b$.
[3] (demostració) (a) $\Rightarrow$ (b). Sigui $\mathcal{V}$ un obert que conté $b$. Aleshores existeix $\epsilon>0$ tal que $B(b,\epsilon)\subseteq\mathcal{V}$ i, per (a), existeix $\delta>0$ tal que $\forall x\in\Omega$ amb $0<d(x,x_0)<\delta$ es té $d'(f(x),b)<\epsilon$.
[4] (demostració) Prenent $\mathcal{U}=B(x_0,\delta)$, que és un obert que conté $x_0$, es dedueix que $f\left((\mathcal{U}\setminus\{x_0\})\cap\Omega\right)\subseteq B(b,\epsilon)\subseteq\mathcal{V}$.
[5] (demostració) (b) $\Rightarrow$ (c). Prenem una successió $(x_n)_{n\in\mathbb{N}}$ amb $x_0\neq x_n\in\Omega$ i $\lim_{n\to+\infty}x_n=x_0$, i un $\epsilon>0$ qualsevol. Per (b) aplicat a $\mathcal{V}=B(b,\epsilon)$, existeix un obert $\mathcal{U}$ que conté $x_0$ tal que $f\left((\mathcal{U}\setminus\{x_0\})\cap\Omega\right)\subseteq\mathcal{V}$.
[6] (demostració) Com que $\mathcal{U}$ és obert, existeix $\delta>0$ tal que $B(x_0,\delta)\subseteq\mathcal{U}$, i com que $x_n\to x_0$, existeix $n_0$ tal que $d(x_n,x_0)<\delta$ si $n\geq n_0$. Així, per a $n\geq n_0$, $x_n\in(\mathcal{U}\setminus\{x_0\})\cap\Omega$ i, per tant, $d'(f(x_n),b)<\epsilon$.
[7] (demostració) (c) $\Rightarrow$ (a). Ho farem per reducció a l'absurd: suposem que (a) no es compleix, és a dir, que existeixen $\epsilon>0$ i $\delta>0$ tals que hi ha algun $x\in\Omega$ amb $0<d(x,x_0)<\delta$ i $d'(f(x),b)\geq\epsilon$. Prenent $\delta=1/n$, per a cada $n$ podem escollir $x_n\in\Omega$ amb $0<d(x_n,x_0)<1/n$ i $d'(f(x_n),b)\geq\epsilon$.
[8] (demostració) Aleshores $x_n\neq x_0$ i $\lim_{n\to+\infty}x_n=x_0$, de manera que, per (c), caldria que $\lim_{n\to+\infty}f(x_n)=b$, cosa incompatible amb $d'(f(x_n),b)\geq\epsilon$ per a tota $n$. Aquesta contradicció demostra (a).


## T2.8:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T2.8] Proposició 8 (Tema 2) — Unicitat del límit
Unicitat del límit. Si existeix $\displaystyle\lim_{x\to x_0}f(x)$, aquest és únic.
Demostració: Suposem que $\displaystyle\lim_{x\to x_0}f(x)=b$ i que $\displaystyle\lim_{x\to x_0}f(x)=c$, amb $b\neq c$.
Sigui $\epsilon=d(b,c)/2$.
Prenem una successió $(x_n)_{n\in\mathbb{N}}$ tal que $x_n\to x_0$ i $x_n\neq x_0$. Aleshores, per l'apartat (c) de la proposició 7, donat $\epsilon>0$, existeix $n_0$ tal que la $d(f(x_n),b)<\epsilon$ per a tota $n\geq n_0$; anàlogament, existeix $n_0'$ tal que la $d(f(x_n),c)<\epsilon$ per a tota $n\geq n_0'$.
Per tant, per a tota $n\geq\max(n_0,n_0')$ i aplicant la desigualtat triangular, tenim que
$$d(b,c)\leq d(b,f(x_n))+d(f(x_n),c)<2\,\epsilon=d(b,c).$$
Arribem, doncs, a contradicció.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $f:\Omega\subseteq M\longrightarrow N$ i $x_0\in\overline{\Omega}$. Si existeix $\lim_{x\to x_0}f(x)$, aquest és únic.
[2] (demostració) Suposem que $\lim_{x\to x_0}f(x)=b$ i que $\lim_{x\to x_0}f(x)=c$, amb $b\neq c$, i sigui $\epsilon=d'(b,c)/2>0$.
[3] (demostració) Prenem una successió $(x_n)_{n\in\mathbb{N}}\subseteq\Omega$ tal que $x_n\to x_0$ i $x_n\neq x_0$ per a tota $n$.
[4] (demostració) Per l'apartat (c) de la proposició 7, existeix $n_0$ tal que $d'(f(x_n),b)<\epsilon$ per a tota $n\geq n_0$; anàlogament, existeix $n_0'$ tal que $d'(f(x_n),c)<\epsilon$ per a tota $n\geq n_0'$.
[5] (demostració) Per tant, per a tota $n\geq\min(n_0,n_0')$, aplicant la desigualtat triangular, tenim $d'(b,c)\leq d'(b,f(x_n))+d'(f(x_n),c)<2\epsilon=d'(b,c)$.
[6] (demostració) Arribem, doncs, a una contradicció, i per tant $b=c$.


## T2.10:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T2.10] Proposició 10 (Tema 2) — Límit per camins
Límit per camins. Si $F:D\subseteq\mathbb{R}^2\longrightarrow\mathbb{R}^m$ i $(a,b)\in D'$ tal que $\displaystyle\exists\lim_{(x,y)\to(a,b)}F(x,y)=L$, llavors per a tota funció real i contínua $g$ definida en un entorn d'$a$, tal que $g(a)=b$, es compleix que
$$\lim_{x\to a}F(x,g(x))=L.$$
Demostració: Per una banda, com que $\displaystyle\lim_{(x,y)\to(a,b)}F(x,y)=L$, sabem que
$$\forall\epsilon>0,\exists\,\delta_1=\delta_1(\epsilon)\text{ tal que si }0<\|(x,y)-(a,b)\|<\delta_1(\epsilon),\text{ aleshores }\|F(x,y)-L\|<\epsilon.\qquad(1)$$
Per altra banda, com que $\displaystyle\lim_{x\to a}g(x)=b$, sabem que
$$\forall\epsilon>0,\exists\,\delta_2=\delta_2(\epsilon)\text{ tal que si }0<|x-a|<\delta_2(\epsilon),\text{ aleshores }\|g(x)-b\|<\epsilon.\qquad(2)$$
Volem veure que donat $\epsilon>0$, $\exists\delta>0$ tal que si $0<|x-a|<\delta$, aleshores $\|F(x,g(x))-L\|<\epsilon$.

[Figura: gràfica de $y=g(x)$ passant pel punt $(a,g(a))=(a,b)$, amb un entorn de radi $\delta_1$ al voltant d'aquest punt i un interval de radi $\delta_2$ al voltant d'$a$ a l'eix horitzontal.]

Per poder jugar amb (1) i (2), donat $\epsilon>0$, definim
$$\delta=\min\left\{\frac{\delta_1(\epsilon)}{\sqrt{2}},\ \delta_2\!\left(\frac{\delta_1(\epsilon)}{\sqrt{2}}\right)\right\}.$$
D'aquesta manera, observem que si a la propietat (2) substituïm $\epsilon$ per $\delta_1(\epsilon)/\sqrt{2}$, tenim que si $0<|x-a|<\delta_2(\delta_1(\epsilon)/\sqrt{2})$, aleshores
$$|g(x)-b|<\delta_1(\epsilon)/\sqrt{2};$$
mentre que si $0<|x-a|<\delta$, és clar que
$$0<|x-a|<\delta_1(\epsilon)/\sqrt{2}.$$
Amb aquestes dues fites, tenim que
$$\|(x,g(x))-(a,b)\|=\sqrt{(x-a)^2+(g(x)-b)^2}<\sqrt{\left(\frac{\delta_1(\epsilon)}{\sqrt{2}}\right)^2+\left(\frac{\delta_1(\epsilon)}{\sqrt{2}}\right)^2}=\delta_1(\epsilon).$$
Llavors, substituint $y$ per $g(x)$ a (1), deduïm que $\|F(x,g(x))-L\|<\epsilon$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Siguin $F:D\subseteq\mathbb{R}^2\longrightarrow\mathbb{R}^m$ i $(a,b)\in D'$. Aleshores, $\lim_{(x,y)\to(a,b)}F(x,y)=L$ si i només si, per a tota funció real i contínua $g$ definida en un entorn d'$a$ tal que $g(a)=b$, es compleix que $\lim_{x\to a}F(x,g(x))=L$.
[2] (demostració) Com que $\lim_{(x,y)\to(a,b)}F(x,y)=L$, per a tot $\epsilon>0$ existeix $\delta_1=\delta_1(\epsilon)>0$ tal que si $0<\|(x,y)-(a,b)\|<\delta_1(\epsilon)$, aleshores $\|F(x,y)-L\|<\epsilon$. (1)
[3] (demostració) Com que $g$ és contínua en $a$ i $g(a)=b$, tenim $\lim_{x\to a}g(x)=b$: per a tot $\epsilon>0$ existeix $\delta_2=\delta_2(\epsilon)>0$ tal que si $0<|x-a|<\delta_2(\epsilon)$, aleshores $|g(x)-b|<\epsilon$. (2)
[4] (demostració) Volem veure que, donat $\epsilon>0$, existeix $\delta>0$ tal que si $0<|x-a|<\delta$, aleshores $\|F(x,g(x))-L\|<\epsilon$.
[5] (demostració) Donat $\epsilon>0$, definim $\delta=\min\left\{\delta_1(\epsilon),\ \delta_2\!\left(\delta_1(\epsilon)/\sqrt{2}\right)\right\}$. Així, si $0<|x-a|<\delta$, és clar que $|x-a|<\delta_1(\epsilon)/\sqrt{2}$ i, aplicant (2) amb $\delta_1(\epsilon)/\sqrt{2}$ en lloc d'$\epsilon$, també $|g(x)-b|<\delta_1(\epsilon)/\sqrt{2}$.
[6] (demostració) Amb aquestes dues fites, $\|(x,g(x))-(a,b)\|=\sqrt{(x-a)^2+(g(x)-b)^2}<\sqrt{\left(\frac{\delta_1(\epsilon)}{\sqrt{2}}\right)^2+\left(\frac{\delta_1(\epsilon)}{\sqrt{2}}\right)^2}=\delta_1(\epsilon)$, i aquesta distància és positiva perquè $x\neq a$.
[7] (demostració) Llavors, substituint $y$ per $g(x)$ a (1), deduïm que $\|F(x,g(x))-L\|<\epsilon$.


## T2.12:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T2.12] Proposició 12 (Tema 2) — Límits iterats
Límits iterats. Sigui $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}^m$ i $(a,b)\in\Omega$ t.q. $(a-\eta,a+\eta)\times(b-\eta,b+\eta)\subseteq\Omega$ per a $\eta>0$. Suposem que $\lim_{(x,y)\to(a,b)}f(x,y)=L$ i $\forall x\in(a-\eta,a+\eta)\ \exists\lim_{y\to b}f(x,y)$, i $\forall y\in(b-\eta,b+\eta)\ \exists\lim_{x\to a}f(x,y)$. Llavors,
$$\lim_{x\to a}\lim_{y\to b}f(x,y)=L=\lim_{y\to b}\lim_{x\to a}f(x,y).$$
Demostració: Farem la demostració només per un dels límits iterats. A més, i sense pèrdua de generalitat, ho demostrarem només per a $m=1$.
L'existència del límit $\displaystyle\lim_{(x,y)\to(a,b)}f(x,y)=L$ implica que per a qualsevol $\epsilon>0$, existeix $\delta_1=\delta_1(\epsilon)>0$ tal que si $\|(x,y)-(a,b)\|<\delta_1$, aleshores $|f(x,y)-L|<\epsilon$.

D'altra banda, per a $x\in(a-\eta,a+\eta)$ qualsevol, donat $\epsilon>0$, existeix $\delta_2=\delta_2(\epsilon,x)>0$ tal que si $|y-b|<\delta_2$, aleshores $|f(x,y)-g(x)|<\epsilon$, on $g(x):=\lim_{y\to b}f(x,y)$.

Volem veure $\lim_{x\to a}g(x)=L$, és a dir, que donat $\epsilon>0$, existeix $\delta>0$ tal que si $|x-a|<\delta$, aleshores $|g(x)-L|<\epsilon$.

Com hem de prendre $\delta$?

- Observem primer que si $|f(x,y)-L|<\epsilon/2$ i $|g(x)-f(x,y)|<\epsilon/2$, llavors
$$|g(x)-L|\leq|g(x)-f(x,y)|+|f(x,y)-L|<\epsilon\qquad\text{(el nostre objectiu!).}$$
- Aconseguirem aquest desigualtat si suposem
$$\|(x,y)-(a,b)\|<\delta_1(\epsilon/2),\qquad\qquad|y-b|<\delta_2(\epsilon/2,x).$$
- Podem aconseguir que
$$\|(x,y)-(a,b)\|=\sqrt{(x-a)^2+(y-b)^2}<\delta_1(\epsilon/2),$$
considerant

(1) $\delta=\dfrac{\delta_1(\epsilon/2)}{\sqrt{2}}$, ja que tindrem $|x-a|<\delta=\dfrac{\delta_1(\epsilon/2)}{\sqrt{2}}$, i, a més,

(2) $|y-b|<\min\left\{\delta_2(\epsilon/2,x),\dfrac{\delta_1(\epsilon/2)}{\sqrt{2}}\right\}.$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}^m$ i $(a,b)\in\Omega$ tal que $(a-\eta,a+\eta)\times(b-\eta,b+\eta)\subseteq\Omega$ per a cert $\eta>0$. Suposem que $\lim_{(x,y)\to(a,b)}f(x,y)=L$, que $\forall x\in(a-\eta,a+\eta)$ existeix $\lim_{y\to b}f(x,y)$ i que $\forall y\in(b-\eta,b+\eta)$ existeix $\lim_{x\to a}f(x,y)$.
[2] (enunciat) Llavors, $\lim_{x\to a}\lim_{y\to b}f(x,y)=L=\lim_{y\to b}\lim_{x\to a}f(x,y)$ i, a més, $\lim_{y\to b}f(x,y)=L$ per a tot $x\in(a-\eta,a+\eta)$.
[3] (demostració) Farem la demostració només per a un dels límits iterats i, sense pèrdua de generalitat, per a $m=1$. Per l'existència del límit doble, per a tot $\epsilon>0$ existeix $\delta_1=\delta_1(\epsilon)>0$ tal que si $0<\|(x,y)-(a,b)\|<\delta_1$, aleshores $|f(x,y)-L|<\epsilon$. (1)
[4] (demostració) D'altra banda, per a cada $x\in(a-\eta,a+\eta)$ sigui $g(x):=\lim_{y\to b}f(x,y)$; com que aquests límits existeixen per a tot $x$, donat $\epsilon>0$ existeix $\delta_2=\delta_2(\epsilon)>0$, el mateix per a tots els $x$, tal que si $0<|y-b|<\delta_2$, aleshores $|f(x,y)-g(x)|<\epsilon$. (2)
[5] (demostració) Volem veure que $\lim_{x\to a}g(x)=L$, és a dir, que donat $\epsilon>0$ existeix $\delta>0$ tal que si $0<|x-a|<\delta$, aleshores $|g(x)-L|<\epsilon$.
[6] (demostració) Observem que si per a algun $y$ es té $|f(x,y)-L|<\epsilon/2$ i $|g(x)-f(x,y)|<\epsilon/2$, llavors $|g(x)-L|\leq|g(x)-f(x,y)|+|f(x,y)-L|<\epsilon$.
[7] (demostració) Prenem $\delta=\min\{\delta_1(\epsilon/2)/\sqrt{2},\,\eta\}$. Donat $x$ amb $0<|x-a|<\delta$, escollim $y\neq b$ amb $|y-b|<\min\left\{\delta_2(\epsilon/2,x),\ \delta_1(\epsilon/2)/\sqrt{2}\right\}$, on $\delta_2(\epsilon/2,x)$ és el radi que dona la definició de $g(x)$ per a aquest $x$.
[8] (demostració) Aleshores $0<\|(x,y)-(a,b)\|=\sqrt{(x-a)^2+(y-b)^2}<\delta_1(\epsilon/2)$ i, per (1) i la tria de $y$, $|f(x,y)-L|<\epsilon/2$ i $|f(x,y)-g(x)|<\epsilon/2$. Per l'observació anterior, $|g(x)-L|<\epsilon$.


## T2.17:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T2.17] Teorema 17 (Tema 2) — Caracteritzacions de la continuïtat
Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents:

(a) $f$ és contínua en $\Omega$;

(b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;

(c) per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$;

(d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.
Demostració: Ens recorda les diferents alternatives de la definició 6 i la proposició 7.

- (a)$\Rightarrow$(b). Volem veure que si és $f$ contínua en $\Omega$, aleshores per a tota successió convergent $(x_n)_n\in\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$.

  Prenem $(x_n)_n\in\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$. Com que $f$ és contínua en $x_0$, podem tenir dues situacions:

  - $x_0\notin\Omega'$, és a dir, $x_0$ és aïllat, i per tant, per força, $x_n=x_0$ per a tota $n$.
  - $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Llavors, $\forall\epsilon>0,\exists\delta_1=\delta_1(\epsilon)$ tal que $d(x,x_0)<\delta_1$ implica que $d(f(x),f(x_0))<\epsilon$.
    Ara bé: com que $\lim_{n\to\infty}x_n=x_0$, llavors $\forall\delta>0,\exists n_0=n_0(\delta)$ tal que $d(x_n,x_0)<\delta$ per a $n\geq n_0$.
    Agrupant les dues afirmacions anteriors, concloem que $\forall\epsilon>0,\exists n_0=n_0(\delta_1(\epsilon))$ tal que $d(f(x_n),f(x_0))<\epsilon$.

- (b)$\Rightarrow$(d). Volem veure que si per a tota successió convergent $(x_n)_n\in\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$, aleshores per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.

  Considerem $f:\Omega\subseteq M\longrightarrow N$ i $E\subseteq N$ tancat (en particular, $\overline{E}=E$). Demostrarem la igualtat
  $$f^{-1}(E)=\{x\in\Omega:f(x)\in E\}=\overline{f^{-1}(E)}\cap\Omega\qquad(\text{prenem }D=\overline{f^{-1}(E)}).$$

  - D'una banda, és evident que $f^{-1}(E)\subseteq\overline{f^{-1}(E)}\cap\Omega$ ja que si $x\in f^{-1}(E)$, aleshores segur que $x\in\Omega$ i $x\in\overline{f^{-1}(E)}$ ja que $f^{-1}(E)\subseteq\overline{f^{-1}(E)}$.
  - Per a la inclusió inversa, prenem $x_0\in\overline{f^{-1}(E)}\cap\Omega$. Pel fet que $x_0\in\overline{f^{-1}(E)}$, sabem que (vegeu proposició 19 del tema 1) $\exists(x_n)_n\in f^{-1}(E)\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0$. Usant la hipòtesi, doncs, $\lim_{n\to\infty}f(x_n)=f(x_0)$. Com que $x_n\in f^{-1}(E)$, aleshores $f(x_n)\in E$ i, en conseqüència, tenim que $f(x_0)\in\overline{E}=E$ (per ser tancat). Per tant, $x_0\in f^{-1}(E)$.

- (d)$\Rightarrow$(c). Volem veure que si per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$, aleshores per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$.

  Prenem un obert $V\subseteq N$. Per definició $V^c\subseteq N$ és tancat i, per la hipòtesi, $\exists D\subseteq M$ tancat tal que $f^{-1}(V^c)=D\cap\Omega$, on $f^{-1}(V^c)=\{x\in\Omega:f(x)\in V^c\}=\Omega\setminus\{x\in\Omega:f(x)\in V\}$. Per tant, $\Omega\setminus f^{-1}(V)=D\cap\Omega$, fet que implica que $f^{-1}(V)=\Omega\setminus(D\cap\Omega)=D^c\cap\Omega$, on $D^c$ és un obert de $M$.

- (c)$\Rightarrow$(a). Volem veure que si per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$, aleshores $f$ és contínua en $\Omega$.

  Si $x_0\notin\Omega'$, no cal demostrar res. Per tant, suposem que $x_0\in\Omega'$ i, donat $\epsilon>0$, prenem $V:=B(f(x_0),\epsilon)\subseteq N$. Per hipòtesi, tenim que existeix $U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$. Per tant, existeix $\delta>0$ tal que $B(x_0,\delta)\subseteq U$.
  Prenem ara $x\in\Omega$ tal que $d(x,x_0)<\delta$. Aleshores, $x\in U\cap\Omega=f^{-1}(V)$ i, per tant, $f(x)\in V$, que equival a dir que $d(f(x),f(x_0))<\epsilon$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents: (a) $f$ és uniformement contínua en $\Omega$; (b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;
[2] (enunciat) (c) per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$; (d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.
[3] (demostració) (a)$\Rightarrow$(b). Sigui $(x_n)_n\subseteq\Omega$ amb $\lim_{n\to\infty}x_n=x_0\in\Omega$. Com que $f$ és contínua en $x_0$, hi ha dues possibilitats. Si $x_0\notin\Omega'$, $x_0$ és aïllat i, com que $x_n\to x_0$, per força $x_n=x_0$ a partir d'un cert terme, de manera que $f(x_n)=f(x_0)$ a partir d'aquest terme.
[4] (demostració) Altrament, existeix $\lim_{x\to x_0}f(x)=f(x_0)$: donat $\epsilon>0$, existeix $\delta_1=\delta_1(\epsilon)>0$ tal que si $x\in\Omega$ i $d(x,x_0)<\delta_1$, aleshores $d'(f(x),f(x_0))<\epsilon$. Com que $x_n\to x_0$, existeix $n_0=n_0(\delta_1)$ tal que $d(x_n,x_0)<\delta_1$ per a $n\geq n_0$ i, per tant, $d'(f(x_n),f(x_0))<\epsilon$ per a $n\geq n_0$.
[5] (demostració) (b)$\Rightarrow$(d). Sigui $E\subseteq N$ tancat. Prenem $D=\overline{f^{-1}(E)}$, que és tancat, i demostrem que $f^{-1}(E)=D\cap\Omega$. La inclusió $f^{-1}(E)\subseteq\overline{f^{-1}(E)}\cap\Omega$ és evident, ja que $f^{-1}(E)\subseteq\Omega$ i tot conjunt està contingut en la seva adherència.
[6] (demostració) Per a la inclusió inversa, sigui $x_0\in\overline{f^{-1}(E)}\cap\Omega$. Per la proposició 19 del tema 1, existeix una successió $(x_n)_n\subseteq f^{-1}(E)\subseteq\Omega$ amb $\lim_{n\to\infty}x_n=x_0$ i, per (b), $\lim_{n\to\infty}f(x_n)=f(x_0)$.
[7] (demostració) Com que $f(x_n)\in E$ per a tota $n$ i $f(x_n)\to f(x_0)$, tenim $f(x_0)\in\overline{E}=E$, per ser $E$ tancat. Per tant, $x_0\in f^{-1}(E)$.
[8] (demostració) (d)$\Rightarrow$(c). Sigui $V\subseteq N$ obert. Aleshores $V^c$ és tancat i, per (d), existeix $D\subseteq M$ tancat amb $f^{-1}(V^c)=D\cap\Omega$. Com que $f^{-1}(V^c)=\Omega\setminus f^{-1}(V)$, resulta $f^{-1}(V)=\Omega\setminus(D\cap\Omega)=D^c\cap\Omega$, on $U=D^c$ és un obert de $M$.
[9] (demostració) (c)$\Rightarrow$(a). Sigui $x_0\in\Omega$. Si $x_0\notin\Omega'$, $f$ és contínua en $x_0$ per definició. Altrament, donat $\epsilon>0$, prenem $V=B(f(x_0),\epsilon)$; per (c), existeix $U\subseteq M$ obert amb $f^{-1}(V)=U\cap\Omega$ i, com que $x_0\in f^{-1}(V)\subseteq U$, existeix $\delta>0$ tal que $B(x_0,\delta)\subseteq U$.
[10] (demostració) Si $x\in\Omega$ i $d(x,x_0)<\delta$, aleshores $x\in U\cap\Omega=f^{-1}(V)$, és a dir, $d'(f(x),f(x_0))<\epsilon$. Per tant, $\lim_{x\to x_0}f(x)=f(x_0)$ i $f$ és contínua en $x_0$.


## T2.17:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T2.17] Teorema 17 (Tema 2) — Caracteritzacions de la continuïtat
Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents:

(a) $f$ és contínua en $\Omega$;

(b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;

(c) per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$;

(d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.
Demostració: Ens recorda les diferents alternatives de la definició 6 i la proposició 7.

- (a)$\Rightarrow$(b). Volem veure que si és $f$ contínua en $\Omega$, aleshores per a tota successió convergent $(x_n)_n\in\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$.

  Prenem $(x_n)_n\in\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$. Com que $f$ és contínua en $x_0$, podem tenir dues situacions:

  - $x_0\notin\Omega'$, és a dir, $x_0$ és aïllat, i per tant, per força, $x_n=x_0$ per a tota $n$.
  - $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Llavors, $\forall\epsilon>0,\exists\delta_1=\delta_1(\epsilon)$ tal que $d(x,x_0)<\delta_1$ implica que $d(f(x),f(x_0))<\epsilon$.
    Ara bé: com que $\lim_{n\to\infty}x_n=x_0$, llavors $\forall\delta>0,\exists n_0=n_0(\delta)$ tal que $d(x_n,x_0)<\delta$ per a $n\geq n_0$.
    Agrupant les dues afirmacions anteriors, concloem que $\forall\epsilon>0,\exists n_0=n_0(\delta_1(\epsilon))$ tal que $d(f(x_n),f(x_0))<\epsilon$.

- (b)$\Rightarrow$(d). Volem veure que si per a tota successió convergent $(x_n)_n\in\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$, aleshores per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.

  Considerem $f:\Omega\subseteq M\longrightarrow N$ i $E\subseteq N$ tancat (en particular, $\overline{E}=E$). Demostrarem la igualtat
  $$f^{-1}(E)=\{x\in\Omega:f(x)\in E\}=\overline{f^{-1}(E)}\cap\Omega\qquad(\text{prenem }D=\overline{f^{-1}(E)}).$$

  - D'una banda, és evident que $f^{-1}(E)\subseteq\overline{f^{-1}(E)}\cap\Omega$ ja que si $x\in f^{-1}(E)$, aleshores segur que $x\in\Omega$ i $x\in\overline{f^{-1}(E)}$ ja que $f^{-1}(E)\subseteq\overline{f^{-1}(E)}$.
  - Per a la inclusió inversa, prenem $x_0\in\overline{f^{-1}(E)}\cap\Omega$. Pel fet que $x_0\in\overline{f^{-1}(E)}$, sabem que (vegeu proposició 19 del tema 1) $\exists(x_n)_n\in f^{-1}(E)\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0$. Usant la hipòtesi, doncs, $\lim_{n\to\infty}f(x_n)=f(x_0)$. Com que $x_n\in f^{-1}(E)$, aleshores $f(x_n)\in E$ i, en conseqüència, tenim que $f(x_0)\in\overline{E}=E$ (per ser tancat). Per tant, $x_0\in f^{-1}(E)$.

- (d)$\Rightarrow$(c). Volem veure que si per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$, aleshores per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$.

  Prenem un obert $V\subseteq N$. Per definició $V^c\subseteq N$ és tancat i, per la hipòtesi, $\exists D\subseteq M$ tancat tal que $f^{-1}(V^c)=D\cap\Omega$, on $f^{-1}(V^c)=\{x\in\Omega:f(x)\in V^c\}=\Omega\setminus\{x\in\Omega:f(x)\in V\}$. Per tant, $\Omega\setminus f^{-1}(V)=D\cap\Omega$, fet que implica que $f^{-1}(V)=\Omega\setminus(D\cap\Omega)=D^c\cap\Omega$, on $D^c$ és un obert de $M$.

- (c)$\Rightarrow$(a). Volem veure que si per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$, aleshores $f$ és contínua en $\Omega$.

  Si $x_0\notin\Omega'$, no cal demostrar res. Per tant, suposem que $x_0\in\Omega'$ i, donat $\epsilon>0$, prenem $V:=B(f(x_0),\epsilon)\subseteq N$. Per hipòtesi, tenim que existeix $U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$. Per tant, existeix $\delta>0$ tal que $B(x_0,\delta)\subseteq U$.
  Prenem ara $x\in\Omega$ tal que $d(x,x_0)<\delta$. Aleshores, $x\in U\cap\Omega=f^{-1}(V)$ i, per tant, $f(x)\in V$, que equival a dir que $d(f(x),f(x_0))<\epsilon$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents: (a) $f$ és contínua en $\Omega$; (b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;
[2] (enunciat) (c) per a tot obert $V\subseteq N$, $f^{-1}(V)$ és un obert de $M$; (d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.
[3] (demostració) (a)$\Rightarrow$(b). Sigui $(x_n)_n\subseteq\Omega$ amb $\lim_{n\to\infty}x_n=x_0\in\Omega$. Com que $f$ és contínua en $x_0$, hi ha dues possibilitats. Si $x_0\notin\Omega'$, $x_0$ és aïllat i, com que $x_n\to x_0$, per força $x_n=x_0$ a partir d'un cert terme, de manera que $f(x_n)=f(x_0)$ a partir d'aquest terme.
[4] (demostració) Altrament, existeix $\lim_{x\to x_0}f(x)=f(x_0)$: donat $\epsilon>0$, existeix $\delta_1=\delta_1(\epsilon)>0$ tal que si $x\in\Omega$ i $d(x,x_0)<\delta_1$, aleshores $d'(f(x),f(x_0))<\epsilon$. Com que $x_n\to x_0$, existeix $n_0$ tal que $d(x_n,x_0)<\epsilon$ per a $n\geq n_0$ i, per tant, $d'(f(x_n),f(x_0))<\epsilon$ per a $n\geq n_0$.
[5] (demostració) (b)$\Rightarrow$(d). Sigui $E\subseteq N$ tancat. Prenem $D=\overline{f^{-1}(E)}$, que és tancat, i demostrem que $f^{-1}(E)=D\cap\Omega$. La inclusió $f^{-1}(E)\subseteq\overline{f^{-1}(E)}\cap\Omega$ és evident, ja que $f^{-1}(E)\subseteq\Omega$ i tot conjunt està contingut en la seva adherència.
[6] (demostració) Per a la inclusió inversa, sigui $x_0\in\overline{f^{-1}(E)}\cap\Omega$. Per la proposició 19 del tema 1, existeix una successió $(x_n)_n\subseteq f^{-1}(E)\subseteq\Omega$ amb $\lim_{n\to\infty}x_n=x_0$ i, per (b), $\lim_{n\to\infty}f(x_n)=f(x_0)$.
[7] (demostració) Com que $f(x_n)\in E$ per a tota $n$ i $f(x_n)\to f(x_0)$, tenim $f(x_0)\in\overline{E}=E$, per ser $E$ tancat. Per tant, $x_0\in f^{-1}(E)$.
[8] (demostració) (d)$\Rightarrow$(c). Sigui $V\subseteq N$ obert. Aleshores $V^c$ és tancat i, per (d), existeix $D\subseteq M$ tancat amb $f^{-1}(V^c)=D\cap\Omega$. Com que $f^{-1}(V^c)=\Omega\setminus f^{-1}(V)$, resulta $f^{-1}(V)=\Omega\setminus(D\cap\Omega)=D^c\cap\Omega$, on $U=D^c$ és un obert de $M$.
[9] (demostració) (c)$\Rightarrow$(a). Sigui $x_0\in\Omega$. Si $x_0\notin\Omega'$, $f$ és contínua en $x_0$ per definició. Altrament, donat $\epsilon>0$, prenem $V=B(f(x_0),\epsilon)$; per (c), existeix $U\subseteq M$ obert amb $f^{-1}(V)=U\cap\Omega$ i, com que $x_0\in f^{-1}(V)\subseteq U$, existeix $\delta>0$ tal que $B(x_0,\delta)\subseteq U$.
[10] (demostració) Si $x\in\Omega$ i $d(x,x_0)<\delta$, aleshores $x\in U\cap\Omega=f^{-1}(V)$, és a dir, $d'(f(x),f(x_0))<\epsilon$. Per tant, $\lim_{x\to x_0}f(x)=f(x_0)$ i $f$ és contínua en $x_0$.


## T2.17:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T2.17] Teorema 17 (Tema 2) — Caracteritzacions de la continuïtat
Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents:

(a) $f$ és contínua en $\Omega$;

(b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;

(c) per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$;

(d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.
Demostració: Ens recorda les diferents alternatives de la definició 6 i la proposició 7.

- (a)$\Rightarrow$(b). Volem veure que si és $f$ contínua en $\Omega$, aleshores per a tota successió convergent $(x_n)_n\in\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$.

  Prenem $(x_n)_n\in\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$. Com que $f$ és contínua en $x_0$, podem tenir dues situacions:

  - $x_0\notin\Omega'$, és a dir, $x_0$ és aïllat, i per tant, per força, $x_n=x_0$ per a tota $n$.
  - $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Llavors, $\forall\epsilon>0,\exists\delta_1=\delta_1(\epsilon)$ tal que $d(x,x_0)<\delta_1$ implica que $d(f(x),f(x_0))<\epsilon$.
    Ara bé: com que $\lim_{n\to\infty}x_n=x_0$, llavors $\forall\delta>0,\exists n_0=n_0(\delta)$ tal que $d(x_n,x_0)<\delta$ per a $n\geq n_0$.
    Agrupant les dues afirmacions anteriors, concloem que $\forall\epsilon>0,\exists n_0=n_0(\delta_1(\epsilon))$ tal que $d(f(x_n),f(x_0))<\epsilon$.

- (b)$\Rightarrow$(d). Volem veure que si per a tota successió convergent $(x_n)_n\in\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$, aleshores per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$.

  Considerem $f:\Omega\subseteq M\longrightarrow N$ i $E\subseteq N$ tancat (en particular, $\overline{E}=E$). Demostrarem la igualtat
  $$f^{-1}(E)=\{x\in\Omega:f(x)\in E\}=\overline{f^{-1}(E)}\cap\Omega\qquad(\text{prenem }D=\overline{f^{-1}(E)}).$$

  - D'una banda, és evident que $f^{-1}(E)\subseteq\overline{f^{-1}(E)}\cap\Omega$ ja que si $x\in f^{-1}(E)$, aleshores segur que $x\in\Omega$ i $x\in\overline{f^{-1}(E)}$ ja que $f^{-1}(E)\subseteq\overline{f^{-1}(E)}$.
  - Per a la inclusió inversa, prenem $x_0\in\overline{f^{-1}(E)}\cap\Omega$. Pel fet que $x_0\in\overline{f^{-1}(E)}$, sabem que (vegeu proposició 19 del tema 1) $\exists(x_n)_n\in f^{-1}(E)\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0$. Usant la hipòtesi, doncs, $\lim_{n\to\infty}f(x_n)=f(x_0)$. Com que $x_n\in f^{-1}(E)$, aleshores $f(x_n)\in E$ i, en conseqüència, tenim que $f(x_0)\in\overline{E}=E$ (per ser tancat). Per tant, $x_0\in f^{-1}(E)$.

- (d)$\Rightarrow$(c). Volem veure que si per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)=D\cap\Omega$, aleshores per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$.

  Prenem un obert $V\subseteq N$. Per definició $V^c\subseteq N$ és tancat i, per la hipòtesi, $\exists D\subseteq M$ tancat tal que $f^{-1}(V^c)=D\cap\Omega$, on $f^{-1}(V^c)=\{x\in\Omega:f(x)\in V^c\}=\Omega\setminus\{x\in\Omega:f(x)\in V\}$. Per tant, $\Omega\setminus f^{-1}(V)=D\cap\Omega$, fet que implica que $f^{-1}(V)=\Omega\setminus(D\cap\Omega)=D^c\cap\Omega$, on $D^c$ és un obert de $M$.

- (c)$\Rightarrow$(a). Volem veure que si per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$, aleshores $f$ és contínua en $\Omega$.

  Si $x_0\notin\Omega'$, no cal demostrar res. Per tant, suposem que $x_0\in\Omega'$ i, donat $\epsilon>0$, prenem $V:=B(f(x_0),\epsilon)\subseteq N$. Per hipòtesi, tenim que existeix $U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$. Per tant, existeix $\delta>0$ tal que $B(x_0,\delta)\subseteq U$.
  Prenem ara $x\in\Omega$ tal que $d(x,x_0)<\delta$. Aleshores, $x\in U\cap\Omega=f^{-1}(V)$ i, per tant, $f(x)\in V$, que equival a dir que $d(f(x),f(x_0))<\epsilon$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:\Omega\subseteq M\to N$. Aleshores, són equivalents: (a) $f$ és contínua en $\Omega$; (b) per a tota successió convergent $(x_n)_n\subseteq\Omega$ tal que $\lim_{n\to\infty}x_n=x_0\in\Omega$, tenim $\lim_{n\to\infty}f(x_n)=f(x_0)$;
[2] (enunciat) (c) per a tot obert $V\subseteq N$, $\exists U\subseteq M$ obert tal que $f^{-1}(V)=U\cap\Omega$; (d) per a tot tancat $E\subseteq N$, $\exists D\subseteq M$ tancat tal que $f^{-1}(E)\subseteq D\cap\Omega$.
[3] (demostració) (a)$\Rightarrow$(b). Sigui $(x_n)_n\subseteq\Omega$ amb $\lim_{n\to\infty}x_n=x_0\in\Omega$. Com que $f$ és contínua en $x_0$, hi ha dues possibilitats. Si $x_0\notin\Omega'$, $x_0$ és aïllat i, com que $x_n\to x_0$, per força $x_n=x_0$ a partir d'un cert terme, de manera que $f(x_n)=f(x_0)$ a partir d'aquest terme.
[4] (demostració) Altrament, existeix $\lim_{x\to x_0}f(x)=f(x_0)$: donat $\epsilon>0$, existeix $\delta_1=\delta_1(\epsilon)>0$ tal que si $x\in\Omega$ i $d(x,x_0)<\delta_1$, aleshores $d'(f(x),f(x_0))<\epsilon$. Com que $x_n\to x_0$, existeix $n_0=n_0(\delta_1)$ tal que $d(x_n,x_0)<\delta_1$ per a $n\geq n_0$ i, per tant, $d'(f(x_n),f(x_0))<\epsilon$ per a $n\geq n_0$.
[5] (demostració) (b)$\Rightarrow$(d). Sigui $E\subseteq N$ tancat. Prenem $D=\overline{f^{-1}(E)}$, que és tancat, i demostrem que $f^{-1}(E)=D\cap\Omega$. La inclusió $f^{-1}(E)\subseteq\overline{f^{-1}(E)}\cap\Omega$ és evident, ja que $f^{-1}(E)\subseteq\Omega$ i tot conjunt està contingut en la seva adherència.
[6] (demostració) Per a la inclusió inversa, sigui $x_0\in\overline{f^{-1}(E)}\cap\Omega$. Per la proposició 19 del tema 1, existeix una successió $(x_n)_n\subseteq f^{-1}(E)\subseteq\Omega$ amb $\lim_{n\to\infty}x_n=x_0$ i, per (b), $\lim_{n\to\infty}f(x_n)=f(x_0)$.
[7] (demostració) Com que $f(x_n)\in E$ per a tota $n$ i $f(x_n)\to f(x_0)$, $f(x_0)$ és un punt d'acumulació d'$E$ i, com que $E$ és tancat, $f(x_0)\in E$. Per tant, $x_0\in f^{-1}(E)$.
[8] (demostració) (d)$\Rightarrow$(c). Sigui $V\subseteq N$ obert. Aleshores $V^c$ és tancat i, per (d), existeix $D\subseteq M$ tancat amb $f^{-1}(V^c)=D\cap\Omega$. Com que $f^{-1}(V^c)=\Omega\setminus f^{-1}(V)$, resulta $f^{-1}(V)=\Omega\setminus(D\cap\Omega)=D^c\cap\Omega$, on $U=D^c$ és un obert de $M$.
[9] (demostració) (c)$\Rightarrow$(a). Sigui $x_0\in\Omega$. Si $x_0\notin\Omega'$, $f$ és contínua en $x_0$ per definició. Altrament, donat $\epsilon>0$, prenem $V=B(f(x_0),\epsilon)$; per (c), existeix $U\subseteq M$ obert amb $f^{-1}(V)=U\cap\Omega$ i, com que $x_0\in f^{-1}(V)\subseteq U$, existeix $\delta>0$ tal que $B(x_0,\delta)\subseteq U\cap\Omega$.
[10] (demostració) Si $x\in\Omega$ i $d(x,x_0)<\delta$, aleshores $x\in U\cap\Omega=f^{-1}(V)$, és a dir, $d'(f(x),f(x_0))<\epsilon$. Per tant, $\lim_{x\to x_0}f(x)=f(x_0)$ i $f$ és contínua en $x_0$.


## T2.18:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T2.18] Corol·lari 18 (Tema 2) — Conjunts definits per desigualtats
Siguin $f,g:\mathbb{R}^n\longrightarrow\mathbb{R}$, funcions contínues. Llavors:

(i) $A=\{x\in\mathbb{R}^n:f(x)>g(x)\}$ és un conjunt obert.

(ii) $B=\{x\in\mathbb{R}^n:f(x)\geq g(x)\}$ és un conjunt tancat.
Demostració: (i) Considerem la funció $h(x)=f(x)-g(x)$. Per la proposició 20(i) (encara no demostrada), $h$ és contínua per a tot $x\in\mathbb{R}^n$.
Prenem $V=(0,+\infty)$, que és un obert de $\mathbb{R}$. Per la definició de continuïtat, existeix $U\subseteq\mathbb{R}^n$ obert tal que
$$\begin{aligned}h^{-1}(V)&=\{x\in\mathbb{R}^n\mid h(x)\in V\}=\{x\in\mathbb{R}^n\mid h(x)>0\}\\&=\{x\in\mathbb{R}^n\mid f(x)>g(x)\}=U\cap\mathbb{R}^n=U.\end{aligned}$$

(ii) Anàleg a (i) canviant "obert" per "tancat", o bé usant que
$$B=\{x\in\mathbb{R}^n:f(x)\geq g(x)\}=\mathbb{R}^n\setminus\{x\in\mathbb{R}^n:f(x)<g(x)\},$$
és a dir, que $B$ és el complementari d'un obert.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Siguin $f,g:\mathbb{R}^n\longrightarrow\mathbb{R}$ funcions contínues. Llavors: (i) $A=\{x\in\mathbb{R}^n:f(x)>g(x)\}$ és un conjunt obert;
[2] (enunciat) (ii) $B=\{x\in\mathbb{R}^n:f(x)\geq g(x)\}$ és un conjunt tancat, i és l'adherència de $A$.
[3] (demostració) (i) Considerem la funció $h(x)=f(x)-g(x)$. Per la proposició 20(i), $h$ és contínua en tot $\mathbb{R}^n$.
[4] (demostració) Prenem $V=(0,+\infty)$, que és un obert de $\mathbb{R}$. Per la continuïtat de $h$ (teorema 17(c)), existeix $U\subseteq\mathbb{R}^n$ obert tal que $h(U)=V$ i, per tant, $h^{-1}(V)=U$.
[5] (demostració) A més, $h^{-1}(V)=\{x\in\mathbb{R}^n:h(x)>0\}=\{x\in\mathbb{R}^n:f(x)>g(x)\}=A$, de manera que $A=U$ és obert.
[6] (demostració) (ii) Per (i), intercanviant els papers de $f$ i $g$, el conjunt $\{x\in\mathbb{R}^n:f(x)<g(x)\}$ és obert, i $B=\mathbb{R}^n\setminus\{x\in\mathbb{R}^n:f(x)<g(x)\}$. És a dir, $B$ és el complementari d'un obert i, per tant, és tancat.


## T2.20:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T2.20] Proposició 20 (Tema 2) — Àlgebra de funcions contínues
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $h:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, contínues. Llavors

(i) $f+g,\ \lambda f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $\lambda\in\mathbb{R}$, són contínues;

(ii) $hf:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ és contínua;

(iii) per a $m=1$, si $g(x)\neq0\ \forall x\in\Omega$, $f/g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(iv) $\langle f,g\rangle:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(v) $\|f\|:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua.
Demostració: Fent servir el teorema 17(b), l'enunciat (i) es desprèn de les propietats dels límits. D'altra banda, si demostrem (ii), aleshores (iii) és immediata substituint $h=1/g$, mentre que per a demostrar (iv) i (v) n'hi ha prou amb les propietats (i) i (ii) per a veure que els productes escalars són continus, i amb l'observació 19 per a assegurar la continuïtat quan es fa la composició amb l'arrel quadrada.

Per demostrar (ii), sabem que, donat $x_0\in\Omega$, per a qualsevol $\epsilon>0$, existeixen $\delta_1=\delta_1(\epsilon)$ i $\delta_2=\delta_2(\epsilon)$ tals que
$$\begin{aligned}&\forall x\text{ tal que }\|x-x_0\|<\delta_1,\ \|f(x)-f(x_0)\|<\epsilon,\\&\forall x\text{ tal que }\|x-x_0\|<\delta_2,\ |h(x)-h(x_0)|<\epsilon.\end{aligned}\qquad(3)$$
Volem veure que per a qualsevol $\epsilon>0$, existeix $\delta$ tal que si $\|x-x_0\|<\delta$, aleshores $\|h(x)f(x)-h(x_0)f(x_0)\|<\epsilon$.
Per la desigualtat triangular,
$$\begin{aligned}\|h(x)f(x)-h(x_0)f(x_0)\|&\leq\|h(x)f(x)-h(x)f(x_0)\|+\|h(x)f(x_0)-h(x_0)f(x_0)\|\\&=|h(x)|\,\|f(x)-f(x_0)\|+\|f(x_0)\|\,|h(x)-h(x_0)|.\end{aligned}$$
El terme $\|f(x_0)\|$ és fix i, per tant, no ens preocupa. Ara volem fitar $|h(x)|$ per alguna expressió que no depengui de $x$. Per la hipòtesi de continuïtat de $h$, prenent per exemple $\epsilon=1$, sabem que existeix $\delta_2(1)$ tal que si $\|x-x_0\|<\delta_2(1)$, aleshores $|h(x)-h(x_0)|<1$, és a dir, $-1+h(x_0)<h(x)<1+h(x_0)$ i, per tant,
$$|h(x)|<1+|h(x_0)|.$$
Apliquem ara les propietats de (3) per a $\dfrac{\epsilon}{2(1+|h(x_0)|)}$ i per a $\dfrac{\epsilon}{2\,\|f(x_0)\|}$, respectivament. Amb les $\delta_1$ i $\delta_2$ resultants, junt amb $\delta_2(1)$, definim:
$$\delta:=\min\left\{\delta_2(1),\ \delta_1\!\left(\frac{\epsilon}{2(1+|h(x_0)|)}\right),\ \delta_2\!\left(\frac{\epsilon}{2\,\|f(x_0)\|}\right)\right\}.$$
Aleshores, per a $\|x-x_0\|<\delta$, tenim que:
$$\begin{aligned}\|h(x)f(x)-h(x_0)f(x_0)\|&\leq|h(x)|\,\|f(x)-f(x_0)\|+\|f(x_0)\|\,\|h(x)-h(x_0)\|\\&\leq(1+|h(x_0)|)\,\frac{\epsilon}{2(1+|h(x_0)|)}+\|f(x_0)\|\,\frac{\epsilon}{2\,\|f(x_0)\|}=\frac{\epsilon}{2}+\frac{\epsilon}{2}=\epsilon.\end{aligned}$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ contínues i $h:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ fitada. Llavors: (i) $f+g$ i $\lambda f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $\lambda\in\mathbb{R}$, són contínues; (ii) $hf:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ és contínua;
[2] (enunciat) (iii) per a $m=1$, si $g(x)\neq0$ per a tot $x\in\Omega$, $f/g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua; (iv) $\langle f,g\rangle:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua; (v) $\|f\|:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua.
[3] (demostració) Fent servir el teorema 17(b), (i) es desprèn de les propietats dels límits. Si demostrem (ii), (iii) és immediata prenent $h=1/g$; per a (iv) n'hi ha prou amb (i) i (ii), ja que $\langle f,g\rangle=\sum_i f_ig_i$, i per a (v) amb (iv) i l'observació 19 (composició amb l'arrel quadrada), ja que $\|f\|=\sqrt{\langle f,f\rangle}$.
[4] (demostració) Per demostrar (ii), fixem $x_0\in\Omega$. Per la continuïtat de $f$ i de $h$ en $x_0$, per a qualsevol $\epsilon>0$ existeixen $\delta_1=\delta_1(\epsilon)$ i $\delta_2=\delta_2(\epsilon)$ tals que si $\|x-x_0\|<\delta_1$, aleshores $\|f(x)-f(x_0)\|<\epsilon$, i si $\|x-x_0\|<\delta_2$, aleshores $|h(x)-h(x_0)|<\epsilon$. (3)
[5] (demostració) Per la desigualtat triangular, $\|h(x)f(x)-h(x_0)f(x_0)\|\leq\|h(x)f(x)-h(x)f(x_0)\|+\|h(x)f(x_0)-h(x_0)f(x_0)\|=|h(x)|\,\|f(x)-f(x_0)\|+\|f(x_0)\|\,|h(x)-h(x_0)|$.
[6] (demostració) El terme $\|f(x_0)\|$ és fix. Per fitar $|h(x)|$, apliquem (3) amb $\epsilon=1$: si $\|x-x_0\|<\delta_2(1)$, aleshores $|h(x)-h(x_0)|<1$ i, per tant, $|h(x)|<1+|h(x_0)|$.
[7] (demostració) Donat $\epsilon>0$, definim $\delta:=\min\left\{\delta_1\!\left(\frac{\epsilon}{2(1+|h(x_0)|)}\right),\ \delta_2\!\left(\frac{\epsilon}{2\|f(x_0)\|}\right)\right\}$ (si $f(x_0)=0$, el segon sumand és nul i no cal la segona condició).
[8] (demostració) Aleshores, si $\|x-x_0\|<\delta$, $\|h(x)f(x)-h(x_0)f(x_0)\|<(1+|h(x_0)|)\frac{\epsilon}{2(1+|h(x_0)|)}+\|f(x_0)\|\frac{\epsilon}{2\|f(x_0)\|}=\epsilon$, i $hf$ és contínua en $x_0$.


## T2.21:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T2.21] Proposició 21 (Tema 2) — Imatge contínua de compactes i connexos
Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $f:\Omega\subseteq M\to N$ contínua i $K\subseteq\Omega$. Aleshores,

(i) $K$ compacte $\Rightarrow f(K)$ compacte;

(ii) $K$ connex $\Rightarrow f(K)$ connex.
Demostració: (i) $K$ compacte $\Rightarrow f(K)$ compacte.
Ho demostrem primer per successions: Volem demostrar que tota successió $(y_n)_n\subset f(K)$ admet una parcial convergent en $f(K)$.
Per construcció, existeix una successió $(x_n)_n\subset K$ tal que $y_n=f(x_n)$ per a tota $n$. Per ser $K$ compacte, existeix una parcial convergent $(x_{n_k})_k\subset K$ a un valor $x_0\in K$. Per continuïtat de $f$, $(y_{n_k})_k:=(f(x_{n_k}))_k$ satisfà $\lim_{k\to\infty}y_{n_k}=f(x_0)\in f(K)$. Per tant, $f(K)$ és compacte.

També es pot demostrar usant recobriments d'oberts: Suposem que $f(K)\subseteq\bigcup_{i\in I}V_i$, on $V_i$ són oberts de $N$. Com que $f$ és contínua, per l'apartat (c) del teorema 17, existeix una col·lecció de $U_i$ oberts de $M$ tals que
$$f^{-1}(V_i)=U_i\cap\Omega;\quad\text{a més, }f(f^{-1}(V_i))=f(U_i\cap\Omega)\subseteq V_i,\ \forall i\in I.\qquad(4)$$
Prenem ara $x\in K$; clarament, $f(x)\in f(K)$ i, per tant, $f(x)\in V_j$ per a algun $j\in I$ i, en conseqüència, $x\in f^{-1}(V_j)\subseteq U_j\cap\Omega$.
D'altra banda, com que $K$ és compacte i $K\subseteq\bigcup_{i\in I}U_i$, existeix un recobriment finit tal que
$$K\subseteq(U_{i_1}\cup\cdots\cup U_{i_r})\cap\Omega=(U_{i_1}\cap\Omega)\cup\cdots\cup(U_{i_r}\cap\Omega).$$
Ajuntant ara aquesta darrera conclusió amb (4), tenim que:
$$f(K)\subseteq f(U_{i_1}\cap\Omega)\cup\cdots\cup f(U_{i_r}\cap\Omega)\subseteq V_{i_1}\cup\cdots\cup V_{i_r},$$
que és un subrecobriment finit de $f(K)$.

(ii) $K$ connex $\Rightarrow f(K)$ connex.
Demostrem el contrarecíproc i, en conseqüència, suposem que $f(K)$ no és connex. Per tant, existeix dos oberts $V_1\subset N$ i $V_2\subset N$ tals que
$$f(K)\subseteq V_1\cup V_2;\ f(K)\cap V_1\neq\emptyset,\ f(K)\cap V_2\neq\emptyset;\ f(K)\cap V_1\cap V_2=\emptyset.$$
Per continuïtat, existeixen dos oberts $U_1,U_2\subset M$ tals que $f^{-1}(V_i)=U_i\cap\Omega$ per a $i=1,2$.
Prenem ara $x\in K$. Llavors, $f(x)\in f(K)$ i, per tant, $f(x)\in V_i$ per a $i=1$ o $i=2$ i, a més, $f(x)\notin V_j$ per a $j=2$ o $j=1$, respectivament; equivalentment, $x\in f^{-1}(V_i)\subseteq U_i$ per a $i=1$ o $i=2$ i $x\notin f^{-1}(V_j)\subseteq U_j$ per a $j=2$ o $j=1$, respectivament. Concloem, doncs, que $K\subseteq U_1\cup U_2$.
D'altra banda, per construcció, $U_1\cap U_2\cap\Omega=\emptyset$, fet que implica que $U_1\cap U_2\cap K=\emptyset$.
Finalment, és fàcil veure també que $K\cap U_1\neq\emptyset$ i que $K\cap U_2\neq\emptyset$ ja que $f^{-1}(V_i)$, per a $i=1,2$, no poden ser buits (per construcció, existeix algun $y_i\in f(K)\cap V_i$ i, per tant, existeix algun $x_i\in K\cap(U_i\cap K)=K\cap U_i$).
Per tant, $K$ és disconnex.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Siguin $(M,d)$ i $(N,d')$ dos espais mètrics, $f:\Omega\subseteq M\to N$ contínua i $K\subseteq\Omega$. Aleshores: (i) $K$ tancat $\Rightarrow f(K)$ tancat; (ii) $K$ connex $\Rightarrow f(K)$ connex.
[2] (demostració) (i) Ho demostrem primer per successions: sigui $(y_n)_n\subseteq f(K)$; volem veure que admet una parcial convergent en $f(K)$. Per construcció, existeix $(x_n)_n\subseteq K$ amb $y_n=f(x_n)$ per a tota $n$.
[3] (demostració) Per ser $K$ compacte, existeix una parcial $(x_{n_k})_k$ convergent a un $x_0\in K$ i, per la continuïtat de $f$, $\lim_{k\to\infty}y_{n_k}=\lim_{k\to\infty}f(x_{n_k})=f(x_0)\in f(K)$. Per tant, $f(K)$ és compacte.
[4] (demostració) També es pot demostrar amb recobriments d'oberts: suposem que $f(K)\subseteq\bigcup_{i\in I}V_i$, amb $V_i$ oberts de $N$. Per l'apartat (c) del teorema 17, existeixen oberts $U_i$ de $M$ amb $f^{-1}(V_i)=U_i\cap\Omega$ i, per tant, $f(U_i\cap\Omega)\subseteq V_i$ per a tot $i\in I$.
[5] (demostració) Si $x\in K$, aleshores $f(x)\in V_j$ per a algun $j\in I$ i $x\in f^{-1}(V_j)=U_j\cap\Omega$; així, $K\subseteq\bigcup_{i\in I}U_i$. Per ser $K$ compacte, existeixen $i_1,\dots,i_r$ tals que $K\subseteq(U_{i_1}\cup\cdots\cup U_{i_r})\cap\Omega=(U_{i_1}\cap\Omega)\cup\cdots\cup(U_{i_r}\cap\Omega)$.
[6] (demostració) Aleshores $f(K)\subseteq f(U_{i_1}\cap\Omega)\cup\cdots\cup f(U_{i_r}\cap\Omega)\subseteq V_{i_1}\cup\cdots\cup V_{i_r}$, que és un subrecobriment finit de $f(K)$.
[7] (demostració) (ii) Demostrem el contrarecíproc: suposem que $f(K)$ no és connex, és a dir, que existeixen dos oberts $V_1,V_2\subseteq N$ amb $f(K)\subseteq V_1\cup V_2$, $f(K)\cap V_1\neq\emptyset$, $f(K)\cap V_2\neq\emptyset$ i $f(K)\cap V_1\cap V_2=\emptyset$. Per continuïtat, existeixen oberts $U_1,U_2\subseteq M$ amb $f^{-1}(V_i)=U_i\cap\Omega$ per a $i=1,2$.
[8] (demostració) Si $x\in K$, aleshores $f(x)\in V_1\cup V_2$, és a dir, $x\in f^{-1}(V_1)\cup f^{-1}(V_2)\subseteq U_1\cup U_2$; per tant, $K\subseteq U_1\cup U_2$.
[9] (demostració) D'altra banda, com que $f(K)\cap V_1\cap V_2=\emptyset$, per construcció tenim $U_1\cap U_2=\emptyset$ i, en particular, $U_1\cap U_2\cap K=\emptyset$.
[10] (demostració) Finalment, $K\cap U_1\neq\emptyset$ i $K\cap U_2\neq\emptyset$: existeix $y_i\in f(K)\cap V_i$, és a dir, $y_i=f(x_i)$ amb $x_i\in K$ i $x_i\in f^{-1}(V_i)\subseteq U_i$, per a $i=1,2$. Per tant, $K$ és disconnex.


## T2.28:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T2.28] Proposició 28 (Tema 2) — Lipschitz, uniforme i contínua
Lipschitz $\Rightarrow$ uniformement contínua $\Rightarrow$ contínua. Els recíprocs són falsos.
Demostració: Demostrem primer que si $f$ és Lipschitz, aleshores, és uniformement contínua. Sabem que $\exists C>0$ tal que $d'(f(x),f(y))<C\,d(x,y),\ \forall x,y\in\Omega$. Donat un $\epsilon>0$ qualsevol, si prenem $\delta=\epsilon/C$, tenim que $\forall x,y\in\Omega$ tal que $d(x,y)<\delta$, aleshores $d'(f(x),f(y))<C\,d(x,y)<\epsilon$. Per tant, $f$ és uniformement contínua.

Per definició, si $f$ uniformement contínua en $\Omega$, aleshores és contínua en tot punt $x_0\in\Omega$.

Ens falta veure que els recíprocs no són certs:

- La funció $f:(0,1]\longrightarrow\mathbb{R}$ definida com $f(x)=1/x$ és contínua, però no pas uniformement. Vegem que $\exists\epsilon>0\ \forall\delta>0$ t.q. $\exists x,y\in(0,1)$ amb $d(x,y)<\delta$ i tals que $|f(x)-f(y)|\geq\epsilon$: Prenem $\epsilon=1$, $x=\delta/2$ i $y=\delta/3$, amb $\delta<1$. Clarament, $|x-y|=\delta/6<\delta$ i
$$|f(x)-f(y)|=\frac{1}{\delta}>1.$$
- La funció $f:[0,1]\longrightarrow\mathbb{R}$ definida com $f(x)=\sqrt{x}$ és uniformement contínua, però no és Lipschitz:
  Suposem que $\exists C>0$ tal que $\forall x,y\in[0,1]$, $|\sqrt{x}-\sqrt{y}|<C\,|x-y|$. Ara bé, pel teorema del valor mitjà sabem que $\exists\xi\in(x,y)$ tal que
  $$|\sqrt{x}-\sqrt{y}|=\frac{1}{2\sqrt{\xi}}\,|x-y|.$$
  Caldria, doncs, que existís $C$ tal que $\dfrac{1}{2\sqrt{\xi}}\leq C$ per a tota $\xi$; però, prenent $x,y$ prou properes a zero, sempre podem aconseguir $\xi$ tan petita com vulguem i, per tant, $\dfrac{1}{2\sqrt{\xi}}$ tan gran com vulguem (!!).

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:\Omega\subseteq M\to N$. Aleshores, $f$ Lipschitz $\Rightarrow$ $f$ uniformement contínua $\Rightarrow$ $f$ contínua. Els recíprocs són falsos, fins i tot quan $\Omega$ és compacte.
[2] (demostració) Si $f$ és Lipschitz, existeix $C>0$ tal que $d'(f(x),f(y))\leq C\,d(x,y)$ per a tot $x,y\in\Omega$. Donat $\epsilon>0$, prenem $\delta=C\,\epsilon$: si $x,y\in\Omega$ i $d(x,y)<\delta$, aleshores $d'(f(x),f(y))\leq C\,d(x,y)<\epsilon$. Per tant, $f$ és uniformement contínua.
[3] (demostració) Per definició, si $f$ és uniformement contínua en $\Omega$, aleshores és contínua en tot punt $x_0\in\Omega$ (el mateix $\delta$ serveix per a tots els punts).
[4] (demostració) Vegem que els recíprocs no són certs. La funció $f:(0,1]\to\mathbb{R}$, $f(x)=1/x$, és contínua però no uniformement contínua: cal veure que existeix $\epsilon>0$ tal que per a tot $\delta>0$ hi ha $x,y\in(0,1]$ amb $|x-y|<\delta$ i $|f(x)-f(y)|\geq\epsilon$.
[5] (demostració) Prenem $\epsilon=1$ i, donat $\delta>0$ (podem suposar $\delta<1$), $x=\delta/2$ i $y=\delta/3$. Aleshores $|x-y|=\delta/6<\delta$ i $|f(x)-f(y)|=\left|\frac{2}{\delta}-\frac{3}{\delta}\right|=\frac{1}{\delta}>1$.
[6] (demostració) La funció $f:[0,1]\to\mathbb{R}$, $f(x)=\sqrt{x}$, és uniformement contínua però no és Lipschitz. Suposem que existeix $C>0$ tal que $|\sqrt{x}-\sqrt{y}|\leq C\,|x-y|$ per a tot $x,y\in[0,1]$.
[7] (demostració) Pel teorema del valor mitjà, per a $0<x<y\leq1$ existeix $\xi\in(x,y)$ tal que $|\sqrt{x}-\sqrt{y}|=\frac{1}{2\sqrt{\xi}}\,|x-y|$. Caldria, doncs, que $\frac{1}{2\sqrt{\xi}}\leq C$ per a totes les $\xi$ obtingudes així.
[8] (demostració) Però, prenent $x,y$ prou propers a zero, $\xi$ és tan petit com vulguem i $\frac{1}{2\sqrt{\xi}}$ tan gran com vulguem, en contradicció amb l'existència de $C$.

## T3.9:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
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
Demostració: (i) Que $f$ sigui diferenciable al punt $a$ equival al fet que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.$$
En particular, aquest límit és zero sigui quin sigui el camí que porti $x$ cap a $a$ (proposició 10 del tema 2). Prenem com a tal la recta definida per $x=a+t\,u$, amb $t\in\mathbb{R}$ i $u$ qualsevol vector no nul a $\mathbb{R}^n$. Així,
$$\begin{aligned}0&=\lim_{t\to0}\frac{\|f(a+tu)-f(a)-Df(a)(tu)\|}{\|tu\|}=\lim_{t\to0}\frac{\|f(a+tu)-f(a)-tDf(a)(u)\|}{\|tu\|}\\&=\frac{1}{\|u\|}\lim_{t\to0}\left\|\frac{f(a+tu)-f(a)-tDf(a)u}{t}\right\|=\frac{1}{\|u\|}\lim_{t\to0}\left\|\frac{f(a+tu)-f(a)}{t}-Df(a)u\right\|.\end{aligned}$$
És a dir,
$$\lim_{t\to0}\frac{f(a+tu)-f(a)}{t}=Df(a)u$$
o, equivalentment,
$$D_uf(a)=Df(a)u.$$

(ii) $Df(a)$ és lineal i, per tant, fixades les bases canòniques a $\mathbb{R}^n$ i $\mathbb{R}^m$, la seva matriu associada $M$ en aquestes bases és única. Noteu que
$$Me_j=D_{e_j}f(a)=\frac{\partial f}{\partial x_j}(a)=\left(\frac{\partial f_1}{\partial x_j}(a)\ \ \frac{\partial f_2}{\partial x_j}(a)\ \ \ldots\ \ \frac{\partial f_m}{\partial x_j}(a)\right)^\top$$
proporciona, necessàriament, la columna $j$-èsima $1\leq j\leq n$ de la matriu, de manera que la matriu $M$ coincideix amb l'expressió donada per a $Jf(a)$ a (4).

(iii) L'hiperplà tangent a $x_{n+1}=f(x)$ en un punt $(a,f(a))$ ve donat per
$$(a,f(a))+\left\langle\left(e_1,\frac{\partial f}{\partial x_1}(a)\right),\ldots,\left(e_n,\frac{\partial f}{\partial x_n}(a)\right)\right\rangle,$$
on $e_j$ és el vector $j$-èsim de la base canònica; és a dir, és el pla a $\mathbb{R}^{n+1}$ que conté el punt $(a,f(a))$ i està generat pels vectors $\left(e_j,\dfrac{\partial f}{\partial x_j}(a)\right)$, per a $j=1,\ldots,n$.
Vegem ara que $(u,D_uf(a))$ es pot posar com a combinació dels generadors de l'hiperplà per a tot $u\in\mathbb{R}^n\setminus\{0\}$.

En efecte, si $u\in\mathbb{R}^n\setminus\{0\}$, el podem expressar de la forma $u=\lambda_1e_1+\lambda_2e_2+\cdots+\lambda_ne_n$ (és a dir, $(\lambda_1,\lambda_2,\ldots,\lambda_n)$ és l'expressió d'$u$ en coordenades de la base $\{e_j\}_{j=1}^n$). Aleshores, $f$ diferenciable en $a$ implica que
$$\begin{aligned}(u,D_uf(a))&=(u,Jf(a)u)=\left(u,\sum_{i=1}^n\lambda_iJf(a)e_i\right)\\&=\left(\lambda_1e_1+\cdots+\lambda_ne_n,\sum_{i=1}^n\lambda_iJf(a)e_i\right)=\sum_{i=1}^n\lambda_i\left(e_i,\frac{\partial f}{\partial x_i}(a)\right).\end{aligned}$$
En el cas particular de $m=1$, tenim que els punts de l'hiperplà tangent satisfan
$$(x,x_{n+1})=(a,f(a))+\lambda_1\left(e_1,\frac{\partial f}{\partial x_1}(a)\right)+\cdots+\lambda_n\left(e_n,\frac{\partial f}{\partial x_n}(a)\right),$$
d'on
$$\begin{aligned}x&=a+\lambda_1e_1+\cdots\lambda_ne_n\Longrightarrow x_i-a_i=\lambda_i,\quad i=1,\ldots n,\\x_{n+1}&=f(a)+\lambda_1\frac{\partial f}{\partial x_1}(a)+\cdots+\lambda_n\frac{\partial f}{\partial x_n}(a).\end{aligned}$$
Ajuntant ambdues expressions obtenim l'expressió del corresponent hiperplà tangent
$$x_{n+1}=f(a)+\frac{\partial f}{\partial x_1}(a)\,(x-a_1)+\cdots+\frac{\partial f}{\partial x_n}(a)\,(x_n-a_n)=f(a)+Jf(a)(x-a).$$
Si $n=1$ l'expressió de la recta tangent al punt $(a,f(a))$ és
$$y=f(a)+f'(a)(x-a),$$
mentre que per a $n=2$, el pla tangent ve donat per l'expressió
$$z=f(a_1,a_2)+\frac{\partial f}{\partial x}(a_1,a_2)\,(x-a_1)+\frac{\partial f}{\partial y}(a_1,a_2)\,(y-a_2).$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, diferenciable en $a\in\mathring{\Omega}$. Llavors: (i) existeixen totes les derivades direccionals de $f$ al punt $a$ i, a més, $D_uf(a)=Df(a)\,\frac{u}{\|u\|}$ per a tot $u\neq0$.
[2] (enunciat) (ii) La diferencial $Df(a)$ és única i, fixades les bases canòniques a $\mathbb{R}^n$ i $\mathbb{R}^m$, té per matriu la jacobiana $Jf(a)=\left(\frac{\partial f_i}{\partial x_j}(a)\right)_{i,j}$, amb $1\leq i\leq m$ i $1\leq j\leq n$.
[3] (enunciat) (iii) Per a $m=1$, l'hiperplà tangent al graf de $f$, $x_{n+1}=f(x)$, en el punt $(a,f(a))$ és $x_{n+1}=f(a)+Jf(a)(x-a)$. En particular, per a $n=2$, el pla tangent a $z=f(x,y)$ en el punt $(a_1,a_2,f(a_1,a_2))$ és $z=f(a)+\frac{\partial f}{\partial x}(a)\,(x-a_1)+\frac{\partial f}{\partial y}(a)\,(y-a_2)$, i en aquest cas $D_uf(a)=Df(a)\,u=\langle\nabla f(a),u\rangle$ per a tot $u\neq0$.
[4] (demostració) (i) Que $f$ sigui diferenciable en $a$ equival a $\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0$. En particular, aquest límit és zero sigui quin sigui el camí pel qual $x$ tendeix a $a$; prenem la recta $x=a+tu$, $t\in\mathbb{R}$, amb $u\neq0$ fixat.
[5] (demostració) Com que $Df(a)$ és lineal, $Df(a)(tu)=t\,Df(a)u$, i per tant $0=\lim_{t\to0}\frac{\|f(a+tu)-f(a)-t\,Df(a)u\|}{\|tu\|}=\frac{1}{\|u\|}\lim_{t\to0}\left\|\frac{f(a+tu)-f(a)}{t}-Df(a)u\right\|$. És a dir, $D_uf(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t}=Df(a)u$.
[6] (demostració) (ii) Com que $Df(a)$ és lineal, fixades les bases canòniques la seva matriu $M$ és única. Pel punt (i), el vector $Me_j=D_{e_j}f(a)=\frac{\partial f}{\partial x_j}(a)=\left(\frac{\partial f_1}{\partial x_j}(a),\ldots,\frac{\partial f_m}{\partial x_j}(a)\right)^\top$ és necessàriament la fila $j$-èsima de $M$, per a $1\leq j\leq n$, i per tant $M=Jf(a)$.
[7] (demostració) (iii) L'hiperplà tangent al graf en $(a,f(a))$ és l'hiperplà de $\mathbb{R}^{n+1}$ que passa per $(a,f(a))$ i està generat pels vectors $\left(e_j,\frac{\partial f}{\partial x_j}(a)\right)$, $j=1,\ldots,n$. Si $u=\lambda_1e_1+\cdots+\lambda_ne_n\neq0$, per (i) i (ii) tenim $(u,D_uf(a))=(u,Jf(a)u)=\sum_{i=1}^n\lambda_i\left(e_i,\frac{\partial f}{\partial x_i}(a)\right)$, de manera que $(u,D_uf(a))$ és combinació dels generadors.
[8] (demostració) Per tant, els punts de l'hiperplà tangent són $(x,x_{n+1})=(a,f(a))+\sum_{i=1}^n\lambda_i\left(e_i,\frac{\partial f}{\partial x_i}(a)\right)$, d'on $x_i-a_i=\lambda_i$ per a $i=1,\ldots,n$ i $x_{n+1}=f(a)+\sum_{i=1}^n\frac{\partial f}{\partial x_i}(a)\,(x_i-a_i)=f(a)+Jf(a)(x-a)$.
[9] (demostració) Per a $n=2$ això dona el pla $z=f(a_1,a_2)+\frac{\partial f}{\partial x}(a_1,a_2)\,(x-a_1)+\frac{\partial f}{\partial y}(a_1,a_2)\,(y-a_2)$; i, com que per a $m=1$ la jacobiana $Jf(a)$ s'identifica amb el gradient $\nabla f(a)$, de (i) resulta $D_uf(a)=Df(a)\,u=\langle\nabla f(a),u\rangle$.


## T3.13:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.13] Proposició 13 (Tema 3) — Direcció de màxim creixement i gradient
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciable en un punt $a\in\mathring{\Omega}$. Aleshores:

(i) $\displaystyle\max_{\|u\|=1}\{D_uf(a)\}=\|\nabla f(a)\|$ i aquest valor s'obté per a $u=\dfrac{\nabla f(a)}{\|\nabla f(a)\|}$.

(ii) De manera anàloga, $\displaystyle\min_{\|u\|=1}\{D_uf(a)\}=-\|\nabla f(a)\|$ i aquest valor s'obté per al vector $u=-\dfrac{\nabla f(a)}{\|\nabla f(a)\|}$.

(iii) Considerem el cas $n=2$. Sigui $\gamma=\{x\in\mathbb{R}^2\mid f(x,y)=f(a_1,a_2)\}$ la corba de nivell (al pla $(x,y)$) d'alçada $f(a_1,a_2)$. Aleshores, el vector gradient de $f$ al punt $(a_1,a_2)$, $\nabla f(a_1,a_2)$, és ortogonal a la corba $\gamma$ en el punt $(a_1,a_2)$.
Demostració: Sigui $u\in\mathbb{R}^n\setminus\{0\}$, normalitzat (és a dir $\|u\|=1$). (Nota: Per defecte, si no es diu el contrari, al llarg d'aquesta secció la norma vectorial considerada serà l'euclidiana. En qualsevol cas, les fites emprades són també vàlides per a normes matricials que siguin consistents amb la norma vectorial fixada.) Del fet que $f$ és diferenciable al punt $a$ es deriva que
$$D_uf(a)=\langle\nabla f(a),u\rangle=\|\nabla f(a)\|\|u\|\cos\alpha=\|\nabla f(a)\|\cos\alpha,$$
on $\alpha$ és l'angle (petit) comprès entre els vectors $\nabla f(a)$ i $u$. És clar que
$$-\|\nabla f(a)\|\leq\|\nabla f(a)\|\cos\alpha\leq\|\nabla f(a)\|.$$
El valor màxim s'ateny per a $\cos\alpha=1$, és a dir $\alpha=0$ i, en conseqüència, per a $u=\nabla f(a)/\|\nabla f(a)\|$:
$$\max_{\|u\|=1}\{D_uf(a)\}=D_{\frac{\nabla f(a)}{\|\nabla f(a)\|}}f(a)=\|\nabla f(a)\|.$$
De manera similar, el valor mínim correspon a $\cos\alpha=-1$, o sigui, l'angle entre $u$ i $\nabla f(a)$ és igual a $\pi$. Així, $u=-\nabla f(a)/\|\nabla f(a)\|$ i
$$\min_{\|u\|=1}\{D_uf(a)\}=D_{-\frac{\nabla f(a)}{\|\nabla f(a)\|}}f(a)=-\|\nabla f(a)\|.$$

(iii) Clarament, el punt $(a_1,a_2)$ pertany a la corba $\gamma$. La corresponent corba dins de la gràfica $z=f(x,y)$, donada per
$$\Gamma=\{(x,y,z)\in\mathbb{R}^3\mid(x,y)\in\gamma,\ z=f(a_1,a_2)\},$$
està caracteritzada pel fet que tots els seus punts tenen la mateixa alçada $f(a_1,a_2)$. En particular, al punt $(a_1,a_2)\in\gamma$. La derivada direccional $D_{u_\tau}f(a_1,a_2)$ en la direcció i sentit del vector (unitari) tangent $u_\tau$ a $\gamma$ ens manté dins la corba $\gamma$, no varia el valor de $f$ i, per tant, satisfà que $D_{u_\tau}f(a_1,a_2)=0$. Del fet que $f$ és diferenciable al punt $a$ es dedueix que
$$0=D_{u_\tau}f(a_1,a_2)=\langle\nabla f(a_1,a_2),u_\tau\rangle\Rightarrow\nabla f(a_1,a_2)\perp u_\tau.$$
És a dir, per definició, $\nabla f(a_1,a_2)$ és ortogonal a la corba $\gamma$ al punt $(a_1,a_2)$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciable en un punt $a\in\mathring{\Omega}$. Aleshores: (i) $\displaystyle\max_{u\neq0}\{D_uf(a)\}=\|\nabla f(a)\|$ i aquest valor s'obté per a $u=\dfrac{\nabla f(a)}{\|\nabla f(a)\|}$; (ii) de manera anàloga, $\displaystyle\min_{\|u\|=1}\{D_uf(a)\}=-\|\nabla f(a)\|$ i aquest valor s'obté per al vector $u=-\dfrac{\nabla f(a)}{\|\nabla f(a)\|}$.
[2] (enunciat) (iii) Considerem el cas $n=2$ i sigui $\gamma=\{(x,y)\in\mathbb{R}^2\mid f(x,y)=f(a_1,a_2)\}$ la corba de nivell d'alçada $f(a_1,a_2)$. Aleshores el vector gradient $\nabla f(a_1,a_2)$ és ortogonal a la corba $\gamma$ en el punt $(a_1,a_2)$.
[3] (demostració) Sigui $u\in\mathbb{R}^n$ amb $\|u\|=1$ (norma euclidiana). Com que $f$ és diferenciable en $a$, $D_uf(a)=\langle\nabla f(a),u\rangle=\|\nabla f(a)\|\,\|u\|\cos\alpha=\|\nabla f(a)\|\cos\alpha$, on $\alpha$ és l'angle entre els vectors $\nabla f(a)$ i $u$.
[4] (demostració) És clar que $0\leq\|\nabla f(a)\|\cos\alpha\leq\|\nabla f(a)\|$.
[5] (demostració) El valor màxim s'ateny per a $\cos\alpha=1$, és a dir $\alpha=0$ i, en conseqüència, per a $u=\nabla f(a)/\|\nabla f(a)\|$: $\displaystyle\max_{\|u\|=1}\{D_uf(a)\}=D_{\frac{\nabla f(a)}{\|\nabla f(a)\|}}f(a)=\|\nabla f(a)\|$.
[6] (demostració) De manera similar, el valor mínim correspon a $\cos\alpha=-1$, és a dir, a un angle $\pi$ entre $u$ i $\nabla f(a)$. Així, $u=-\nabla f(a)/\|\nabla f(a)\|$ i $\displaystyle\min_{\|u\|=1}\{D_uf(a)\}=D_{-\frac{\nabla f(a)}{\|\nabla f(a)\|}}f(a)=-\|\nabla f(a)\|$.
[7] (demostració) (iii) Clarament, el punt $(a_1,a_2)$ pertany a $\gamma$. La corba corresponent dins de la gràfica, $\Gamma=\{(x,y,z)\in\mathbb{R}^3\mid(x,y)\in\gamma,\ z=f(a_1,a_2)\}$, està caracteritzada pel fet que tots els seus punts tenen la mateixa alçada $f(a_1,a_2)$.
[8] (demostració) La derivada direccional $D_{u_\tau}f(a_1,a_2)$ segons el vector unitari tangent $u_\tau$ a $\gamma$ ens manté dins la corba $\gamma$, on el valor de $f$ no varia; per tant, $D_{u_\tau}f(a_1,a_2)=0$.
[9] (demostració) Com que $f$ és diferenciable, $0=D_{u_\tau}f(a_1,a_2)=\langle\nabla f(a_1,a_2),u_\tau\rangle$, és a dir, $\nabla f(a_1,a_2)\perp u_\tau$. Per definició, això vol dir que $\nabla f(a_1,a_2)$ és ortogonal a la corba $\gamma$ en el punt $(a_1,a_2)$.


## T3.14:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.14] Proposició 14 (Tema 3) — Diferenciable implica contínua i Lipschitz
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $a\in\mathring{\Omega}$. Si $f$ és diferenciable al punt $a$, aleshores:

(i) $f$ és contínua al punt $a$.

(ii) $f$ és localment Lipschitz en $a$. (Nota: De fet, és més precís dir que és localment puntualment Lipschitz en $a$; és a dir que existeix $\delta>0$ i $M>0$ tal que $d(f8x),f(x))<M\,d(x,a)$ per a tota $x\in B(a,\delta)$. [transcripció literal de la nota; sembla un error tipogràfic de l'original])
Demostració: Observem primer que
$$\begin{aligned}\|f(x)-f(a)\|&\leq\|f(x)-f(a)-Df(a)(x-a)\|+\|Df(a)(x-a)\|\\&\leq\|f(x)-f(a)-Df(a)(x-a)\|+\|Jf(a)\|\|(x-a)\|,\end{aligned}\tag{8}$$
on hem considerat una norma matricial consistent amb la norma vectorial (per exemple, euclidiana). Per la diferenciabilitat de $f$ en $a$, per a tot $\varepsilon>0$, existeix $\delta_1=\delta_1(\epsilon)$ tal que si $\|x-a\|<\delta_1$, aleshores
$$\|f(x)-f(a)-Df(a)(x-a)\|<\varepsilon\,\|x-a\|.$$
(ii) Si fixem $\varepsilon=\varepsilon_0>0$ qualsevol, aleshores, a partir de (8), tenim que si $\|x-a\|<\delta_1(\varepsilon_0)$, llavors
$$\|f(x)-f(a)\|<(\varepsilon_0+\|Jf(a)\|)\,\|x-a\|;\tag{9}$$
és a dir, $f$ és (puntualment) localment Lipschitz al punt $a$, amb constant de Lipschitz $L:=L(a)=\varepsilon_0+\|Jf(a)\|$.

(i) Donat $\varepsilon>0$, si definim $\delta=\min\left\{\delta_1(\varepsilon_0),\dfrac{\varepsilon}{L}\right\}$, prenent $\|x-a\|<\delta$ i usant (9), obtenim que
$$\|f(x)-f(a)\|<L\,\|x-a\|<L\frac{\varepsilon}{L}=\varepsilon,$$
i, per tant, $f$ és contínua en $a$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $a\in\mathring{\Omega}$. Si $f$ és diferenciable al punt $a$, aleshores: (i) $f$ és contínua al punt $a$;
[2] (enunciat) (ii) $f$ és localment Lipschitz en $a$, és a dir, existeixen $\delta>0$ i $M>0$ tals que $\|f(x)-f(y)\|\leq M\|x-y\|$ per a tots $x,y\in B(a,\delta)$.
[3] (demostració) Observem primer que, per la desigualtat triangular i considerant una norma matricial consistent amb la norma vectorial, $\|f(x)-f(a)\|\leq\|f(x)-f(a)-Df(a)(x-a)\|+\|Df(a)(x-a)\|\leq\|f(x)-f(a)-Df(a)(x-a)\|+\|Jf(a)\|\,\|x-a\|$. (8)
[4] (demostració) Per la diferenciabilitat de $f$ en $a$, per a tot $\varepsilon>0$ existeix $\delta_1=\delta_1(\varepsilon)>0$ tal que si $0<\|x-a\|<\delta_1$, aleshores $\|f(x)-f(a)-Df(a)(x-a)\|<\varepsilon\,\|x-a\|$.
[5] (demostració) (ii) Fixem $\varepsilon_0>0$ qualsevol. A partir de (8), si $0<\|x-a\|<\delta_1(\varepsilon_0)$, llavors $\|f(x)-f(a)\|<(\varepsilon_0+\|Jf(a)\|)\,\|x-a\|$ (9); és a dir, $f$ és (puntualment) localment Lipschitz al punt $a$, amb constant $L:=\varepsilon_0+\|Jf(a)\|$.
[6] (demostració) (i) Donat $\varepsilon>0$, definim $\delta=\dfrac{\varepsilon}{L}$. Si $0<\|x-a\|<\delta$, usant (9) obtenim $\|f(x)-f(a)\|<L\,\|x-a\|<L\,\dfrac{\varepsilon}{L}=\varepsilon$.
[7] (demostració) Com que per a $x=a$ la desigualtat $\|f(x)-f(a)\|<\varepsilon$ és immediata, concloem que $f$ és contínua en $a$.


## T3.23:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.23] Proposició 23 (Tema 3) — Àlgebra de funcions diferenciables
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciables en $a\in\mathring{\Omega}$ i sigui $\lambda\in\mathbb{R}$. Llavors,

(i) $f+g$ és diferenciable en $a$ i $D(f+g)(a)=Df(a)+Dg(a)$.

(ii) $\lambda f$ és diferenciable en $a$ i $D(\lambda f)(a)=\lambda Df(a)$.

(iii) $fg$ és diferenciable en $a$ i $J(fg)(a)=g(a)Jf(a)+f(a)Jg(a)$.

(iv) $\dfrac{f}{g}$ és diferenciable en $a$ si $g(a)\neq0$. A més
$$J\left(\frac{f}{g}\right)(a)=\frac{g(a)Jf(a)-f(a)Jg(a)}{g(a)^2}.$$
Demostració: Farem la demostració de la primera afirmació (i) i deixarem la resta com a exercici. Es basen en idees similars.

(i) Cal veure que, fixat $\varepsilon>0$, existeix $\delta=\delta(\varepsilon)>0$ i una aplicació lineal $D(f+g)(a)$ tals que si $x\in\Omega$, amb $\|x-a\|<\delta$ aleshores
$$\|(f+g)(x)-(f+g)(a)-D(f+g)(a)(x-a)\|<\varepsilon\|x-a\|.$$
Definim $D(f+g)(a)$ com l'aplicació lineal de $\mathbb{R}^n$ a $\mathbb{R}$ que té matriu associada, en les bases canòniques, $J(f+g)(a)=Jf(a)+Jg(a)$. Aleshores, del fet que $f$ i $g$ siguin diferenciables en $a$ es deriva que existeixen $\delta_1(\varepsilon)$ i $\delta_2(\varepsilon)$ de forma que, si $x\in\Omega$ i $\|x-a\|<\delta_1$, llavors
$$\|f(x)-f(a)-Jf(a)(x-a)\|<\frac{\varepsilon}{2}\|x-a\|,$$
i si $x\in\Omega$ amb $\|x-a\|<\delta_2$, llavors
$$\|g(x)-g(a)-Jg(a)(x-a)\|<\frac{\varepsilon}{2}\|x-a\|.$$
Per tant, per a tot $x\in\Omega$ tal que $\|x-a\|<\delta$, amb $\delta<\min\{\delta_1,\delta_2\}$, tenim que
$$\begin{aligned}\|(f+g)(x)&-(f+g)(a)-D(f+g)(a)(x-a)\|\\&=\|(f+g)(x)-(f+g)(a)-(Jf(a)+Jg(a))(a)(x-a)\|\\&\leq\|f(x)-f(a)-Jf(a)(x-a)\|+\|g(x)-g(a)-Jg(a)(x-a)\|<\varepsilon\|x-a\|\end{aligned}$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciables en $a\in\mathring{\Omega}$ i sigui $\lambda\in\mathbb{R}$. Llavors: (i) $f+g$ és diferenciable en $a$ i $D(f+g)(a)=Df(a)+Dg(a)$; (ii) $\lambda f$ és diferenciable en $a$ i $D(\lambda f)(a)=\lambda Df(a)$.
[2] (enunciat) (iii) $fg$ és diferenciable en $a$ i $J(fg)(a)=g(a)Jf(a)+f(a)Jg(a)$; (iv) si $g(a)\neq0$, $\dfrac{f}{g}$ és diferenciable en $a$ i, a més, $J\left(\dfrac{f}{g}\right)(a)=\dfrac{g(a)Jf(a)-f(a)Jg(a)}{g(a)}$.
[3] (demostració) Farem la demostració de l'afirmació (i); la resta es basen en idees similars i queden com a exercici. Cal veure que, fixat $\varepsilon>0$, existeix $\delta=\delta(\varepsilon)>0$ tal que si $x\in\Omega$ i $0<\|x-a\|<\delta$, aleshores $|(f+g)(x)-(f+g)(a)-D(f+g)(a)(x-a)|<\varepsilon\|x-a\|$, on $D(f+g)(a)$ és una aplicació lineal.
[4] (demostració) Definim $D(f+g)(a)$ com l'aplicació lineal de $\mathbb{R}^n$ a $\mathbb{R}$ que té matriu associada, en les bases canòniques, $J(f+g)(a)=Jf(a)+Jg(a)$.
[5] (demostració) Com que $f$ i $g$ són diferenciables en $a$, existeixen $\delta_1,\delta_2>0$ tals que si $x\in\Omega$ i $0<\|x-a\|<\delta_1$, llavors $|f(x)-f(a)-Jf(a)(x-a)|<\frac{\varepsilon}{2}\|x-a\|$, i si $x\in\Omega$ i $0<\|x-a\|<\delta_2$, llavors $|g(x)-g(a)-Jg(a)(x-a)|<\frac{\varepsilon}{2}\|x-a\|$.
[6] (demostració) Prenem $\delta=\max\{\delta_1,\delta_2\}$ i sigui $x\in\Omega$ amb $0<\|x-a\|<\delta$.
[7] (demostració) Per la desigualtat triangular, $|(f+g)(x)-(f+g)(a)-(Jf(a)+Jg(a))(x-a)|\leq|f(x)-f(a)-Jf(a)(x-a)|+|g(x)-g(a)-Jg(a)(x-a)|<\frac{\varepsilon}{2}\|x-a\|+\frac{\varepsilon}{2}\|x-a\|=\varepsilon\|x-a\|$, i per tant $f+g$ és diferenciable en $a$ amb $D(f+g)(a)=Df(a)+Dg(a)$.


## T3.26:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.26] Corol·lari 26 (Tema 3) — Teorema del valor mitjà (cas m=1)
(Cas $m=1$). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciable en un obert $\Omega\subseteq\mathbb{R}^n$. Aleshores, $\forall a,b\in\Omega$ tal que $[a,b]\subseteq\Omega$ existeix un $\xi\in[a,b]$ tal que $f(b)-f(a)=\langle\nabla f(\xi),b-a\rangle$.
Demostració: N'hi ha prou a considerar $u=1$ en el cas general i usar que $\langle1,Jf(\xi)\,(b-a)\rangle=\langle1,\langle\nabla f(\xi),b-a\rangle\rangle=\langle\nabla f(\xi),b-a\rangle$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Cas $m=1$). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciable en un obert $\Omega\subseteq\mathbb{R}^n$.
[2] (enunciat) Aleshores existeix un $\xi\in\Omega$ tal que, per a tots $a,b\in\Omega$ amb $[a,b]\subseteq\Omega$, es té $f(b)-f(a)=\langle\nabla f(\xi),b-a\rangle$.
[3] (demostració) Com que $f$ és diferenciable a l'obert $\Omega$, és de classe $\mathcal{C}^1(\Omega)$, i això ens permet aplicar el teorema del valor mitjà general (teorema 25) en el cas $m=1$.
[4] (demostració) Siguin $a,b\in\Omega$ amb $[a,b]\subseteq\Omega$. Pel teorema 25, per a cada $u\in\mathbb{R}$ existeix $\xi\in(a,b)$ tal que $\langle u,f(b)-f(a)\rangle=\langle u,Jf(\xi)\,(b-a)\rangle$. N'hi ha prou a considerar $u=1$, de manera que el membre esquerre és $\langle1,f(b)-f(a)\rangle=f(b)-f(a)$.
[5] (demostració) Per a $m=1$, la jacobiana $Jf(\xi)$ és la matriu fila que s'identifica amb $\nabla f(\xi)$, de manera que $\langle1,Jf(\xi)\,(b-a)\rangle=Jf(\xi)\,(b-a)=\langle\nabla f(\xi),b-a\rangle$.
[6] (demostració) En conseqüència, $f(b)-f(a)=\langle\nabla f(\xi),b-a\rangle$ per a un cert $\xi\in(a,b)\subseteq[a,b]$.


## T3.28:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.28] Corol·lari 28 (Tema 3) — Jacobiana nul·la implica funció constant
Sigui $f:\mathbb{R}^n\to\mathbb{R}^m$ diferenciable en un obert pre-convex $\Omega\subseteq\mathbb{R}^n$. Aleshores, si $Jf(a)=0$ per a tot $a\in\Omega$, llavors $f$ és constant a $\Omega$.
Demostració: Siguin $a,b\in\Omega$ dos punts qualsevol. Donat que $\Omega$ és pre-convex, existeix una cadena de segments consecutius que connecten $a$ i $b$: $z_0=a,z_1,z_2,\ldots,z_r=b\in\Omega$ tals que $[z_i,z_{i+1}]\subseteq\Omega$. Llavors, per a $u\in\mathbb{R}^m$:

$\exists\xi_1\in[z_0,z_1]$ tal que $\langle u,f(z_1)-f(z_0)\rangle=\langle u,Jf(\xi_1)\,(z_1-z_0)\rangle=\langle u,0\rangle=0$,

$\exists\xi_2\in[z_1,z_2]$ tal que $\langle u,f(z_2)-f(z_1)\rangle=\langle u,Jf(\xi_2)\,(z_2-z_1)\rangle=\langle u,0\rangle=0$,

$\ldots\exists\xi_r\in[z_{r-1},z_r]$ tal que $\langle u,f(z_r)-f(z_{r-1})\rangle=\langle u,Jf(\xi_r)\,(z_r-z_{r-1})\rangle=\langle u,0\rangle=0$.

D'aquí es deriva que
$$\langle u,f(b)-f(a)\rangle=\sum_{i=1}^r\langle u,f(z_i)-f(z_{i-1})\rangle=0.$$
Si prenem $u=f(b)-f(a)$ aleshores, a l'anterior expressió, s'obté que
$$0=\langle f(b)-f(a),f(b)-f(a)\rangle=\|f(b)-f(a)\|^2,$$
d'on $f(b)=f(a)$, és a dir, $f$ és constant a $\Omega$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:\mathbb{R}^n\to\mathbb{R}^m$ diferenciable en un obert pre-convex $\Omega\subseteq\mathbb{R}^n$. Aleshores, si $Jf(a)=0$ per a tot $a\in\Omega$, llavors $f$ és constant a tot $\mathbb{R}^n$.
[2] (demostració) Siguin $a,b\in\Omega$ dos punts qualsevol. Com que $\Omega$ és pre-convex, existeixen $z_0=a,z_1,\ldots,z_r=b\in\Omega$ tals que $[z_{i-1},z_i]\subseteq\Omega$ per a $i=1,\ldots,r$. Fixem $u\in\mathbb{R}^m$.
[3] (demostració) Pel teorema del valor mitjà aplicat a cada segment, per a cada $i=1,\ldots,r$ existeix $\xi_i\in[z_{i-1},z_i]$ tal que $\langle u,f(z_i)-f(z_{i-1})\rangle=\langle u,Jf(\xi_i)\,(z_i-z_{i-1})\rangle$.
[4] (demostració) Com que $\xi_i\in\Omega$, tenim $Jf(\xi_i)=0$ i, per tant, $\langle u,f(z_i)-f(z_{i-1})\rangle=\langle u,0\rangle=0$ per a tot $i=1,\ldots,r$.
[5] (demostració) D'aquí es dedueix que $\langle u,f(b)-f(a)\rangle=\sum_{i=1}^r\langle u,f(z_i)-f(z_{i-1})\rangle=0$, i això per a tot $u\in\mathbb{R}^m$.
[6] (demostració) Prenent $u=e_1$, el primer vector de la base canònica, s'obté $f_1(b)-f_1(a)=0$, d'on $f(b)=f(a)$.
[7] (demostració) Com que $a,b\in\Omega$ eren arbitraris, $f$ és constant a $\Omega$.


## T3.18:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.
Demostració: Primer, recordem que a $\mathbb{R}^n$ totes les normes són equivalents. En particular, existeix $\mu>0$ de manera que $\|x\|=\|x\|_2\leq\mu\|x\|_1$.

Reduirem la demostració a provar que totes les funcions component $f_i$ ($i=1,2,\ldots,m$) són diferenciables al punt $a$. Suposem que el següent resultat és cert.

Afirmació. Totes les funcions component de $f$, o sigui $f_i$, per a $i=1,2,\ldots,m$, són diferenciables al punt $x=a$.

Si aquesta afirmació és certa, llavors $f$ és diferenciable al punt $x=a$. En efecte, fixat $\varepsilon>0$, sabem que existeix $\delta_i>0$ de manera que si $\|x-a\|<\delta_i$ aleshores
$$|f_i(x)-f_i(a)-Jf_i(a)(x-a)|<\frac{\varepsilon}{\mu m}\|x-a\|,$$
per a $i=1,2,\ldots,m$ i on
$$Jf_i(a)=Df_i(a)=\left(\frac{\partial f_i}{\partial x_1}(a)\ \ \frac{\partial f_i}{\partial x_2}(a)\ \ \cdots\ \ \frac{\partial f_i}{\partial x_n}(a)\right).$$
En conseqüència, si $\|x-a\|<\delta<\min_{i\in\{1,2,\ldots,m\}}\delta_i$, es dedueix que
$$\begin{aligned}\|f(x)-f(a)-Jf(a)(x-a)\|&\leq\mu\|f(x)-f(a)-Jf(a)(x-a)\|_1\\&=\mu\sum_{i=1}^m|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\mu\sum_{i=1}^m\frac{\varepsilon}{\mu m}\|x-a\|=\varepsilon\|x-a\|,\end{aligned}$$
que és el que volíem provar. Per tant, demostrem ara l'Afirmació anterior. Prenem $i\in\{1,2,\ldots,m\}$ qualsevol i vegem que $f_i$ és diferenciable a $x=a$. Cal provar que, fixat $\varepsilon>0$, existeix un $\delta=\delta(\varepsilon)>0$ tal que si $x\in\Omega$, $\|x-a\|<\delta$ aleshores
$$|f_i(x)-f_i(a)-Jf_i(a)(x-a)|<\varepsilon\|x-a\|,$$
per a $i=1,2\ldots,m$. La idea és aplicar, coordenada a coordenada, el teorema del valor mitjà (TVM) per a funcions d'una variable. (Nota: Sigui $f:[a,b]\to\mathbb{R}$ contínua a $[a,b]$ i derivable a $(a,b)$. Aleshores, existeix $\xi\in(a,b)$ tal que $f(b)-f(a)=f'(\xi)(b-a)$.) Del fet que $a\in\mathring{\Omega}$ es deriva que existeix un $\delta_0>0$ tal que $R(a,\delta_0):=(a_1-\delta_0,a_1+\delta_0)\times\cdots\times(a_n-\delta_0,a_n+\delta_0)\subseteq\Omega$. Aleshores, per a valors de $x\in R(a,\delta_0)$, podem escriure
$$\begin{aligned}f_i(x)-f_i(a)&=f_i(x_1,x_2,x_3,\ldots,x_n)-f_i(a_1,a_2,a_3,\ldots,a_n)\\&=f_i(x_1,x_2,x_3,x_4,\ldots,x_n)-f_i(a_1,x_2,x_3,x_4,\ldots,x_n)\\&\quad+f_i(a_1,x_2,x_3,x_4,\ldots,x_n)-f_i(a_1,a_2,x_3,x_4,\ldots,x_n)\\&\quad+f_i(a_1,a_2,x_3,x_3,\ldots,x_n)-f_i(a_1,a_2,a_3,x_4,\ldots,x_n)\\&\quad+\cdots\\&\quad+f_i(a_1,a_2,\ldots,a_{n-1},x_n)-f_i(a_1,a_2,\ldots,a_{n-1},a_n)\\&\overset{\text{TVM}}{=}\frac{\partial f_i}{\partial x_1}(\xi_1,x_2,x_3,x_4,\ldots,x_n)(x_1-a_1)\\&\quad+\frac{\partial f_i}{\partial x_2}(a_1,\xi_2,x_3,x_4,\ldots,x_n)(x_2-a_2)\\&\quad+\frac{\partial f_i}{\partial x_3}(a_1,a_2,\xi_3,x_4,\ldots,x_n)(x_3-a_3)\\&\quad+\cdots\\&\quad+\frac{\partial f_i}{\partial x_n}(a_1,a_2,\ldots,a_{n-1},\xi_n)(x_n-a_n),\end{aligned}$$
on cada $\xi_j$, $j=1,2,\ldots,n$ pertany a l'interior del mínim interval (a $\mathbb{R}$) que conté $x_j$ i $a_j$ i, per tant a $R(a,\delta_0)$. En particular, això implica que $x_j$ tendeix a $a_j$, aleshores $\xi_j$ tendeix a $a_j$. Així doncs, si denotem $(a_{<j},\xi_j,x_{>j}):=(a_1,a_2,\ldots,a_{j-1},\xi_j,x_{j+1},\ldots,x_n)$, (Nota: Entenent que $a_{<1}=\emptyset$ i $x_{>n}=\emptyset$) tenim que
$$\begin{aligned}&|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\\&=\left|\sum_{j=1}^n\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})(x_j-a_j)-\sum_{j=1}^n\frac{\partial f_i}{\partial x_j}(a)(x_j-a_j)\right|\\&\leq\sum_{j=1}^n\left|\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right|\,|x_j-a_j|\,.\end{aligned}$$
De la continuïtat de les derivades parcials al punt $a$, es dedueix que existeix un $0<\delta_0'<\delta_0$, prou petit, tal que $R(a,\delta_0'):=(a_1-\delta_0',a_1+\delta_0')\times\cdots\times(a_n-\delta_0',a_n+\delta_0')\subseteq\Omega$ de manera que $\xi_j\in(a_j-\delta_0',a_j+\delta_0')$ per a tot $j\in\{1,2,\ldots,n\}$ i, a més, que
$$\sum_{j=1}^n\left|\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right|\,|x_j-a_j|<\varepsilon\|x-a\|,$$
per a tot $x\in R(a,\delta_0')$. En particular, verificant que
$$|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\varepsilon\|x-a\|$$
si $\|x-a\|<\delta_0'$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, i sigui $a\in\mathring{\Omega}$.
[2] (enunciat) Aleshores, $f$ és diferenciable al punt $a$ si i només si existeixen totes les derivades parcials $\frac{\partial f_i}{\partial x_j}$ en un entorn del punt $a$ i són contínues al punt $a$.
[3] (demostració) Recordem que a $\mathbb{R}^m$ totes les normes són equivalents; en particular, existeix $\mu>0$ tal que $\|y\|=\|y\|_2\leq\mu\|y\|_1$ per a tot $y\in\mathbb{R}^m$.
[4] (demostració) Reduirem la demostració a l'Afirmació següent: totes les funcions component $f_i$, $i=1,\ldots,m$, són diferenciables al punt $a$, amb $Jf_i(a)=\left(\frac{\partial f_i}{\partial x_1}(a)\ \cdots\ \frac{\partial f_i}{\partial x_n}(a)\right)$.
[5] (demostració) Suposem-la certa. Fixat $\varepsilon>0$, per a cada $i$ existeix $\delta_i>0$ tal que si $\|x-a\|<\delta_i$, aleshores $|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\frac{\varepsilon}{\mu m}\|x-a\|$.
[6] (demostració) Per tant, si $\|x-a\|<\delta:=\min_i\delta_i$, es té $\|f(x)-f(a)-Jf(a)(x-a)\|\leq\mu\sum_{i=1}^m|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\mu\sum_{i=1}^m\frac{\varepsilon}{\mu m}\|x-a\|=\varepsilon\|x-a\|$, i $f$ és diferenciable en $a$.
[7] (demostració) Demostrem l'Afirmació. Fixem $i$ i $\varepsilon>0$. Com que $a\in\mathring{\Omega}$ i les derivades parcials existeixen en un entorn de $a$, hi ha $\delta_0>0$ tal que el cub $R(a,\delta_0)=(a_1-\delta_0,a_1+\delta_0)\times\cdots\times(a_n-\delta_0,a_n+\delta_0)$ està contingut a $\Omega$ i totes les derivades parcials hi existeixen.
[8] (demostració) Per a $x\in R(a,\delta_0)$ escrivim $f_i(x)-f_i(a)$ com a suma telescòpica, canviant una coordenada cada vegada: $f_i(x)-f_i(a)=\sum_{j=1}^n\left[f_i(a_{<j},x_j,x_{>j})-f_i(a_{<j},a_j,x_{>j})\right]$, on $(a_{<j},t,x_{>j}):=(a_1,\ldots,a_{j-1},t,x_{j+1},\ldots,x_n)$.
[9] (demostració) Cada sumand és l'increment de la funció d'una variable $t\mapsto f_i(a_{<j},t,x_{>j})$, que és derivable, amb derivada $\frac{\partial f_i}{\partial x_j}(a_{<j},t,x_{>j})$, a l'interval tancat d'extrems $a_j$ i $x_j$. Pel teorema del valor mitjà en una variable, existeix $\xi_j$ a l'interior d'aquest interval tal que el sumand val $\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})\,(x_j-a_j)$ (si $x_j=a_j$, el sumand és nul).
[10] (demostració) Per tant, $|f_i(x)-f_i(a)-Jf_i(a)(x-a)|=\left|\sum_{j=1}^n\left(\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right)(x_j-a_j)\right|\leq\sum_{j=1}^n\left|\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right|\,|x_j-a_j|$.
[11] (demostració) Per la continuïtat de les derivades parcials al punt $a$, existeix $0<\delta_0'<\delta_0$ tal que $\left|\frac{\partial f_i}{\partial x_j}(p)-\frac{\partial f_i}{\partial x_j}(a)\right|<\frac{\varepsilon}{n}$ per a tot $p\in R(a,\delta_0')$ i tot $j$. Si $\|x-a\|<\delta_0'$, els punts $(a_{<j},\xi_j,x_{>j})$ pertanyen a $R(a,\delta_0')$, perquè cada coordenada dista de la de $a$ com a molt $\|x-a\|$.
[12] (demostració) Com que $|x_j-a_j|\leq\|x-a\|$, si $\|x-a\|<\delta_0'$ obtenim $|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\sum_{j=1}^n\frac{\varepsilon}{n}\|x-a\|=\varepsilon\|x-a\|$, que prova l'Afirmació.


## T3.18:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.
Demostració: Primer, recordem que a $\mathbb{R}^n$ totes les normes són equivalents. En particular, existeix $\mu>0$ de manera que $\|x\|=\|x\|_2\leq\mu\|x\|_1$.

Reduirem la demostració a provar que totes les funcions component $f_i$ ($i=1,2,\ldots,m$) són diferenciables al punt $a$. Suposem que el següent resultat és cert.

Afirmació. Totes les funcions component de $f$, o sigui $f_i$, per a $i=1,2,\ldots,m$, són diferenciables al punt $x=a$.

Si aquesta afirmació és certa, llavors $f$ és diferenciable al punt $x=a$. En efecte, fixat $\varepsilon>0$, sabem que existeix $\delta_i>0$ de manera que si $\|x-a\|<\delta_i$ aleshores
$$|f_i(x)-f_i(a)-Jf_i(a)(x-a)|<\frac{\varepsilon}{\mu m}\|x-a\|,$$
per a $i=1,2,\ldots,m$ i on
$$Jf_i(a)=Df_i(a)=\left(\frac{\partial f_i}{\partial x_1}(a)\ \ \frac{\partial f_i}{\partial x_2}(a)\ \ \cdots\ \ \frac{\partial f_i}{\partial x_n}(a)\right).$$
En conseqüència, si $\|x-a\|<\delta<\min_{i\in\{1,2,\ldots,m\}}\delta_i$, es dedueix que
$$\begin{aligned}\|f(x)-f(a)-Jf(a)(x-a)\|&\leq\mu\|f(x)-f(a)-Jf(a)(x-a)\|_1\\&=\mu\sum_{i=1}^m|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\mu\sum_{i=1}^m\frac{\varepsilon}{\mu m}\|x-a\|=\varepsilon\|x-a\|,\end{aligned}$$
que és el que volíem provar. Per tant, demostrem ara l'Afirmació anterior. Prenem $i\in\{1,2,\ldots,m\}$ qualsevol i vegem que $f_i$ és diferenciable a $x=a$. Cal provar que, fixat $\varepsilon>0$, existeix un $\delta=\delta(\varepsilon)>0$ tal que si $x\in\Omega$, $\|x-a\|<\delta$ aleshores
$$|f_i(x)-f_i(a)-Jf_i(a)(x-a)|<\varepsilon\|x-a\|,$$
per a $i=1,2\ldots,m$. La idea és aplicar, coordenada a coordenada, el teorema del valor mitjà (TVM) per a funcions d'una variable. (Nota: Sigui $f:[a,b]\to\mathbb{R}$ contínua a $[a,b]$ i derivable a $(a,b)$. Aleshores, existeix $\xi\in(a,b)$ tal que $f(b)-f(a)=f'(\xi)(b-a)$.) Del fet que $a\in\mathring{\Omega}$ es deriva que existeix un $\delta_0>0$ tal que $R(a,\delta_0):=(a_1-\delta_0,a_1+\delta_0)\times\cdots\times(a_n-\delta_0,a_n+\delta_0)\subseteq\Omega$. Aleshores, per a valors de $x\in R(a,\delta_0)$, podem escriure
$$\begin{aligned}f_i(x)-f_i(a)&=f_i(x_1,x_2,x_3,\ldots,x_n)-f_i(a_1,a_2,a_3,\ldots,a_n)\\&=f_i(x_1,x_2,x_3,x_4,\ldots,x_n)-f_i(a_1,x_2,x_3,x_4,\ldots,x_n)\\&\quad+f_i(a_1,x_2,x_3,x_4,\ldots,x_n)-f_i(a_1,a_2,x_3,x_4,\ldots,x_n)\\&\quad+f_i(a_1,a_2,x_3,x_3,\ldots,x_n)-f_i(a_1,a_2,a_3,x_4,\ldots,x_n)\\&\quad+\cdots\\&\quad+f_i(a_1,a_2,\ldots,a_{n-1},x_n)-f_i(a_1,a_2,\ldots,a_{n-1},a_n)\\&\overset{\text{TVM}}{=}\frac{\partial f_i}{\partial x_1}(\xi_1,x_2,x_3,x_4,\ldots,x_n)(x_1-a_1)\\&\quad+\frac{\partial f_i}{\partial x_2}(a_1,\xi_2,x_3,x_4,\ldots,x_n)(x_2-a_2)\\&\quad+\frac{\partial f_i}{\partial x_3}(a_1,a_2,\xi_3,x_4,\ldots,x_n)(x_3-a_3)\\&\quad+\cdots\\&\quad+\frac{\partial f_i}{\partial x_n}(a_1,a_2,\ldots,a_{n-1},\xi_n)(x_n-a_n),\end{aligned}$$
on cada $\xi_j$, $j=1,2,\ldots,n$ pertany a l'interior del mínim interval (a $\mathbb{R}$) que conté $x_j$ i $a_j$ i, per tant a $R(a,\delta_0)$. En particular, això implica que $x_j$ tendeix a $a_j$, aleshores $\xi_j$ tendeix a $a_j$. Així doncs, si denotem $(a_{<j},\xi_j,x_{>j}):=(a_1,a_2,\ldots,a_{j-1},\xi_j,x_{j+1},\ldots,x_n)$, (Nota: Entenent que $a_{<1}=\emptyset$ i $x_{>n}=\emptyset$) tenim que
$$\begin{aligned}&|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\\&=\left|\sum_{j=1}^n\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})(x_j-a_j)-\sum_{j=1}^n\frac{\partial f_i}{\partial x_j}(a)(x_j-a_j)\right|\\&\leq\sum_{j=1}^n\left|\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right|\,|x_j-a_j|\,.\end{aligned}$$
De la continuïtat de les derivades parcials al punt $a$, es dedueix que existeix un $0<\delta_0'<\delta_0$, prou petit, tal que $R(a,\delta_0'):=(a_1-\delta_0',a_1+\delta_0')\times\cdots\times(a_n-\delta_0',a_n+\delta_0')\subseteq\Omega$ de manera que $\xi_j\in(a_j-\delta_0',a_j+\delta_0')$ per a tot $j\in\{1,2,\ldots,n\}$ i, a més, que
$$\sum_{j=1}^n\left|\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right|\,|x_j-a_j|<\varepsilon\|x-a\|,$$
per a tot $x\in R(a,\delta_0')$. En particular, verificant que
$$|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\varepsilon\|x-a\|$$
si $\|x-a\|<\delta_0'$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, i sigui $a\in\mathring{\Omega}$.
[2] (enunciat) Si existeixen totes les derivades parcials $\frac{\partial f_i}{\partial x_j}$ en un entorn del punt $a$ i són contínues al punt $a$, aleshores $f$ és diferenciable en tots els punts d'un entorn de $a$.
[3] (demostració) Recordem que a $\mathbb{R}^m$ totes les normes són equivalents; en particular, existeix $\mu>0$ tal que $\|y\|=\|y\|_2\leq\mu\|y\|_1$ per a tot $y\in\mathbb{R}^m$.
[4] (demostració) Reduirem la demostració a l'Afirmació següent: totes les funcions component $f_i$, $i=1,\ldots,m$, són diferenciables al punt $a$, amb $Jf_i(a)=\left(\frac{\partial f_i}{\partial x_1}(a)\ \cdots\ \frac{\partial f_i}{\partial x_n}(a)\right)$.
[5] (demostració) Suposem-la certa. Fixat $\varepsilon>0$, per a cada $i$ existeix $\delta_i>0$ tal que si $\|x-a\|<\delta_i$, aleshores $|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\frac{\varepsilon}{m}\|x-a\|$.
[6] (demostració) Per tant, si $\|x-a\|<\delta:=\min_i\delta_i$, es té $\|f(x)-f(a)-Jf(a)(x-a)\|\leq\mu\sum_{i=1}^m|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\mu\sum_{i=1}^m\frac{\varepsilon}{m}\|x-a\|=\varepsilon\|x-a\|$, i $f$ és diferenciable en $a$.
[7] (demostració) Demostrem l'Afirmació. Fixem $i$ i $\varepsilon>0$. Com que $a\in\mathring{\Omega}$ i les derivades parcials existeixen en un entorn de $a$, hi ha $\delta_0>0$ tal que el cub $R(a,\delta_0)=(a_1-\delta_0,a_1+\delta_0)\times\cdots\times(a_n-\delta_0,a_n+\delta_0)$ està contingut a $\Omega$ i totes les derivades parcials hi existeixen.
[8] (demostració) Per a $x\in R(a,\delta_0)$ escrivim $f_i(x)-f_i(a)$ com a suma telescòpica, canviant una coordenada cada vegada: $f_i(x)-f_i(a)=\sum_{j=1}^n\left[f_i(a_{<j},x_j,x_{>j})-f_i(a_{<j},a_j,x_{>j})\right]$, on $(a_{<j},t,x_{>j}):=(a_1,\ldots,a_{j-1},t,x_{j+1},\ldots,x_n)$.
[9] (demostració) Cada sumand és l'increment de la funció d'una variable $t\mapsto f_i(a_{<j},t,x_{>j})$, que és derivable, amb derivada $\frac{\partial f_i}{\partial x_j}(a_{<j},t,x_{>j})$, a l'interval tancat d'extrems $a_j$ i $x_j$. Pel teorema del valor mitjà en una variable, existeix $\xi_j$ a l'interior d'aquest interval tal que el sumand val $\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})\,(x_j-a_j)$ (si $x_j=a_j$, el sumand és nul).
[10] (demostració) Per tant, $|f_i(x)-f_i(a)-Jf_i(a)(x-a)|=\left|\sum_{j=1}^n\left(\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right)(x_j-a_j)\right|\leq\sum_{j=1}^n\left|\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right|\,|x_j-a_j|$.
[11] (demostració) Per la continuïtat de les derivades parcials al punt $a$, existeix $0<\delta_0'<\delta_0$ tal que $\left|\frac{\partial f_i}{\partial x_j}(p)-\frac{\partial f_i}{\partial x_j}(a)\right|<\frac{\varepsilon}{n}$ per a tot $p\in R(a,\delta_0')$ i tot $j$. Si $\|x-a\|<\delta_0'$, els punts $(a_{<j},\xi_j,x_{>j})$ pertanyen a $R(a,\delta_0')$, perquè cada coordenada dista de la de $a$ com a molt $\|x-a\|$.
[12] (demostració) Com que $|x_j-a_j|\leq\|x-a\|$, si $\|x-a\|<\delta_0'$ obtenim $|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\sum_{j=1}^n\frac{\varepsilon}{n}\|x-a\|=\varepsilon\|x-a\|$, que prova l'Afirmació.


## T3.18:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.
Demostració: Primer, recordem que a $\mathbb{R}^n$ totes les normes són equivalents. En particular, existeix $\mu>0$ de manera que $\|x\|=\|x\|_2\leq\mu\|x\|_1$.

Reduirem la demostració a provar que totes les funcions component $f_i$ ($i=1,2,\ldots,m$) són diferenciables al punt $a$. Suposem que el següent resultat és cert.

Afirmació. Totes les funcions component de $f$, o sigui $f_i$, per a $i=1,2,\ldots,m$, són diferenciables al punt $x=a$.

Si aquesta afirmació és certa, llavors $f$ és diferenciable al punt $x=a$. En efecte, fixat $\varepsilon>0$, sabem que existeix $\delta_i>0$ de manera que si $\|x-a\|<\delta_i$ aleshores
$$|f_i(x)-f_i(a)-Jf_i(a)(x-a)|<\frac{\varepsilon}{\mu m}\|x-a\|,$$
per a $i=1,2,\ldots,m$ i on
$$Jf_i(a)=Df_i(a)=\left(\frac{\partial f_i}{\partial x_1}(a)\ \ \frac{\partial f_i}{\partial x_2}(a)\ \ \cdots\ \ \frac{\partial f_i}{\partial x_n}(a)\right).$$
En conseqüència, si $\|x-a\|<\delta<\min_{i\in\{1,2,\ldots,m\}}\delta_i$, es dedueix que
$$\begin{aligned}\|f(x)-f(a)-Jf(a)(x-a)\|&\leq\mu\|f(x)-f(a)-Jf(a)(x-a)\|_1\\&=\mu\sum_{i=1}^m|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\mu\sum_{i=1}^m\frac{\varepsilon}{\mu m}\|x-a\|=\varepsilon\|x-a\|,\end{aligned}$$
que és el que volíem provar. Per tant, demostrem ara l'Afirmació anterior. Prenem $i\in\{1,2,\ldots,m\}$ qualsevol i vegem que $f_i$ és diferenciable a $x=a$. Cal provar que, fixat $\varepsilon>0$, existeix un $\delta=\delta(\varepsilon)>0$ tal que si $x\in\Omega$, $\|x-a\|<\delta$ aleshores
$$|f_i(x)-f_i(a)-Jf_i(a)(x-a)|<\varepsilon\|x-a\|,$$
per a $i=1,2\ldots,m$. La idea és aplicar, coordenada a coordenada, el teorema del valor mitjà (TVM) per a funcions d'una variable. (Nota: Sigui $f:[a,b]\to\mathbb{R}$ contínua a $[a,b]$ i derivable a $(a,b)$. Aleshores, existeix $\xi\in(a,b)$ tal que $f(b)-f(a)=f'(\xi)(b-a)$.) Del fet que $a\in\mathring{\Omega}$ es deriva que existeix un $\delta_0>0$ tal que $R(a,\delta_0):=(a_1-\delta_0,a_1+\delta_0)\times\cdots\times(a_n-\delta_0,a_n+\delta_0)\subseteq\Omega$. Aleshores, per a valors de $x\in R(a,\delta_0)$, podem escriure
$$\begin{aligned}f_i(x)-f_i(a)&=f_i(x_1,x_2,x_3,\ldots,x_n)-f_i(a_1,a_2,a_3,\ldots,a_n)\\&=f_i(x_1,x_2,x_3,x_4,\ldots,x_n)-f_i(a_1,x_2,x_3,x_4,\ldots,x_n)\\&\quad+f_i(a_1,x_2,x_3,x_4,\ldots,x_n)-f_i(a_1,a_2,x_3,x_4,\ldots,x_n)\\&\quad+f_i(a_1,a_2,x_3,x_3,\ldots,x_n)-f_i(a_1,a_2,a_3,x_4,\ldots,x_n)\\&\quad+\cdots\\&\quad+f_i(a_1,a_2,\ldots,a_{n-1},x_n)-f_i(a_1,a_2,\ldots,a_{n-1},a_n)\\&\overset{\text{TVM}}{=}\frac{\partial f_i}{\partial x_1}(\xi_1,x_2,x_3,x_4,\ldots,x_n)(x_1-a_1)\\&\quad+\frac{\partial f_i}{\partial x_2}(a_1,\xi_2,x_3,x_4,\ldots,x_n)(x_2-a_2)\\&\quad+\frac{\partial f_i}{\partial x_3}(a_1,a_2,\xi_3,x_4,\ldots,x_n)(x_3-a_3)\\&\quad+\cdots\\&\quad+\frac{\partial f_i}{\partial x_n}(a_1,a_2,\ldots,a_{n-1},\xi_n)(x_n-a_n),\end{aligned}$$
on cada $\xi_j$, $j=1,2,\ldots,n$ pertany a l'interior del mínim interval (a $\mathbb{R}$) que conté $x_j$ i $a_j$ i, per tant a $R(a,\delta_0)$. En particular, això implica que $x_j$ tendeix a $a_j$, aleshores $\xi_j$ tendeix a $a_j$. Així doncs, si denotem $(a_{<j},\xi_j,x_{>j}):=(a_1,a_2,\ldots,a_{j-1},\xi_j,x_{j+1},\ldots,x_n)$, (Nota: Entenent que $a_{<1}=\emptyset$ i $x_{>n}=\emptyset$) tenim que
$$\begin{aligned}&|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\\&=\left|\sum_{j=1}^n\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})(x_j-a_j)-\sum_{j=1}^n\frac{\partial f_i}{\partial x_j}(a)(x_j-a_j)\right|\\&\leq\sum_{j=1}^n\left|\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right|\,|x_j-a_j|\,.\end{aligned}$$
De la continuïtat de les derivades parcials al punt $a$, es dedueix que existeix un $0<\delta_0'<\delta_0$, prou petit, tal que $R(a,\delta_0'):=(a_1-\delta_0',a_1+\delta_0')\times\cdots\times(a_n-\delta_0',a_n+\delta_0')\subseteq\Omega$ de manera que $\xi_j\in(a_j-\delta_0',a_j+\delta_0')$ per a tot $j\in\{1,2,\ldots,n\}$ i, a més, que
$$\sum_{j=1}^n\left|\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right|\,|x_j-a_j|<\varepsilon\|x-a\|,$$
per a tot $x\in R(a,\delta_0')$. En particular, verificant que
$$|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\varepsilon\|x-a\|$$
si $\|x-a\|<\delta_0'$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, i sigui $a\in\mathring{\Omega}$.
[2] (enunciat) Si existeixen totes les derivades parcials $\frac{\partial f_i}{\partial x_j}$ en un entorn del punt $a$ i són contínues al punt $a$, aleshores $f$ és diferenciable al punt $a$ i la seva matriu jacobiana és $Jf(a)=\left(\frac{\partial f_j}{\partial x_i}(a)\right)_{i,j}$, amb $1\leq i\leq n$ i $1\leq j\leq m$.
[3] (demostració) Recordem que a $\mathbb{R}^m$ totes les normes són equivalents; en particular, existeix $\mu>0$ tal que $\|y\|=\|y\|_2\leq\mu\|y\|_1$ per a tot $y\in\mathbb{R}^m$.
[4] (demostració) Reduirem la demostració a l'Afirmació següent: totes les funcions component $f_i$, $i=1,\ldots,m$, són diferenciables al punt $a$, amb $Jf_i(a)=\left(\frac{\partial f_i}{\partial x_1}(a)\ \cdots\ \frac{\partial f_i}{\partial x_n}(a)\right)$.
[5] (demostració) Suposem-la certa. Fixat $\varepsilon>0$, per a cada $i$ existeix $\delta_i>0$ tal que si $\|x-a\|<\delta_i$, aleshores $|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\frac{\varepsilon}{\mu m}\|x-a\|$.
[6] (demostració) Per tant, si $\|x-a\|<\delta:=\min_i\delta_i$, es té $\|f(x)-f(a)-Jf(a)(x-a)\|\leq\mu\sum_{i=1}^m|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\mu\sum_{i=1}^m\frac{\varepsilon}{\mu m}\|x-a\|=\varepsilon\|x-a\|$, i $f$ és diferenciable en $a$.
[7] (demostració) Demostrem l'Afirmació. Fixem $i$ i $\varepsilon>0$. Com que $a\in\mathring{\Omega}$ i les derivades parcials existeixen en un entorn de $a$, hi ha $\delta_0>0$ tal que el cub $R(a,\delta_0)=(a_1-\delta_0,a_1+\delta_0)\times\cdots\times(a_n-\delta_0,a_n+\delta_0)$ està contingut a $\Omega$ i totes les derivades parcials hi existeixen.
[8] (demostració) Per a $x\in R(a,\delta_0)$ escrivim $f_i(x)-f_i(a)$ com a suma telescòpica, canviant una coordenada cada vegada: $f_i(x)-f_i(a)=\sum_{j=1}^n\left[f_i(a_{<j},x_j,x_{>j})-f_i(a_{<j},a_j,x_{>j})\right]$, on $(a_{<j},t,x_{>j}):=(a_1,\ldots,a_{j-1},t,x_{j+1},\ldots,x_n)$.
[9] (demostració) Cada sumand és l'increment de la funció d'una variable $t\mapsto f_i(a_{<j},t,x_{>j})$, que és derivable a l'interval tancat d'extrems $a_j$ i $x_j$ perquè $f_i$ és diferenciable a $R(a,\delta_0)$. Pel teorema del valor mitjà en una variable, existeix $\xi_j$ a l'interior d'aquest interval tal que el sumand val $\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})\,(x_j-a_j)$ (si $x_j=a_j$, el sumand és nul).
[10] (demostració) Per tant, $|f_i(x)-f_i(a)-Jf_i(a)(x-a)|=\left|\sum_{j=1}^n\left(\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right)(x_j-a_j)\right|\leq\sum_{j=1}^n\left|\frac{\partial f_i}{\partial x_j}(a_{<j},\xi_j,x_{>j})-\frac{\partial f_i}{\partial x_j}(a)\right|\,|x_j-a_j|$.
[11] (demostració) Per la continuïtat de les derivades parcials al punt $a$, existeix $0<\delta_0'<\delta_0$ tal que $\left|\frac{\partial f_i}{\partial x_j}(p)-\frac{\partial f_i}{\partial x_j}(a)\right|<\varepsilon$ per a tot $p\in R(a,\delta_0')$ i tot $j$. Si $\|x-a\|<\delta_0'$, els punts $(a_{<j},\xi_j,x_{>j})$ pertanyen a $R(a,\delta_0')$, perquè cada coordenada dista de la de $a$ com a molt $\|x-a\|$.
[12] (demostració) Com que $\sum_{j=1}^n|x_j-a_j|=\|x-a\|_1\leq\|x-a\|$, si $\|x-a\|<\delta_0'$ obtenim $|f_i(x)-f_i(a)-Jf_i(a)(x-a)|\leq\varepsilon\sum_{j=1}^n|x_j-a_j|\leq\varepsilon\|x-a\|$, que prova l'Afirmació.


## T3.21:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$
Demostració: Que $f$ i $g$ siguin diferenciables als punts $a$ i $f(a)$, respectivament, equival a que $\forall\tilde\varepsilon>0$ fixat, $\exists\delta_1(\tilde\varepsilon),\delta_2(\tilde\varepsilon)$ positius, tals que

(a) $\forall x\in\Omega$ tal que $\|x-a\|<\delta_1(\tilde\varepsilon)$ aleshores $\|f(x)-f(a)-Jf(a)(x-a)\|<\tilde\varepsilon\|x-a\|$;

(b) $\forall y\in\Theta$ tal que $\|y-f(a)\|<\delta_2(\tilde\varepsilon)$ llavors
$$\|g(y)-g(f(a))-Jg(f(a))(y-f(a))\|<\tilde\varepsilon\|y-f(a)\|.$$

Per veure que $g\circ f$ és diferenciable al punt $a$, cal provar que, fixat $\varepsilon>0$ existeix un $\delta=\delta(\varepsilon)>0$ i una aplicació lineal $D(g\circ f)(a)$ de manera que si $\|x-a\|<\delta$, $x\in\Omega$, llavors
$$\|(g\circ f)(x)-(g\circ f)(a)-D(g\circ f)(a)(x-a)\|<\varepsilon\|x-a\|.$$
En primer lloc, per composició de les matrius jacobianes associades a $f$ al punt $a$ i a $g$ al punt $f(a)$, tenim que l'única candidata a matriu jacobiana associada a $D(g\circ f)(a)$ és $Jg(f(a))\cdot Jf(a)$. És a dir $J(g\circ f)(a)=Jg(f(a))\cdot Jf(a)$. Així, sumant i restant l'expressió $Jg(f(a))\,(f(x)-f(a))$, tenim que
$$\begin{aligned}&\|(g\circ f)(x)-(g\circ f)(a)-D(g\circ f)(a)(x-a)\|\\&=\|g(f(x))-g(f(a))-Jg(f(a))\cdot Jf(a)(x-a)\|\\&=\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))+Jg(f(a))\,(f(x)-f(a))\\&\quad-Jg(f(a))\cdot Jf(a)(x-a)\|\leq\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))\|\\&\quad+\left\|Jg(f(a))\big(f(x)-f(a)-Jf(a)(x-a)\big)\right\|\end{aligned}$$
Fitem cadascun d'aquests dos termes per separat.

- Respecte el primer terme,
$$\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))\|,$$
el fet que $f$ sigui diferenciable en $a$ implica que $f$ és puntualment localment Lipschitz en $a$ i, en conseqüència, existeixen $\delta_3>0$ i $M>0$ tal que per a tot $x\in\Omega$ satisfent que $\|x-a\|<\delta_3$ aleshores $\|f(x)-f(a)\|\leq M\|x-a\|$.
Per (b) tenim que fixat $\tilde\varepsilon$, existeix un $\delta_2(\tilde\varepsilon)>0$ de manera que per a tot $y\in\Theta$ tal que $\|y-f(a)\|<\delta_2\left(\frac{\varepsilon}{2M}\right)$, llavors
$$\|g(y)-g(f(a))-Jg(f(a))\,(y-f(a))\|\leq\frac{\varepsilon}{2M}\|y-f(a)\|.$$
Per tant, si prenem $\delta<\min\{\delta_3,\delta_2(\varepsilon/2M)\}$, es deriva que si $x\in\Omega$ amb $\|x-a\|<\delta$, aleshores
$$\begin{aligned}\|g(f(x))-g(f(a))&-Jg(f(a))\,(f(x)-f(a))\|\\&\leq\frac{\varepsilon}{2M}\|f(x)-f(a)\|\leq\frac{\varepsilon}{2M}M\|x-a\|=\frac{\varepsilon}{2}\|x-a\|.\end{aligned}\tag{11}$$

- Quant al segon terme, tenim que
$$\left\|Jg(f(a))\big(f(x)-f(a)-Jf(a)(x-a)\big)\right\|\leq\|Jg(f(a))\|\,\|f(x)-f(a)-Jf(a)(x-a)\|,$$
per a qualsevol norma matricial (que denotem, per abús de llenguatge, també per $\|\cdot\|$) consistent amb la norma vectorial $\|\cdot\|$. Tenint en compte (a), si prenem ara $\tilde\varepsilon=\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}$, aleshores existeix $\delta_1=\delta_1\left(\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}\right)$ de manera que si $x\in\Omega$ satisfà $\|x-a\|<\delta_1$, llavors (Nota: La raó d'usar el denominador $2(\|Jg(f(a))\|+1)$ en lloc de $2\|Jg(f(a))\|$ és per prevenir el cas en què $Jg(f(a))$ sigui la matriu de zeros i, per tant, $\|Jg(f(a))\|=0$.)
$$\|f(x)-f(a)-Jf(a)(x-a)\|\leq\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}\|x-a\|\leq\frac{\varepsilon}{2}\|x-a\|.$$
En conseqüència,
$$\|Jg(f(a))\,(f(x)-f(a)-Jf(a)(x-a))\|\leq\frac{\varepsilon\,\|Jg(f(a))\|}{2(\|Jg(f(a))\|+1)}\|x-a\|\leq\frac{\varepsilon}{2}\|x-a\|.\tag{12}$$
Per tant, si prenem $x\in\Omega$ tal que
$$\|x-a\|<\delta<\min\left\{\delta_3,\delta_2\left(\frac{\varepsilon}{2M}\right),\delta_1\left(\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}\right)\right\}$$
aleshores les expressions (11), (12) es satisfan i, en conseqüència,
$$\|(g\circ f)(x)-(g\circ f)(a)-D(g\circ f)(a)(x-a)\|<\varepsilon\|x-a\|,$$
que demostra que $g\circ f$ és diferenciable al punt $x=a$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$, i sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$.
[2] (enunciat) A més, $J(g\circ f)(a)=Jf(a)\cdot Jg(f(a))$, és a dir, per a tots $i=1,\ldots,p$ i $j=1,\ldots,n$, $\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a)$.
[3] (demostració) Que $f$ i $g$ siguin diferenciables en $a$ i $f(a)$, respectivament, vol dir que per a tot $\tilde\varepsilon>0$ existeixen $\delta_1(\tilde\varepsilon),\delta_2(\tilde\varepsilon)>0$ tals que: (a) si $x\in\Omega$ i $\|x-a\|<\delta_1(\tilde\varepsilon)$, aleshores $\|f(x)-f(a)-Jf(a)(x-a)\|\leq\tilde\varepsilon\|x-a\|$; (b) si $y\in\Theta$ i $\|y-f(a)\|<\delta_2(\tilde\varepsilon)$, aleshores $\|g(y)-g(f(a))-Jg(f(a))(y-f(a))\|\leq\tilde\varepsilon\|y-f(a)\|$.
[4] (demostració) Per composició de les jacobianes de $f$ en $a$ i de $g$ en $f(a)$, l'única candidata a matriu de $D(g\circ f)(a)$ és $Jg(f(a))\cdot Jf(a)$. Cal veure, doncs, que fixat $\varepsilon>0$ existeix $\delta>0$ tal que si $x\in\Omega$ i $\|x-a\|<\delta$, aleshores $\|g(f(x))-g(f(a))-Jg(f(a))\,Jf(a)(x-a)\|\leq\varepsilon\|x-a\|$.
[5] (demostració) Sumant i restant $Jg(f(a))\,(f(x)-f(a))$ i aplicant la desigualtat triangular, aquesta norma és menor o igual que $\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))\|+\|Jg(f(a))\big(f(x)-f(a)-Jf(a)(x-a)\big)\|$. Fitem cada terme per separat.
[6] (demostració) Primer terme. Com que $f$ és diferenciable en $a$, $f$ és puntualment localment Lipschitz en $a$: existeixen $\delta_3>0$ i $M>0$ tals que $\|f(x)-f(a)\|\leq M\|x-a\|$ per a tot $x\in\Omega$ amb $\|x-a\|<\delta_3$.
[7] (demostració) Apliquem (b) amb $\tilde\varepsilon=\frac{\varepsilon}{2M}$ i $y=f(x)\in\Theta$. Si $x\in\Omega$ i $\|x-a\|<\min\left\{\delta_3,\frac{1}{M}\delta_2\left(\frac{\varepsilon}{2M}\right)\right\}$, aleshores $\|f(x)-f(a)\|\leq M\|x-a\|<\delta_2\left(\frac{\varepsilon}{2M}\right)$ i, per tant, $\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))\|\leq\frac{\varepsilon}{2M}\|f(x)-f(a)\|\leq\frac{\varepsilon}{2}\|x-a\|$. (11)
[8] (demostració) Segon terme. Per a qualsevol norma matricial consistent amb la norma vectorial, $\|Jg(f(a))\big(f(x)-f(a)-Jf(a)(x-a)\big)\|\leq\|Jg(f(a))\|\,\|f(x)-f(a)-Jf(a)(x-a)\|$.
[9] (demostració) Apliquem (a) amb $\tilde\varepsilon=\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}$ (el $+1$ evita dividir per zero quan $Jg(f(a))$ és la matriu nul·la): si $x\in\Omega$ i $\|x-a\|<\delta_1(\tilde\varepsilon)$, el segon terme és menor o igual que $\frac{\varepsilon\,\|Jg(f(a))\|}{2(\|Jg(f(a))\|+1)}\|x-a\|\leq\frac{\varepsilon}{2}\|x-a\|$. (12)
[10] (demostració) Per tant, si $x\in\Omega$ i $\|x-a\|<\delta:=\min\left\{\delta_3,\frac{1}{M}\delta_2\left(\frac{\varepsilon}{2M}\right),\delta_1(\tilde\varepsilon)\right\}$, de (11) i (12) s'obté $\|(g\circ f)(x)-(g\circ f)(a)-Jg(f(a))\,Jf(a)(x-a)\|\leq\varepsilon\|x-a\|$, és a dir, $g\circ f$ és diferenciable en $a$ amb $J(g\circ f)(a)=Jg(f(a))\cdot Jf(a)$.


## T3.21:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$
Demostració: Que $f$ i $g$ siguin diferenciables als punts $a$ i $f(a)$, respectivament, equival a que $\forall\tilde\varepsilon>0$ fixat, $\exists\delta_1(\tilde\varepsilon),\delta_2(\tilde\varepsilon)$ positius, tals que

(a) $\forall x\in\Omega$ tal que $\|x-a\|<\delta_1(\tilde\varepsilon)$ aleshores $\|f(x)-f(a)-Jf(a)(x-a)\|<\tilde\varepsilon\|x-a\|$;

(b) $\forall y\in\Theta$ tal que $\|y-f(a)\|<\delta_2(\tilde\varepsilon)$ llavors
$$\|g(y)-g(f(a))-Jg(f(a))(y-f(a))\|<\tilde\varepsilon\|y-f(a)\|.$$

Per veure que $g\circ f$ és diferenciable al punt $a$, cal provar que, fixat $\varepsilon>0$ existeix un $\delta=\delta(\varepsilon)>0$ i una aplicació lineal $D(g\circ f)(a)$ de manera que si $\|x-a\|<\delta$, $x\in\Omega$, llavors
$$\|(g\circ f)(x)-(g\circ f)(a)-D(g\circ f)(a)(x-a)\|<\varepsilon\|x-a\|.$$
En primer lloc, per composició de les matrius jacobianes associades a $f$ al punt $a$ i a $g$ al punt $f(a)$, tenim que l'única candidata a matriu jacobiana associada a $D(g\circ f)(a)$ és $Jg(f(a))\cdot Jf(a)$. És a dir $J(g\circ f)(a)=Jg(f(a))\cdot Jf(a)$. Així, sumant i restant l'expressió $Jg(f(a))\,(f(x)-f(a))$, tenim que
$$\begin{aligned}&\|(g\circ f)(x)-(g\circ f)(a)-D(g\circ f)(a)(x-a)\|\\&=\|g(f(x))-g(f(a))-Jg(f(a))\cdot Jf(a)(x-a)\|\\&=\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))+Jg(f(a))\,(f(x)-f(a))\\&\quad-Jg(f(a))\cdot Jf(a)(x-a)\|\leq\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))\|\\&\quad+\left\|Jg(f(a))\big(f(x)-f(a)-Jf(a)(x-a)\big)\right\|\end{aligned}$$
Fitem cadascun d'aquests dos termes per separat.

- Respecte el primer terme,
$$\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))\|,$$
el fet que $f$ sigui diferenciable en $a$ implica que $f$ és puntualment localment Lipschitz en $a$ i, en conseqüència, existeixen $\delta_3>0$ i $M>0$ tal que per a tot $x\in\Omega$ satisfent que $\|x-a\|<\delta_3$ aleshores $\|f(x)-f(a)\|\leq M\|x-a\|$.
Per (b) tenim que fixat $\tilde\varepsilon$, existeix un $\delta_2(\tilde\varepsilon)>0$ de manera que per a tot $y\in\Theta$ tal que $\|y-f(a)\|<\delta_2\left(\frac{\varepsilon}{2M}\right)$, llavors
$$\|g(y)-g(f(a))-Jg(f(a))\,(y-f(a))\|\leq\frac{\varepsilon}{2M}\|y-f(a)\|.$$
Per tant, si prenem $\delta<\min\{\delta_3,\delta_2(\varepsilon/2M)\}$, es deriva que si $x\in\Omega$ amb $\|x-a\|<\delta$, aleshores
$$\begin{aligned}\|g(f(x))-g(f(a))&-Jg(f(a))\,(f(x)-f(a))\|\\&\leq\frac{\varepsilon}{2M}\|f(x)-f(a)\|\leq\frac{\varepsilon}{2M}M\|x-a\|=\frac{\varepsilon}{2}\|x-a\|.\end{aligned}\tag{11}$$

- Quant al segon terme, tenim que
$$\left\|Jg(f(a))\big(f(x)-f(a)-Jf(a)(x-a)\big)\right\|\leq\|Jg(f(a))\|\,\|f(x)-f(a)-Jf(a)(x-a)\|,$$
per a qualsevol norma matricial (que denotem, per abús de llenguatge, també per $\|\cdot\|$) consistent amb la norma vectorial $\|\cdot\|$. Tenint en compte (a), si prenem ara $\tilde\varepsilon=\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}$, aleshores existeix $\delta_1=\delta_1\left(\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}\right)$ de manera que si $x\in\Omega$ satisfà $\|x-a\|<\delta_1$, llavors (Nota: La raó d'usar el denominador $2(\|Jg(f(a))\|+1)$ en lloc de $2\|Jg(f(a))\|$ és per prevenir el cas en què $Jg(f(a))$ sigui la matriu de zeros i, per tant, $\|Jg(f(a))\|=0$.)
$$\|f(x)-f(a)-Jf(a)(x-a)\|\leq\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}\|x-a\|\leq\frac{\varepsilon}{2}\|x-a\|.$$
En conseqüència,
$$\|Jg(f(a))\,(f(x)-f(a)-Jf(a)(x-a))\|\leq\frac{\varepsilon\,\|Jg(f(a))\|}{2(\|Jg(f(a))\|+1)}\|x-a\|\leq\frac{\varepsilon}{2}\|x-a\|.\tag{12}$$
Per tant, si prenem $x\in\Omega$ tal que
$$\|x-a\|<\delta<\min\left\{\delta_3,\delta_2\left(\frac{\varepsilon}{2M}\right),\delta_1\left(\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}\right)\right\}$$
aleshores les expressions (11), (12) es satisfan i, en conseqüència,
$$\|(g\circ f)(x)-(g\circ f)(a)-D(g\circ f)(a)(x-a)\|<\varepsilon\|x-a\|,$$
que demostra que $g\circ f$ és diferenciable al punt $x=a$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$, i sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores $g\circ f$ és diferenciable en $a$ si i només si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$.
[2] (enunciat) A més, $J(g\circ f)(a)=Jg(f(a))\cdot Jf(a)$, és a dir, per a tots $i=1,\ldots,p$ i $j=1,\ldots,n$, $\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a)$.
[3] (demostració) Que $f$ i $g$ siguin diferenciables en $a$ i $f(a)$, respectivament, vol dir que per a tot $\tilde\varepsilon>0$ existeixen $\delta_1(\tilde\varepsilon),\delta_2(\tilde\varepsilon)>0$ tals que: (a) si $x\in\Omega$ i $\|x-a\|<\delta_1(\tilde\varepsilon)$, aleshores $\|f(x)-f(a)-Jf(a)(x-a)\|\leq\tilde\varepsilon\|x-a\|$; (b) si $y\in\Theta$ i $\|y-f(a)\|<\delta_2(\tilde\varepsilon)$, aleshores $\|g(y)-g(f(a))-Jg(f(a))(y-f(a))\|\leq\tilde\varepsilon\|y-f(a)\|$.
[4] (demostració) Per composició de les jacobianes de $f$ en $a$ i de $g$ en $f(a)$, l'única candidata a matriu de $D(g\circ f)(a)$ és $Jg(f(a))\cdot Jf(a)$. Cal veure, doncs, que fixat $\varepsilon>0$ existeix $\delta>0$ tal que si $x\in\Omega$ i $\|x-a\|<\delta$, aleshores $\|g(f(x))-g(f(a))-Jg(f(a))\,Jf(a)(x-a)\|\leq\varepsilon\|x-a\|$.
[5] (demostració) Sumant i restant $Jg(f(a))\,(f(x)-f(a))$ i aplicant la desigualtat triangular, aquesta norma és menor o igual que $\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))\|+\|Jg(f(a))\big(f(x)-f(a)-Jf(a)(x-a)\big)\|$. Fitem cada terme per separat.
[6] (demostració) Primer terme. Com que $f$ és diferenciable en $a$, $f$ és puntualment localment Lipschitz en $a$: existeixen $\delta_3>0$ i $M>0$ tals que $\|f(x)-f(a)\|\leq M\|x-a\|$ per a tot $x\in\Omega$ amb $\|x-a\|<\delta_3$.
[7] (demostració) Apliquem (b) amb $\tilde\varepsilon=\frac{\varepsilon}{2M}$ i $y=f(x)\in\Theta$. Si $x\in\Omega$ i $\|x-a\|<\min\left\{\delta_3,\frac{1}{M}\delta_2\left(\frac{\varepsilon}{2M}\right)\right\}$, aleshores $\|f(x)-f(a)\|\leq M\|x-a\|<\delta_2\left(\frac{\varepsilon}{2M}\right)$ i, per tant, $\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))\|\leq\frac{\varepsilon}{2M}\|f(x)-f(a)\|\leq\frac{\varepsilon}{2}\|x-a\|$. (11)
[8] (demostració) Segon terme. Per a qualsevol norma matricial consistent amb la norma vectorial, $\|Jg(f(a))\big(f(x)-f(a)-Jf(a)(x-a)\big)\|\leq\|Jg(f(a))\|\,\|f(x)-f(a)-Jf(a)(x-a)\|$.
[9] (demostració) Apliquem (a) amb $\tilde\varepsilon=\frac{\varepsilon}{2\|Jg(f(a))\|}$: si $x\in\Omega$ i $\|x-a\|<\delta_1(\tilde\varepsilon)$, el segon terme és menor o igual que $\|Jg(f(a))\|\,\frac{\varepsilon}{2\|Jg(f(a))\|}\|x-a\|=\frac{\varepsilon}{2}\|x-a\|$. (12)
[10] (demostració) Per tant, si $x\in\Omega$ i $\|x-a\|<\delta:=\min\left\{\delta_3,\frac{1}{M}\delta_2\left(\frac{\varepsilon}{2M}\right),\delta_1(\tilde\varepsilon)\right\}$, de (11) i (12) s'obté $\|(g\circ f)(x)-(g\circ f)(a)-Jg(f(a))\,Jf(a)(x-a)\|\leq\varepsilon\|x-a\|$, és a dir, $g\circ f$ és diferenciable en $a$ amb $J(g\circ f)(a)=Jg(f(a))\cdot Jf(a)$.


## T3.21:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.21] Teorema 21 (Tema 3) — Regla de la cadena
Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$. Sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Aleshores, si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$. A més,
$$J(g\circ f)(a)=Jg(f(a))\cdot Jf(a),$$
és a dir, $\forall i=1,2,\ldots,p$, $\forall j=1,2,\ldots,n$ es té
$$\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^m\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a).\tag{10}$$
Demostració: Que $f$ i $g$ siguin diferenciables als punts $a$ i $f(a)$, respectivament, equival a que $\forall\tilde\varepsilon>0$ fixat, $\exists\delta_1(\tilde\varepsilon),\delta_2(\tilde\varepsilon)$ positius, tals que

(a) $\forall x\in\Omega$ tal que $\|x-a\|<\delta_1(\tilde\varepsilon)$ aleshores $\|f(x)-f(a)-Jf(a)(x-a)\|<\tilde\varepsilon\|x-a\|$;

(b) $\forall y\in\Theta$ tal que $\|y-f(a)\|<\delta_2(\tilde\varepsilon)$ llavors
$$\|g(y)-g(f(a))-Jg(f(a))(y-f(a))\|<\tilde\varepsilon\|y-f(a)\|.$$

Per veure que $g\circ f$ és diferenciable al punt $a$, cal provar que, fixat $\varepsilon>0$ existeix un $\delta=\delta(\varepsilon)>0$ i una aplicació lineal $D(g\circ f)(a)$ de manera que si $\|x-a\|<\delta$, $x\in\Omega$, llavors
$$\|(g\circ f)(x)-(g\circ f)(a)-D(g\circ f)(a)(x-a)\|<\varepsilon\|x-a\|.$$
En primer lloc, per composició de les matrius jacobianes associades a $f$ al punt $a$ i a $g$ al punt $f(a)$, tenim que l'única candidata a matriu jacobiana associada a $D(g\circ f)(a)$ és $Jg(f(a))\cdot Jf(a)$. És a dir $J(g\circ f)(a)=Jg(f(a))\cdot Jf(a)$. Així, sumant i restant l'expressió $Jg(f(a))\,(f(x)-f(a))$, tenim que
$$\begin{aligned}&\|(g\circ f)(x)-(g\circ f)(a)-D(g\circ f)(a)(x-a)\|\\&=\|g(f(x))-g(f(a))-Jg(f(a))\cdot Jf(a)(x-a)\|\\&=\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))+Jg(f(a))\,(f(x)-f(a))\\&\quad-Jg(f(a))\cdot Jf(a)(x-a)\|\leq\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))\|\\&\quad+\left\|Jg(f(a))\big(f(x)-f(a)-Jf(a)(x-a)\big)\right\|\end{aligned}$$
Fitem cadascun d'aquests dos termes per separat.

- Respecte el primer terme,
$$\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))\|,$$
el fet que $f$ sigui diferenciable en $a$ implica que $f$ és puntualment localment Lipschitz en $a$ i, en conseqüència, existeixen $\delta_3>0$ i $M>0$ tal que per a tot $x\in\Omega$ satisfent que $\|x-a\|<\delta_3$ aleshores $\|f(x)-f(a)\|\leq M\|x-a\|$.
Per (b) tenim que fixat $\tilde\varepsilon$, existeix un $\delta_2(\tilde\varepsilon)>0$ de manera que per a tot $y\in\Theta$ tal que $\|y-f(a)\|<\delta_2\left(\frac{\varepsilon}{2M}\right)$, llavors
$$\|g(y)-g(f(a))-Jg(f(a))\,(y-f(a))\|\leq\frac{\varepsilon}{2M}\|y-f(a)\|.$$
Per tant, si prenem $\delta<\min\{\delta_3,\delta_2(\varepsilon/2M)\}$, es deriva que si $x\in\Omega$ amb $\|x-a\|<\delta$, aleshores
$$\begin{aligned}\|g(f(x))-g(f(a))&-Jg(f(a))\,(f(x)-f(a))\|\\&\leq\frac{\varepsilon}{2M}\|f(x)-f(a)\|\leq\frac{\varepsilon}{2M}M\|x-a\|=\frac{\varepsilon}{2}\|x-a\|.\end{aligned}\tag{11}$$

- Quant al segon terme, tenim que
$$\left\|Jg(f(a))\big(f(x)-f(a)-Jf(a)(x-a)\big)\right\|\leq\|Jg(f(a))\|\,\|f(x)-f(a)-Jf(a)(x-a)\|,$$
per a qualsevol norma matricial (que denotem, per abús de llenguatge, també per $\|\cdot\|$) consistent amb la norma vectorial $\|\cdot\|$. Tenint en compte (a), si prenem ara $\tilde\varepsilon=\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}$, aleshores existeix $\delta_1=\delta_1\left(\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}\right)$ de manera que si $x\in\Omega$ satisfà $\|x-a\|<\delta_1$, llavors (Nota: La raó d'usar el denominador $2(\|Jg(f(a))\|+1)$ en lloc de $2\|Jg(f(a))\|$ és per prevenir el cas en què $Jg(f(a))$ sigui la matriu de zeros i, per tant, $\|Jg(f(a))\|=0$.)
$$\|f(x)-f(a)-Jf(a)(x-a)\|\leq\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}\|x-a\|\leq\frac{\varepsilon}{2}\|x-a\|.$$
En conseqüència,
$$\|Jg(f(a))\,(f(x)-f(a)-Jf(a)(x-a))\|\leq\frac{\varepsilon\,\|Jg(f(a))\|}{2(\|Jg(f(a))\|+1)}\|x-a\|\leq\frac{\varepsilon}{2}\|x-a\|.\tag{12}$$
Per tant, si prenem $x\in\Omega$ tal que
$$\|x-a\|<\delta<\min\left\{\delta_3,\delta_2\left(\frac{\varepsilon}{2M}\right),\delta_1\left(\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}\right)\right\}$$
aleshores les expressions (11), (12) es satisfan i, en conseqüència,
$$\|(g\circ f)(x)-(g\circ f)(a)-D(g\circ f)(a)(x-a)\|<\varepsilon\|x-a\|,$$
que demostra que $g\circ f$ és diferenciable al punt $x=a$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Siguin $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $g:\Theta\subseteq\mathbb{R}^m\to\mathbb{R}^p$, amb $f(\Omega)\subseteq\Theta$, i sigui $a\in\mathring{\Omega}$ tal que $f(a)\in\mathring{\Theta}$. Si $f$ és diferenciable en $a$ i $g$ és diferenciable en $f(a)$, llavors $g\circ f$ és diferenciable en $a$.
[2] (enunciat) A més, $J(g\circ f)(a)=Jg(f(a))\cdot Jf(a)$, és a dir, per a tots $i=1,\ldots,p$ i $j=1,\ldots,n$, $\frac{\partial(g\circ f)_i}{\partial x_j}(a)=\sum_{\ell=1}^n\frac{\partial g_i}{\partial x_\ell}(f(a))\cdot\frac{\partial f_\ell}{\partial x_j}(a)$.
[3] (demostració) Que $f$ i $g$ siguin diferenciables en $a$ i $f(a)$, respectivament, vol dir que per a tot $\tilde\varepsilon>0$ existeixen $\delta_1(\tilde\varepsilon),\delta_2(\tilde\varepsilon)>0$ tals que: (a) si $x\in\Omega$ i $\|x-a\|<\delta_1(\tilde\varepsilon)$, aleshores $\|f(x)-f(a)-Jf(a)(x-a)\|\leq\tilde\varepsilon\|x-a\|$; (b) si $y\in\Theta$ i $\|y-f(a)\|<\delta_2(\tilde\varepsilon)$, aleshores $\|g(y)-g(f(a))-Jg(f(a))(y-f(a))\|\leq\tilde\varepsilon\|y-f(a)\|$.
[4] (demostració) Per composició de les jacobianes de $f$ en $a$ i de $g$ en $f(a)$, l'única candidata a matriu de $D(g\circ f)(a)$ és $Jg(f(a))\cdot Jf(a)$. Cal veure, doncs, que fixat $\varepsilon>0$ existeix $\delta>0$ tal que si $x\in\Omega$ i $\|x-a\|<\delta$, aleshores $\|g(f(x))-g(f(a))-Jg(f(a))\,Jf(a)(x-a)\|\leq\varepsilon\|x-a\|$.
[5] (demostració) Sumant i restant $Jg(f(a))\,(f(x)-f(a))$ i aplicant la desigualtat triangular, aquesta norma és menor o igual que $\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))\|+\|Jg(f(a))\big(f(x)-f(a)+Jf(a)(x-a)\big)\|$. Fitem cada terme per separat.
[6] (demostració) Primer terme. Com que $f$ és contínua en $a$, $f$ és puntualment localment Lipschitz en $a$: existeixen $\delta_3>0$ i $M>0$ tals que $\|f(x)-f(a)\|\leq M\|x-a\|$ per a tot $x\in\Omega$ amb $\|x-a\|<\delta_3$.
[7] (demostració) Apliquem (b) amb $\tilde\varepsilon=\frac{\varepsilon}{2M}$ i $y=f(x)\in\Theta$. Si $x\in\Omega$ i $\|x-a\|<\min\left\{\delta_3,\frac{1}{M}\delta_2\left(\frac{\varepsilon}{2M}\right)\right\}$, aleshores $\|f(x)-f(a)\|\leq M\|x-a\|<\delta_2\left(\frac{\varepsilon}{2M}\right)$ i, per tant, $\|g(f(x))-g(f(a))-Jg(f(a))\,(f(x)-f(a))\|\leq\frac{\varepsilon}{2M}\|f(x)-f(a)\|\leq\frac{\varepsilon}{2}\|x-a\|$. (11)
[8] (demostració) Segon terme. Per a qualsevol norma matricial consistent amb la norma vectorial, $\|Jg(f(a))\big(f(x)-f(a)-Jf(a)(x-a)\big)\|\leq\|Jg(f(a))\|\,\|f(x)-f(a)-Jf(a)(x-a)\|$.
[9] (demostració) Apliquem (a) amb $\tilde\varepsilon=\frac{\varepsilon}{2(\|Jg(f(a))\|+1)}$ (el $+1$ evita dividir per zero quan $Jg(f(a))$ és la matriu nul·la): si $x\in\Omega$ i $\|x-a\|<\delta_1(\tilde\varepsilon)$, el segon terme és menor o igual que $\frac{\varepsilon\,\|Jg(f(a))\|}{2(\|Jg(f(a))\|+1)}\|x-a\|\leq\frac{\varepsilon}{2}\|x-a\|$. (12)
[10] (demostració) Per tant, si $x\in\Omega$ i $\|x-a\|<\delta:=\min\left\{\delta_3,\frac{1}{M}\delta_2\left(\frac{\varepsilon}{2M}\right),\delta_1(\tilde\varepsilon)\right\}$, de (11) i (12) s'obté $\|(g\circ f)(x)-(g\circ f)(a)-Jg(f(a))\,Jf(a)(x-a)\|\leq\varepsilon\|x-a\|$, és a dir, $g\circ f$ és diferenciable en $a$ amb $J(g\circ f)(a)=Jg(f(a))\cdot Jf(a)$.


## T3.25:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.25] Teorema 25 (Tema 3) — Teorema del valor mitjà
(Teorema del valor mitjà). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, diferenciable en un obert $\Omega\subseteq\mathbb{R}^n$. Sigui $u\in\mathbb{R}^m$. Aleshores, per a tot $a,b\in\Omega$ tals que $[a,b]\subseteq\Omega$ existeix $\xi\in(a,b)$ tal que
$$\langle u,f(b)-f(a)\rangle=\langle u,Jf(\xi)(b-a)\rangle.$$
Demostració: Considerem les següents funcions:
$$\begin{aligned}h:\ [0,1]&\longrightarrow\Omega\subseteq\mathbb{R}^n,&f:\ \Omega\subseteq\mathbb{R}^n&\longrightarrow\mathbb{R}^m,&g_u:\ \mathbb{R}^m&\longrightarrow\mathbb{R}.\\t&\longmapsto(1-t)a+tb&x&\longmapsto f(x)&y&\longmapsto\langle u,y\rangle\end{aligned}$$
Noteu que $(g_u\circ f\circ h)(t)=\langle u,f((1-t)a+tb)\rangle$ és una funció diferenciable (per composició; de fet, derivable) de $[0,1]$ a $\mathbb{R}$. Si apliquem el teorema del valor mitjà clàssic, tenim que existeix $\eta\in(0,1)$ de manera que
$$\langle u,f(b)-f(a)\rangle=g_u(f(h(1)))-g_u(f(h(0)))=(g_u\circ f\circ h)'(\eta)\,(1-0).$$
Calculem ara $(g_u\circ f\circ h)'(t)$. Aplicant la regla de la cadena,
$$(g_u\circ f\circ h)'(t)=\nabla g_u(f(h(t)))\cdot Jf(h(t))\cdot Jh(t),$$
es dedueix que
$$\begin{aligned}(g_u\circ f\circ h)'(\eta)&=(u_1\ \ u_2\ \ \ldots\ \ u_m)\cdot\left.\begin{pmatrix}\dfrac{\partial f_1}{\partial x_1}(x)&\cdots&\dfrac{\partial f_1}{\partial x_n}(x)\\\dfrac{\partial f_2}{\partial x_1}(x)&\cdots&\dfrac{\partial f_2}{\partial x_n}(x)\\\vdots&\ddots&\vdots\\\dfrac{\partial f_m}{\partial x_1}(x)&\cdots&\dfrac{\partial f_m}{\partial x_n}(x)\end{pmatrix}\right|_{x=h(\eta)}\cdot\begin{pmatrix}-a_1+b_1\\-a_2+b_2\\\vdots\\-a_n+b_n\end{pmatrix}\\&=\langle u,Jf(h(\eta))\,(b-a)\rangle=\langle u,Jf(\xi)\,(b-a)\rangle,\end{aligned}$$
on $\xi=h(\eta)\in[a,b]$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Teorema del valor mitjà). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ diferenciable en un obert $\Omega\subseteq\mathbb{R}^n$.
[2] (enunciat) Aleshores, per a tots $a,b\in\Omega$ tals que $[a,b]\subseteq\Omega$, existeix $\xi\in(a,b)$ tal que $f(b)-f(a)=Jf(\xi)\,(b-a)$.
[3] (demostració) Siguin $a,b\in\Omega$ amb $[a,b]\subseteq\Omega$ i sigui $u\in\mathbb{R}^m$. Considerem les funcions $h:[0,1]\to\Omega$, $h(t)=(1-t)a+tb$, i $g_u:\mathbb{R}^m\to\mathbb{R}$, $g_u(y)=\langle u,y\rangle$.
[4] (demostració) La funció $\varphi=g_u\circ f\circ h$, $\varphi(t)=\langle u,f((1-t)a+tb)\rangle$, és derivable a $[0,1]$ per composició de funcions diferenciables; en particular, és contínua a $[0,1]$ i derivable a $(0,1)$.
[5] (demostració) Pel teorema del valor mitjà clàssic, existeix $\eta\in(0,1)$ tal que $\langle u,f(b)-f(a)\rangle=\varphi(1)-\varphi(0)=\varphi'(\eta)\,(1-0)$.
[6] (demostració) Per la regla de la cadena, $\varphi'(t)=\nabla g_u(f(h(t)))\cdot Jf(h(t))\cdot Jh(t)$, on $\nabla g_u(y)=(u_1\ \cdots\ u_m)$ per a tot $y$ i $Jh(t)=b-a$, vist com a vector columna.
[7] (demostració) Per tant, $\varphi'(\eta)=(u_1\ \cdots\ u_m)\,Jf(h(\eta))\,(b-a)=\langle u,Jf(h(\eta))\,(b-a)\rangle$.
[8] (demostració) Prenent $\xi=h(\eta)$, que pertany a $(a,b)$ perquè $\eta\in(0,1)$, obtenim $\langle u,f(b)-f(a)\rangle=\langle u,Jf(\xi)\,(b-a)\rangle$.


## T3.25:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.25] Teorema 25 (Tema 3) — Teorema del valor mitjà
(Teorema del valor mitjà). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, diferenciable en un obert $\Omega\subseteq\mathbb{R}^n$. Sigui $u\in\mathbb{R}^m$. Aleshores, per a tot $a,b\in\Omega$ tals que $[a,b]\subseteq\Omega$ existeix $\xi\in(a,b)$ tal que
$$\langle u,f(b)-f(a)\rangle=\langle u,Jf(\xi)(b-a)\rangle.$$
Demostració: Considerem les següents funcions:
$$\begin{aligned}h:\ [0,1]&\longrightarrow\Omega\subseteq\mathbb{R}^n,&f:\ \Omega\subseteq\mathbb{R}^n&\longrightarrow\mathbb{R}^m,&g_u:\ \mathbb{R}^m&\longrightarrow\mathbb{R}.\\t&\longmapsto(1-t)a+tb&x&\longmapsto f(x)&y&\longmapsto\langle u,y\rangle\end{aligned}$$
Noteu que $(g_u\circ f\circ h)(t)=\langle u,f((1-t)a+tb)\rangle$ és una funció diferenciable (per composició; de fet, derivable) de $[0,1]$ a $\mathbb{R}$. Si apliquem el teorema del valor mitjà clàssic, tenim que existeix $\eta\in(0,1)$ de manera que
$$\langle u,f(b)-f(a)\rangle=g_u(f(h(1)))-g_u(f(h(0)))=(g_u\circ f\circ h)'(\eta)\,(1-0).$$
Calculem ara $(g_u\circ f\circ h)'(t)$. Aplicant la regla de la cadena,
$$(g_u\circ f\circ h)'(t)=\nabla g_u(f(h(t)))\cdot Jf(h(t))\cdot Jh(t),$$
es dedueix que
$$\begin{aligned}(g_u\circ f\circ h)'(\eta)&=(u_1\ \ u_2\ \ \ldots\ \ u_m)\cdot\left.\begin{pmatrix}\dfrac{\partial f_1}{\partial x_1}(x)&\cdots&\dfrac{\partial f_1}{\partial x_n}(x)\\\dfrac{\partial f_2}{\partial x_1}(x)&\cdots&\dfrac{\partial f_2}{\partial x_n}(x)\\\vdots&\ddots&\vdots\\\dfrac{\partial f_m}{\partial x_1}(x)&\cdots&\dfrac{\partial f_m}{\partial x_n}(x)\end{pmatrix}\right|_{x=h(\eta)}\cdot\begin{pmatrix}-a_1+b_1\\-a_2+b_2\\\vdots\\-a_n+b_n\end{pmatrix}\\&=\langle u,Jf(h(\eta))\,(b-a)\rangle=\langle u,Jf(\xi)\,(b-a)\rangle,\end{aligned}$$
on $\xi=h(\eta)\in[a,b]$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Teorema del valor mitjà). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ diferenciable en un obert $\Omega\subseteq\mathbb{R}^n$ i sigui $u\in\mathbb{R}^m$.
[2] (enunciat) Aleshores, per a tots $a,b\in\Omega$ tals que $[a,b]\subseteq\Omega$ i per a tot $\xi\in(a,b)$, es té $\langle u,f(b)-f(a)\rangle=\langle u,Jf(\xi)\,(b-a)\rangle$.
[3] (demostració) Siguin $a,b\in\Omega$ amb $[a,b]\subseteq\Omega$. Considerem les funcions $h:[0,1]\to\Omega$, $h(t)=(1-t)a+tb$, i $g_u:\mathbb{R}^m\to\mathbb{R}$, $g_u(y)=\langle u,y\rangle$.
[4] (demostració) La funció $\varphi=g_u\circ f\circ h$, $\varphi(t)=\langle u,f((1-t)a+tb)\rangle$, és derivable a $[0,1]$ per composició de funcions diferenciables; en particular, és contínua a $[0,1]$ i derivable a $(0,1)$.
[5] (demostració) Pel teorema del valor mitjà clàssic, existeix $\eta\in(0,1)$ tal que $\langle u,f(b)-f(a)\rangle=\varphi(1)-\varphi(0)=\varphi'(\eta)\,(1-0)$.
[6] (demostració) Per la regla de la cadena, $\varphi'(t)=\nabla g_u(f(h(t)))\cdot Jf(h(t))\cdot Jh(t)$, on $\nabla g_u(y)=(u_1\ \cdots\ u_m)$ per a tot $y$ i $Jh(t)=a-b$, vist com a vector columna.
[7] (demostració) Per tant, $\varphi'(\eta)=(u_1\ \cdots\ u_m)\,Jf(h(\eta))\,(b-a)=\langle u,Jf(h(\eta))\,(b-a)\rangle$.
[8] (demostració) Prenent $\xi=h(\eta)$, que pertany a $(a,b)$ perquè $\eta\in(0,1)$, obtenim $\langle u,f(b)-f(a)\rangle=\langle u,Jf(\xi)\,(b-a)\rangle$.


## T3.25:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.25] Teorema 25 (Tema 3) — Teorema del valor mitjà
(Teorema del valor mitjà). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, diferenciable en un obert $\Omega\subseteq\mathbb{R}^n$. Sigui $u\in\mathbb{R}^m$. Aleshores, per a tot $a,b\in\Omega$ tals que $[a,b]\subseteq\Omega$ existeix $\xi\in(a,b)$ tal que
$$\langle u,f(b)-f(a)\rangle=\langle u,Jf(\xi)(b-a)\rangle.$$
Demostració: Considerem les següents funcions:
$$\begin{aligned}h:\ [0,1]&\longrightarrow\Omega\subseteq\mathbb{R}^n,&f:\ \Omega\subseteq\mathbb{R}^n&\longrightarrow\mathbb{R}^m,&g_u:\ \mathbb{R}^m&\longrightarrow\mathbb{R}.\\t&\longmapsto(1-t)a+tb&x&\longmapsto f(x)&y&\longmapsto\langle u,y\rangle\end{aligned}$$
Noteu que $(g_u\circ f\circ h)(t)=\langle u,f((1-t)a+tb)\rangle$ és una funció diferenciable (per composició; de fet, derivable) de $[0,1]$ a $\mathbb{R}$. Si apliquem el teorema del valor mitjà clàssic, tenim que existeix $\eta\in(0,1)$ de manera que
$$\langle u,f(b)-f(a)\rangle=g_u(f(h(1)))-g_u(f(h(0)))=(g_u\circ f\circ h)'(\eta)\,(1-0).$$
Calculem ara $(g_u\circ f\circ h)'(t)$. Aplicant la regla de la cadena,
$$(g_u\circ f\circ h)'(t)=\nabla g_u(f(h(t)))\cdot Jf(h(t))\cdot Jh(t),$$
es dedueix que
$$\begin{aligned}(g_u\circ f\circ h)'(\eta)&=(u_1\ \ u_2\ \ \ldots\ \ u_m)\cdot\left.\begin{pmatrix}\dfrac{\partial f_1}{\partial x_1}(x)&\cdots&\dfrac{\partial f_1}{\partial x_n}(x)\\\dfrac{\partial f_2}{\partial x_1}(x)&\cdots&\dfrac{\partial f_2}{\partial x_n}(x)\\\vdots&\ddots&\vdots\\\dfrac{\partial f_m}{\partial x_1}(x)&\cdots&\dfrac{\partial f_m}{\partial x_n}(x)\end{pmatrix}\right|_{x=h(\eta)}\cdot\begin{pmatrix}-a_1+b_1\\-a_2+b_2\\\vdots\\-a_n+b_n\end{pmatrix}\\&=\langle u,Jf(h(\eta))\,(b-a)\rangle=\langle u,Jf(\xi)\,(b-a)\rangle,\end{aligned}$$
on $\xi=h(\eta)\in[a,b]$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Teorema del valor mitjà). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ diferenciable en un obert $\Omega\subseteq\mathbb{R}^n$ i sigui $u\in\mathbb{R}^m$.
[2] (enunciat) Aleshores, per a tots $a,b\in\Omega$ existeix $\xi\in(a,b)$ tal que $\langle u,f(b)-f(a)\rangle=\langle u,Jf(\xi)\,(b-a)\rangle$.
[3] (demostració) Siguin $a,b\in\Omega$ amb $[a,b]\subseteq\Omega$. Considerem les funcions $h:[0,1]\to\Omega$, $h(t)=(1-t)a+tb$, i $g_u:\mathbb{R}^m\to\mathbb{R}$, $g_u(y)=\langle u,y\rangle$.
[4] (demostració) La funció $\varphi=g_u\circ f\circ h$, $\varphi(t)=\langle u,f((1-t)a+tb)\rangle$, és derivable a $[0,1]$ per composició de $h$ i $g_u$, que són diferenciables, amb $f$, que és contínua; en particular, és contínua a $[0,1]$ i derivable a $(0,1)$.
[5] (demostració) Pel teorema del valor mitjà clàssic, existeix $\eta\in(0,1)$ tal que $\langle u,f(b)-f(a)\rangle=\varphi(1)-\varphi(0)=\varphi'(\eta)\,(1-0)$.
[6] (demostració) Per la regla de la cadena, $\varphi'(t)=Jh(t)\cdot Jf(h(t))\cdot\nabla g_u(f(h(t)))$, on $\nabla g_u(y)=(u_1\ \cdots\ u_m)$ per a tot $y$ i $Jh(t)=b-a$, vist com a vector columna.
[7] (demostració) Per tant, $\varphi'(\eta)=(u_1\ \cdots\ u_m)\,Jf(h(\eta))\,(b-a)=\langle u,Jf(h(\eta))\,(b-a)\rangle$.
[8] (demostració) Prenent $\xi=h(\eta)$, que pertany a $(a,b)$ perquè $\eta\in(0,1)$, obtenim $\langle u,f(b)-f(a)\rangle=\langle u,Jf(\xi)\,(b-a)\rangle$.


## T3.32:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.32] Teorema 32 (Tema 3) — Regla de Leibniz
(Regla de Leibniz). Sigui $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^1(\Omega)$, amb $\Omega$ obert. Siguin $a,b,c,d\in\mathbb{R}$ tals que $[a,b]\times[c,d]\subseteq\Omega$ i considereu $u,v:(c,d)\to[a,b]$ dues funcions derivables. Llavors,

(i) La funció
$$F(y)=\int_a^bf(x,y)\,dx$$
és derivable a l'interval $(c,d)$ i $F'(y)=\displaystyle\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$.

(ii) La funció
$$G(y)=\int_{u(y)}^{v(y)}f(x,y)\,dx$$
és derivable a l'interval $(c,d)$ i la seva derivada val
$$G'(y)=f(v(y),y)v'(y)-f(u(y),y)u'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx.$$
Demostració: (i) Veure que $F$ és derivable a un punt $y$ és equivalent a demostrar que existeix
$$F'(y)=\lim_{h\to0}\frac{F(y+h)-F(y)}{h}.$$
Volem, a més, demostrar que aquest límit és justament $\displaystyle\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$. En primer lloc, observeu que
$$\begin{aligned}\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|&=\left|\frac{1}{h}\left(\int_a^bf(x,y+h)\,dx-\int_a^bf(x,y)\,dx\right)-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|\\&=\left|\int_a^b\frac{f(x,y+h)-f(x,y)}{h}-\frac{\partial f}{\partial y}(x,y)\,dx\right|\end{aligned}\tag{13}$$
Fixada $x$, la funció $f(x,\cdot)$ està definida a l'interval $[y,y+h]$, hi és derivable i $\mathcal{C}^1$. Per tant, aplicant el teorema del valor mitjà, tenim que existeix un valor $\xi_{h,x}\in(y,y+h)$ de forma que
$$f(x,y+h)-f(x,y)=\frac{\partial f}{\partial y}(x,\xi_{h,x})\,h.$$
Si ho apliquem a l'anterior expressió (13) i usem que $\left|\displaystyle\int_a^bg\right|\leq\displaystyle\int_a^b|g|$, obtenim
$$\left|\int_a^b\frac{f(x,y+h)-f(x,y)}{h}-\frac{\partial f}{\partial y}(x,y)\,dx\right|\leq\int_a^b\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|\,dx\tag{14}$$
Del fet que $f\in\mathcal{C}^1$ es deriva que la funció $\dfrac{\partial f}{\partial y}(x,y):[a,b]\times[c,d]$ és contínua i, atès que $[a,b]\times[c,d]$ és compacte, uniformement contínua. És a dir, per a tot $\varepsilon>0$ existeix un $\delta_1(\varepsilon)>0$ tal que per a tot $x\in[a,b]$ i $\forall y,y'\in[c,d]$ satisfent que $|y'-y|<\delta_1$ es té que
$$\left|\frac{\partial f}{\partial y}(x,y')-\frac{\partial f}{\partial y}(x,y)\right|<\varepsilon.\tag{15}$$
Amb aquestes desigualtats, fixat $\varepsilon>0$, volem trobar $\delta=\delta(\varepsilon)>0$ de forma que si $|h|<\delta$ aleshores
$$\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|<\varepsilon.$$
Per a $x\in[a,b]$ fixat, si prenem $\delta<\delta_1(\varepsilon/(b-a))$ es dedueix que $|\xi_{h,x}-y|\leq|h|<\delta_1$ (ja que $\xi_{h,x}\in(y,y+h)$), i aplicant (15) tenim
$$\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|<\frac{\varepsilon}{b-a}.$$
Substituint a les expressions (13) i (14) s'obté que si $|h|<\delta$ llavors
$$\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|\leq\int_a^b\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|\,dx\leq\int_a^b\frac{\varepsilon}{b-a}\,dx=\varepsilon,$$
que era el que volíem demostrar.

(ii) Observem primer que, pel teorema fonamental del càlcul a $\mathbb{R}$, si $g:[a,b]\to\mathbb{R}$ contínua, aleshores
$$\frac{d}{dy}\int_{u(y)}^{v(y)}g(x)\,dx=g(v(y))\,v'(y)-g(u(y))\,u'(y).$$
Construïm:
$$\begin{aligned}F&:[a,b]\times[a,b]\times[c,d]\to\mathbb{R},&F(u,v,y)&=\int_u^vf(x,y)\,dx\in\mathcal{C}^1,\\h&:(c,d)\to[a,b]\times[a,b]\times[c,d],&h(y)&=(u(y),v(y),y),\quad h\text{ diferenciable}\end{aligned}$$
i la seva composició $G=F\circ h:(c,d)\to\mathbb{R}$,
$$G(y)=(F\circ h)(y)=\int_{u(y)}^{v(y)}f(x,y)\,dx,$$
que és diferenciable a l'interval $(c,d)$. Noteu que
$$\frac{\partial F}{\partial u}(u,v,y)=-f(u,y),\qquad\frac{\partial F}{\partial v}(u,v,y)=f(v,y),\qquad\frac{\partial F}{\partial y}(u,v,y)=\int_u^v\frac{\partial f}{\partial y}(x,y)\,dx$$
i que $Jh(y)=(u'(y),v'(y),1)$. Llavors, aplicant la regla de la cadena, obtenim que
$$\begin{aligned}G'(y)&=(F\circ h)'(y)=JF(h(y))\,Jh(y)\\&=\left(-f(u(y),y)\quad f(v(y),y)\quad\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx\right)\begin{pmatrix}u'(y)\\v'(y)\\1\end{pmatrix}\\&=-f(u(y),y)\,u'(y)+f(v(y),y)\,v'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx.\end{aligned}$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Regla de Leibniz). Sigui $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^1(\Omega)$, amb $\Omega$ obert. Siguin $a,b,c,d\in\mathbb{R}$ tals que $[a,b]\times[c,d]\subseteq\Omega$ i siguin $u,v:(c,d)\to[a,b]$ dues funcions derivables.
[2] (enunciat) (i) La funció $F(y)=\int_a^bf(x,y)\,dx$ és derivable a l'interval $(c,d)$ i $F'(y)=\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$.
[3] (enunciat) (ii) La funció $G(y)=\int_{u(y)}^{v(y)}f(x,y)\,dx$ és derivable a l'interval $(c,d)$ i $G'(y)=f(v(y),y)\,v'(y)+f(u(y),y)\,u'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx$.
[4] (demostració) (i) Fixem $y\in(c,d)$; cal veure que $\lim_{h\to0}\frac{F(y+h)-F(y)}{h}=\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$. Per a $h\neq0$ amb $y+h\in(c,d)$, per la linealitat de la integral, $\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|=\left|\int_a^b\left(\frac{f(x,y+h)-f(x,y)}{h}-\frac{\partial f}{\partial y}(x,y)\right)dx\right|$. (13)
[5] (demostració) Fixada $x\in[a,b]$, la funció $f(x,\cdot)$ és derivable a l'interval d'extrems $y$ i $y+h$. Pel teorema del valor mitjà, existeix $\xi_{h,x}$ estrictament entre $y$ i $y+h$ tal que $f(x,y+h)-f(x,y)=\frac{\partial f}{\partial y}(x,\xi_{h,x})\,h$.
[6] (demostració) Substituint-ho a (13) i usant que $\left|\int_a^bg\right|\leq\int_a^b|g|$, obtenim que (13) és menor o igual que $\int_a^b\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|dx$. (14)
[7] (demostració) Com que $f\in\mathcal{C}^1$, la funció $\frac{\partial f}{\partial y}$ és contínua al compacte $[a,b]\times[c,d]$ i, per tant, uniformement contínua: per a tot $\varepsilon>0$ existeix $\delta_1(\varepsilon)>0$ tal que per a tot $x\in[a,b]$ i tots $y,y'\in[c,d]$ amb $|y'-y|<\delta_1$ es té $\left|\frac{\partial f}{\partial y}(x,y')-\frac{\partial f}{\partial y}(x,y)\right|<\varepsilon$. (15)
[8] (demostració) Donat $\varepsilon>0$, prenem $\delta$ amb $0<\delta<\delta_1\left(\frac{\varepsilon}{b-a}\right)$. Si $0<|h|<\delta$ (i $y+h\in(c,d)$), aleshores $|\xi_{h,x}-y|<|h|<\delta_1$ per a tot $x\in[a,b]$ i, per (15), $\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|<\frac{\varepsilon}{b-a}$.
[9] (demostració) Substituint a (13) i (14): $\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|\leq\int_a^b\frac{\varepsilon}{b-a}\,dx=\varepsilon$ si $0<|h|<\delta$, que és el que volíem demostrar.
[10] (demostració) (ii) Recordem que, pel teorema fonamental del càlcul, si $g:[a,b]\to\mathbb{R}$ és contínua, aleshores $\frac{d}{dy}\int_{u(y)}^{v(y)}g(x)\,dx=g(v(y))\,v'(y)-g(u(y))\,u'(y)$.
[11] (demostració) Considerem $\Phi:[a,b]\times[a,b]\times[c,d]\to\mathbb{R}$, $\Phi(s,t,y)=\int_s^tf(x,y)\,dx$, i $h:(c,d)\to[a,b]\times[a,b]\times[c,d]$, $h(y)=(u(y),v(y),y)$, que és derivable perquè ho són $u$ i $v$. Aleshores $G=\Phi\circ h$.
[12] (demostració) Pel teorema fonamental del càlcul i per l'apartat (i), $\frac{\partial\Phi}{\partial s}(s,t,y)=-f(s,y)$, $\frac{\partial\Phi}{\partial t}(s,t,y)=f(t,y)$ i $\frac{\partial\Phi}{\partial y}(s,t,y)=\int_s^t\frac{\partial f}{\partial y}(x,y)\,dx$, que són contínues; per tant $\Phi$ és de classe $\mathcal{C}^1$. A més, $Jh(y)=(u'(y),v'(y),1)^\top$.
[13] (demostració) Aplicant la regla de la cadena, $G'(y)=J\Phi(h(y))\,Jh(y)=-f(u(y),y)\,u'(y)+f(v(y),y)\,v'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx$.


## T3.32:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.32] Teorema 32 (Tema 3) — Regla de Leibniz
(Regla de Leibniz). Sigui $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^1(\Omega)$, amb $\Omega$ obert. Siguin $a,b,c,d\in\mathbb{R}$ tals que $[a,b]\times[c,d]\subseteq\Omega$ i considereu $u,v:(c,d)\to[a,b]$ dues funcions derivables. Llavors,

(i) La funció
$$F(y)=\int_a^bf(x,y)\,dx$$
és derivable a l'interval $(c,d)$ i $F'(y)=\displaystyle\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$.

(ii) La funció
$$G(y)=\int_{u(y)}^{v(y)}f(x,y)\,dx$$
és derivable a l'interval $(c,d)$ i la seva derivada val
$$G'(y)=f(v(y),y)v'(y)-f(u(y),y)u'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx.$$
Demostració: (i) Veure que $F$ és derivable a un punt $y$ és equivalent a demostrar que existeix
$$F'(y)=\lim_{h\to0}\frac{F(y+h)-F(y)}{h}.$$
Volem, a més, demostrar que aquest límit és justament $\displaystyle\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$. En primer lloc, observeu que
$$\begin{aligned}\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|&=\left|\frac{1}{h}\left(\int_a^bf(x,y+h)\,dx-\int_a^bf(x,y)\,dx\right)-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|\\&=\left|\int_a^b\frac{f(x,y+h)-f(x,y)}{h}-\frac{\partial f}{\partial y}(x,y)\,dx\right|\end{aligned}\tag{13}$$
Fixada $x$, la funció $f(x,\cdot)$ està definida a l'interval $[y,y+h]$, hi és derivable i $\mathcal{C}^1$. Per tant, aplicant el teorema del valor mitjà, tenim que existeix un valor $\xi_{h,x}\in(y,y+h)$ de forma que
$$f(x,y+h)-f(x,y)=\frac{\partial f}{\partial y}(x,\xi_{h,x})\,h.$$
Si ho apliquem a l'anterior expressió (13) i usem que $\left|\displaystyle\int_a^bg\right|\leq\displaystyle\int_a^b|g|$, obtenim
$$\left|\int_a^b\frac{f(x,y+h)-f(x,y)}{h}-\frac{\partial f}{\partial y}(x,y)\,dx\right|\leq\int_a^b\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|\,dx\tag{14}$$
Del fet que $f\in\mathcal{C}^1$ es deriva que la funció $\dfrac{\partial f}{\partial y}(x,y):[a,b]\times[c,d]$ és contínua i, atès que $[a,b]\times[c,d]$ és compacte, uniformement contínua. És a dir, per a tot $\varepsilon>0$ existeix un $\delta_1(\varepsilon)>0$ tal que per a tot $x\in[a,b]$ i $\forall y,y'\in[c,d]$ satisfent que $|y'-y|<\delta_1$ es té que
$$\left|\frac{\partial f}{\partial y}(x,y')-\frac{\partial f}{\partial y}(x,y)\right|<\varepsilon.\tag{15}$$
Amb aquestes desigualtats, fixat $\varepsilon>0$, volem trobar $\delta=\delta(\varepsilon)>0$ de forma que si $|h|<\delta$ aleshores
$$\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|<\varepsilon.$$
Per a $x\in[a,b]$ fixat, si prenem $\delta<\delta_1(\varepsilon/(b-a))$ es dedueix que $|\xi_{h,x}-y|\leq|h|<\delta_1$ (ja que $\xi_{h,x}\in(y,y+h)$), i aplicant (15) tenim
$$\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|<\frac{\varepsilon}{b-a}.$$
Substituint a les expressions (13) i (14) s'obté que si $|h|<\delta$ llavors
$$\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|\leq\int_a^b\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|\,dx\leq\int_a^b\frac{\varepsilon}{b-a}\,dx=\varepsilon,$$
que era el que volíem demostrar.

(ii) Observem primer que, pel teorema fonamental del càlcul a $\mathbb{R}$, si $g:[a,b]\to\mathbb{R}$ contínua, aleshores
$$\frac{d}{dy}\int_{u(y)}^{v(y)}g(x)\,dx=g(v(y))\,v'(y)-g(u(y))\,u'(y).$$
Construïm:
$$\begin{aligned}F&:[a,b]\times[a,b]\times[c,d]\to\mathbb{R},&F(u,v,y)&=\int_u^vf(x,y)\,dx\in\mathcal{C}^1,\\h&:(c,d)\to[a,b]\times[a,b]\times[c,d],&h(y)&=(u(y),v(y),y),\quad h\text{ diferenciable}\end{aligned}$$
i la seva composició $G=F\circ h:(c,d)\to\mathbb{R}$,
$$G(y)=(F\circ h)(y)=\int_{u(y)}^{v(y)}f(x,y)\,dx,$$
que és diferenciable a l'interval $(c,d)$. Noteu que
$$\frac{\partial F}{\partial u}(u,v,y)=-f(u,y),\qquad\frac{\partial F}{\partial v}(u,v,y)=f(v,y),\qquad\frac{\partial F}{\partial y}(u,v,y)=\int_u^v\frac{\partial f}{\partial y}(x,y)\,dx$$
i que $Jh(y)=(u'(y),v'(y),1)$. Llavors, aplicant la regla de la cadena, obtenim que
$$\begin{aligned}G'(y)&=(F\circ h)'(y)=JF(h(y))\,Jh(y)\\&=\left(-f(u(y),y)\quad f(v(y),y)\quad\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx\right)\begin{pmatrix}u'(y)\\v'(y)\\1\end{pmatrix}\\&=-f(u(y),y)\,u'(y)+f(v(y),y)\,v'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx.\end{aligned}$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Regla de Leibniz). Sigui $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^1(\Omega)$, amb $\Omega$ obert. Siguin $a,b,c,d\in\mathbb{R}$ tals que $[a,b]\times[c,d]\subseteq\Omega$ i siguin $u,v:(c,d)\to[a,b]$ dues funcions derivables.
[2] (enunciat) (i) La funció $F(y)=\int_a^bf(x,y)\,dx$ és derivable a l'interval $(c,d)$ i $F'(y)=\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$.
[3] (enunciat) (ii) La funció $G(y)=\int_{u(y)}^{v(y)}f(x,y)\,dx$ és derivable a l'interval $(c,d)$ i $G'(y)=f(v(y),y)\,v'(y)-f(u(y),y)\,u'(y)+\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$.
[4] (demostració) (i) Fixem $y\in(c,d)$; cal veure que $\lim_{h\to0}\frac{F(y+h)-F(y)}{h}=\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$. Per a $h\neq0$ amb $y+h\in(c,d)$, per la linealitat de la integral, $\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|=\left|\int_a^b\left(\frac{f(x,y+h)-f(x,y)}{h}-\frac{\partial f}{\partial y}(x,y)\right)dx\right|$. (13)
[5] (demostració) Fixada $x\in[a,b]$, la funció $f(x,\cdot)$ és derivable a l'interval d'extrems $y$ i $y+h$. Pel teorema del valor mitjà, existeix $\xi_{h,x}$ estrictament entre $y$ i $y+h$ tal que $f(x,y+h)-f(x,y)=\frac{\partial f}{\partial y}(x,\xi_{h,x})\,h$.
[6] (demostració) Substituint-ho a (13) i usant que $\left|\int_a^bg\right|\leq\int_a^b|g|$, obtenim que (13) és menor o igual que $\int_a^b\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|dx$. (14)
[7] (demostració) Com que $f\in\mathcal{C}^1$, la funció $\frac{\partial f}{\partial y}$ és contínua al compacte $[a,b]\times[c,d]$ i, per tant, uniformement contínua: per a tot $\varepsilon>0$ existeix $\delta_1(\varepsilon)>0$ tal que per a tot $x\in[a,b]$ i tots $y,y'\in[c,d]$ amb $|y'-y|<\delta_1$ es té $\left|\frac{\partial f}{\partial y}(x,y')-\frac{\partial f}{\partial y}(x,y)\right|<\varepsilon$. (15)
[8] (demostració) Donat $\varepsilon>0$, prenem $\delta$ amb $0<\delta<\delta_1(\varepsilon)$. Si $0<|h|<\delta$ (i $y+h\in(c,d)$), aleshores $|\xi_{h,x}-y|<|h|<\delta_1$ per a tot $x\in[a,b]$ i, per (15), $\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|<\varepsilon$.
[9] (demostració) Substituint a (13) i (14): $\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|\leq\int_a^b\varepsilon\,dx\leq\varepsilon$ si $0<|h|<\delta$, que és el que volíem demostrar.
[10] (demostració) (ii) Recordem que, pel teorema fonamental del càlcul, si $g:[a,b]\to\mathbb{R}$ és contínua, aleshores $\frac{d}{dy}\int_{u(y)}^{v(y)}g(x)\,dx=g(v(y))\,v'(y)-g(u(y))\,u'(y)$.
[11] (demostració) Considerem $\Phi:[a,b]\times[a,b]\times[c,d]\to\mathbb{R}$, $\Phi(s,t,y)=\int_s^tf(x,y)\,dx$, i $h:(c,d)\to[a,b]\times[a,b]\times[c,d]$, $h(y)=(u(y),v(y),y)$, que és derivable perquè ho són $u$ i $v$. Aleshores $G=\Phi\circ h$.
[12] (demostració) Pel teorema fonamental del càlcul i per l'apartat (i), $\frac{\partial\Phi}{\partial s}(s,t,y)=-f(s,y)$, $\frac{\partial\Phi}{\partial t}(s,t,y)=f(t,y)$ i $\frac{\partial\Phi}{\partial y}(s,t,y)=\int_s^t\frac{\partial f}{\partial y}(x,y)\,dx$, que són contínues; per tant $\Phi$ és de classe $\mathcal{C}^1$. A més, $Jh(y)=(u'(y),v'(y),1)^\top$.
[13] (demostració) Aplicant la regla de la cadena, $G'(y)=J\Phi(h(y))\,Jh(y)=-f(u(y),y)\,u'(y)+f(v(y),y)\,v'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx$.


## T3.32:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T3.32] Teorema 32 (Tema 3) — Regla de Leibniz
(Regla de Leibniz). Sigui $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^1(\Omega)$, amb $\Omega$ obert. Siguin $a,b,c,d\in\mathbb{R}$ tals que $[a,b]\times[c,d]\subseteq\Omega$ i considereu $u,v:(c,d)\to[a,b]$ dues funcions derivables. Llavors,

(i) La funció
$$F(y)=\int_a^bf(x,y)\,dx$$
és derivable a l'interval $(c,d)$ i $F'(y)=\displaystyle\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$.

(ii) La funció
$$G(y)=\int_{u(y)}^{v(y)}f(x,y)\,dx$$
és derivable a l'interval $(c,d)$ i la seva derivada val
$$G'(y)=f(v(y),y)v'(y)-f(u(y),y)u'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx.$$
Demostració: (i) Veure que $F$ és derivable a un punt $y$ és equivalent a demostrar que existeix
$$F'(y)=\lim_{h\to0}\frac{F(y+h)-F(y)}{h}.$$
Volem, a més, demostrar que aquest límit és justament $\displaystyle\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$. En primer lloc, observeu que
$$\begin{aligned}\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|&=\left|\frac{1}{h}\left(\int_a^bf(x,y+h)\,dx-\int_a^bf(x,y)\,dx\right)-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|\\&=\left|\int_a^b\frac{f(x,y+h)-f(x,y)}{h}-\frac{\partial f}{\partial y}(x,y)\,dx\right|\end{aligned}\tag{13}$$
Fixada $x$, la funció $f(x,\cdot)$ està definida a l'interval $[y,y+h]$, hi és derivable i $\mathcal{C}^1$. Per tant, aplicant el teorema del valor mitjà, tenim que existeix un valor $\xi_{h,x}\in(y,y+h)$ de forma que
$$f(x,y+h)-f(x,y)=\frac{\partial f}{\partial y}(x,\xi_{h,x})\,h.$$
Si ho apliquem a l'anterior expressió (13) i usem que $\left|\displaystyle\int_a^bg\right|\leq\displaystyle\int_a^b|g|$, obtenim
$$\left|\int_a^b\frac{f(x,y+h)-f(x,y)}{h}-\frac{\partial f}{\partial y}(x,y)\,dx\right|\leq\int_a^b\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|\,dx\tag{14}$$
Del fet que $f\in\mathcal{C}^1$ es deriva que la funció $\dfrac{\partial f}{\partial y}(x,y):[a,b]\times[c,d]$ és contínua i, atès que $[a,b]\times[c,d]$ és compacte, uniformement contínua. És a dir, per a tot $\varepsilon>0$ existeix un $\delta_1(\varepsilon)>0$ tal que per a tot $x\in[a,b]$ i $\forall y,y'\in[c,d]$ satisfent que $|y'-y|<\delta_1$ es té que
$$\left|\frac{\partial f}{\partial y}(x,y')-\frac{\partial f}{\partial y}(x,y)\right|<\varepsilon.\tag{15}$$
Amb aquestes desigualtats, fixat $\varepsilon>0$, volem trobar $\delta=\delta(\varepsilon)>0$ de forma que si $|h|<\delta$ aleshores
$$\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|<\varepsilon.$$
Per a $x\in[a,b]$ fixat, si prenem $\delta<\delta_1(\varepsilon/(b-a))$ es dedueix que $|\xi_{h,x}-y|\leq|h|<\delta_1$ (ja que $\xi_{h,x}\in(y,y+h)$), i aplicant (15) tenim
$$\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|<\frac{\varepsilon}{b-a}.$$
Substituint a les expressions (13) i (14) s'obté que si $|h|<\delta$ llavors
$$\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|\leq\int_a^b\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|\,dx\leq\int_a^b\frac{\varepsilon}{b-a}\,dx=\varepsilon,$$
que era el que volíem demostrar.

(ii) Observem primer que, pel teorema fonamental del càlcul a $\mathbb{R}$, si $g:[a,b]\to\mathbb{R}$ contínua, aleshores
$$\frac{d}{dy}\int_{u(y)}^{v(y)}g(x)\,dx=g(v(y))\,v'(y)-g(u(y))\,u'(y).$$
Construïm:
$$\begin{aligned}F&:[a,b]\times[a,b]\times[c,d]\to\mathbb{R},&F(u,v,y)&=\int_u^vf(x,y)\,dx\in\mathcal{C}^1,\\h&:(c,d)\to[a,b]\times[a,b]\times[c,d],&h(y)&=(u(y),v(y),y),\quad h\text{ diferenciable}\end{aligned}$$
i la seva composició $G=F\circ h:(c,d)\to\mathbb{R}$,
$$G(y)=(F\circ h)(y)=\int_{u(y)}^{v(y)}f(x,y)\,dx,$$
que és diferenciable a l'interval $(c,d)$. Noteu que
$$\frac{\partial F}{\partial u}(u,v,y)=-f(u,y),\qquad\frac{\partial F}{\partial v}(u,v,y)=f(v,y),\qquad\frac{\partial F}{\partial y}(u,v,y)=\int_u^v\frac{\partial f}{\partial y}(x,y)\,dx$$
i que $Jh(y)=(u'(y),v'(y),1)$. Llavors, aplicant la regla de la cadena, obtenim que
$$\begin{aligned}G'(y)&=(F\circ h)'(y)=JF(h(y))\,Jh(y)\\&=\left(-f(u(y),y)\quad f(v(y),y)\quad\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx\right)\begin{pmatrix}u'(y)\\v'(y)\\1\end{pmatrix}\\&=-f(u(y),y)\,u'(y)+f(v(y),y)\,v'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx.\end{aligned}$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Regla de Leibniz). Sigui $f:\Omega\subseteq\mathbb{R}^2\to\mathbb{R}$ de classe $\mathcal{C}^1(\Omega)$, amb $\Omega$ obert. Siguin $a,b,c,d\in\mathbb{R}$ tals que $(a,b)\times(c,d)\subseteq\Omega$ i siguin $u,v:(c,d)\to[a,b]$ dues funcions derivables.
[2] (enunciat) (i) La funció $F(y)=\int_a^bf(x,y)\,dx$ és derivable a l'interval $(c,d)$ i $F'(y)=\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$.
[3] (enunciat) (ii) La funció $G(y)=\int_{u(y)}^{v(y)}f(x,y)\,dx$ és derivable a l'interval $(c,d)$ i $G'(y)=f(v(y),y)\,v'(y)-f(u(y),y)\,u'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx$.
[4] (demostració) (i) Fixem $y\in(c,d)$; cal veure que $\lim_{h\to0}\frac{F(y+h)-F(y)}{h}=\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx$. Per a $h\neq0$ amb $y+h\in(c,d)$, per la linealitat de la integral, $\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|=\left|\int_a^b\left(\frac{f(x,y+h)-f(x,y)}{h}-\frac{\partial f}{\partial y}(x,y)\right)dx\right|$. (13)
[5] (demostració) Fixada $x\in[a,b]$, la funció $f(x,\cdot)$ és derivable a l'interval d'extrems $y$ i $y+h$. Pel teorema del valor mitjà, existeix $\xi_{h,x}$ estrictament entre $y$ i $y+h$ tal que $f(x,y+h)-f(x,y)=\frac{\partial f}{\partial y}(x,\xi_{h,x})\,h$.
[6] (demostració) Substituint-ho a (13) i usant que $\left|\int_a^bg\right|\leq\int_a^b|g|$, obtenim que (13) és menor o igual que $\int_a^b\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|dx$. (14)
[7] (demostració) Com que $f\in\mathcal{C}^1$, la funció $\frac{\partial f}{\partial y}$ és contínua al compacte $[a,b]\times[c,d]$ i, per tant, uniformement contínua: per a tot $\varepsilon>0$ existeix $\delta_1(\varepsilon)>0$ tal que per a tot $x\in[a,b]$ i tots $y,y'\in[c,d]$ amb $|y'-y|<\delta_1$ es té $\left|\frac{\partial f}{\partial y}(x,y')-\frac{\partial f}{\partial y}(x,y)\right|<\varepsilon$. (15)
[8] (demostració) Donat $\varepsilon>0$, prenem $\delta$ amb $0<\delta<\delta_1\left(\frac{\varepsilon}{b-a}\right)$. Si $0<|h|<\delta$ (i $y+h\in(c,d)$), aleshores $|\xi_{h,x}-y|<|h|<\delta_1$ per a tot $x\in[a,b]$ i, per (15), $\left|\frac{\partial f}{\partial y}(x,\xi_{h,x})-\frac{\partial f}{\partial y}(x,y)\right|<\frac{\varepsilon}{b-a}$.
[9] (demostració) Substituint a (13) i (14): $\left|\frac{F(y+h)-F(y)}{h}-\int_a^b\frac{\partial f}{\partial y}(x,y)\,dx\right|\leq\int_a^b\frac{\varepsilon}{b-a}\,dx=\varepsilon$ si $0<|h|<\delta$, que és el que volíem demostrar.
[10] (demostració) (ii) Recordem que, pel teorema fonamental del càlcul, si $g:[a,b]\to\mathbb{R}$ és integrable, aleshores $\frac{d}{dy}\int_{u(y)}^{v(y)}g(x)\,dx=g(v(y))\,v'(y)-g(u(y))\,u'(y)$.
[11] (demostració) Considerem $\Phi:[a,b]\times[a,b]\times[c,d]\to\mathbb{R}$, $\Phi(s,t,y)=\int_s^tf(x,y)\,dx$, i $h:(c,d)\to[a,b]\times[a,b]\times[c,d]$, $h(y)=(u(y),v(y),y)$, que és derivable perquè $u$ i $v$ són contínues. Aleshores $G=\Phi\circ h$.
[12] (demostració) Pel teorema fonamental del càlcul i per l'apartat (i), $\frac{\partial\Phi}{\partial s}(s,t,y)=-f(s,y)$, $\frac{\partial\Phi}{\partial t}(s,t,y)=f(t,y)$ i $\frac{\partial\Phi}{\partial y}(s,t,y)=\int_s^t\frac{\partial f}{\partial y}(x,y)\,dx$, que són contínues; per tant $\Phi$ és de classe $\mathcal{C}^1$. A més, $Jh(y)=(u'(y),v'(y),1)^\top$.
[13] (demostració) Aplicant la regla de la cadena, $G'(y)=J\Phi(h(y))\,Jh(y)=-f(u(y),y)\,u'(y)+f(v(y),y)\,v'(y)+\int_{u(y)}^{v(y)}\frac{\partial f}{\partial y}(x,y)\,dx$.

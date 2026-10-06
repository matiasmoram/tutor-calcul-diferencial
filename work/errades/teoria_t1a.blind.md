## T1.6:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.6] Proposició 6 (Tema 1) — Euclidià implica normat implica mètric
i) Tot espai euclidià és un espai normat si definim $\|u\|=\sqrt{\langle u,u\rangle}$.

ii) Tot espai normat és un espai mètric si prenem $d(u,v)=\|u-v\|$.

[Figura: diagrama de conjunts imbricats: espais euclidians dins d'espais normats dins d'espais mètrics.]

Figura 1: Espais euclidians $\subset$ espais normats $\subset$ espais mètrics.

Per a demostrar aquesta proposició usarem, en algun moment, el següent resultat:
Demostració: **Demostració de la proposició 6:**

i) Sigui $E$ un espai euclidià i definim la norma $\|u\|=\sqrt{\langle u,u\rangle}$.
Vegem que satisfà les propietats que defineixen una norma:

- $\|u\|=\sqrt{\langle u,u\rangle}\geq 0$ ja que $\langle u,u\rangle\geq 0$. $\|u\|=0\iff\langle u,u\rangle=0\iff u=0$.
- $\|\lambda u\|=\sqrt{\langle\lambda u,\lambda u\rangle}=\sqrt{\lambda^2\langle u,u\rangle}=|\lambda|\sqrt{\langle u,u\rangle}=|\lambda|\,\|u\|$.
- Veure que $\|u+v\|\leq\|u\|+\|v\|$ és equivalent a veure que $(\|u+v\|)^2\leq(\|u\|+\|v\|)^2$ (ja que ambdós costats són positius).

Aleshores,

$$\|u+v\|^2=\langle u+v,u+v\rangle=\langle u,u\rangle+2\langle u,v\rangle+\langle v,v\rangle=\|u\|^2+\|v\|^2+2\langle u,v\rangle\ \underset{\text{Cauchy-Schwarz}}{\leq}\ \|u\|^2+\|v\|^2+2\|u\|\,\|v\|=(\|u\|+\|v\|)^2.$$

Per tant, $\|u\|=\sqrt{\langle u,u\rangle}$ és una norma i $(E,\|\cdot\|)$ és un espai normat.

ii) Anàlogament, veiem que si $(E,\|\cdot\|)$ és un espai normat i definim $d(u,v)=\|u-v\|$, aleshores $d(\cdot,\cdot)$ satisfà les propietats per a ser una distància i, per tant, $(E,d)$ és un espai mètric.

- $d(u,v)=\|u-v\|\geq 0$; $d(u,v)=0\iff\|u-v\|=0\iff u-v=0\iff u=v$.
- $d(u,v)=\|u-v\|=\|(-1)(v-u)\|=|-1|\,\|v-u\|=\|v-u\|=d(v,u)$.
- Respecte la desigualtat triangular:

$$\begin{aligned}d(u,w)&=\|u-w\|=\|u-v+v-w\|=\|(u-v)+(v-w)\|\\&\leq\|u-v\|+\|v-w\|=d(u,v)+d(v,w).\end{aligned}$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) i) Sigui $E$ un espai euclidià. Si definim $\|u\|=\sqrt{\langle u,u\rangle}$, aleshores $(E,\|\cdot\|)$ és un espai normat.
[2] (enunciat) ii) Tot espai normat $(E,\|\cdot\|)$ és un espai mètric si prenem $d(u,v)=\|u-v\|$ i, recíprocament, tota distància $d$ sobre un espai vectorial $E$ prové d'una norma, definida per $\|u\|=d(u,0)$.
[3] (demostració) i) Vegem que $\|u\|=\sqrt{\langle u,u\rangle}$ satisfà les propietats d'una norma. Com que $\langle u,u\rangle\geq 0$, tenim $\|u\|\geq 0$, i $\|u\|=0\iff\langle u,u\rangle=0\iff u=0$.
[4] (demostració) Per a $\lambda\in\mathbb{R}$, $\|\lambda u\|=\sqrt{\langle\lambda u,\lambda u\rangle}=\sqrt{\lambda^2\langle u,u\rangle}=\lambda\sqrt{\langle u,u\rangle}=\lambda\,\|u\|$, que és la propietat d'homogeneïtat.
[5] (demostració) Per a la desigualtat triangular, com que els dos costats són no negatius, veure que $\|u+v\|\leq\|u\|+\|v\|$ és equivalent a veure que $\|u+v\|^2\leq(\|u\|+\|v\|)^2$.
[6] (demostració) Ara, $\|u+v\|^2=\langle u+v,u+v\rangle=\|u\|^2+\|v\|^2+2\langle u,v\rangle\leq\|u\|^2+\|v\|^2+2\|u\|\,\|v\|=(\|u\|+\|v\|)^2$, on hem usat la desigualtat de Cauchy-Schwarz. Per tant, $(E,\|\cdot\|)$ és un espai normat.
[7] (demostració) ii) Sigui $d(u,v)=\|u-v\|$. Tenim $d(u,v)\geq 0$ i $d(u,v)=0\iff\|u-v\|=0\iff u=v$. A més, $d(u,v)=\|(-1)(v-u)\|=|-1|\,\|v-u\|=d(v,u)$.
[8] (demostració) Finalment, $d(u,w)=\|(u-v)+(v-w)\|\leq\|u-v\|+\|v-w\|=d(u,v)+d(v,w)$, i per tant $(E,d)$ és un espai mètric.


## T1.7:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.7] Proposició 7 (Tema 1) — Desigualtat de Cauchy-Schwarz
(Desigualtat de Cauchy-Schwarz.) Sigui $(E,\langle\cdot,\cdot\rangle)$ un espai euclidià (normat si definim $\|u\|=\sqrt{\langle u,u\rangle}$). Aleshores es verifica que

$$|\langle u,v\rangle|\leq\|u\|\cdot\|v\|.$$

(Nota: Augustin Louis Cauchy (1789-1857), Hermann Schwarz (1843-1921).)
Demostració: **Demostració de la desigualtat de Cauchy-Schwarz:**

- Vegem primer que se satisfà per al cas $u=0$ (anàlogament, per al cas $v=0$). D'un costat, $u=0\implies\|u\|=0\implies\|u\|\cdot\|v\|=0$. De l'altre,

$$\langle 0,v\rangle=\langle 0+0,v\rangle=\langle 0,v\rangle+\langle 0,v\rangle\implies\langle 0,v\rangle=2\langle 0,v\rangle\implies\langle 0,v\rangle=0.$$

Per tant,

$$\left.\begin{aligned}|\langle 0,v\rangle|&=0\\\|0\|\cdot\|v\|&=0\end{aligned}\right\}\implies|\langle 0,v\rangle|\leq\|0\|\cdot\|v\|.$$

- Suposem ara el cas que $u\neq 0$ i $v\neq 0$. Això implica que $\|u\|\neq 0$ i $\|v\|\neq 0$, de manera que podem definir

$$u'=\frac{1}{\|u\|}u\quad\text{i}\quad v'=\frac{1}{\|v\|}v.$$

És directe comprovar que $\|u'\|=1$ i $\|v'\|=1$. En efecte:

$$\|u'\|=\left\|\frac{1}{\|u\|}u\right\|=\frac{1}{\|u\|}\|u\|=1.\quad\text{(ídem per a } v'\text{)}.$$

Aleshores:

$$\begin{aligned}0&\leq\|u'-v'\|^2=\langle u'-v',u'-v'\rangle=\langle u',u'\rangle-2\langle u',v'\rangle+\langle v',v'\rangle\\&=\underbrace{\|u'\|^2}_{=1}-2\langle u',v'\rangle+\underbrace{\|v'\|^2}_{=1}=2-2\langle u',v'\rangle.\end{aligned}$$

Per tant,

$$2\langle u',v'\rangle\leq 2,\ \text{és a dir, }\langle u',v'\rangle\leq 1\Rightarrow\langle u,v\rangle\leq\|u\|\cdot\|v\|,\tag{1}$$

on hem usat que

$$\langle u',v'\rangle=\left\langle\frac{u}{\|u\|},\frac{v}{\|v\|}\right\rangle=\frac{1}{\|u\|\,\|v\|}\langle u,v\rangle.$$

Vegem ara la desigualtat contrària, és a dir, que $\langle u,v\rangle\geq-\|u\|\,\|v\|$. En efecte:

$$-\langle u,v\rangle=\langle u,-v\rangle\ \underset{C-S}{\leq}\ \|u\|\,\|-v\|=\|u\|\,\|v\|\implies\langle u,v\rangle\geq-\|u\|\,\|v\|.\tag{2}$$

Usant (1) i (2), es dedueix que:

$$-\|u\|\,\|v\|\leq\langle u,v\rangle\leq\|u\|\,\|v\|\implies|\langle u,v\rangle|\leq\|u\|\,\|v\|.$$

Ara ja podem fer la demostració de la proposició anterior.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Desigualtat de Cauchy-Schwarz.) Sigui $(E,\langle\cdot,\cdot\rangle)$ un espai euclidià, normat amb $\|u\|=\sqrt{\langle u,u\rangle}$. Aleshores, per a tot $u,v\in E$, es verifica que $|\langle u,v\rangle|<\|u\|\cdot\|v\|$.
[2] (demostració) Comencem pel cas $u=0$. D'una banda, $\|0\|=0$ i, per tant, $\|u\|\cdot\|v\|=0$. De l'altra, $\langle 0,v\rangle=\langle 0+0,v\rangle=2\langle 0,v\rangle$, d'on $\langle 0,v\rangle=0$. Així, $|\langle 0,v\rangle|\leq\|0\|\cdot\|v\|$.
[3] (demostració) Suposem ara que $u\neq 0$. Aleshores $\|u\|\neq 0$ i podem definir $u'=\frac{1}{\|u\|}u$ i $v'=\frac{1}{\|v\|}v$, que compleixen $\|u'\|=\frac{1}{\|u\|}\|u\|=1$ i, anàlogament, $\|v'\|=1$.
[4] (demostració) Aleshores $0\leq\|u'-v'\|^2=\langle u',u'\rangle-2\langle u',v'\rangle+\langle v',v'\rangle=2-2\langle u',v'\rangle$, i per tant $\langle u',v'\rangle\leq 1$.
[5] (demostració) Com que $\langle u',v'\rangle=\frac{1}{\|u\|\,\|v\|}\langle u,v\rangle$, es dedueix que $\langle u,v\rangle\leq\|u\|\cdot\|v\|$. (1)
[6] (demostració) Per a la desigualtat contrària, apliquem (1) als vectors $u$ i $-v$: $-\langle u,v\rangle=\langle u,-v\rangle\leq\|u\|\,\|-v\|=\|u\|\,\|v\|$, és a dir, $\langle u,v\rangle\geq-\|u\|\,\|v\|$. (2)
[7] (demostració) De (1) i (2) obtenim $-\|u\|\,\|v\|\leq\langle u,v\rangle\leq\|u\|\,\|v\|$, és a dir, $|\langle u,v\rangle|\leq\|u\|\,\|v\|$.


## T1.12:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.12] Proposició 12 (Tema 1) — Propietats dels conjunts oberts
(Propietats dels conjunts oberts.) Sigui $(M,d)$ un espai mètric. Aleshores,

i) tota bola oberta $B_r(x)$ és un conjunt obert;

ii) la unió arbitrària (finita o infinita) d'oberts és un obert;

iii) la intersecció finita d'oberts és un obert;

iv) $M$ i $\varnothing$ són conjunts oberts.
Demostració: **Demostració de la proposició 12:**

i) Cal veure que $\forall y\in B_r(x)$ existeix $r_y>0$ tal que $B_{r_y}(y)\subset B_r(x)$.

Del fet que $y\in B_r(x)$ es dedueix que $d(x,y)<r$. Definim $r_y:=r-d(x,y)>0$. Aleshores, si $z\in B_{r_y}(y)\Rightarrow d(y,z)<r_y=r-d(x,y)$, de forma que

$$d(z,x)\leq d(z,y)+d(y,x)<(r-d(x,y))+d(x,y)=r,$$

fet que implica que $B_{r_y}(y)\subset B_r(x)$.

ii) Sigui $(A_\mu)_{\mu\in I}$, $I$ conjunt arbitrari, $A_\mu$ obert, $A_\mu\subset M$. Volem veure que $\bigcup_{\mu\in I}A_\mu$ és també un conjunt obert de $M$.

Clarament $\bigcup_{\mu\in I}A_\mu\subset M$. Per tant, si $x\in\bigcup_{\mu\in I}A_\mu$ llavors existeix $\mu_0\in I$ tal que $x\in A_{\mu_0}$. Del fet que $A_{\mu_0}$ és un obert (a $M$) es té que existeix $r_0>0$ de manera que $B_{r_0}(x)\subseteq A_{\mu_0}\subseteq\bigcup_{\mu\in I}A_\mu$.

iii) És suficient mostrar que si $A_1$ i $A_2$ són oberts de $M$ aleshores $A_1\cap A_2$ també és un obert de $M$. La resta s'obté per inducció

En efecte, sigui $x\in A_1\cap A_2$. D'una banda, $x\in A_1$, obert, i per tant existeix $r_1>0$ tal que $B_{r_1}(x)\subseteq A_1$. De l'altra, $x\in A_2$, obert, d'on es té que existeix $r_2>0$ tal que $B_{r_2}(x)\subseteq A_2$. Aleshores, si definim $r=\min\{r_1,r_2\}$ tenim:

$$B_r(x)\subseteq B_{r_1}(x)\subseteq A_1,\quad\text{i}\quad B_r(x)\subseteq B_{r_2}(x)\subseteq A_2\quad\Rightarrow B_r(x)\subseteq A_1\cap A_2$$

iv) Clarament $M$ és obert. En efecte, sigui $x\in M$. Considerem $r>0$ qualsevol. Aleshores la bola oberta de centre $x$ i radi $r$ es defineix com $B_r(x)=\{y\in M\mid d(x,y)<r\}$. Noteu que, per definició, tot punt $y$ d'aquesta bola ha de pertànyer, necessàriament, al conjunt $M$. Per tant $B_r(x)\subseteq M$, que implica que $M$ és un obert.

La demostració de que $\varnothing$ és un obert serà conseqüència del fet que $M$ és també un tancat (vegeu Prop. 13) i $\varnothing$ és el seu complementari a $M$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Propietats dels conjunts oberts.) Sigui $(M,d)$ un espai mètric. Aleshores: i) tota bola oberta $B_r(x)$ és un conjunt obert i tancat; ii) la unió arbitrària (finita o infinita) d'oberts és un obert;
[2] (enunciat) iii) la intersecció finita d'oberts és un obert; iv) $M$ i $\varnothing$ són conjunts oberts.
[3] (demostració) i) Sigui $y\in B_r(x)$; cal trobar $r_y>0$ tal que $B_{r_y}(y)\subset B_r(x)$. Com que $d(x,y)<r$, definim $r_y:=r-d(x,y)>0$.
[4] (demostració) Si $z\in B_{r_y}(y)$, aleshores $d(z,x)\leq d(z,y)+d(y,x)<(r-d(x,y))+d(x,y)=r$, i per tant $B_{r_y}(y)\subset B_r(x)$.
[5] (demostració) ii) Sigui $(A_\mu)_{\mu\in I}$, amb $I$ un conjunt arbitrari, una família d'oberts de $M$. Si $x\in\bigcup_{\mu\in I}A_\mu$, existeix $\mu_0\in I$ tal que $x\in A_{\mu_0}$ i, com que $A_{\mu_0}$ és obert, existeix $r_0>0$ tal que $B_{r_0}(x)\subseteq A_{\mu_0}\subseteq\bigcup_{\mu\in I}A_\mu$.
[6] (demostració) iii) N'hi ha prou de veure que si $A_1$ i $A_2$ són oberts, $A_1\cap A_2$ també ho és; la resta s'obté per inducció. Sigui $x\in A_1\cap A_2$: existeixen $r_1>0$ i $r_2>0$ tals que $B_{r_1}(x)\subseteq A_1$ i $B_{r_2}(x)\subseteq A_2$.
[7] (demostració) Si definim $r=\max\{r_1,r_2\}$, tenim $B_r(x)\subseteq B_{r_1}(x)\subseteq A_1$ i $B_r(x)\subseteq B_{r_2}(x)\subseteq A_2$, d'on $B_r(x)\subseteq A_1\cap A_2$.
[8] (demostració) iv) $M$ és obert: si $x\in M$ i $r>0$, per definició $B_r(x)=\{y\in M\mid d(x,y)<r\}\subseteq M$. I $\varnothing$ és obert perquè no té cap punt, de manera que la condició de la definició es compleix trivialment.


## T1.13:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.13] Proposició 13 (Tema 1) — Propietats dels conjunts tancats
Sigui $M$ un conjunt i $d$ una distància definida sobre ell. Considereu la topologia sobre $M$ induïda per $d$. Aleshores:

i) les boles tancades de $M$ són conjunts tancats.

ii) La intersecció arbitrària de tancats és un tancat.

iii) La unió finita de tancats és un tancat.

iv) $M$ i $\varnothing$ són conjunts tancats.
Demostració: **Demostració de la proposició 13:**

i) Sigui $\overline{B}_r(x)=\{y\in M\mid d(x,y)\leq r\}$, amb $x\in M$ i $r>0$. Vegem que és un tancat.

Per a fer-ho, demostrarem que el seu complementari a $M$, $\overline{B}_r^c(x)$ és un obert.

En efecte, per a qualsevol $y\in\overline{B}_r^c(x)$ es té que $d(x,y)>r$. Sigui $r_1=d(x,y)-r>0$. Si provem que $B_{r_1}(y)\subseteq\overline{B}_r^c(x)$ aleshores $\overline{B}_r^c(x)$ és un obert.

En efecte (per reducció a l'absurd, _R.A._): suposem que $B_{r_1}(y)\not\subseteq\overline{B}_r^c(x)$. Això implica que existeix $z\in B_{r_1}(y)\cap\overline{B}_r(x)$, d'on es deriva que

$$\begin{cases}z\in B_{r_1}(y)&\Rightarrow d(z,y)<r_1\\z\in\overline{B}_r(x)&\Rightarrow d(z,x)\leq r\end{cases}$$

En conseqüència, per la desigualtat triangular,

$$d(y,x)\leq d(y,z)+d(z,x)<r_1+r=d(x,y)-r+r=d(x,y),\qquad\text{contradicció!!}$$

Per tant, $B_{r_1}(y)\subseteq\overline{B}_r^c(x)$ i $\overline{B}_r(x)$ és un tancat.

ii) D'un costat, si $(F_\mu)_{\mu\in I}$ és una col·lecció arbitrària de tancats, aleshores $(F_\mu^c)_{\mu\in I}$ és una col·lecció arbitrària d'oberts. De l'altre, per teoria de conjunts, tenim que

$$\bigcap_{\mu\in I}F_\mu=\left(\bigcup_{\mu\in I}F_\mu^c\right)^c$$

De la Proposició 12 es dedueix que $\bigcup_{\mu\in I}F_\mu^c$ és un obert (per ser unió arbitrària d'oberts) i, conseqüentment, el seu complementari $\left(\cup_{\mu\in I}F_\mu^c\right)^c$ és un tancat.

iii) Siguin $F_1,F_2,\ldots,F_k$ una col·lecció finita de tancats. Per tant $F_1^c,F_2^c,\ldots,F_k^c$ és una col·lecció finita d'oberts. A més, per teoria de conjunts,

$$\bigcup_{i=1}^k F_i=\left(\bigcap_{i=1}^k F_i^c\right)^c.$$

Com que $\bigcap_{i=1}^k F_i^c$ és un obert (per ser intersecció finita d'oberts), el seu complementari és un tancat. És a dir, $\bigcup_{i=1}^k F_i$ és un tancat.

iv) La demostració de que $M$ és tancat dins de $M$ és directa: per a tot punt $x\in M$, donat $r>0$, la bola tancada $\{y\in M\mid d(y,x)\leq r\}$ cau dins del conjunt $M$.

D'aquest fet i del que $M$ sigui també un conjunt obert (dins $M$) es dedueix que $\varnothing$ és obert i tancat a $M$ (per ser complementari de tancat i obert, respectivament).

RESULTATS DELS APUNTS QUE CITA:
[T1.12] Proposició 12 (Tema 1) — Propietats dels conjunts oberts
(Propietats dels conjunts oberts.) Sigui $(M,d)$ un espai mètric. Aleshores,

i) tota bola oberta $B_r(x)$ és un conjunt obert;

ii) la unió arbitrària (finita o infinita) d'oberts és un obert;

iii) la intersecció finita d'oberts és un obert;

iv) $M$ i $\varnothing$ són conjunts oberts.
</apunts>

### Document a revisar

[1] (enunciat) Sigui $M$ un conjunt i $d$ una distància definida sobre $M$, i considerem la topologia sobre $M$ induïda per $d$. Aleshores: i) les boles tancades de $M$ són conjunts tancats; ii) la intersecció arbitrària de tancats és un tancat;
[2] (enunciat) iii) la unió arbitrària (finita o infinita) de tancats és un tancat; iv) $M$ i $\varnothing$ són conjunts tancats.
[3] (demostració) i) Sigui $\overline{B}_r(x)=\{y\in M\mid d(x,y)\leq r\}$, amb $x\in M$ i $r>0$. Per veure que és tancat, provarem que el seu complementari a $M$, $\overline{B}_r^c(x)$, és obert.
[4] (demostració) Sigui $y\in\overline{B}_r^c(x)$, de manera que $d(x,y)>r$, i sigui $r_1=d(x,y)-r>0$. Suposem, per reducció a l'absurd, que $B_{r_1}(y)\not\subseteq\overline{B}_r^c(x)$: aleshores existeix $z\in B_{r_1}(y)\cap\overline{B}_r(x)$, és a dir, $d(z,y)<r_1$ i $d(z,x)\leq r$.
[5] (demostració) Per la desigualtat triangular, $d(y,x)\leq d(y,z)+d(z,x)<r_1+r=d(x,y)$, una contradicció. Per tant, $B_{r_1}(y)\subseteq\overline{B}_r^c(x)$, i $\overline{B}_r(x)$ és un tancat.
[6] (demostració) ii) Si $(F_\mu)_{\mu\in I}$ és una col·lecció arbitrària de tancats, $(F_\mu^c)_{\mu\in I}$ és una col·lecció arbitrària d'oberts, i $\bigcap_{\mu\in I}F_\mu=\left(\bigcup_{\mu\in I}F_\mu^c\right)^c$. Per la Proposició 12, $\bigcup_{\mu\in I}F_\mu^c$ és obert, i el seu complementari és tancat.
[7] (demostració) iii) Siguin $F_1,F_2,\ldots,F_k$ una col·lecció finita de tancats. Aleshores $F_1^c,F_2^c,\ldots,F_k^c$ són oberts i, per teoria de conjunts, $\bigcup_{i=1}^k F_i=\left(\bigcup_{i=1}^k F_i^c\right)^c$.
[8] (demostració) Com que $\bigcap_{i=1}^k F_i^c$ és obert, per ser intersecció finita d'oberts, el seu complementari $\bigcup_{i=1}^k F_i$ és tancat.
[9] (demostració) iv) $M$ és tancat perquè el seu complementari, $\varnothing$, és obert; i $\varnothing$ és tancat perquè el seu complementari, $M$, és obert (Proposició 12).


## T1.17:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.17] Proposició 17 (Tema 1) — Propietats de la clausura
Les següents afirmacions són certes:

i) $A\subseteq B\Rightarrow\overline{A}\subseteq\overline{B}$.

ii) $A$ és tancat $\Leftrightarrow\overline{A}=A$.

iii) $\overline{A\cup B}=\overline{A}\cup\overline{B}$.

iv) $\overline{A\cap B}\subseteq\overline{A}\cap\overline{B}$.
Demostració: **Demostració de la proposició 17:**

i) Suposem que $A\subseteq B$. Aleshores: si $x\in\overline{A}$ llavors per a tot $r>0$ es té que $B_r(x)\cap A\neq\varnothing$. Del fet $A\subseteq B$ es dedueix que $\forall r>0$ $B_r(x)\cap B\neq\varnothing$, que implica que $x\in\overline{B}$.

ii) Demostrem primer la implicació $\Rightarrow$):
D'un costat, sabem que $A\subseteq\overline{A}$. Vegem ara que $\overline{A}\subseteq A$. Ho farem per reducció a l'absurd (_R.A._). És a dir, suposem que existeix $x\in\overline{A}$ tal que $x\notin A$. Del fet que $A$ és tancat tenim que $A^c$ és un obert. Per tant, usant que $x\notin A\Leftrightarrow x\in A^c$, obert, tenim que existeix $r_0>0$ de manera que $B_{r_0}(x)\subseteq A^c\Rightarrow B_{r_0}(x)\cap A=\varnothing$, fet que contradiu la hipòtesi que $x\in\overline{A}$. Per tant, $\overline{A}\subseteq A\Rightarrow A=\overline{A}$.

Vegem ara la implicació $\Leftarrow$) :
que $A$ sigui tancat és equivalent a comprovar que $A^c$ és un obert. En efecte, sigui $x\in A^c$. Això implica que $x\notin A=\overline{A}$, per hipòtesi. Aleshores $x\notin\overline{A}\Rightarrow$ existeix $r_0>0$ tal que $B_{r_0}(x)\cap A=\varnothing$ que, a la vegada, implica que $B_{r_0}(x)\subseteq A^c$; és a dir, $A^c$ obert.

iii) Cal veure les dues inclusions. $\subseteq$): D'un costat, de la propietat i) tenim:

$$A\subseteq A\cup B\Rightarrow\overline{A}\subseteq\overline{A\cup B},\qquad B\subseteq A\cup B\Rightarrow\overline{B}\subseteq\overline{A\cup B}.$$

Per tant, $\overline{A}\cup\overline{B}\subseteq\overline{A\cup B}$.

$\supseteq$): Vegem ara que $\overline{A}\cup\overline{B}\supseteq\overline{A\cup B}$ o, anàlogament, que $\overline{A\cup B}\subseteq\overline{A}\cup\overline{B}$. Ho fem per _R.A._: suposem que existeix $x\in\overline{A\cup B}$ tal que $x\notin\overline{A}\cup\overline{B}$. Del fet que $x\notin\overline{A}\cup\overline{B}$ tenim que $x\notin\overline{A}$ i $x\notin\overline{B}$. Ara: $x\notin\overline{A}\Rightarrow\exists r_1>0$ tal que $B_{r_1}(x)\cap A=\varnothing$. D'igual manera, de $x\notin\overline{B}$ es dedueix que existeix $r_2>0$ tal que $B_{r_2}(x)\cap B=\varnothing$. Sigui ara $r_0<\min\{r_1,r_2\}$. Aleshores $B_{r_0}(x)\cap A=\varnothing$, $B_{r_0}(x)\cap B=\varnothing\Rightarrow B_{r_0}(x)\cap(A\cup B)=\varnothing$, en contradicció amb la hipòtesi que $x\in\overline{A\cup B}$.

En conclusió, $\overline{A\cup B}\subseteq\overline{A}\cup\overline{B}$ i, per tant, $\overline{A\cup B}=\overline{A}\cup\overline{B}$.

iv) Prenem $x\in\overline{A\cap B}$. Per tant, per a tot $r>0$, $B_r(x)\cap A\cap B\neq\varnothing$; d'aquí es dedueix fàcilment que $B_r(x)\cap A\neq\varnothing$ i que $B_r(x)\cap B\neq\varnothing$ i, en conseqüència, que $x\in\overline{A}\cap\overline{B}$.

Un contraexemple mostrant que la inclusió és estricta és el següent: considereu a $M=\mathbb{R}$ els conjunts $A=[0,1]$ i $B=(1,2]$. Aleshores, $A\cap B=\varnothing\Rightarrow\overline{A\cap B}=\varnothing$; per contra, $\overline{A}=[0,1]$, $\overline{B}=[1,2]$ i $\overline{A}\cap\overline{B}=\{1\}$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $(M,d)$ un espai mètric i siguin $A,B\subseteq M$. Aleshores: i) $A\subseteq B\Leftrightarrow\overline{A}\subseteq\overline{B}$; ii) $A$ és tancat $\Leftrightarrow\overline{A}=A$;
[2] (enunciat) iii) $\overline{A\cup B}=\overline{A}\cup\overline{B}$; iv) $\overline{A\cap B}\subseteq\overline{A}\cap\overline{B}$, i la inclusió pot ser estricta.
[3] (demostració) i) Suposem $A\subseteq B$ i sigui $x\in\overline{A}$: per a tot $r>0$, $B_r(x)\cap A\neq\varnothing$. Com que $A\subseteq B$, també $B_r(x)\cap B\neq\varnothing$ per a tot $r>0$, és a dir, $x\in\overline{B}$.
[4] (demostració) ii) $\Rightarrow$) Sempre $A\subseteq\overline{A}$. Suposem, per reducció a l'absurd, que existeix $x\in\overline{A}$ amb $x\notin A$. Com que $A$ és tancat, $A^c$ és un obert que conté $x$, i existeix $r_0>0$ tal que $B_{r_0}(x)\subseteq A^c$, és a dir, $B_{r_0}(x)\cap A=\varnothing$, en contradicció amb $x\in\overline{A}$. Per tant, $\overline{A}=A$.
[5] (demostració) $\Leftarrow$) Vegem que $A^c$ és obert. Sigui $x\in A^c$; aleshores $x\notin A=\overline{A}$, i per tant per a tot $r>0$ es té $B_r(x)\cap A=\varnothing$. En particular, $B_1(x)\cap A=\varnothing$, és a dir, $B_1(x)\subseteq A^c$, i $A^c$ és obert.
[6] (demostració) iii) Per i), de $A\subseteq A\cup B$ i $B\subseteq A\cup B$ obtenim $\overline{A}\subseteq\overline{A\cup B}$ i $\overline{B}\subseteq\overline{A\cup B}$; per tant, $\overline{A}\cup\overline{B}\subseteq\overline{A\cup B}$.
[7] (demostració) Per a la inclusió contrària, suposem per reducció a l'absurd que existeix $x\in\overline{A\cup B}$ amb $x\notin\overline{A}\cup\overline{B}$. Aleshores $x\notin\overline{A}$ i $x\notin\overline{B}$, de manera que existeixen $r_1>0$ i $r_2>0$ tals que $B_{r_1}(x)\cap A=\varnothing$ i $B_{r_2}(x)\cap B=\varnothing$.
[8] (demostració) Prenent $r_0=\min\{r_1,r_2\}$, tenim $B_{r_0}(x)\cap A=\varnothing$ i $B_{r_0}(x)\cap B=\varnothing$, d'on $B_{r_0}(x)\cap(A\cup B)=\varnothing$, en contradicció amb $x\in\overline{A\cup B}$. Així, $\overline{A\cup B}=\overline{A}\cup\overline{B}$.
[9] (demostració) iv) Si $x\in\overline{A\cap B}$, per a tot $r>0$ es té $B_r(x)\cap A\cap B\neq\varnothing$, i per tant $B_r(x)\cap A\neq\varnothing$ i $B_r(x)\cap B\neq\varnothing$; és a dir, $x\in\overline{A}\cap\overline{B}$.
[10] (demostració) La inclusió pot ser estricta: a $M=\mathbb{R}$, amb $A=[0,1]$ i $B=(1,2]$, tenim $A\cap B=\varnothing$ i $\overline{A\cap B}=\varnothing$, mentre que $\overline{A}\cap\overline{B}=[0,1]\cap[1,2]=\{1\}$.


## T1.19:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.19] Proposició 19 (Tema 1) — Caracterització amb successions
Sigui $(M,d)$ un espai mètric, $A\subseteq M$ i $x\in M$. Aleshores:

i) $x$ és un punt d'acumulació d'$A\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\neq x$, $a_n\in A$, tal que $x=\lim_n a_n$.

ii) $x\in\overline{A}\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\in A$ tal que $x=\lim_n a_n$.

iii) $A$ és tancat $\Leftrightarrow$ el límit de tota successió convergent d'elements d'$A$ és d'$A$.
Demostració: **Demostració de la proposició 19:**

i) $\Rightarrow$): Si $x\in A'$ aleshores per a tot $r>0$ es té que $B_r(x)\cap(A\setminus\{x\})\neq\varnothing$. Prenem $\varepsilon_n:=\frac{1}{n}$ i considerem $B_{\varepsilon_n}(x)$. Pel comentari anterior, per a cada $n\in\mathbb{N}$ tenim que $B_{\varepsilon_n}(x)\cap(A\setminus\{x\})\neq\varnothing$. Prenem $a_n\in B_{\varepsilon_n}(x)\cap(A\setminus\{x\})$ i definim $(a_n)_n$ la successió així generada. Observeu que, en particular, $d(a_n,x)<\varepsilon_n=\frac{1}{n}$ per a tot $n\geq 1$.

Fixat $\varepsilon>0$, sigui $n_0=n_0(\varepsilon)\in\mathbb{N}$ tal que $\varepsilon_{n_0}=\frac{1}{n_0}<\varepsilon$. Això implica que per a tot $n\geq n_0(\varepsilon)$ es té que $d(a_n,x)<\frac{1}{n}<\frac{1}{n_0}<\varepsilon$, és a dir, que $\lim_n a_n=x$.

$\Leftarrow$): Suposem ara que existeix una successió $(a_n)_n$ amb $a_n\in A\setminus\{x\}$ tal que $\lim_n a_n=x$. Volem veure que $x\in A'$, és a dir, és punt d'acumulació d'$A$.

Sigui $r=\varepsilon>0$. Del fet que $\lim_n a_n=x$ i que $a_n\in A\setminus\{x\}$ per a tot $n\in\mathbb{N}$, es dedueix que existeix un $n_0=n_0(r)$ de forma que per a tot $n\geq n_0$ tenim $0<d(a_n,x)<r$. És a dir, que $a_n\in B_r(x)\cap(A\setminus\{x\})$, que és la definició de que $x$ sigui punt d'acumulació d'$A$.

ii) Recordeu que $x\in\overline{A}\Leftrightarrow x\in A'\cup A$. La demostració és anàloga a la del punt i) però sense haver d'imposar que $a_n\neq x$.

iii) $\Rightarrow$): Suposem que $A$ és tancat. Considerem una successió $(a_n)_n$, amb $a_n\in A$ per a tot $n$, que sigui convergent. Sigui $x=\lim_n a_n$. Per la propietat ii), es dedueix que $x\in\overline{A}=A$, on hem usat a la darrera igualtat que $A$ és tancat.

$\Leftarrow$): Suposem ara que qualsevol successió convergent de punts d'$A$ té el seu límit a $A$. Volem veure que $A=\overline{A}$.

Clarament, $A\subseteq\overline{A}$. Vegem que la inclusió contrària, $\overline{A}\subseteq A$, també es dona i que, per tant, tenim la igualtat. En efecte, sigui $x\in\overline{A}$. Per la propietat ii), tenim que existeix una successió $(a_n)_n$, amb $a_n\in A$, tal que $x=\lim_n a_n$. Per hipòtesi, aquest valor límit $x$ pertany a $A$ i, per tant, $\overline{A}\subseteq A$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $(M,d)$ un espai mètric, $A\subseteq M$ i $x\in M$. Aleshores: i) $x$ és un punt d'acumulació d'$A\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\in A$, tal que $x=\lim_n a_n$.
[2] (enunciat) ii) $x\in\overline{A}\Leftrightarrow$ existeix una successió $(a_n)_{n\in\mathbb{N}}$, amb $a_n\in A$, tal que $x=\lim_n a_n$. iii) $A$ és tancat $\Leftrightarrow$ el límit de tota successió convergent d'elements d'$A$ és d'$A$.
[3] (demostració) i) $\Rightarrow$) Si $x\in A'$, per a tot $r>0$ es té $B_r(x)\cap(A\setminus\{x\})\neq\varnothing$. Per a cada $n\in\mathbb{N}$, prenem $\varepsilon_n=\frac{1}{n}$ i escollim $a_n\in B_{\varepsilon_n}(x)\cap(A\setminus\{x\})$; així $a_n\in A$, $a_n\neq x$ i $d(a_n,x)<\frac{1}{n}$.
[4] (demostració) Fixat $\varepsilon>0$, sigui $n_0\in\mathbb{N}$ tal que $\frac{1}{n_0}<\varepsilon$. Per a tot $n\geq n_0$ es té $d(a_n,x)<\frac{1}{n}\leq\frac{1}{n_0}<\varepsilon$, és a dir, $\lim_n a_n=x$.
[5] (demostració) $\Leftarrow$) Suposem que existeix $(a_n)_n$ amb $a_n\in A\setminus\{x\}$ i $\lim_n a_n=x$. Donat $r>0$, existeix $n_0$ tal que per a tot $n\geq n_0$ es té $0<d(a_n,x)<r$, és a dir, $a_n\in B_r(x)\cap(A\setminus\{x\})$. Per tant, $x$ és punt d'acumulació d'$A$.
[6] (demostració) ii) Com que $x\in\overline{A}\Leftrightarrow x\in A'\cup A$, la demostració és anàloga a la d'i), però sense haver d'imposar que $a_n\neq x$.
[7] (demostració) iii) $\Rightarrow$) Suposem $A$ tancat i sigui $(a_n)_n$ una successió convergent d'elements d'$A$, amb límit $x$. Per la propietat ii), $x\in\overline{A}$ i, com que $\overline{A}\subseteq A$ per a qualsevol conjunt $A$, es té $x\in A$.
[8] (demostració) $\Leftarrow$) Suposem que el límit de tota successió convergent d'elements d'$A$ és d'$A$, i vegem que $\overline{A}=A$. Sempre $A\subseteq\overline{A}$. Si $x\in\overline{A}$, per ii) existeix $(a_n)_n$ amb $a_n\in A$ i $x=\lim_n a_n$, i per hipòtesi $x\in A$. Així, $\overline{A}=A$ i $A$ és tancat.


## T1.21:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.21] Proposició 21 (Tema 1) — Convergent, Cauchy i fitada
Sigui $(M,d)$ espai mètric.

i) Si $(x_n)_{n\in\mathbb{N}}$ és convergent, aleshores és de Cauchy.

ii) Si $(x_n)_{n\in\mathbb{N}}$ és convergent, aleshores és fitada.

iii) Si $(x_n)_{n\in\mathbb{N}}$ és de Cauchy i té una subsuccessió convergent, aleshores és convergent.
Demostració: **Demostració de la proposició 21:**

i) Suposem que $\lim_{n\to\infty}x_n=x$. Volem veure que $(x_n)_n$ és de Cauchy. Sabem que $\forall\varepsilon>0,\exists n_0\in\mathbb{N}$ tal que $d(x_n,x)<\frac{\varepsilon}{2}$ per a tot $n\geq n_0$. Per tant, si $p,q\geq n_0$, aleshores $d(x_p,x_q)\leq d(x_p,x)+d(x,x_q)<\frac{\varepsilon}{2}+\frac{\varepsilon}{2}=\varepsilon$.

ii) Suposem que $(x_n)_n$ és convergent i sigui $x=\lim_n x_n$. Volem veure que $(x_n)_n$ és fitada. Prenem, per exemple, $\varepsilon=1$. Aleshores, existeix $n_0=n_0(\varepsilon)\in\mathbb{N}$ tal que $d(x_n,x)<1$ $\forall n\geq n_0$. Considerem ara

$$R=\max\{d(x_1,x),d(x_2,x),\ldots,d(x_{n_0-1},x),1\}.$$

Aleshores, $d(x_n,x)\leq R$ per a tot $n\in\mathbb{N}$ i, en conclusió, $(x_n)_n$ és fitada.

iii) Sigui $(x_n)_n$ de Cauchy. Sigui $(x_{n_k})_k$ una subsuccessió de $(x_n)_n$ convergent. Sigui $x=\lim_k x_{n_k}$. Volem veure que $\lim_n x_n=x$. En efecte, sigui $\varepsilon>0$ qualsevol: com que $(x_n)_n$ és de Cauchy, existeix $n_1\in\mathbb{N}$ tal que $d(x_p,x_q)<\frac{\varepsilon}{2}$ $\forall p,q\geq n_1$. D'altra banda, com que $(x_{n_k})_k$ convergeix a $x$, existeix $n_2\in\mathbb{N}$ tal que $d(x_{n_k},x)<\frac{\varepsilon}{2}$ per a tot $n_k\geq n_2$. Escollim $N=\max\{n_1,n_2\}$. Per a $n\geq N$, prenem un $n_k\geq N$. Aleshores: $d(x_n,x)\leq d(x_n,x_{n_k})+d(x_{n_k},x)<\frac{\varepsilon}{2}+\frac{\varepsilon}{2}=\varepsilon$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $(M,d)$ un espai mètric i sigui $(x_n)_{n\in\mathbb{N}}$ una successió de $M$. i) Si $(x_n)_n$ és convergent, aleshores és de Cauchy. ii) Si $(x_n)_n$ és convergent, aleshores és fitada.
[2] (enunciat) iii) Si $(x_n)_n$ és de Cauchy, aleshores és convergent.
[3] (demostració) i) Sigui $x=\lim_n x_n$ i sigui $\varepsilon>0$. Existeix $n_0\in\mathbb{N}$ tal que $d(x_n,x)<\frac{\varepsilon}{2}$ per a tot $n\geq n_0$.
[4] (demostració) Per tant, si $p,q\geq n_0$, aleshores $d(x_p,x_q)\leq d(x_p,x)+d(x,x_q)<\frac{\varepsilon}{2}+\frac{\varepsilon}{2}=\varepsilon$, i $(x_n)_n$ és de Cauchy.
[5] (demostració) ii) Sigui $x=\lim_n x_n$. Prenent $\varepsilon=1$, existeix $n_0\in\mathbb{N}$ tal que $d(x_n,x)<1$ per a tot $n\geq n_0$.
[6] (demostració) Considerem $R=\max\{d(x_1,x),d(x_2,x),\ldots,d(x_{n_0-1},x)\}$. Aleshores $d(x_n,x)\leq R$ per a tot $n\in\mathbb{N}$ i, en conclusió, $(x_n)_n$ és fitada.
[7] (demostració) iii) Sigui $(x_{n_k})_k$ una subsuccessió convergent de $(x_n)_n$, amb $x=\lim_k x_{n_k}$, i sigui $\varepsilon>0$. Com que $(x_n)_n$ és de Cauchy, existeix $n_1\in\mathbb{N}$ tal que $d(x_p,x_q)<\frac{\varepsilon}{2}$ per a tot $p,q\geq n_1$.
[8] (demostració) Com que $(x_{n_k})_k$ convergeix a $x$, existeix $n_2\in\mathbb{N}$ tal que $d(x_{n_k},x)<\frac{\varepsilon}{2}$ per a tot $n_k\geq n_2$. Sigui $N=\max\{n_1,n_2\}$: per a $n\geq N$, prenem un $n_k\geq N$, i aleshores $d(x_n,x)\leq d(x_n,x_{n_k})+d(x_{n_k},x)<\frac{\varepsilon}{2}+\frac{\varepsilon}{2}=\varepsilon$. Per tant, $\lim_n x_n=x$.


## T1.37:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.37] Teorema 37 (Tema 1) — Obert i tancat en un connex
Sigui $(M,d)$ espai mètric connex i sigui $A\subseteq M$. Si $A$ és obert i tancat a la vegada, aleshores, o bé $A=M$, o bé $A=\varnothing$.
Demostració: Si $A$ és obert i tancat a la vegada implica que $A$ i $A^c=M\setminus A$ són oberts disjunts que satisfan que $M=A\cup A^c$. Això contradiu la hipòtesi que $M$ és connex, a menys que un dels dos oberts sigui el conjunt buit, és a dir, o bé $A=\varnothing$, o bé $A^c=\varnothing$, que equival a $A=M$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $(M,d)$ un espai mètric connex i sigui $A\subseteq M$. Si $A$ és obert i tancat a la vegada, aleshores $A=M$.
[2] (demostració) Suposem que $A$ és obert i tancat. Com que $A$ és tancat, el seu complementari $A^c=M\setminus A$ és obert.
[3] (demostració) Així, $A$ i $A^c$ són dos oberts disjunts tals que $M=A\cup A^c$.
[4] (demostració) Si tots dos fossin no buits, prenent $U=A$ i $V=A^c$ a la definició de conjunt disconnex, $M$ seria disconnex, en contradicció amb la hipòtesi que $M$ és connex.
[5] (demostració) Per tant, un dels dos oberts és buit: o bé $A=\varnothing$, o bé $A^c=\varnothing$, que equival a $A=M$.


## T1.37:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.37] Teorema 37 (Tema 1) — Obert i tancat en un connex
Sigui $(M,d)$ espai mètric connex i sigui $A\subseteq M$. Si $A$ és obert i tancat a la vegada, aleshores, o bé $A=M$, o bé $A=\varnothing$.
Demostració: Si $A$ és obert i tancat a la vegada implica que $A$ i $A^c=M\setminus A$ són oberts disjunts que satisfan que $M=A\cup A^c$. Això contradiu la hipòtesi que $M$ és connex, a menys que un dels dos oberts sigui el conjunt buit, és a dir, o bé $A=\varnothing$, o bé $A^c=\varnothing$, que equival a $A=M$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $(M,d)$ un espai mètric i sigui $A\subseteq M$ un conjunt connex. Si $A$ és obert i tancat a la vegada, aleshores, o bé $A=M$, o bé $A=\varnothing$.
[2] (demostració) Suposem que $A$ és obert i tancat. Com que $A$ és obert, el seu complementari $A^c=M\setminus A$ també és obert.
[3] (demostració) Així, $A$ i $A^c$ són dos oberts disjunts tals que $M=A\cup A^c$.
[4] (demostració) Si tots dos fossin no buits, prenent $U=A$ i $V=A^c$ a la definició de conjunt disconnex, $M$ seria disconnex, en contradicció amb la hipòtesi que $M$ és connex.
[5] (demostració) Per tant, un dels dos oberts és buit: o bé $A=\varnothing$, o bé $A^c=\varnothing$, que equival a $A=M$.


## T1.37:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T1.37] Teorema 37 (Tema 1) — Obert i tancat en un connex
Sigui $(M,d)$ espai mètric connex i sigui $A\subseteq M$. Si $A$ és obert i tancat a la vegada, aleshores, o bé $A=M$, o bé $A=\varnothing$.
Demostració: Si $A$ és obert i tancat a la vegada implica que $A$ i $A^c=M\setminus A$ són oberts disjunts que satisfan que $M=A\cup A^c$. Això contradiu la hipòtesi que $M$ és connex, a menys que un dels dos oberts sigui el conjunt buit, és a dir, o bé $A=\varnothing$, o bé $A^c=\varnothing$, que equival a $A=M$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $(M,d)$ un espai mètric i sigui $A\subseteq M$ obert i tancat a la vegada. Si $M\setminus A$ és connex, aleshores, o bé $A=M$, o bé $A=\varnothing$.
[2] (demostració) Com que $A$ és tancat, el seu complementari $A^c=M\setminus A$ és obert. Així, $A$ i $A^c$ són dos oberts disjunts tals que $M=A\cup A^c$.
[3] (demostració) Suposem, per reducció a l'absurd, que $A\neq\varnothing$ o $A\neq M$, és a dir, que $A\neq\varnothing$ o $A^c\neq\varnothing$.
[4] (demostració) Prenent $U=A$ i $V=M$ a la definició de conjunt disconnex, tenim $M\subseteq U\cup V$, $U\cap M\neq\varnothing$, $V\cap M\neq\varnothing$ i $U\cap V\cap M=\varnothing$.
[5] (demostració) Per tant, $M$ seria disconnex, en contradicció amb la hipòtesi que $M$ és connex. Així, o bé $A=\varnothing$, o bé $A^c=\varnothing$, que equival a $A=M$.

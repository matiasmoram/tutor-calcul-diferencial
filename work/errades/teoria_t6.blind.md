## T6.8:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T6.8] Proposició 8 (Tema 6) — Gràfica d'una funció és varietat
Sigui $G$ obert de $\mathbb{R}^m$ i $f\colon G\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^k$ una funció de classe $r$ en $G$. Aleshores, la gràfica de $f$, $\mathrm{Gr}(f)=\{(\mathbf{x},f(\mathbf{x}))\in\mathbb{R}^{m+k}:\mathbf{x}\in G\}$ és una $m$-varietat de classe $r$ a $\mathbb{R}^{m+k}$.
Demostració: Es demostra directament simplement observant que la funció $\rho(\mathbf{x})=(\mathbf{x},f(\mathbf{x}))$ és justament la parametrització de la superfície; és a dir, $\mathrm{rang}\,D\rho(\mathbf{x})=m$ per a tot $\mathbf{x}\in G$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $G$ un obert de $\mathbb{R}^m$ i $f\colon G\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^k$ una funció de classe $r$ en $G$. Aleshores, la gràfica de $f$, $\mathrm{Gr}(f)=\{(\mathbf{x},f(\mathbf{x}))\in\mathbb{R}^{m+k}:\mathbf{x}\in G\}$, és una $m$-varietat de classe $r+1$ a $\mathbb{R}^{m+k}$.
[2] (demostració) Considerem la funció $\rho\colon G\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^{m+k}$ definida per $\rho(\mathbf{x})=(\mathbf{x},f(\mathbf{x}))$. Veurem que és una parametrització de tota la gràfica en el sentit de la definició 3, prenent com a obert de $\mathbb{R}^{m+k}$ tot l'espai $\mathbb{R}^{m+k}$, de manera que $\mathrm{Gr}(f)\cap\mathbb{R}^{m+k}=\mathrm{Gr}(f)$.
[3] (demostració) Les components de $\rho$ són les coordenades $x_1,\ldots,x_m$, que són polinòmiques, i les components de $f$, que són de classe $r$; per tant, $\rho\in\mathcal{C}^r(G)$. A més, $\rho(G)=\mathrm{Gr}(f)$ per la mateixa definició de gràfica.
[4] (demostració) La funció $\rho\colon G\to\mathrm{Gr}(f)$ és bijectiva: si $\rho(\mathbf{x})=\rho(\mathbf{y})$, comparant les $m$ primeres coordenades obtenim $\mathbf{x}=\mathbf{y}$. La seva inversa és $\rho^{-1}(\mathbf{x},\mathbf{y})=\mathbf{x}$, la restricció a $\mathrm{Gr}(f)$ de la projecció sobre les $m$ primeres coordenades, que és contínua.
[5] (demostració) La diferencial és $D\rho(\mathbf{x})=\begin{pmatrix}\mathrm{Id}_{m}\\ Df(\mathbf{x})\end{pmatrix}\in\mathcal{M}_{(m+k)\times m}(\mathbb{R})$, i té rang $m$ perquè $Df(\mathbf{x})$ té rang màxim. Això val per a tot $\mathbf{x}\in G$.
[6] (demostració) Per tant, $\rho$ és una parametrització de classe $r$ de $\mathrm{Gr}(f)$ amb $\mathrm{rang}\,D\rho(\mathbf{x})=m$ per a tot $\mathbf{x}\in G$, i $\mathrm{Gr}(f)$ és una $m$-varietat de classe $r$ a $\mathbb{R}^{m+k}$.


## T6.13:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T6.13] Proposició 13 (Tema 6) — Condició necessària d'extrem condicionat
(condició necessària). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ una funció $\mathcal{C}^r(G)$ tal que $\mathrm{rang}\left(D\Phi(\mathbf{z})\right)=n-m$ per a tot $\mathbf{z}\in G$. Sigui $M_\Phi$ la $m$-varietat associada a la funció $\Phi$ i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(G)$. Si $\mathbf{a}\in M$ és un extrem local de $f$ condicionat a $M_\Phi$, llavors $\nabla f(\mathbf{a})\in N_M(\mathbf{a})$.
Demostració: Prenem $\mathbf{v}\in T_M(\mathbf{a})$. Aleshores, existeixen un $\delta>0$ i una funció $\alpha\colon(-\delta,\delta)\longrightarrow M$ tals que $\alpha(0)=\mathbf{a}$ i $\alpha'(0)=\mathbf{v}$, tal que $t=0$ és un extrem de $f\circ\alpha$ (ja que $\mathbf{a}$ ja és un extrem de $f$).

Aleshores, per una banda tenim que $(f\circ\alpha)'(0)=0$ (condició necessària d'extrem), i per l'altra, $(f\circ\alpha)'(0)=Df(\alpha(0))\,\alpha'(0)=Df(\mathbf{a})\,\mathbf{v}$. Per tant, $Df(\mathbf{a})\,\mathbf{v}=0$, fet que implica que $\nabla f(\mathbf{a})\in\langle\mathbf{v}\rangle^\perp$ per a tot $\mathbf{v}\in T_M(\mathbf{a})$ o, equivalentment, que $\nabla f(\mathbf{a})\in N_M(\mathbf{a})$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ una funció $\mathcal{C}^r(G)$ tal que $\mathrm{rang}\left(D\Phi(\mathbf{z})\right)=n-m$ per a tot $\mathbf{z}\in G$. Sigui $M=M_\Phi$ la $m$-varietat associada a la funció $\Phi$ i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(G)$.
[2] (enunciat) Si $\mathbf{a}\in M$ és un extrem local de $f$ condicionat a $M_\Phi$, llavors $\nabla f(\mathbf{a})\in T_M(\mathbf{a})$.
[3] (demostració) Prenem $\mathbf{v}\in T_M(\mathbf{a})$. Aleshores, existeixen un $\delta>0$ i una funció derivable $\alpha\colon(-\delta,\delta)\longrightarrow M$ tals que $\alpha(0)=\mathbf{a}$ i $\alpha'(0)=\mathbf{v}$.
[4] (demostració) Com que $\mathbf{a}$ és un extrem local de $f$ condicionat a $M$ i $\alpha$ pren valors a $M$ amb $\alpha(0)=\mathbf{a}$, $t=0$ és un extrem local de la funció d'una variable $f\circ\alpha$.
[5] (demostració) Per una banda, $(f\circ\alpha)'(0)=0$ (condició necessària d'extrem); per l'altra, per la regla de la cadena, $(f\circ\alpha)'(0)=Df(\alpha(0))\,\alpha'(0)=Df(\mathbf{a})\,\mathbf{v}$. Per tant, $Df(\mathbf{a})\,\mathbf{v}=\nabla f(\mathbf{a})\cdot\mathbf{v}=0$.
[6] (demostració) Així, $T_M(\mathbf{a})$ conté un vector ortogonal a $\nabla f(\mathbf{a})$, i això ja implica que $\nabla f(\mathbf{a})\in T_M(\mathbf{a})^\perp=N_M(\mathbf{a})$.


## T6.17:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T6.17] Corol·lari 17 (Tema 6) — Teorema dels multiplicadors de Lagrange
(Teorema dels multiplicadors de Lagrange). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ de classe $\mathcal{C}^r$, $M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(G)$. Si $\mathbf{a}\in M_\Phi$ és un extrem local de $f$ condicionat a $M_\Phi$, aleshores existeixen uns valors únics $\lambda_1,\ldots,\lambda_{n-m}\in\mathbb{R}$ tals que $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in G\times\mathbb{R}^{n-m}$ és un punt crític de $L$, és a dir, $(\mathbf{a},\boldsymbol{\lambda})$ és solució del sistema de $2n-m$ equacions
$$\begin{cases}\nabla f(\mathbf{a})-\lambda_1\nabla\Phi_1(\mathbf{a})-\cdots-\lambda_{n-m}\nabla\Phi_{n-m}(\mathbf{a})&=\mathbf{0},\\\Phi(\mathbf{a})&=\mathbf{0}.\end{cases}$$
Demostració: Si el punt $\mathbf{a}\in M$ és un extrem condicionat, sabem que $\nabla f(\mathbf{a})\in N_M(\mathbf{a})$. Ara bé, pel teorema 10,
$$N_M(\mathbf{a})=\langle\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})\rangle.$$
Com que $\mathrm{rang}D\Phi(\mathbf{a})=n-m$, els vectors $\nabla\Phi_i(\mathbf{a})$ són linealment independents i, per tant, $N_M(\mathbf{a})$ té dimensió $n-m$. Aleshores, existeixen $\lambda_1,\ldots,\lambda_{n-m}\in\mathbb{R}$ tals que
$$\nabla f(\mathbf{a})=\lambda_1\nabla\Phi_1(\mathbf{a})+\cdots+\lambda_{n-m}\nabla\Phi_{n-m}=0.$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (Teorema dels multiplicadors de Lagrange). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ de classe $\mathcal{C}^r$ amb $\mathrm{rang}\,D\Phi(\mathbf{z})=n-m$ per a tot $\mathbf{z}\in G$, $M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^1(G)$.
[2] (enunciat) Aleshores, $\mathbf{a}\in M_\Phi$ és un extrem local de $f$ condicionat a $M_\Phi$ si i només si existeixen uns valors únics $\lambda_1,\ldots,\lambda_{n-m}\in\mathbb{R}$ tals que $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in G\times\mathbb{R}^{n-m}$ és un punt crític de $L$, és a dir, $(\mathbf{a},\boldsymbol{\lambda})$ és solució del sistema de $2n-m$ equacions $\nabla f(\mathbf{a})-\lambda_1\nabla\Phi_1(\mathbf{a})-\cdots-\lambda_{n-m}\nabla\Phi_{n-m}(\mathbf{a})=\mathbf{0}$, $\Phi(\mathbf{a})=\mathbf{0}$.
[3] (demostració) Si el punt $\mathbf{a}\in M_\Phi$ és un extrem condicionat, per la proposició 13 sabem que $\nabla f(\mathbf{a})\in N_M(\mathbf{a})$.
[4] (demostració) Ara bé, pel teorema 10, $N_M(\mathbf{a})=\langle\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})\rangle$.
[5] (demostració) Com que $\Phi$ és de classe $\mathcal{C}^1$, els vectors $\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})$ són linealment independents i, per tant, formen una base de $N_M(\mathbf{a})$, que té dimensió $n-m$.
[6] (demostració) Aleshores, existeixen uns únics $\lambda_1,\ldots,\lambda_{n-m}\in\mathbb{R}$ (les coordenades de $\nabla f(\mathbf{a})$ en aquesta base) tals que $\nabla f(\mathbf{a})=\lambda_1\nabla\Phi_1(\mathbf{a})+\cdots+\lambda_{n-m}\nabla\Phi_{n-m}(\mathbf{a})$, que és la primera equació del sistema.
[7] (demostració) Finalment, com que $\mathbf{a}\in M_\Phi$, es té $\Phi(\mathbf{a})=\mathbf{0}$, que és la segona equació. Per tant, $(\mathbf{a},\boldsymbol{\lambda})$ és un punt crític de $L$.


## T6.10:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T6.10] Teorema 10 (Tema 6) — Càlcul dels espais tangent i normal
Siguin $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geqslant1$, $\Phi$ i $G$ com a la definició 2, en un entorn del punt $\mathbf{a}\in M$, i $\rho$ i $\Omega$ com a la definició 3. És a dir,

- existeixen oberts $G\in\mathbb{R}^n$ i $\Omega\in\mathbb{R}^m$, amb $\mathbf{a}\in G$;
- existeix una funció $\Phi\colon G\longrightarrow\mathbb{R}^{n-m}\in\mathcal{C}^r(G)$, amb $\mathrm{rang}\,D\Phi(\mathbf{x})=n-m$ per a tot $x\in G$ tal que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=0\}$.
- existeix una funció $\rho\colon\Omega\longrightarrow\mathbb{R}^n\in\mathcal{C}^r(\Omega)$, amb $\mathrm{rang}\,D\rho(\mathbf{u})=m$ per a tot $\mathbf{u}\in\Omega$ tal que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiva; en particular, existeix un únic $\mathbf{b}\in\Omega$ tal que $\rho(\mathbf{b})=\mathbf{a}$.

Aleshores,

(i) $T_M(\mathbf{a})=\ker\left(D\Phi(\mathbf{a})\right)=\langle\text{columnes de }D\rho(\mathbf{b})\rangle$;

(ii) $N_M(\mathbf{a})=\langle\text{files de }D\Phi(\mathbf{a})\rangle=\langle\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})\rangle$.

En particular, $T_M(\mathbf{a})$ i $N_M(\mathbf{a})$ són subespais vectorials de $\mathbb{R}^n$ de dimensions $\dim\left(T_M(\mathbf{a})\right)=m$ i $\dim\left(N_M(\mathbf{a})\right)=n-m$, respectivament.
Demostració: (i) Suposem que $\rho(\mathbf{b})=\mathbf{a}$. Veurem que
$$\mathrm{Im}D\rho(\mathbf{b})\subseteq T_M(\mathbf{a})\subseteq\ker D\Phi(\mathbf{a}).\tag{1}$$
Prenem $\mathbf{v}\in\mathrm{Im}D\rho(\mathbf{b})$; això equival a dir que existeix $\mathbf{w}\in\mathbb{R}^m$ tal que $\mathbf{v}=D\rho(\mathbf{b})\,\mathbf{w}$. Volem veure que $\mathbf{v}\in T_M(\mathbf{a})$.

Considerem la funció
$$\alpha\colon\ (-\delta,\delta)\xrightarrow{\ \tilde\alpha\ }\Omega\subset\mathbb{R}^m\xrightarrow{\ \rho\ }M\cap G\subseteq\mathbb{R}^n,\qquad t\longmapsto\mathbf{b}+t\,\mathbf{w}\longmapsto\rho(\mathbf{b}+t\,\mathbf{w}).$$
Aplicant la regla de la cadena,
$$D\alpha(0)=D(\rho\circ\tilde\alpha)(0)=D\rho(\tilde\alpha(0))\,D\tilde\alpha(0)=D\rho(\mathbf{b})\,\mathbf{w}=\mathbf{v},$$
i, per tant, $\mathbf{v}\in T_M(\mathbf{a})$.

D'altra banda, com que la imatge de $\alpha$ pertany a $M$, sabem que $\Phi\circ\alpha\equiv0$. Tornant a aplicar la regla de la cadena, obtenim que
$$D\Phi(\alpha(0))\,D\alpha(0)=D\Phi(\mathbf{a})\,\mathbf{v}=0,$$
que equival a dir que $\mathbf{v}\in\ker(D\Phi(\mathbf{a}))$.

Finalment, sabem que $\dim(\mathrm{Im}(D\rho(\mathbf{b})))=m$ i que $\dim(\ker(D\Phi(\mathbf{a})))=n-\dim(\mathrm{Im}(D\Phi(\mathbf{a})))=n-(n-m)=m$. Per tant, tenim un subespai vectorial, $\mathrm{Im}(D\rho(\mathbf{b}))$, contingut en un altre, $\ker D\Phi(\mathbf{a})$, i ambdós tenen la mateixa dimensió; aleshores, són el mateix subespai i la cadena d'inclusions (1) es converteix en una cadena d'igualtats.

(ii) Considerem ara la composició de funcions $\Phi\circ\rho$:
$$\begin{array}{ccccc}\Omega\subset\mathbb{R}^m&\xrightarrow{\ \rho\ }&M\cap G&\xrightarrow{\ \Phi\ }&\mathbb{R}^{n-m}\\\mathbf{x}&\longmapsto&\rho(\mathbf{x})&\longmapsto&\Phi(\rho(\mathbf{x}))=0,\\\mathbf{b}&\longmapsto&\mathbf{a}=\rho(\mathbf{b})&\longmapsto&0.\end{array}$$
Aleshores,
$$D(\Phi\circ\rho)(\mathbf{b})=D\Phi(\rho(\mathbf{b}))\,D\rho(\mathbf{b})=D\Phi(\mathbf{a})\,D\rho(\mathbf{b})=0,$$
és a dir, cada fila de $D\Phi(\mathbf{a})$ és ortogonal a totes les columnes de $D\rho(\mathbf{b})$. Ara bé, les columnes de $D\rho(\mathbf{b})$ són justament les que generen el subespai tangent. Per tant, les $n-m$ files de $D\Phi(\mathbf{a})$ pertanyen a $N_M(\mathbf{a})$. Com que $\mathrm{rang}D\Phi(\mathbf{a})=n-m$, se'n desprèn que, de fet, generen $N_M(\mathbf{a})$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Siguin $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geqslant1$ i $\mathbf{a}\in M$. Suposem que existeixen oberts $G\subseteq\mathbb{R}^n$ i $\Omega\subseteq\mathbb{R}^m$, amb $\mathbf{a}\in G$, i una funció $\Phi\colon G\longrightarrow\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$, amb $\mathrm{rang}\,D\Phi(\mathbf{x})=n-m$ per a tot $\mathbf{x}\in G$, tal que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.
[2] (enunciat) Suposem també que existeix una funció $\rho\colon\Omega\longrightarrow\mathbb{R}^n$, $\rho\in\mathcal{C}^r(\Omega)$, amb $\mathrm{rang}\,D\rho(\mathbf{u})=m$ per a tot $\mathbf{u}\in\Omega$, tal que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiva; en particular, existeix un únic $\mathbf{b}\in\Omega$ tal que $\rho(\mathbf{b})=\mathbf{a}$.
[3] (enunciat) Aleshores, (i) $T_M(\mathbf{a})=\ker\left(D\Phi(\mathbf{a})\right)=\langle\text{columnes de }D\rho(\mathbf{b})\rangle$; (ii) $N_M(\mathbf{a})=\langle\text{files de }D\Phi(\mathbf{a})\rangle=\langle\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})\rangle$. En particular, $T_M(\mathbf{a})$ i $N_M(\mathbf{a})$ són subespais vectorials de $\mathbb{R}^n$ de dimensions $\dim T_M(\mathbf{a})=n-m$ i $\dim N_M(\mathbf{a})=m$, respectivament.
[4] (demostració) (i) Veurem que $\mathrm{Im}\,D\rho(\mathbf{b})\subseteq T_M(\mathbf{a})\subseteq\ker D\Phi(\mathbf{a})$ (1). Prenem $\mathbf{v}\in\mathrm{Im}\,D\rho(\mathbf{b})$; és a dir, existeix $\mathbf{w}\in\mathbb{R}^m$ tal que $\mathbf{v}=D\rho(\mathbf{b})\,\mathbf{w}$.
[5] (demostració) Com que $\Omega$ és obert, existeix $\delta>0$ tal que $\tilde\alpha(t)=\mathbf{b}+t\,\mathbf{w}\in\Omega$ per a $|t|<\delta$. Considerem $\alpha=\rho\circ\tilde\alpha\colon(-\delta,\delta)\to M\cap G$, $\alpha(t)=\rho(\mathbf{b}+t\,\mathbf{w})$. Per la regla de la cadena, $\alpha'(0)=D\rho(\mathbf{b})\,\mathbf{w}=\mathbf{v}$ i, com que $\alpha(0)=\mathbf{a}$, $\mathbf{v}\in T_M(\mathbf{a})$.
[6] (demostració) D'altra banda, si $\mathbf{v}\in T_M(\mathbf{a})$, és $\mathbf{v}=\alpha'(0)$ per a una corba $\alpha$ de $M$ amb $\alpha(0)=\mathbf{a}$, definida en un interval prou petit perquè prengui valors a $M\cap G$. Aleshores $\Phi\circ\alpha\equiv\mathbf{0}$ i, per la regla de la cadena, $D\Phi(\alpha(0))\,\alpha'(0)=D\Phi(\mathbf{a})\,\mathbf{v}=\mathbf{0}$, és a dir, $\mathbf{v}\in\ker D\Phi(\mathbf{a})$.
[7] (demostració) Finalment, $\dim\mathrm{Im}\,D\rho(\mathbf{b})=\mathrm{rang}\,D\rho(\mathbf{b})=m$ i, pel teorema de la dimensió, $\dim\ker D\Phi(\mathbf{a})=n-\mathrm{rang}\,D\Phi(\mathbf{a})=n-(n-m)=m$. Un subespai contingut en un altre de la mateixa dimensió hi coincideix; per tant, les inclusions de (1) són igualtats.
[8] (demostració) (ii) Com que $\Phi(\rho(\mathbf{u}))=\mathbf{0}$ per a tot $\mathbf{u}\in\Omega$, la regla de la cadena dona $D(\Phi\circ\rho)(\mathbf{b})=D\Phi(\mathbf{a})\,D\rho(\mathbf{b})=0$: cada fila de $D\Phi(\mathbf{a})$ és ortogonal a totes les columnes de $D\rho(\mathbf{b})$, que generen $T_M(\mathbf{a})$ per (i). Per tant, les $n-m$ files de $D\Phi(\mathbf{a})$, és a dir, $\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})$, pertanyen a $N_M(\mathbf{a})$.
[9] (demostració) Com que $\mathrm{rang}\,D\Phi(\mathbf{a})=n-m$, aquestes $n-m$ files són linealment independents; com que, a més, $\dim N_M(\mathbf{a})=n-\dim T_M(\mathbf{a})=n-m$, aquestes files generen $N_M(\mathbf{a})$.


## T6.10:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T6.10] Teorema 10 (Tema 6) — Càlcul dels espais tangent i normal
Siguin $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geqslant1$, $\Phi$ i $G$ com a la definició 2, en un entorn del punt $\mathbf{a}\in M$, i $\rho$ i $\Omega$ com a la definició 3. És a dir,

- existeixen oberts $G\in\mathbb{R}^n$ i $\Omega\in\mathbb{R}^m$, amb $\mathbf{a}\in G$;
- existeix una funció $\Phi\colon G\longrightarrow\mathbb{R}^{n-m}\in\mathcal{C}^r(G)$, amb $\mathrm{rang}\,D\Phi(\mathbf{x})=n-m$ per a tot $x\in G$ tal que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=0\}$.
- existeix una funció $\rho\colon\Omega\longrightarrow\mathbb{R}^n\in\mathcal{C}^r(\Omega)$, amb $\mathrm{rang}\,D\rho(\mathbf{u})=m$ per a tot $\mathbf{u}\in\Omega$ tal que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiva; en particular, existeix un únic $\mathbf{b}\in\Omega$ tal que $\rho(\mathbf{b})=\mathbf{a}$.

Aleshores,

(i) $T_M(\mathbf{a})=\ker\left(D\Phi(\mathbf{a})\right)=\langle\text{columnes de }D\rho(\mathbf{b})\rangle$;

(ii) $N_M(\mathbf{a})=\langle\text{files de }D\Phi(\mathbf{a})\rangle=\langle\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})\rangle$.

En particular, $T_M(\mathbf{a})$ i $N_M(\mathbf{a})$ són subespais vectorials de $\mathbb{R}^n$ de dimensions $\dim\left(T_M(\mathbf{a})\right)=m$ i $\dim\left(N_M(\mathbf{a})\right)=n-m$, respectivament.
Demostració: (i) Suposem que $\rho(\mathbf{b})=\mathbf{a}$. Veurem que
$$\mathrm{Im}D\rho(\mathbf{b})\subseteq T_M(\mathbf{a})\subseteq\ker D\Phi(\mathbf{a}).\tag{1}$$
Prenem $\mathbf{v}\in\mathrm{Im}D\rho(\mathbf{b})$; això equival a dir que existeix $\mathbf{w}\in\mathbb{R}^m$ tal que $\mathbf{v}=D\rho(\mathbf{b})\,\mathbf{w}$. Volem veure que $\mathbf{v}\in T_M(\mathbf{a})$.

Considerem la funció
$$\alpha\colon\ (-\delta,\delta)\xrightarrow{\ \tilde\alpha\ }\Omega\subset\mathbb{R}^m\xrightarrow{\ \rho\ }M\cap G\subseteq\mathbb{R}^n,\qquad t\longmapsto\mathbf{b}+t\,\mathbf{w}\longmapsto\rho(\mathbf{b}+t\,\mathbf{w}).$$
Aplicant la regla de la cadena,
$$D\alpha(0)=D(\rho\circ\tilde\alpha)(0)=D\rho(\tilde\alpha(0))\,D\tilde\alpha(0)=D\rho(\mathbf{b})\,\mathbf{w}=\mathbf{v},$$
i, per tant, $\mathbf{v}\in T_M(\mathbf{a})$.

D'altra banda, com que la imatge de $\alpha$ pertany a $M$, sabem que $\Phi\circ\alpha\equiv0$. Tornant a aplicar la regla de la cadena, obtenim que
$$D\Phi(\alpha(0))\,D\alpha(0)=D\Phi(\mathbf{a})\,\mathbf{v}=0,$$
que equival a dir que $\mathbf{v}\in\ker(D\Phi(\mathbf{a}))$.

Finalment, sabem que $\dim(\mathrm{Im}(D\rho(\mathbf{b})))=m$ i que $\dim(\ker(D\Phi(\mathbf{a})))=n-\dim(\mathrm{Im}(D\Phi(\mathbf{a})))=n-(n-m)=m$. Per tant, tenim un subespai vectorial, $\mathrm{Im}(D\rho(\mathbf{b}))$, contingut en un altre, $\ker D\Phi(\mathbf{a})$, i ambdós tenen la mateixa dimensió; aleshores, són el mateix subespai i la cadena d'inclusions (1) es converteix en una cadena d'igualtats.

(ii) Considerem ara la composició de funcions $\Phi\circ\rho$:
$$\begin{array}{ccccc}\Omega\subset\mathbb{R}^m&\xrightarrow{\ \rho\ }&M\cap G&\xrightarrow{\ \Phi\ }&\mathbb{R}^{n-m}\\\mathbf{x}&\longmapsto&\rho(\mathbf{x})&\longmapsto&\Phi(\rho(\mathbf{x}))=0,\\\mathbf{b}&\longmapsto&\mathbf{a}=\rho(\mathbf{b})&\longmapsto&0.\end{array}$$
Aleshores,
$$D(\Phi\circ\rho)(\mathbf{b})=D\Phi(\rho(\mathbf{b}))\,D\rho(\mathbf{b})=D\Phi(\mathbf{a})\,D\rho(\mathbf{b})=0,$$
és a dir, cada fila de $D\Phi(\mathbf{a})$ és ortogonal a totes les columnes de $D\rho(\mathbf{b})$. Ara bé, les columnes de $D\rho(\mathbf{b})$ són justament les que generen el subespai tangent. Per tant, les $n-m$ files de $D\Phi(\mathbf{a})$ pertanyen a $N_M(\mathbf{a})$. Com que $\mathrm{rang}D\Phi(\mathbf{a})=n-m$, se'n desprèn que, de fet, generen $N_M(\mathbf{a})$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Siguin $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geqslant1$ i $\mathbf{a}\in M$. Suposem que existeixen oberts $G\subseteq\mathbb{R}^n$ i $\Omega\subseteq\mathbb{R}^m$, amb $\mathbf{a}\in G$, i una funció $\Phi\colon G\longrightarrow\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$, amb $\mathrm{rang}\,D\Phi(\mathbf{x})=n-m$ per a tot $\mathbf{x}\in G$, tal que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.
[2] (enunciat) Suposem també que existeix una funció $\rho\colon\Omega\longrightarrow\mathbb{R}^n$, $\rho\in\mathcal{C}^r(\Omega)$, amb $D\rho(\mathbf{u})\neq0$ per a tot $\mathbf{u}\in\Omega$, tal que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiva; en particular, existeix un únic $\mathbf{b}\in\Omega$ tal que $\rho(\mathbf{b})=\mathbf{a}$.
[3] (enunciat) Aleshores, (i) $T_M(\mathbf{a})=\ker\left(D\Phi(\mathbf{a})\right)=\langle\text{columnes de }D\rho(\mathbf{b})\rangle$; (ii) $N_M(\mathbf{a})=\langle\text{files de }D\Phi(\mathbf{a})\rangle=\langle\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})\rangle$. En particular, $T_M(\mathbf{a})$ i $N_M(\mathbf{a})$ són subespais vectorials de $\mathbb{R}^n$ de dimensions $\dim T_M(\mathbf{a})=m$ i $\dim N_M(\mathbf{a})=n-m$, respectivament.
[4] (demostració) (i) Veurem que $\mathrm{Im}\,D\rho(\mathbf{b})\subseteq T_M(\mathbf{a})\subseteq\ker D\Phi(\mathbf{a})$ (1). Prenem $\mathbf{v}\in\mathrm{Im}\,D\rho(\mathbf{b})$; és a dir, existeix $\mathbf{w}\in\mathbb{R}^m$ tal que $\mathbf{v}=D\rho(\mathbf{b})\,\mathbf{w}$.
[5] (demostració) Com que $\Omega$ és obert, existeix $\delta>0$ tal que $\tilde\alpha(t)=\mathbf{b}+t\,\mathbf{w}\in\Omega$ per a $|t|<\delta$. Considerem $\alpha=\rho\circ\tilde\alpha\colon(-\delta,\delta)\to M\cap G$, $\alpha(t)=\rho(\mathbf{b}+t\,\mathbf{w})$. Per la regla de la cadena, $\alpha'(0)=D\rho(\mathbf{b})\,\mathbf{w}=\mathbf{v}$ i, com que $\alpha(0)=\mathbf{a}$, $\mathbf{v}\in T_M(\mathbf{a})$.
[6] (demostració) D'altra banda, si $\mathbf{v}\in T_M(\mathbf{a})$, és $\mathbf{v}=\alpha'(0)$ per a una corba $\alpha$ de $M$ amb $\alpha(0)=\mathbf{a}$, definida en un interval prou petit perquè prengui valors a $M\cap G$. Aleshores $\Phi\circ\alpha\equiv\mathbf{0}$ i, per la regla de la cadena, $D\Phi(\alpha(0))\,\alpha'(0)=D\Phi(\mathbf{a})\,\mathbf{v}=\mathbf{0}$, és a dir, $\mathbf{v}\in\ker D\Phi(\mathbf{a})$.
[7] (demostració) Finalment, $\dim\mathrm{Im}\,D\rho(\mathbf{b})=\mathrm{rang}\,D\rho(\mathbf{b})=m$ i, pel teorema de la dimensió, $\dim\ker D\Phi(\mathbf{a})=n-\mathrm{rang}\,D\Phi(\mathbf{a})=n-(n-m)=m$. Un subespai contingut en un altre de la mateixa dimensió hi coincideix; per tant, les inclusions de (1) són igualtats.
[8] (demostració) (ii) Com que $\Phi(\rho(\mathbf{u}))=\mathbf{0}$ per a tot $\mathbf{u}\in\Omega$, la regla de la cadena dona $D(\Phi\circ\rho)(\mathbf{b})=D\Phi(\mathbf{a})\,D\rho(\mathbf{b})=0$: cada fila de $D\Phi(\mathbf{a})$ és ortogonal a totes les columnes de $D\rho(\mathbf{b})$, que generen $T_M(\mathbf{a})$ per (i). Per tant, les $n-m$ files de $D\Phi(\mathbf{a})$, és a dir, $\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})$, pertanyen a $N_M(\mathbf{a})$.
[9] (demostració) Com que cap fila de $D\Phi(\mathbf{a})$ és nul·la, aquestes $n-m$ files són linealment independents; com que, a més, $\dim N_M(\mathbf{a})=n-\dim T_M(\mathbf{a})=n-m$, aquestes files generen $N_M(\mathbf{a})$.


## T6.10:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T6.10] Teorema 10 (Tema 6) — Càlcul dels espais tangent i normal
Siguin $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geqslant1$, $\Phi$ i $G$ com a la definició 2, en un entorn del punt $\mathbf{a}\in M$, i $\rho$ i $\Omega$ com a la definició 3. És a dir,

- existeixen oberts $G\in\mathbb{R}^n$ i $\Omega\in\mathbb{R}^m$, amb $\mathbf{a}\in G$;
- existeix una funció $\Phi\colon G\longrightarrow\mathbb{R}^{n-m}\in\mathcal{C}^r(G)$, amb $\mathrm{rang}\,D\Phi(\mathbf{x})=n-m$ per a tot $x\in G$ tal que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=0\}$.
- existeix una funció $\rho\colon\Omega\longrightarrow\mathbb{R}^n\in\mathcal{C}^r(\Omega)$, amb $\mathrm{rang}\,D\rho(\mathbf{u})=m$ per a tot $\mathbf{u}\in\Omega$ tal que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiva; en particular, existeix un únic $\mathbf{b}\in\Omega$ tal que $\rho(\mathbf{b})=\mathbf{a}$.

Aleshores,

(i) $T_M(\mathbf{a})=\ker\left(D\Phi(\mathbf{a})\right)=\langle\text{columnes de }D\rho(\mathbf{b})\rangle$;

(ii) $N_M(\mathbf{a})=\langle\text{files de }D\Phi(\mathbf{a})\rangle=\langle\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})\rangle$.

En particular, $T_M(\mathbf{a})$ i $N_M(\mathbf{a})$ són subespais vectorials de $\mathbb{R}^n$ de dimensions $\dim\left(T_M(\mathbf{a})\right)=m$ i $\dim\left(N_M(\mathbf{a})\right)=n-m$, respectivament.
Demostració: (i) Suposem que $\rho(\mathbf{b})=\mathbf{a}$. Veurem que
$$\mathrm{Im}D\rho(\mathbf{b})\subseteq T_M(\mathbf{a})\subseteq\ker D\Phi(\mathbf{a}).\tag{1}$$
Prenem $\mathbf{v}\in\mathrm{Im}D\rho(\mathbf{b})$; això equival a dir que existeix $\mathbf{w}\in\mathbb{R}^m$ tal que $\mathbf{v}=D\rho(\mathbf{b})\,\mathbf{w}$. Volem veure que $\mathbf{v}\in T_M(\mathbf{a})$.

Considerem la funció
$$\alpha\colon\ (-\delta,\delta)\xrightarrow{\ \tilde\alpha\ }\Omega\subset\mathbb{R}^m\xrightarrow{\ \rho\ }M\cap G\subseteq\mathbb{R}^n,\qquad t\longmapsto\mathbf{b}+t\,\mathbf{w}\longmapsto\rho(\mathbf{b}+t\,\mathbf{w}).$$
Aplicant la regla de la cadena,
$$D\alpha(0)=D(\rho\circ\tilde\alpha)(0)=D\rho(\tilde\alpha(0))\,D\tilde\alpha(0)=D\rho(\mathbf{b})\,\mathbf{w}=\mathbf{v},$$
i, per tant, $\mathbf{v}\in T_M(\mathbf{a})$.

D'altra banda, com que la imatge de $\alpha$ pertany a $M$, sabem que $\Phi\circ\alpha\equiv0$. Tornant a aplicar la regla de la cadena, obtenim que
$$D\Phi(\alpha(0))\,D\alpha(0)=D\Phi(\mathbf{a})\,\mathbf{v}=0,$$
que equival a dir que $\mathbf{v}\in\ker(D\Phi(\mathbf{a}))$.

Finalment, sabem que $\dim(\mathrm{Im}(D\rho(\mathbf{b})))=m$ i que $\dim(\ker(D\Phi(\mathbf{a})))=n-\dim(\mathrm{Im}(D\Phi(\mathbf{a})))=n-(n-m)=m$. Per tant, tenim un subespai vectorial, $\mathrm{Im}(D\rho(\mathbf{b}))$, contingut en un altre, $\ker D\Phi(\mathbf{a})$, i ambdós tenen la mateixa dimensió; aleshores, són el mateix subespai i la cadena d'inclusions (1) es converteix en una cadena d'igualtats.

(ii) Considerem ara la composició de funcions $\Phi\circ\rho$:
$$\begin{array}{ccccc}\Omega\subset\mathbb{R}^m&\xrightarrow{\ \rho\ }&M\cap G&\xrightarrow{\ \Phi\ }&\mathbb{R}^{n-m}\\\mathbf{x}&\longmapsto&\rho(\mathbf{x})&\longmapsto&\Phi(\rho(\mathbf{x}))=0,\\\mathbf{b}&\longmapsto&\mathbf{a}=\rho(\mathbf{b})&\longmapsto&0.\end{array}$$
Aleshores,
$$D(\Phi\circ\rho)(\mathbf{b})=D\Phi(\rho(\mathbf{b}))\,D\rho(\mathbf{b})=D\Phi(\mathbf{a})\,D\rho(\mathbf{b})=0,$$
és a dir, cada fila de $D\Phi(\mathbf{a})$ és ortogonal a totes les columnes de $D\rho(\mathbf{b})$. Ara bé, les columnes de $D\rho(\mathbf{b})$ són justament les que generen el subespai tangent. Per tant, les $n-m$ files de $D\Phi(\mathbf{a})$ pertanyen a $N_M(\mathbf{a})$. Com que $\mathrm{rang}D\Phi(\mathbf{a})=n-m$, se'n desprèn que, de fet, generen $N_M(\mathbf{a})$.

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Siguin $M\subseteq\mathbb{R}^n$ una $m$-varietat de classe $r\geqslant1$ i $\mathbf{a}\in M$. Suposem que existeixen oberts $G\subseteq\mathbb{R}^n$ i $\Omega\subseteq\mathbb{R}^m$, amb $\mathbf{a}\in G$, i una funció $\Phi\colon G\longrightarrow\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$, amb $\mathrm{rang}\,D\Phi(\mathbf{x})=n-m$ per a tot $\mathbf{x}\in G$, tal que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.
[2] (enunciat) Suposem també que existeix una funció $\rho\colon\Omega\longrightarrow\mathbb{R}^n$, $\rho\in\mathcal{C}^r(\Omega)$, amb $\mathrm{rang}\,D\rho(\mathbf{u})=m$ per a tot $\mathbf{u}\in\Omega$, tal que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiva; en particular, existeix un únic $\mathbf{b}\in\Omega$ tal que $\rho(\mathbf{b})=\mathbf{a}$.
[3] (enunciat) Aleshores, (i) $T_M(\mathbf{a})=\ker\left(D\Phi(\mathbf{a})\right)=\langle\text{columnes de }D\rho(\mathbf{u})\rangle$ per a tot $\mathbf{u}\in\Omega$; (ii) $N_M(\mathbf{a})=\langle\text{files de }D\Phi(\mathbf{a})\rangle=\langle\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})\rangle$. En particular, $T_M(\mathbf{a})$ i $N_M(\mathbf{a})$ són subespais vectorials de $\mathbb{R}^n$ de dimensions $\dim T_M(\mathbf{a})=m$ i $\dim N_M(\mathbf{a})=n-m$, respectivament.
[4] (demostració) (i) Veurem que $\mathrm{Im}\,D\rho(\mathbf{b})\subseteq T_M(\mathbf{a})\subseteq\ker D\Phi(\mathbf{a})$ (1). Prenem $\mathbf{v}\in\mathrm{Im}\,D\rho(\mathbf{b})$; és a dir, existeix $\mathbf{w}\in\mathbb{R}^m$ tal que $\mathbf{v}=D\rho(\mathbf{b})\,\mathbf{w}$.
[5] (demostració) Com que $\Omega$ és obert, per a qualsevol $\delta>0$ es té $\tilde\alpha(t)=\mathbf{b}+t\,\mathbf{w}\in\Omega$ si $|t|<\delta$. Considerem $\alpha=\rho\circ\tilde\alpha\colon(-\delta,\delta)\to M\cap G$, $\alpha(t)=\rho(\mathbf{b}+t\,\mathbf{w})$. Per la regla de la cadena, $\alpha'(0)=D\rho(\mathbf{b})\,\mathbf{w}=\mathbf{v}$ i, com que $\alpha(0)=\mathbf{a}$, $\mathbf{v}\in T_M(\mathbf{a})$.
[6] (demostració) D'altra banda, si $\mathbf{v}\in T_M(\mathbf{a})$, és $\mathbf{v}=\alpha'(0)$ per a una corba $\alpha$ de $M$ amb $\alpha(0)=\mathbf{a}$, definida en un interval prou petit perquè prengui valors a $M\cap G$. Aleshores $\Phi\circ\alpha\equiv\mathbf{0}$ i, per la regla de la cadena, $D\Phi(\alpha(0))\,\alpha'(0)=D\Phi(\mathbf{a})\,\mathbf{v}=\mathbf{0}$, és a dir, $\mathbf{v}\in\ker D\Phi(\mathbf{a})$.
[7] (demostració) Finalment, $\dim\mathrm{Im}\,D\rho(\mathbf{b})=\mathrm{rang}\,D\rho(\mathbf{b})=m$ i, pel teorema de la dimensió, $\dim\ker D\Phi(\mathbf{a})=n-\mathrm{rang}\,D\Phi(\mathbf{a})=n-(n-m)=m$. Un subespai contingut en un altre de la mateixa dimensió hi coincideix; per tant, les inclusions de (1) són igualtats.
[8] (demostració) (ii) Com que $\Phi(\rho(\mathbf{b}))=\Phi(\mathbf{a})=\mathbf{0}$, la regla de la cadena dona $D(\Phi\circ\rho)(\mathbf{b})=D\Phi(\mathbf{a})\,D\rho(\mathbf{b})=0$: cada fila de $D\Phi(\mathbf{a})$ és ortogonal a totes les columnes de $D\rho(\mathbf{b})$, que generen $T_M(\mathbf{a})$ per (i). Per tant, les $n-m$ files de $D\Phi(\mathbf{a})$, és a dir, $\nabla\Phi_1(\mathbf{a}),\ldots,\nabla\Phi_{n-m}(\mathbf{a})$, pertanyen a $N_M(\mathbf{a})$.
[9] (demostració) Com que $\mathrm{rang}\,D\Phi(\mathbf{a})=n-m$, aquestes $n-m$ files són linealment independents; com que, a més, $\dim N_M(\mathbf{a})=n-\dim T_M(\mathbf{a})=n-m$, aquestes files generen $N_M(\mathbf{a})$.


## T6.4:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T6.4] Teorema 4 (Tema 6) — Equivalència de les definicions de varietat
Les definicions 2 i 3 són equivalents.

[Figura: quadre "Varietat $M$ de dimensió $m$ en $\mathbb{R}^n$ i de classe $\mathcal{C}^r$" amb dues caixes. DEF. 2: FORMA IMPLÍCITA: $\forall\mathbf{a}\in M$, $\exists G$ obert, $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$, tals que $\mathrm{rg}(D\Phi(\mathbf{x}))=n-m$ $\forall\mathbf{x}\in G$, $M\cap G=\{x\in G\mid\Phi(x)=0\}$. DEF. 3: FORMA PARAMÈTRICA: $\forall\mathbf{a}\in M$, $\exists G$ obert, $a\in G\subseteq\mathbb{R}^n$, $\Omega\subseteq\mathbb{R}^m$ obert, $\boldsymbol{\rho}\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^n$, $\boldsymbol{\rho}\in\mathcal{C}^r(\Omega)$, tals que $\mathrm{rg}(D\boldsymbol{\rho}(u))=m$ $\forall u\in\Omega$, $\boldsymbol{\rho}\colon\Omega\to M\cap G$ és bijectiva. (A les caixes, $n$ es marca en verd i $m$, $n-m$ en vermell.)]

[Figura: quadre "RELACIÓ AMB LA NOTACIÓ DEL TEOREMA DE LA FUNCIÓ IMPLÍCITA". Prenem $N=m$, $M=n-m$. $G$ obert, $G\subseteq\mathbb{R}^{N+M}(=\mathbb{R}^n)$, $\Phi\colon G\to\mathbb{R}^M(=\mathbb{R}^{n-m})$, $\Phi\in\mathcal{C}^r(G)$, $\mathbf{a}=(a,b)\in G$, $\Phi(a)=0$, $0\neq\det\left(\frac{\partial\Phi_i}{\partial y_j}\right)_{i,j=1\ldots M(=n-m)}$. Existeixen oberts $U\subseteq G\subseteq\mathbb{R}^{N+M}(=\mathbb{R}^n)$, $\Omega\subseteq\mathbb{R}^N(=\mathbb{R}^m)$, i una funció $\varphi\colon\Omega\to\mathbb{R}^M(=\mathbb{R}^{n-m})$ t.q. ... (iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$, on $x,u\in\mathbb{R}^N(=\mathbb{R}^m)$ i $y,\varphi(u)\in\mathbb{R}^M(=\mathbb{R}^{n-m})$; (ii) $\varphi\in\mathcal{C}^r(\Omega)$, $\varphi(a)=b$ (OBS) $\mathbf{x}=(x,y)$, $\boldsymbol{\rho}(u)=(u,\varphi(u))$.]

Esbós de la relació entre les dues definicions de varietat diferenciable via l'enunciat del teorema de la funció implícita. Fixeu-vos en la coincidència de les notacions un cop assumit que la $N$ i la $M$ del teorema de la funció implícita es corresponen a $m$ i $n-m$, respectivament, en la definició de varietat. Aquesta relació és el nucli de la demostració del teorema 4.
Demostració: $\Longrightarrow$ Fixem $\mathbf{a}\in M$. Per hipòtesi, existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i una funció $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$ amb $\mathrm{rang}\left(D\Phi(\mathbf{x})\right)=n-m$ per a tot $\mathbf{x}\in G$, tals que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.

Com que $\mathbf{a}\in M\cap G$, $\Phi(\mathbf{a})=\mathbf{0}$, i, a més, el rang és màxim, és a dir, $\mathrm{rang}\left(D\Phi(\mathbf{a})\right)=n-m$. Per tant, hi ha un *requadre* de mida $(n-m)\times(n-m)$ dins de $D\Phi(\mathbf{a})$ amb determinant no nul. Fent permutacions de variables si cal, podem aconseguir que el requadre ocupi les darreres $(n-m)$ columnes de $D\Phi(\mathbf{a})\in\mathcal{M}_{(n-m)\times n}(\mathbb{R})$, és a dir,
$$D\Phi(\mathbf{a})=\begin{pmatrix}*&\big|&\neq0\end{pmatrix},$$
amb $*$ de mida $(n-m)\times m$ (columnes: $m$) i el bloc $\neq0$ de mida $(n-m)\times(n-m)$ (columnes: $n-m$).

Aplicant el teorema de la funció implícita, existeix $U\subseteq G\subseteq\mathbb{R}^n$ i $\Omega\subseteq\mathbb{R}^m$ oberts, amb $\mathbf{a}=(a_1,\ldots,a_m,a_{m+1},\ldots,a_n)\in U$ i $(a_1,\ldots,a_m)\in\Omega$, i una funció $\varphi\colon\Omega\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^{n-m}$, $\varphi\in\mathcal{C}^r$, tal que

- $\varphi(a_1,\ldots,a_m)=(a_{m+1},\ldots,a_n)$.
- $\{\mathbf{x}\in U\mid\Phi(\mathbf{x})=0\}=\{(\mathbf{u},\varphi(\mathbf{u}))\mid\mathbf{u}\in\Omega\}$.

Definim
$$\rho\colon\ \Omega\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^n,\qquad\mathbf{u}\longmapsto(\mathbf{u},\varphi(\mathbf{u})),$$
que compleix que

- $\rho$ és injectiva i de classe $\mathcal{C}^r$;
- $\mathrm{rang}\left(D\rho(\mathbf{u})\right)=m$ ja que
$$D\rho(\mathbf{u})=\begin{pmatrix}\mathrm{Id}_{m\times m}\\\hline D\varphi(\mathbf{u})\end{pmatrix},$$
i, en conseqüència, el rang és $m$ per a tot $u\in\Omega$.
- $\rho(\Omega)=\{(\mathbf{u},\varphi(\mathbf{u})),\ \mathbf{u}\in\Omega\}=\{\mathbf{x}\in U:\ \Phi(\mathbf{x})=0\}=U\cap\{\mathbf{x}\in G:\ \Phi(\mathbf{x})=0\}$ perquè $U\subseteq G$. Ara bé, $U\cap\{\mathbf{x}\in G:\ \Phi(\mathbf{x})=0\}=U\cap(M\cap G)=M\cap U$.

Llavors, $\rho\colon\Omega\longrightarrow M\cap U$ és bijectiva i
$$\rho^{-1}\colon\ M\cap U\longrightarrow\Omega,\qquad(\mathbf{x},\mathbf{y})\longmapsto\mathbf{x}$$
és contínua.

$\Longleftarrow$ Fixem $\mathbf{a}\in M$. Sabem que existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, un obert $\Omega\subseteq\mathbb{R}^m$ i una funció $\rho\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^n$, $\rho\in\mathcal{C}^r(\Omega)$ amb $\mathrm{rang}\left(D\rho(\mathbf{u})\right)=m$ per a tot $\mathbf{u}\in\Omega$, tals que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiu i $\rho^{-1}$ és contínua.

En particular, sabem que existeix un únic valor $\mathbf{b}\in\Omega$ tal que $\rho(\mathbf{b})=\mathbf{a}$ i $\mathrm{rang}\left(D\rho(\mathbf{b})\right)=m$.

Podem descompondre la imatge de qualsevol element $\mathbf{u}\in\Omega$ com a
$$\rho(\mathbf{u})=:(\rho_m(\mathbf{u}),\rho_{n-m}(\mathbf{u})),$$
de manera que si $\mathbf{v}=\rho(\mathbf{u})$, aleshores $\rho_m(\mathbf{u})=(v_1,\ldots,v_m)$ i $\rho_{n-m}(\mathbf{u})=(v_{m+1},\ldots,v_n)$ són les projeccions en les $m$ primeres i en les $n-m$ darreres variables, respectivament.

Reordenant variables si cal, podem suposar que
$$D\rho(\mathbf{b})=\begin{pmatrix}D\rho_m(\mathbf{b})\\\hline\star\end{pmatrix}\in\mathcal{M}_{n\times m}(\mathbb{R}),$$
on $\rho_m\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^m$ i $\det D\rho_m(\mathbf{b})\neq0$. Per tant, podem aplicar el teorema de la funció inversa i deduïm que existeix un obert $\Omega'\subseteq\Omega\subseteq\mathbb{R}^m$ tal que $U=\rho_m(\Omega')$ és un obert de $\mathbb{R}^m$, $\rho_m\colon\Omega'\longrightarrow U$ és bijectiva i $\rho_m^{-1}\in\mathcal{C}^r(U)$.

Prenem ara $G'=U\times\mathbb{R}^{n-m}$ obert de $\mathbb{R}^n$ i considerem l'aplicació
$$\Phi\colon\ G\cap G'\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^{n-m},\qquad(x_1,\ldots,x_n)\longmapsto(x_{m+1},\ldots,x_n)-\rho_{n-m}(\rho_m^{-1}(x_1,\ldots,x_m)).$$
Observem que

- $\Phi$ està ben definida i $\Phi\in\mathcal{C}^r$. Efectivament, si $(x_1,\ldots,x_n)\in G'$, aleshores $(x_1,\ldots,x_m)\in U$ i, per tant, $\rho_m^{-1}(x_1,\ldots,x_m)\in\Omega'$ i té sentit. En conseqüència, $\rho_{n-m}(\rho_m^{-1}(x_1,\ldots,x_m))$ també té sentit.
- El rang de
$$D\Phi(x)=(\star\mid\mathrm{Id})\in\mathcal{M}_{(n-m)\times n}(\mathbb{R})$$
és $n-m$ per a tot $x\in G\cap G'$.

En aquest punt, no es pot assegurar encara que $M\cap(G\cap G')=\{\mathbf{x}\in G\cap G'\mid\Phi(\mathbf{x})=0\}$; cal restringir-se a un obert més petit que $G\cap G'$.

Observem que $\rho\colon\Omega\subseteq\mathbb{R}^m\longrightarrow M\cap G\subseteq\mathbb{R}^n$ és bijectiva, contínua i $\rho^{-1}\colon M\cap G\longrightarrow\Omega$ i que $\Omega'\subseteq\Omega$. Llavors,
$$\rho(\Omega')=\left(\rho^{-1}\right)^{-1}(\Omega')=G''\cap(M\cap G),$$
per a un determinat obert $G''$ de $\mathbb{R}^n$.

Finalment, restringim $\Phi$ a $\mathcal{G}:=G\cap G'\cap G''$ i demostrarem que
$$\{\mathbf{x}\in\mathcal{G}\mid\Phi(\mathbf{x})=0\}=\mathcal{G}\cap M:$$

$\subseteq$ Només cal veure que $\mathbf{x}\in M$.
$$\mathbf{x}\in G'\Rightarrow(x_1,\ldots,x_m)\in U\Rightarrow\rho_m(\rho_m^{-1}(x_1,\ldots,x_m))=(x_1,\ldots,x_m).$$
Recordem que $\rho_m^{-1}(x_1,\ldots,x_m)\in\Omega'$; llavors $\rho(\rho_m^{-1}(x_1,\ldots,x_m))=(x_1,\ldots,x_m,x_{m+1},\ldots,x_n)=\mathbf{x}$.
D'altra banda, $\Phi(\mathbf{x})=0$ implica que $\rho_{n-m}(\rho_m(x_1,\ldots,x_m))=(x_{m+1},\ldots,x_n)$.
Finalment, deduïm que $\mathbf{x}\in\rho(\Omega')\subseteq\rho(\Omega)=G\cap M$; en particular, $\mathbf{x}\in M$.

$\supseteq$ Si $\mathbf{x}\in G\cap G'\cap G''$, aleshores $\mathbf{x}\in G''\cap G\cap M=\rho(\Omega')$. Per tant, existeix $\mathbf{u}'\in\Omega'$ tal que $\rho(\mathbf{u}')=\mathbf{x}$; en particular, $\rho_m(\mathbf{u}')=(x_1,\ldots,x_m)$ i $\rho_{n-m}(\mathbf{u}')=(x_{m+1},\ldots,x_n)$.
Llavors,
$$\begin{aligned}\Phi(\mathbf{x})&=(x_{m+1},\ldots,x_n)-\rho_{n-m}(\rho_m^{-1}(x_1,\ldots,x_m))=(x_{m+1},\ldots,x_n)-\rho_{n-m}(\mathbf{u}')\\&=(x_{m+1},\ldots,x_n)-(x_{m+1},\ldots,x_n)=(0,\ldots,0).\end{aligned}$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $M\subseteq\mathbb{R}^n$. Definició 2 (forma implícita) de $m$-varietat de classe $\mathcal{C}^r$: per a tot $\mathbf{a}\in M$ existeixen un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i una funció $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$, tals que $\mathrm{rang}\left(D\Phi(\mathbf{x})\right)=n-m$ per a algun $\mathbf{x}\in G$ i $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.
[2] (enunciat) Definició 3 (forma paramètrica): per a tot $\mathbf{a}\in M$ existeixen un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, un obert $\Omega\subseteq\mathbb{R}^m$ i una funció $\rho\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^n$, $\rho\in\mathcal{C}^r(\Omega)$, tals que $\mathrm{rang}\left(D\rho(\mathbf{u})\right)=m$ per a tot $\mathbf{u}\in\Omega$ i $\rho\colon\Omega\to M\cap G$ és bijectiva amb inversa contínua.
[3] (enunciat) Aleshores, les definicions 2 i 3 són equivalents: $M$ és una $m$-varietat de classe $\mathcal{C}^r$ segons la definició 2 si i només si ho és segons la definició 3.
[4] (demostració) $\Longrightarrow$ Fixem $\mathbf{a}\in M$ i prenem $G$ i $\Phi$ com a la definició 2. Com que $\mathbf{a}\in M\cap G$, $\Phi(\mathbf{a})=\mathbf{0}$ i, com que $\mathrm{rang}\left(D\Phi(\mathbf{a})\right)=n-m$, hi ha un requadre $(n-m)\times(n-m)$ de $D\Phi(\mathbf{a})$ amb determinant no nul; fent permutacions de variables si cal, podem suposar que ocupa les darreres $n-m$ columnes.
[5] (demostració) Aplicant el teorema de la funció implícita (amb $N=m$ i $M=n-m$), existeixen oberts $U\subseteq G\subseteq\mathbb{R}^n$ i $\Omega\subseteq\mathbb{R}^m$, amb $\mathbf{a}\in U$ i $(a_1,\ldots,a_m)\in\Omega$, i una funció $\varphi\colon\Omega\to\mathbb{R}^{n-m}$ de classe $\mathcal{C}^r$ tals que $\varphi(a_1,\ldots,a_m)=(a_{m+1},\ldots,a_n)$ i $\{\mathbf{x}\in U\mid\Phi(\mathbf{x})=\mathbf{0}\}=\{(\mathbf{u},\varphi(\mathbf{u}))\mid\mathbf{u}\in\Omega\}$.
[6] (demostració) Definim $\rho\colon\Omega\to\mathbb{R}^n$, $\rho(\mathbf{u})=(\mathbf{u},\varphi(\mathbf{u}))$. És injectiva i de classe $\mathcal{C}^r$, i $D\rho(\mathbf{u})=\begin{pmatrix}\mathrm{Id}_{m\times m}\\ D\varphi(\mathbf{u})\end{pmatrix}$ té rang $m$ per a tot $\mathbf{u}\in\Omega$.
[7] (demostració) A més, $\rho(\Omega)=\{\mathbf{x}\in U\mid\Phi(\mathbf{x})=\mathbf{0}\}=U\cap\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}=U\cap(M\cap G)=M\cap U$, ja que $U\subseteq G$. Per tant, $\rho\colon\Omega\to M\cap U$ és bijectiva i la seva inversa, $(\mathbf{x},\mathbf{y})\mapsto\mathbf{x}$, és contínua: prenent l'obert $U$, es compleix la definició 3.
[8] (demostració) $\Longleftarrow$ Fixem $\mathbf{a}\in M$ i prenem $G$, $\Omega$ i $\rho$ com a la definició 3, i sigui $\mathbf{b}\in\Omega$ l'únic punt amb $\rho(\mathbf{b})=\mathbf{a}$. Escrivim $\rho=(\rho_m,\rho_{n-m})$, on $\rho_m$ són les $m$ primeres components i $\rho_{n-m}$ les $n-m$ darreres. Com que $\mathrm{rang}\left(D\rho(\mathbf{b})\right)=m$, $D\rho(\mathbf{b})$ té algun menor d'ordre $m$ no nul i, reordenant variables si cal, podem suposar que és el de les $m$ primeres files: $\det D\rho_m(\mathbf{b})\neq0$.
[9] (demostració) Pel teorema de la funció inversa, existeix un obert $\Omega'\subseteq\Omega$, amb $\mathbf{b}\in\Omega'$, tal que $U=\rho_m(\Omega')$ és un obert de $\mathbb{R}^m$, $\rho_m\colon\Omega'\to U$ és bijectiva i $\rho_m^{-1}\in\mathcal{C}^r(U)$.
[10] (demostració) Prenem $G'=U\times\mathbb{R}^{n-m}$, obert de $\mathbb{R}^n$, i $\Phi\colon G\cap G'\to\mathbb{R}^{n-m}$, $\Phi(x_1,\ldots,x_n)=(x_{m+1},\ldots,x_n)-\rho_{n-m}(\rho_m^{-1}(x_1,\ldots,x_m))$. Està ben definida (si $\mathbf{x}\in G'$, $(x_1,\ldots,x_m)\in U$), és de classe $\mathcal{C}^r$ i $D\Phi(\mathbf{x})=(\star\mid\mathrm{Id}_{n-m})$ té rang $n-m$ per a tot $\mathbf{x}\in G\cap G'$.
[11] (demostració) Encara no podem assegurar que $M\cap(G\cap G')$ sigui el conjunt de zeros de $\Phi$. Com que $\rho^{-1}\colon M\cap G\to\Omega$ és contínua i $\Omega'$ és obert, $\rho(\Omega')=(\rho^{-1})^{-1}(\Omega')$ és un obert relatiu de $M\cap G$, és a dir, $\rho(\Omega')=G''\cap(M\cap G)$ per a cert obert $G''$ de $\mathbb{R}^n$. Restringim $\Phi$ a $\mathcal{G}:=G\cap G'\cap G''$, que conté $\mathbf{a}$.
[12] (demostració) $\subseteq$ Si $\mathbf{x}\in\mathcal{G}$ i $\Phi(\mathbf{x})=\mathbf{0}$, sigui $\mathbf{u}=\rho_m^{-1}(x_1,\ldots,x_m)\in\Omega'$. Aleshores $\rho_m(\mathbf{u})=(x_1,\ldots,x_m)$ i, per $\Phi(\mathbf{x})=\mathbf{0}$, $\rho_{n-m}(\mathbf{u})=(x_{m+1},\ldots,x_n)$; és a dir, $\mathbf{x}=\rho(\mathbf{u})\in\rho(\Omega')\subseteq M$.
[13] (demostració) $\supseteq$ Si $\mathbf{x}\in\mathcal{G}\cap M$, aleshores $\mathbf{x}\in G''\cap(M\cap G)=\rho(\Omega')$, i $\mathbf{x}=\rho(\mathbf{u})$ amb $\mathbf{u}\in\Omega'$; com que $\rho_m(\mathbf{u})=(x_1,\ldots,x_m)$, és $\mathbf{u}=\rho_m^{-1}(x_1,\ldots,x_m)$ i $\Phi(\mathbf{x})=(x_{m+1},\ldots,x_n)-\rho_{n-m}(\mathbf{u})=\mathbf{0}$. Per tant, $M\cap\mathcal{G}=\{\mathbf{x}\in\mathcal{G}\mid\Phi(\mathbf{x})=\mathbf{0}\}$ i es compleix la definició 2.


## T6.4:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T6.4] Teorema 4 (Tema 6) — Equivalència de les definicions de varietat
Les definicions 2 i 3 són equivalents.

[Figura: quadre "Varietat $M$ de dimensió $m$ en $\mathbb{R}^n$ i de classe $\mathcal{C}^r$" amb dues caixes. DEF. 2: FORMA IMPLÍCITA: $\forall\mathbf{a}\in M$, $\exists G$ obert, $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$, tals que $\mathrm{rg}(D\Phi(\mathbf{x}))=n-m$ $\forall\mathbf{x}\in G$, $M\cap G=\{x\in G\mid\Phi(x)=0\}$. DEF. 3: FORMA PARAMÈTRICA: $\forall\mathbf{a}\in M$, $\exists G$ obert, $a\in G\subseteq\mathbb{R}^n$, $\Omega\subseteq\mathbb{R}^m$ obert, $\boldsymbol{\rho}\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^n$, $\boldsymbol{\rho}\in\mathcal{C}^r(\Omega)$, tals que $\mathrm{rg}(D\boldsymbol{\rho}(u))=m$ $\forall u\in\Omega$, $\boldsymbol{\rho}\colon\Omega\to M\cap G$ és bijectiva. (A les caixes, $n$ es marca en verd i $m$, $n-m$ en vermell.)]

[Figura: quadre "RELACIÓ AMB LA NOTACIÓ DEL TEOREMA DE LA FUNCIÓ IMPLÍCITA". Prenem $N=m$, $M=n-m$. $G$ obert, $G\subseteq\mathbb{R}^{N+M}(=\mathbb{R}^n)$, $\Phi\colon G\to\mathbb{R}^M(=\mathbb{R}^{n-m})$, $\Phi\in\mathcal{C}^r(G)$, $\mathbf{a}=(a,b)\in G$, $\Phi(a)=0$, $0\neq\det\left(\frac{\partial\Phi_i}{\partial y_j}\right)_{i,j=1\ldots M(=n-m)}$. Existeixen oberts $U\subseteq G\subseteq\mathbb{R}^{N+M}(=\mathbb{R}^n)$, $\Omega\subseteq\mathbb{R}^N(=\mathbb{R}^m)$, i una funció $\varphi\colon\Omega\to\mathbb{R}^M(=\mathbb{R}^{n-m})$ t.q. ... (iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$, on $x,u\in\mathbb{R}^N(=\mathbb{R}^m)$ i $y,\varphi(u)\in\mathbb{R}^M(=\mathbb{R}^{n-m})$; (ii) $\varphi\in\mathcal{C}^r(\Omega)$, $\varphi(a)=b$ (OBS) $\mathbf{x}=(x,y)$, $\boldsymbol{\rho}(u)=(u,\varphi(u))$.]

Esbós de la relació entre les dues definicions de varietat diferenciable via l'enunciat del teorema de la funció implícita. Fixeu-vos en la coincidència de les notacions un cop assumit que la $N$ i la $M$ del teorema de la funció implícita es corresponen a $m$ i $n-m$, respectivament, en la definició de varietat. Aquesta relació és el nucli de la demostració del teorema 4.
Demostració: $\Longrightarrow$ Fixem $\mathbf{a}\in M$. Per hipòtesi, existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i una funció $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$ amb $\mathrm{rang}\left(D\Phi(\mathbf{x})\right)=n-m$ per a tot $\mathbf{x}\in G$, tals que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.

Com que $\mathbf{a}\in M\cap G$, $\Phi(\mathbf{a})=\mathbf{0}$, i, a més, el rang és màxim, és a dir, $\mathrm{rang}\left(D\Phi(\mathbf{a})\right)=n-m$. Per tant, hi ha un *requadre* de mida $(n-m)\times(n-m)$ dins de $D\Phi(\mathbf{a})$ amb determinant no nul. Fent permutacions de variables si cal, podem aconseguir que el requadre ocupi les darreres $(n-m)$ columnes de $D\Phi(\mathbf{a})\in\mathcal{M}_{(n-m)\times n}(\mathbb{R})$, és a dir,
$$D\Phi(\mathbf{a})=\begin{pmatrix}*&\big|&\neq0\end{pmatrix},$$
amb $*$ de mida $(n-m)\times m$ (columnes: $m$) i el bloc $\neq0$ de mida $(n-m)\times(n-m)$ (columnes: $n-m$).

Aplicant el teorema de la funció implícita, existeix $U\subseteq G\subseteq\mathbb{R}^n$ i $\Omega\subseteq\mathbb{R}^m$ oberts, amb $\mathbf{a}=(a_1,\ldots,a_m,a_{m+1},\ldots,a_n)\in U$ i $(a_1,\ldots,a_m)\in\Omega$, i una funció $\varphi\colon\Omega\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^{n-m}$, $\varphi\in\mathcal{C}^r$, tal que

- $\varphi(a_1,\ldots,a_m)=(a_{m+1},\ldots,a_n)$.
- $\{\mathbf{x}\in U\mid\Phi(\mathbf{x})=0\}=\{(\mathbf{u},\varphi(\mathbf{u}))\mid\mathbf{u}\in\Omega\}$.

Definim
$$\rho\colon\ \Omega\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^n,\qquad\mathbf{u}\longmapsto(\mathbf{u},\varphi(\mathbf{u})),$$
que compleix que

- $\rho$ és injectiva i de classe $\mathcal{C}^r$;
- $\mathrm{rang}\left(D\rho(\mathbf{u})\right)=m$ ja que
$$D\rho(\mathbf{u})=\begin{pmatrix}\mathrm{Id}_{m\times m}\\\hline D\varphi(\mathbf{u})\end{pmatrix},$$
i, en conseqüència, el rang és $m$ per a tot $u\in\Omega$.
- $\rho(\Omega)=\{(\mathbf{u},\varphi(\mathbf{u})),\ \mathbf{u}\in\Omega\}=\{\mathbf{x}\in U:\ \Phi(\mathbf{x})=0\}=U\cap\{\mathbf{x}\in G:\ \Phi(\mathbf{x})=0\}$ perquè $U\subseteq G$. Ara bé, $U\cap\{\mathbf{x}\in G:\ \Phi(\mathbf{x})=0\}=U\cap(M\cap G)=M\cap U$.

Llavors, $\rho\colon\Omega\longrightarrow M\cap U$ és bijectiva i
$$\rho^{-1}\colon\ M\cap U\longrightarrow\Omega,\qquad(\mathbf{x},\mathbf{y})\longmapsto\mathbf{x}$$
és contínua.

$\Longleftarrow$ Fixem $\mathbf{a}\in M$. Sabem que existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, un obert $\Omega\subseteq\mathbb{R}^m$ i una funció $\rho\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^n$, $\rho\in\mathcal{C}^r(\Omega)$ amb $\mathrm{rang}\left(D\rho(\mathbf{u})\right)=m$ per a tot $\mathbf{u}\in\Omega$, tals que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiu i $\rho^{-1}$ és contínua.

En particular, sabem que existeix un únic valor $\mathbf{b}\in\Omega$ tal que $\rho(\mathbf{b})=\mathbf{a}$ i $\mathrm{rang}\left(D\rho(\mathbf{b})\right)=m$.

Podem descompondre la imatge de qualsevol element $\mathbf{u}\in\Omega$ com a
$$\rho(\mathbf{u})=:(\rho_m(\mathbf{u}),\rho_{n-m}(\mathbf{u})),$$
de manera que si $\mathbf{v}=\rho(\mathbf{u})$, aleshores $\rho_m(\mathbf{u})=(v_1,\ldots,v_m)$ i $\rho_{n-m}(\mathbf{u})=(v_{m+1},\ldots,v_n)$ són les projeccions en les $m$ primeres i en les $n-m$ darreres variables, respectivament.

Reordenant variables si cal, podem suposar que
$$D\rho(\mathbf{b})=\begin{pmatrix}D\rho_m(\mathbf{b})\\\hline\star\end{pmatrix}\in\mathcal{M}_{n\times m}(\mathbb{R}),$$
on $\rho_m\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^m$ i $\det D\rho_m(\mathbf{b})\neq0$. Per tant, podem aplicar el teorema de la funció inversa i deduïm que existeix un obert $\Omega'\subseteq\Omega\subseteq\mathbb{R}^m$ tal que $U=\rho_m(\Omega')$ és un obert de $\mathbb{R}^m$, $\rho_m\colon\Omega'\longrightarrow U$ és bijectiva i $\rho_m^{-1}\in\mathcal{C}^r(U)$.

Prenem ara $G'=U\times\mathbb{R}^{n-m}$ obert de $\mathbb{R}^n$ i considerem l'aplicació
$$\Phi\colon\ G\cap G'\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^{n-m},\qquad(x_1,\ldots,x_n)\longmapsto(x_{m+1},\ldots,x_n)-\rho_{n-m}(\rho_m^{-1}(x_1,\ldots,x_m)).$$
Observem que

- $\Phi$ està ben definida i $\Phi\in\mathcal{C}^r$. Efectivament, si $(x_1,\ldots,x_n)\in G'$, aleshores $(x_1,\ldots,x_m)\in U$ i, per tant, $\rho_m^{-1}(x_1,\ldots,x_m)\in\Omega'$ i té sentit. En conseqüència, $\rho_{n-m}(\rho_m^{-1}(x_1,\ldots,x_m))$ també té sentit.
- El rang de
$$D\Phi(x)=(\star\mid\mathrm{Id})\in\mathcal{M}_{(n-m)\times n}(\mathbb{R})$$
és $n-m$ per a tot $x\in G\cap G'$.

En aquest punt, no es pot assegurar encara que $M\cap(G\cap G')=\{\mathbf{x}\in G\cap G'\mid\Phi(\mathbf{x})=0\}$; cal restringir-se a un obert més petit que $G\cap G'$.

Observem que $\rho\colon\Omega\subseteq\mathbb{R}^m\longrightarrow M\cap G\subseteq\mathbb{R}^n$ és bijectiva, contínua i $\rho^{-1}\colon M\cap G\longrightarrow\Omega$ i que $\Omega'\subseteq\Omega$. Llavors,
$$\rho(\Omega')=\left(\rho^{-1}\right)^{-1}(\Omega')=G''\cap(M\cap G),$$
per a un determinat obert $G''$ de $\mathbb{R}^n$.

Finalment, restringim $\Phi$ a $\mathcal{G}:=G\cap G'\cap G''$ i demostrarem que
$$\{\mathbf{x}\in\mathcal{G}\mid\Phi(\mathbf{x})=0\}=\mathcal{G}\cap M:$$

$\subseteq$ Només cal veure que $\mathbf{x}\in M$.
$$\mathbf{x}\in G'\Rightarrow(x_1,\ldots,x_m)\in U\Rightarrow\rho_m(\rho_m^{-1}(x_1,\ldots,x_m))=(x_1,\ldots,x_m).$$
Recordem que $\rho_m^{-1}(x_1,\ldots,x_m)\in\Omega'$; llavors $\rho(\rho_m^{-1}(x_1,\ldots,x_m))=(x_1,\ldots,x_m,x_{m+1},\ldots,x_n)=\mathbf{x}$.
D'altra banda, $\Phi(\mathbf{x})=0$ implica que $\rho_{n-m}(\rho_m(x_1,\ldots,x_m))=(x_{m+1},\ldots,x_n)$.
Finalment, deduïm que $\mathbf{x}\in\rho(\Omega')\subseteq\rho(\Omega)=G\cap M$; en particular, $\mathbf{x}\in M$.

$\supseteq$ Si $\mathbf{x}\in G\cap G'\cap G''$, aleshores $\mathbf{x}\in G''\cap G\cap M=\rho(\Omega')$. Per tant, existeix $\mathbf{u}'\in\Omega'$ tal que $\rho(\mathbf{u}')=\mathbf{x}$; en particular, $\rho_m(\mathbf{u}')=(x_1,\ldots,x_m)$ i $\rho_{n-m}(\mathbf{u}')=(x_{m+1},\ldots,x_n)$.
Llavors,
$$\begin{aligned}\Phi(\mathbf{x})&=(x_{m+1},\ldots,x_n)-\rho_{n-m}(\rho_m^{-1}(x_1,\ldots,x_m))=(x_{m+1},\ldots,x_n)-\rho_{n-m}(\mathbf{u}')\\&=(x_{m+1},\ldots,x_n)-(x_{m+1},\ldots,x_n)=(0,\ldots,0).\end{aligned}$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $M\subseteq\mathbb{R}^n$. Definició 2 (forma implícita) de $m$-varietat de classe $\mathcal{C}^r$: per a tot $\mathbf{a}\in M$ existeixen un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i una funció $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$, tals que $\mathrm{rang}\left(D\Phi(\mathbf{x})\right)=n-m$ per a tot $\mathbf{x}\in G$ i $M\cap G\subseteq\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.
[2] (enunciat) Definició 3 (forma paramètrica): per a tot $\mathbf{a}\in M$ existeixen un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, un obert $\Omega\subseteq\mathbb{R}^m$ i una funció $\rho\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^n$, $\rho\in\mathcal{C}^r(\Omega)$, tals que $\mathrm{rang}\left(D\rho(\mathbf{u})\right)=m$ per a tot $\mathbf{u}\in\Omega$ i $\rho\colon\Omega\to M\cap G$ és bijectiva amb inversa contínua.
[3] (enunciat) Aleshores, les definicions 2 i 3 són equivalents: $M$ és una $m$-varietat de classe $\mathcal{C}^r$ segons la definició 2 si i només si ho és segons la definició 3.
[4] (demostració) $\Longrightarrow$ Fixem $\mathbf{a}\in M$ i prenem $G$ i $\Phi$ com a la definició 2. Com que $\mathbf{a}\in M\cap G$, $\Phi(\mathbf{a})=\mathbf{0}$ i, com que $\mathrm{rang}\left(D\Phi(\mathbf{a})\right)=n-m$, hi ha un requadre $(n-m)\times(n-m)$ de $D\Phi(\mathbf{a})$ amb determinant no nul; fent permutacions de variables si cal, podem suposar que ocupa les darreres $n-m$ columnes.
[5] (demostració) Aplicant el teorema de la funció implícita (amb $N=m$ i $M=n-m$), existeixen oberts $U\subseteq G\subseteq\mathbb{R}^n$ i $\Omega\subseteq\mathbb{R}^m$, amb $\mathbf{a}\in U$ i $(a_1,\ldots,a_m)\in\Omega$, i una funció $\varphi\colon\Omega\to\mathbb{R}^{n-m}$ de classe $\mathcal{C}^r$ tals que $\varphi(a_1,\ldots,a_m)=(a_{m+1},\ldots,a_n)$ i $\{\mathbf{x}\in U\mid\Phi(\mathbf{x})=\mathbf{0}\}=\{(\mathbf{u},\varphi(\mathbf{u}))\mid\mathbf{u}\in\Omega\}$.
[6] (demostració) Definim $\rho\colon\Omega\to\mathbb{R}^n$, $\rho(\mathbf{u})=(\mathbf{u},\varphi(\mathbf{u}))$. És injectiva i de classe $\mathcal{C}^r$, i $D\rho(\mathbf{u})=\begin{pmatrix}\mathrm{Id}_{m\times m}\\ D\varphi(\mathbf{u})\end{pmatrix}$ té rang $m$ per a tot $\mathbf{u}\in\Omega$.
[7] (demostració) A més, $\rho(\Omega)=\{\mathbf{x}\in U\mid\Phi(\mathbf{x})=\mathbf{0}\}=U\cap\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}=U\cap(M\cap G)=M\cap U$, ja que $U\subseteq G$. Per tant, $\rho\colon\Omega\to M\cap U$ és bijectiva i la seva inversa, $(\mathbf{x},\mathbf{y})\mapsto\mathbf{x}$, és contínua: prenent l'obert $U$, es compleix la definició 3.
[8] (demostració) $\Longleftarrow$ Fixem $\mathbf{a}\in M$ i prenem $G$, $\Omega$ i $\rho$ com a la definició 3, i sigui $\mathbf{b}\in\Omega$ l'únic punt amb $\rho(\mathbf{b})=\mathbf{a}$. Escrivim $\rho=(\rho_m,\rho_{n-m})$, on $\rho_m$ són les $m$ primeres components i $\rho_{n-m}$ les $n-m$ darreres. Com que $\mathrm{rang}\left(D\rho(\mathbf{b})\right)=m$, $D\rho(\mathbf{b})$ té algun menor d'ordre $m$ no nul i, reordenant variables si cal, podem suposar que és el de les $m$ primeres files: $\det D\rho_m(\mathbf{b})\neq0$.
[9] (demostració) Pel teorema de la funció inversa, existeix un obert $\Omega'\subseteq\Omega$, amb $\mathbf{b}\in\Omega'$, tal que $U=\rho_m(\Omega')$ és un obert de $\mathbb{R}^m$, $\rho_m\colon\Omega'\to U$ és bijectiva i $\rho_m^{-1}\in\mathcal{C}^r(U)$.
[10] (demostració) Prenem $G'=U\times\mathbb{R}^{n-m}$, obert de $\mathbb{R}^n$, i $\Phi\colon G\cap G'\to\mathbb{R}^{n-m}$, $\Phi(x_1,\ldots,x_n)=(x_{m+1},\ldots,x_n)-\rho_{n-m}(\rho_m^{-1}(x_1,\ldots,x_m))$. Està ben definida (si $\mathbf{x}\in G'$, $(x_1,\ldots,x_m)\in U$), és de classe $\mathcal{C}^r$ i $D\Phi(\mathbf{x})=(\star\mid\mathrm{Id}_{n-m})$ té rang $n-m$ per a tot $\mathbf{x}\in G\cap G'$.
[11] (demostració) Encara no podem assegurar que $M\cap(G\cap G')$ sigui el conjunt de zeros de $\Phi$. Com que $\rho$ és contínua i $\Omega'$ és obert, $\rho(\Omega')$ és un obert relatiu de $M\cap G$, és a dir, $\rho(\Omega')=G''\cap(M\cap G)$ per a cert obert $G''$ de $\mathbb{R}^n$. Restringim $\Phi$ a $\mathcal{G}:=G\cap G'\cap G''$, que conté $\mathbf{a}$.
[12] (demostració) $\subseteq$ Si $\mathbf{x}\in\mathcal{G}$ i $\Phi(\mathbf{x})=\mathbf{0}$, sigui $\mathbf{u}=\rho_m^{-1}(x_1,\ldots,x_m)\in\Omega'$. Aleshores $\rho_m(\mathbf{u})=(x_1,\ldots,x_m)$ i, per $\Phi(\mathbf{x})=\mathbf{0}$, $\rho_{n-m}(\mathbf{u})=(x_{m+1},\ldots,x_n)$; és a dir, $\mathbf{x}=\rho(\mathbf{u})\in\rho(\Omega')\subseteq M$.
[13] (demostració) $\supseteq$ Si $\mathbf{x}\in\mathcal{G}\cap M$, aleshores $\mathbf{x}\in G''\cap(M\cap G)=\rho(\Omega')$, i $\mathbf{x}=\rho(\mathbf{u})$ amb $\mathbf{u}\in\Omega'$; com que $\rho_m(\mathbf{u})=(x_1,\ldots,x_m)$, és $\mathbf{u}=\rho_m^{-1}(x_1,\ldots,x_m)$ i $\Phi(\mathbf{x})=(x_{m+1},\ldots,x_n)-\rho_{n-m}(\mathbf{u})=\mathbf{0}$. Per tant, $M\cap\mathcal{G}=\{\mathbf{x}\in\mathcal{G}\mid\Phi(\mathbf{x})=\mathbf{0}\}$ i es compleix la definició 2.


## T6.4:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T6.4] Teorema 4 (Tema 6) — Equivalència de les definicions de varietat
Les definicions 2 i 3 són equivalents.

[Figura: quadre "Varietat $M$ de dimensió $m$ en $\mathbb{R}^n$ i de classe $\mathcal{C}^r$" amb dues caixes. DEF. 2: FORMA IMPLÍCITA: $\forall\mathbf{a}\in M$, $\exists G$ obert, $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$, tals que $\mathrm{rg}(D\Phi(\mathbf{x}))=n-m$ $\forall\mathbf{x}\in G$, $M\cap G=\{x\in G\mid\Phi(x)=0\}$. DEF. 3: FORMA PARAMÈTRICA: $\forall\mathbf{a}\in M$, $\exists G$ obert, $a\in G\subseteq\mathbb{R}^n$, $\Omega\subseteq\mathbb{R}^m$ obert, $\boldsymbol{\rho}\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^n$, $\boldsymbol{\rho}\in\mathcal{C}^r(\Omega)$, tals que $\mathrm{rg}(D\boldsymbol{\rho}(u))=m$ $\forall u\in\Omega$, $\boldsymbol{\rho}\colon\Omega\to M\cap G$ és bijectiva. (A les caixes, $n$ es marca en verd i $m$, $n-m$ en vermell.)]

[Figura: quadre "RELACIÓ AMB LA NOTACIÓ DEL TEOREMA DE LA FUNCIÓ IMPLÍCITA". Prenem $N=m$, $M=n-m$. $G$ obert, $G\subseteq\mathbb{R}^{N+M}(=\mathbb{R}^n)$, $\Phi\colon G\to\mathbb{R}^M(=\mathbb{R}^{n-m})$, $\Phi\in\mathcal{C}^r(G)$, $\mathbf{a}=(a,b)\in G$, $\Phi(a)=0$, $0\neq\det\left(\frac{\partial\Phi_i}{\partial y_j}\right)_{i,j=1\ldots M(=n-m)}$. Existeixen oberts $U\subseteq G\subseteq\mathbb{R}^{N+M}(=\mathbb{R}^n)$, $\Omega\subseteq\mathbb{R}^N(=\mathbb{R}^m)$, i una funció $\varphi\colon\Omega\to\mathbb{R}^M(=\mathbb{R}^{n-m})$ t.q. ... (iii) $\{(x,y)\in U\mid\Phi(x,y)=0\}=\{(u,\varphi(u))\mid u\in\Omega\}$, on $x,u\in\mathbb{R}^N(=\mathbb{R}^m)$ i $y,\varphi(u)\in\mathbb{R}^M(=\mathbb{R}^{n-m})$; (ii) $\varphi\in\mathcal{C}^r(\Omega)$, $\varphi(a)=b$ (OBS) $\mathbf{x}=(x,y)$, $\boldsymbol{\rho}(u)=(u,\varphi(u))$.]

Esbós de la relació entre les dues definicions de varietat diferenciable via l'enunciat del teorema de la funció implícita. Fixeu-vos en la coincidència de les notacions un cop assumit que la $N$ i la $M$ del teorema de la funció implícita es corresponen a $m$ i $n-m$, respectivament, en la definició de varietat. Aquesta relació és el nucli de la demostració del teorema 4.
Demostració: $\Longrightarrow$ Fixem $\mathbf{a}\in M$. Per hipòtesi, existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i una funció $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$ amb $\mathrm{rang}\left(D\Phi(\mathbf{x})\right)=n-m$ per a tot $\mathbf{x}\in G$, tals que $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.

Com que $\mathbf{a}\in M\cap G$, $\Phi(\mathbf{a})=\mathbf{0}$, i, a més, el rang és màxim, és a dir, $\mathrm{rang}\left(D\Phi(\mathbf{a})\right)=n-m$. Per tant, hi ha un *requadre* de mida $(n-m)\times(n-m)$ dins de $D\Phi(\mathbf{a})$ amb determinant no nul. Fent permutacions de variables si cal, podem aconseguir que el requadre ocupi les darreres $(n-m)$ columnes de $D\Phi(\mathbf{a})\in\mathcal{M}_{(n-m)\times n}(\mathbb{R})$, és a dir,
$$D\Phi(\mathbf{a})=\begin{pmatrix}*&\big|&\neq0\end{pmatrix},$$
amb $*$ de mida $(n-m)\times m$ (columnes: $m$) i el bloc $\neq0$ de mida $(n-m)\times(n-m)$ (columnes: $n-m$).

Aplicant el teorema de la funció implícita, existeix $U\subseteq G\subseteq\mathbb{R}^n$ i $\Omega\subseteq\mathbb{R}^m$ oberts, amb $\mathbf{a}=(a_1,\ldots,a_m,a_{m+1},\ldots,a_n)\in U$ i $(a_1,\ldots,a_m)\in\Omega$, i una funció $\varphi\colon\Omega\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^{n-m}$, $\varphi\in\mathcal{C}^r$, tal que

- $\varphi(a_1,\ldots,a_m)=(a_{m+1},\ldots,a_n)$.
- $\{\mathbf{x}\in U\mid\Phi(\mathbf{x})=0\}=\{(\mathbf{u},\varphi(\mathbf{u}))\mid\mathbf{u}\in\Omega\}$.

Definim
$$\rho\colon\ \Omega\subseteq\mathbb{R}^m\longrightarrow\mathbb{R}^n,\qquad\mathbf{u}\longmapsto(\mathbf{u},\varphi(\mathbf{u})),$$
que compleix que

- $\rho$ és injectiva i de classe $\mathcal{C}^r$;
- $\mathrm{rang}\left(D\rho(\mathbf{u})\right)=m$ ja que
$$D\rho(\mathbf{u})=\begin{pmatrix}\mathrm{Id}_{m\times m}\\\hline D\varphi(\mathbf{u})\end{pmatrix},$$
i, en conseqüència, el rang és $m$ per a tot $u\in\Omega$.
- $\rho(\Omega)=\{(\mathbf{u},\varphi(\mathbf{u})),\ \mathbf{u}\in\Omega\}=\{\mathbf{x}\in U:\ \Phi(\mathbf{x})=0\}=U\cap\{\mathbf{x}\in G:\ \Phi(\mathbf{x})=0\}$ perquè $U\subseteq G$. Ara bé, $U\cap\{\mathbf{x}\in G:\ \Phi(\mathbf{x})=0\}=U\cap(M\cap G)=M\cap U$.

Llavors, $\rho\colon\Omega\longrightarrow M\cap U$ és bijectiva i
$$\rho^{-1}\colon\ M\cap U\longrightarrow\Omega,\qquad(\mathbf{x},\mathbf{y})\longmapsto\mathbf{x}$$
és contínua.

$\Longleftarrow$ Fixem $\mathbf{a}\in M$. Sabem que existeix un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, un obert $\Omega\subseteq\mathbb{R}^m$ i una funció $\rho\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^n$, $\rho\in\mathcal{C}^r(\Omega)$ amb $\mathrm{rang}\left(D\rho(\mathbf{u})\right)=m$ per a tot $\mathbf{u}\in\Omega$, tals que $\rho\colon\Omega\longrightarrow M\cap G$ és bijectiu i $\rho^{-1}$ és contínua.

En particular, sabem que existeix un únic valor $\mathbf{b}\in\Omega$ tal que $\rho(\mathbf{b})=\mathbf{a}$ i $\mathrm{rang}\left(D\rho(\mathbf{b})\right)=m$.

Podem descompondre la imatge de qualsevol element $\mathbf{u}\in\Omega$ com a
$$\rho(\mathbf{u})=:(\rho_m(\mathbf{u}),\rho_{n-m}(\mathbf{u})),$$
de manera que si $\mathbf{v}=\rho(\mathbf{u})$, aleshores $\rho_m(\mathbf{u})=(v_1,\ldots,v_m)$ i $\rho_{n-m}(\mathbf{u})=(v_{m+1},\ldots,v_n)$ són les projeccions en les $m$ primeres i en les $n-m$ darreres variables, respectivament.

Reordenant variables si cal, podem suposar que
$$D\rho(\mathbf{b})=\begin{pmatrix}D\rho_m(\mathbf{b})\\\hline\star\end{pmatrix}\in\mathcal{M}_{n\times m}(\mathbb{R}),$$
on $\rho_m\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^m$ i $\det D\rho_m(\mathbf{b})\neq0$. Per tant, podem aplicar el teorema de la funció inversa i deduïm que existeix un obert $\Omega'\subseteq\Omega\subseteq\mathbb{R}^m$ tal que $U=\rho_m(\Omega')$ és un obert de $\mathbb{R}^m$, $\rho_m\colon\Omega'\longrightarrow U$ és bijectiva i $\rho_m^{-1}\in\mathcal{C}^r(U)$.

Prenem ara $G'=U\times\mathbb{R}^{n-m}$ obert de $\mathbb{R}^n$ i considerem l'aplicació
$$\Phi\colon\ G\cap G'\subseteq\mathbb{R}^n\longrightarrow\mathbb{R}^{n-m},\qquad(x_1,\ldots,x_n)\longmapsto(x_{m+1},\ldots,x_n)-\rho_{n-m}(\rho_m^{-1}(x_1,\ldots,x_m)).$$
Observem que

- $\Phi$ està ben definida i $\Phi\in\mathcal{C}^r$. Efectivament, si $(x_1,\ldots,x_n)\in G'$, aleshores $(x_1,\ldots,x_m)\in U$ i, per tant, $\rho_m^{-1}(x_1,\ldots,x_m)\in\Omega'$ i té sentit. En conseqüència, $\rho_{n-m}(\rho_m^{-1}(x_1,\ldots,x_m))$ també té sentit.
- El rang de
$$D\Phi(x)=(\star\mid\mathrm{Id})\in\mathcal{M}_{(n-m)\times n}(\mathbb{R})$$
és $n-m$ per a tot $x\in G\cap G'$.

En aquest punt, no es pot assegurar encara que $M\cap(G\cap G')=\{\mathbf{x}\in G\cap G'\mid\Phi(\mathbf{x})=0\}$; cal restringir-se a un obert més petit que $G\cap G'$.

Observem que $\rho\colon\Omega\subseteq\mathbb{R}^m\longrightarrow M\cap G\subseteq\mathbb{R}^n$ és bijectiva, contínua i $\rho^{-1}\colon M\cap G\longrightarrow\Omega$ i que $\Omega'\subseteq\Omega$. Llavors,
$$\rho(\Omega')=\left(\rho^{-1}\right)^{-1}(\Omega')=G''\cap(M\cap G),$$
per a un determinat obert $G''$ de $\mathbb{R}^n$.

Finalment, restringim $\Phi$ a $\mathcal{G}:=G\cap G'\cap G''$ i demostrarem que
$$\{\mathbf{x}\in\mathcal{G}\mid\Phi(\mathbf{x})=0\}=\mathcal{G}\cap M:$$

$\subseteq$ Només cal veure que $\mathbf{x}\in M$.
$$\mathbf{x}\in G'\Rightarrow(x_1,\ldots,x_m)\in U\Rightarrow\rho_m(\rho_m^{-1}(x_1,\ldots,x_m))=(x_1,\ldots,x_m).$$
Recordem que $\rho_m^{-1}(x_1,\ldots,x_m)\in\Omega'$; llavors $\rho(\rho_m^{-1}(x_1,\ldots,x_m))=(x_1,\ldots,x_m,x_{m+1},\ldots,x_n)=\mathbf{x}$.
D'altra banda, $\Phi(\mathbf{x})=0$ implica que $\rho_{n-m}(\rho_m(x_1,\ldots,x_m))=(x_{m+1},\ldots,x_n)$.
Finalment, deduïm que $\mathbf{x}\in\rho(\Omega')\subseteq\rho(\Omega)=G\cap M$; en particular, $\mathbf{x}\in M$.

$\supseteq$ Si $\mathbf{x}\in G\cap G'\cap G''$, aleshores $\mathbf{x}\in G''\cap G\cap M=\rho(\Omega')$. Per tant, existeix $\mathbf{u}'\in\Omega'$ tal que $\rho(\mathbf{u}')=\mathbf{x}$; en particular, $\rho_m(\mathbf{u}')=(x_1,\ldots,x_m)$ i $\rho_{n-m}(\mathbf{u}')=(x_{m+1},\ldots,x_n)$.
Llavors,
$$\begin{aligned}\Phi(\mathbf{x})&=(x_{m+1},\ldots,x_n)-\rho_{n-m}(\rho_m^{-1}(x_1,\ldots,x_m))=(x_{m+1},\ldots,x_n)-\rho_{n-m}(\mathbf{u}')\\&=(x_{m+1},\ldots,x_n)-(x_{m+1},\ldots,x_n)=(0,\ldots,0).\end{aligned}$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) Sigui $M\subseteq\mathbb{R}^n$. Definició 2 (forma implícita) de $m$-varietat de classe $\mathcal{C}^r$: per a tot $\mathbf{a}\in M$ existeixen un obert $G$, amb $\mathbf{a}\in G\subseteq\mathbb{R}^n$, i una funció $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$, $\Phi\in\mathcal{C}^r(G)$, tals que $\mathrm{rang}\left(D\Phi(\mathbf{x})\right)=n-m$ per a tot $\mathbf{x}\in G$ i $M\cap G=\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}$.
[2] (enunciat) Definició 3 (forma paramètrica): existeixen un obert $G$, amb $M\subseteq G\subseteq\mathbb{R}^n$, un obert $\Omega\subseteq\mathbb{R}^m$ i una funció $\rho\colon\Omega\subseteq\mathbb{R}^m\to\mathbb{R}^n$, $\rho\in\mathcal{C}^r(\Omega)$, tals que $\mathrm{rang}\left(D\rho(\mathbf{u})\right)=m$ per a tot $\mathbf{u}\in\Omega$ i $\rho\colon\Omega\to M\cap G$ és bijectiva amb inversa contínua.
[3] (enunciat) Aleshores, les definicions 2 i 3 són equivalents: $M$ és una $m$-varietat de classe $\mathcal{C}^r$ segons la definició 2 si i només si ho és segons la definició 3.
[4] (demostració) $\Longrightarrow$ Fixem $\mathbf{a}\in M$ i prenem $G$ i $\Phi$ com a la definició 2. Com que $\mathbf{a}\in M\cap G$, $\Phi(\mathbf{a})=\mathbf{0}$ i, com que $\mathrm{rang}\left(D\Phi(\mathbf{a})\right)=n-m$, hi ha un requadre $(n-m)\times(n-m)$ de $D\Phi(\mathbf{a})$ amb determinant no nul; fent permutacions de variables si cal, podem suposar que ocupa les darreres $n-m$ columnes.
[5] (demostració) Aplicant el teorema de la funció implícita (amb $N=m$ i $M=n-m$), existeixen oberts $U\subseteq G\subseteq\mathbb{R}^n$ i $\Omega\subseteq\mathbb{R}^m$, amb $\mathbf{a}\in U$ i $(a_1,\ldots,a_m)\in\Omega$, i una funció $\varphi\colon\Omega\to\mathbb{R}^{n-m}$ de classe $\mathcal{C}^r$ tals que $\varphi(a_1,\ldots,a_m)=(a_{m+1},\ldots,a_n)$ i $\{\mathbf{x}\in U\mid\Phi(\mathbf{x})=\mathbf{0}\}=\{(\mathbf{u},\varphi(\mathbf{u}))\mid\mathbf{u}\in\Omega\}$.
[6] (demostració) Definim $\rho\colon\Omega\to\mathbb{R}^n$, $\rho(\mathbf{u})=(\mathbf{u},\varphi(\mathbf{u}))$. És injectiva i de classe $\mathcal{C}^r$, i $D\rho(\mathbf{u})=\begin{pmatrix}\mathrm{Id}_{m\times m}\\ D\varphi(\mathbf{u})\end{pmatrix}$ té rang $m$ per a tot $\mathbf{u}\in\Omega$.
[7] (demostració) A més, $\rho(\Omega)=\{\mathbf{x}\in U\mid\Phi(\mathbf{x})=\mathbf{0}\}=U\cap\{\mathbf{x}\in G\mid\Phi(\mathbf{x})=\mathbf{0}\}=U\cap(M\cap G)=M\cap U$, ja que $G\subseteq U$. Per tant, $\rho\colon\Omega\to M\cap U$ és bijectiva i la seva inversa, $(\mathbf{x},\mathbf{y})\mapsto\mathbf{x}$, és contínua: prenent l'obert $U$, es compleix la definició 3.
[8] (demostració) $\Longleftarrow$ Fixem $\mathbf{a}\in M$ i prenem $G$, $\Omega$ i $\rho$ com a la definició 3, i sigui $\mathbf{b}\in\Omega$ l'únic punt amb $\rho(\mathbf{b})=\mathbf{a}$. Escrivim $\rho=(\rho_m,\rho_{n-m})$, on $\rho_m$ són les $m$ primeres components i $\rho_{n-m}$ les $n-m$ darreres. Com que $\mathrm{rang}\left(D\rho(\mathbf{b})\right)=m$, tots els menors d'ordre $m$ de $D\rho(\mathbf{b})$ són no nuls; en particular, el de les $m$ primeres files: $\det D\rho_m(\mathbf{b})\neq0$.
[9] (demostració) Pel teorema de la funció inversa, existeix un obert $\Omega'\subseteq\Omega$, amb $\mathbf{b}\in\Omega'$, tal que $U=\rho_m(\Omega')$ és un obert de $\mathbb{R}^m$, $\rho_m\colon\Omega'\to U$ és bijectiva i $\rho_m^{-1}\in\mathcal{C}^r(U)$.
[10] (demostració) Prenem $G'=U\times\mathbb{R}^{n-m}$, obert de $\mathbb{R}^n$, i $\Phi\colon G\cap G'\to\mathbb{R}^{n-m}$, $\Phi(x_1,\ldots,x_n)=(x_{m+1},\ldots,x_n)-\rho_{n-m}(\rho_m^{-1}(x_1,\ldots,x_m))$. Està ben definida (si $\mathbf{x}\in G'$, $(x_1,\ldots,x_m)\in U$), és de classe $\mathcal{C}^r$ i $D\Phi(\mathbf{x})=(\star\mid\mathrm{Id}_{n-m})$ té rang $n-m$ per a tot $\mathbf{x}\in G\cap G'$.
[11] (demostració) Encara no podem assegurar que $M\cap(G\cap G')$ sigui el conjunt de zeros de $\Phi$. Com que $\rho^{-1}\colon M\cap G\to\Omega$ és contínua i $\Omega'$ és obert, $\rho(\Omega')=(\rho^{-1})^{-1}(\Omega')$ és un obert relatiu de $M\cap G$, és a dir, $\rho(\Omega')=G''\cap(M\cap G)$ per a cert obert $G''$ de $\mathbb{R}^n$. Restringim $\Phi$ a $\mathcal{G}:=G\cap G'\cap G''$, que conté $\mathbf{a}$.
[12] (demostració) $\subseteq$ Si $\mathbf{x}\in\mathcal{G}$ i $\Phi(\mathbf{x})=\mathbf{0}$, sigui $\mathbf{u}=\rho_m^{-1}(x_1,\ldots,x_m)\in\Omega'$. Aleshores $\rho_m(\mathbf{u})=(x_1,\ldots,x_m)$ i, per $\Phi(\mathbf{x})=\mathbf{0}$, $\rho_{n-m}(\mathbf{u})=(x_{m+1},\ldots,x_n)$; és a dir, $\mathbf{x}=\rho(\mathbf{u})\in\rho(\Omega')\subseteq M$.
[13] (demostració) $\supseteq$ Si $\mathbf{x}\in\mathcal{G}\cap M$, aleshores $\mathbf{x}\in G''\cap(M\cap G)=\rho(\Omega')$, i $\mathbf{x}=\rho(\mathbf{u})$ amb $\mathbf{u}\in\Omega'$; com que $\rho_m(\mathbf{u})=(x_1,\ldots,x_m)$, és $\mathbf{u}=\rho_m^{-1}(x_1,\ldots,x_m)$ i $\Phi(\mathbf{x})=(x_{m+1},\ldots,x_n)-\rho_{n-m}(\mathbf{u})=\mathbf{0}$. Per tant, $M\cap\mathcal{G}=\{\mathbf{x}\in\mathcal{G}\mid\Phi(\mathbf{x})=\mathbf{0}\}$ i es compleix la definició 2.


## T6.19:facil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T6.19] Teorema 19 (Tema 6) — Condicions suficients d'extrem condicionat
(condicions suficients). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ com en el corol·lari 17, amb $r\geq2$, $M=M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^2(G)$. Sigui $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in M\times\mathbb{R}^{n-m}$ un punt crític de la funció de Lagrange $L$; considerem la subfunció $F\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ donada per $F(\mathbf{x})=L(\mathbf{x},\lambda_1,\ldots,\lambda_{n-m})$. Llavors,

(i) $q_{HF(\mathbf{a})}$ és definida negativa ($\ominus$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un màxim local estricte de $f$ condicionat a $M$;

(ii) $q_{HF(\mathbf{a})}$ és definida positiva ($\oplus$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un mínim local estricte de $f$ condicionat a $M$;

(iii) $q_{HF(\mathbf{a})}$ és indefinida ($\odot$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un punt de sella de $f$ condicionat a $M$;

(iv) $\mathbf{a}$ és un màxim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida negativa ($\underline{\ominus}$) sobre $T_M(\mathbf{a})$;

(v) $\mathbf{a}$ és un mínim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida positiva ($\underline{\oplus}$) sobre $T_M(\mathbf{a})$.
Demostració: Sigui $\rho$ una parametrització de $M$:
$$\begin{array}{cccc}\rho\colon&\Omega\subset\mathbb{R}^m&\longrightarrow&M\cap G\subseteq\mathbb{R}^n\\&\mathbf{u}&\longmapsto&\rho(\mathbf{u})\\&\mathbf{b}&\longmapsto&\mathbf{a}\end{array}$$
Més concretament, sabem que $\rho\in\mathcal{C}^r(\Omega)$, $\mathrm{rang}D\rho(\mathbf{u})=m$ per a tot $\mathbf{u}\in\Omega$, $\rho$ bijectiva i amb inversa contínua.

Recordem, a més, que $T_M(\mathbf{a})=\mathrm{Im}(D\rho(\mathbf{b}))=\langle\text{columnes de }D\rho(\mathbf{b})\rangle\subseteq\mathbb{R}^n$.

Considerem ara la composició de $\rho$ amb $f$:
$$\begin{array}{ccccc}\Omega\subset\mathbb{R}^m&\xrightarrow{\ \rho\ }&M\cap G&\xrightarrow{\ f\ }&\mathbb{R}\\\mathbf{u}&\longmapsto&\rho(\mathbf{u})&\longrightarrow&f(\rho(\mathbf{u}))\\\mathbf{b}&\longmapsto&\mathbf{a}&\longrightarrow&f(\mathbf{a})\end{array}$$
A continuació, farem tres observacions que ens conduiran a la demostració.

**Observació 19.1** $\mathbf{a}$ és un màxim (respectivament, mínim o punt de sella) de $f$ condicionat a $M\Leftrightarrow\mathbf{b}$ és un màxim (resp., mínim o punt de sella) de $g:=f\circ\rho$.

Per a demostrar-la, només cal veure que $\nabla g(\mathbf{b})=\nabla f(\mathbf{a})\,D\rho(\mathbf{b})=0$ perquè $\nabla f(\mathbf{a})\in N_M(\mathbf{a})$ (la igualtat ens diu que és ortogonal a tota columna de $D\rho(\mathbf{b})$, i les columnes de $D\rho(\mathbf{b})$ generen $T_M(\mathbf{a})$).

**Observació 19.2** Sigui $G=F\circ\rho$:
$$\begin{array}{ccccc}G\colon&\Omega&\xrightarrow{\ \rho\ }&M\cap G&\xrightarrow{\ F\ }&\mathbb{R}\\&\mathbf{u}&\longmapsto&\rho(\mathbf{u})&\longrightarrow&F(\rho(\mathbf{u}))=f(\rho(\mathbf{u}))+\boldsymbol{\lambda}\cdot\Phi(\rho(\mathbf{u}))\end{array}$$
Aleshores, $G=F\circ\rho=f\circ\rho=g$.

Per valorar l'interès d'aquesta observació, recordem que $f$ és la funció que volem estudiar sobre $M$ mentre que $F$ és la funció de Lagrange per a un $\boldsymbol{\lambda}$ fixat (corresponent al punt crític de la funció de Lagrange).

Per a demostrar-la, fixem-nos que, $\Phi(\rho(u))=0$ ja que $\rho(u)\in M_\Phi$. Per tant, $\boldsymbol{\lambda}\cdot\Phi(\rho(u))=0$ i, aleshores, $F(\rho(u))=f(\rho(u))+0$.

Aquesta observació ens servirà per a calcular la hessiana de $G$ en lloc de la hessiana de $g$. En la següent observació connectem les hessianes de $G$ i $F$.

**Observació 19.3** Per a tot $\mathbf{v}\in\mathbb{R}^m$,
$$\mathbf{v}^T\,HG(\mathbf{b})\,\mathbf{v}=\mathbf{v}^T\,(D\rho(\mathbf{b}))^T\,HF(\mathbf{a})\,D\rho(\mathbf{b})\,\mathbf{v}.$$
Per a demostrar-ho, calcularem ambdós costats de la demostració per separat i veurem que coincideixen.

- Calculem $\mathbf{v}^T\,HG(\mathbf{b})\,\mathbf{v}$:

Les primeres derivades de $G$, per a $i=1,\ldots,m$, s'expressen com:
$$\frac{\partial G}{\partial u_i}(\mathbf{u})=\sum_{k=1}^n\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_k}{\partial u_i}(\mathbf{u}).$$
Fem ara la segona derivada respecte una variable $u_j$:
$$\begin{aligned}\frac{\partial^2G}{\partial u_j\partial u_i}(\mathbf{u})&=\frac{\partial}{\partial u_j}\left(\sum_{k=1}^n\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})\right)\\&=\sum_{k=1}^n\left(\frac{\partial}{\partial u_j}\left(\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\right)\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})+\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial}{\partial u_j}\left(\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})\right)\right)\\&=\sum_{k=1}^n\left(\left(\sum_{l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_l}{\partial u_j}(\mathbf{u})\right)\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})+\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial^2\rho_k}{\partial u_j\partial u_i}(\mathbf{u})\right)\end{aligned}$$
Substituint $\mathbf{u}=\mathbf{b}$ i tenint en compte que $\dfrac{\partial F}{\partial x_k}(\rho(\mathbf{b}))\dfrac{\partial^2\rho_k}{\partial u_j\partial u_i}(\mathbf{b})=0$ ja que $\dfrac{\partial L}{\partial x_k}(\mathbf{a},\boldsymbol{\lambda})=0$ (i, per tant, $\dfrac{\partial F}{\partial x_k}(\rho(\mathbf{b}))=\dfrac{\partial F}{\partial x_k}(\mathbf{a})=0$), per a $k=1,\ldots,n$, obtenim:
$$\frac{\partial^2G}{\partial u_j\partial u_i}(\mathbf{b})=\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\frac{\partial\rho_k}{\partial u_i}(\mathbf{b}).$$
Llavors,
$$\mathbf{v}^T\,HG(\mathbf{b})\,\mathbf{v}=\sum_{i,j=1}^m\left(\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})\right)v_i\,v_j.\tag{2}$$

- Calculem $\mathbf{v}^T\,(D\rho(\mathbf{b}))^T\,HF(\mathbf{a})\,D\rho(\mathbf{b})\,\mathbf{v}$:

Comencem amb el terme $D\rho(\mathbf{b})\,\mathbf{v}$:
$$D\rho(\mathbf{b})\,\mathbf{v}=\begin{pmatrix}\frac{\partial\rho_1}{\partial u_1}&\cdots&\frac{\partial\rho_1}{\partial u_m}\\\vdots&\vdots&\vdots\\\frac{\partial\rho_n}{\partial u_1}&\cdots&\frac{\partial\rho_n}{\partial u_m}\end{pmatrix}\begin{pmatrix}v_1\\\vdots\\v_m\end{pmatrix}=\begin{pmatrix}\sum_{r=1}^m\frac{\partial\rho_1}{\partial u_r}(\mathbf{b})\,v_r\\\vdots\\\sum_{r=1}^m\frac{\partial\rho_n}{\partial u_r}(\mathbf{b})\,v_r\end{pmatrix}$$
Llavors,
$$\begin{aligned}\mathbf{v}^T\,(D\rho(\mathbf{b}))^T\,HF(\mathbf{a})\,D\rho(\mathbf{b})\,\mathbf{v}&=\sum_{k,l=1}^n\left(\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\left(\sum_{i=1}^m\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})\,v_i\right)\left(\sum_{j=1}^m\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\,v_j\right)\right)\\&=\sum_{k,l=1}^n\left(\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\sum_{i,j=1}^m\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})\,v_i\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\,v_j\right)\\&=\sum_{i,j=1}^m\left(\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\right)v_i\,v_j,\end{aligned}$$
que coincideix amb l'equació (2).

Finalment, ajuntant les tres observacions, per exemple, en el cas d'un màxim (els demés casos són anàlegs seguint l'esperit del teorema 33 del tema 5), tenim que:
$$\begin{aligned}&\mathbf{a}\text{ és un màxim de }f\text{ condicionat a }M\text{ estricte}\\\Leftrightarrow\ &\mathbf{b}\text{ és un màxim local estricte de }g=G\\\Leftrightarrow\ &q_{HG(\mathbf{b})}<0\text{ per a tot }\mathbf{v}\in\mathbb{R}^n\\\Leftrightarrow\ &q_{HF(\mathbf{a})}<0\text{ per a tot vector de la forma }D\rho(\mathbf{b})\,\mathbf{v}\in\mathbb{R}^n.\end{aligned}$$
Però, com que les columnes de $D\rho(\mathbf{b})$ generen l'espai tangent, equival a dir que
$$\mathbf{a}\text{ és un màxim de }f\text{ condicionat a }M\text{ estricte}\Leftrightarrow q_{HF(\mathbf{a})}<0\text{ per a tot }\mathbf{w}\in T_M(\mathbf{a}).$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (condicions suficients). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ com en el corol·lari 17, amb $r\geq2$, $M=M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^2(G)$. Sigui $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in M\times\mathbb{R}^{n-m}$ un punt crític de la funció de Lagrange $L$, i considerem $F\colon G\to\mathbb{R}$, $F(\mathbf{x})=L(\mathbf{x},\lambda_1,\ldots,\lambda_{n-m})=f(\mathbf{x})+\boldsymbol{\lambda}\cdot\Phi(\mathbf{x})$.
[2] (enunciat) Llavors, (i) $q_{HF(\mathbf{a})}$ és definida negativa sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un mínim local estricte de $f$ condicionat a $M$; (ii) $q_{HF(\mathbf{a})}$ és definida positiva sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un mínim local estricte de $f$ condicionat a $M$; (iii) $q_{HF(\mathbf{a})}$ és indefinida sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un punt de sella de $f$ condicionat a $M$.
[3] (enunciat) (iv) $\mathbf{a}$ és un màxim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida negativa sobre $T_M(\mathbf{a})$; (v) $\mathbf{a}$ és un mínim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida positiva sobre $T_M(\mathbf{a})$.
[4] (demostració) Sigui $\rho\colon\Omega\subseteq\mathbb{R}^m\to M\cap G$ una parametrització de $M$ al voltant de $\mathbf{a}$, amb $\rho(\mathbf{b})=\mathbf{a}$: $\rho\in\mathcal{C}^r(\Omega)$, $\mathrm{rang}\,D\rho(\mathbf{u})=m$ per a tot $\mathbf{u}\in\Omega$, $\rho$ bijectiva i amb inversa contínua. Pel teorema 10, $T_M(\mathbf{a})=\mathrm{Im}\,D\rho(\mathbf{b})=\langle\text{columnes de }D\rho(\mathbf{b})\rangle$.
[5] (demostració) Observació 19.1: sigui $g:=f\circ\rho\colon\Omega\to\mathbb{R}$. Com que $\rho$ és un homeomorfisme de $\Omega$ sobre l'entorn $M\cap G$ de $\mathbf{a}$ en $M$, $\mathbf{a}$ és un màxim (resp. mínim, punt de sella) local de $f$ condicionat a $M$, estricte o no, si i només si $\mathbf{b}$ ho és de $g$. A més, $\nabla g(\mathbf{b})=\nabla f(\mathbf{a})\,D\rho(\mathbf{b})=\mathbf{0}$, perquè $\nabla f(\mathbf{a})=-\lambda_1\nabla\Phi_1(\mathbf{a})-\cdots-\lambda_{n-m}\nabla\Phi_{n-m}(\mathbf{a})$ (ja que $(\mathbf{a},\boldsymbol{\lambda})$ és punt crític de $L$) pertany a $N_M(\mathbf{a})$ pel teorema 10, i per tant és ortogonal a les columnes de $D\rho(\mathbf{b})$.
[6] (demostració) Observació 19.2: com que $\rho(\mathbf{u})\in M_\Phi$, $\Phi(\rho(\mathbf{u}))=\mathbf{0}$ per a tot $\mathbf{u}\in\Omega$; per tant, $F\circ\rho=f\circ\rho+\boldsymbol{\lambda}\cdot(\Phi\circ\rho)=g$. Així, podem calcular la hessiana de $g$ com la de $F\circ\rho$.
[7] (demostració) Observació 19.3: per la regla de la cadena, $\frac{\partial g}{\partial u_i}(\mathbf{u})=\sum_{k=1}^n\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})$ i, derivant de nou respecte de $u_j$ (regla del producte i de la cadena), $\frac{\partial^2g}{\partial u_j\partial u_i}(\mathbf{u})=\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_l}{\partial u_j}(\mathbf{u})\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})+\sum_{k=1}^n\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial^2\rho_k}{\partial u_j\partial u_i}(\mathbf{u})$.
[8] (demostració) En $\mathbf{u}=\mathbf{b}$ el segon sumatori s'anul·la, ja que $\frac{\partial F}{\partial x_k}(\mathbf{a})=\frac{\partial L}{\partial x_k}(\mathbf{a},\boldsymbol{\lambda})=0$ per a $k=1,\ldots,n$, perquè $(\mathbf{a},\boldsymbol{\lambda})$ és un punt crític de $L$. Per tant, $\frac{\partial^2g}{\partial u_j\partial u_i}(\mathbf{b})=\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})$.
[9] (demostració) Matricialment, $Hg(\mathbf{b})=D\rho(\mathbf{b})^T\,HF(\mathbf{a})\,D\rho(\mathbf{b})$ i, per a tot $\mathbf{v}\in\mathbb{R}^m$, $\mathbf{v}^T\,Hg(\mathbf{b})\,\mathbf{v}=(D\rho(\mathbf{b})\,\mathbf{v})^T\,HF(\mathbf{a})\,(D\rho(\mathbf{b})\,\mathbf{v})$, és a dir, $q_{Hg(\mathbf{b})}(\mathbf{v})=q_{HF(\mathbf{a})}(D\rho(\mathbf{b})\,\mathbf{v})$.
[10] (demostració) L'aplicació $\mathbf{v}\mapsto D\rho(\mathbf{b})\,\mathbf{v}$ és un isomorfisme de $\mathbb{R}^m$ sobre $T_M(\mathbf{a})$, ja que $D\rho(\mathbf{b})$ té rang $m$ i la seva imatge és $T_M(\mathbf{a})$. Per tant, $q_{Hg(\mathbf{b})}$ és definida negativa (positiva, indefinida, semidefinida negativa, semidefinida positiva) en $\mathbb{R}^m$ si i només si $q_{HF(\mathbf{a})}$ ho és sobre $T_M(\mathbf{a})$.
[11] (demostració) Ara apliquem a $g$, que és de classe $\mathcal{C}^2$ (perquè $f\in\mathcal{C}^2$ i $r\geq2$) i té $\mathbf{b}$ com a punt crític, els criteris del tema 5 (teorema 33): si $q_{HF(\mathbf{a})}$ és definida negativa sobre $T_M(\mathbf{a})$, $q_{Hg(\mathbf{b})}$ és definida negativa, $\mathbf{b}$ és un màxim local estricte de $g$ i, per l'observació 19.1, $\mathbf{a}$ és un màxim local estricte de $f$ condicionat a $M$. Els casos (ii) i (iii) són anàlegs.
[12] (demostració) Recíprocament, si $\mathbf{a}$ és un màxim (mínim) local de $f$ condicionat a $M$, per l'observació 19.1 $\mathbf{b}$ és un màxim (mínim) local de $g$, i la condició necessària de segon ordre dona $q_{Hg(\mathbf{b})}$ semidefinida negativa (positiva). Per l'equivalència anterior, $q_{HF(\mathbf{a})}$ ho és sobre $T_M(\mathbf{a})$, cosa que prova (iv) i (v).


## T6.19:normal

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T6.19] Teorema 19 (Tema 6) — Condicions suficients d'extrem condicionat
(condicions suficients). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ com en el corol·lari 17, amb $r\geq2$, $M=M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^2(G)$. Sigui $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in M\times\mathbb{R}^{n-m}$ un punt crític de la funció de Lagrange $L$; considerem la subfunció $F\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ donada per $F(\mathbf{x})=L(\mathbf{x},\lambda_1,\ldots,\lambda_{n-m})$. Llavors,

(i) $q_{HF(\mathbf{a})}$ és definida negativa ($\ominus$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un màxim local estricte de $f$ condicionat a $M$;

(ii) $q_{HF(\mathbf{a})}$ és definida positiva ($\oplus$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un mínim local estricte de $f$ condicionat a $M$;

(iii) $q_{HF(\mathbf{a})}$ és indefinida ($\odot$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un punt de sella de $f$ condicionat a $M$;

(iv) $\mathbf{a}$ és un màxim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida negativa ($\underline{\ominus}$) sobre $T_M(\mathbf{a})$;

(v) $\mathbf{a}$ és un mínim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida positiva ($\underline{\oplus}$) sobre $T_M(\mathbf{a})$.
Demostració: Sigui $\rho$ una parametrització de $M$:
$$\begin{array}{cccc}\rho\colon&\Omega\subset\mathbb{R}^m&\longrightarrow&M\cap G\subseteq\mathbb{R}^n\\&\mathbf{u}&\longmapsto&\rho(\mathbf{u})\\&\mathbf{b}&\longmapsto&\mathbf{a}\end{array}$$
Més concretament, sabem que $\rho\in\mathcal{C}^r(\Omega)$, $\mathrm{rang}D\rho(\mathbf{u})=m$ per a tot $\mathbf{u}\in\Omega$, $\rho$ bijectiva i amb inversa contínua.

Recordem, a més, que $T_M(\mathbf{a})=\mathrm{Im}(D\rho(\mathbf{b}))=\langle\text{columnes de }D\rho(\mathbf{b})\rangle\subseteq\mathbb{R}^n$.

Considerem ara la composició de $\rho$ amb $f$:
$$\begin{array}{ccccc}\Omega\subset\mathbb{R}^m&\xrightarrow{\ \rho\ }&M\cap G&\xrightarrow{\ f\ }&\mathbb{R}\\\mathbf{u}&\longmapsto&\rho(\mathbf{u})&\longrightarrow&f(\rho(\mathbf{u}))\\\mathbf{b}&\longmapsto&\mathbf{a}&\longrightarrow&f(\mathbf{a})\end{array}$$
A continuació, farem tres observacions que ens conduiran a la demostració.

**Observació 19.1** $\mathbf{a}$ és un màxim (respectivament, mínim o punt de sella) de $f$ condicionat a $M\Leftrightarrow\mathbf{b}$ és un màxim (resp., mínim o punt de sella) de $g:=f\circ\rho$.

Per a demostrar-la, només cal veure que $\nabla g(\mathbf{b})=\nabla f(\mathbf{a})\,D\rho(\mathbf{b})=0$ perquè $\nabla f(\mathbf{a})\in N_M(\mathbf{a})$ (la igualtat ens diu que és ortogonal a tota columna de $D\rho(\mathbf{b})$, i les columnes de $D\rho(\mathbf{b})$ generen $T_M(\mathbf{a})$).

**Observació 19.2** Sigui $G=F\circ\rho$:
$$\begin{array}{ccccc}G\colon&\Omega&\xrightarrow{\ \rho\ }&M\cap G&\xrightarrow{\ F\ }&\mathbb{R}\\&\mathbf{u}&\longmapsto&\rho(\mathbf{u})&\longrightarrow&F(\rho(\mathbf{u}))=f(\rho(\mathbf{u}))+\boldsymbol{\lambda}\cdot\Phi(\rho(\mathbf{u}))\end{array}$$
Aleshores, $G=F\circ\rho=f\circ\rho=g$.

Per valorar l'interès d'aquesta observació, recordem que $f$ és la funció que volem estudiar sobre $M$ mentre que $F$ és la funció de Lagrange per a un $\boldsymbol{\lambda}$ fixat (corresponent al punt crític de la funció de Lagrange).

Per a demostrar-la, fixem-nos que, $\Phi(\rho(u))=0$ ja que $\rho(u)\in M_\Phi$. Per tant, $\boldsymbol{\lambda}\cdot\Phi(\rho(u))=0$ i, aleshores, $F(\rho(u))=f(\rho(u))+0$.

Aquesta observació ens servirà per a calcular la hessiana de $G$ en lloc de la hessiana de $g$. En la següent observació connectem les hessianes de $G$ i $F$.

**Observació 19.3** Per a tot $\mathbf{v}\in\mathbb{R}^m$,
$$\mathbf{v}^T\,HG(\mathbf{b})\,\mathbf{v}=\mathbf{v}^T\,(D\rho(\mathbf{b}))^T\,HF(\mathbf{a})\,D\rho(\mathbf{b})\,\mathbf{v}.$$
Per a demostrar-ho, calcularem ambdós costats de la demostració per separat i veurem que coincideixen.

- Calculem $\mathbf{v}^T\,HG(\mathbf{b})\,\mathbf{v}$:

Les primeres derivades de $G$, per a $i=1,\ldots,m$, s'expressen com:
$$\frac{\partial G}{\partial u_i}(\mathbf{u})=\sum_{k=1}^n\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_k}{\partial u_i}(\mathbf{u}).$$
Fem ara la segona derivada respecte una variable $u_j$:
$$\begin{aligned}\frac{\partial^2G}{\partial u_j\partial u_i}(\mathbf{u})&=\frac{\partial}{\partial u_j}\left(\sum_{k=1}^n\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})\right)\\&=\sum_{k=1}^n\left(\frac{\partial}{\partial u_j}\left(\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\right)\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})+\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial}{\partial u_j}\left(\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})\right)\right)\\&=\sum_{k=1}^n\left(\left(\sum_{l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_l}{\partial u_j}(\mathbf{u})\right)\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})+\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial^2\rho_k}{\partial u_j\partial u_i}(\mathbf{u})\right)\end{aligned}$$
Substituint $\mathbf{u}=\mathbf{b}$ i tenint en compte que $\dfrac{\partial F}{\partial x_k}(\rho(\mathbf{b}))\dfrac{\partial^2\rho_k}{\partial u_j\partial u_i}(\mathbf{b})=0$ ja que $\dfrac{\partial L}{\partial x_k}(\mathbf{a},\boldsymbol{\lambda})=0$ (i, per tant, $\dfrac{\partial F}{\partial x_k}(\rho(\mathbf{b}))=\dfrac{\partial F}{\partial x_k}(\mathbf{a})=0$), per a $k=1,\ldots,n$, obtenim:
$$\frac{\partial^2G}{\partial u_j\partial u_i}(\mathbf{b})=\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\frac{\partial\rho_k}{\partial u_i}(\mathbf{b}).$$
Llavors,
$$\mathbf{v}^T\,HG(\mathbf{b})\,\mathbf{v}=\sum_{i,j=1}^m\left(\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})\right)v_i\,v_j.\tag{2}$$

- Calculem $\mathbf{v}^T\,(D\rho(\mathbf{b}))^T\,HF(\mathbf{a})\,D\rho(\mathbf{b})\,\mathbf{v}$:

Comencem amb el terme $D\rho(\mathbf{b})\,\mathbf{v}$:
$$D\rho(\mathbf{b})\,\mathbf{v}=\begin{pmatrix}\frac{\partial\rho_1}{\partial u_1}&\cdots&\frac{\partial\rho_1}{\partial u_m}\\\vdots&\vdots&\vdots\\\frac{\partial\rho_n}{\partial u_1}&\cdots&\frac{\partial\rho_n}{\partial u_m}\end{pmatrix}\begin{pmatrix}v_1\\\vdots\\v_m\end{pmatrix}=\begin{pmatrix}\sum_{r=1}^m\frac{\partial\rho_1}{\partial u_r}(\mathbf{b})\,v_r\\\vdots\\\sum_{r=1}^m\frac{\partial\rho_n}{\partial u_r}(\mathbf{b})\,v_r\end{pmatrix}$$
Llavors,
$$\begin{aligned}\mathbf{v}^T\,(D\rho(\mathbf{b}))^T\,HF(\mathbf{a})\,D\rho(\mathbf{b})\,\mathbf{v}&=\sum_{k,l=1}^n\left(\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\left(\sum_{i=1}^m\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})\,v_i\right)\left(\sum_{j=1}^m\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\,v_j\right)\right)\\&=\sum_{k,l=1}^n\left(\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\sum_{i,j=1}^m\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})\,v_i\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\,v_j\right)\\&=\sum_{i,j=1}^m\left(\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\right)v_i\,v_j,\end{aligned}$$
que coincideix amb l'equació (2).

Finalment, ajuntant les tres observacions, per exemple, en el cas d'un màxim (els demés casos són anàlegs seguint l'esperit del teorema 33 del tema 5), tenim que:
$$\begin{aligned}&\mathbf{a}\text{ és un màxim de }f\text{ condicionat a }M\text{ estricte}\\\Leftrightarrow\ &\mathbf{b}\text{ és un màxim local estricte de }g=G\\\Leftrightarrow\ &q_{HG(\mathbf{b})}<0\text{ per a tot }\mathbf{v}\in\mathbb{R}^n\\\Leftrightarrow\ &q_{HF(\mathbf{a})}<0\text{ per a tot vector de la forma }D\rho(\mathbf{b})\,\mathbf{v}\in\mathbb{R}^n.\end{aligned}$$
Però, com que les columnes de $D\rho(\mathbf{b})$ generen l'espai tangent, equival a dir que
$$\mathbf{a}\text{ és un màxim de }f\text{ condicionat a }M\text{ estricte}\Leftrightarrow q_{HF(\mathbf{a})}<0\text{ per a tot }\mathbf{w}\in T_M(\mathbf{a}).$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (condicions suficients). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ com en el corol·lari 17, amb $r\geq2$, $M=M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^2(G)$. Sigui $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in M\times\mathbb{R}^{n-m}$ un punt crític de la funció de Lagrange $L$, i considerem $F\colon G\to\mathbb{R}$, $F(\mathbf{x})=L(\mathbf{x},\lambda_1,\ldots,\lambda_{n-m})=f(\mathbf{x})+\boldsymbol{\lambda}\cdot\Phi(\mathbf{x})$.
[2] (enunciat) Llavors, (i) $q_{HF(\mathbf{a})}$ és definida negativa sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un màxim local estricte de $f$ condicionat a $M$; (ii) $q_{HF(\mathbf{a})}$ és definida positiva sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un mínim local estricte de $f$ condicionat a $M$; (iii) $q_{HF(\mathbf{a})}$ és indefinida sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un punt de sella de $f$ condicionat a $M$.
[3] (enunciat) (iv) $\mathbf{a}$ és un màxim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és definida negativa sobre $T_M(\mathbf{a})$; (v) $\mathbf{a}$ és un mínim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida positiva sobre $T_M(\mathbf{a})$.
[4] (demostració) Sigui $\rho\colon\Omega\subseteq\mathbb{R}^m\to M\cap G$ una parametrització de $M$ al voltant de $\mathbf{a}$, amb $\rho(\mathbf{b})=\mathbf{a}$: $\rho\in\mathcal{C}^r(\Omega)$, $\mathrm{rang}\,D\rho(\mathbf{u})=m$ per a tot $\mathbf{u}\in\Omega$, $\rho$ bijectiva i amb inversa contínua. Pel teorema 10, $T_M(\mathbf{a})=\mathrm{Im}\,D\rho(\mathbf{b})=\langle\text{columnes de }D\rho(\mathbf{b})\rangle$.
[5] (demostració) Observació 19.1: sigui $g:=f\circ\rho\colon\Omega\to\mathbb{R}$. Com que $\rho$ és un homeomorfisme de $\Omega$ sobre l'entorn $M\cap G$ de $\mathbf{a}$ en $M$, $\mathbf{a}$ és un màxim (resp. mínim, punt de sella) local de $f$ condicionat a $M$, estricte o no, si i només si $\mathbf{b}$ ho és de $g$. A més, $\nabla g(\mathbf{b})=\nabla f(\mathbf{a})\,D\rho(\mathbf{b})=\mathbf{0}$, perquè $\nabla f(\mathbf{a})=-\lambda_1\nabla\Phi_1(\mathbf{a})-\cdots-\lambda_{n-m}\nabla\Phi_{n-m}(\mathbf{a})$ (ja que $(\mathbf{a},\boldsymbol{\lambda})$ és punt crític de $L$) pertany a $N_M(\mathbf{a})$ pel teorema 10, i per tant és ortogonal a les columnes de $D\rho(\mathbf{b})$.
[6] (demostració) Observació 19.2: com que $\rho(\mathbf{u})\in M_\Phi$, $\Phi(\rho(\mathbf{u}))=\mathbf{0}$ per a tot $\mathbf{u}\in\Omega$; per tant, $F\circ\rho=f\circ\rho+\boldsymbol{\lambda}\cdot(\Phi\circ\rho)=g$. Així, podem calcular la hessiana de $g$ com la de $F\circ\rho$.
[7] (demostració) Observació 19.3: per la regla de la cadena, $\frac{\partial g}{\partial u_i}(\mathbf{u})=\sum_{k=1}^n\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})$ i, derivant de nou respecte de $u_j$ (regla del producte i de la cadena), $\frac{\partial^2g}{\partial u_j\partial u_i}(\mathbf{u})=\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_l}{\partial u_j}(\mathbf{u})\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})+\sum_{k=1}^n\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial^2\rho_k}{\partial u_j\partial u_i}(\mathbf{u})$.
[8] (demostració) En $\mathbf{u}=\mathbf{b}$ el segon sumatori s'anul·la, ja que, com que $\mathbf{b}$ és un punt crític de $g$, les derivades segones $\frac{\partial^2\rho_k}{\partial u_j\partial u_i}(\mathbf{b})$ són nul·les. Per tant, $\frac{\partial^2g}{\partial u_j\partial u_i}(\mathbf{b})=\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})$.
[9] (demostració) Matricialment, $Hg(\mathbf{b})=D\rho(\mathbf{b})^T\,HF(\mathbf{a})\,D\rho(\mathbf{b})$ i, per a tot $\mathbf{v}\in\mathbb{R}^m$, $\mathbf{v}^T\,Hg(\mathbf{b})\,\mathbf{v}=(D\rho(\mathbf{b})\,\mathbf{v})^T\,HF(\mathbf{a})\,(D\rho(\mathbf{b})\,\mathbf{v})$, és a dir, $q_{Hg(\mathbf{b})}(\mathbf{v})=q_{HF(\mathbf{a})}(D\rho(\mathbf{b})\,\mathbf{v})$.
[10] (demostració) L'aplicació $\mathbf{v}\mapsto D\rho(\mathbf{b})\,\mathbf{v}$ és un isomorfisme de $\mathbb{R}^m$ sobre $T_M(\mathbf{a})$, ja que $D\rho(\mathbf{b})$ té rang $m$ i la seva imatge és $T_M(\mathbf{a})$. Per tant, $q_{Hg(\mathbf{b})}$ és definida negativa (positiva, indefinida, semidefinida negativa, semidefinida positiva) en $\mathbb{R}^m$ si i només si $q_{HF(\mathbf{a})}$ ho és sobre $T_M(\mathbf{a})$.
[11] (demostració) Ara apliquem a $g$, que és de classe $\mathcal{C}^2$ (perquè $f\in\mathcal{C}^2$ i $r\geq2$) i té $\mathbf{b}$ com a punt crític, els criteris del tema 5 (teorema 33): si $q_{HF(\mathbf{a})}$ és definida negativa sobre $T_M(\mathbf{a})$, $q_{Hg(\mathbf{b})}$ és definida negativa, $\mathbf{b}$ és un màxim local estricte de $g$ i, per l'observació 19.1, $\mathbf{a}$ és un màxim local estricte de $f$ condicionat a $M$. Els casos (ii) i (iii) són anàlegs.
[12] (demostració) Recíprocament, si $\mathbf{a}$ és un màxim (mínim) local de $f$ condicionat a $M$, per l'observació 19.1 $\mathbf{b}$ és un màxim (mínim) local de $g$, i la condició necessària de segon ordre dona $q_{Hg(\mathbf{b})}$ semidefinida negativa (positiva). Per l'equivalència anterior, $q_{HF(\mathbf{a})}$ ho és sobre $T_M(\mathbf{a})$, cosa que prova (iv) i (v).


## T6.19:dificil

### Referència

<apunts>
ÍTEM DELS APUNTS (versió CORRECTA, la referència):
[T6.19] Teorema 19 (Tema 6) — Condicions suficients d'extrem condicionat
(condicions suficients). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ com en el corol·lari 17, amb $r\geq2$, $M=M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^2(G)$. Sigui $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in M\times\mathbb{R}^{n-m}$ un punt crític de la funció de Lagrange $L$; considerem la subfunció $F\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ donada per $F(\mathbf{x})=L(\mathbf{x},\lambda_1,\ldots,\lambda_{n-m})$. Llavors,

(i) $q_{HF(\mathbf{a})}$ és definida negativa ($\ominus$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un màxim local estricte de $f$ condicionat a $M$;

(ii) $q_{HF(\mathbf{a})}$ és definida positiva ($\oplus$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un mínim local estricte de $f$ condicionat a $M$;

(iii) $q_{HF(\mathbf{a})}$ és indefinida ($\odot$) sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un punt de sella de $f$ condicionat a $M$;

(iv) $\mathbf{a}$ és un màxim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida negativa ($\underline{\ominus}$) sobre $T_M(\mathbf{a})$;

(v) $\mathbf{a}$ és un mínim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida positiva ($\underline{\oplus}$) sobre $T_M(\mathbf{a})$.
Demostració: Sigui $\rho$ una parametrització de $M$:
$$\begin{array}{cccc}\rho\colon&\Omega\subset\mathbb{R}^m&\longrightarrow&M\cap G\subseteq\mathbb{R}^n\\&\mathbf{u}&\longmapsto&\rho(\mathbf{u})\\&\mathbf{b}&\longmapsto&\mathbf{a}\end{array}$$
Més concretament, sabem que $\rho\in\mathcal{C}^r(\Omega)$, $\mathrm{rang}D\rho(\mathbf{u})=m$ per a tot $\mathbf{u}\in\Omega$, $\rho$ bijectiva i amb inversa contínua.

Recordem, a més, que $T_M(\mathbf{a})=\mathrm{Im}(D\rho(\mathbf{b}))=\langle\text{columnes de }D\rho(\mathbf{b})\rangle\subseteq\mathbb{R}^n$.

Considerem ara la composició de $\rho$ amb $f$:
$$\begin{array}{ccccc}\Omega\subset\mathbb{R}^m&\xrightarrow{\ \rho\ }&M\cap G&\xrightarrow{\ f\ }&\mathbb{R}\\\mathbf{u}&\longmapsto&\rho(\mathbf{u})&\longrightarrow&f(\rho(\mathbf{u}))\\\mathbf{b}&\longmapsto&\mathbf{a}&\longrightarrow&f(\mathbf{a})\end{array}$$
A continuació, farem tres observacions que ens conduiran a la demostració.

**Observació 19.1** $\mathbf{a}$ és un màxim (respectivament, mínim o punt de sella) de $f$ condicionat a $M\Leftrightarrow\mathbf{b}$ és un màxim (resp., mínim o punt de sella) de $g:=f\circ\rho$.

Per a demostrar-la, només cal veure que $\nabla g(\mathbf{b})=\nabla f(\mathbf{a})\,D\rho(\mathbf{b})=0$ perquè $\nabla f(\mathbf{a})\in N_M(\mathbf{a})$ (la igualtat ens diu que és ortogonal a tota columna de $D\rho(\mathbf{b})$, i les columnes de $D\rho(\mathbf{b})$ generen $T_M(\mathbf{a})$).

**Observació 19.2** Sigui $G=F\circ\rho$:
$$\begin{array}{ccccc}G\colon&\Omega&\xrightarrow{\ \rho\ }&M\cap G&\xrightarrow{\ F\ }&\mathbb{R}\\&\mathbf{u}&\longmapsto&\rho(\mathbf{u})&\longrightarrow&F(\rho(\mathbf{u}))=f(\rho(\mathbf{u}))+\boldsymbol{\lambda}\cdot\Phi(\rho(\mathbf{u}))\end{array}$$
Aleshores, $G=F\circ\rho=f\circ\rho=g$.

Per valorar l'interès d'aquesta observació, recordem que $f$ és la funció que volem estudiar sobre $M$ mentre que $F$ és la funció de Lagrange per a un $\boldsymbol{\lambda}$ fixat (corresponent al punt crític de la funció de Lagrange).

Per a demostrar-la, fixem-nos que, $\Phi(\rho(u))=0$ ja que $\rho(u)\in M_\Phi$. Per tant, $\boldsymbol{\lambda}\cdot\Phi(\rho(u))=0$ i, aleshores, $F(\rho(u))=f(\rho(u))+0$.

Aquesta observació ens servirà per a calcular la hessiana de $G$ en lloc de la hessiana de $g$. En la següent observació connectem les hessianes de $G$ i $F$.

**Observació 19.3** Per a tot $\mathbf{v}\in\mathbb{R}^m$,
$$\mathbf{v}^T\,HG(\mathbf{b})\,\mathbf{v}=\mathbf{v}^T\,(D\rho(\mathbf{b}))^T\,HF(\mathbf{a})\,D\rho(\mathbf{b})\,\mathbf{v}.$$
Per a demostrar-ho, calcularem ambdós costats de la demostració per separat i veurem que coincideixen.

- Calculem $\mathbf{v}^T\,HG(\mathbf{b})\,\mathbf{v}$:

Les primeres derivades de $G$, per a $i=1,\ldots,m$, s'expressen com:
$$\frac{\partial G}{\partial u_i}(\mathbf{u})=\sum_{k=1}^n\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_k}{\partial u_i}(\mathbf{u}).$$
Fem ara la segona derivada respecte una variable $u_j$:
$$\begin{aligned}\frac{\partial^2G}{\partial u_j\partial u_i}(\mathbf{u})&=\frac{\partial}{\partial u_j}\left(\sum_{k=1}^n\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})\right)\\&=\sum_{k=1}^n\left(\frac{\partial}{\partial u_j}\left(\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\right)\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})+\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial}{\partial u_j}\left(\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})\right)\right)\\&=\sum_{k=1}^n\left(\left(\sum_{l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_l}{\partial u_j}(\mathbf{u})\right)\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})+\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial^2\rho_k}{\partial u_j\partial u_i}(\mathbf{u})\right)\end{aligned}$$
Substituint $\mathbf{u}=\mathbf{b}$ i tenint en compte que $\dfrac{\partial F}{\partial x_k}(\rho(\mathbf{b}))\dfrac{\partial^2\rho_k}{\partial u_j\partial u_i}(\mathbf{b})=0$ ja que $\dfrac{\partial L}{\partial x_k}(\mathbf{a},\boldsymbol{\lambda})=0$ (i, per tant, $\dfrac{\partial F}{\partial x_k}(\rho(\mathbf{b}))=\dfrac{\partial F}{\partial x_k}(\mathbf{a})=0$), per a $k=1,\ldots,n$, obtenim:
$$\frac{\partial^2G}{\partial u_j\partial u_i}(\mathbf{b})=\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\frac{\partial\rho_k}{\partial u_i}(\mathbf{b}).$$
Llavors,
$$\mathbf{v}^T\,HG(\mathbf{b})\,\mathbf{v}=\sum_{i,j=1}^m\left(\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})\right)v_i\,v_j.\tag{2}$$

- Calculem $\mathbf{v}^T\,(D\rho(\mathbf{b}))^T\,HF(\mathbf{a})\,D\rho(\mathbf{b})\,\mathbf{v}$:

Comencem amb el terme $D\rho(\mathbf{b})\,\mathbf{v}$:
$$D\rho(\mathbf{b})\,\mathbf{v}=\begin{pmatrix}\frac{\partial\rho_1}{\partial u_1}&\cdots&\frac{\partial\rho_1}{\partial u_m}\\\vdots&\vdots&\vdots\\\frac{\partial\rho_n}{\partial u_1}&\cdots&\frac{\partial\rho_n}{\partial u_m}\end{pmatrix}\begin{pmatrix}v_1\\\vdots\\v_m\end{pmatrix}=\begin{pmatrix}\sum_{r=1}^m\frac{\partial\rho_1}{\partial u_r}(\mathbf{b})\,v_r\\\vdots\\\sum_{r=1}^m\frac{\partial\rho_n}{\partial u_r}(\mathbf{b})\,v_r\end{pmatrix}$$
Llavors,
$$\begin{aligned}\mathbf{v}^T\,(D\rho(\mathbf{b}))^T\,HF(\mathbf{a})\,D\rho(\mathbf{b})\,\mathbf{v}&=\sum_{k,l=1}^n\left(\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\left(\sum_{i=1}^m\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})\,v_i\right)\left(\sum_{j=1}^m\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\,v_j\right)\right)\\&=\sum_{k,l=1}^n\left(\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\sum_{i,j=1}^m\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})\,v_i\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\,v_j\right)\\&=\sum_{i,j=1}^m\left(\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\right)v_i\,v_j,\end{aligned}$$
que coincideix amb l'equació (2).

Finalment, ajuntant les tres observacions, per exemple, en el cas d'un màxim (els demés casos són anàlegs seguint l'esperit del teorema 33 del tema 5), tenim que:
$$\begin{aligned}&\mathbf{a}\text{ és un màxim de }f\text{ condicionat a }M\text{ estricte}\\\Leftrightarrow\ &\mathbf{b}\text{ és un màxim local estricte de }g=G\\\Leftrightarrow\ &q_{HG(\mathbf{b})}<0\text{ per a tot }\mathbf{v}\in\mathbb{R}^n\\\Leftrightarrow\ &q_{HF(\mathbf{a})}<0\text{ per a tot vector de la forma }D\rho(\mathbf{b})\,\mathbf{v}\in\mathbb{R}^n.\end{aligned}$$
Però, com que les columnes de $D\rho(\mathbf{b})$ generen l'espai tangent, equival a dir que
$$\mathbf{a}\text{ és un màxim de }f\text{ condicionat a }M\text{ estricte}\Leftrightarrow q_{HF(\mathbf{a})}<0\text{ per a tot }\mathbf{w}\in T_M(\mathbf{a}).$$

RESULTATS DELS APUNTS QUE CITA:
(cap)
</apunts>

### Document a revisar

[1] (enunciat) (condicions suficients). Sigui $\Phi\colon G\subseteq\mathbb{R}^n\to\mathbb{R}^{n-m}$ com en el corol·lari 17, amb $r\geq2$, $M=M_\Phi\neq\emptyset$ la seva varietat associada, i $f\colon G\subseteq\mathbb{R}^n\to\mathbb{R}$ una funció $\mathcal{C}^2(G)$. Sigui $(\mathbf{a},\lambda_1,\ldots,\lambda_{n-m})\in M\times\mathbb{R}^{n-m}$ un punt crític de la funció de Lagrange $L$, i considerem $F\colon G\to\mathbb{R}$, $F(\mathbf{x})=L(\mathbf{x},\lambda_1,\ldots,\lambda_{n-m})=f(\mathbf{x})+\boldsymbol{\lambda}\cdot\Phi(\mathbf{x})$.
[2] (enunciat) Llavors, (i) $q_{HF(\mathbf{a})}$ és definida negativa sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un màxim local estricte de $f$ condicionat a $M$; (ii) $q_{Hf(\mathbf{a})}$ és definida positiva sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un mínim local estricte de $f$ condicionat a $M$; (iii) $q_{HF(\mathbf{a})}$ és indefinida sobre $T_M(\mathbf{a})\Rightarrow\mathbf{a}$ és un punt de sella de $f$ condicionat a $M$.
[3] (enunciat) (iv) $\mathbf{a}$ és un màxim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida negativa sobre $T_M(\mathbf{a})$; (v) $\mathbf{a}$ és un mínim local de $f$ condicionat a $M\Rightarrow q_{HF(\mathbf{a})}$ és semidefinida positiva sobre $T_M(\mathbf{a})$.
[4] (demostració) Sigui $\rho\colon\Omega\subseteq\mathbb{R}^m\to M\cap G$ una parametrització de $M$ al voltant de $\mathbf{a}$, amb $\rho(\mathbf{b})=\mathbf{a}$: $\rho\in\mathcal{C}^r(\Omega)$, $\mathrm{rang}\,D\rho(\mathbf{u})=m$ per a tot $\mathbf{u}\in\Omega$, $\rho$ bijectiva i amb inversa contínua. Pel teorema 10, $T_M(\mathbf{a})=\mathrm{Im}\,D\rho(\mathbf{b})=\langle\text{columnes de }D\rho(\mathbf{b})\rangle$.
[5] (demostració) Observació 19.1: sigui $g:=f\circ\rho\colon\Omega\to\mathbb{R}$. Com que $\rho$ és un homeomorfisme de $\Omega$ sobre l'entorn $M\cap G$ de $\mathbf{a}$ en $M$, $\mathbf{a}$ és un màxim (resp. mínim, punt de sella) local de $f$ condicionat a $M$, estricte o no, si i només si $\mathbf{b}$ ho és de $g$. A més, $\nabla g(\mathbf{b})=\nabla f(\mathbf{a})\,D\rho(\mathbf{b})=\mathbf{0}$, perquè, per la proposició 13, $\nabla f(\mathbf{a})\in N_M(\mathbf{a})$ i per tant és ortogonal a les columnes de $D\rho(\mathbf{b})$.
[6] (demostració) Observació 19.2: com que $\rho(\mathbf{u})\in M_\Phi$, $\Phi(\rho(\mathbf{u}))=\mathbf{0}$ per a tot $\mathbf{u}\in\Omega$; per tant, $F\circ\rho=f\circ\rho+\boldsymbol{\lambda}\cdot(\Phi\circ\rho)=g$. Així, podem calcular la hessiana de $g$ com la de $F\circ\rho$.
[7] (demostració) Observació 19.3: per la regla de la cadena, $\frac{\partial g}{\partial u_i}(\mathbf{u})=\sum_{k=1}^n\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})$ i, derivant de nou respecte de $u_j$ (regla del producte i de la cadena), $\frac{\partial^2g}{\partial u_j\partial u_i}(\mathbf{u})=\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\rho(\mathbf{u}))\frac{\partial\rho_l}{\partial u_j}(\mathbf{u})\frac{\partial\rho_k}{\partial u_i}(\mathbf{u})+\sum_{k=1}^n\frac{\partial F}{\partial x_k}(\rho(\mathbf{u}))\frac{\partial^2\rho_k}{\partial u_j\partial u_i}(\mathbf{u})$.
[8] (demostració) En $\mathbf{u}=\mathbf{b}$ el segon sumatori s'anul·la, ja que $\frac{\partial F}{\partial x_k}(\mathbf{a})=\frac{\partial L}{\partial x_k}(\mathbf{a},\boldsymbol{\lambda})=0$ per a $k=1,\ldots,n$, perquè $(\mathbf{a},\boldsymbol{\lambda})$ és un punt crític de $L$. Per tant, $\frac{\partial^2g}{\partial u_j\partial u_i}(\mathbf{b})=\sum_{k,l=1}^n\frac{\partial^2F}{\partial x_l\partial x_k}(\mathbf{a})\frac{\partial\rho_l}{\partial u_j}(\mathbf{b})\frac{\partial\rho_k}{\partial u_i}(\mathbf{b})$.
[9] (demostració) Matricialment, $Hg(\mathbf{b})=D\rho(\mathbf{b})^T\,HF(\mathbf{a})\,D\rho(\mathbf{b})$ i, per a tot $\mathbf{v}\in\mathbb{R}^m$, $\mathbf{v}^T\,Hg(\mathbf{b})\,\mathbf{v}=(D\rho(\mathbf{b})\,\mathbf{v})^T\,HF(\mathbf{a})\,(D\rho(\mathbf{b})\,\mathbf{v})$, és a dir, $q_{Hg(\mathbf{b})}(\mathbf{v})=q_{HF(\mathbf{a})}(D\rho(\mathbf{b})\,\mathbf{v})$.
[10] (demostració) L'aplicació $\mathbf{v}\mapsto D\rho(\mathbf{b})\,\mathbf{v}$ és un isomorfisme de $\mathbb{R}^m$ sobre $T_M(\mathbf{a})$, ja que $D\rho(\mathbf{b})$ és una matriu quadrada invertible. Per tant, $q_{Hg(\mathbf{b})}$ és definida negativa (positiva, indefinida, semidefinida negativa, semidefinida positiva) en $\mathbb{R}^m$ si i només si $q_{HF(\mathbf{a})}$ ho és sobre $T_M(\mathbf{a})$.
[11] (demostració) Ara apliquem a $g$, que és de classe $\mathcal{C}^2$ (perquè $f\in\mathcal{C}^2$ i $r\geq2$) i té $\mathbf{b}$ com a punt crític, els criteris del tema 5 (teorema 33): si $q_{HF(\mathbf{a})}$ és definida negativa sobre $T_M(\mathbf{a})$, $q_{Hg(\mathbf{b})}$ és definida negativa, $\mathbf{b}$ és un màxim local estricte de $g$ i, per l'observació 19.1, $\mathbf{a}$ és un màxim local estricte de $f$ condicionat a $M$. Els casos (ii) i (iii) són anàlegs.
[12] (demostració) Recíprocament, si $\mathbf{a}$ és un màxim (mínim) local de $f$ condicionat a $M$, per l'observació 19.1 $\mathbf{b}$ és un màxim (mínim) local de $g$, i la condició necessària de segon ordre dona $q_{Hg(\mathbf{b})}$ semidefinida negativa (positiva). Per l'equivalència anterior, $q_{HF(\mathbf{a})}$ ho és sobre $T_M(\mathbf{a})$, cosa que prova (iv) i (v).

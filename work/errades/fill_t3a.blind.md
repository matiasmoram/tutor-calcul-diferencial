## t3-1a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Calculeu les derivades parcials de les funcions següents en un punt arbitrari del seu domini:

(a) $u(x,y)=\dfrac{x^2+y^2}{x^2-y^2}$;
RESULTAT CORRECTE: El domini és $\{(x,y)\in\mathbb{R}^2 : x^2\neq y^2\}$ (fora de les rectes $y=\pm x$), que és obert. En tot punt del domini:
$\dfrac{\partial u}{\partial x}(x,y)=\dfrac{-4xy^2}{(x^2-y^2)^2}$, $\qquad\dfrac{\partial u}{\partial y}(x,y)=\dfrac{4x^2y}{(x^2-y^2)^2}$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [domini] Determinar el domini
     objectiu: Determinar on està definida $u$ i comprovar que tots els punts del domini són interiors.
     idea: Un quocient està definit on el denominador no s'anul·la; mira quin tipus de conjunt queda.
     detall: Cal $x^2-y^2\neq0$, és a dir $y\neq\pm x$. El domini és el complementari de les dues rectes $y=x$ i $y=-x$, que és un obert, de manera que té sentit parlar de derivades parcials a tot punt.
  2. [parcial_x] Derivada parcial respecte de x  (teoria: T3.2)
     objectiu: Calcular $\dfrac{\partial u}{\partial x}(x,y)$ en un punt qualsevol del domini.
     idea: Per definició, és la derivada de la funció d'una variable $x\mapsto u(x,y)$ amb $y$ fixat: deriva com a quocient tractant $y$ com a constant.
     detall: $\dfrac{\partial u}{\partial x}=\dfrac{2x(x^2-y^2)-(x^2+y^2)\,2x}{(x^2-y^2)^2}=\dfrac{-4xy^2}{(x^2-y^2)^2}$.
  3. [parcial_y] Derivada parcial respecte de y  (teoria: T3.2)
     objectiu: Calcular $\dfrac{\partial u}{\partial y}(x,y)$ en un punt qualsevol del domini.
     idea: Ara $x$ és la constant; vigila el signe de la derivada del denominador respecte de $y$.
     detall: $\dfrac{\partial u}{\partial y}=\dfrac{2y(x^2-y^2)-(x^2+y^2)(-2y)}{(x^2-y^2)^2}=\dfrac{4x^2y}{(x^2-y^2)^2}$.
ERRORS COMUNS:
  - [signe_denominador] En derivar respecte de $y$, oblida que la derivada de $x^2-y^2$ és $-2y$ (posa $+2y$) i obté un numerador que no simplifica.
  - [no_tracta_constant] Deriva també la variable que hauria de tractar com a constant (p. ex. escriu termes amb $2y$ en $\partial u/\partial x$ provinents de $y^2$).
  - [oblida_domini] Dona les fórmules sense dir on són vàlides, o inclou punts de les rectes $y=\pm x$.

TEORIA DEL CURS QUE FA SERVIR:
[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.
</solucio_de_referencia>

### Document a revisar

[1] La funció $u$ és un quocient de polinomis, de manera que està definida exactament on el denominador no s'anul·la: cal $x^2-y^2\neq0$, és a dir, $y\neq x$ i $y\neq-x$.
[2] El domini és, doncs, el complementari de les rectes $y=x$ i $y=-x$. Com que la unió d'aquestes dues rectes és un conjunt tancat, el domini és obert i té sentit calcular les derivades parcials a qualsevol punt seu.
[3] Per calcular $\dfrac{\partial u}{\partial x}$ fixem $y$ i derivem el quocient respecte de $x$: la derivada del numerador $x^2+y^2$ és $2x$, i la del denominador $x^2-y^2$ també és $2x$.
[4] Aplicant la regla del quocient, $\dfrac{\partial u}{\partial x}=\dfrac{2x(x^2-y^2)-(x^2+y^2)\,2x}{(x^2-y^2)^2}=\dfrac{4xy^2}{(x^2-y^2)^2}$.
[5] Per calcular $\dfrac{\partial u}{\partial y}$ fixem $x$. Com que la derivada de $x^2-y^2$ respecte de $y$ és $2y$, la regla del quocient dona $\dfrac{\partial u}{\partial y}=\dfrac{2y(x^2-y^2)-(x^2+y^2)\,2y}{(x^2-y^2)^2}=\dfrac{-4y^3}{(x^2-y^2)^2}$.
[6] Aquestes fórmules són vàlides a tot punt del domini, ja que el denominador $(x^2-y^2)^2$ hi és estrictament positiu.


## t3-2:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Donada $f(x,y)=y+x^{(\log x)(\arctan(\sin(\cos xy)))}$, calculeu $\dfrac{\partial f}{\partial y}(1,1)$.
RESULTAT CORRECTE: $\dfrac{\partial f}{\partial y}(1,1)=1$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [restringir] Fixar la variable que no es deriva  (teoria: T3.2)
     objectiu: Escriure la funció d'una variable que cal derivar per obtenir $\dfrac{\partial f}{\partial y}(1,1)$.
     idea: Per definició, la parcial respecte de $y$ al punt $(1,1)$ és la derivada a $y=1$ de $y\mapsto f(1,y)$: fixa $x$ abans de derivar.
     detall: $f(1,y)=y+1^{(\log 1)(\arctan(\sin(\cos y)))}=y+1^{0}=y+1$, ja que $\log1=0$ (i, de fet, $1^a=1$ per a tot $a$).
  2. [derivar] Derivar la funció d'una variable  (teoria: T3.2)
     objectiu: Obtenir el valor de la parcial.
     idea: Deriva la funció d'una variable que has obtingut i avalua-la a $y=1$.
     detall: $\dfrac{d}{dy}(y+1)=1$, per tant $\dfrac{\partial f}{\partial y}(1,1)=1$.
ERRORS COMUNS:
  - [deriva_tot] Intenta derivar l'expressió completa respecte de $y$ (amb la regla de la cadena per a $x^{g(x,y)}=e^{g\log x}$) i s'embolica, en lloc de fixar $x=1$ primer.
  - [exponent_derivada] Deriva $x^{g}$ respecte de $y$ com si fos $g\,x^{g-1}$.

TEORIA DEL CURS QUE FA SERVIR:
[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.
</solucio_de_referencia>

### Document a revisar

[1] Per definició, $\dfrac{\partial f}{\partial y}(1,1)$ és la derivada en $y=1$ de la funció d'una variable $y\mapsto f(1,y)$, de manera que podem fixar $x=1$ abans de derivar.
[2] La potència $x^{(\log x)(\arctan(\sin(\cos xy)))}$ està definida per a $x>0$, i el semiplà obert $\{x>0\}$ conté tota la recta $x=1$; per tant $f(1,y)$ està definida per a tot $y$.
[3] Amb $x=1$, l'exponent és $(\log 1)\,\arctan(\sin(\cos y))=0$, perquè $\log1=0$.
[4] Per tant, $f(1,y)=y+1^{0}=y$ per a tot $y\in\mathbb{R}$.
[5] Derivant aquesta funció d'una variable, $\dfrac{d}{dy}f(1,y)=1$ per a tot $y$, i en particular $\dfrac{\partial f}{\partial y}(1,1)=1$.
[6] Com a comprovació, derivem directament: si $g(x,y)=(\log x)\arctan(\sin(\cos xy))$, aleshores $\dfrac{\partial}{\partial y}x^{g}=g\,x^{g-1}\dfrac{\partial g}{\partial y}$, que a $(1,1)$ val $0$ perquè $g(1,1)=0$; així torna a sortir $\dfrac{\partial f}{\partial y}(1,1)=1+0=1$.


## t3-3:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Trobeu totes les derivades direccionals a l'origen de
$$f(x,y)=\begin{cases}\dfrac{x^2y}{x^2+y^2} & \text{si } (x,y)\neq(0,0)\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$
RESULTAT CORRECTE: Existeixen totes: per a $u=(u_1,u_2)\neq(0,0)$, $D_uf(0,0)=\dfrac{u_1^2u_2}{u_1^2+u_2^2}$. Si $u$ és unitari, $D_uf(0,0)=u_1^2u_2$ (en particular les dues parcials valen $0$). Com que $u\mapsto D_uf(0,0)$ no és lineal, $f$ no és diferenciable a l'origen.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [definicio] Plantejar la definició  (teoria: T3.1)
     objectiu: Escriure el límit que defineix $D_uf(0,0)$ per a una direcció $u=(u_1,u_2)\neq(0,0)$ qualsevol.
     idea: Restringeix $f$ a la recta $t\mapsto tu$ i fes el quocient incremental a $t=0$; recorda quant val $f$ a l'origen.
     detall: $D_uf(0,0)=\displaystyle\lim_{t\to0}\frac{f(tu_1,tu_2)-f(0,0)}{t}=\lim_{t\to0}\frac{1}{t}\cdot\frac{t^3u_1^2u_2}{t^2(u_1^2+u_2^2)}$.
  2. [calcular] Simplificar i calcular el límit  (teoria: T3.1, T3.5)
     objectiu: Calcular el límit i decidir per a quines direccions existeix.
     idea: Simplifica les potències de $t$: queda una expressió que no depèn de $t$.
     detall: El quocient val $\dfrac{u_1^2u_2}{u_1^2+u_2^2}$ per a tot $t\neq0$, per tant el límit existeix per a tota $u$ i $D_uf(0,0)=\dfrac{u_1^2u_2}{u_1^2+u_2^2}$; per a $u$ unitari, $u_1^2u_2$. En particular $\partial_xf(0,0)=\partial_yf(0,0)=0$.
ERRORS COMUNS:
  - [nomes_parcials] Calcula només les dues derivades parcials i les combina com $\nabla f(0,0)\cdot u=0$, suposant que $f$ és diferenciable.
  - [oblida_dividir_t] Calcula $\lim_{t\to0}f(tu)$ en lloc del quocient incremental i obté $0$ per a tota direcció.
  - [simplificacio] Simplifica malament les potències de $t$ (p. ex. deixa un factor $t$ i conclou que el límit és $0$).

TEORIA DEL CURS QUE FA SERVIR:
[T3.1] Definició 1 (Tema 3) — Derivada direccional
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $a\in\mathring{\Omega}$, i $u\in\mathbb{R}^n\setminus\{0\}$. Es defineix la derivada direccional de $f$ en el punt $a$ segons la direcció i sentit del vector $u$ com
$$D_uf(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t},\tag{1}$$
si aquest límit existeix. (Nota: De fet, si definim $g(t)=f(a+tu)$, la funció $f$ restringida a la recta $\{a+tu\mid t\in\mathbb{R}\}$, aleshores $D_uf(a)=g'(0)$.)

[T3.5] Observació 5 (Tema 3) — Homogeneïtat en la direcció
És fàcil comprovar que $D_{\lambda u}f(a)=\lambda D_uf(a)$. Això fa que si es vol "comparar" els diferents valors de les derivades direccionals en un punt $a$ fixat, el vector $u$ es consideri unitari.

[T3.17] Observació 17 (Tema 3) — Direccionals sense diferenciabilitat
Fins i tot l'existència de totes les derivades direccionals en un punt no implica la diferenciabilitat en aquell punt. Un exemple clàssic és aquest:
$$f(x,y)=\begin{cases}\dfrac{x^2y}{x^2+y^2} & \text{si } (x,y)\neq(0,0)\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$
</solucio_de_referencia>

### Document a revisar

[1] Sigui $u=(u_1,u_2)\neq(0,0)$. Per definició, $D_uf(0,0)=\displaystyle\lim_{t\to0}\frac{f(tu_1,tu_2)-f(0,0)}{t}$, si aquest límit existeix.
[2] Per a $t\neq0$ el punt $(tu_1,tu_2)$ no és l'origen, i $f(tu_1,tu_2)=\dfrac{t^3u_1^2u_2}{t^2(u_1^2+u_2^2)}=\dfrac{t\,u_1^2u_2}{u_1^2+u_2^2}$.
[3] Com que $f(0,0)=0$, el quocient incremental val $\dfrac{1}{t}\cdot\dfrac{t\,u_1^2u_2}{u_1^2+u_2^2}=\dfrac{u_1^2u_2}{u_1^2+u_2^2}$ per a tot $t\neq0$, que no depèn de $t$.
[4] Per tant el límit existeix per a tota $u\neq(0,0)$ i $D_uf(0,0)=\dfrac{u_1^2u_2}{u_1^2+u_2^2}$; si $u$ és unitari, $D_uf(0,0)=u_1u_2^2$.
[5] Prenent $u=(1,0)$ i $u=(0,1)$ a la fórmula general, obtenim $\dfrac{\partial f}{\partial x}(0,0)=\dfrac{\partial f}{\partial y}(0,0)=0$, és a dir, $\nabla f(0,0)=(0,0)$.
[6] Si $f$ fos diferenciable a l'origen, tindríem $D_uf(0,0)=\nabla f(0,0)\cdot u=0$ per a tota $u$.
[7] Però per a $u=(1,1)$ la fórmula dona $D_uf(0,0)=\dfrac{1\cdot1}{1+1}=\dfrac12\neq0$, de manera que $u\mapsto D_uf(0,0)$ no és lineal.
[8] Per tant $f$ no és diferenciable a l'origen i, en particular, tampoc no hi és contínua.


## t3-4:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Trobeu totes les direccions respecte de les quals les funcions següents tenen derivades direccionals a l'origen:
$$f(x,y)=\begin{cases}\dfrac{2xy}{x^2+y^2} & \text{si } (x,y)\neq(0,0)\\ 1 & \text{si } (x,y)=(0,0)\end{cases},\qquad g(x,y)=\begin{cases}\dfrac{x^3}{x^2+y^2} & \text{si } (x,y)\neq(0,0)\\ 0 & \text{si } (x,y)=(0,0).\end{cases}$$
RESULTAT CORRECTE: $f$: només en les direccions $u=(a,a)$, $a\neq0$ (la bisectriu $y=x$, en tots dos sentits), i hi val $D_uf(0,0)=0$. En qualsevol altra direcció el límit és infinit.
$g$: en totes les direccions, amb $D_ug(0,0)=\dfrac{u_1^3}{u_1^2+u_2^2}$ (per a $u$ unitari, $u_1^3$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [plantejar_f] Quocient incremental per a f  (teoria: T3.1)
     objectiu: Escriure el quocient de la definició de $D_uf(0,0)$ per a $u=(u_1,u_2)\neq(0,0)$.
     idea: Aplica la definició de derivada direccional; fixa't en el valor de $f$ a l'origen, que no és $0$.
     detall: $\dfrac{f(tu)-f(0,0)}{t}=\dfrac{1}{t}\left(\dfrac{2u_1u_2}{u_1^2+u_2^2}-1\right)=-\dfrac{1}{t}\cdot\dfrac{(u_1-u_2)^2}{u_1^2+u_2^2}$, ja que $f(tu)$ no depèn de $t$.
  2. [direccions_f] Decidir les direccions per a f  (teoria: T3.1)
     objectiu: Determinar per a quines direccions el límit quan $t\to0$ existeix i quant val.
     idea: Un quocient de la forma $C/t$ amb $C$ constant només té límit finit en un cas.
     detall: El límit existeix si i només si $(u_1-u_2)^2=0$, és a dir $u_1=u_2$; aleshores el quocient és $0$ i $D_uf(0,0)=0$. Si $u_1\neq u_2$ el quocient tendeix a $\mp\infty$ (laterals) i no existeix. En particular, no existeixen les parcials.
  3. [direccions_g] Derivades direccionals de g  (teoria: T3.1, T3.5)
     objectiu: Calcular $D_ug(0,0)$ i decidir per a quines direccions existeix.
     idea: Mateixa definició; ara $g(0,0)=0$ i el numerador és homogeni de grau 3.
     detall: $\dfrac{g(tu)-g(0,0)}{t}=\dfrac{t^3u_1^3}{t\cdot t^2(u_1^2+u_2^2)}=\dfrac{u_1^3}{u_1^2+u_2^2}$, independent de $t$: existeix per a tota $u$, i $D_ug(0,0)=\dfrac{u_1^3}{u_1^2+u_2^2}$ ($=u_1^3$ si $\|u\|=1$).
ERRORS COMUNS:
  - [f_origen_zero] Pren $f(0,0)=0$ en lloc de $1$ i conclou que el quocient és $\frac{2u_1u_2}{t(u_1^2+u_2^2)}$, amb direccions errònies (només els eixos).
  - [limit_sense_t] Calcula $\lim f(tu)$ en lloc del quocient incremental i conclou que la derivada direccional existeix sempre.
  - [nomes_unitaris_o_sentit] Per a $f$ només dona $u=(1,1)/\sqrt2$ i oblida el sentit oposat $(-1,-1)$ o els múltiples.

TEORIA DEL CURS QUE FA SERVIR:
[T3.1] Definició 1 (Tema 3) — Derivada direccional
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $a\in\mathring{\Omega}$, i $u\in\mathbb{R}^n\setminus\{0\}$. Es defineix la derivada direccional de $f$ en el punt $a$ segons la direcció i sentit del vector $u$ com
$$D_uf(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t},\tag{1}$$
si aquest límit existeix. (Nota: De fet, si definim $g(t)=f(a+tu)$, la funció $f$ restringida a la recta $\{a+tu\mid t\in\mathbb{R}\}$, aleshores $D_uf(a)=g'(0)$.)

[T3.5] Observació 5 (Tema 3) — Homogeneïtat en la direcció
És fàcil comprovar que $D_{\lambda u}f(a)=\lambda D_uf(a)$. Això fa que si es vol "comparar" els diferents valors de les derivades direccionals en un punt $a$ fixat, el vector $u$ es consideri unitari.
</solucio_de_referencia>

### Document a revisar

[1] Comencem per $f$. Sigui $u=(u_1,u_2)\neq(0,0)$. Per a $t\neq0$, $f(tu)=\dfrac{2t^2u_1u_2}{t^2(u_1^2+u_2^2)}=\dfrac{2u_1u_2}{u_1^2+u_2^2}$, que no depèn de $t$.
[2] Com que $f(0,0)=1$, el quocient incremental és $\dfrac{f(tu)-f(0,0)}{t}=\dfrac{1}{t}\left(\dfrac{2u_1u_2}{u_1^2+u_2^2}-1\right)=\dfrac{1}{t}\cdot\dfrac{(u_1-u_2)^2}{u_1^2+u_2^2}$.
[3] Aquest quocient té límit quan $t\to0$ si i només si $(u_1-u_2)^2=0$, és a dir, $u_1=u_2$: en aquest cas és idènticament $0$ i $D_uf(0,0)=0$. Si $u_1\neq u_2$, el quocient tendeix a $+\infty$ per un costat i a $-\infty$ per l'altre, i no hi ha derivada direccional.
[4] Per tant, $f$ té derivada direccional a l'origen només en la direcció $u=\dfrac{1}{\sqrt2}(1,1)$, i hi val $0$.
[5] En particular, no existeixen les derivades parcials de $f$ a l'origen, ja que $(1,0)$ i $(0,1)$ no compleixen $u_1=u_2$.
[6] Per a $g$, si $t\neq0$, $\dfrac{g(tu)-g(0,0)}{t}=\dfrac{t^3u_1^3}{t\cdot t^2(u_1^2+u_2^2)}=\dfrac{u_1^3}{u_1^2+u_2^2}$, que no depèn de $t$.
[7] Així, el límit existeix per a tota $u\neq(0,0)$: $g$ té derivada direccional a l'origen en totes les direccions, amb $D_ug(0,0)=\dfrac{u_1^3}{u_1^2+u_2^2}$, que per a $u$ unitari és $u_1^3$.


## t3-6:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Sigui $f:\mathbb{R}^2\longrightarrow\mathbb{R}$ una funció diferenciable en $(0,0)$ tal que $f(x,y)=f(y,x)$ per tot $(x,y)\in\mathbb{R}^2$ i $Df(0,0)\neq0$. Determineu el nucli de $Df(0,0)$.
RESULTAT CORRECTE: $\ker Df(0,0)=\{(h,k)\in\mathbb{R}^2 : h+k=0\}=\langle(1,-1)\rangle$, la recta $y=-x$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [parcials_iguals] Relacionar les dues parcials  (teoria: T3.4, T3.2)
     objectiu: Esbrinar quina relació hi ha entre $\dfrac{\partial f}{\partial x}(0,0)$ i $\dfrac{\partial f}{\partial y}(0,0)$.
     idea: Usa la simetria $f(x,y)=f(y,x)$ a la definició de derivada parcial (o el resultat dels apunts sobre funcions simètriques) en el punt $(0,0)$, que és fix per l'intercanvi.
     detall: $\dfrac{\partial f}{\partial y}(0,0)=\lim_{t\to0}\dfrac{f(0,t)-f(0,0)}{t}=\lim_{t\to0}\dfrac{f(t,0)-f(0,0)}{t}=\dfrac{\partial f}{\partial x}(0,0)=:a$.
  2. [matriu] Escriure la diferencial  (teoria: T3.9, T3.10)
     objectiu: Escriure $Df(0,0)$ com a aplicació lineal explícita.
     idea: Si $f$ és diferenciable, la matriu de la diferencial és la jacobiana, formada per les parcials. Usa també la hipòtesi $Df(0,0)\neq0$.
     detall: $Jf(0,0)=(a\ \ a)$, així $Df(0,0)(h,k)=a(h+k)$, i $a\neq0$ perquè $Df(0,0)\neq0$.
  3. [nucli] Calcular el nucli
     objectiu: Determinar el conjunt de vectors on s'anul·la la diferencial.
     idea: Resol l'equació lineal $Df(0,0)(h,k)=0$; el fet que la diferencial no sigui nul·la t'ho permet simplificar.
     detall: $a(h+k)=0\iff h+k=0$ (perquè $a\neq0$). $\ker Df(0,0)=\{(h,-h): h\in\mathbb{R}\}=\langle(1,-1)\rangle$.
ERRORS COMUNS:
  - [oblida_hipotesi] No usa que $Df(0,0)\neq0$ i conclou que el nucli podria ser tot $\mathbb{R}^2$, o no justifica que $a\neq0$.
  - [simetria_mal_usada] Dedueix de la simetria que $\partial_xf=-\partial_yf$, o que les parcials són iguals a qualsevol punt $(x,y)$ (no només a la diagonal).
  - [nucli_imatge] Confon el nucli amb la imatge (respon $\mathbb{R}$) o amb la direcció del gradient.

TEORIA DEL CURS QUE FA SERVIR:
[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$

[T3.4] Exercici 4 (Tema 3) — Funció simètrica i derivades parcials
Sigui $f:\mathbb{R}^2\to\mathbb{R}$ tal que $f(x,y)=f(y,x)$, és a dir $f$ és simètrica respecte de la involució $x\leftrightarrow y$. Demostreu que
$$\frac{\partial f}{\partial y}(x_0,y_0)=\frac{\partial f}{\partial x}(y_0,x_0).$$

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

[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$
</solucio_de_referencia>

### Document a revisar

[1] Siguin $a=\dfrac{\partial f}{\partial x}(0,0)$ i $b=\dfrac{\partial f}{\partial y}(0,0)$, que existeixen perquè $f$ és diferenciable a l'origen.
[2] Per la simetria, $f(0,t)=f(t,0)$ per a tot $t$, i per tant $b=\displaystyle\lim_{t\to0}\frac{f(0,t)-f(0,0)}{t}=\lim_{t\to0}\frac{f(t,0)-f(0,0)}{t}=a$.
[3] Més en general, el mateix argument mostra que $\dfrac{\partial f}{\partial x}(x,y)=\dfrac{\partial f}{\partial y}(x,y)$ a tot punt $(x,y)$ on existeixin les parcials.
[4] Com que $f$ és diferenciable a $(0,0)$, la seva diferencial és l'aplicació lineal de matriu $Jf(0,0)=(a\ \ a)$, és a dir, $Df(0,0)(h,k)=a(h+k)$.
[5] A més, $a\neq0$: si fos $a=0$, tindríem $Df(0,0)=0$, en contra de la hipòtesi.
[6] Per tant, $Df(0,0)(h,k)=0\iff h+k=0$, i $\ker Df(0,0)=\{(h,k)\in\mathbb{R}^2: h+k=0\}$, que és la recta generada pel vector $(1,1)$.


## t3-7:normal

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
[2] A l'origen, com que $\sqrt{x^2+y^2}\le|x|$, tenim $|f(x,y)|=\dfrac{|x|\,|y|}{\sqrt{x^2+y^2}}\le|y|\to0$. Pel criteri del sandvitx, el límit a l'origen és $0=f(0,0)$, i $f$ és contínua a tot $\mathbb{R}^2$.
[3] A l'obert $\{y>0\}$ tenim $f=\dfrac{xy}{\sqrt{x^2+y^2}}$, i a l'obert $\{y<0\}$ també $f=\dfrac{xy}{\sqrt{x^2+y^2}}$. En cadascun d'aquests oberts les parcials són quocients de funcions de classe $\mathcal{C}^1$ amb denominador no nul, i per tant contínues; per la condició suficient, $f$ és diferenciable a tot punt amb $y\neq0$.
[4] En un punt $(x_0,0)$ amb $x_0\neq0$: $\dfrac{f(x_0,t)-f(x_0,0)}{t}=\dfrac{x_0|t|}{t\sqrt{x_0^2+t^2}}$, que tendeix a $\dfrac{x_0}{|x_0|}$ quan $t\to0^+$ i a $-\dfrac{x_0}{|x_0|}$ quan $t\to0^-$. Els límits laterals són diferents, no existeix $\dfrac{\partial f}{\partial y}(x_0,0)$ i, per tant, $f$ no és diferenciable en aquests punts.
[5] A l'origen, $f(t,0)=0$ i $f(0,t)=0$ per a tot $t$, així que $\nabla f(0,0)=(0,0)$ i l'única candidata a diferencial és l'aplicació lineal nul·la.
[6] Cal doncs que $\dfrac{f(x,y)}{\sqrt{x^2+y^2}}=\dfrac{x|y|}{x^2+y^2}$ tendeixi a $0$ quan $(x,y)\to(0,0)$. Però sobre la recta $y=x$, amb $x>0$, val $\dfrac{x^2}{2x^2}=\dfrac12$, de manera que $f$ no és diferenciable a l'origen.
[7] En resum, $f$ és contínua a tot $\mathbb{R}^2$ i és diferenciable exactament als punts amb $y\neq0$: no ho és en cap punt de l'eix $y=0$.


## t3-8:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Raoneu si la funció
$$f(x,y)=\begin{cases}\dfrac{(x+y)^2}{x^2+y^2} & \text{si } (x,y)\neq(0,0)\\ 1 & \text{si } (x,y)=(0,0).\end{cases}$$
és contínua, si té derivades parcials i si és diferenciable.
RESULTAT CORRECTE: Fora de l'origen $f$ és contínua, té parcials ($\partial_xf=\dfrac{2y(y^2-x^2)}{(x^2+y^2)^2}$, $\partial_yf=\dfrac{2x(x^2-y^2)}{(x^2+y^2)^2}$) i és diferenciable. A l'origen: no és contínua (val $1$ sobre $y=0$ i $2$ sobre $y=x$), però sí que té derivades parcials, $\partial_xf(0,0)=\partial_yf(0,0)=0$; no és diferenciable perquè no és contínua.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [fora_origen] Fora de l'origen  (teoria: T2.20, T3.23)
     objectiu: Estudiar continuïtat, parcials i diferenciabilitat als punts $(x,y)\neq(0,0)$.
     idea: Allà és un quocient de polinomis amb denominador no nul, en un obert: aplica els resultats d'àlgebra de funcions contínues i diferenciables.
     detall: A $\mathbb{R}^2\setminus\{(0,0)\}$, $f=1+\dfrac{2xy}{x^2+y^2}$ és contínua i diferenciable (quocient amb denominador no nul). Parcials: $\partial_xf=\dfrac{2y(y^2-x^2)}{(x^2+y^2)^2}$, $\partial_yf=\dfrac{2x(x^2-y^2)}{(x^2+y^2)^2}$.
  2. [continuitat_origen] Continuïtat a l'origen  (teoria: T2.10, T2.14)
     objectiu: Decidir si $f$ és contínua a $(0,0)$.
     idea: Estudia el límit al llarg de diferents rectes per l'origen.
     detall: Sobre $y=mx$: $f(x,mx)=\dfrac{(1+m)^2}{1+m^2}$, que depèn de $m$ (val $1$ per a $m=0$ i $2$ per a $m=1$). No existeix el límit: $f$ no és contínua a l'origen.
  3. [parcials_origen] Parcials a l'origen  (teoria: T3.2)
     objectiu: Calcular, si existeixen, les derivades parcials a l'origen.
     idea: Usa la definició, restringint $f$ als eixos; recorda el valor de $f(0,0)$.
     detall: $f(t,0)=\dfrac{t^2}{t^2}=1$, així $\dfrac{f(t,0)-f(0,0)}{t}=0$ i $\partial_xf(0,0)=0$. Igualment $f(0,t)=1$ i $\partial_yf(0,0)=0$. Existeixen totes dues.
  4. [diferenciabilitat_origen] Diferenciabilitat a l'origen  (teoria: T3.14)
     objectiu: Decidir si $f$ és diferenciable a $(0,0)$.
     idea: Relaciona la diferenciabilitat amb la continuïtat que ja has estudiat.
     detall: Diferenciable implica contínua; com que $f$ no és contínua a l'origen, no hi és diferenciable (tot i tenir les dues parcials).
ERRORS COMUNS:
  - [parcials_implica_continua] Creu que, com que existeixen les parcials a l'origen, la funció hi és contínua o diferenciable.
  - [origen_valor_zero] Usa $f(0,0)=0$ i conclou que les parcials no existeixen.
  - [no_conclou_diferenciabilitat] Intenta estudiar el límit de la definició de diferenciabilitat sense adonar-se que n'hi ha prou amb la discontinuïtat.

TEORIA DEL CURS QUE FA SERVIR:
[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$

[T2.20] Proposició 20 (Tema 2) — Àlgebra de funcions contínues
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ i $h:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, contínues. Llavors

(i) $f+g,\ \lambda f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $\lambda\in\mathbb{R}$, són contínues;

(ii) $hf:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$ és contínua;

(iii) per a $m=1$, si $g(x)\neq0\ \forall x\in\Omega$, $f/g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(iv) $\langle f,g\rangle:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua;

(v) $\|f\|:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ és contínua.

[T3.23] Proposició 23 (Tema 3) — Àlgebra de funcions diferenciables
Siguin $f,g:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciables en $a\in\mathring{\Omega}$ i sigui $\lambda\in\mathbb{R}$. Llavors,

(i) $f+g$ és diferenciable en $a$ i $D(f+g)(a)=Df(a)+Dg(a)$.

(ii) $\lambda f$ és diferenciable en $a$ i $D(\lambda f)(a)=\lambda Df(a)$.

(iii) $fg$ és diferenciable en $a$ i $J(fg)(a)=g(a)Jf(a)+f(a)Jg(a)$.

(iv) $\dfrac{f}{g}$ és diferenciable en $a$ si $g(a)\neq0$. A més
$$J\left(\frac{f}{g}\right)(a)=\frac{g(a)Jf(a)-f(a)Jg(a)}{g(a)^2}.$$

[T2.10] Proposició 10 (Tema 2) — Límit per camins
Límit per camins. Si $F:D\subseteq\mathbb{R}^2\longrightarrow\mathbb{R}^m$ i $(a,b)\in D'$ tal que $\displaystyle\exists\lim_{(x,y)\to(a,b)}F(x,y)=L$, llavors per a tota funció real i contínua $g$ definida en un entorn d'$a$, tal que $g(a)=b$, es compleix que
$$\lim_{x\to a}F(x,g(x))=L.$$

[T3.14] Proposició 14 (Tema 3) — Diferenciable implica contínua i Lipschitz
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $a\in\mathring{\Omega}$. Si $f$ és diferenciable al punt $a$, aleshores:

(i) $f$ és contínua al punt $a$.

(ii) $f$ és localment Lipschitz en $a$. (Nota: De fet, és més precís dir que és localment puntualment Lipschitz en $a$; és a dir que existeix $\delta>0$ i $M>0$ tal que $d(f8x),f(x))<M\,d(x,a)$ per a tota $x\in B(a,\delta)$. [transcripció literal de la nota; sembla un error tipogràfic de l'original])
</solucio_de_referencia>

### Document a revisar

[1] Fora de l'origen, $f=\dfrac{x^2+2xy+y^2}{x^2+y^2}=1+\dfrac{2xy}{x^2+y^2}$ és un quocient de polinomis amb denominador no nul, i per tant és contínua i diferenciable a $\mathbb{R}^2\setminus\{(0,0)\}$, amb $\dfrac{\partial f}{\partial x}=\dfrac{2y(x^2-y^2)}{(x^2+y^2)^2}$ i $\dfrac{\partial f}{\partial y}=\dfrac{2x(x^2-y^2)}{(x^2+y^2)^2}$.
[2] A l'origen, sobre la recta $y=mx$ amb $x\neq0$ tenim $f(x,mx)=\dfrac{(1+m)^2x^2}{(1+m^2)x^2}=\dfrac{(1+m)^2}{1+m^2}$, que depèn de $m$: val $1$ per a $m=0$ i $2$ per a $m=1$.
[3] Per tant no existeix $\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)$, i $f$ no és contínua a l'origen.
[4] Per a les parcials a l'origen, $f(t,0)=\dfrac{t^2}{t^2}=1$ per a $t\neq0$, així que $\dfrac{f(t,0)-f(0,0)}{t}=\dfrac{1-1}{t}=0$ i $\dfrac{\partial f}{\partial x}(0,0)=0$. Igualment $f(0,t)=1$ i $\dfrac{\partial f}{\partial y}(0,0)=0$: existeixen totes dues.
[5] Tot i així, $f$ no és diferenciable a l'origen: les parcials no hi són contínues, ja que per exemple $\dfrac{\partial f}{\partial y}(x,0)=\dfrac{2}{x}$ no té límit quan $x\to0$.
[6] En resum: fora de l'origen $f$ és contínua, té derivades parcials i és diferenciable; a l'origen no és contínua, té les dues derivades parcials (nul·les) i no és diferenciable.


## t3-9:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Estudieu la continuïtat, l'existència de derivades direccionals, i la diferenciabilitat de la funció $f(x,y)=x^{1/3}y^{1/3}$, definida a $\mathbb{R}^2$.
RESULTAT CORRECTE: $f=\sqrt[3]{xy}$ és contínua a tot $\mathbb{R}^2$. Als punts amb $xy\neq0$ és diferenciable i té totes les derivades direccionals. Als punts dels eixos: a l'origen només existeixen les derivades direccionals en les direccions dels eixos ($u_1u_2=0$), i valen $0$; a $(x_0,0)$ amb $x_0\neq0$ només existeix en les direccions horitzontals (valor $0$), i a $(0,y_0)$, $y_0\neq0$, només en les verticals (valor $0$). Per tant $f$ és diferenciable exactament a $\{xy\neq0\}$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [continuitat] Continuïtat  (teoria: T2.19, T2.20)
     objectiu: Estudiar la continuïtat de $f$ a $\mathbb{R}^2$.
     idea: Escriu $f$ com a composició i producte de funcions contínues conegudes.
     detall: $t\mapsto t^{1/3}$ (arrel cúbica real) és contínua a $\mathbb{R}$, i $f(x,y)=x^{1/3}\,y^{1/3}$ és producte de composicions de contínues: $f$ és contínua a tot $\mathbb{R}^2$.
  2. [fora_eixos] Punts fora dels eixos  (teoria: T3.18, T3.9)
     objectiu: Estudiar diferenciabilitat i derivades direccionals als punts amb $x\neq0$ i $y\neq0$.
     idea: L'arrel cúbica és derivable fora de $0$; mira la continuïtat de les parcials en un entorn.
     detall: A l'obert $\{xy\neq0\}$, $\partial_xf=\frac13x^{-2/3}y^{1/3}$ i $\partial_yf=\frac13x^{1/3}y^{-2/3}$ són contínues, per tant $f$ hi és diferenciable i té totes les derivades direccionals, $D_uf=\nabla f\cdot u$.
  3. [origen] Direccionals a l'origen  (teoria: T3.1)
     objectiu: Calcular, per a cada direcció $u=(u_1,u_2)$, la derivada direccional a l'origen si existeix.
     idea: Aplica la definició i compta la potència de $t$ que queda.
     detall: $\dfrac{f(tu)-f(0,0)}{t}=\dfrac{t^{2/3}(u_1u_2)^{1/3}}{t}=(u_1u_2)^{1/3}\,t^{-1/3}$. Si $u_1u_2\neq0$ no té límit finit; si $u_1u_2=0$ val $0$. Només existeixen les parcials, $\partial_xf(0,0)=\partial_yf(0,0)=0$.
  4. [eixos] Direccionals als altres punts dels eixos  (teoria: T3.1)
     objectiu: Estudiar les derivades direccionals als punts $(x_0,0)$ amb $x_0\neq0$ (i, per simetria, $(0,y_0)$).
     idea: Separa les direccions segons si són paral·leles a l'eix o no, i aplica la definició.
     detall: $\dfrac{f(x_0+tu_1,tu_2)}{t}=(x_0+tu_1)^{1/3}u_2^{1/3}\,t^{-2/3}$: si $u_2\neq0$ tendeix a $\pm\infty$ (el factor $(x_0+tu_1)^{1/3}\to x_0^{1/3}\neq0$), no existeix; si $u_2=0$, $f=0$ sobre l'eix i $D_uf(x_0,0)=0$. Anàlogament a $(0,y_0)$ només existeix si $u_1=0$.
  5. [diferenciabilitat_eixos] Diferenciabilitat als eixos  (teoria: T3.9)
     objectiu: Decidir si $f$ és diferenciable als punts dels eixos.
     idea: Recorda quina propietat de les derivades direccionals té tota funció diferenciable.
     detall: Si $f$ fos diferenciable en un punt, hi existirien totes les derivades direccionals. Als punts dels eixos (inclòs l'origen) n'hi ha que no existeixen: $f$ no hi és diferenciable. Conclusió: diferenciable exactament a $\{xy\neq0\}$.
ERRORS COMUNS:
  - [parcials_suficients] A l'origen troba $\partial_xf=\partial_yf=0$ i conclou que és diferenciable amb diferencial $0$.
  - [arrel_negatius] Creu que $x^{1/3}$ no està definida (o no és contínua) per a $x<0$.
  - [oblida_eixos] Només estudia l'origen i oblida els altres punts dels eixos, on una de les parcials no existeix.

TEORIA DEL CURS QUE FA SERVIR:
[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T3.1] Definició 1 (Tema 3) — Derivada direccional
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $a\in\mathring{\Omega}$, i $u\in\mathbb{R}^n\setminus\{0\}$. Es defineix la derivada direccional de $f$ en el punt $a$ segons la direcció i sentit del vector $u$ com
$$D_uf(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t},\tag{1}$$
si aquest límit existeix. (Nota: De fet, si definim $g(t)=f(a+tu)$, la funció $f$ restringida a la recta $\{a+tu\mid t\in\mathbb{R}\}$, aleshores $D_uf(a)=g'(0)$.)

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
</solucio_de_referencia>

### Document a revisar

[1] La funció $t\mapsto t^{1/3}$ (l'arrel cúbica real) és contínua a tot $\mathbb{R}$, i $f(x,y)=x^{1/3}y^{1/3}$ és producte de composicions de funcions contínues; per tant $f$ és contínua a tot $\mathbb{R}^2$.
[2] A l'obert $\{xy\neq0\}$, $\dfrac{\partial f}{\partial x}=\dfrac13x^{-2/3}y^{1/3}$ i $\dfrac{\partial f}{\partial y}=\dfrac13x^{1/3}y^{-2/3}$ són contínues; per la condició suficient, $f$ hi és diferenciable i hi té totes les derivades direccionals, $D_uf=\nabla f\cdot u$.
[3] A l'origen, per a $u=(u_1,u_2)\neq(0,0)$, $f(tu_1,tu_2)=(tu_1)^{1/3}(tu_2)^{1/3}=t^{1/3}(u_1u_2)^{1/3}$, de manera que el quocient incremental és $(u_1u_2)^{1/3}\,t^{-2/3}$.
[4] Si $u_1u_2\neq0$ aquest quocient no té límit finit quan $t\to0$; si $u_1u_2=0$ és idènticament $0$. Així, a l'origen només existeixen les derivades direccionals en les direccions dels eixos, i valen $0$; en particular $\dfrac{\partial f}{\partial x}(0,0)=\dfrac{\partial f}{\partial y}(0,0)=0$.
[5] En un punt $(x_0,0)$ amb $x_0\neq0$: $\dfrac{f(x_0+tu_1,tu_2)-f(x_0,0)}{t}=(x_0+tu_1)^{1/3}u_2^{1/3}\,t^{-2/3}$. Si $u_2\neq0$, el factor $(x_0+tu_1)^{1/3}$ tendeix a $x_0^{1/3}\neq0$ i el quocient tendeix a $\pm\infty$; si $u_2=0$, $f$ és nul·la sobre l'eix i $D_uf(x_0,0)=0$.
[6] Anàlogament, en un punt $(0,y_0)$ amb $y_0\neq0$ la derivada direccional només existeix si $u_2=0$, i aleshores val $0$.
[7] Si $f$ fos diferenciable en un punt, hi existirien totes les derivades direccionals. Als punts dels eixos (inclòs l'origen) n'hi ha que no existeixen, i per tant $f$ no hi és diferenciable.
[8] Conclusió: $f$ és contínua a tot $\mathbb{R}^2$ i és diferenciable exactament al conjunt $\{(x,y): xy\neq0\}$.


## t3-11a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Considerem la funció $f(x,y)=\log(x+y+1)+\displaystyle\int_0^x y\cos t^2\,dt$. Justifiqueu que és diferenciable en el seu domini, calculeu-ne la diferencial en el punt $(0,0)$, i useu-la per calcular un valor aproximat de $f(0.03,0.02)$.
RESULTAT CORRECTE: Domini: $\{x+y+1>0\}$, obert. Hi és $\mathcal C^1$ (parcials $\partial_xf=\dfrac{1}{x+y+1}+y\cos x^2$, $\partial_yf=\dfrac{1}{x+y+1}+\displaystyle\int_0^x\cos t^2\,dt$, contínues), per tant diferenciable. $Df(0,0)(h,k)=h+k$ (jacobiana $(1\ \ 1)$). Aproximació: $f(0.03,0.02)\approx f(0,0)+0.03+0.02=0.05$ (el valor exacte és $\approx0.0494$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [domini_parcials] Domini i derivades parcials  (teoria: T3.2)
     objectiu: Determinar el domini de $f$ i calcular-ne les derivades parcials.
     idea: El logaritme demana argument positiu. A la integral, $y$ no depèn de $t$ i surt fora; deriva-la respecte de $x$ amb el teorema fonamental del càlcul.
     detall: Domini $\{(x,y):x+y+1>0\}$, obert. $f=\log(x+y+1)+y\,G(x)$ amb $G(x)=\int_0^x\cos t^2\,dt$, $G'(x)=\cos x^2$. $\partial_xf=\dfrac{1}{x+y+1}+y\cos x^2$, $\partial_yf=\dfrac{1}{x+y+1}+G(x)$.
  2. [diferenciable] Justificar la diferenciabilitat  (teoria: T3.18, T3.20)
     objectiu: Justificar que $f$ és diferenciable a tot el seu domini.
     idea: Mira si les parcials són contínues en un obert i aplica una condició suficient.
     detall: Les dues parcials són contínues a l'obert $\{x+y+1>0\}$ ($G$ és contínua, i la resta són composicions i quocients de contínues amb denominador no nul). Per la condició suficient de diferenciabilitat, $f$ és diferenciable (de fet $\mathcal C^1$) al domini.
  3. [diferencial] Diferencial a l'origen  (teoria: T3.9, T3.10)
     objectiu: Calcular $Df(0,0)$.
     idea: La matriu de la diferencial és la jacobiana: avalua les parcials a $(0,0)$.
     detall: $\partial_xf(0,0)=1+0=1$, $\partial_yf(0,0)=1+G(0)=1$. $Jf(0,0)=(1\ \ 1)$, és a dir $Df(0,0)(h,k)=h+k$.
  4. [aproximar] Aproximació lineal  (teoria: T3.x4)
     objectiu: Obtenir un valor aproximat de $f(0.03,0.02)$.
     idea: Prop del punt, $f$ s'aproxima per la seva aproximació afí $f(a)+Df(a)(x-a)$.
     detall: $f(0,0)=\log1+0=0$. $f(0.03,0.02)\approx0+0.03+0.02=0.05$.
ERRORS COMUNS:
  - [ftc_malament] Deriva la integral respecte de $x$ incorrectament (p. ex. deixa la integral, o obté $\cos t^2$ amb $t$ lliure) o respecte de $y$ s'oblida que $y$ surt de la integral.
  - [no_justifica] Afirma que és diferenciable perquè "té parcials", sense parlar de la seva continuïtat.
  - [oblida_f_a] Aproxima $f(0.03,0.02)$ per $Df(0,0)(0.03,0.02)$ sense sumar $f(0,0)$, o hi suma un valor incorrecte.

TEORIA DEL CURS QUE FA SERVIR:
[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$

[T3.2] Definició 2 (Tema 3) — Derivada parcial
Si $u=e_i$, l'element $i$-èsim de la base canònica a $\mathbb{R}^n$, la derivada direccional $D_{e_i}f(a)$ s'anomena derivada parcial $i$-èsima de $f$ al punt $a$, i es denota per
$$\frac{\partial f}{\partial x_i}(a)=D_{e_i}f(a).$$
És a dir,
$$\frac{\partial f}{\partial x_i}(a)=\lim_{t\to0}\frac{f(a+te_i)-f(a)}{t},\tag{2}$$
sempre que el límit existeixi.

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

[T3.20] Definició 20 (Tema 3) — Funció de classe C^1
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $\Omega$ obert. Direm que $f$ és de classe $\mathcal{C}^1(\Omega)$ si $f$ és diferenciable a $\Omega$ i, per a tot punt $a\in\Omega$, existeixen totes les derivades parcials de $f$ al punt $a$ i hi són contínues. De manera anàloga a definicions anteriors, direm que $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, amb $f=(f_1,f_2,\ldots,f_m)$, és de classe $\mathcal{C}^1(\Omega)$ si $f_i\in\mathcal{C}^1(\Omega)$, per a tot $i=1,2,\ldots,m$.

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

[1] El logaritme demana $x+y+1>0$, i la integral $\displaystyle\int_0^x y\cos t^2\,dt$ està definida per a tot $(x,y)$ perquè l'integrand és continu en $t$. El domini és el semiplà $\{(x,y): x+y+1>0\}$, que és obert.
[2] Escrivim $f(x,y)=\log(x+y+1)+y\,G(x)$, amb $G(x)=\displaystyle\int_0^x\cos t^2\,dt$, ja que $y$ no depèn de la variable d'integració $t$.
[3] Pel teorema fonamental del càlcul, $G'(x)=2x\cos x^2$, i per tant $\dfrac{\partial f}{\partial x}=\dfrac{1}{x+y+1}+2xy\cos x^2$.
[4] Respecte de $y$, $G(x)$ és constant i $\dfrac{\partial f}{\partial y}=\dfrac{1}{x+y+1}+G(x)$.
[5] Les dues parcials són contínues a l'obert $\{x+y+1>0\}$ ($G$ és contínua, i la resta són composicions, productes i quocients de funcions contínues amb denominador no nul). Per la condició suficient de diferenciabilitat, $f$ és diferenciable (de fet, de classe $\mathcal{C}^1$) a tot el domini.
[6] A l'origen, $\dfrac{\partial f}{\partial x}(0,0)=1+0=1$ i $\dfrac{\partial f}{\partial y}(0,0)=1+G(0)=1$. Així $Jf(0,0)=(1\ \ 1)$, és a dir, $Df(0,0)(h,k)=h+k$.
[7] Com que $f(0,0)=\log1+0=0$, l'aproximació lineal dona $f(0.03,0.02)\approx f(0,0)+Df(0,0)(0.03,0.02)=0+0.03+0.02=0.05$.
[8] A més, com que $\log(1+s)\ge s$ per a tot $s>-1$, el valor exacte $f(0.03,0.02)=\log(1.05)+0.02\,G(0.03)$ és una mica més gran que $0.05$.


## t3-14a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Calculeu les derivades direccionals de les funcions següents en els punts i direccions que s'indiquen:

(a) $f(x,y)=\log\left(\sqrt{x^2+y^2}\right)$, $a=(1,0)$, $\mathbf{v}=(2,1)$;
RESULTAT CORRECTE: $D_{\mathbf v}f(1,0)=2$ (amb el vector $\mathbf v=(2,1)$ tal com és donat; si es normalitza, $D_{\mathbf v/\|\mathbf v\|}f(1,0)=2/\sqrt5$).
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [diferenciable] Diferenciabilitat al punt  (teoria: T3.18)
     objectiu: Decidir si es pot calcular la derivada direccional a partir del gradient.
     idea: Si $f$ és diferenciable al punt, la derivada direccional s'obté de la diferencial; comprova-ho amb la condició suficient.
     detall: $f(x,y)=\frac12\log(x^2+y^2)$ té parcials $\frac{x}{x^2+y^2}$, $\frac{y}{x^2+y^2}$, contínues a $\mathbb{R}^2\setminus\{(0,0)\}$; per tant $f$ és diferenciable a $(1,0)$.
  2. [gradient] Gradient al punt  (teoria: T3.10)
     objectiu: Calcular $\nabla f(1,0)$.
     idea: Simplifica primer el logaritme de l'arrel i deriva.
     detall: $\nabla f(x,y)=\left(\frac{x}{x^2+y^2},\frac{y}{x^2+y^2}\right)$, així que $\nabla f(1,0)=(1,0)$.
  3. [direccional] Derivada direccional  (teoria: T3.9)
     objectiu: Calcular $D_{\mathbf v}f(1,0)$.
     idea: Per a una funció diferenciable, la derivada direccional és el producte escalar del gradient amb el vector.
     detall: $D_{\mathbf v}f(1,0)=\langle(1,0),(2,1)\rangle=2$.
ERRORS COMUNS:
  - [normalitzacio] Normalitza el vector sense que calgui, o barreja el vector normalitzat amb el no normalitzat (amb la definició dels apunts, $D_{\mathbf v}f$ es calcula amb $\mathbf v$ tal com és).
  - [derivada_log] Deriva malament $\log\sqrt{x^2+y^2}$ (oblida el factor $\frac12$ o el de la cadena).
  - [sense_justificar] Usa $\nabla f\cdot\mathbf v$ sense justificar la diferenciabilitat.

TEORIA DEL CURS QUE FA SERVIR:
[T3.1] Definició 1 (Tema 3) — Derivada direccional
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $a\in\mathring{\Omega}$, i $u\in\mathbb{R}^n\setminus\{0\}$. Es defineix la derivada direccional de $f$ en el punt $a$ segons la direcció i sentit del vector $u$ com
$$D_uf(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t},\tag{1}$$
si aquest límit existeix. (Nota: De fet, si definim $g(t)=f(a+tu)$, la funció $f$ restringida a la recta $\{a+tu\mid t\in\mathbb{R}\}$, aleshores $D_uf(a)=g'(0)$.)

[T3.18] Teorema 18 (Tema 3) — Condició suficient de diferenciabilitat
(Condició suficient de diferenciabilitat). Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$, $f=(f_1,f_2,\ldots,f_m)$, $a\in\mathring{\Omega}$. Si existeixen totes les derivades parcials $\dfrac{\partial f_i}{\partial x_j}$ al punt $a$ i són contínues al punt $a$ aleshores $f$ és diferenciable al punt $a$.

[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$

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
</solucio_de_referencia>

### Document a revisar

[1] La funció està definida a $\mathbb{R}^2\setminus\{(0,0)\}$ i hi podem escriure $f(x,y)=\log\sqrt{x^2+y^2}=\dfrac12\log(x^2+y^2)$.
[2] Les seves parcials són $\dfrac{\partial f}{\partial x}=\dfrac12\cdot\dfrac{2x}{x^2+y^2}=\dfrac{x}{x^2+y^2}$ i $\dfrac{\partial f}{\partial y}=\dfrac{y}{(x^2+y^2)^2}$.
[3] Aquestes parcials són contínues a l'obert $\mathbb{R}^2\setminus\{(0,0)\}$, que conté $(1,0)$; per la condició suficient, $f$ és diferenciable a $(1,0)$ i podem calcular les derivades direccionals amb el gradient.
[4] A $(1,0)$, $\dfrac{\partial f}{\partial x}(1,0)=\dfrac{1}{1}=1$ i $\dfrac{\partial f}{\partial y}(1,0)=0$, de manera que $\nabla f(1,0)=(1,0)$.
[5] Per tant, $D_{\mathbf v}f(1,0)=\langle\nabla f(1,0),\mathbf v\rangle=\langle(1,0),(2,1)\rangle=2$.
[6] Si es vol la derivada en la direcció unitària de $\mathbf v$, com que $\|\mathbf v\|=\sqrt5$, s'obté $D_{\mathbf v/\|\mathbf v\|}f(1,0)=\dfrac{2}{5}$.


## t3-15a:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Justifiqueu l'existència d'hiperplà tangent a les gràfiques de les funcions següents en el punt $(a,f(a))$ i calculeu-lo:

(a) $f(x,y,z)=y\arcsin(x\log y)+2^{x/y}$, $a=(0,1,2)$;
RESULTAT CORRECTE: $f$ és de classe $\mathcal{C}^1$ a l'obert $\{y>0,\ |x\log y|<1\}$, que conté $a$, i per tant diferenciable a $a$. Amb $f(a)=1$ i $\nabla f(a)=(\log2,\ 0,\ 0)$, l'hiperplà tangent (a $\mathbb{R}^4$, coordenades $(x,y,z,w)$) és
$w=1+(\log2)\,x$.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [diferenciable] Justificar la diferenciabilitat  (teoria: T3.18)
     objectiu: Trobar un obert al voltant de $a$ on $f$ sigui diferenciable.
     idea: Identifica on cada peça ($\log y$, $\arcsin$, $2^{x/y}$) és derivable amb derivada contínua i aplica la condició suficient.
     detall: $\log y$ i $x/y$ són $\mathcal{C}^1$ per $y>0$; $\arcsin$ és derivable amb derivada contínua a $(-1,1)$. A l'obert $U=\{y>0,\ |x\log y|<1\}$ (a $a$: $x\log y=0$) totes les parcials existeixen i són contínues, per tant $f$ és diferenciable a $a$ i existeix l'hiperplà tangent.
  2. [valor] Valor al punt
     objectiu: Calcular $f(a)$.
     idea: Substitueix directament.
     detall: $f(0,1,2)=1\cdot\arcsin(0)+2^0=1$.
  3. [gradient] Gradient al punt  (teoria: T3.10)
     objectiu: Calcular $\nabla f(a)$.
     idea: Deriva cada sumand (regla de la cadena d'una variable) i avalua; observa de quines variables depèn realment $f$.
     detall: $\frac{\partial f}{\partial x}=\frac{y\log y}{\sqrt{1-x^2\log^2y}}+\frac{\log2}{y}2^{x/y}$, $\frac{\partial f}{\partial y}=\arcsin(x\log y)+\frac{x}{\sqrt{1-x^2\log^2y}}-\frac{x\log2}{y^2}2^{x/y}$, $\frac{\partial f}{\partial z}=0$. A $a$: $\nabla f(a)=(\log2,\ 0,\ 0)$.
  4. [hiperpla] Escriure l'hiperplà  (teoria: T3.9)
     objectiu: Escriure l'equació de l'hiperplà tangent a la gràfica a $(a,f(a))$.
     idea: Usa la fórmula de l'hiperplà tangent: valor al punt més el gradient aplicat a $x-a$.
     detall: $w=1+\log2\,(x-0)+0\,(y-1)+0\,(z-2)$, és a dir $w=1+(\log2)\,x$, a $\mathbb{R}^4$.
ERRORS COMUNS:
  - [pla_a_R3] Escriu un pla de $\mathbb{R}^3$ en lloc d'un hiperplà de $\mathbb{R}^4$ (la gràfica d'una funció de 3 variables viu a $\mathbb{R}^4$).
  - [derivada_exponencial] Deriva $2^{x/y}$ com si fos $e^{x/y}$ (oblida el factor $\log2$).
  - [domini_arcsin] No comprova que l'argument de l'arcsinus és a $(-1,1)$ prop de $a$, on $\arcsin$ és derivable.

TEORIA DEL CURS QUE FA SERVIR:
[T3.8] Definició 8 (Tema 3) — Funció diferenciable
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}^m$. Direm que $f$ és diferenciable a un punt $a\in\mathring{\Omega}$ si existeix $Df(a)\in\mathcal{L}(\mathbb{R}^n;\mathbb{R}^m)$ tal que
$$\lim_{x\to a}\frac{\|f(x)-f(a)-Df(a)(x-a)\|}{\|x-a\|}=0.\tag{3}$$

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

[T3.10] Definició 10 (Tema 3) — Matriu jacobiana i gradient
La matriu $Jf(a)$ s'anomena matriu de Jacobi o jacobiana de $f$ al punt $a$.
En el cas $m=1$, la matriu $Jf(a)\in\mathcal{M}_{1\times n}(\mathbb{R})$ s'identifica amb l'anomenat vector gradient de $f$ al punt $a$, que es denota per
$$\nabla f(a)=\left(\frac{\partial f}{\partial x_1}(a),\frac{\partial f}{\partial x_2}(a),\ldots,\frac{\partial f}{\partial x_n}(a)\right).\tag{7}$$
</solucio_de_referencia>

### Document a revisar

[1] Les funcions $\log y$ i $x/y$ són de classe $\mathcal{C}^1$ per a $y>0$, i $\arcsin$ és derivable, amb derivada contínua, a l'interval tancat $[-1,1]$. Per tant, a l'obert $U=\{(x,y,z): y>0,\ |x\log y|<1\}$, que conté $a$ (allà $x\log y=0$), totes les parcials de $f$ existeixen i són contínues, i $f$ és diferenciable a $a$: existeix l'hiperplà tangent a la gràfica.
[2] El valor al punt és $f(0,1,2)=1\cdot\arcsin(0\cdot\log1)+2^{0}=0+1=1$.
[3] Derivant respecte de $x$, $\dfrac{\partial f}{\partial x}=\dfrac{y\log y}{\sqrt{1-x^2\log^2y}}+\dfrac{\log2}{y}\,2^{x/y}$, que a $a$ val $0+\log2=\log2$.
[4] Respecte de $y$, $\dfrac{\partial f}{\partial y}=\arcsin(x\log y)+\dfrac{x}{\sqrt{1-x^2\log^2y}}-\dfrac{x\log2}{y}\,2^{x/y}$, que a $a$ val $0$ perquè $x=0$. A més, $f$ no depèn de $z$, així que $\dfrac{\partial f}{\partial z}=0$ i $\nabla f(a)=(\log2,0,0)$.
[5] La gràfica de $f$ és a $\mathbb{R}^4$; amb coordenades $(x,y,z,w)$, l'hiperplà tangent és $w=f(a)+\nabla f(a)\cdot(x-0,y-1,z-2)$.
[6] Substituint, $w=1+\log2\,(x-0)+0\,(y-1)+0\,(z-2)$, és a dir, $w=1+(\log2)\,x$.


## t3-17:normal

### Referència

<solucio_de_referencia>
ENUNCIAT: Estudieu la continuïtat, l'existència de les derivades direccionals i la diferenciabilitat de la funció $f(x,y)=e^{\sqrt{|xy|}}$, definida a $\mathbb{R}^2$.
RESULTAT CORRECTE: Continuïtat: $f$ és contínua a tot $\mathbb{R}^2$.
Derivades direccionals: als punts amb $xy\neq0$ existeixen totes ($D_uf=\langle\nabla f,u\rangle$). A $(a,0)$ amb $a\neq0$ només existeixen per a $u=(u_1,0)$ (valen $0$); a $(0,b)$ amb $b\neq0$ només per a $u=(0,u_2)$ (valen $0$); a l'origen només existeixen en les direccions dels eixos ($u_1u_2=0$), i valen $0$.
Diferenciabilitat: $f$ és diferenciable exactament a $\{(x,y):xy\neq0\}$; no ho és a cap punt dels eixos.
PASSOS DE LA SOLUCIÓ (en ordre):
  1. [continuitat] Continuïtat  (teoria: T2.19, T2.20)
     objectiu: Estudiar la continuïtat de $f$ a $\mathbb{R}^2$.
     idea: Descompon $f$ com a composició de funcions contínues conegudes.
     detall: $(x,y)\mapsto|xy|$ és contínua (producte i valor absolut), $\sqrt{\cdot}$ és contínua a $[0,\infty)$ i $\exp$ a $\mathbb{R}$; per composició, $f$ és contínua a tot $\mathbb{R}^2$.
  2. [fora_eixos] Fora dels eixos  (teoria: T3.18, T3.9)
     objectiu: Estudiar derivades direccionals i diferenciabilitat als punts amb $xy\neq0$.
     idea: En un entorn d'un punt amb $xy\neq0$ el signe de $xy$ és constant: el valor absolut i l'arrel deixen de ser problemàtics. Aplica la condició suficient.
     detall: En un entorn on $\operatorname{sgn}(xy)=s$ constant, $f=e^{\sqrt{sxy}}$ amb $sxy>0$; les parcials $\frac{\partial f}{\partial x}=e^{\sqrt{|xy|}}\frac{sy}{2\sqrt{|xy|}}$, $\frac{\partial f}{\partial y}=e^{\sqrt{|xy|}}\frac{sx}{2\sqrt{|xy|}}$ són contínues; $f$ és diferenciable i té totes les derivades direccionals, $D_uf=\langle\nabla f,u\rangle$.
  3. [eixos_no_origen] Punts dels eixos fora de l'origen  (teoria: T3.1)
     objectiu: Estudiar les derivades direccionals a $(a,0)$ amb $a\neq0$ (i, per simetria, a $(0,b)$ amb $b\neq0$).
     idea: Aplica la definició de derivada direccional i separa la direcció de l'eix de la resta; compara el creixement de $\sqrt{|t|}$ amb $t$.
     detall: $\frac{f(a+tu_1,tu_2)-1}{t}=\frac{e^{\sqrt{|a+tu_1||u_2|}\sqrt{|t|}}-1}{t}\sim\frac{\sqrt{|a||u_2|}\sqrt{|t|}}{t}$, que no té límit finit si $u_2\neq0$. Si $u_2=0$, $f\equiv1$ sobre l'eix i $D_uf(a,0)=0$. Igualment a $(0,b)$: només existeix per a $u_1=0$, i val $0$.
  4. [origen] L'origen  (teoria: T3.1)
     objectiu: Estudiar les derivades direccionals a $(0,0)$.
     idea: Aplica la definició; calcula $f(tu)$ explícitament i mira els límits laterals.
     detall: $f(tu_1,tu_2)=e^{|t|\sqrt{|u_1u_2|}}$, i $\frac{e^{c|t|}-1}{t}$ amb $c=\sqrt{|u_1u_2|}$ té límit $c$ per $t\to0^+$ i $-c$ per $t\to0^-$. Existeix només si $c=0$, és a dir $u_1u_2=0$ (direccions dels eixos), i llavors val $0$.
  5. [diferenciabilitat_eixos] No diferenciabilitat als eixos  (teoria: T3.9)
     objectiu: Decidir si $f$ és diferenciable als punts dels eixos.
     idea: Recorda què implica la diferenciabilitat sobre les derivades direccionals.
     detall: Si $f$ fos diferenciable en un punt dels eixos, hi existirien totes les derivades direccionals; com que no és així, $f$ no és diferenciable a cap punt amb $xy=0$.
ERRORS COMUNS:
  - [parcials_suficients] Als eixos troba que les parcials existeixen (o que una existeix) i conclou que és diferenciable.
  - [limits_laterals] A l'origen calcula només el límit per $t\to0^+$ i conclou que la derivada direccional val $\sqrt{|u_1u_2|}$.
  - [oblida_eixos] Estudia només l'origen i oblida la resta de punts dels eixos.
  - [discontinua] Creu que $f$ no és contínua als eixos perquè no hi és diferenciable.

TEORIA DEL CURS QUE FA SERVIR:
[T2.14] Definició 14 (Tema 2) — Funció contínua
Sigui $f:\Omega\subseteq M\to N$ i $x_0\in\Omega$. Diem que $f$ és contínua en $x_0\Leftrightarrow x_0\notin\Omega'$ o bé $\exists\lim_{x\to x_0}f(x)=f(x_0)$. Diem que $f$ és contínua (en $\Omega$) si ho és en tot punt $x_0\in\Omega$.

[T3.1] Definició 1 (Tema 3) — Derivada direccional
Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $a\in\mathring{\Omega}$, i $u\in\mathbb{R}^n\setminus\{0\}$. Es defineix la derivada direccional de $f$ en el punt $a$ segons la direcció i sentit del vector $u$ com
$$D_uf(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t},\tag{1}$$
si aquest límit existeix. (Nota: De fet, si definim $g(t)=f(a+tu)$, la funció $f$ restringida a la recta $\{a+tu\mid t\in\mathbb{R}\}$, aleshores $D_uf(a)=g'(0)$.)

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
</solucio_de_referencia>

### Document a revisar

[1] La funció $(x,y)\mapsto|xy|$ és contínua, $\sqrt{\cdot}$ és contínua a $[0,+\infty)$ i l'exponencial ho és a $\mathbb{R}$; per composició, $f$ és contínua a tot $\mathbb{R}^2$.
[2] Sigui $(x_0,y_0)$ amb $x_0y_0\neq0$. En un entorn seu el signe de $xy$ és constant, i hi tenim $|xy|=s\,xy$ amb $s=\pm1$ fix. Allà $\dfrac{\partial f}{\partial x}=e^{\sqrt{|xy|}}\,\dfrac{y}{2\sqrt{|xy|}}$ i $\dfrac{\partial f}{\partial y}=e^{\sqrt{|xy|}}\,\dfrac{x}{2\sqrt{|xy|}}$.
[3] Aquestes parcials són contínues a l'obert $\{xy\neq0\}$, de manera que $f$ hi és diferenciable i hi té totes les derivades direccionals, $D_uf=\langle\nabla f,u\rangle$.
[4] En un punt $(a,0)$ amb $a\neq0$: $\dfrac{f(a+tu_1,tu_2)-1}{t}=\dfrac{e^{\sqrt{|a+tu_1|\,|u_2|}\sqrt{|t|}}-1}{t}\sim\dfrac{\sqrt{|a|\,|u_2|}\,\sqrt{|t|}}{t}$, que no té límit finit si $u_2\neq0$. Si $u_2=0$, $f\equiv1$ sobre l'eix i $D_uf(a,0)=0$. Anàlogament, a $(0,b)$ amb $b\neq0$ només existeix si $u_1=0$, i val $0$.
[5] A l'origen, $f(tu_1,tu_2)=e^{c|t|}$ amb $c=\sqrt{|u_1u_2|}$, i $\dfrac{e^{c|t|}-1}{t}$ tendeix a $c$ quan $t\to0^+$ i a $-c$ quan $t\to0^-$. El límit existeix només si $c=0$, és a dir $u_1u_2=0$ (direccions dels eixos), i llavors val $0$.
[6] Finalment, als punts dels eixos, inclòs l'origen, alguna de les dues derivades parcials no existeix, i per tant $f$ no hi és diferenciable.
[7] En resum: $f$ és contínua a tot $\mathbb{R}^2$, té totes les derivades direccionals als punts amb $xy\neq0$ i només les de les direccions indicades als eixos, i és diferenciable exactament a $\{(x,y): xy\neq0\}$.

TITLE hhBC.mod   sodium, potassium, and leak channels
 
COMMENT
  This is a Hodgkin-Huxley euqation set for the sodium,  
  potassium, and leakage channels found in basket cell axons. 
  modified from file hh.mod by SW Jaslove  6 March, 1992
  Peter Jonas, 20.02.2017 
  K channels with two n particles to describe experimental data 
  17.03.2017 - update of Na inactivation values 
  24.12.2018 - modified phiM, phiH, and phiN to ensure compatibility with new mknrndll 
  
ENDCOMMENT
 
UNITS {
        (mA) = (milliamp)
        (mV) = (millivolt)
	    (S) = (siemens)
}
 
? interface
NEURON {
        SUFFIX hhBC
        NONSPECIFIC_CURRENT il, ina, ik
        RANGE gnabar, gkbar, gl, el, gna, gk
        GLOBAL minf, hinf, ninf1, ninf2, mtau, htau, ntau1, ntau2, expoN1, expoN2, shiftM, shiftH, shiftN
	    THREADSAFE : assigned GLOBALs will be per thread
}
 
PARAMETER {
        gnabar = .050 (S/cm2)	<0,1e9>
        gkbar = .030 (S/cm2)	<0,1e9>
        gl = .0001 (S/cm2)	<0,1e9>
		ena = 55 (mV) 
		ek = -90 (mV) 
        el = -65 (mV) 

		expoN1 = 1 ()
		expoN2 = 3 ()
		shiftM = 20.0 (mV) : RIGHT shift Na+ channel gating according to Donnan potentials 
		shiftH = 20.0 (mV) 
		shiftN = 0.0 (mV)
}
 
STATE {
        m h n1 n2
}
 
ASSIGNED {
        v (mV)
        gna (S/cm2)
	    gk (S/cm2)
        ina (mA/cm2)
        ik (mA/cm2)
        il (mA/cm2)
        minf hinf ninf1 ninf2
	    mtau (ms) htau (ms) ntau1 (ms) ntau2 (ms)
		celsius (degC)
}
 
? currents
BREAKPOINT {
        SOLVE states METHOD cnexp
        gna = gnabar*m*m*m*h
	    ina = gna*(v - ena)
        gk = gkbar*(n1^expoN1)*(n2^expoN2)
	    ik = gk*(v - ek)      
        il = gl*(v - el)
}
 
 
INITIAL {
	rates(v)
	m = minf
	h = hinf
	n1 = ninf1
	n2 = ninf2
}

? states
DERIVATIVE states {  
        rates(v)
        m' =  (minf-m)/mtau
        h' = (hinf-h)/htau
        n1' = (ninf1-n1)/ntau1
        n2' = (ninf2-n2)/ntau2
}
 
LOCAL phiM, phiH, phiN

? rates
PROCEDURE rates(v(mV)) {  :Computes rate and other constants at current v.
                      :Call once from HOC to initialize inf at resting v.
        LOCAL  alpha, beta, sum
        TABLE minf, mtau, hinf, htau, ninf1, ntau1, ninf2, ntau2 FROM -100 TO 100 WITH 200

UNITSOFF
        phiM = 2.2^((celsius - 23.5)/10) 
	    phiH =  2.9^((celsius - 23.5)/10)
		phiN = 3.0^((celsius - 23.5)/10)
		
		:"m" sodium activation system
        alpha = .2567 * vtrap(-(v+60.84-shiftM),9.722)
        :beta =  4 * exp(-(v+65)/18)
		beta = .1133 * vtrap((v+30.253-shiftM),2.848)
        sum = alpha + beta
		mtau = 1/(phiM*sum)
        minf = alpha/sum
		
		:"h" sodium inactivation system
        alpha = 0.00105 * exp(-(v-shiftH)/20.000)
        beta = 4.827 / (exp(-(v+18.646-shiftH)/12.452) + 1)
        sum = alpha + beta
	    htau = 1/(phiH*sum)
        hinf = alpha/sum

		 :"n1" potassium activation system
        alpha = .0993*vtrap(-(v-33.720-shiftN),12.742) 
        beta = .1379*exp(-(v-shiftN)/500)
	    sum = alpha + beta
        ntau1 = 1/(phiN*sum)
        ninf1 = alpha/sum
        :"n2" potassium activation system
        alpha = .0610*vtrap(-(v-29.991-shiftN),27.502) 
        beta = .001504*exp(-(v-shiftN)/17.177)
	    sum = alpha + beta
        ntau2 = 1/(phiN*sum)
        ninf2 = alpha/sum
}
 
FUNCTION vtrap(x,y) {  :Traps for 0 in denominator of rate eqns.
        if (fabs(x/y) < 1e-6) {
                vtrap = y*(1 - x/y/2)
        }else{
                vtrap = x/(exp(x/y) - 1)
        }
}
 
UNITSON

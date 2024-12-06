:-------------------------------------------------------------------
FUNCTION fun1(v(mV),V0(mV),A(/ms),B(mV))(/ms) {

	 fun1 = A*exp((v-V0)/B)
}

FUNCTION fun2(v(mV),V0(mV),A(/ms),B(mV))(/ms) {

	 fun2 = A/(exp((v-V0)/B)+1)
}

FUNCTION fun3(v(mV),V0(mV),A(/ms),B(mV))(/ms) {

    if(fabs((v-V0)/B)<1e-6) {
    :if(v==V0) {
        fun3 = A*B/1(mV) * (1- 0.5 * (v-V0)/B)
    } else {
        fun3 = A/1(mV)*(v-V0)/(exp((v-V0)/B)-1)
    }
}

FUNCTION min(x,y) { if (x<=y){ min = x }else{ min = y } }
FUNCTION max(x,y) { if (x>=y){ max = x }else{ max = y } }



: $Id: nafbwb.mod,v 1.4 2010/12/13 21:35:08 samn Exp $ 
COMMENT

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//
// NOTICE OF COPYRIGHT AND OWNERSHIP OF SOFTWARE
//
// Copyright 2007, The University Of Pennsylvania
// 	School of Engineering & Applied Science.
//   All rights reserved.
//   For research use only; commercial use prohibited.
//   Distribution without permission of Maciej T. Lazarewicz not permitted.
//   mlazarew@seas.upenn.edu
//
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

ENDCOMMENT

UNITS {
  (mA) = (milliamp)
  (mV) = (millivolt)
  (mS) = (millisiemens)
}

NEURON {
  SUFFIX Nafbwb
  USEION na WRITE ina
  RANGE phih
  RANGE gna, ena, taoh : testing
}
	
PARAMETER {
  gna  = 35 (mS/cm2)
  ena  = 55 (mV)
  phih = 5
}
    
ASSIGNED {
  v       (mV)
  ina     (mA/cm2)
  minf    (1)
  hinf    (1)
  taoh    (ms)
  celsius (degC)
}

STATE { h }

PROCEDURE iassign () { ina = (1e-3) * gna * minf^3 * h * (v-ena) }

INITIAL {
  rates(v)
  h = hinf
  iassign()
}

BREAKPOINT {
  SOLVE states METHOD cnexp	
  iassign()
}

DERIVATIVE states { 
  rates(v)
  h' = (hinf-h)/taoh
}

PROCEDURE rates(v(mV)) { LOCAL am, bm, ah, bh, q10
    
  q10  = phih:^((celsius-27.0(degC))/10.0(degC))	
    
  am   = fun3(v,  -35, -0.1,    -10)
  bm   = fun1(v,  -60,  4,      -18) 
  minf = am/(am+bm)
 
  ah   = fun1(v,  -58,    0.07,  -20)
  bh   = fun2(v,  -28,    1,     -10)
  hinf = ah/(ah+bh)
  taoh = 1./((ah+bh)*q10)
}


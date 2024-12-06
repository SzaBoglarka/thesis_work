
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


: $Id: kdrbwb.mod,v 1.4 2010/12/13 21:35:26 samn Exp $ 
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
  SUFFIX Kdrbwb
  USEION k WRITE ik
  RANGE phin,gkdr,ek
  RANGE taon,ninf
}
	
PARAMETER {
  gkdr =   9 (mS/cm2)
  ek   = -90 (mV)
  phin = 5
}
    
ASSIGNED {
  v       (mV)
  ik      (mA/cm2)
  celsius (degC)
  ninf    (1)
  taon    (ms)
}

STATE { n }

PROCEDURE iassign () { ik = (1e-3) * gkdr * n^4 * (v-ek) }

INITIAL { 
  rates(v)
  n  = ninf
  iassign()
}

BREAKPOINT {
  SOLVE states METHOD cnexp	
  iassign()
}

DERIVATIVE states { 
  rates(v)
  n' = (ninf-n)/taon
}

PROCEDURE rates(v(mV)) { LOCAL an, bn, q10
  q10  = phin:^((celsius-27.0(degC))/10.0(degC))
    
  an = fun3(v,  -34,  -0.01,   -10)
  bn = fun1(v,  -44,   0.125,  -80)
    
  ninf = an/(an+bn)
  taon = 1./((an+bn)*q10)
}



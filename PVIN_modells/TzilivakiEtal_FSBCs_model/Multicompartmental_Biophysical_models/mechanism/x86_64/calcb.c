/* Created by Language version: 7.7.0 */
/* NOT VECTORIZED */
#define NRN_VECTORIZED 0
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__calcb
#define _nrn_initial _nrn_initial__calcb
#define nrn_cur _nrn_cur__calcb
#define _nrn_current _nrn_current__calcb
#define nrn_jacob _nrn_jacob__calcb
#define nrn_state _nrn_state__calcb
#define _net_receive _net_receive__calcb 
#define rates rates__calcb 
#define states states__calcb 
 
#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 static double *_p; static Datum *_ppvar;
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define gcalbar _p[0]
#define ica _p[1]
#define po _p[2]
#define m _p[3]
#define s _p[4]
#define cai _p[5]
#define eca _p[6]
#define Dm _p[7]
#define Ds _p[8]
#define _g _p[9]
#define _ion_cai	*_ppvar[0]._pval
#define _ion_eca	*_ppvar[1]._pval
#define _ion_ica	*_ppvar[2]._pval
#define _ion_dicadv	*_ppvar[3]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_alp(void);
 static void _hoc_h2(void);
 static void _hoc_rates(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _p = _prop->param; _ppvar = _prop->dparam;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_calcb", _hoc_setdata,
 "alp_calcb", _hoc_alp,
 "h2_calcb", _hoc_h2,
 "rates_calcb", _hoc_rates,
 0, 0
};
#define alp alp_calcb
#define h2 h2_calcb
 extern double alp( double );
 extern double h2( double );
 /* declare global and static user variables */
#define bo bo_calcb
 double bo = 8;
#define ba ba_calcb
 double ba = 0.01;
#define b b_calcb
 double b = 0.01;
#define inf inf_calcb
 double inf = 0;
#define ki ki_calcb
 double ki = 0.025;
#define s_inf s_inf_calcb
 double s_inf = 0;
#define t0 t0_calcb
 double t0 = 1.5;
#define taumin taumin_calcb
 double taumin = 180;
#define tau_m tau_m_calcb
 double tau_m = 0;
#define vhalf vhalf_calcb
 double vhalf = -1;
#define zeta zeta_calcb
 double zeta = -4.6;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "ki_calcb", "mM",
 "taumin_calcb", "ms",
 "vhalf_calcb", "mV",
 "t0_calcb", "ms",
 "b_calcb", "mM",
 "ba_calcb", "mM",
 "tau_m_calcb", "ms",
 "gcalbar_calcb", "mho/cm2",
 "ica_calcb", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double m0 = 0;
 static double s0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "ki_calcb", &ki_calcb,
 "taumin_calcb", &taumin_calcb,
 "vhalf_calcb", &vhalf_calcb,
 "zeta_calcb", &zeta_calcb,
 "t0_calcb", &t0_calcb,
 "b_calcb", &b_calcb,
 "ba_calcb", &ba_calcb,
 "bo_calcb", &bo_calcb,
 "inf_calcb", &inf_calcb,
 "s_inf_calcb", &s_inf_calcb,
 "tau_m_calcb", &tau_m_calcb,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(_NrnThread*, _Memb_list*, int);
static void _ode_matsol(_NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[4]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"calcb",
 "gcalbar_calcb",
 0,
 "ica_calcb",
 "po_calcb",
 0,
 "m_calcb",
 "s_calcb",
 0,
 0};
 static Symbol* _ca_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 10, _prop);
 	/*initialize range parameters*/
 	gcalbar = 0;
 	_prop->param = _p;
 	_prop->param_size = 10;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 5, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_ca_sym);
 nrn_promote(prop_ion, 1, 1);
 	_ppvar[0]._pval = &prop_ion->param[1]; /* cai */
 	_ppvar[1]._pval = &prop_ion->param[0]; /* eca */
 	_ppvar[2]._pval = &prop_ion->param[3]; /* ica */
 	_ppvar[3]._pval = &prop_ion->param[4]; /* _ion_dicadv */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _calcb_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("ca", -10000.);
 	_ca_sym = hoc_lookup("ca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 10, 5);
  hoc_register_dparam_semantics(_mechtype, 0, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 calcb /home/szabobogi/BC_modells/TzilivakiEtal_FSBCs_model/Multicompartmental_Biophysical_models/mechanism/calcb.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 96485.3;
 static double R = 8.3145;
static int _reset;
static char *modelname = "L-type calcium channel with high threshold for activation";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rates(double, double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[2], _dlist1[2];
 static int states(_threadargsproto_);
 
double h2 (  double _lcai ) {
   double _lh2;
 _lh2 = ki / ( ki + _lcai ) ;
   
return _lh2;
 }
 
static void _hoc_h2(void) {
  double _r;
   _r =  h2 (  *getarg(1) );
 hoc_retpushx(_r);
}
 
/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   rates ( _threadargscomma_ v , cai ) ;
   Dm = ( inf - m ) / t0 ;
   Ds = ( s_inf - s ) / tau_m ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 rates ( _threadargscomma_ v , cai ) ;
 Dm = Dm  / (1. - dt*( ( ( ( - 1.0 ) ) ) / t0 )) ;
 Ds = Ds  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_m )) ;
  return 0;
}
 /*END CVODE*/
 static int states () {_reset=0;
 {
   rates ( _threadargscomma_ v , cai ) ;
    m = m + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / t0)))*(- ( ( ( inf ) ) / t0 ) / ( ( ( ( - 1.0 ) ) ) / t0 ) - m) ;
    s = s + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_m)))*(- ( ( ( s_inf ) ) / tau_m ) / ( ( ( ( - 1.0 ) ) ) / tau_m ) - s) ;
   }
  return 0;
}
 
double alp (  double _lv ) {
   double _lalp;
  _lalp = exp ( 1.e-3 * zeta * ( _lv - vhalf ) * 9.648e4 / ( 8.315 * ( 273.16 + celsius ) ) ) ;
    
return _lalp;
 }
 
static void _hoc_alp(void) {
  double _r;
   _r =  alp (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static int  rates (  double _lv , double _lcai ) {
   double _la , _lalpha2 ;
 _la = alp ( _threadargscomma_ _lv ) ;
   inf = 1.0 / ( 1.0 + _la ) ;
   _lalpha2 = pow( ( _lcai / b ) , 2.0 ) ;
   s_inf = _lalpha2 / ( _lalpha2 + 1.0 ) ;
   tau_m = taumin + 1.0 * 1.0 / ( _lcai + ba ) ;
    return 0; }
 
static void _hoc_rates(void) {
  double _r;
   _r = 1.;
 rates (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 2;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  cai = _ion_cai;
  eca = _ion_eca;
     _ode_spec1 ();
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 2; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 ();
 }
 
static void _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  cai = _ion_cai;
  eca = _ion_eca;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_ca_sym, _ppvar, 0, 1);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 1, 0);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 2, 3);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 3, 4);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  m = m0;
  s = s0;
 {
   rates ( _threadargscomma_ v , cai ) ;
   m = inf ;
   s = s_inf ;
   }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
  cai = _ion_cai;
  eca = _ion_eca;
 initmodel();
 }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   po = m * m * h2 ( _threadargscomma_ cai ) ;
   ica = gcalbar * ( po + s * s * bo ) * ( v - eca ) ;
   }
 _current += ica;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
  cai = _ion_cai;
  eca = _ion_eca;
 _g = _nrn_current(_v + .001);
 	{ double _dica;
  _dica = ica;
 _rhs = _nrn_current(_v);
  _ion_dicadv += (_dica - ica)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ica += ica ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
  cai = _ion_cai;
  eca = _ion_eca;
 { error =  states();
 if(error){fprintf(stderr,"at line 67 in file calcb.mod:\n	SOLVE states METHOD cnexp\n"); nrn_complain(_p); abort_run(error);}
 } }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(m) - _p;  _dlist1[0] = &(Dm) - _p;
 _slist1[1] = &(s) - _p;  _dlist1[1] = &(Ds) - _p;
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "/home/szabobogi/BC_modells/TzilivakiEtal_FSBCs_model/Multicompartmental_Biophysical_models/mechanism/calcb.mod";
static const char* nmodl_file_text = 
  "TITLE L-type calcium channel with high threshold for activation\n"
  ": used in somatic and dendritic regions \n"
  ": \n"
  ": After Borg \n"
  ":  Updated by Maria Markaki  12/02/03\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX calcb\n"
  "	USEION ca READ cai, eca WRITE ica\n"
  "        RANGE gcalbar, ica, po\n"
  "	GLOBAL inf, s_inf, tau_m\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mA) = (milliamp)\n"
  "	(mV) = (millivolt)\n"
  "	(molar) = (1/liter)\n"
  "	(mM) =	(millimolar)\n"
  "	FARADAY = (faraday) (coulomb)\n"
  "	R = (k-mole) (joule/degC)\n"
  "}\n"
  "\n"
  "\n"
  "PARAMETER {     \n"
  "  	ki     = 0.025  (mM)            : middle point of inactivation fct\n"
  "	gcalbar = 0   (mho/cm2)  : initialized conductance\n"
  " 	taumin  = 180    (ms)            : minimal value of the time cst\n"
  "        vhalf = -1 (mV)       :half potential for activation \n"
  "	zeta=-4.6\n"
  "	t0=1.5(ms)\n"
  "	b = 0.01 	(mM) \n"
  "        ba = 0.01	(mM)\n"
  "	bo = 8\n"
  "}\n"
  "\n"
  "\n"
  "ASSIGNED {      : parameters needed to solve DE\n"
  "        v               (mV)\n"
  " 	celsius         (degC)\n"
  "	cai             (mM)      : initial internal Ca++ concentration\n"
  "	ica             (mA/cm2)\n"
  "	eca             (mV)\n"
  ":	ical             (mA/cm2)\n"
  "	po\n"
  "        inf\n"
  "	s_inf\n"
  "	tau_m           (ms)\n"
  "}\n"
  "\n"
  "STATE {	\n"
  "	m \n"
  "	s \n"
  "} \n"
  "\n"
  "\n"
  "INITIAL {\n"
  "	rates(v,cai)\n"
  "	m = inf    : initial activation parameter value\n"
  "	s = s_inf\n"
  "}\n"
  "\n"
  "FUNCTION h2(cai(mM)) {\n"
  "	h2 = ki/(ki+cai)\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE states METHOD cnexp\n"
  "	po = m*m*h2(cai)\n"
  "	ica = gcalbar*(po+s*s*bo)*(v-eca)\n"
  "}\n"
  "\n"
  "\n"
  "DERIVATIVE states {\n"
  "	rates(v,cai)\n"
  "	m' = (inf-m)/t0\n"
  "	s' = (s_inf-s)/tau_m\n"
  "}\n"
  "\n"
  "\n"
  "\n"
  "FUNCTION alp(v(mV)) {       \n"
  "UNITSOFF\n"
  "  alp = exp(1.e-3*zeta*(v-vhalf)*9.648e4/(8.315*(273.16+celsius))) \n"
  "UNITSON\n"
  "}\n"
  "\n"
  "PROCEDURE rates(v(mV), cai(mM)) {LOCAL a, alpha2\n"
  "		a = alp(v)\n"
  "		inf = 1/(1+a)\n"
  "		alpha2 = (cai/b)^2\n"
  "		s_inf = alpha2 / (alpha2 + 1)\n"
  "		tau_m = taumin+ 1(ms)*1(mM)/(cai+ba)\n"
  "}\n"
  "\n"
  ;
#endif

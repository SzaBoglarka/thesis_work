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
 
#define nrn_init _nrn_init__HH
#define _nrn_initial _nrn_initial__HH
#define nrn_cur _nrn_cur__HH
#define _nrn_current _nrn_current__HH
#define nrn_jacob _nrn_jacob__HH
#define nrn_state _nrn_state__HH
#define _net_receive _net_receive__HH 
#define _f_rates _f_rates__HH 
#define rates rates__HH 
#define states states__HH 
 
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
#define gnabar _p[0]
#define gkbar _p[1]
#define m _p[2]
#define h _p[3]
#define n _p[4]
#define ena _p[5]
#define ek _p[6]
#define Dm _p[7]
#define Dh _p[8]
#define Dn _p[9]
#define ina _p[10]
#define ik _p[11]
#define _g _p[12]
#define _ion_ena	*_ppvar[0]._pval
#define _ion_ina	*_ppvar[1]._pval
#define _ion_dinadv	*_ppvar[2]._pval
#define _ion_ek	*_ppvar[3]._pval
#define _ion_ik	*_ppvar[4]._pval
#define _ion_dikdv	*_ppvar[5]._pval
 
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
 static void _hoc_rates(void);
 static void _hoc_states(void);
 static void _hoc_vtrap(void);
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
 "setdata_HH", _hoc_setdata,
 "rates_HH", _hoc_rates,
 "states_HH", _hoc_states,
 "vtrap_HH", _hoc_vtrap,
 0, 0
};
#define vtrap vtrap_HH
 extern double vtrap( double , double );
 /* declare global and static user variables */
#define hexp hexp_HH
 double hexp = 0;
#define hinf hinf_HH
 double hinf = 0;
#define mexp mexp_HH
 double mexp = 0;
#define minf minf_HH
 double minf = 0;
#define nexp nexp_HH
 double nexp = 0;
#define ninf ninf_HH
 double ninf = 0;
#define usetable usetable_HH
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "usetable_HH", 0, 1,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "gnabar_HH", "mho/cm2",
 "gkbar_HH", "mho/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double h0 = 0;
 static double m0 = 0;
 static double n0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "minf_HH", &minf_HH,
 "hinf_HH", &hinf_HH,
 "ninf_HH", &ninf_HH,
 "mexp_HH", &mexp_HH,
 "hexp_HH", &hexp_HH,
 "nexp_HH", &nexp_HH,
 "usetable_HH", &usetable_HH,
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
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"HH",
 "gnabar_HH",
 "gkbar_HH",
 0,
 0,
 "m_HH",
 "h_HH",
 "n_HH",
 0,
 0};
 static Symbol* _na_sym;
 static Symbol* _k_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 13, _prop);
 	/*initialize range parameters*/
 	gnabar = 0.184;
 	gkbar = 0.14;
 	_prop->param = _p;
 	_prop->param_size = 13;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 6, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_na_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ena */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ina */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dinadv */
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[3]._pval = &prop_ion->param[0]; /* ek */
 	_ppvar[4]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[5]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 
}
 static void _initlists();
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _hh_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("na", -10000.);
 	ion_reg("k", -10000.);
 	_na_sym = hoc_lookup("na_ion");
 	_k_sym = hoc_lookup("k_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 13, 6);
  hoc_register_dparam_semantics(_mechtype, 0, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "k_ion");
 	hoc_register_cvode(_mechtype, _ode_count, 0, 0, 0);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 HH /home/szabobogi/BC_modells/CA1_Saraga_2006/hh.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double *_t_minf;
 static double *_t_mexp;
 static double *_t_hinf;
 static double *_t_hexp;
 static double *_t_ninf;
 static double *_t_nexp;
static int _reset;
static char *modelname = "Sodium, Potassium and leak channels for basket cell model";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int _f_rates(double);
static int rates(double);
static int states();
 static void _n_rates(double);
 
static int  states (  ) {
   rates ( _threadargscomma_ v ) ;
   m = m + mexp * ( minf - m ) ;
   h = h + hexp * ( hinf - h ) ;
   n = n + nexp * ( ninf - n ) ;
    return 0; }
 
static void _hoc_states(void) {
  double _r;
   _r = 1.;
 states (  );
 hoc_retpushx(_r);
}
 static double _mfac_rates, _tmin_rates;
 static void _check_rates();
 static void _check_rates() {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_dt;
  static double _sav_celsius;
  if (!usetable) {return;}
  if (_sav_dt != dt) { _maktable = 1;}
  if (_sav_celsius != celsius) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_rates =  - 100.0 ;
   _tmax =  100.0 ;
   _dx = (_tmax - _tmin_rates)/200.; _mfac_rates = 1./_dx;
   for (_i=0, _x=_tmin_rates; _i < 201; _x += _dx, _i++) {
    _f_rates(_x);
    _t_minf[_i] = minf;
    _t_mexp[_i] = mexp;
    _t_hinf[_i] = hinf;
    _t_hexp[_i] = hexp;
    _t_ninf[_i] = ninf;
    _t_nexp[_i] = nexp;
   }
   _sav_dt = dt;
   _sav_celsius = celsius;
  }
 }

 static int rates(double _lv){ _check_rates();
 _n_rates(_lv);
 return 0;
 }

 static void _n_rates(double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 _f_rates(_lv); return; 
}
 _xi = _mfac_rates * (_lv - _tmin_rates);
 if (isnan(_xi)) {
  minf = _xi;
  mexp = _xi;
  hinf = _xi;
  hexp = _xi;
  ninf = _xi;
  nexp = _xi;
  return;
 }
 if (_xi <= 0.) {
 minf = _t_minf[0];
 mexp = _t_mexp[0];
 hinf = _t_hinf[0];
 hexp = _t_hexp[0];
 ninf = _t_ninf[0];
 nexp = _t_nexp[0];
 return; }
 if (_xi >= 200.) {
 minf = _t_minf[200];
 mexp = _t_mexp[200];
 hinf = _t_hinf[200];
 hexp = _t_hexp[200];
 ninf = _t_ninf[200];
 nexp = _t_nexp[200];
 return; }
 _i = (int) _xi;
 _theta = _xi - (double)_i;
 minf = _t_minf[_i] + _theta*(_t_minf[_i+1] - _t_minf[_i]);
 mexp = _t_mexp[_i] + _theta*(_t_mexp[_i+1] - _t_mexp[_i]);
 hinf = _t_hinf[_i] + _theta*(_t_hinf[_i+1] - _t_hinf[_i]);
 hexp = _t_hexp[_i] + _theta*(_t_hexp[_i+1] - _t_hexp[_i]);
 ninf = _t_ninf[_i] + _theta*(_t_ninf[_i+1] - _t_ninf[_i]);
 nexp = _t_nexp[_i] + _theta*(_t_nexp[_i+1] - _t_nexp[_i]);
 }

 
static int  _f_rates (  double _lv ) {
   double _lq10 , _ltinc , _lalpha , _lbeta , _lsum ;
 _lq10 = pow( 3.0 , ( ( celsius - 6.3 ) / 10.0 ) ) ;
   _ltinc = - dt * _lq10 ;
   _lalpha = .1 * vtrap ( _threadargscomma_ - ( _lv + 35.0 ) , 10.0 ) ;
   _lbeta = 4.0 * exp ( - ( _lv + 60.0 ) / 18.0 ) ;
   _lsum = _lalpha + _lbeta ;
   minf = _lalpha / _lsum ;
   mexp = 1.0 - exp ( _ltinc * _lsum ) ;
   _lalpha = .07 * exp ( - ( _lv + 58.0 ) / 20.0 ) ;
   _lbeta = 1.0 / ( exp ( - ( _lv + 28.0 ) / 10.0 ) + 1.0 ) ;
   _lsum = _lalpha + _lbeta ;
   hinf = _lalpha / _lsum ;
   hexp = 1.0 - exp ( _ltinc * _lsum ) ;
   _lalpha = .01 * vtrap ( _threadargscomma_ - ( _lv + 34.0 ) , 10.0 ) ;
   _lbeta = .125 * exp ( - ( _lv + 44.0 ) / 80.0 ) ;
   _lsum = _lalpha + _lbeta ;
   ninf = _lalpha / _lsum ;
   nexp = 1.0 - exp ( _ltinc * _lsum ) ;
    return 0; }
 
static void _hoc_rates(void) {
  double _r;
    _r = 1.;
 rates (  *getarg(1) );
 hoc_retpushx(_r);
}
 
double vtrap (  double _lx , double _ly ) {
   double _lvtrap;
 if ( fabs ( _lx / _ly ) < 1e-6 ) {
     _lvtrap = _ly * ( 1.0 - _lx / _ly / 2.0 ) ;
     }
   else {
     _lvtrap = _lx / ( exp ( _lx / _ly ) - 1.0 ) ;
     }
   
return _lvtrap;
 }
 
static void _hoc_vtrap(void) {
  double _r;
   _r =  vtrap (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ hoc_execerror("HH", "cannot be used with CVODE"); return 0;}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_na_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_na_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_na_sym, _ppvar, 2, 4);
   nrn_update_ion_pointer(_k_sym, _ppvar, 3, 0);
   nrn_update_ion_pointer(_k_sym, _ppvar, 4, 3);
   nrn_update_ion_pointer(_k_sym, _ppvar, 5, 4);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  h = h0;
  m = m0;
  n = n0;
 {
   rates ( _threadargscomma_ v ) ;
   m = minf ;
   h = hinf ;
   n = ninf ;
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
  ena = _ion_ena;
  ek = _ion_ek;
 initmodel();
  }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   ina = gnabar * m * m * m * h * ( v - ena ) ;
   ik = gkbar * n * n * n * n * ( v - ek ) ;
   }
 _current += ina;
 _current += ik;

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
  ena = _ion_ena;
  ek = _ion_ek;
 _g = _nrn_current(_v + .001);
 	{ double _dik;
 double _dina;
  _dina = ina;
  _dik = ik;
 _rhs = _nrn_current(_v);
  _ion_dinadv += (_dina - ina)/.001 ;
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ina += ina ;
  _ion_ik += ik ;
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
  ena = _ion_ena;
  ek = _ion_ek;
 { error =  states();
 if(error){fprintf(stderr,"at line 44 in file hh.mod:\n        SOLVE states\n"); nrn_complain(_p); abort_run(error);}
 }  }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
   _t_minf = makevector(201*sizeof(double));
   _t_mexp = makevector(201*sizeof(double));
   _t_hinf = makevector(201*sizeof(double));
   _t_hexp = makevector(201*sizeof(double));
   _t_ninf = makevector(201*sizeof(double));
   _t_nexp = makevector(201*sizeof(double));
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "/home/szabobogi/BC_modells/CA1_Saraga_2006/hh.mod";
static const char* nmodl_file_text = 
  "TITLE Sodium, Potassium and leak channels for basket cell model\n"
  " \n"
  "COMMENT\n"
  "The parameters for these channels are taken from Wang and Buzsaki's \"Gamma \n"
  "Oscillation by Synaptic Inhibition in a Hippocampal Interneuronal Network \n"
  "Model\", J. Neurosci. 16:6402-6413, 1996.  Passive properties may have to \n"
  "be adjusted.  Dendrities will be kept passive for now.\n"
  "ENDCOMMENT\n"
  " \n"
  "UNITS {\n"
  "        (mA) = (milliamp)\n"
  "        (mV) = (millivolt)\n"
  "}\n"
  " \n"
  "NEURON {\n"
  "        SUFFIX HH\n"
  "        USEION na READ ena WRITE ina\n"
  "        USEION k READ ek WRITE ik\n"
  "        RANGE gnabar, gkbar\n"
  "        GLOBAL minf, hinf, ninf, mexp, hexp, nexp\n"
  "}\n"
  " \n"
  "PARAMETER {\n"
  "        v (mV)\n"
  "        celsius = 5 (degC)\n"
  "        dt (ms)\n"
  "        gnabar = .184 (mho/cm2)\n"
  "        ena = 55 (mV)\n"
  "        gkbar = .14 (mho/cm2)\n"
  "        ek = -90 (mV)\n"
  "}\n"
  " \n"
  "STATE {\n"
  "        m h n\n"
  "}\n"
  " \n"
  "ASSIGNED {\n"
  "        ina (mA/cm2)\n"
  "        ik (mA/cm2)\n"
  "        minf hinf ninf mexp hexp nexp\n"
  "}\n"
  " \n"
  "BREAKPOINT {\n"
  "        SOLVE states\n"
  "        ina = gnabar*m*m*m*h*(v - ena)\n"
  "        ik = gkbar*n*n*n*n*(v - ek)      \n"
  "}\n"
  " \n"
  "UNITSOFF\n"
  " \n"
  "INITIAL {\n"
  "	rates(v)\n"
  "	m = minf\n"
  "	h = hinf\n"
  "	n = ninf\n"
  "}\n"
  "\n"
  "PROCEDURE states() {  :Computes state variables m, h, and n \n"
  "        rates(v)      :             at the current v and dt.\n"
  "        m = m + mexp*(minf-m)\n"
  "        h = h + hexp*(hinf-h)\n"
  "        n = n + nexp*(ninf-n)\n"
  "}\n"
  " \n"
  "PROCEDURE rates(v) {  :Computes rate and other constants at current v.\n"
  "                      :Call once from HOC to initialize inf at resting v.\n"
  "        LOCAL  q10, tinc, alpha, beta, sum\n"
  "        TABLE minf, mexp, hinf, hexp, ninf, nexp DEPEND dt, celsius FROM -100 TO 100 WITH 200\n"
  "        q10 = 3^((celsius - 6.3)/10)\n"
  "        tinc = -dt * q10\n"
  "                :\"m\" sodium activation system\n"
  "        alpha = .1 * vtrap(-(v+35),10)\n"
  "        beta =  4 * exp(-(v+60)/18)\n"
  "        sum = alpha + beta\n"
  "        minf = alpha/sum\n"
  "        mexp = 1 - exp(tinc*sum)\n"
  "                :\"h\" sodium inactivation system\n"
  "        alpha = .07 * exp(-(v+58)/20)\n"
  "        beta = 1 / (exp(-(v+28)/10) + 1)\n"
  "        sum = alpha + beta\n"
  "        hinf = alpha/sum\n"
  "        hexp = 1 - exp(tinc*sum)\n"
  "                :\"n\" potassium activation system\n"
  "        alpha = .01*vtrap(-(v+34),10) \n"
  "        beta = .125*exp(-(v+44)/80)\n"
  "        sum = alpha + beta\n"
  "        ninf = alpha/sum\n"
  "        nexp = 1 - exp(tinc*sum)\n"
  "}\n"
  " \n"
  "FUNCTION vtrap(x,y) {  :Traps for 0 in denominator of rate eqns.\n"
  "        if (fabs(x/y) < 1e-6) {\n"
  "                vtrap = y*(1 - x/y/2)\n"
  "        }else{\n"
  "                vtrap = x/(exp(x/y) - 1)\n"
  "        }\n"
  "}\n"
  " \n"
  "UNITSON\n"
  ;
#endif

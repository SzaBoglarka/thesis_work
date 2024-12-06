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
 
#define nrn_init _nrn_init__hhI
#define _nrn_initial _nrn_initial__hhI
#define nrn_cur _nrn_cur__hhI
#define _nrn_current _nrn_current__hhI
#define nrn_jacob _nrn_jacob__hhI
#define nrn_state _nrn_state__hhI
#define _net_receive _net_receive__hhI 
#define _f_rates _f_rates__hhI 
#define rates rates__hhI 
#define states states__hhI 
 
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
#define gl _p[2]
#define el _p[3]
#define gna _p[4]
#define ina _p[5]
#define gk _p[6]
#define ik _p[7]
#define il _p[8]
#define h _p[9]
#define n _p[10]
#define Dh _p[11]
#define Dn _p[12]
#define ena _p[13]
#define ek _p[14]
#define minf _p[15]
#define _g _p[16]
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
 "setdata_hhI", _hoc_setdata,
 "rates_hhI", _hoc_rates,
 "vtrap_hhI", _hoc_vtrap,
 0, 0
};
#define vtrap vtrap_hhI
 extern double vtrap( double , double );
 /* declare global and static user variables */
#define htau htau_hhI
 double htau = 0;
#define hinf hinf_hhI
 double hinf = 0;
#define ntau ntau_hhI
 double ntau = 0;
#define ninf ninf_hhI
 double ninf = 0;
#define speed speed_hhI
 double speed = 5;
#define usetable usetable_hhI
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "gl_hhI", 0, 1e+09,
 "gkbar_hhI", 0, 1e+09,
 "gnabar_hhI", 0, 1e+09,
 "speed_hhI", 0, 1e+09,
 "usetable_hhI", 0, 1,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "speed_hhI", "1",
 "htau_hhI", "ms",
 "ntau_hhI", "ms",
 "gnabar_hhI", "mho/cm2",
 "gkbar_hhI", "mho/cm2",
 "gl_hhI", "mho/cm2",
 "el_hhI", "mV",
 "gna_hhI", "mho/cm2",
 "ina_hhI", "mA/cm2",
 "gk_hhI", "mho/cm2",
 "ik_hhI", "mA/cm2",
 "il_hhI", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double h0 = 0;
 static double n0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "speed_hhI", &speed_hhI,
 "hinf_hhI", &hinf_hhI,
 "ninf_hhI", &ninf_hhI,
 "htau_hhI", &htau_hhI,
 "ntau_hhI", &ntau_hhI,
 "usetable_hhI", &usetable_hhI,
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
 
#define _cvode_ieq _ppvar[6]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"hhI",
 "gnabar_hhI",
 "gkbar_hhI",
 "gl_hhI",
 "el_hhI",
 0,
 "gna_hhI",
 "ina_hhI",
 "gk_hhI",
 "ik_hhI",
 "il_hhI",
 0,
 "h_hhI",
 "n_hhI",
 0,
 0};
 static Symbol* _na_sym;
 static Symbol* _k_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 17, _prop);
 	/*initialize range parameters*/
 	gnabar = 0.035;
 	gkbar = 0.009;
 	gl = 0.0001;
 	el = -65;
 	_prop->param = _p;
 	_prop->param_size = 17;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 7, _prop);
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

 void _hhI_reg() {
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
  hoc_register_prop_size(_mechtype, 17, 7);
  hoc_register_dparam_semantics(_mechtype, 0, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 6, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 hhI /home/szabobogi/BC_modells/Edin_2017_(WB)/hhI.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double _zmexp , _zhexp , _znexp ;
 static double _zq10 ;
 static double *_t_minf;
 static double *_t_hinf;
 static double *_t_ninf;
 static double *_t_htau;
 static double *_t_ntau;
static int _reset;
static char *modelname = "hhI.mod   interneuron sodium, potassium, and leak channels";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int _f_rates(double);
static int rates(double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static void _n_rates(double);
 static int _slist1[2], _dlist1[2];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   rates ( _threadargscomma_ v ) ;
   Dh = speed * ( hinf - h ) / htau ;
   Dn = speed * ( ninf - n ) / ntau ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 rates ( _threadargscomma_ v ) ;
 Dh = Dh  / (1. - dt*( ( ( speed )*( ( ( - 1.0 ) ) ) ) / htau )) ;
 Dn = Dn  / (1. - dt*( ( ( speed )*( ( ( - 1.0 ) ) ) ) / ntau )) ;
  return 0;
}
 /*END CVODE*/
 static int states () {_reset=0;
 {
   rates ( _threadargscomma_ v ) ;
    h = h + (1. - exp(dt*(( ( speed )*( ( ( - 1.0 ) ) ) ) / htau)))*(- ( ( ( speed )*( ( hinf ) ) ) / htau ) / ( ( ( speed )*( ( ( - 1.0 ) ) ) ) / htau ) - h) ;
    n = n + (1. - exp(dt*(( ( speed )*( ( ( - 1.0 ) ) ) ) / ntau)))*(- ( ( ( speed )*( ( ninf ) ) ) / ntau ) / ( ( ( speed )*( ( ( - 1.0 ) ) ) ) / ntau ) - n) ;
   }
  return 0;
}
 static double _mfac_rates, _tmin_rates;
 static void _check_rates();
 static void _check_rates() {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_celsius;
  if (!usetable) {return;}
  if (_sav_celsius != celsius) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_rates =  - 100.0 ;
   _tmax =  100.0 ;
   _dx = (_tmax - _tmin_rates)/200.; _mfac_rates = 1./_dx;
   for (_i=0, _x=_tmin_rates; _i < 201; _x += _dx, _i++) {
    _f_rates(_x);
    _t_minf[_i] = minf;
    _t_hinf[_i] = hinf;
    _t_ninf[_i] = ninf;
    _t_htau[_i] = htau;
    _t_ntau[_i] = ntau;
   }
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
  hinf = _xi;
  ninf = _xi;
  htau = _xi;
  ntau = _xi;
  return;
 }
 if (_xi <= 0.) {
 minf = _t_minf[0];
 hinf = _t_hinf[0];
 ninf = _t_ninf[0];
 htau = _t_htau[0];
 ntau = _t_ntau[0];
 return; }
 if (_xi >= 200.) {
 minf = _t_minf[200];
 hinf = _t_hinf[200];
 ninf = _t_ninf[200];
 htau = _t_htau[200];
 ntau = _t_ntau[200];
 return; }
 _i = (int) _xi;
 _theta = _xi - (double)_i;
 minf = _t_minf[_i] + _theta*(_t_minf[_i+1] - _t_minf[_i]);
 hinf = _t_hinf[_i] + _theta*(_t_hinf[_i+1] - _t_hinf[_i]);
 ninf = _t_ninf[_i] + _theta*(_t_ninf[_i+1] - _t_ninf[_i]);
 htau = _t_htau[_i] + _theta*(_t_htau[_i+1] - _t_htau[_i]);
 ntau = _t_ntau[_i] + _theta*(_t_ntau[_i+1] - _t_ntau[_i]);
 }

 
static int  _f_rates (  double _lv ) {
   double _lalpha , _lbeta , _lsum ;
  _zq10 = pow( 3.0 , ( ( celsius - 6.3 ) / 10.0 ) ) ;
   _lalpha = .1 * vtrap ( _threadargscomma_ - ( _lv + 35.0 ) , 10.0 ) ;
   _lbeta = 4.0 * exp ( - ( _lv + 60.0 ) / 18.0 ) ;
   _lsum = _lalpha + _lbeta ;
   minf = _lalpha / _lsum ;
   _lalpha = .07 * exp ( - ( _lv + 58.0 ) / 20.0 ) ;
   _lbeta = 1.0 / ( exp ( - ( _lv + 28.0 ) / 10.0 ) + 1.0 ) ;
   _lsum = _lalpha + _lbeta ;
   htau = 1.0 / ( _zq10 * _lsum ) ;
   hinf = _lalpha / _lsum ;
   _lalpha = .01 * vtrap ( _threadargscomma_ - ( _lv + 34.0 ) , 10.0 ) ;
   _lbeta = .125 * exp ( - ( _lv + 44.0 ) / 80.0 ) ;
   _lsum = _lalpha + _lbeta ;
   ntau = 1.0 / ( _zq10 * _lsum ) ;
   ninf = _lalpha / _lsum ;
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
  ena = _ion_ena;
  ek = _ion_ek;
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
  ena = _ion_ena;
  ek = _ion_ek;
 _ode_matsol_instance1(_threadargs_);
 }}
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
  n = n0;
 {
   rates ( _threadargscomma_ v ) ;
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
   gna = gnabar * minf * minf * minf * h ;
   ina = gna * ( v - ena ) ;
   gk = gkbar * n * n * n * n ;
   ik = gk * ( v - ek ) ;
   il = gl * ( v - el ) ;
   }
 _current += ina;
 _current += ik;
 _current += il;

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
 if(error){fprintf(stderr,"at line 91 in file hhI.mod:\n        SOLVE states METHOD cnexp\n"); nrn_complain(_p); abort_run(error);}
 }  }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(h) - _p;  _dlist1[0] = &(Dh) - _p;
 _slist1[1] = &(n) - _p;  _dlist1[1] = &(Dn) - _p;
   _t_minf = makevector(201*sizeof(double));
   _t_hinf = makevector(201*sizeof(double));
   _t_ninf = makevector(201*sizeof(double));
   _t_htau = makevector(201*sizeof(double));
   _t_ntau = makevector(201*sizeof(double));
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "/home/szabobogi/BC_modells/Edin_2017_(WB)/hhI.mod";
static const char* nmodl_file_text = 
  "TITLE hhI.mod   interneuron sodium, potassium, and leak channels\n"
  " \n"
  "COMMENT\n"
  "\n"
  " This file is based on the original hh.mod file (see original comment\n"
  " below). It was modified to match the model that was used in the\n"
  " simulations of Wang and Buzsaki (1996, J. Neurosci. 16).\n"
  "\n"
  " Author: Fredrik Edin, 2003\n"
  " Address: freedin@nada.kth.se\n"
  "\n"
  " Original comment:\n"
  " ***************************************************************************\n"
  " This is the original Hodgkin-Huxley treatment for the set of sodium, \n"
  "  potassium, and leakage channels found in the squid giant axon membrane.\n"
  "  (\"A quantitative description of membrane current and its application \n"
  "  conduction and excitation in nerve\" J.Physiol. (Lond.) 117:500-544 (1952).)\n"
  " Membrane voltage is in absolute mV and has been reversed in polarity\n"
  "  from the original HH convention and shifted to reflect a resting potential\n"
  "  of -65 mV.\n"
  " Remember to set celsius=6.3 (or whatever) in your HOC file.\n"
  " See squid.hoc for an example of a simulation using this model.\n"
  " SW Jaslove  6 March, 1992\n"
  " ***************************************************************************\n"
  "\n"
  " changes:\n"
  "\n"
  "  - m is substituted by its steady state value: m_inf - see 'BREAKPOINT'\n"
  "  {as a result mtau is not needed, 'minf' is removed from\n"
  "  GLOBAL declaration and 'm' is included in the RANGE var list\n"
  "  otherwise it will be handled as a GLOBAL var and will not be\n"
  "  evaluated separately for the 'sections'; for 'h' an 'n' this \n"
  "  is not a problem}\n"
  "\n"
  "  - for h and n alpha and beta values are multiplied by 5 \n"
  "  (see factor \"Phi\" in the W&B model)\n"
  "\n"
  "  - temp: set to 6.3 Celsius, alpha and beta values are set/manipulated\n"
  "  directly to simulate characteristic firing pattern\n"
  "\n"
  "  ***************************************************************************\n"
  "ENDCOMMENT\n"
  " \n"
  "UNITS {\n"
  "        (mA) = (milliamp)\n"
  "        (mV) = (millivolt)\n"
  "	(S) = (siemens)\n"
  "}\n"
  "\n"
  "? interface\n"
  "\n"
  "NEURON {\n"
  "        SUFFIX hhI\n"
  "	USEION na READ ena WRITE ina\n"
  "	USEION k READ ek WRITE ik\n"
  "        NONSPECIFIC_CURRENT il\n"
  "        RANGE gnabar, gna, gkbar, gk, gl, el, ek, ena, ina, ik, il\n"
  "	GLOBAL hinf, ninf, htau, ntau, speed\n"
  "}\n"
  " \n"
  "PARAMETER {\n"
  "	speed 	= 5 	(1)     	<0,1e9>\n"
  "        gnabar	= .035 	(mho/cm2)	<0,1e9>\n"
  "	gkbar 	= .009 	(mho/cm2)	<0,1e9>\n"
  "        gl	= .0001 (mho/cm2)	<0,1e9>\n"
  "        el 	= -65 	(mV)\n"
  "}\n"
  "  \n"
  "STATE {\n"
  "        h n\n"
  "}\n"
  " \n"
  "ASSIGNED {\n"
  "        v (mV)\n"
  "	celsius (degC)\n"
  "	ena 	(mV)\n"
  "	gna 	(mho/cm2)\n"
  "        ina 	(mA/cm2) \n"
  "	ek	(mV)\n"
  "	gk 	(mho/cm2) \n"
  "        ik 	(mA/cm2)\n"
  "        il 	(mA/cm2)\n"
  "        minf hinf ninf\n"
  "	htau (ms) ntau (ms)\n"
  "}\n"
  " \n"
  "LOCAL mexp, hexp, nexp        \n"
  " \n"
  "? currents\n"
  "BREAKPOINT {\n"
  "        SOLVE states METHOD cnexp\n"
  "	gna = gnabar*minf*minf*minf*h\n"
  "	ina = gna*(v - ena)\n"
  "        gk = gkbar*n*n*n*n\n"
  "	ik = gk*(v - ek)      \n"
  "        il = gl*(v - el)\n"
  "}\n"
  "\n"
  "\n"
  "INITIAL {\n"
  "	rates(v)\n"
  "	h = hinf\n"
  "	n = ninf\n"
  "}\n"
  "\n"
  "\n"
  "? states\n"
  "DERIVATIVE states {\n"
  "        rates(v)\n"
  "        h' = speed * (hinf-h)/htau\n"
  "        n' = speed * (ninf-n)/ntau\n"
  "}\n"
  " \n"
  "LOCAL q10\n"
  "\n"
  "\n"
  "? rates\n"
  "PROCEDURE rates(v(mV)) {  :Computes rate and other constants at current v.\n"
  "                          :Call once from HOC to initialize inf at resting v.\n"
  "		      \n"
  "        LOCAL  alpha, beta, sum\n"
  "        TABLE minf, hinf, ninf, htau, ntau DEPEND celsius FROM -100 TO 100 WITH 200\n"
  "\n"
  "UNITSOFF\n"
  "        q10 = 3^((celsius - 6.3)/10)\n"
  "\n"
  "        :\"m\" sodium activation system\n"
  "        alpha = .1 * vtrap(-(v+35),10)\n"
  "        beta =  4 * exp(-(v+60)/18)\n"
  "        sum = alpha + beta\n"
  "        minf = alpha/sum\n"
  "\n"
  "        :\"h\" sodium inactivation system\n"
  "        alpha = .07 * exp(-(v+58)/20)\n"
  "        beta = 1 / (exp(-(v+28)/10) + 1)\n"
  "        sum = alpha + beta\n"
  "	htau = 1/(q10*sum)\n"
  "        hinf = alpha/sum\n"
  "\n"
  "        :\"n\" potassium activation system\n"
  "        alpha = .01*vtrap(-(v+34),10) \n"
  "        beta = .125*exp(-(v+44)/80)\n"
  "	sum = alpha + beta\n"
  "        ntau = 1/(q10*sum)\n"
  "        ninf = alpha/sum\n"
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

/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
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
 
#define nrn_init _nrn_init__hhBC
#define _nrn_initial _nrn_initial__hhBC
#define nrn_cur _nrn_cur__hhBC
#define _nrn_current _nrn_current__hhBC
#define nrn_jacob _nrn_jacob__hhBC
#define nrn_state _nrn_state__hhBC
#define _net_receive _net_receive__hhBC 
#define _f_rates _f_rates__hhBC 
#define rates rates__hhBC 
#define states states__hhBC 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define gnabar _p[0]
#define gkbar _p[1]
#define gl _p[2]
#define el _p[3]
#define gna _p[4]
#define gk _p[5]
#define ina _p[6]
#define ik _p[7]
#define il _p[8]
#define m _p[9]
#define h _p[10]
#define n1 _p[11]
#define n2 _p[12]
#define Dm _p[13]
#define Dh _p[14]
#define Dn1 _p[15]
#define Dn2 _p[16]
#define v _p[17]
#define _g _p[18]
 
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
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
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
 _extcall_prop = _prop;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_hhBC", _hoc_setdata,
 "rates_hhBC", _hoc_rates,
 "vtrap_hhBC", _hoc_vtrap,
 0, 0
};
#define vtrap vtrap_hhBC
 extern double vtrap( _threadargsprotocomma_ double , double );
 
static void _check_rates(double*, Datum*, Datum*, _NrnThread*); 
static void _check_table_thread(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, int _type) {
   _check_rates(_p, _ppvar, _thread, _nt);
 }
 #define _zphiM _thread[0]._pval[0]
 #define _zphiH _thread[0]._pval[1]
 #define _zphiN _thread[0]._pval[2]
 /* declare global and static user variables */
 static int _thread1data_inuse = 0;
static double _thread1data[8];
#define _gth 1
#define ek ek_hhBC
 double ek = -90;
#define ena ena_hhBC
 double ena = 55;
#define expoN2 expoN2_hhBC
 double expoN2 = 3;
#define expoN1 expoN1_hhBC
 double expoN1 = 1;
#define htau_hhBC _thread1data[0]
#define htau _thread[_gth]._pval[0]
#define hinf_hhBC _thread1data[1]
#define hinf _thread[_gth]._pval[1]
#define mtau_hhBC _thread1data[2]
#define mtau _thread[_gth]._pval[2]
#define minf_hhBC _thread1data[3]
#define minf _thread[_gth]._pval[3]
#define ntau2_hhBC _thread1data[4]
#define ntau2 _thread[_gth]._pval[4]
#define ntau1_hhBC _thread1data[5]
#define ntau1 _thread[_gth]._pval[5]
#define ninf2_hhBC _thread1data[6]
#define ninf2 _thread[_gth]._pval[6]
#define ninf1_hhBC _thread1data[7]
#define ninf1 _thread[_gth]._pval[7]
#define shiftN shiftN_hhBC
 double shiftN = 0;
#define shiftH shiftH_hhBC
 double shiftH = 20;
#define shiftM shiftM_hhBC
 double shiftM = 20;
#define usetable usetable_hhBC
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "gl_hhBC", 0, 1e+09,
 "gkbar_hhBC", 0, 1e+09,
 "gnabar_hhBC", 0, 1e+09,
 "usetable_hhBC", 0, 1,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "ena_hhBC", "mV",
 "ek_hhBC", "mV",
 "shiftM_hhBC", "mV",
 "shiftH_hhBC", "mV",
 "shiftN_hhBC", "mV",
 "mtau_hhBC", "ms",
 "htau_hhBC", "ms",
 "ntau1_hhBC", "ms",
 "ntau2_hhBC", "ms",
 "gnabar_hhBC", "S/cm2",
 "gkbar_hhBC", "S/cm2",
 "gl_hhBC", "S/cm2",
 "el_hhBC", "mV",
 "gna_hhBC", "S/cm2",
 "gk_hhBC", "S/cm2",
 "ina_hhBC", "mA/cm2",
 "ik_hhBC", "mA/cm2",
 "il_hhBC", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double h0 = 0;
 static double m0 = 0;
 static double n20 = 0;
 static double n10 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "ena_hhBC", &ena_hhBC,
 "ek_hhBC", &ek_hhBC,
 "expoN1_hhBC", &expoN1_hhBC,
 "expoN2_hhBC", &expoN2_hhBC,
 "shiftM_hhBC", &shiftM_hhBC,
 "shiftH_hhBC", &shiftH_hhBC,
 "shiftN_hhBC", &shiftN_hhBC,
 "minf_hhBC", &minf_hhBC,
 "hinf_hhBC", &hinf_hhBC,
 "ninf1_hhBC", &ninf1_hhBC,
 "ninf2_hhBC", &ninf2_hhBC,
 "mtau_hhBC", &mtau_hhBC,
 "htau_hhBC", &htau_hhBC,
 "ntau1_hhBC", &ntau1_hhBC,
 "ntau2_hhBC", &ntau2_hhBC,
 "usetable_hhBC", &usetable_hhBC,
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
 
#define _cvode_ieq _ppvar[0]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"hhBC",
 "gnabar_hhBC",
 "gkbar_hhBC",
 "gl_hhBC",
 "el_hhBC",
 0,
 "gna_hhBC",
 "gk_hhBC",
 "ina_hhBC",
 "ik_hhBC",
 "il_hhBC",
 0,
 "m_hhBC",
 "h_hhBC",
 "n1_hhBC",
 "n2_hhBC",
 0,
 0};
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 19, _prop);
 	/*initialize range parameters*/
 	gnabar = 0.05;
 	gkbar = 0.03;
 	gl = 0.0001;
 	el = -65;
 	_prop->param = _p;
 	_prop->param_size = 19;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 1, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _thread_mem_init(Datum*);
 static void _thread_cleanup(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _hhBC_reg() {
	int _vectorized = 1;
  _initlists();
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 3);
  _extcall_thread = (Datum*)ecalloc(2, sizeof(Datum));
  _thread_mem_init(_extcall_thread);
  _thread1data_inuse = 0;
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 1, _thread_mem_init);
     _nrn_thread_reg(_mechtype, 0, _thread_cleanup);
     _nrn_thread_table_reg(_mechtype, _check_table_thread);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 19, 1);
  hoc_register_dparam_semantics(_mechtype, 0, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 hhBC /home/szabobogi/BC_modells/Hu_2018_(WB)/hhBC.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 /*Top LOCAL _zphiM , _zphiH , _zphiN */
 static double *_t_minf;
 static double *_t_mtau;
 static double *_t_hinf;
 static double *_t_htau;
 static double *_t_ninf1;
 static double *_t_ntau1;
 static double *_t_ninf2;
 static double *_t_ntau2;
static int _reset;
static char *modelname = "hhBC.mod   sodium, potassium, and leak channels";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int _f_rates(_threadargsprotocomma_ double);
static int rates(_threadargsprotocomma_ double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static void _n_rates(_threadargsprotocomma_ double _lv);
 static int _slist1[4], _dlist1[4];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset = 0; {
   rates ( _threadargscomma_ v ) ;
   Dm = ( minf - m ) / mtau ;
   Dh = ( hinf - h ) / htau ;
   Dn1 = ( ninf1 - n1 ) / ntau1 ;
   Dn2 = ( ninf2 - n2 ) / ntau2 ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
 rates ( _threadargscomma_ v ) ;
 Dm = Dm  / (1. - dt*( ( ( ( - 1.0 ) ) ) / mtau )) ;
 Dh = Dh  / (1. - dt*( ( ( ( - 1.0 ) ) ) / htau )) ;
 Dn1 = Dn1  / (1. - dt*( ( ( ( - 1.0 ) ) ) / ntau1 )) ;
 Dn2 = Dn2  / (1. - dt*( ( ( ( - 1.0 ) ) ) / ntau2 )) ;
  return 0;
}
 /*END CVODE*/
 static int states (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) { {
   rates ( _threadargscomma_ v ) ;
    m = m + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / mtau)))*(- ( ( ( minf ) ) / mtau ) / ( ( ( ( - 1.0 ) ) ) / mtau ) - m) ;
    h = h + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / htau)))*(- ( ( ( hinf ) ) / htau ) / ( ( ( ( - 1.0 ) ) ) / htau ) - h) ;
    n1 = n1 + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / ntau1)))*(- ( ( ( ninf1 ) ) / ntau1 ) / ( ( ( ( - 1.0 ) ) ) / ntau1 ) - n1) ;
    n2 = n2 + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / ntau2)))*(- ( ( ( ninf2 ) ) / ntau2 ) / ( ( ( ( - 1.0 ) ) ) / ntau2 ) - n2) ;
   }
  return 0;
}
 static double _mfac_rates, _tmin_rates;
  static void _check_rates(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
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
    _f_rates(_p, _ppvar, _thread, _nt, _x);
    _t_minf[_i] = minf;
    _t_mtau[_i] = mtau;
    _t_hinf[_i] = hinf;
    _t_htau[_i] = htau;
    _t_ninf1[_i] = ninf1;
    _t_ntau1[_i] = ntau1;
    _t_ninf2[_i] = ninf2;
    _t_ntau2[_i] = ntau2;
   }
   _sav_celsius = celsius;
  }
 }

 static int rates(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv) { 
#if 0
_check_rates(_p, _ppvar, _thread, _nt);
#endif
 _n_rates(_p, _ppvar, _thread, _nt, _lv);
 return 0;
 }

 static void _n_rates(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 _f_rates(_p, _ppvar, _thread, _nt, _lv); return; 
}
 _xi = _mfac_rates * (_lv - _tmin_rates);
 if (isnan(_xi)) {
  minf = _xi;
  mtau = _xi;
  hinf = _xi;
  htau = _xi;
  ninf1 = _xi;
  ntau1 = _xi;
  ninf2 = _xi;
  ntau2 = _xi;
  return;
 }
 if (_xi <= 0.) {
 minf = _t_minf[0];
 mtau = _t_mtau[0];
 hinf = _t_hinf[0];
 htau = _t_htau[0];
 ninf1 = _t_ninf1[0];
 ntau1 = _t_ntau1[0];
 ninf2 = _t_ninf2[0];
 ntau2 = _t_ntau2[0];
 return; }
 if (_xi >= 200.) {
 minf = _t_minf[200];
 mtau = _t_mtau[200];
 hinf = _t_hinf[200];
 htau = _t_htau[200];
 ninf1 = _t_ninf1[200];
 ntau1 = _t_ntau1[200];
 ninf2 = _t_ninf2[200];
 ntau2 = _t_ntau2[200];
 return; }
 _i = (int) _xi;
 _theta = _xi - (double)_i;
 minf = _t_minf[_i] + _theta*(_t_minf[_i+1] - _t_minf[_i]);
 mtau = _t_mtau[_i] + _theta*(_t_mtau[_i+1] - _t_mtau[_i]);
 hinf = _t_hinf[_i] + _theta*(_t_hinf[_i+1] - _t_hinf[_i]);
 htau = _t_htau[_i] + _theta*(_t_htau[_i+1] - _t_htau[_i]);
 ninf1 = _t_ninf1[_i] + _theta*(_t_ninf1[_i+1] - _t_ninf1[_i]);
 ntau1 = _t_ntau1[_i] + _theta*(_t_ntau1[_i+1] - _t_ntau1[_i]);
 ninf2 = _t_ninf2[_i] + _theta*(_t_ninf2[_i+1] - _t_ninf2[_i]);
 ntau2 = _t_ntau2[_i] + _theta*(_t_ntau2[_i+1] - _t_ntau2[_i]);
 }

 
static int  _f_rates ( _threadargsprotocomma_ double _lv ) {
   double _lalpha , _lbeta , _lsum ;
  _zphiM = pow( 2.2 , ( ( celsius - 23.5 ) / 10.0 ) ) ;
   _zphiH = pow( 2.9 , ( ( celsius - 23.5 ) / 10.0 ) ) ;
   _zphiN = pow( 3.0 , ( ( celsius - 23.5 ) / 10.0 ) ) ;
   _lalpha = .2567 * vtrap ( _threadargscomma_ - ( _lv + 60.84 - shiftM ) , 9.722 ) ;
   _lbeta = .1133 * vtrap ( _threadargscomma_ ( _lv + 30.253 - shiftM ) , 2.848 ) ;
   _lsum = _lalpha + _lbeta ;
   mtau = 1.0 / ( _zphiM * _lsum ) ;
   minf = _lalpha / _lsum ;
   _lalpha = 0.00105 * exp ( - ( _lv - shiftH ) / 20.000 ) ;
   _lbeta = 4.827 / ( exp ( - ( _lv + 18.646 - shiftH ) / 12.452 ) + 1.0 ) ;
   _lsum = _lalpha + _lbeta ;
   htau = 1.0 / ( _zphiH * _lsum ) ;
   hinf = _lalpha / _lsum ;
   _lalpha = .0993 * vtrap ( _threadargscomma_ - ( _lv - 33.720 - shiftN ) , 12.742 ) ;
   _lbeta = .1379 * exp ( - ( _lv - shiftN ) / 500.0 ) ;
   _lsum = _lalpha + _lbeta ;
   ntau1 = 1.0 / ( _zphiN * _lsum ) ;
   ninf1 = _lalpha / _lsum ;
   _lalpha = .0610 * vtrap ( _threadargscomma_ - ( _lv - 29.991 - shiftN ) , 27.502 ) ;
   _lbeta = .001504 * exp ( - ( _lv - shiftN ) / 17.177 ) ;
   _lsum = _lalpha + _lbeta ;
   ntau2 = 1.0 / ( _zphiN * _lsum ) ;
   ninf2 = _lalpha / _lsum ;
    return 0; }
 
static void _hoc_rates(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 
#if 1
 _check_rates(_p, _ppvar, _thread, _nt);
#endif
 _r = 1.;
 rates ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
double vtrap ( _threadargsprotocomma_ double _lx , double _ly ) {
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
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  vtrap ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 4;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
     _ode_spec1 (_p, _ppvar, _thread, _nt);
 }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 4; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 (_p, _ppvar, _thread, _nt);
 }
 
static void _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
 _ode_matsol_instance1(_threadargs_);
 }}
 
static void _thread_mem_init(Datum* _thread) {
   _thread[0]._pval = (double*)ecalloc(3, sizeof(double));
  if (_thread1data_inuse) {_thread[_gth]._pval = (double*)ecalloc(8, sizeof(double));
 }else{
 _thread[_gth]._pval = _thread1data; _thread1data_inuse = 1;
 }
 }
 
static void _thread_cleanup(Datum* _thread) {
   free((void*)(_thread[0]._pval));
  if (_thread[_gth]._pval == _thread1data) {
   _thread1data_inuse = 0;
  }else{
   free((void*)_thread[_gth]._pval);
  }
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  h = h0;
  m = m0;
  n2 = n20;
  n1 = n10;
 {
   rates ( _threadargscomma_ v ) ;
   m = minf ;
   h = hinf ;
   n1 = ninf1 ;
   n2 = ninf2 ;
   }
 
}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];

#if 0
 _check_rates(_p, _ppvar, _thread, _nt);
#endif
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
 initmodel(_p, _ppvar, _thread, _nt);
}
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   gna = gnabar * m * m * m * h ;
   ina = gna * ( v - ena ) ;
   gk = gkbar * ( pow( n1 , expoN1 ) ) * ( pow( n2 , expoN2 ) ) ;
   ik = gk * ( v - ek ) ;
   il = gl * ( v - el ) ;
   }
 _current += il;
 _current += ina;
 _current += ik;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
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
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
 	}
 _g = (_g - _rhs)/.001;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
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
 
}
 
}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
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
 {   states(_p, _ppvar, _thread, _nt);
  }}}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(m) - _p;  _dlist1[0] = &(Dm) - _p;
 _slist1[1] = &(h) - _p;  _dlist1[1] = &(Dh) - _p;
 _slist1[2] = &(n1) - _p;  _dlist1[2] = &(Dn1) - _p;
 _slist1[3] = &(n2) - _p;  _dlist1[3] = &(Dn2) - _p;
   _t_minf = makevector(201*sizeof(double));
   _t_mtau = makevector(201*sizeof(double));
   _t_hinf = makevector(201*sizeof(double));
   _t_htau = makevector(201*sizeof(double));
   _t_ninf1 = makevector(201*sizeof(double));
   _t_ntau1 = makevector(201*sizeof(double));
   _t_ninf2 = makevector(201*sizeof(double));
   _t_ntau2 = makevector(201*sizeof(double));
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/home/szabobogi/BC_modells/Hu_2018_(WB)/hhBC.mod";
static const char* nmodl_file_text = 
  "TITLE hhBC.mod   sodium, potassium, and leak channels\n"
  " \n"
  "COMMENT\n"
  "  This is a Hodgkin-Huxley equation set for the sodium,  \n"
  "  potassium, and leakage channels found in basket cell axons. \n"
  "  modified from file hh.mod by SW Jaslove  6 March, 1992\n"
  "  Peter Jonas, 20.02.2017 \n"
  "  K channels with two n particles to describe experimental data \n"
  "  17.03.2017 - update of Na inactivation values \n"
  "  24.12.2018 - modified phiM, phiH, and phiN to ensure compatibility with new mknrndll \n"
  "  05.03.2020 - modified celsius allowing repeated changes in temperature \n"
  "  \n"
  "  \n"
  "ENDCOMMENT\n"
  " \n"
  "UNITS {\n"
  "        (mA) = (milliamp)\n"
  "        (mV) = (millivolt)\n"
  "	    (S) = (siemens)\n"
  "}\n"
  " \n"
  "? interface\n"
  "NEURON {\n"
  "        SUFFIX hhBC\n"
  "        NONSPECIFIC_CURRENT il, ina, ik\n"
  "        RANGE gnabar, gkbar, gl, el, gna, gk\n"
  "        GLOBAL minf, hinf, ninf1, ninf2, mtau, htau, ntau1, ntau2, expoN1, expoN2, shiftM, shiftH, shiftN\n"
  "	    THREADSAFE : assigned GLOBALs will be per thread\n"
  "}\n"
  " \n"
  "PARAMETER {\n"
  "        gnabar = .050 (S/cm2)	<0,1e9>\n"
  "        gkbar = .030 (S/cm2)	<0,1e9>\n"
  "        gl = .0001 (S/cm2)	<0,1e9>\n"
  "		ena = 55 (mV) \n"
  "		ek = -90 (mV) \n"
  "        el = -65 (mV) \n"
  "\n"
  "		expoN1 = 1 ()\n"
  "		expoN2 = 3 ()\n"
  "		shiftM = 20.0 (mV) : RIGHT shift Na+ channel gating according to Donnan potentials \n"
  "		shiftH = 20.0 (mV) \n"
  "		shiftN = 0.0 (mV)\n"
  "}\n"
  " \n"
  "STATE {\n"
  "        m h n1 n2\n"
  "}\n"
  " \n"
  "ASSIGNED {\n"
  "        v (mV)\n"
  "        gna (S/cm2)\n"
  "	    gk (S/cm2)\n"
  "        ina (mA/cm2)\n"
  "        ik (mA/cm2)\n"
  "        il (mA/cm2)\n"
  "        minf hinf ninf1 ninf2\n"
  "	    mtau (ms) htau (ms) ntau1 (ms) ntau2 (ms)\n"
  "		celsius (degC)\n"
  "}\n"
  " \n"
  "? currents\n"
  "BREAKPOINT {\n"
  "        SOLVE states METHOD cnexp\n"
  "        gna = gnabar*m*m*m*h\n"
  "	    ina = gna*(v - ena)\n"
  "        gk = gkbar*(n1^expoN1)*(n2^expoN2)\n"
  "	    ik = gk*(v - ek)      \n"
  "        il = gl*(v - el)\n"
  "}\n"
  " \n"
  " \n"
  "INITIAL {\n"
  "	rates(v)\n"
  "	m = minf\n"
  "	h = hinf\n"
  "	n1 = ninf1\n"
  "	n2 = ninf2\n"
  "}\n"
  "\n"
  "? states\n"
  "DERIVATIVE states {  \n"
  "        rates(v)\n"
  "        m' =  (minf-m)/mtau\n"
  "        h' = (hinf-h)/htau\n"
  "        n1' = (ninf1-n1)/ntau1\n"
  "        n2' = (ninf2-n2)/ntau2\n"
  "}\n"
  " \n"
  "LOCAL phiM, phiH, phiN\n"
  "\n"
  "? rates\n"
  "PROCEDURE rates(v(mV)) {  :Computes rate and other constants at current v.\n"
  "                      :Call once from HOC to initialize inf at resting v.\n"
  "        LOCAL  alpha, beta, sum\n"
  "        TABLE minf, mtau, hinf, htau, ninf1, ntau1, ninf2, ntau2 DEPEND celsius FROM -100 TO 100 WITH 200\n"
  "\n"
  "UNITSOFF\n"
  "        phiM = 2.2^((celsius - 23.5)/10) \n"
  "	    phiH =  2.9^((celsius - 23.5)/10)\n"
  "		phiN = 3.0^((celsius - 23.5)/10)\n"
  "		\n"
  "		:\"m\" sodium activation system\n"
  "        alpha = .2567 * vtrap(-(v+60.84-shiftM),9.722)\n"
  "        :beta =  4 * exp(-(v+65)/18)\n"
  "		beta = .1133 * vtrap((v+30.253-shiftM),2.848)\n"
  "        sum = alpha + beta\n"
  "		mtau = 1/(phiM*sum)\n"
  "        minf = alpha/sum\n"
  "		\n"
  "		:\"h\" sodium inactivation system\n"
  "        alpha = 0.00105 * exp(-(v-shiftH)/20.000)\n"
  "        beta = 4.827 / (exp(-(v+18.646-shiftH)/12.452) + 1)\n"
  "        sum = alpha + beta\n"
  "	    htau = 1/(phiH*sum)\n"
  "        hinf = alpha/sum\n"
  "\n"
  "		 :\"n1\" potassium activation system\n"
  "        alpha = .0993*vtrap(-(v-33.720-shiftN),12.742) \n"
  "        beta = .1379*exp(-(v-shiftN)/500)\n"
  "	    sum = alpha + beta\n"
  "        ntau1 = 1/(phiN*sum)\n"
  "        ninf1 = alpha/sum\n"
  "        :\"n2\" potassium activation system\n"
  "        alpha = .0610*vtrap(-(v-29.991-shiftN),27.502) \n"
  "        beta = .001504*exp(-(v-shiftN)/17.177)\n"
  "	    sum = alpha + beta\n"
  "        ntau2 = 1/(phiN*sum)\n"
  "        ninf2 = alpha/sum\n"
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

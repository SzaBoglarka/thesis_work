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
 
#define nrn_init _nrn_init__ch_NavPVBC
#define _nrn_initial _nrn_initial__ch_NavPVBC
#define nrn_cur _nrn_cur__ch_NavPVBC
#define _nrn_current _nrn_current__ch_NavPVBC
#define nrn_jacob _nrn_jacob__ch_NavPVBC
#define nrn_state _nrn_state__ch_NavPVBC
#define _net_receive _net_receive__ch_NavPVBC 
#define _f_trates _f_trates__ch_NavPVBC 
#define rates rates__ch_NavPVBC 
#define states states__ch_NavPVBC 
#define trates trates__ch_NavPVBC 
 
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
#define gmax _p[0]
#define vshift _p[1]
#define g _p[2]
#define ina _p[3]
#define minf _p[4]
#define hinf _p[5]
#define mtau _p[6]
#define htau _p[7]
#define myi _p[8]
#define m _p[9]
#define h _p[10]
#define ena _p[11]
#define Dm _p[12]
#define Dh _p[13]
#define mexp _p[14]
#define hexp _p[15]
#define _g _p[16]
#define _ion_ena	*_ppvar[0]._pval
#define _ion_ina	*_ppvar[1]._pval
#define _ion_dinadv	*_ppvar[2]._pval
 
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
 static void _hoc_trates(void);
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
 "setdata_ch_NavPVBC", _hoc_setdata,
 "rates_ch_NavPVBC", _hoc_rates,
 "states_ch_NavPVBC", _hoc_states,
 "trates_ch_NavPVBC", _hoc_trates,
 "vtrap_ch_NavPVBC", _hoc_vtrap,
 0, 0
};
#define vtrap vtrap_ch_NavPVBC
 extern double vtrap( double , double );
 /* declare global and static user variables */
#define usetable usetable_ch_NavPVBC
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "usetable_ch_NavPVBC", 0, 1,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "gmax_ch_NavPVBC", "mho/cm2",
 "vshift_ch_NavPVBC", "mV",
 "g_ch_NavPVBC", "mho/cm2",
 "ina_ch_NavPVBC", "mA/cm2",
 "mtau_ch_NavPVBC", "ms",
 "htau_ch_NavPVBC", "ms",
 "myi_ch_NavPVBC", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double h0 = 0;
 static double m0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "usetable_ch_NavPVBC", &usetable_ch_NavPVBC,
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
"ch_NavPVBC",
 "gmax_ch_NavPVBC",
 "vshift_ch_NavPVBC",
 0,
 "g_ch_NavPVBC",
 "ina_ch_NavPVBC",
 "minf_ch_NavPVBC",
 "hinf_ch_NavPVBC",
 "mtau_ch_NavPVBC",
 "htau_ch_NavPVBC",
 "myi_ch_NavPVBC",
 0,
 "m_ch_NavPVBC",
 "h_ch_NavPVBC",
 0,
 0};
 static Symbol* _na_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 17, _prop);
 	/*initialize range parameters*/
 	gmax = 0;
 	vshift = 0;
 	_prop->param = _p;
 	_prop->param_size = 17;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_na_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ena */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ina */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dinadv */
 
}
 static void _initlists();
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _ch_NavPVBC_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("na", 1.0);
 	_na_sym = hoc_lookup("na_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 17, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "na_ion");
 	hoc_register_cvode(_mechtype, _ode_count, 0, 0, 0);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 ch_NavPVBC C:/Users/DELL 111/Documents/Bogl�rka nagyon komoly mapp�ja/Suli muri/TDK szakdoga stuff/Kos�rsejt modellek/Modell csupasz�t�s/CA1 modellek/CA1 Lee et al. 2014/ch_NavPVBC.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 96520.0;
 static double R = 8.3134;
 static double _zq10 ;
 static double *_t_minf;
 static double *_t_mexp;
 static double *_t_hinf;
 static double *_t_hexp;
 static double *_t_mtau;
 static double *_t_htau;
static int _reset;
static char *modelname = "Voltage-gated sodium channel";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int _f_trates(double);
static int rates(double);
static int states();
static int trates(double);
 static void _n_trates(double);
 
/*VERBATIM*/
#include <stdlib.h> 
/* 	Include this library so that the following (innocuous) warning does not appear:
		In function '_thread_cleanup':
		warning: incompatible implicit declaration of built-in function 'free'  */
 
static int  states (  ) {
   trates ( _threadargscomma_ v ) ;
   m = m + mexp * ( minf - m ) ;
   h = h + hexp * ( hinf - h ) ;
    return 0; }
 
static void _hoc_states(void) {
  double _r;
   _r = 1.;
 states (  );
 hoc_retpushx(_r);
}
 
static int  rates (  double _lv ) {
   double _lalpha , _lbeta , _lsum ;
 _zq10 = pow( 3.0 , ( ( celsius - 34.0 ) / 10.0 ) ) ;
   _lalpha = - 0.3 * vtrap ( _threadargscomma_ ( _lv + 60.0 - 17.0 + vshift ) , - 5.0 ) ;
   _lbeta = 0.3 * vtrap ( _threadargscomma_ ( _lv + 60.0 - 45.0 + vshift ) , 5.0 ) ;
   _lsum = _lalpha + _lbeta ;
   mtau = 1.0 / _lsum ;
   minf = _lalpha / _lsum ;
   _lalpha = 0.23 / exp ( ( _lv + 60.0 + 5.0 + vshift ) / 20.0 ) ;
   _lbeta = 3.33 / ( 1.0 + exp ( ( _lv + 60.0 - 47.5 + vshift ) / - 10.0 ) ) ;
   _lsum = _lalpha + _lbeta ;
   htau = 1.0 / _lsum ;
   hinf = _lalpha / _lsum ;
    return 0; }
 
static void _hoc_rates(void) {
  double _r;
   _r = 1.;
 rates (  *getarg(1) );
 hoc_retpushx(_r);
}
 static double _mfac_trates, _tmin_trates;
 static void _check_trates();
 static void _check_trates() {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_dt;
  static double _sav_celsius;
  if (!usetable) {return;}
  if (_sav_dt != dt) { _maktable = 1;}
  if (_sav_celsius != celsius) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_trates =  - 100.0 ;
   _tmax =  100.0 ;
   _dx = (_tmax - _tmin_trates)/200.; _mfac_trates = 1./_dx;
   for (_i=0, _x=_tmin_trates; _i < 201; _x += _dx, _i++) {
    _f_trates(_x);
    _t_minf[_i] = minf;
    _t_mexp[_i] = mexp;
    _t_hinf[_i] = hinf;
    _t_hexp[_i] = hexp;
    _t_mtau[_i] = mtau;
    _t_htau[_i] = htau;
   }
   _sav_dt = dt;
   _sav_celsius = celsius;
  }
 }

 static int trates(double _lv){ _check_trates();
 _n_trates(_lv);
 return 0;
 }

 static void _n_trates(double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 _f_trates(_lv); return; 
}
 _xi = _mfac_trates * (_lv - _tmin_trates);
 if (isnan(_xi)) {
  minf = _xi;
  mexp = _xi;
  hinf = _xi;
  hexp = _xi;
  mtau = _xi;
  htau = _xi;
  return;
 }
 if (_xi <= 0.) {
 minf = _t_minf[0];
 mexp = _t_mexp[0];
 hinf = _t_hinf[0];
 hexp = _t_hexp[0];
 mtau = _t_mtau[0];
 htau = _t_htau[0];
 return; }
 if (_xi >= 200.) {
 minf = _t_minf[200];
 mexp = _t_mexp[200];
 hinf = _t_hinf[200];
 hexp = _t_hexp[200];
 mtau = _t_mtau[200];
 htau = _t_htau[200];
 return; }
 _i = (int) _xi;
 _theta = _xi - (double)_i;
 minf = _t_minf[_i] + _theta*(_t_minf[_i+1] - _t_minf[_i]);
 mexp = _t_mexp[_i] + _theta*(_t_mexp[_i+1] - _t_mexp[_i]);
 hinf = _t_hinf[_i] + _theta*(_t_hinf[_i+1] - _t_hinf[_i]);
 hexp = _t_hexp[_i] + _theta*(_t_hexp[_i+1] - _t_hexp[_i]);
 mtau = _t_mtau[_i] + _theta*(_t_mtau[_i+1] - _t_mtau[_i]);
 htau = _t_htau[_i] + _theta*(_t_htau[_i+1] - _t_htau[_i]);
 }

 
static int  _f_trates (  double _lv ) {
   double _ltinc ;
 rates ( _threadargscomma_ _lv ) ;
   _ltinc = - dt * _zq10 ;
   mexp = 1.0 - exp ( _ltinc / mtau ) ;
   hexp = 1.0 - exp ( _ltinc / htau ) ;
    return 0; }
 
static void _hoc_trates(void) {
  double _r;
    _r = 1.;
 trates (  *getarg(1) );
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
 
static int _ode_count(int _type){ hoc_execerror("ch_NavPVBC", "cannot be used with CVODE"); return 0;}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_na_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_na_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_na_sym, _ppvar, 2, 4);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  h = h0;
  m = m0;
 {
   trates ( _threadargscomma_ v ) ;
   m = minf ;
   h = hinf ;
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
 initmodel();
 }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   g = gmax * m * m * m * h ;
   ina = g * ( v - ena ) ;
   myi = ina ;
   }
 _current += ina;

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
 _g = _nrn_current(_v + .001);
 	{ double _dina;
  _dina = ina;
 _rhs = _nrn_current(_v);
  _ion_dinadv += (_dina - ina)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ina += ina ;
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
 { error =  states();
 if(error){fprintf(stderr,"at line 66 in file ch_NavPVBC.mod:\n	SOLVE states\n"); nrn_complain(_p); abort_run(error);}
 } }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
   _t_minf = makevector(201*sizeof(double));
   _t_mexp = makevector(201*sizeof(double));
   _t_hinf = makevector(201*sizeof(double));
   _t_hexp = makevector(201*sizeof(double));
   _t_mtau = makevector(201*sizeof(double));
   _t_htau = makevector(201*sizeof(double));
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "ch_NavPVBC.mod";
static const char* nmodl_file_text = 
  "TITLE Voltage-gated sodium channel\n"
  " \n"
  "COMMENT\n"
  "Voltage-gated Na+ channel\n"
  "From: \n"
  "Notes: none\n"
  "Updates:\n"
  "	20100916 - documented and cleaned - marianne.case@uci.edu\n"
  " ENDCOMMENT\n"
  "\n"
  "\n"
  "VERBATIM\n"
  "#include <stdlib.h> \n"
  "/* 	Include this library so that the following (innocuous) warning does not appear:\n"
  "		In function '_thread_cleanup':\n"
  "		warning: incompatible implicit declaration of built-in function 'free'  */\n"
  "ENDVERBATIM\n"
  "\n"
  "UNITS {\n"
  "	(mA) =(milliamp)\n"
  "	(mV) =(millivolt)\n"
  "	(uF) = (microfarad)\n"
  "	(molar) = (1/liter)\n"
  "	(nA) = (nanoamp)\n"
  "	(mM) = (millimolar)\n"
  "	(um) = (micron)\n"
  "	FARADAY = 96520 (coul)\n"
  "	R = 8.3134	(joule/degC)\n"
  "}\n"
  " \n"
  "NEURON { \n"
  "	SUFFIX ch_NavPVBC \n"
  "	USEION na READ ena WRITE ina VALENCE 1\n"
  "	RANGE g, gmax, minf, mtau, hinf, htau, ina, m, h\n"
  "	RANGE myi, vshift\n"
  "	THREADSAFE\n"
  "}\n"
  " \n"
  "PARAMETER {\n"
  "	ena  (mV)\n"
  "	gmax (mho/cm2)  \n"
  "	vshift (mV)\n"
  "}\n"
  " \n"
  "STATE {\n"
  "	m h\n"
  "}\n"
  " \n"
  "ASSIGNED {\n"
  "	v (mV) \n"
  "	celsius (degC) : temperature - set in hoc; default is 6.3\n"
  "	dt (ms) \n"
  "\n"
  "	g (mho/cm2)\n"
  "	ina (mA/cm2)\n"
  "	minf\n"
  "	hinf\n"
  "	mtau (ms)\n"
  "	htau (ms)\n"
  "	mexp\n"
  "	hexp \n"
  "	myi (mA/cm2)\n"
  "} \n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE states\n"
  "	g = gmax*m*m*m*h  \n"
  "	ina = g*(v - ena)\n"
  "	myi = ina\n"
  "}\n"
  " \n"
  "UNITSOFF\n"
  " \n"
  "INITIAL {\n"
  "	trates(v)\n"
  "	m = minf\n"
  "	h = hinf\n"
  "}\n"
  "\n"
  "PROCEDURE states() {	:Computes state variables m, h, and n \n"
  "	trates(v)			:      at the current v and dt.\n"
  "	m = m + mexp*(minf-m)\n"
  "	h = h + hexp*(hinf-h)\n"
  "}\n"
  " \n"
  "LOCAL q10	: declare outside a block so available to whole mechanism\n"
  "PROCEDURE rates(v) {  :Computes rate and other constants at current v.\n"
  "                      :Call once from HOC to initialize inf at resting v.\n"
  "	LOCAL  alpha, beta, sum	: only available to block; must be first line in block\n"
  "\n"
  "	q10 = 3^((celsius - 34)/10) : but were the parameters obtained in the paper gotten at 6.3 celsius, or did they just choose this b/c of the NEURON default?\n"
  "\n"
  "	:\"m\" sodium activation system - act and inact cross at -40\n"
  "	alpha = -0.3*vtrap((v+60-17+vshift),-5)\n"
  "	beta = 0.3*vtrap((v+60-45+vshift),5)\n"
  "	sum = alpha+beta        \n"
  "	mtau = 1/sum \n"
  "	minf = alpha/sum\n"
  "	\n"
  "	:\"h\" sodium inactivation system\n"
  "	alpha = 0.23/exp((v+60+5+vshift)/20)\n"
  "	beta = 3.33/(1+exp((v+60-47.5+vshift)/-10))\n"
  "	sum = alpha+beta\n"
  "	htau = 1/sum \n"
  "	hinf = alpha/sum 	\n"
  "}\n"
  " \n"
  "PROCEDURE trates(v) {  :Computes rate and other constants at current v.\n"
  "                      :Call once from HOC to initialize inf at resting v.\n"
  "	LOCAL tinc	: only available to block; must be first line in block\n"
  "	TABLE minf, mexp, hinf, hexp, mtau, htau\n"
  "	DEPEND dt, celsius FROM -100 TO 100 WITH 200\n"
  "                                   \n"
  "	rates(v)	: not consistently executed from here if usetable_hh == 1\n"
  "				: so don't expect the tau values to be tracking along with\n"
  "				: the inf values in hoc\n"
  "\n"
  "	tinc = -dt * q10\n"
  "\n"
  "	mexp = 1 - exp(tinc/mtau)\n"
  "	hexp = 1 - exp(tinc/htau)\n"
  " }\n"
  " \n"
  "FUNCTION vtrap(x,y) {  :Traps for 0 in denominator of rate eqns.\n"
  "	if (fabs(x/y) < 1e-6) {\n"
  "		vtrap = y*(1 - x/y/2)\n"
  "	}else{  \n"
  "		vtrap = x/(exp(x/y) - 1)\n"
  "	}\n"
  "}\n"
  " \n"
  "UNITSON\n"
  "\n"
  ;
#endif

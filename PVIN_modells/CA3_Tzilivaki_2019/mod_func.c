#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _cadynin_reg();
extern void _cal_reg();
extern void _can_reg();
extern void _cat_reg();
extern void _hin_reg();
extern void _iksin_reg();
extern void _kadistin_reg();
extern void _kaproxin_reg();
extern void _kcain_reg();
extern void _kctin_reg();
extern void _kdrin_reg();
extern void _nafx_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," cadynin.mod");
fprintf(stderr," cal.mod");
fprintf(stderr," can.mod");
fprintf(stderr," cat.mod");
fprintf(stderr," hin.mod");
fprintf(stderr," iksin.mod");
fprintf(stderr," kadistin.mod");
fprintf(stderr," kaproxin.mod");
fprintf(stderr," kcain.mod");
fprintf(stderr," kctin.mod");
fprintf(stderr," kdrin.mod");
fprintf(stderr," nafx.mod");
fprintf(stderr, "\n");
    }
_cadynin_reg();
_cal_reg();
_can_reg();
_cat_reg();
_hin_reg();
_iksin_reg();
_kadistin_reg();
_kaproxin_reg();
_kcain_reg();
_kctin_reg();
_kdrin_reg();
_nafx_reg();
}

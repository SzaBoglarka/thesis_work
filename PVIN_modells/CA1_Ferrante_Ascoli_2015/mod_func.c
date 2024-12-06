#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _distr_reg();
extern void _h_reg();
extern void _kadist_reg();
extern void _kaprox_reg();
extern void _kdrca1_reg();
extern void _na3n_reg();
extern void _naxn_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," distr.mod");
fprintf(stderr," h.mod");
fprintf(stderr," kadist.mod");
fprintf(stderr," kaprox.mod");
fprintf(stderr," kdrca1.mod");
fprintf(stderr," na3n.mod");
fprintf(stderr," naxn.mod");
fprintf(stderr, "\n");
    }
_distr_reg();
_h_reg();
_kadist_reg();
_kaprox_reg();
_kdrca1_reg();
_na3n_reg();
_naxn_reg();
}

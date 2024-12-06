#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _LcaMig_reg();
extern void _bgka_reg();
extern void _cagk_reg();
extern void _cal_reg();
extern void _ccanl_reg();
extern void _gskch_reg();
extern void _ichan2_reg();
extern void _kca_reg();
extern void _nca_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," LcaMig.mod");
fprintf(stderr," bgka.mod");
fprintf(stderr," cagk.mod");
fprintf(stderr," cal.mod");
fprintf(stderr," ccanl.mod");
fprintf(stderr," gskch.mod");
fprintf(stderr," ichan2.mod");
fprintf(stderr," kca.mod");
fprintf(stderr," nca.mod");
fprintf(stderr, "\n");
    }
_LcaMig_reg();
_bgka_reg();
_cagk_reg();
_cal_reg();
_ccanl_reg();
_gskch_reg();
_ichan2_reg();
_kca_reg();
_nca_reg();
}

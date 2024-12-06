#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _CaT4_reg();
extern void _HH2_reg();
extern void _LeakConductance_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," CaT4.mod");
fprintf(stderr," HH2.mod");
fprintf(stderr," LeakConductance.mod");
fprintf(stderr, "\n");
    }
_CaT4_reg();
_HH2_reg();
_LeakConductance_reg();
}

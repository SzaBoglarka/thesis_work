#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _HCN1_reg();
extern void _kdrbwb_reg();
extern void _nafbwb_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," HCN1.mod");
fprintf(stderr," kdrbwb.mod");
fprintf(stderr," nafbwb.mod");
fprintf(stderr, "\n");
    }
_HCN1_reg();
_kdrbwb_reg();
_nafbwb_reg();
}

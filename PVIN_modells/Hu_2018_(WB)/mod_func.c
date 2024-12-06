#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _hhBC_reg();
extern void _locus_reg();
extern void _syn2_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," hhBC.mod");
fprintf(stderr," locus.mod");
fprintf(stderr," syn2.mod");
fprintf(stderr, "\n");
    }
_hhBC_reg();
_locus_reg();
_syn2_reg();
}

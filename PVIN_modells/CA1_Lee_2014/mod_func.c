#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _ch_CavL_reg();
extern void _ch_CavN_reg();
extern void _ch_KCaS_reg();
extern void _ch_Kdrfast_reg();
extern void _ch_KvA_reg();
extern void _ch_KvCaB_reg();
extern void _ch_NavPVBC_reg();
extern void _ch_leak_reg();
extern void _iconc_Ca_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," ch_CavL.mod");
fprintf(stderr," ch_CavN.mod");
fprintf(stderr," ch_KCaS.mod");
fprintf(stderr," ch_Kdrfast.mod");
fprintf(stderr," ch_KvA.mod");
fprintf(stderr," ch_KvCaB.mod");
fprintf(stderr," ch_NavPVBC.mod");
fprintf(stderr," ch_leak.mod");
fprintf(stderr," iconc_Ca.mod");
fprintf(stderr, "\n");
    }
_ch_CavL_reg();
_ch_CavN_reg();
_ch_KCaS_reg();
_ch_Kdrfast_reg();
_ch_KvA_reg();
_ch_KvCaB_reg();
_ch_NavPVBC_reg();
_ch_leak_reg();
_iconc_Ca_reg();
}

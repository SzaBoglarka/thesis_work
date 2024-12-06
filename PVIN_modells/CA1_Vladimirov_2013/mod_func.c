#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _KdrTraub1994ax_reg();
extern void _KdrTraub1994sd_reg();
extern void _NafTraub1994ax_reg();
extern void _NafTraub1994sd_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," KdrTraub1994ax.mod");
fprintf(stderr," KdrTraub1994sd.mod");
fprintf(stderr," NafTraub1994ax.mod");
fprintf(stderr," NafTraub1994sd.mod");
fprintf(stderr, "\n");
    }
_KdrTraub1994ax_reg();
_KdrTraub1994sd_reg();
_NafTraub1994ax_reg();
_NafTraub1994sd_reg();
}

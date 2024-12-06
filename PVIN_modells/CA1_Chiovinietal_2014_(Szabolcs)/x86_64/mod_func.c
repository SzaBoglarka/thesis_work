#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _CaT4_reg(void);
extern void _HH2_reg(void);
extern void _LeakConductance_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"CaT4.mod\"");
    fprintf(stderr," \"HH2.mod\"");
    fprintf(stderr," \"LeakConductance.mod\"");
    fprintf(stderr, "\n");
  }
  _CaT4_reg();
  _HH2_reg();
  _LeakConductance_reg();
}

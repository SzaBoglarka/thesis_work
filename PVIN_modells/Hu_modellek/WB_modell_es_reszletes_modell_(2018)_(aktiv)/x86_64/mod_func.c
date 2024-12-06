#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _hhBC_reg(void);
extern void _locus_reg(void);
extern void _syn2_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"hhBC.mod\"");
    fprintf(stderr," \"locus.mod\"");
    fprintf(stderr," \"syn2.mod\"");
    fprintf(stderr, "\n");
  }
  _hhBC_reg();
  _locus_reg();
  _syn2_reg();
}

#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _kdrbwb_reg(void);
extern void _nafbwb_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"kdrbwb.mod\"");
    fprintf(stderr," \"nafbwb.mod\"");
    fprintf(stderr, "\n");
  }
  _kdrbwb_reg();
  _nafbwb_reg();
}

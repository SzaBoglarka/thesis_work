#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _bgka_reg(void);
extern void _cagk2_reg(void);
extern void _cal_reg(void);
extern void _ccanl_reg(void);
extern void _gskch_reg(void);
extern void _ichan2_reg(void);
extern void _LcaMig_reg(void);
extern void _nca_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"bgka.mod\"");
    fprintf(stderr," \"cagk2.mod\"");
    fprintf(stderr," \"cal.mod\"");
    fprintf(stderr," \"ccanl.mod\"");
    fprintf(stderr," \"gskch.mod\"");
    fprintf(stderr," \"ichan2.mod\"");
    fprintf(stderr," \"LcaMig.mod\"");
    fprintf(stderr," \"nca.mod\"");
    fprintf(stderr, "\n");
  }
  _bgka_reg();
  _cagk2_reg();
  _cal_reg();
  _ccanl_reg();
  _gskch_reg();
  _ichan2_reg();
  _LcaMig_reg();
  _nca_reg();
}

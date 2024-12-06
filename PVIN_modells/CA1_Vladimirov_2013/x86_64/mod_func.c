#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _KdrTraub1994ax_reg(void);
extern void _KdrTraub1994sd_reg(void);
extern void _NafTraub1994ax_reg(void);
extern void _NafTraub1994sd_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"KdrTraub1994ax.mod\"");
    fprintf(stderr," \"KdrTraub1994sd.mod\"");
    fprintf(stderr," \"NafTraub1994ax.mod\"");
    fprintf(stderr," \"NafTraub1994sd.mod\"");
    fprintf(stderr, "\n");
  }
  _KdrTraub1994ax_reg();
  _KdrTraub1994sd_reg();
  _NafTraub1994ax_reg();
  _NafTraub1994sd_reg();
}

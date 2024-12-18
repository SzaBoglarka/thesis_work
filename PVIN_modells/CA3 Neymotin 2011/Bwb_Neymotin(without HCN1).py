#
# Basket Cell -- Bwb
#
###############################################################################

import neuron

class Bwb(Cell):
	"Basket cell"
	
	def set_morphology(self):
		total_area = 10000 # um2
		self.soma.nseg  = 1
		self.soma.cm    = 1      # uF/cm2
		diam = sqrt(total_area) # um
		L    = diam/pi  # um
			
		h.pt3dclear(sec=self.soma)
		h.pt3dadd(self.x, self.y, self.z,   diam, sec=self.soma)
		h.pt3dadd(self.x, self.y, self.z+L, diam, sec=self.soma)
			
	def set_conductances(self):
		self.soma.insert('pas')
		self.soma.e_pas = -65     # mV
		self.soma.g_pas = 0.1e-3  # S/cm2 
	  
		self.soma.insert('Nafbwb')
		self.soma.insert('Kdrbwb')




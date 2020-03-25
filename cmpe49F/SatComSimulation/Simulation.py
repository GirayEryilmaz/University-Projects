import simpy
from SatComSimulation import Formulas
import matplotlib.pyplot as plt
import sys,os
import random
import numpy as np
import time


class Simulation(object):
	servant = Formulas.Servent()
	ter_PU_count = 1
	ter_SU_count = 1
	sat_count = 1
	HU_count = 1
	pemted_HU_bases = 0
	pemted_HU_enchs = 0
	
	HU_ter = 0
	HU_sat = 0
	
	terPU_in = 0
	
	# bits delivered succesfully
	ter_PU_delivered = 0
	ter_SU_delivered = 0
	sat_PU_delivered = 0
	HU_base_delivered = 0
	HU_ench_delivered = 0
	
	"""
	crowdThreshold holds the max percentage of
	fullness for terrestrial link that a HU accepts to join
	"""
	crowdThreshold = 0
	

	
	def __init__(self, crowdThreshold=0.5, isRandom = False):
		self.crowdThreshold = crowdThreshold
		self.isRandom = isRandom
	
	def arrivalHU(self, name, env, sat, ter):

		yield env.timeout(Formulas.HU_nextArrival())
		#print('%s arrived at %f' % (name, env.now))
		# algorithm goes here to deceide to decide which link to use ter or sat
		
		chunkSizeBase = self.servant.getChunkSize(isBase=True)
		chunkSizeEnch = self.servant.getChunkSize(isBase=False)
		if not self.isRandom:


			# if ter.count / ter.capacity < self.crowdThreshold:
			# 	env.process(self.HU(name + '_onTer', env, sat, 'ter', 'base',chunkSizeBase))
			# el
			
			if chunkSizeBase < 18000000:
				env.process(self.HU(name + '_onTer', env, sat, 'ter', 'base', chunkSizeBase))
			else:
				env.process(self.HU(name + '_onSat', env, sat, 'sat', 'base', chunkSizeBase))
				
			if chunkSizeEnch < 3000000:
				env.process(self.HU(name + '_onTer', env, ter, 'ter', 'ench',chunkSizeEnch))
			else:
				env.process(self.HU(name + '_onSat', env, sat, 'sat', 'ench',chunkSizeEnch))
			
		else:
			
			if random.choice([True, False]):
				env.process(self.HU(name + '_onTer', env, ter, 'ter', 'base', chunkSizeBase))
			else:
				env.process(self.HU(name + '_onSat', env, sat, 'sat', 'base', chunkSizeBase))
			
			if random.choice([True, False]):
				env.process(self.HU(name + '_onTer', env, ter, 'ter', 'ench',chunkSizeEnch))
			else:
				env.process(self.HU(name + '_onSat', env, sat, 'sat', 'ench',chunkSizeEnch))
			
			

				#env.process(self.HU(name + '_onSat_ench', env, sat, 'sat', 'ench'))
				

		
		self.HU_count += 1
		env.process(self.arrivalHU('HU_' + str(self.HU_count), env, sat, ter))
	
	def arrivalSat(self, name, env, sat):
		
		yield env.timeout(Formulas.satalite_nextArrival())
		#print('%s arrived at %f' % (name, env.now))
		env.process(self.satPU(name, env, sat))
		self.sat_count += 1
		env.process(self.arrivalSat('sat_' + str(self.sat_count), env, sat))
	
	def arrivalTerPU(self, name, env, ter):
		yield env.timeout(Formulas.terrestrialPU_nextArrival())
		#print('%s arrived at %f' % (name, env.now))
		env.process(self.terrestrialPU(name, env, ter))
		self.ter_PU_count += 1
		env.process(self.arrivalTerPU('terPU_' + str(self.ter_PU_count), env, ter))
	
	def arrivalTerSU(self, name, env, ter):
		yield env.timeout(Formulas.terrestrialSU_nextArrival())
		#print('%s arrived at %f' % (name, env.now))
		env.process(self.terrestrialSU(name, env, ter))
		self.ter_SU_count += 1
		env.process(self.arrivalTerSU('terSU_' + str(self.ter_SU_count), env, ter))
	
	def HU(self, name, env, link, link_type, base_ench,chunkSize):
		
		if base_ench == 'base':
			if (link_type == 'ter'):
				with link.request(priority=2) as req:
					try:
						#print('%s requesting at %f' % (name, env.now))
						yield req
						#print('%s got resource at %f' % (name, env.now))
						
						chunkSize, servDur = self.servant.calcServDur(link_type, base_ench,chunkSize)
						yield env.timeout(servDur)
						
						#print('%s done at %f' % (name, env.now))
						self.HU_base_delivered += chunkSize
					except simpy.Interrupt:
						#print('%s got preempted at %f' % (name, env.now))
						self.pemted_HU_bases += 1
						req.cancel()
			
			elif (link_type == 'sat'):
				with link.request(priority=1) as req:
					#print('%s requesting at %f' % (name, env.now))
					yield req
					#print('%s got resource at %f' % (name, env.now))
					
					chunkSize, servDur = self.servant.calcServDur(link_type, base_ench,chunkSize)
					yield env.timeout(servDur)
					
					#print('%s done at %f' % (name, env.now))
					self.HU_base_delivered += chunkSize
		
		elif base_ench == 'ench':
			if (link_type == 'ter'):
				with link.request(priority=2) as req:
					try:
						#print('%s requesting at %f' % (name, env.now))
						yield req
						#print('%s got resource at %f' % (name, env.now))
						chunkSize, servDur = self.servant.calcServDur(link_type, base_ench,chunkSize)
						yield env.timeout(servDur)
						#print('%s done at %f' % (name, env.now))
						self.HU_ench_delivered += chunkSize
					except simpy.Interrupt:
						#print('%s got preempted at %f' % (name, env.now))
						self.pemted_HU_enchs += 1
						req.cancel()
			
			
			elif (link_type == 'sat'):
				with link.request(priority=1) as req:
					try:
						#print('%s requesting at %f' % (name, env.now))
						yield req
						#print('%s got resource at %f' % (name, env.now))
						chunkSize, servDur = self.servant.calcServDur(link_type, base_ench,chunkSize)
						yield env.timeout(servDur)
						#print('%s done at %f' % (name, env.now))
						self.HU_ench_delivered += chunkSize
					except simpy.Interrupt:
						#print('%s got preempted at %f' % (name, env.now))
						self.pemted_HU_enchs += 1
						req.cancel()
	
	def satPU(self, name, env, satLink):
		with satLink.request(priority=1) as req:
			#print('%s requesting at %f' % (name, env.now))
			yield req
			#print('%s got resource at %f' % (name, env.now))
			
			chunkSize, servDur = self.servant.servDur('sat', 'base')
			yield env.timeout(servDur)
			#print('%s done at %f' % (name, env.now))
			self.sat_PU_delivered += chunkSize
	
	def terrestrialSU(self, name, env, terLink, prio=2):
		with terLink.request(priority=prio) as req:
			try:
				#print('%s requesting at %f' % (name, env.now))
				yield req
				#print('%s got resource at %f' % (name, env.now))
				
				chunkSize, servDur = self.servant.servDur('ter', 'base')
				yield env.timeout(servDur)
				#print('%s done at %f' % (name, env.now))
				
				self.ter_SU_delivered += chunkSize
			
			except simpy.Interrupt:
				#print('%s got preempted at %f' % (name, env.now))
				req.cancel()
	
	def terrestrialPU(self, name, env, terLink, prio=1):
		with terLink.request(priority=prio) as req:
		
			#print('%s requesting at %f' % (name, env.now))
			yield req
			#print('%s got resource at %f' % (name, env.now))
			self.terPU_in += 1
			
			chunkSize, servDur = self.servant.servDur('ter', 'base')
			yield env.timeout(servDur)
			#print('%s done at %f' % (name, env.now))
			self.terPU_in -= 1
			
			self.ter_PU_delivered += chunkSize

	
	def run(self, until=100):
		
		env = simpy.Environment()
		
		terLink = simpy.PreemptiveResource(env, capacity=Formulas.N_f_ter)  # Formulas.N_f_ter
		satLink = simpy.PreemptiveResource(env, capacity=Formulas.N_f_sat)  # Formulas.N_f_sat
		
		env.process(self.arrivalTerPU('terPU_1', env, terLink))
		env.process(self.arrivalTerSU('terSU_1', env, terLink))
		env.process(self.arrivalSat('sat_1', env, satLink))
		env.process(self.arrivalHU('HU_1', env, satLink, terLink))
		
		env.run(until=until)
		
		#print('\n')
		#print("%d, HU base chunks received; %d preempted" % (self.HU_count - self.pemted_HU_bases, self.pemted_HU_bases))
		#print("%d, HU ench chunks received; %d preempted" % (self.HU_count - self.pemted_HU_enchs, self.pemted_HU_enchs))
		
		# tPU = Formulas.formatBits(self.ter_PU_delivered)
		# tSU = Formulas.formatBits(self.ter_SU_delivered)
		# sPU = Formulas.formatBits(self.sat_PU_delivered)
		# HU_bs = Formulas.formatBits(self.HU_base_delivered)
		# HU_ench = Formulas.formatBits(self.HU_ench_delivered)
		# s="ter_PU_dlvrd: %s,\nter_SU_dlvrd: %s,\nsat_dlvrd: %s,\nHU_base_dlvrd: %s,\nHU_ench_dlvrd: %s ."
		#print(s % (tPU, tSU, sPU, HU_bs ,HU_ench))
		
		HU_baseChunk_throughput = self.HU_base_delivered / 1024 / until
		HU_enchChunk_throughput = self.HU_ench_delivered / 1024 / until
		
		#print(HU_baseChunk_throughput)
		#print(HU_enchChunk_throughput)
		
		totBits = (self.ter_SU_delivered + self.ter_PU_delivered + self.HU_base_delivered + self.sat_PU_delivered)

		return HU_baseChunk_throughput, HU_enchChunk_throughput , totBits / 1024 / until



def multiple(repeats = 100, until= 100,isRandom = False):
	
	
	HUbaseThPuts = []
	HUenchThPuts = []
	totalTPs = []
	for i in range(repeats):
		baseThPut, enchThPut, totalTP = Simulation(isRandom = isRandom).run(until=until)
		HUbaseThPuts.append(baseThPut)
		HUenchThPuts.append(enchThPut)
		totalTPs.append(totalTP)
	
	# t = [i / repeats for i in range(repeats)]
	#
	# plt.plot(t, totalTPs)
	#
	# plt.xlabel('threshold')
	# plt.ylabel('throughput')
	# plt.title('total')
	# plt.grid(True)
	# plt.savefig("total_random.png")
	# plt.show()
	#
	# plt.plot(t, HUbaseThPuts)
	#
	# plt.xlabel('threshold')
	# plt.ylabel('throughput')
	# plt.title('HU base chunks')
	# plt.grid(True)
	# plt.savefig("baseHU_random.png")
	# plt.show()
	#
	# plt.plot(t, HUenchThPuts)
	#
	# plt.xlabel('threshold')
	# plt.ylabel('throughput')
	# plt.title('HU ench chunks')
	# plt.grid(True)
	# plt.savefig("enchHU_random.png")
	# plt.show()
	
	return sum(HUbaseThPuts)/repeats , sum(HUenchThPuts)/repeats , sum(totalTPs)/repeats

def once():
	baseThPut, enchThPut, totalTP = Simulation().run()
	
def demo():
	
	seed = int(round(time.time() * 1000))
	
	repeats = 100
	until = 1000
	random.seed(seed)
	tpBase, tpEnch ,tpTotal= multiple(repeats=repeats, until=until)
	
	random.seed(seed)
	tpBaseRand, tpEnchRand , tpTotalRand= multiple(repeats=repeats, until=until, isRandom=True)
	
	# data to plot
	n_groups = 3
	myTPs = (tpBase, tpEnch,tpBase + tpEnch)
	randomTPs = (tpBaseRand, tpEnchRand, tpBaseRand + tpEnchRand)
	
	print("bases " + str(tpBase/(tpBaseRand+0.000000001)))
	print("enchs " + str(tpEnch/(tpEnchRand+0.000000001)))
	print("totals " + str(tpTotal/(tpTotalRand+0.000000001)))
	
	# create plot
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.35
	opacity = 0.8
	
	rects1 = plt.bar(index, myTPs, bar_width,
	                 alpha=opacity,
	                 color='b',
	                 label='Mine')
	
	rects2 = plt.bar(index + bar_width, randomTPs, bar_width,
	                 alpha=opacity,
	                 color='g',
	                 label='Random')
	

	
	plt.xlabel('Techniques')
	plt.ylabel('Throughputs(KBps)')
	plt.title('Throughput by Techniques')
	plt.xticks(index + 2*bar_width, ('Bases', 'Enchs'))
	plt.legend()
	
	plt.tight_layout()
	
	
	i = 0
	filename = 'output'
	while True:
		i += 1
		newname = '{}{:d}.png'.format(filename, i)
		if os.path.exists(newname):
			continue
		plt.savefig(newname)
		break

	plt.show()


if __name__ == '__main__':
	for i in range(10):
		demo()
	


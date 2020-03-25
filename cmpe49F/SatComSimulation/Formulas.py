import math
import random
from SatComSimulation import Zipf

print('hi')




"""
this file shall contain provided parameters
ONLY IN STANDAT FORMAT

Hz, meters, seconds etc and not MHz or kilometers

"""

numberOfDistinctContents = 100

"""FROM TABLE I : NETWORK PARAMETERS"""
N_f_sat = 5  # Total number of satellite bands

N_f_ter = 10  # Total number of terrestrial bands

lambda_sat_PU = 0.15  # user/sec #Arrival rate of PUs at satellite link

lambda_ter_PU = 0.8  # user/sec #Arrival rate of PUs at terrestrial link

lambda_ter_SU = 0.5  # user/sec #Arrival rate of SUs at terrestrial link

λ_HU = 0.3  # user/sec #Arrival rate of HUs at the system

W_sat = 36 * (10 ** 6)  # Hz #Bandwidth of satellite link

W_ter = 2 * (10 ** 6)  # Hz #Bandwidth of terrestrial link

f_sat = 20 * (10 ** 9)  # Hz #Frequency of satellite link

f_ter = 700 * (10 ** 6)  # Hz #Frequency of terrestrial link

"""TABLE II : RECEIVED POWER STRENGTH PARAMETERS"""

# f_sat = 20 * (10**9) #Hz #Frequency of satellite link

# f_ter = 700 * (10**6) #Hz #Frequency of terrestrial link

G_sat = 2.5 * (10 ** 4)  # Gain of the satellite

G_BS = 4 * (10 ** -5)  # Gain of the base station

G_dev_HU = 6 * (10 ** -2)  # Gain of a hybrid user

G_dev_PU_ter = 11 * (10 ** -2)  # Gain of a primary user requesting service at terrestrial link

G_dev_SU_ter = 6 * (10 ** -2)  # ??????

R_BS = 300  # The radius of the BS

d_sat_LEO = 300 * 1000  # Distance from satellite to earth

d_BS = 150  # The distance between any user (PU,SU,HU) and the BS

P_total_sat = 240  # Total transmission power of the satellite

P_total_BS = 60  # Total transmission power of the BS

P_ch_sat = P_total_sat / N_f_sat  # Per channel transmission power of the satellite

P_ch_BS = P_total_BS / N_f_ter  # Per channel transmission power of the BS

"""TABLE III : CAPACITY PARAMETERS"""

# W_sat = 36 * 10**6 #Hz #Bandwidth of satellite link

# W_ter = 2 * 10**6 #Hz #Bandwidth of terrestrial link

Noise_sat = (10 ** (-18))  # Watt/Hz Noise at satellite link

Noise_ter = 1.5 * (10 ** (-19))  # Watt/Hz Noise at terrestrial link

"""TABLE IV : CONTENT PARAMETERS"""

base_chunk_size_HU = 25 * (10 ** 6)  # bits Mean base content chunk size requested by an HU

enhancement_chunk_size_HU = 5 * (10 ** 6)  # bits Mean enhancement content chunk size requested by an HU

base_chunk_size_nonHybrid = 25 * (10 ** 6)  # bits Mean base content size requested  by a nonhybrid user

# base_chunk_size_PU_sat = 5 * (10 ** 6)  # bits Mean base content size requested by a PU at satellite link

# base_chunk_size_PU_ter = 5 * (10 ** 6)  # bits Mean base content size requested by a PU at terrestrial link

# base_chunk_size_SU_ter = 5 * (10 ** 6)  # bits Mean base content size requested by a SU at terrestrial link

r_enh = 1  # The ratio of HUs that request both base and enhancement content chunks (ratio of high quality consumers)

pi = math.pi
C = speed_of_light = 299792458  # meters/sec


def calcChunkSize(lamda=1 / (25 * (10 ** 6))):
	return random.expovariate(lambd=lamda)

zf = Zipf.Zipf()
baseChunks = [calcChunkSize() for i in range(100)]
enchChunks = [calcChunkSize(lamda=1 / (5 * (10 ** 6))) for i in range(100)]
popularities = zf.getZipf()

chunkPairsWeighted = []
for i in range(100):
	b = baseChunks[i]
	e = enchChunks[i]
	p = popularities[i]
	chunkPairsWeighted.extend([[b, e]] * p)

def log2(x):
	return math.log(x, 2)


def receivedPowerStrength(initlialPower, GainOfStation, GainOfUser, freq, dist, c=C):
	return (initlialPower * GainOfStation * GainOfUser * (c ** 2)) / ((4 * pi * freq * dist) ** 2)


def calculateCapacity(bandWidth, power, noise):
	return bandWidth * log2(1 + (power / (noise * bandWidth)))


def calculateServiceDuration(chunkSize, channelCapacity):
	return chunkSize / channelCapacity





class Servent:
	def __init__(self):
		zf = Zipf.Zipf()
		self.baseChunks =   baseChunks
		self.enchChunks =   enchChunks
		self.popularities = popularities
		
		
		self.chunkPairsWeighted = chunkPairsWeighted

		
		# print(self.chunkPairsWeighted)
		# print(random.sample(self.chunkPairsWeighted,5))
	
	def getChunkSize(self,isBase):
		if isBase:
			return random.choice(self.chunkPairsWeighted)[0]
		else:
			return random.choice(self.chunkPairsWeighted)[1]
	
	def calcServDur(self, sat_ter, base_Ench, currChunkSize):
		
		if sat_ter == 'ter' and base_Ench == 'base':
			# currChunkSize = self.getChunkSize(isBase=True)
			temp = currChunkSize, calculateServiceDuration(currChunkSize,
			                                               calculateCapacity(bandWidth=W_ter,
			                                                                 power=receivedPowerStrength(P_ch_BS, G_BS,
			                                                                                             G_dev_PU_ter,
			                                                                                             f_ter,
			                                                                                             d_BS),
			                                                                 noise=Noise_ter))
			return temp
		
		elif sat_ter == 'ter' and base_Ench == 'ench':
			# currChunkSize = self.getChunkSize(isBase=False)
			temp = currChunkSize, calculateServiceDuration(currChunkSize,
			                                               calculateCapacity(bandWidth=W_ter,
			                                                                 power=receivedPowerStrength(P_ch_BS, G_BS,
			                                                                                             G_dev_PU_ter,
			                                                                                             f_ter,
			                                                                                             d_BS),
			                                                                 noise=Noise_ter))
			return temp
		elif sat_ter == 'sat' and base_Ench == 'base':
			# currChunkSize = self.getChunkSize(isBase=True)
			temp = currChunkSize, calculateServiceDuration(currChunkSize,
			                                               calculateCapacity(bandWidth=W_sat,
			                                                                 power=receivedPowerStrength(P_ch_sat,
			                                                                                             G_sat,
			                                                                                             G_dev_PU_ter,
			                                                                                             f_sat,
			                                                                                             d_sat_LEO),
			                                                                 noise=Noise_sat))
			return temp
		elif sat_ter == 'sat' and base_Ench == 'ench':
			# currChunkSize = self.getChunkSize(isBase=False)  # self.getChunkSize(lamda=1/(5 * (10 ** 6)))
			temp = currChunkSize, calculateServiceDuration(currChunkSize,
			                                               calculateCapacity(bandWidth=W_sat,
			                                                                 power=receivedPowerStrength(P_ch_sat,
			                                                                                             G_sat,
			                                                                                             G_dev_PU_ter,
			                                                                                             f_sat,
			                                                                                             d_sat_LEO),
			                                                                 noise=Noise_sat))
			return temp
		else:
			raise Exception(
				'Wrong string arguments provided!\nbase_Ench = [\'base\' | \'ench\']\nsat_ter = [\'ter\' | \'sat\']')
	
	def servDur(self, sat_ter, base_Ench):
		
		if sat_ter == 'ter' and base_Ench == 'base':
			currChunkSize = self.getChunkSize(isBase=True)
			temp =  currChunkSize, calculateServiceDuration(currChunkSize,
			                                               calculateCapacity(bandWidth=W_ter,
			                                                                 power=receivedPowerStrength(P_ch_BS, G_BS,
			                                                                                             G_dev_PU_ter,
			                                                                                             f_ter,
			                                                                                             d_BS),
			                                                                 noise=Noise_ter))
			return temp
		
		elif sat_ter == 'ter' and base_Ench == 'ench':
			currChunkSize = self.getChunkSize(isBase=False)
			temp = currChunkSize, calculateServiceDuration(currChunkSize,
			                                               calculateCapacity(bandWidth=W_ter,
			                                                                 power=receivedPowerStrength(P_ch_BS, G_BS,
			                                                                                             G_dev_PU_ter,
			                                                                                             f_ter,
			                                                                                             d_BS),
			                                                                 noise=Noise_ter))
			return temp
		elif sat_ter == 'sat' and base_Ench == 'base':
			currChunkSize = self.getChunkSize(isBase=True)
			temp = currChunkSize, calculateServiceDuration(currChunkSize,
			                                               calculateCapacity(bandWidth=W_sat,
			                                                                 power=receivedPowerStrength(P_ch_sat,
			                                                                                             G_sat,
			                                                                                             G_dev_PU_ter,
			                                                                                             f_sat,
			                                                                                             d_sat_LEO),
			                                                                 noise=Noise_sat))
			return temp
		elif sat_ter == 'sat' and base_Ench == 'ench':
			currChunkSize = self.getChunkSize(isBase=False)  # self.getChunkSize(lamda=1/(5 * (10 ** 6)))
			temp =  currChunkSize, calculateServiceDuration(currChunkSize,
			                                               calculateCapacity(bandWidth=W_sat,
			                                                                 power=receivedPowerStrength(P_ch_sat,
			                                                                                             G_sat,
			                                                                                             G_dev_PU_ter,
			                                                                                             f_sat,
			                                                                                             d_sat_LEO),
			                                                                 noise=Noise_sat))
			return temp
		else:
			raise Exception(
				'Wrong string arguments provided!\nbase_Ench = [\'base\' | \'ench\']\nsat_ter = [\'ter\' | \'sat\']')
	




# mean arrival times

def terrestrialPU_nextArrival(lamda=lambda_ter_PU):
	return random.expovariate(lambd=lamda)


def terrestrialSU_nextArrival(lamda=lambda_ter_SU):
	return random.expovariate(lambd=lamda)


def satalite_nextArrival(lamda=lambda_sat_PU):
	return random.expovariate(lambd=lamda)


def HU_nextArrival(lamda=λ_HU):
	return random.expovariate(lambd=lamda)


def formatBits(bits):
	Bytes = bits // 8
	leftBytes = Bytes % 1024
	# leftBits = bits % 8
	GBs = Bytes // (1024 * 1024)
	MBs = Bytes % 1024
	return "%d GBs, %d MBs, %d Bytes" % (GBs, MBs, leftBytes)



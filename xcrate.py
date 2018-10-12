import configparser
import time
import urllib.request 
import json


class XChange(object):
	"""Class build request URL and get the exchange rate"""
	def __init__(self, configFileName='cem_config.ini'):
		"""Initialises the class and retrieves the current exchange rate

		configFileName -- config file with related parameters
		"""
		super(XChange, self).__init__()

		#configure the parser
		self.configObject = configparser.ConfigParser()
		self.configObject.read(configFileName)
		#build the URL from parameters from config file
		self.reqURL = self.configObject['XCRES']['targetURL'] + \
			"?access_key=" + self.configObject['XCRES']['accessKey'] +\
			"&base=" + self.configObject['XCRES']['baseCurr'] +\
			"&symbols=" + self.configObject['XCRES']['targetCurr']
		#set the debug flag
		self.debug = self.configObject['XCRES']['debug']
		if self.debug == 'False':	
			#Retrive current exchange rate from built URL
			with urllib.request.urlopen(self.reqURL) as url:
				data = json.loads(url.read().decode())
				self.currXCRate = data['rates']['INR']
				self.lastURLCall = data['timestamp']
		else:
			#When debug, set default exchange rate
			self.currXCRate = float(self.configObject['XCRES']['defaultXCRate'])
			self.lastURLCall = time.time()


	def getURL(self):
		"""Returns the built URL for Exchange Rate"""
		return self.reqURL

	def getCurrXCRate(self):
		"""Returns the retrieved current exchange rate"""
		return self.currXCRate

	def refreshXCRate(self):
		"""Refresh the current exchange rate at least every 1 hour"""
		t_interval = time.time() - self.lastURLCall
		if (t_interval > (24*60*60)):
			#If the last call is not within the last 24 hours
			if self.debug == 'False':
				#Retrive current exchange rate from built URL
				with urllib.request.urlopen(self.reqURL) as url:
					data = json.loads(url.read().decode())
					self.currXCRate = data['rates']['INR']
					self.lastURLCall = data['timestamp']
			else:
				#When debug, set default exchange rate
				self.currXCRate = float(self.configObject['XCRES']['defaultXCRate'])
				self.lastURLCall = time.time()



class InterestRate(object):
	"""docstring for InterestRate"""
	def __init__(self, configFileName='cem_config.ini'):
		"""Initialises the class and retrieves interest rates from the config file

		configFileName -- config file with related parameters
		"""
		super(InterestRate, self).__init__()
		self.configObject = configparser.ConfigParser()
		self.configObject.read(configFileName)
		self.FDRate = self.configObject['IRATES']['fixedRate']
		self.SBRate = self.configObject['IRATES']['savingsRate']

	def getFDRate(self):
		"""Returns the FD interest rate"""
		return int(self.FDRate)

	def getSBRate(self):
		"""Returns the SB interest rate"""
		return int(self.SBRate)



if __name__ == '__main__':
	xcObject = XChange("cem_config.ini")
	iRate = InterestRate("cem_config.ini")

	print("**** START XCHANGE TEST ****")
	print("Built URL: " + xcObject.getURL())
	print("Current Exchange rate: " + str(xcObject.getCurrXCRate()))
	print("**** END XCHANGE TEST ****")
	print()
	print("**** START INTERESTRATE TEST ****")
	print("FD Interest rate: " + iRate.getFDRate())
	print("SB Interest rate: " + iRate.getSBRate())
	print("**** END INTERESTRATE TEST ****")
from xcrate import *
from datetime import date, timedelta
import matplotlib.pyplot as plt 


class FavourableCurrencyProjectionModel(object):
	"""docstring for FavourableCurrencyProjectionModel"""
	def __init__(self):
		"""Initialise the class and objects"""
		super(FavourableCurrencyProjectionModel, self).__init__()
		self.xcObject = XChange()
		self.iRateObject = InterestRate()
		self.currXCRate = self.xcObject.getCurrXCRate()
		self.FDProjection = []
		self.SBProjection = [] 
		self.dateRange = []
		
	def __buildXCRateProjection(self, noOfDays=7):
		"""Function to build the favourable exchange rate projection for the given number of days

		noOfDays -- Number of days for which the projection needs to be built
		"""
		#Today's date
		today = date.today()
		#Start projections with current exchange rate
		self.FDProjection = [self.currXCRate]
		self.SBProjection = [self.currXCRate]
		#Date list, used for plotting the projection
		self.dateRange = [today.strftime("%d/%m")]

		#Interest earned = (P*R*T)/(100*365), where
		#P = Principle (1€ in INR today)
		#R = Rate of interest (per year)
		#T = Time (in days)
		if noOfDays > 0:
			#If noOfDays is positive integer. When negative don't do anything
			for x in range(1,noOfDays):
				#Build projection as a list for every day till the last day is reached

				#date format to DD/MM
				t_date = today + timedelta(days=x)
				self.dateRange.append(t_date.strftime("%d/%m"))
				#calculate FD projection
				fd_int_earned = \
				(self.xcObject.getCurrXCRate() * self.iRateObject.getFDRate() * x) / (100 * 365)
				self.FDProjection.append(self.xcObject.getCurrXCRate() + fd_int_earned)
				#calculate SB projection
				sb_int_earned = \
				(self.xcObject.getCurrXCRate() * self.iRateObject.getSBRate() * x) / (100 * 365)
				self.SBProjection.append(self.xcObject.getCurrXCRate() + sb_int_earned)

	def __plotProjectedData(self):
		"""Function to plot the projections"""
		#set plot window size
		#figsize(11,5) defines the window size of 11x5 inches at 100 dpi
		plt.figure(num=None, figsize=(11,5), dpi=100)
		#plot the FD projection against dates
		plt.plot(self.dateRange, self.FDProjection, 
			label="FD Appreciation", marker='o')
		#plot the SB projections against dates
		plt.plot(self.dateRange, self.SBProjection, 
			label="SB Appreciation", marker='o')
		#label X-Axis
		plt.xlabel('Dates')
		#rotate X-Axis labels by 90°
		plt.xticks(rotation=90)
		#label Y-Axis
		plt.ylabel('Exchange Rate')
		#set title of the plot
		plt.title('Favourable Exchange Rate Projection')
		#set to show the legend of the plot
		plt.legend()
		#show the plot
		plt.show()

	def projectFavourableExchangeRates(self, noOfDays=7):
		"""API for getting the plot of favourable exchange rates

		noOfDays -- The number of days to show the projection for
					Defaults to next 7 days
		"""
		self.__buildXCRateProjection(noOfDays)
		self.__plotProjectedData()




if __name__ == '__main__':
	#instantiate class
	emObj = FavourableCurrencyProjectionModel()
	#call class API
	emObj.projectFavourableExchangeRates(30)
	
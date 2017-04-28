from __future__ import unicode_literals

from django.db import models


class Pricer(models.Model):
	fico = models.CharField(max_length=128)
	ltv = models.CharField(max_length=128)
	citizenship = models.CharField(max_length=128)
	seflag = models.CharField(max_length=128)
	fthbflag = models.CharField(max_length=128)
	doctype = models.CharField(max_length=128)
	dti = models.CharField(max_length=128)
	loanamount = models.CharField(max_length=128)
	purpose = models.CharField(max_length=128)
	state = models.CharField(max_length=128)
	occupancy = models.CharField(max_length=128)
	propType = models.CharField(max_length=128)
	io = models.CharField(max_length=128)
	term = models.CharField(max_length=128)
	prepay = models.CharField(max_length=128)
	reserves = models.CharField(max_length=128)
	dscr = models.CharField(max_length=128)
	x30x12 = models.IntegerField()
	x60x12 = models.IntegerField()
	x90x12 = models.IntegerField()
	x30x24 = models.IntegerField()
	x60x24 = models.IntegerField()
	x90x24 = models.IntegerField()
	monthsFC = models.IntegerField(blank = True, null = True)
	monthsSS = models.IntegerField(blank = True, null = True)
	monthsDIL = models.IntegerField(blank = True, null = True)
	monthsBK = models.IntegerField(blank = True, null = True)
	monthsBK = models.IntegerField(blank = True, null = True)
	bkChapter = models.CharField(max_length=128)
	rate = models.DecimalField(default = 0, max_digits=5, decimal_places = 3)
	eligibility = models.CharField(max_length = 128)

	def __str__(self):
		return self.rate

class BaseRate(models.Model):
	rateSheetName = models.CharField(max_length=128)
	fico = models.CharField(max_length=128)
	ltv = models.CharField(max_length=128)
	adj = models.DecimalField(default = 0, max_digits=6, decimal_places = 4)

	def __str__(self):
		return self.adj

class GradeAdj(models.Model):
	rateSheetName = models.CharField(max_length = 128)
	grade = models.CharField(max_length = 128)
	ltv = models.CharField(max_length=128)
	adj = models.DecimalField(default = 0, max_digits=5, decimal_places = 3)

	def __str__(self):
		return self.adj

class DocTypeAdj(models.Model):
	rateSheetName = models.CharField(max_length = 128)
	docType = models.CharField(max_length = 128)
	grade = models.CharField(max_length = 128)
	ltv = models.CharField(max_length=128)
	adj = models.DecimalField(default = 0, max_digits=5, decimal_places = 3)

	def __str__(self):
		return self.adj

class DTIAdj(models.Model):
	rateSheetName = models.CharField(max_length = 128)
	dti = models.CharField(max_length = 128)
	grade = models.CharField(max_length = 128)
	ltv = models.CharField(max_length=128)
	adj = models.DecimalField(default = 0, max_digits=5, decimal_places = 3)

	def __str__(self):
		return self.adj

class PurposeAdj(models.Model):
	rateSheetName = models.CharField(max_length = 128)
	purpose = models.CharField(max_length = 128)
	grade = models.CharField(max_length = 128)
	ltv = models.CharField(max_length=128)
	adj = models.DecimalField(default = 0, max_digits=5, decimal_places = 3)

	def __str__(self):
		return self.adj

class LoanBalanceAdj(models.Model):
	rateSheetName = models.CharField(max_length = 128)
	balance = models.CharField(max_length = 128)
	ltv = models.CharField(max_length=128)
	adj = models.DecimalField(default = 0, max_digits=5, decimal_places = 3)

	def __str__(self):
		return self.adj

class PropertyTypeAdj(models.Model):
	rateSheetName = models.CharField(max_length = 128)
	propertyType = models.CharField(max_length = 128)
	ltv = models.CharField(max_length=128)
	adj = models.DecimalField(default = 0, max_digits=5, decimal_places = 3)

	def __str__(self):
		return self.adj

class StateAdj(models.Model):
	rateSheetName = models.CharField(max_length = 128)
	state = models.CharField(max_length = 128)
	ltv = models.CharField(max_length=128)
	adj = models.DecimalField(default = 0, max_digits=5, decimal_places = 3)
	def __str__(self):
		return self.adj

class IOAdj(models.Model):
	rateSheetName = models.CharField(max_length = 128)
	io = models.CharField(max_length = 128)
	ltv = models.CharField(max_length=128)
	adj = models.DecimalField(default = 0, max_digits=5, decimal_places = 3)

	def __str__(self):
		return self.adj

class PrepayAdj(models.Model):
	rateSheetName = models.CharField(max_length = 128)
	prepayTerm = models.CharField(max_length = 128)
	ltv = models.CharField(max_length=128)
	adj = models.DecimalField(default = 0, max_digits=5, decimal_places = 3)

	def __str__(self):
		return self.adj

class LoanTermAdj(models.Model):
	rateSheetName = models.CharField(max_length = 128)
	loanTerm = models.CharField(max_length = 128)
	adj = models.DecimalField(default = 0, max_digits=5, decimal_places = 3)

	def __str__(self):
		return self.adj

class OccupancyAdj(models.Model):
	rateSheetName = models.CharField(max_length = 128)
	occupancy = models.CharField(max_length = 128)
	ltv = models.CharField(max_length=128)
	adj = models.DecimalField(default = 0, max_digits=5, decimal_places = 3)

	def __str__(self):
		return self.adj

class ReservesAdj(models.Model):
	rateSheetName = models.CharField(max_length = 128)
	reserves = models.CharField(max_length = 128)
	ltv = models.CharField(max_length=128)
	adj = models.DecimalField(default = 0, max_digits=5, decimal_places = 3)

	def __str__(self):
		return self.adj

class CAProductMatrix(models.Model):
	occupancy = models.CharField(max_length = 128)
	grade = models.CharField(max_length = 128)
	fico = models.CharField(max_length = 128)
	loanamount = models.CharField(max_length = 128)
	docType = models.CharField(max_length = 128)
	purpose = models.CharField(max_length = 128)
	maxLTV = models.CharField(max_length = 128)

	def __str__(self):
		return self.maxLTV

	def getFICO(self):
		return self.fico

class DTIProductMatrix(models.Model):
	grade = models.CharField(max_length = 128)
	fico = models.CharField(max_length = 128)
	loanamount = models.CharField(max_length = 128)
	docType = models.CharField(max_length = 128)
	purpose = models.CharField(max_length = 128)
	maxLTV = models.CharField(max_length = 128)

	def __str__(self):
		return self.maxLTV

class PIProductMatrix(models.Model):
	docType = models.CharField(max_length = 128)
	fico = models.CharField(max_length = 128)
	loanamount = models.CharField(max_length = 128)
	reserves = models.CharField(max_length = 128)
	purpose = models.CharField(max_length = 128)
	maxLTV = models.CharField(max_length = 128)

	def __str__(self):
		return self.maxLTV

class FNProductMatrix(models.Model):
	docType = models.CharField(max_length = 128)
	grade = models.CharField(max_length = 128)
	loanamount = models.CharField(max_length = 128)
	purpose = models.CharField(max_length = 128)
	maxLTV = models.CharField(max_length = 128)

	def __str__(self):
		return self.maxLTV


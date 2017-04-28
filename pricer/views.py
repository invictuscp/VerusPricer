from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from pricer.forms import PricerForm
from pricer.models import BaseRate, GradeAdj, DocTypeAdj, DTIAdj, LoanBalanceAdj, PurposeAdj, OccupancyAdj, PropertyTypeAdj, StateAdj, IOAdj, LoanTermAdj, ReservesAdj, PrepayAdj
from pricer.models import CAProductMatrix, PIProductMatrix, DTIProductMatrix, FNProductMatrix

def index(request):
	baseRate = ""
	eligibility = ""
	reasons = ""
	grade = ""
	if request.method == 'POST':
		form = PricerForm(request.POST)
		if form.is_valid():
			#Save form but don't commit to database yet
			instance = form.save(commit=False)
			#Extract data from form
			fico = instance.fico
			ltv = instance.ltv
			citizenship = instance.citizenship
			seflag = instance.seflag
			fthbflag = instance.fthbflag
			doctype = instance.doctype
			dti = instance.dti
			loanamount = instance.loanamount
			purpose = instance.purpose
			state = instance.state
			occupancy = instance.occupancy
			propType = instance.propType
			io = instance.io
			term = instance.term
			prepay = instance.prepay
			reserves = instance.reserves
			dscr = instance.dscr
			se = instance.seflag
			fthb = instance.fthbflag
			x30x12 = instance.x30x12
			x60x12 = instance.x60x12
			x90x12 = instance.x90x12
			x30x24 = instance.x30x24
			x60x24 = instance.x60x24
			x90x24 = instance.x90x24
			monthsFC = instance.monthsFC
			monthsSS = instance.monthsSS
			monthsDIL = instance.monthsDIL
			monthsBK = instance.monthsBK
			bkChapter = instance.bkChapter
			eligibility = "Eligible"
			ficoEligible = False
			reservesEligible = False

			#Get Base Rate
			if citizenship == "Yes" and (occupancy == "Primary" or occupancy == "2nd Home"):
				baseRate = get_or_none(BaseRate, rateSheetName = "Credit Ascent", fico = "Foreign National1", ltv = ltv)
			elif occupancy == "Primary" or occupancy == "2nd Home":
				baseRate = get_or_none(BaseRate, rateSheetName = "Credit Ascent", fico = fico, ltv = ltv)
			elif citizenship == "Yes" and occupancy == "Investor" and (doctype == "No Ratio" or doctype == "DSCR"):
				baseRate = get_or_none(BaseRate, rateSheetName = "Investor PI", fico = "Foreign National", ltv = ltv)
			elif occupancy == "Investor" and (doctype == "No Ratio" or doctype == "DSCR"):
				baseRate = get_or_none(BaseRate, rateSheetName = "Investor PI", fico = fico, ltv = ltv)
			elif citizenship == "Yes" and occupancy == "Investor":
				baseRate = get_or_none(BaseRate, rateSheetName = "Investor DTI", fico = "Foreign National1", ltv = ltv)
			elif occupancy == "Investor":
				baseRate = get_or_none(BaseRate, rateSheetName = "Investor DTI", fico = fico, ltv = ltv)

			#Calculate Grade
			if (doctype == "DSCR" or doctype == "No Ratio") and occupancy == "Investor":
				grade = "N/A"
				eligibility = getPIHousingEligibility(monthsBK, bkChapter, monthsDIL, monthsSS, monthsFC, int(x30x12), int(x60x12), int(x90x12), int(x30x24), int(x60x24), int(x90x24))
			else:
				grade = getGrade(occupancy, fico, monthsBK, bkChapter, monthsDIL, monthsSS, monthsFC, int(x30x12), int(x60x12), int(x90x12), int(x30x24), int(x60x24), int(x90x24), citizenship)

			#Calculate Grade Adjustment
			if (citizenship == "Yes" and fico == "Foreign Credit"):
				gradeAdj = get_or_none(GradeAdj, rateSheetName = "Credit Ascent", grade = "Foreign Credit", ltv = ltv)
			elif occupancy == "Primary":
				gradeAdj = get_or_none(GradeAdj, rateSheetName = "Credit Ascent", grade = grade, ltv = ltv)
			else: 
				gradeAdj = get_or_none(GradeAdj, rateSheetName = "Investor DTI", grade = grade, ltv = ltv)

			#Get remaining adjustments
			if (occupancy == "Primary" or occupancy == "2nd Home"):
				docAdj = get_or_none(DocTypeAdj, rateSheetName = "Credit Ascent", docType = doctype, grade = grade, ltv = ltv)
				dtiAdj = get_or_none(DTIAdj, rateSheetName = "Credit Ascent", dti = dti, grade = grade, ltv = ltv)
				loanAdj = get_or_none(LoanBalanceAdj, rateSheetName = "Credit Ascent", balance = loanamount, ltv = ltv)
				purposeAdj = get_or_none(PurposeAdj, rateSheetName = "Credit Ascent", purpose = purpose, grade = grade, ltv = ltv)
				occAdj = get_or_none(OccupancyAdj, rateSheetName = "Credit Ascent", occupancy = occupancy, ltv = ltv)
				propAdj = get_or_none(PropertyTypeAdj, rateSheetName = "Credit Ascent", propertyType = propType, ltv = ltv)
				stateAdj = get_or_none(StateAdj, rateSheetName = "Credit Ascent", state = getTier(state), ltv = ltv)
				ioAdj = get_or_none(IOAdj, rateSheetName = "Credit Ascent", io = io, ltv = ltv)
				termAdj = get_or_none(LoanTermAdj, rateSheetName = "Credit Ascent", loanTerm = term)

			elif (doctype == "DSCR" or doctype == "No Ratio") and occupancy == "Investor":
				docAdj = get_or_none(DocTypeAdj, rateSheetName = "Investor PI", docType = doctype, grade = "A", ltv = ltv)
				reservesAdj = get_or_none(ReservesAdj, rateSheetName = "Investor PI", reserves = reserves, ltv = ltv)
				loanAdj = get_or_none(LoanBalanceAdj, rateSheetName = "Investor PI", balance = loanamount, ltv = ltv)
				purposeAdj = get_or_none(PurposeAdj, rateSheetName = "Investor PI", purpose = purpose, grade = "A", ltv = ltv)
				propAdj = get_or_none(PropertyTypeAdj, rateSheetName = "Investor PI", propertyType = propType, ltv = ltv)
				stateAdj = get_or_none(StateAdj, rateSheetName = "Investor PI", state = getTier(state), ltv = ltv)
				ioAdj = get_or_none(IOAdj, rateSheetName = "Investor PI", io = io, ltv = ltv)
				prepayAdj = get_or_none(PrepayAdj, rateSheetName = "Investor PI", prepayTerm = prepay, ltv = ltv)
				termAdj = get_or_none(LoanTermAdj, rateSheetName = "Investor PI", loanTerm = term)
				#print "Base: " + str(baseRate.adj)
				#print "Doc: " + str(docAdj.adj)
				#print "DTI: " + str(dtiAdj.adj)
				#print "Loan Amount: " + str(loanAdj.adj)
				#print "Reserves: " + str(reservesAdj.adj)
				#print "Purpose: " + str(purposeAdj.adj)
				#print "Occ: " + str(occAdj.adj)
				#print "Property: " + str(propAdj.adj)
				#print "State: " + str(stateAdj.adj)
				#print "IO: " + str(ioAdj.adj)
				#print "Prepay: " + str(prepayAdj.adj)
				#print "Term: " + str(termAdj.adj)

			else:
				docAdj = get_or_none(DocTypeAdj, rateSheetName = "Investor DTI", docType = doctype, grade = grade, ltv = ltv)
				dtiAdj = get_or_none(DTIAdj, rateSheetName = "Investor DTI", dti = dti, grade = grade, ltv = ltv)
				loanAdj = get_or_none(LoanBalanceAdj, rateSheetName = "Investor DTI", balance = loanamount, ltv = ltv)
				purposeAdj = get_or_none(PurposeAdj, rateSheetName = "Investor DTI", purpose = purpose, grade = grade, ltv = ltv)
				propAdj = get_or_none(PropertyTypeAdj, rateSheetName = "Investor DTI", propertyType = propType, ltv = ltv)
				stateAdj = get_or_none(StateAdj, rateSheetName = "Investor DTI", state = getTier(state), ltv = ltv)
				ioAdj = get_or_none(IOAdj, rateSheetName = "Investor DTI", io = io, ltv = ltv)
				prepayAdj = get_or_none(PrepayAdj, rateSheetName = "Investor DTI", prepayTerm = prepay, ltv = ltv)
				termAdj = get_or_none(LoanTermAdj, rateSheetName = "Investor DTI", loanTerm = term)

			#Sum adjustments and determine preliminary eligibility
			if (occupancy == "Primary" or occupancy == "2nd Home"):
				if (gradeAdj is not None) and (docAdj is not None) and (dtiAdj is not None) and (loanAdj is not None) and (purposeAdj is not None) and (occAdj is not None) and (propAdj is not None) \
					and (stateAdj is not None) and (ioAdj is not None) and (termAdj is not None):
					sumAdj = gradeAdj.adj + docAdj.adj + dtiAdj.adj + loanAdj.adj + purposeAdj.adj + occAdj.adj + propAdj.adj + stateAdj.adj + ioAdj.adj + termAdj.adj
				else:
					eligibility = "Not Eligible"
			elif (doctype == "DSCR" or doctype == "No Ratio") and occupancy == "Investor":
				if (docAdj is not None) and (reservesAdj is not None) and (loanAdj is not None) and (purposeAdj is not None) and (propAdj is not None) \
					and (stateAdj is not None) and (ioAdj is not None) and (prepayAdj is not None) and (termAdj is not None):
					sumAdj = docAdj.adj + reservesAdj.adj + loanAdj.adj + purposeAdj.adj + prepayAdj.adj + propAdj.adj + stateAdj.adj + ioAdj.adj + termAdj.adj
				else:
					eligibility = "Not Eligible"
			else:
				if (gradeAdj is not None) and (docAdj is not None) and (dtiAdj is not None) and (loanAdj is not None) and (purposeAdj is not None) and (propAdj is not None) \
					and (stateAdj is not None) and (ioAdj is not None) and (prepayAdj is not None) and (termAdj is not None):
					sumAdj = gradeAdj.adj + docAdj.adj + dtiAdj.adj + loanAdj.adj + purposeAdj.adj + prepayAdj.adj + propAdj.adj + stateAdj.adj + ioAdj.adj + termAdj.adj
				else:
					eligibility = "Not Eligible"

			# CREDIT ASCENT ELIGIBILITY
			if (occupancy == "Primary" or occupancy == "2nd Home") and citizenship == "No" and fico != "Foreign Credit":
				#LTV/FICO/LOAN AMOUNT MATRIX ELIGIBILITY
				if not CAProductMatrix.objects.all().filter(occupancy = occupancy, grade = grade, loanamount = loanamount, docType = doctype, purpose = purpose):
					reasons = reasons + "Loan Amount Exceeds Limit" + "\n"
					eligibility = "Not Eligible"
				else:
					for matrix in CAProductMatrix.objects.all().filter(occupancy = occupancy, grade = grade, loanamount = loanamount, docType = doctype, purpose = purpose):
						if matchMatrixFICO(fico, matrix.fico) == True:
							ficoEligible = True
							if matrix.maxLTV == "NA":
								reasons = reasons + "LTV Exceeds Limit For Given FICO/LTV/Loan Amount Combination" + '\n'
								eligibility = "Not Eligible"
							elif int(getLTV(ltv)) > int(matrix.maxLTV):
								reasons = reasons + "LTV Exceeds Limit For Given FICO/LTV/Loan Amount Combination" + '\n'
								eligibility = "Not Eligible"

				if ficoEligible == False:
					reasons = reasons + "FICO Below Limit For Given FICO/LTV/Loan Amount Combination" + '\n'

				# DTI/RESERVES MATRIX ELIGIBILITY
				if dti != "N/A":
					if getDTIReservesEligibility(occupancy, doctype, getLTV(ltv), getDTI(dti), getLoanAmount(loanamount), getReserves(reserves)) == "Not Eligible":
						reasons = reasons + "Reserves/DTI/Doc Type/Loan Amount Combination Not Eligible" + '\n'
						eligibility = "Not Eligible"

				# ONE-OFF ELIGIBILITY RULES
				if occupancy =="Primary": 
					if grade in ("A", "A-"):
						if propType in ("Condo", "2-4 Unit") and getLTV(ltv) > 80:
							reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
							eligibility = "Not Eligible"
						elif propType == "Non-Warrantable Condo" and getLTV(ltv) > 75:
							reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
							eligibility = "Not Eligible"
						elif getLoanAmount(loanamount) < 150000 and getLTV(ltv) > 80:
							reasons = reasons + "LTV Exceeded for Given Loan Amount" + '\n'
							eligibility = "Not Eligible"
					elif grade in ("B+", "B", "B-", "C"):
						if propType in ("Condo", "2-4 Unit") and getLTV(ltv) > 75:
							reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
							eligibility = "Not Eligible"
						elif propType == "Non-Warrantable Condo" and getLTV(ltv) > 70:
							reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
							eligibility = "Not Eligible"
						elif propType == "Non-Warrantable Condo" and grade == "C":
							reasons = reasons + "Grade Below Limit for Given Property Type" + '\n'
							eligibility = "Not Eligible"
						elif getLoanAmount(loanamount) < 150000 and getLTV(ltv) > 75:
							reasons = reasons + "LTV Exceeded for Given Loan Amount" + '\n'
							eligibility = "Not Eligible"
				elif occupancy =="2nd Home":
					if grade in ("A", "A-"):
						if propType in ("Condo", "2-4 Unit") and getLTV(ltv) > 70:
							reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
							eligibility = "Not Eligible"
						elif propType == "Non-Warrantable Condo" and getLTV(ltv) > 65:
							reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
							eligibility = "Not Eligible"
						elif getLoanAmount(loanamount) < 150000 and getLTV(ltv) > 70:
							reasons = reasons + "LTV Exceeded for Given Loan Amount" + '\n'
							eligibility = "Not Eligible"
					elif grade in ("B+", "B", "B-", "C"):
						if propType in ("Condo", "2-4 Unit") and getLTV(ltv) > 65:
							reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
							eligibility = "Not Eligible"
						elif propType == "Non-Warrantable Condo" and getLTV(ltv) > 65:
							reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
							eligibility = "Not Eligible"
						elif propType == "Non-Warrantable Condo" and grade == "C":
							reasons = reasons + "Grade Below Limit for Given Property Type" + '\n'
							eligibility = "Not Eligible"
						elif getLoanAmount(loanamount) < 150000 and getLTV(ltv) < 65:
							reasons = reasons + "LTV Exceeded for Given Loan Amount" + '\n'
							eligibility = "Not Eligible"

				if getLoanAmount(loanamount) < 100000:
					reasons = reasons + "Loan Amount Below Minimum for Verus Credit Ascent Program" + '\n'
					eligibility = "Not Eligible"

				if propType == "Non-Warrantable Condo":
					if getDTI(dti) > 43:
						reasons = reasons + "DTI Exceeded for Given Property Type" + '\n'
						eligibility = "Not Eligible"
					if getReserves(reserves) < 6:
						reasons = reasons + "Reserves Below Minimum for Given Property Type" + '\n'
						eligibility = "Not Eligible"
					if getLoanAmount(loanamount) > 1000000:
						reasons = reasons + "Loan Amount Exceeds Limit for Given Property Type" + '\n'
						eligibility = "Not Eligible"

				if dti == "N/A":
					reasons = reasons + "DTI Required for Verus Credit Ascent Program" + '\n'
					eligibility = "Not Eligible"

				# IO ELIGIBILITY
				if io == "Yes":
					if doctype == "Full Doc" and fico != "Foreign Credit":
						if int(fico[:3]) < 660:
							reasons = reasons + "FICO Below Minimum for IO" + '\n'
							eligibility = "Not Eligible"
					elif doctype in ("24 Mo Bank Statement", "12 Mo Bank Statement", "Asset Utilization") and fico != "Foreign Credit":
						if int(fico[:3]) < 680:
							reasons = reasons + "FICO Below Minimum for IO" + '\n'
							eligibility = "Not Eligible"

					if getLTV(ltv) > 80:
						reasons = reasons + "LTV Exceeds Limit for IO" + '\n'
						eligibility = "Not Eligible"

					if grade in ("B", "B-", "C"):
						reasons = reasons + "Grade Below Minimum for IO" + '\n'
						eligibility = "Not Eligible"

					if term == "15 Yr Fix":
						reasons = reasons + "Term Ineligible for IO" + '\n'
						eligibility = "Not Eligible"

					if occupancy == "2nd Home":
						reasons = reasons + "IO Product Ineligible for 2nd Home Borrowers" + '\n'
						eligibility = "Not Eligible"

				# MISC STATE ELIGIBILITY
				if state in ("DC", "MD", "NJ", "NY") and fico != "Foreign Credit":
					if int(fico[:3]) < 660:
						reasons = reasons + "FICO Below Minimum for Given State" + '\n'
						eligibility = "Not Eligible"

					if getLTV(ltv) > 80:
						reasons = reasons + "FICO Below Minimum for Given State" + '\n'
						eligibility = "Not Eligible"

				# PI INPUT CHECK
				if prepay != "N/A" and prepay != "No Penalty":
					reasons = reasons + "Prepay Not Allowed for Primary/2nd Home Borrowers" + '\n'
					eligibility = "Not Eligible"

				if doctype in ("No Ratio", "DSCR"):
					reasons = reasons + "Selected Doc Type Not Allowed for Primary/2nd Home Borrowers" + '\n'
					eligibility = "Not Eligible"

				if term == "3/1 ARM":
					reasons = reasons + "Term Not Allowed for Primary/2nd Home Borrowers" + '\n'
					eligibility = "Not Eligible"

				if dscr not in ("N/A", "No Penalty"):
					reasons = reasons + "DSCR Not Allowed for Primary/2nd Home Borrowers" + '\n'
					eligibility = "Not Eligible"

			# INVESTOR DSCR/NO RATIO ELIGIBILITY
			elif (doctype == "DSCR" or doctype == "No Ratio") and occupancy == "Investor":
				# LTV/FICO/LOAN AMOUNT MATRIX ELIGIBILITY
				if not PIProductMatrix.objects.all().filter(docType = doctype, loanamount = loanamount, purpose = purpose):
					reasons = reasons + "Loan Amount Exceeds Limit For Given FICO/LTV/Loan Amount Combination" + '\n'
					eligibility = "Not Eligible"
				else:
					for matrix in PIProductMatrix.objects.all().filter(docType = doctype, loanamount = loanamount, purpose = purpose):
						if matchMatrixFICO(fico, matrix.fico) == True and matchMatrixReserves(reserves, matrix.reserves) == True:
							ficoEligible = True
							reservesEligible = True
							if matrix.maxLTV == "NA":
								reasons = reasons + "LTV Exceeds Limit For Given FICO/LTV/Loan Amount Combination" + '\n'
								eligibility = "Not Eligible"
							elif int(getLTV(ltv)) > int(matrix.maxLTV):
								reasons = reasons + "LTV Exceeds Limit For Given FICO/LTV/Loan Amount Combination" + '\n'
								eligibility = "Not Eligible"

				# ONE-OFF ELIGIBILITY
				if ficoEligible == False:
					reasons = reasons + "FICO Below Limit For Given FICO/LTV/Loan Amount Combination" + '\n'
					eligibility = "Not Eligible"
				if reservesEligible == False:
					reasons = reasons + "Reserves Below Limit For Given FICO/LTV/Loan Amount Combination" + '\n'
					eligibility = "Not Eligible"

				if getLoanAmount(loanamount) < 150000 and getLTV(ltv) > 70:
					reasons = reasons + "LTV Exceeds Limit for Given Loan Amount" + '\n'
					eligibility = "Not Eligible"

				if getLoanAmount(loanamount) < 100000:
					reasons = reasons + "Loan Amount Below Limit for Verus Professional Investor Program" + '\n'
					eligibility = "Not Eligible"

				if propType == "2-4 Unit" and getLTV(ltv) > 70:
					reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
					eligibility = "Not Eligible"

				if propType == "Non-Warrantable Condo":
						reasons = reasons + "Property Type Not Eligible for Verus Professional Investor Program" + '\n'
						eligibility = "Not Eligible"

				# IO ELIGIBILITY
				if io == "Yes":
					if int(fico[:3]) < 680:
						reasons = reasons + "FICO Below Minimum for IO" + '\n'
						eligibility = "Not Eligible"

					if getLTV(ltv) > 70:
						reasons = reasons + "LTV Exceeds Limit for IO" + '\n'
						eligibility = "Not Eligible"

					if term == "15 Yr Fix":
						reasons = reasons + "Term Ineligible for IO" + '\n'
						eligibility = "Not Eligible"

				# DSCR ELIGIBILITY
				if doctype == "DSCR":
					if dscr == "N/A":
						reasons = reasons + "DSCR Product Missing DSCR Value" + '\n'
						eligibility = "Not Eligible"
					elif getLoanAmount(loanamount) < 100000 and getDSCR(dscr) < 1.3:
						reasons = reasons + "DSCR Below Limit Given Loan Amount" + '\n'
						eligibility = "Not Eligible"
					elif getLoanAmount(loanamount) < 400000 and getDSCR(dscr) < 1.25:
						reasons = reasons + "DSCR Below Limit Given Loan Amount" + '\n'
						eligibility = "Not Eligible"
					elif getDSCR(dscr) < 1.15:
						reasons = reasons + "DSCR Below Limit Given Loan Amount" + '\n'
						eligibility = "Not Eligible"

				# MISC STATE ELIGIBILITY
				if state in ("DC", "MD", "NJ", "NY") and fico != "Foreign Credit":
					if int(fico[:3]) < 680:
						reasons = reasons + "FICO Below Minimum for Given State" + '\n'
						eligibility = "Not Eligible"

					if grade not in ("A", "A-"):
						reasons = reasons + "Grade Below Minimum for Given State" + '\n'
						eligibility = "Not Eligible"

				if dti != "N/A":
					reasons = reasons + "DTI Not Allowed for Verus Professional Investor Program" + '\n'
					eligibility = "Not Eligible"

			# FOREIGN NATIONAL ELIGIBILITY
			elif citizenship == "Yes":
				# LTV/FICO/LOAN AMOUNT MATRIX ELIGIBILITY
				matrix = get_or_none(FNProductMatrix, docType = doctype, grade = grade, loanamount = loanamount, purpose = purpose)
				if doctype in ("Full Doc", "DSCR", "No Ratio") and matrix is None:
					reasons = reasons + "Loan Amount Exceeds Limit For Given FICO/LTV/Loan Amount Combination" + '\n'
					eligibility = "Not Eligible"
				elif doctype in ("12 Mo Bank Statement", "24 Mo Bank Statement", "Asset Utilization"):
					reasons = reasons + "Doc Type Not Eligible For Foreign National Borrowers" + '\n'
					eligibility = "Not Eligible"
				else:
					if matrix.maxLTV == "NA":
						reasons = reasons + "Not Allowed" + '\n'
						eligibility = "Not Eligible"
					elif int(getLTV(ltv)) > int(matrix.maxLTV):
						reasons = reasons + "LTV Exceeds Limit For Given FICO/LTV/Loan Amount Combination" + '\n'
						eligibility = "Not Eligible"

				# ONE-OFF ELIGIBILITY
				if occupancy == "Primary":
					reasons = reasons + "Occupancy Not Eligible for Foreign National Borrowers" + '\n'
					eligibility = "Not Eligible"
				elif occupancy == "2nd Home":
					if doctype != "Full Doc":
						reasons = reasons + "Doc Type Not Eligible for 2nd Home Foreign National Borrowers" + '\n'
						eligibility = "Not Eligible"
					if prepay not in ("N/A", "No Penalty"):
						reasons = reasons + "Prepay Penalty Not Eligible for 2nd Home Foreign National Borrowers" + '\n'
						eligibility = "Not Eligible"

				if io == "Yes":
					reasons = reasons + "IO Product Not Eligible for Foreign National Borrowers" + '\n'
					eligibility = "Not Eligible"

				if getLoanAmount(loanamount) < 150000 and getLTV(ltv) > 70:
					reasons = reasons + "LTV Exceeds Limit for Given Loan Amount" + '\n'
					eligibility = "Not Eligible"

				if getLoanAmount(loanamount) < 100000:
					reasons = reasons + "Loan Amount Below Limit for Verus Professional Investor Program" + '\n'
					eligibility = "Not Eligible"

				if propType == "2-4 Unit" and getLTV(ltv) > 70:
					reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
					eligibility = "Not Eligible"

				if propType == "Non-Warrantable Condo":
						reasons = reasons + "Property Type Not Eligible for Verus Professional Investor Program" + '\n'
						eligibility = "Not Eligible"

				if grade in ("B", "B-", "C",):
					reasons = reasons + "Grade Below Limit for Foreign National Borrowers" + '\n'
					eligibility = "Not Eligible"

				if fico != "Foreign Credit" and getLTV(ltv) > 75:
					reasons = reasons + "LTV Exceeds Limit for Foreign National Borrowers" + '\n'
					eligibility = "Not Eligible"
				if fico == "Foreign Credit" and getLTV(ltv) > 70:
					reasons = reasons + "LTV Exceeds Limit for Foreign National Borrowers" + '\n'
					eligibility = "Not Eligible"

				if int(fico[:3]) < 620:
					reasons = reasons + "FICO Below Limit for Foreign National Borrowers" + '\n'
					eligibility = "Not Eligible"

				if getReserves(reserves) < 12:
					reasons = reasons + "Reserves Below Limit for Foreign National Borrowers" + '\n'
					eligibility = "Not Eligible"

				if dti == "N/A" and doctype in ("Full Doc", "24 Mo Bank Statement", "12 Mo Bank Statement", "Asset Utilization"):
					reasons = reasons + "DTI Required for Foreign National Borrowers with Selected Doc Type" + '\n'
					eligibility = "Not Eligible"
				else:
					if dti != "N/A" and doctype in ("DSCR", "No Ratio"):
						reasons = reasons + "DTI Not Allowed for Foreign National Borrowers with Selected Doc Type" + '\n'
						eligibility = "Not Eligible"

				# DSCR ELIGIBILITY
				if doctype == "DSCR":
					if dscr == "N/A":
						reasons = reasons + "DSCR Product Missing DSCR Value" + '\n'
						eligibility = "Not Eligible"
					elif getLoanAmount(loanamount) < 100000 and getDSCR(dscr) < 1.3:
						reasons = reasons + "DSCR Below Limit Given Loan Amount" + '\n'
						eligibility = "Not Eligible"
					elif getLoanAmount(loanamount) < 400000 and getDSCR(dscr) < 1.25:
						reasons = reasons + "DSCR Below Limit Given Loan Amount" + '\n'
						eligibility = "Not Eligible"
					elif getDSCR(dscr) < 1.15:
						reasons = reasons + "DSCR Below Limit Given Loan Amount" + '\n'
						eligibility = "Not Eligible"
				else:
					if dscr != "N/A":
						reasons = reasons + "DSCR Not Allowed for Selected Doc Type" + '\n'
						eligibility = "Not Eligible"


			# INVESTOR DTI ELIGIBILITY
			elif occupancy == "Investor" and fico != "Foreign Credit":
				# LTV/FICO/LOAN AMOUNT MATRIX ELIGIBILITY
				if not DTIProductMatrix.objects.all().filter(grade = grade, loanamount = loanamount, docType = doctype, purpose = purpose):
					reasons = reasons + "Loan Amount Exceeds Limit For Given FICO/LTV/Loan Amount Combination" + '\n'
					eligibility = "Not Eligible"
				else:
					for matrix in DTIProductMatrix.objects.all().filter(grade = grade, loanamount = loanamount, docType = doctype, purpose = purpose):
						if matchMatrixFICO(fico, matrix.fico) == True:
							ficoEligible = True
							if matrix.maxLTV == "NA":
								reasons = reasons + "LTV Exceeds Limit For Given FICO/LTV/Loan Amount Combination" + '\n'
								eligibility = "Not Eligible"
							elif int(getLTV(ltv)) > int(matrix.maxLTV):
								reasons = reasons + "LTV Exceeds Limit For Given FICO/LTV/Loan Amount Combination" + '\n'
								eligibility = "Not Eligible"

				if ficoEligible == False:
					reasons = reasons + "FICO Below Limit For Given FICO/LTV/Loan Amount Combination" + '\n'
					eligibility = "Not Eligible"

				# DTI/RESERVES MATRIX ELIGIBILITY
				if dti != "N/A":
					if getDTIReservesEligibility(occupancy, doctype, getLTV(ltv), getDTI(dti), getLoanAmount(loanamount), getReserves(reserves)) == "Not Eligible":
						reasons = reasons + "Reserves/DTI/Doc Type/Loan Amount Combination Not Eligible" + '\n'
						eligibility = "Not Eligible"

				# ONE-OFF ELIGIBILITY RULES
				if grade in ("A", "A-"):
					if propType in ("Condo", "2-4 Unit") and getLTV(ltv) > 70:
						reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
						eligibility = "Not Eligible"
					elif propType == "Non-Warrantable Condo" and getLTV(ltv) > 65:
						reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
						eligibility = "Not Eligible"
					elif getLoanAmount(loanamount) < 150000 and getLTV(ltv) > 70:
						reasons = reasons + "LTV Exceeded for Given Loan Amount" + '\n'
						eligibility = "Not Eligible"
				elif grade in ("B+", "B", "B-", "C"):
					if propType in ("Condo", "2-4 Unit") and getLTV(ltv) > 65:
						reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
						eligibility = "Not Eligible"
					elif propType == "Non-Warrantable Condo" and getLTV(ltv) > 65:
						reasons = reasons + "LTV Exceeded for Given Property Type" + '\n'
						eligibility = "Not Eligible"
					elif getLoanAmount(loanamount) < 150000 and getLTV(ltv) > 65:
						reasons = reasons + "LTV Exceeded for Given Loan Amount" + '\n'
						eligibility = "Not Eligible"
				
				if getLoanAmount(loanamount) < 100000:
					reasons = reasons + "Loan Amount Below Minimum for Verus Investor DTI Program" + '\n'
					eligibility = "Not Eligible"

				if propType == "Non-Warrantable Condo":
					if getDTI(dti) > 43:
						reasons = reasons + "DTI Exceeded for Given Property Type" + '\n'
						eligibility = "Not Eligible"
					if getReserves(reserves) < 6:
						reasons = reasons + "Reserves Below Minimum for Given Property Type" + '\n'
						eligibility = "Not Eligible"
					if getLoanAmount(loanamount) > 1000000:
						reasons = reasons + "Loan Amount Exceeds Limit for Given Property Type" + '\n'
						eligibility = "Not Eligible"

				# IO ELIGIBILITY
				if io == "Yes":
					if doctype == "Full Doc" and fico != "Foreign Credit":
						if int(fico[:3]) < 660:
							reasons = reasons + "FICO Below Minimum for IO" + '\n'
							eligibility = "Not Eligible"
					elif doctype in ("24 Mo Bank Statement", "12 Mo Bank Statement", "Asset Utilization") and fico != "Foreign Credit":
						if int(fico[:3]) < 680:
							reasons = reasons + "FICO Below Minimum for IO" + '\n'
							eligibility = "Not Eligible"

					if getLTV(ltv) > 75:
						reasons = reasons + "LTV Exceeds Limit for IO" + '\n'
						eligibility = "Not Eligible"

					if grade in ("B", "B-", "C"):
						reasons = reasons + "Grade Below Minimum for IO" + '\n'
						eligibility = "Not Eligible"

					if term == "15 Yr Fix":
						reasons = reasons + "Term Ineligible for IO" + '\n'
						eligibility = "Not Eligible"

				# MISC STATE ELIGIBILITY
				if state in ("DC", "MD", "NJ", "NY") and fico != "Foreign Credit":
					if int(fico[:3]) < 680:
						reasons = reasons + "FICO Below Minimum for Given State" + '\n'
						eligibility = "Not Eligible"

					if getLTV(ltv) > 75:
						reasons = reasons + "FICO Below Minimum for Given State" + '\n'
						eligibility = "Not Eligible"

					if grade not in ("A", "A-"):
						reasons = reasons + "Grade Below Minimum for Given State" + '\n'
						eligibility = "Not Eligible"

				if dti == "N/A":
					reasons = reasons + "DTI Required for Verus Investor DTI Program" + '\n'
					eligibility = "Not Eligible"

			# FTHB ELIGIBILITY
			if fthb == "Yes":
				if occupancy != "Primary":
					reasons = reasons + "Occupancy Not Eligible for First Time Home Buyers" + '\n'
					eligibility = "Not Eligible"
				if int(fico[:3]) < 540:
					reasons = reasons + "FICO Below Limit for First Time Home Buyers" + '\n'
					eligibility = "Not Eligible"
				if getReserves(reserves) < 6:
					reasons = reasons + "Reserves Below Limit for First Time Home Buyers" + '\n'
					eligibility = "Not Eligible"
				if int(x30x12) > 0:
					reasons = reasons + "Housing Lates Exceed Limit for First Time Home Buyers" + '\n'
					eligibility = "Not Eligible"
				if doctype == "12 Mo Bank Statement":
					reasons = reasons + "Doc Type Not Allowed for First Time Home Buyers" + '\n'
					eligibility = "Not Eligible"

			# SELF EMPLOYED ELIGIBILITY
			if se == "No":
				if doctype in ("24 Mo Bank Statement", "12 Mo Bank Statement"):
					reasons = reasons + "Non Self-Employed Borrowers Ineligible For Selected Doc Type" + '\n'
					eligibility = "Not Eligible"

			# Set final eligibility
			if (occupancy == "Primary" or occupancy == "2nd Home") and eligibility == "Eligible":
				eligibility = "Eligible for Verus Credit Ascent (Owner Occupied & 2nd Home) Program"
			elif (doctype == "DSCR" or doctype == "No Ratio") and occupancy == "Investor" and eligibility == "Eligible":
				eligibility = "Eligible for Verus Investor Solutions - Professional Investor Program"
			elif eligibility == "Eligible":
				eligibility = "Eligible for Verus Investor Solutions - Borrower DTI Program"

			# Return base rate and eligibility
			if baseRate is not None and eligibility[:8] == "Eligible":
				baseRate = "{0:.3f}%".format((baseRate.adj*100)+sumAdj)
			else:
				baseRate = "N/A"
				eligibility = "Not Eligible"

	else:
		form = PricerForm()
	return render(request, 'pricer/index.html', {'form': form, 'baseRate': baseRate, 'eligibility': eligibility, 'grade': grade, 'reasons': reasons})



def get_or_none(classmodel, **kwargs):
	try:
		return classmodel.objects.get(**kwargs)
	except classmodel.DoesNotExist:
		return None

def getLoanAmount(loanamount):
	if loanamount == "< $100,000":
		value = 99000
	elif loanamount == "$100,000 - $149,999":
		value = 125000
	elif loanamount == "$150,000 - $399,999":
		value = 200000
	elif loanamount == "$400,000 - $499,999":
		value = 450000
	elif loanamount == "$500,000 - $749,999":
		value = 600000
	elif loanamount == "$750,000 - $799,999":
		value = 775000
	elif loanamount == "$800,000 - $999,999":
		value = 900000
	elif loanamount == "$1,000,000 - $1,249,999":
		value = 1125000
	elif loanamount == "$1,250,000 - $1,499,999":
		value = 1375000
	elif loanamount == "$1,500,000 - $2,000,000":
		value = 1750000

	return value

def getLTV(ltv):
	if ltv == "<=55":
		value = 54
	elif ltv == "55.01-60":
		value = 57
	elif ltv == "60.01-65":
		value = 63
	elif ltv == "65.01-70":
		value = 67
	elif ltv == "70.01-75":
		value = 73
	elif ltv == "75.01-80":
		value = 77
	elif ltv == "80.01-85":
		value = 83
	elif ltv == "85.01-90":
		value = 87

	return value

def getDTI(dti):
	if dti == "<= 36%":
		value = 35
	elif dti == "36.01% - 43%":
		value = 40
	elif dti == "43.01% - 50%":
		value = 45
	elif dti == "> 50%":
		value = 55

	return value

def getReserves(reserves):
	if reserves == "None":
		value = 0
	elif reserves == "< 6 Months":
		value = 5
	elif reserves == "6 - 11 Months":
		value = 10
	elif reserves == "12 - 17 Months":
		value = 15
	elif reserves == "18 - 23 Months":
		value = 20
	elif reserves == ">= 24 Months":
		value = 25

	return value

def getDSCR(dscr):
	if dscr == "< 1.15":
		value = 1
	elif dscr == "1.15 - 1.24":
		value = 1.20
	elif dscr == "1.25 - 1.29":
		value = 1.27
	elif dscr == ">= 1.30":
		value = 1.50

	return value

def matchMatrixFICO(formFICO, matrixFICO):
	match = False
	formFICO = int(formFICO[:3])
	if matrixFICO[3] == "+":
		if formFICO >= 	int(matrixFICO[:3]):
			match = True
	else:
		if formFICO >= int(matrixFICO[:3]) and formFICO <= int(matrixFICO[-3:]):
			match = True
	return match

def matchMatrixReserves(formReserves, matrixReserves):
	match = False
	if matrixReserves == "6 Months" and formReserves in ("6 - 11 Months", "12 - 17 Months", "18 - 23 Months", ">= 24 Months"):
		match = True
	elif matrixReserves == "12 Months" and formReserves in ("12 - 17 Months", "18 - 23 Months", ">= 24 Months"):
		match = True
	elif matrixReserves == "None" and formReserves in ("None", "< 6 Months", "6 - 11 Months", "12 - 17 Months", "18 - 23 Months", ">= 24 Months"):
		match = True
	return match

def getGrade(occupancy, fico, monthsBK, bkChapter, monthsDIL, monthsSS, monthsFC, x30x12, x60x12, x90x12, x30x24, x60x24, x90x24, citizenship):
	if citizenship == "Yes" and fico == "Foreign Credit":
		return "B+"
	if citizenship == "No" and fico == "Foreign Credit":
		return "N/A"
	else:
		fico = int(fico[:3])

	if fico <= 540 and occupancy[:1] == "I":
		grade = "N/A"

	if (fico >= 680) and (x30x12 == 0 or x30x12 is None) and (x60x24 == 0 or x60x24 is None) and ((monthsBK >= 24 and bkChapter == 13) or (monthsBK >= 48 and bkChapter != 13) or monthsBK is None) and (monthsFC >= 48 or monthsFC is None) and (monthsSS >= 36 or monthsSS is None) and (monthsDIL >= 36 or monthsDIL is None):
		grade = "A"
	elif (fico >= 660) and (x30x12 == 0 or x30x12 is None) and ((monthsBK >= 12 and bkChapter == 13) or (monthsBK >= 24 and bkChapter != 13) or monthsBK is None) and (monthsFC >= 24 or monthsFC is None) and (monthsSS >= 24 or monthsSS is None) and (monthsDIL >= 24 or monthsDIL is None):
		grade = "A-"
	elif (fico >= 580) and (x30x12 <= 1 or x30x12 is None) and ((monthsBK >= 24 and bkChapter != 13) or monthsBK is None) and (monthsFC >= 24 or monthsFC is None) and (monthsSS >= 12 or monthsSS is None) and (monthsDIL >= 12 or monthsDIL is None):
		grade = "B+"
	elif (fico >= 540) and (x60x12 == 0 or x60x12 is None) and ((monthsBK >= 24 and bkChapter != 13) or monthsBK is None) and (monthsFC >= 24 or monthsFC is None):
		grade = "B"
	elif (fico >= 500) and (x90x12 == 0 or x90x12 is None) and ((monthsBK >= 12 and bkChapter != 13) or monthsBK is None) and (monthsFC >= 12 or monthsFC is None):
		grade = "B-"
	elif (fico >= 500) and (x90x12 == 0 or x90x12 is None):
		grade = "C"
	else:
		grade = "N/A"

	if bkChapter != "N/A" and occupancy == "Primary":
		grade = "C"
	if bkChapter != "N/A" and occupancy == "Investor":
		grade = "B-"
	return grade

def getPIHousingEligibility(monthsBK, bkChapter, monthsDIL, monthsSS, monthsFC, x30x12, x60x12, x90x12, x30x24, x60x24, x90x24):
	if (x30x12 > 0) or (monthsBK <= 12 and bkChapter == 13 and monthsBK is not None) or (monthsBK < 36 and monthsBK is not None) or (monthsFC <= 36 and monthsFC is not None) or (monthsSS <= 24 and monthsSS is not None) or (monthsDIL <= 24 and monthsDIL is not None):
		return "Not Eligible"
	else:
		return "Eligible"

def getTier(state):
	if state in ("AK", "AL", "AR", "GA", "IA", "IN", "KS", "KY", "MO", "MS", "NC", "NE", "NH", "SC", "TN", "UT", "WA"):
		tier = "Tier 1"
	elif state in ("AZ", "CA", "CO", "DE", "FL", "HI", "ID", "IL", "LA", "MA", "ME", "MI", "MN", "ND", "NM", "NV", "OH", "OK", "OR", "PA", "RI", "TX", "VA", "WI", "WV", "WY"):
		tier = "Tier 2"
	else:
		tier = "Tier 3"

	return tier

def getDTIReservesEligibility(occupancy, doctype, ltv, dti, loanamount, reserves):
	result = "Eligible"
	if occupancy == "Primary":
		if doctype == "Full Doc":
			if ltv > 85:
				if loanamount <= 1000000:
					if dti > 43:
						result = "Not Eligible"
					else:
						if reserves < 6:
							result = "Not Eligible"
				else:
					result = "Not Eligible"
			else:
				if loanamount <= 1000000:
					if dti <= 43:
						if reserves <= 2:
							result = "Not Eligible"
					elif dti <= 50:
						if reserves <= 6:
							result = "Not Eligible"
					else:
						result = "Not Eligible"
				elif loanamount <= 1500000:
					if dti <= 43:
						if reserves <= 6:
							result = "Not Eligible"
					elif dti <= 50:
						if reserves <= 12:
							result = "Not Eligible"
					else:
						result = "Not Eligible"
				else:
					if dti <= 43:
						if reserves <= 9:
							result = "Not Eligible"
					elif dti <= 50:
						if reserves <= 18:
							result = "Not Eligible"
					else:
						result = "Not Eligible"
		elif doctype == "24 Mo Bank Statement":
			if loanamount <= 1000000:
				if dti <= 43:
					if reserves <= 6:
						result = "Not Eligible"
				elif dti <= 50:
					if reserves <= 12:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			elif loanamount <= 1500000:
				if dti <= 43:
					if reserves <= 9:
						result = "Not Eligible"
				elif dti <= 50:
					if reserves <= 18:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			else:
				if dti <= 43:
					if reserves <= 12:
						result = "Not Eligible"
				elif dti <= 50:
					if reserves <= 24:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
		elif doctype == "12 Mo Bank Statement":
			if loanamount <= 1000000:
				if dti <= 36:
					if reserves <= 24:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			elif loanamount <= 1500000:
				if dti <= 36:
					if reserves <= 24:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			else:
				result = "Not Eligible"
		elif doctype == "Asset Utilization":
			if loanamount <= 1000000:
				if dti <= 43:
					if reserves <= 6:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			else:
				result = "Not Eligible"

	elif occupancy == "2nd Home":
		if doctype == "Full Doc":
			if loanamount <= 1000000:
				if dti <= 43:
					if reserves <= 6:
						result = "Not Eligible"
				elif dti <= 50:
					if reserves <= 12:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			elif loanamount <= 1500000:
				if dti <= 43:
					if reserves <= 12:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			else:
				if dti <= 43:
					if reserves <= 15:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
		elif doctype == "24 Mo Bank Statement":
			if loanamount <= 1000000:
				if dti <= 43:
					if reserves <= 9:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			elif loanamount <= 1500000:
				if dti <= 43:
					if reserves <= 12:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			else:
				if dti <= 43:
					if reserves <= 15:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
		elif doctype == "12 Mo Bank Statement":
			if loanamount <= 1000000:
				if dti <= 36:
					if reserves <= 24:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			elif loanamount <= 1500000:
				if dti <= 36:
					if reserves <= 24:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			else:
				result = "Not Eligible"
		elif doctype == "Asset Utilization":
			if loanamount <= 1000000:
				if dti <= 43:
					if reserves <= 9:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			else:
				result = "Not Eligible"

	elif occupancy == "Investor":
		if doctype == "Full Doc":
			if loanamount <= 1000000:
				if dti <= 43:
					if reserves <= 6:
						result = "Not Eligible"
				elif dti <= 50:
					if reserves <= 12:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			elif loanamount <= 1500000:
				if dti <= 43:
					if reserves <= 12:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
		elif doctype == "24 Mo Bank Statement":
			if loanamount <= 1000000:
				if dti <= 43:
					if reserves <= 9:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			elif loanamount <= 1500000:
				if dti <= 43:
					if reserves <= 12:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
		elif doctype == "12 Mo Bank Statement":
			if loanamount <= 1000000:
				if dti <= 36:
					if reserves <= 24:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			elif loanamount <= 1500000:
				if dti <= 36:
					if reserves <= 24:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
		elif doctype == "Asset Utilization":
			if loanamount <= 1000000:
				if dti <= 43:
					if reserves <= 9:
						result = "Not Eligible"
				else:
					result = "Not Eligible"
			else:
				result = "Not Eligible"
	return result

				
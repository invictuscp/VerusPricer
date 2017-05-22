from django import forms

from pricer.models import Pricer

FICOS = (("740+", "740+"),
		("720-739", "720-739"),
		("700-719", "700-719"),
		("680-699", "680-699"),
		("660-679", "660-679"),
		("640-659", "640-659"),
		("620-639", "620-639"),
		("600-619", "600-619"),
		("580-599", "580-599"),
		("560-579", "560-579"),
		("540-559", "540-559"),
		("520-539", "520-539"),
		("500-519", "500-519"),
		("Foreign Credit", "Foreign Credit"))

LTVS = (("<=55", "<=55"),
		("55.01-60", "55.01-60"),
		("60.01-65", "60.01-65"),
		("65.01-70", "65.01-70"),
		("70.01-75", "70.01-75"),
		("75.01-80", "75.01-80"),
		("80.01-85", "80.01-85"),
		("85.01-90", "85.01-90"))

FLAGYN = (("No", "No"), ("Yes", "Yes"))

DOCS = (("Full Doc", "Full Doc"),
		("24 Mo Bank Statement", "24 Mo Bank Statement"),
		("12 Mo Bank Statement", "12 Mo Bank Statement"),
		("Asset Utilization", "Asset Utilization"),
		("DSCR", "DSCR"))

DTIS = (("<= 36%", "<= 36%"), ("36.01% - 43%", "36.01% - 43%"), ("43.01% - 50%", "43.01% - 50%"), ("> 50%", "> 50%"), ("N/A", "N/A"))

LOANSIZES = (("< $100,000", "< $100,000"),
			("$100,000 - $149,999", "$100,000 - $149,999"),
			("$150,000 - $399,999", "$150,000 - $399,999"),
			("$400,000 - $499,999", "$400,000 - $499,999"),
			("$500,000 - $749,999", "$500,000 - $749,999"),
			("$750,000 - $799,999", "$750,000 - $799,999"),
			("$800,000 - $999,999", "$800,000 - $999,999"),
			("$1,000,000 - $1,249,999", "$1,000,000 - $1,249,999"),
			("$1,250,000 - $1,499,999", "$1,250,000 - $1,499,999"),
			("$1,500,000 - $2,000,000", "$1,500,000 - $2,000,000"))

PURPOSES = (("Purchase", "Purchase"), ("Cash Out Refinance", "Cash Out Refinance"), ("Rate/Term Refinance", "Rate/Term Refinance"))

OCCS = (("Primary", "Primary"), ("2nd Home", "2nd Home"), ("Investor", "Investor"))

PROPTYPES = (("PUD", "PUD"), ("SFR", "SFR"), ("2-4 Unit", "2-4 Unit"), ("Condo", "Condo"), ("Non-Warrantable Condo", "Non-Warrantable Condo"))

STATES = (("AL", "AL"), ("AK", "AK"), ("AZ", "AZ"), ("AR", "AR"), ("CA", "CA"), ("CO", "CO"), ("CT", "CT"), ("DE", "DE"), ("FL", "FL"), ("GA", "GA"),
			("HI", "HI"), ("ID", "ID"), ("IL", "IL"), ("IN", "IN"), ("IA", "IA"), ("KS", "KS"), ("KY", "KY"), ("LA", "LA"), ("ME", "ME"), ("MD", "MD"),
			("MA", "MA"), ("MI", "MI"), ("MN", "MN"), ("MS", "MS"), ("MO", "MO"), ("MT", "MT"), ("NE", "NE"), ("NV", "NV"), ("NH", "NH"), ("NJ", "NJ"),
			("NM", "NM"), ("NY", "NY"), ("NC", "NC"), ("ND", "ND"), ("OH", "OH"), ("OK", "OK"), ("OR", "OR"), ("PA", "PA"), ("RI", "RI"), ("SC", "SC"),
			("SD", "SD"), ("TN", "TN"), ("TX", "TX"), ("UT", "UT"), ("VT", "VT"), ("VA", "VA"), ("WA", "WA"), ("WV", "WV"), ("WI", "WI"), ("WY", "WY"))

TERMS = (("3/1 ARM", "3/1 ARM"), ("5/1 ARM", "5/1 ARM"), ("7/1 ARM", "7/1 ARM"), ("15 Yr Fix", "15 Yr Fix"), ("30 Yr Fix", "30 Yr Fix"))

PREPAYS = (("No Penalty", "No Penalty"), ("12 Months", "12 Months"), ("24 Months", "24 Months"), ("36 Months", "36 Months"))

RESERVES = (("None", "None"), ("< 6 Months", "< 6 Months"), ("6 - 11 Months", "6 - 11 Months"), ("12 - 17 Months", "12 - 17 Months"), ("18 - 23 Months", "18 - 23 Months"), (">= 24 Months", ">= 24 Months"))

CHAPTERS = (("N/A", "N/A"), ("Chapter 7", "Chapter 7"), ("Chapter 11", "Chapter 11"), ("Chapter 13", "Chapter 13"), ("Other", "Other"))

DSCRS = (("N/A", "N/A"), ("< 1.15", "< 1.15"), ("1.15 - 1.24", "1.15 - 1.24"), ("1.25 - 1.29", "1.25 - 1.29"), (">= 1.30", ">= 1.30"))


class PricerForm(forms.ModelForm):
	fico = forms.ChoiceField(choices=FICOS, label = "FICO", widget=forms.Select(attrs={'class':'regDropDown'}))
	ltv = forms.ChoiceField(choices=LTVS, label = "LTV", widget=forms.Select(attrs={'class':'regDropDown'}))
	citizenship = forms.ChoiceField(choices=FLAGYN, label = "Foreign National", widget=forms.Select(attrs={'class':'regDropDown'}))
	seflag = forms.ChoiceField(choices=FLAGYN, label = "Self Employed", widget=forms.Select(attrs={'class':'regDropDown'}))
	fthbflag = forms.ChoiceField(choices=FLAGYN, label = "First Time Home Buyer", widget=forms.Select(attrs={'class':'regDropDown'}))
	doctype = forms.ChoiceField(choices=DOCS, label = "Documentation Type", widget=forms.Select(attrs={'class':'regDropDown'}))
	dti = forms.ChoiceField(choices=DTIS, label = "DTI", widget=forms.Select(attrs={'class':'regDropDown'}))
	loanamount = forms.ChoiceField(choices=LOANSIZES, label = "Loan Amount", widget=forms.Select(attrs={'class':'regDropDown'}))
	purpose = forms.ChoiceField(choices=PURPOSES, label = "Loan Purpose", widget=forms.Select(attrs={'class':'regDropDown'}))
	state = forms.ChoiceField(choices=STATES, label = "State", widget=forms.Select(attrs={'class':'regDropDown'}))
	occupancy = forms.ChoiceField(choices=OCCS, label = "Occupancy", widget=forms.Select(attrs={'class':'regDropDown'}))
	propType = forms.ChoiceField(choices=PROPTYPES, label = "Property Type", widget=forms.Select(attrs={'class':'regDropDown'}))
	io = forms.ChoiceField(choices=FLAGYN, label = "IO", widget=forms.Select(attrs={'class':'regDropDown'}))
	term = forms.ChoiceField(choices=TERMS, label = "Loan Term", widget=forms.Select(attrs={'class':'regDropDown'}))
	prepay = forms.ChoiceField(choices = PREPAYS, label = "Prepayment Term", widget=forms.Select(attrs={'class':'regDropDown'}))
	reserves = forms.ChoiceField(choices = RESERVES, label = "Reserves", widget=forms.Select(attrs={'class':'regDropDown'}))
	dscr = forms.ChoiceField(choices = DSCRS, label = "DSCR", widget=forms.Select(attrs={'class':'regDropDown'}))
	x30x12 = forms.IntegerField(initial = 0, min_value = 0, label = "x30x12", widget=forms.NumberInput(attrs={'class':'regTextBox'}))
	x60x12 = forms.IntegerField(initial = 0, min_value = 0, label = "x60x12", widget=forms.NumberInput(attrs={'class':'regTextBox'}))
	x90x12 = forms.IntegerField(initial = 0, min_value = 0, label = "x90x12", widget=forms.NumberInput(attrs={'class':'regTextBox'}))
	x30x24 = forms.IntegerField(initial = 0, min_value = 0, label = "x30x24", widget=forms.NumberInput(attrs={'class':'regTextBox'}))
	x60x24 = forms.IntegerField(initial = 0, min_value = 0, label = "x60x24", widget=forms.NumberInput(attrs={'class':'regTextBox'}))
	x90x24 = forms.IntegerField(initial = 0, min_value = 0, label = "x90x24", widget=forms.NumberInput(attrs={'class':'regTextBox'}))
	monthsFC = forms.IntegerField(required = False, min_value = 0, label = "Months since Foreclosure", widget=forms.NumberInput(attrs={'class':'regTextBox'}))
	monthsSS = forms.IntegerField(required = False, min_value = 0, label = "Months since Short Sale", widget=forms.NumberInput(attrs={'class':'regTextBox'}))
	monthsDIL = forms.IntegerField(required = False, min_value = 0, label = "Months since Deed-In-Lieu", widget=forms.NumberInput(attrs={'class':'regTextBox'}))
	monthsBK = forms.IntegerField(required = False, min_value = 0, label = "Months since Bankruptcy", widget=forms.NumberInput(attrs={'class':'regTextBox'}))
	bkChapter = forms.ChoiceField(choices = CHAPTERS, label = "Bankruptcy Chapter", widget=forms.Select(attrs={'class':'regDropDown2'}))
        
	class Meta:
		model = Pricer
		exclude = ('rate', 'eligibility')



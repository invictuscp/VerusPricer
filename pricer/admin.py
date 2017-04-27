from django.contrib import admin
from pricer.models import BaseRate, DocTypeAdj, DTIAdj, GradeAdj, IOAdj, LoanBalanceAdj
from pricer.models import LoanTermAdj, OccupancyAdj, PrepayAdj, PropertyTypeAdj, PurposeAdj
from pricer.models import ReservesAdj, StateAdj, Pricer, CAProductMatrix, FNProductMatrix, PIProductMatrix, DTIProductMatrix

# Register your models here.

admin.site.register(BaseRate)
admin.site.register(DocTypeAdj)
admin.site.register(DTIAdj)
admin.site.register(GradeAdj)
admin.site.register(IOAdj)
admin.site.register(LoanBalanceAdj)
admin.site.register(LoanTermAdj)
admin.site.register(OccupancyAdj)
admin.site.register(PrepayAdj)
admin.site.register(PropertyTypeAdj)
admin.site.register(PurposeAdj)
admin.site.register(ReservesAdj)
admin.site.register(StateAdj)
admin.site.register(Pricer)

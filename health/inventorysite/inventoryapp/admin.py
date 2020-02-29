from django.contrib import admin


from .models import Lender,Borrower

#class PlaceAdmin(admin.ModelAdmin):
#    list_display = ('product_name')



#admin.site.register(Lender,LenderAdmin)



admin.site.register(Lender)
admin.site.register(Borrower)	

from django.contrib import admin
from .models import TSJ, House, Flat, FlatTenant, FlatOwner, User, News, Request, HelpInfo, Voting

admin.site.register(User)
admin.site.register(Flat)
admin.site.register(FlatTenant)
admin.site.register(FlatOwner)
admin.site.register(House)
admin.site.register(TSJ)
admin.site.register(News)
admin.site.register(Request)
admin.site.register(HelpInfo)
admin.site.register(Voting)

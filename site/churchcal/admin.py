import calendar

from django.contrib import admin

from churchcal.models import Commemoration, SanctoraleCommemoration


class CommemorationAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "rank", "color", "calendar")
    search_fields = ("name",)
    list_filter = ("calendar", "rank", "color",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("rank", "calendar__denomination")
        return queryset

    def date(self, obj):
        if hasattr(obj, "month"):
            return "{}-{} {} {}".format(obj.month, obj.day, calendar.month_name[obj.month], obj.day)


class SanctoraleCommemorationAdmin(admin.ModelAdmin):
    list_display = ("name", "month", "day", "saint_type", "rank", "color", "calendar")

    search_fields = ("name",)
    list_filter = ("calendar", "saint_type", "rank", "color",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("rank", "calendar__denomination")
        return queryset

    def date(self, obj):
        if hasattr(obj, "month"):
            return "{}-{} {} {}".format(obj.month, obj.day, calendar.month_name[obj.month], obj.day)


admin.site.register(Commemoration, CommemorationAdmin)
admin.site.register(SanctoraleCommemoration, SanctoraleCommemorationAdmin)

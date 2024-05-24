# # -*- coding: utf-8 -*-
# from django.contrib import admin
# from modeltranslation.admin import TranslationAdmin
# from .models import TSJ, House, News, Vote, Request_Vote_News
#
#
# class TSJAdmin(TranslationAdmin):
#     list_display = ('name',)
#
#
# class HouseAdmin(TranslationAdmin):
#     list_display = ('name_block', 'address',)
#
#
# class NewsAdmin(TranslationAdmin):
#     list_display = ('title', 'tsj', 'type', 'view_count', 'created_date')
#
#
# class VoteAdmin(TranslationAdmin):
#     list_display = ('title', 'tjs', 'created_date', 'deadline', 'yes_count', 'no_count')
#
#
# class RequestVoteNewsAdmin(TranslationAdmin):
#     list_display = ('title', 'tsj', 'user', 'choice', 'created_date', 'status')
#
#
# admin.site.register(TSJ, TSJAdmin)
# admin.site.register(House, HouseAdmin)
# admin.site.register(News, NewsAdmin)
# admin.site.register(Vote, VoteAdmin)
# admin.site.register(Request_Vote_News, RequestVoteNewsAdmin)

# -*- coding: utf-8 -*-
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import TSJ, House, News, Vote, Request_Vote_News

class TSJAdmin(TranslationAdmin):
    list_display = ('name',)

    class Media:
        js = (
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
        }

class HouseAdmin(TranslationAdmin):
    list_display = ('name_block', 'address',)

    class Media:
        js = (
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
        }

class NewsAdmin(TranslationAdmin):
    list_display = ('title', 'tsj', 'type', 'view_count', 'created_date')

    class Media:
        js = (
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
        }

class VoteAdmin(TranslationAdmin):
    list_display = ('title', 'tjs', 'created_date', 'deadline', 'yes_count', 'no_count')

    class Media:
        js = (
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
        }

class RequestVoteNewsAdmin(TranslationAdmin):
    list_display = ('title', 'tsj', 'user', 'choice', 'created_date', 'status')

    class Media:
        js = (
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(TSJ, TSJAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Request_Vote_News, RequestVoteNewsAdmin)

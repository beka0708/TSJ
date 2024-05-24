# translation.py

from modeltranslation.translator import translator, TranslationOptions

from .models import TSJ, House, FlatOwner, FlatTenant, ViewRecord, Request_Vote_News, Votes, Vote, News, Flat, \
    ApartmentHistory


class TSJTranslationOptions(TranslationOptions):
    fields = ('name',)


class HouseTranslationOptions(TranslationOptions):
    fields = ('name_block', 'address', 'geo_position',)


class FlatOwnerTranslationOptions(TranslationOptions):
    fields = ()


class FlatTenantTranslationOptions(TranslationOptions):
    fields = ()


class FlatTranslationOptions(TranslationOptions):
    fields = ()


class ApartmentHistoryTranslationOptions(TranslationOptions):
    fields = ('description',)


class NewsTranslationOptions(TranslationOptions):
    fields = ('type', 'title', 'description', 'link',)


class VoteTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


class VotesTranslationOptions(TranslationOptions):
    fields = ('vote',)


class RequestVoteNewsTranslationOptions(TranslationOptions):
    fields = ('choice', 'title', 'description', 'link', 'status',)


class ViewRecordTranslationOptions(TranslationOptions):
    fields = ('content_type',)


translator.register(TSJ, TSJTranslationOptions)
translator.register(House, HouseTranslationOptions)
translator.register(FlatOwner, FlatOwnerTranslationOptions)
translator.register(FlatTenant, FlatTenantTranslationOptions)
translator.register(Flat, FlatTranslationOptions)
translator.register(ApartmentHistory, ApartmentHistoryTranslationOptions)
translator.register(News, NewsTranslationOptions)
translator.register(Vote, VoteTranslationOptions)
translator.register(Votes, VotesTranslationOptions)
translator.register(Request_Vote_News, RequestVoteNewsTranslationOptions)
translator.register(ViewRecord, ViewRecordTranslationOptions)

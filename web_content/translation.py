from modeltranslation.translator import register, TranslationOptions

from web_content.models import ServiceType, Service


@register(ServiceType)
class ServiceTypeTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ("name", "description")

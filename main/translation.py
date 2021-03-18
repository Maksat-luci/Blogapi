from .models import Post
from modeltranslation.translator import translator,TranslationOptions

class PostTranslationOptions(TranslationOptions):
    fields = ('title','text')


translator.register(Post,PostTranslationOptions)


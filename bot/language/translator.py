from typing import Any

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub, TranslatorRunner


class LocalizedTranslator:
    translator: TranslatorRunner

    def __init__(self, translator: TranslatorRunner) -> None:
        self.translator = translator

    def get(self, key: str, **kwargs: Any) -> str:
        return self.translator.get(key, **kwargs)


class Translator:
    t_hub: TranslatorHub

    def __init__(self) -> None:
        self.t_hub = TranslatorHub(
            {"ru": ("ru", "en"), "en": ("en",)},
            [
                FluentTranslator(
                    "en",
                    translator=FluentBundle.from_files("en-US", filenames=["./bot/language/locales/en.ftl"]),
                ),
                FluentTranslator(
                    "ru",
                    translator=FluentBundle.from_files("ru-RU", filenames=["./bot/language/locales/ru.ftl"]),
                ),
            ],
            root_locale="en",
        )

    def __call__(self, language: str) -> LocalizedTranslator:
        return self.t_hub.get_translator_by_locale(language)

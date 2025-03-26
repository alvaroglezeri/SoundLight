import allin1.analyze
from allin1.typings import AnalysisResult


from typing import cast

from core.logger import LOG_CAT, Logger


class PhraseAnalysis():
    @staticmethod
    def getSections_AIO(filepath: str) -> AnalysisResult:
        """
        WRITE
        """
        # DOCUMENT: AIO does not support BinaryIO objects.

        Logger.log(LOG_CAT.INFO, 'Analyzing phrases with AIO...')
        result = allin1.analyze(
            filepath, out_dir='./output', keep_byproducts=True)

        # Either this or # type: ignore can be used to avoid warnings
        return cast(AnalysisResult, result)

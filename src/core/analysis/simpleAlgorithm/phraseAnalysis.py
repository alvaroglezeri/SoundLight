from allin1.analyze import analyze
from allin1.typings import AnalysisResult

from typing import cast
from pathlib import Path

from ...conf import Conf
from ...logger import LOG_CAT, Logger


class PhraseAnalysis():
    """Analyzes the song and divides it into functional segments (phrases).
    """

    @staticmethod
    def get_sections_aio(filepath: str | Path) -> AnalysisResult:
        """Gets the song sections using AllIn1 AI analysis.

        Args:
            filepath (str | Path): Path to the file, as AllIn1 does not support BinaryIO objects.

        Returns:
            AnalysisResult: AllIn1 structure containing the analysis results.
        """

        Logger.log(LOG_CAT.INFO, 'Analyzing phrases with AIO...')

        try:
            options = Conf()['analysis']['simpleAlgorithm']['aio']
        except:
            raise ValueError(
                "Couldn't find [analysis.simpleAlgorithm.aio] in the configuration file")

        paths = filepath
        out_dir = options['out_dir'] if 'out_dir' in options else None
        visualize = options['visualize'] if 'visualize' in options else False
        sonify = options['sonify'] if 'sonify' in options else False
        # model: autoselect
        # device: autoselect
        include_activations = options['include_activations'] if 'include_activations' in options else False
        include_embeddings = options['include_embeddings'] if 'include_embeddings' in options else False
        demix_dir = options['demix_dir'] if 'demix_dir' in options else '/demix'
        # spec_dir: disabled
        # keep_byproducts must always be true, to keep the demixed audio for furter analysis
        keep_byproducts = True
        overwrite = options['overwrite'] if 'overwrite' in options else False
        multiprocess = options['multiprocess'] if 'multiprocess' in options else True

        result = analyze(
            paths=paths,
            out_dir=out_dir,
            visualize=visualize,
            sonify=sonify,
            include_activations=include_activations,
            include_embeddings=include_embeddings,
            demix_dir=demix_dir,
            keep_byproducts=keep_byproducts,
            overwrite=overwrite,
            multiprocess=multiprocess)

        return cast(AnalysisResult, result)

"""Parser package - modular pipeline for reading playerInfo.dat files.

Pipeline:
    playerInfo.dat
        └─ GzipParser       (decompress)
        └─ BinaryFormatter  (decode .NET BinaryFormatter stream)
        └─ ObjectGraph      (reconstruct Unity IL2CPP object graph)
        └─ Serializer       (map to Pydantic SaveData models)
"""

from tower_analyzer.parser.binary_formatter import BinaryFormatterParser
from tower_analyzer.parser.gzip_parser import GzipParser
from tower_analyzer.parser.object_graph import ObjectGraph
from tower_analyzer.parser.pipeline import ParserPipeline
from tower_analyzer.parser.serializer import SaveDataSerializer

__all__ = [
    "BinaryFormatterParser",
    "GzipParser",
    "ObjectGraph",
    "ParserPipeline",
    "SaveDataSerializer",
]

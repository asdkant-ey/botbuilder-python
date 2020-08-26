import re
from functools import lru_cache
from antlr4 import InputStream
from antlr4 import CommonTokenStream
from .generated.common_regexLexer import common_regexLexer
from .generated.common_regexParser import common_regexParser
from .regex_error_listener import RegexErrorListener


class CommonRegex:
    @staticmethod
    @lru_cache(15)
    def create_regex(pattern: str):
        if (pattern is None and len(pattern) == 0) or not CommonRegex.is_common_regex(
            pattern
        ):
            raise Exception("'{}' is not a valid regex.".format(pattern))
        return re.compile(pattern)

    @staticmethod
    def is_common_regex(pattern: str):
        try:
            CommonRegex.antlr_parse(pattern)
        except:
            return False
        return True

    @staticmethod
    def antlr_parse(pattern: str):
        input_stream = InputStream(pattern)
        lexer = common_regexLexer(input_stream)
        lexer.removeErrorListeners()
        token_stream = CommonTokenStream(lexer)
        parser = common_regexParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(RegexErrorListener())
        parser.buildParseTrees = True

        return parser.parse()

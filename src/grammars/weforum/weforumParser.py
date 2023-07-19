# Generated from weforumParser.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,6,25,2,0,7,0,2,1,7,1,1,0,4,0,6,8,0,11,0,12,0,7,1,1,3,1,11,8,
        1,1,1,4,1,14,8,1,11,1,12,1,15,1,1,1,1,3,1,20,8,1,1,1,3,1,23,8,1,
        1,1,0,0,2,0,2,0,0,27,0,5,1,0,0,0,2,10,1,0,0,0,4,6,3,2,1,0,5,4,1,
        0,0,0,6,7,1,0,0,0,7,5,1,0,0,0,7,8,1,0,0,0,8,1,1,0,0,0,9,11,5,1,0,
        0,10,9,1,0,0,0,10,11,1,0,0,0,11,13,1,0,0,0,12,14,5,2,0,0,13,12,1,
        0,0,0,14,15,1,0,0,0,15,13,1,0,0,0,15,16,1,0,0,0,16,17,1,0,0,0,17,
        19,5,3,0,0,18,20,5,4,0,0,19,18,1,0,0,0,19,20,1,0,0,0,20,22,1,0,0,
        0,21,23,5,5,0,0,22,21,1,0,0,0,22,23,1,0,0,0,23,3,1,0,0,0,5,7,10,
        15,19,22
    ]

class weforumParser ( Parser ):

    grammarFileName = "weforumParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "Topic", "Author", "Article", "TopicRef", 
                      "AuthorsRef", "ANY" ]

    RULE_r = 0
    RULE_article = 1

    ruleNames =  [ "r", "article" ]

    EOF = Token.EOF
    Topic=1
    Author=2
    Article=3
    TopicRef=4
    AuthorsRef=5
    ANY=6

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def article(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(weforumParser.ArticleContext)
            else:
                return self.getTypedRuleContext(weforumParser.ArticleContext,i)


        def getRuleIndex(self):
            return weforumParser.RULE_r

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterR" ):
                listener.enterR(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitR" ):
                listener.exitR(self)




    def r(self):

        localctx = weforumParser.RContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_r)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 5 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 4
                self.article()
                self.state = 7 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1 or _la==2):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArticleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Article(self):
            return self.getToken(weforumParser.Article, 0)

        def Topic(self):
            return self.getToken(weforumParser.Topic, 0)

        def Author(self, i:int=None):
            if i is None:
                return self.getTokens(weforumParser.Author)
            else:
                return self.getToken(weforumParser.Author, i)

        def TopicRef(self):
            return self.getToken(weforumParser.TopicRef, 0)

        def AuthorsRef(self):
            return self.getToken(weforumParser.AuthorsRef, 0)

        def getRuleIndex(self):
            return weforumParser.RULE_article

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArticle" ):
                listener.enterArticle(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArticle" ):
                listener.exitArticle(self)




    def article(self):

        localctx = weforumParser.ArticleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_article)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 9
                self.match(weforumParser.Topic)


            self.state = 13 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 12
                self.match(weforumParser.Author)
                self.state = 15 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==2):
                    break

            self.state = 17
            self.match(weforumParser.Article)
            self.state = 19
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 18
                self.match(weforumParser.TopicRef)


            self.state = 22
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 21
                self.match(weforumParser.AuthorsRef)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx






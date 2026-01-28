from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def summarize_text(text, sentences=2, language="english"):
    text = (text or "").strip()
    if not text:
        return ""
    try:
        parser = PlaintextParser.from_string(text, Tokenizer(language))
        summarizer = TextRankSummarizer()
        sents = summarizer(parser.document, sentences)
        return " ".join([str(s) for s in sents]) if sents else (text[:240] + ("..." if len(text)>240 else ""))
    except Exception:
        return text[:240]

"""Dependency-free transcript normalization without relaxing dialogue checks."""
import re
from types import SimpleNamespace

def normal(word):
    return re.sub(r'[^a-z0-9]', '', word.lower())

def merge_asr_words(heard, reference):
    """Join ASR token splits only when their exact letters match a script word.

    Wi + -Fi and C + E + O are formatting differences, never substitutions.
    Retain the full time interval for caption alignment.
    """
    vocabulary = {normal(w) for w in reference}
    merged = []
    i = 0
    while i < len(heard):
        end = i + 1
        joined = normal(heard[i].word)
        if joined not in vocabulary:
            for j in range(i + 1, min(i + 5, len(heard))):
                joined += normal(heard[j].word)
                if joined in vocabulary:
                    end = j + 1
                    break
        merged.append(SimpleNamespace(
            word=''.join(w.word.strip() for w in heard[i:end]),
            start=heard[i].start, end=heard[end-1].end))
        i = end
    return merged


def expand_asr_numbers(heard, reference):
    """Expand digit spellings only if the exact number words occur in the script.

    Preserve the recognized interval and divide it across equivalent written words.
    This does not accept a different number, insert omitted speech, or alter pronouns.
    """
    ones=['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
    tens=['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
    def spell(n):
        if n<20:return [ones[n]]
        if n<100:return [tens[n//10]]+(spell(n%10) if n%10 else [])
        for amount,label in [(10**9,'billion'),(10**6,'million'),(1000,'thousand'),(100,'hundred')]:
            if n>=amount:return spell(n//amount)+[label]+(spell(n%amount) if n%amount else [])
    refs=[normal(w) for w in reference];result=[]
    for word in heard:
        digits=word.word.strip().strip('.,!?;:').replace(',','')
        dollars=digits.startswith('$')
        if dollars: digits=digits[1:]
        percent=digits.endswith('%')
        if percent: digits=digits[:-1]
        expanded=spell(int(digits)) if digits.isdigit() and int(digits)<10**12 else None
        if expanded and percent: expanded=expanded+['percent']
        if expanded and dollars: expanded=expanded+['dollar' if int(digits)==1 else 'dollars']
        allowed=expanded and any(refs[i:i+len(expanded)]==expanded for i in range(len(refs)))
        if allowed:
            for j,w in enumerate(expanded):
                result.append(SimpleNamespace(word=w,start=word.start+(word.end-word.start)*j/len(expanded),end=word.start+(word.end-word.start)*(j+1)/len(expanded)))
        else:result.append(word)
    return result


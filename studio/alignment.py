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


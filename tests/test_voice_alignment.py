import sys, unittest
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'studio'))
from alignment import merge_asr_words, normal, expand_asr_numbers

def heard(words):
    return [SimpleNamespace(word=w,start=i*.2,end=(i+1)*.2) for i,w in enumerate(words)]

class AlignmentTests(unittest.TestCase):
    def test_number_formatting_is_equivalent(self):
        result=expand_asr_numbers(heard(['24','hours']), ['twenty','four','hours'])
        self.assertEqual([w.word for w in result],['twenty','four','hours'])
        self.assertEqual(result[0].start,0)
        self.assertEqual(result[1].end,.2)
    def test_different_number_not_accepted(self):
        result=expand_asr_numbers(heard(['25','hours']), ['twenty','four','hours'])
        self.assertEqual(result[0].word,'25')
    def test_wifi_split_and_timestamps(self):
        result=merge_asr_words(heard(['Vote','A','blame','Wi','-Fi','B','let','Dino','talk']), 'Vote A: blame Wi-Fi! B: let Dino talk!'.split())
        self.assertEqual([normal(w.word) for w in result], ['vote','a','blame','wifi','b','let','dino','talk'])
        self.assertAlmostEqual(result[3].start,.6)
        self.assertAlmostEqual(result[3].end,1.)
    def test_wrong_pronoun_still_rejected(self):
        result=merge_asr_words(heard(['You',"can't",'even','wear','pants']), "He can't even wear pants!".split())
        self.assertNotEqual([normal(w.word) for w in result], ['he','cant','even','wear','pants'])
    def test_missing_word_not_invented(self):
        result=merge_asr_words(heard(['let','talk']), ['let','Dino','talk'])
        self.assertEqual([w.word for w in result], ['let','talk'])
    def test_exact_words_keep_separate(self):
        result=merge_asr_words(heard(['a','part']), ['a','part','apart'])
        self.assertEqual(len(result),2)

if __name__=='__main__': unittest.main()

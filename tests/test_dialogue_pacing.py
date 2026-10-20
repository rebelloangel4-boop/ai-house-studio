import sys, unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'studio'))
from render import SR, polish_dialogue, caption_at, mix

class PacingTests(unittest.TestCase):
    def test_trim_and_tempo_preserve_all_word_intervals(self):
        t=np.arange(SR)/SR
        audio=np.concatenate([np.zeros(SR//3),.12*np.sin(2*np.pi*220*t),np.zeros(SR//2)]).astype(np.float32)
        tokens=[{'text':'Hello','phonemes':'hello','start':1/3,'end':.8},
                {'text':'there','phonemes':'there','start':.8,'end':4/3}]
        result,aligned,report=polish_dialogue(audio,tokens,'Zig')
        self.assertEqual([q['text'] for q in aligned],['Hello','there'])
        self.assertLess(len(result),len(audio))
        self.assertGreater(len(result)/SR,.9)
        self.assertGreater(report['trimmed_seconds'],.5)
        self.assertTrue(all(0<=q['start']<q['end']<=len(result)/SR for q in aligned))

    def test_caption_clears_during_long_pause(self):
        tokens=[{'text':w,'start':i*.1,'end':i*.1+.08} for i,w in enumerate('one two three four five'.split())]
        tokens[-1].update(start=2.,end=2.2)
        self.assertEqual(caption_at(tokens,.15),'one two three four')
        self.assertEqual(caption_at(tokens,1.),'')
        self.assertEqual(caption_at(tokens,2.1),'five')

    def test_silent_dialogue_is_rejected(self):
        with self.assertRaises(ValueError):
            polish_dialogue(np.zeros(SR),[{'start':0,'end':.5}],'Luna')

if __name__=='__main__':unittest.main()

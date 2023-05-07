import os
os.environ["XDG_CACHE_HOME"] = r"/Users/lizi/Desktop/GithubWorks/[models]";
#os.environ["SUNO_ENABLE_MPS"] = "True"
os.environ["SUNO_OFFLOAD_CPU"] = "False"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"
os.environ["CUDA_VISIBLE_DEVICES"] = "False"

from bark import SAMPLE_RATE, generate_audio
from scipy.io.wavfile import write as write_wav

from bark.api import semantic_to_waveform
from bark.generation import generate_text_semantic

import nltk
import numpy as np
import subprocess

# download and load all models
preload_models()
nltk.download('punkt')

# generate audio from text
script = """
Hey, have you heard about this new text-to-audio model called "Bark"? 
Apparently, it's the most realistic and natural-sounding text-to-audio model 
out there right now. People are saying it sounds just like a real person speaking. 
I think it uses advanced machine learning algorithms to analyze and understand the 
nuances of human speech, and then replicates those nuances in its own speech output. 
It's pretty impressive, and I bet it could be used for things like audiobooks or podcasts. 
In fact, I heard that some publishers are already starting to use Bark to create audiobooks. 
It would be like having your own personal voiceover artist. I really think Bark is going to 
be a game-changer in the world of text-to-audio technology.
""".replace("\n", " ").strip()

script = """
In my younger and more vulnerable years my father gave me some advice that I’ve been turning over in my mind ever since.
"Whenever you feel like criticizing any one,” he told me, “just remember that all the people in this world haven’t had
the advantages that you’ve had." He didn’t say any more, but we’ve always been unusually communicative in a reserved way, 
and I understood that he meant a great deal more than that.
""".replace("\n", " ").strip()

sentences = nltk.sent_tokenize(script)

SPEAKER = "v2/en_speaker_0"
silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence
print('Size========>>>', len(sentences))

pieces = [] # total audios
for index, sentence in enumerate(sentences):
     print('Fxkk========>>>', index)
     semantic_tokens = generate_text_semantic(
          sentence,
          history_prompt = SPEAKER,
          temp = 0.6,
          min_eos_p = 0.05, # this controls how likely the generation is to end
     )
     #audio_array = generate_audio(sentence, history_prompt=SPEAKER)
     audio_array = semantic_to_waveform(semantic_tokens, history_prompt=SPEAKER)
     pieces += [audio_array, silence.copy()]
     #if index >= 2: break

# save audio to disk
filename = "bark_generation.wav"
write_wav(filename, SAMPLE_RATE, np.concatenate(pieces))

cmd = ['ffplay', filename, '-autoexit']
subprocess.run(cmd, shell=False)

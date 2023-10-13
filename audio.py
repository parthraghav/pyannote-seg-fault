import faulthandler
faulthandler.enable()
from pyannote.audio import Pipeline

# the following line throws a segmentation fault
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.0", use_auth_token="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")
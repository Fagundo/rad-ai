#!/bin/bash

# A bit hacky, but lets encapsulate the model download in the dockerfile buid 
# Because it is so large, it makes sense to get from huggingface now
echo Downloading google/pegasus-newsroom from HugginFace
echo this may take 5 minutes ....

python - <<-EOF
from transformers import pipeline
pipe = pipeline(model='facebook/bart-large-cnn')
EOF

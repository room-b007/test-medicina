#!/bin/bash

# Model to evaluate: meta-llama/Meta-Llama-3.1-8B-Instruct (in bfloat16)
MODEL_ARGS="pretrained=meta-llama/Meta-Llama-3.1-8B-Instruct,dtype=bfloat16"

# Evaluate the model on both multiple-choice and cloze-style formats
TASKS="medschool_test_it_mc,medschool_test_it_cloze"

# Create the output directory if it does not exist
OUTPUT_DIR="outputs/"
mkdir -p $OUTPUT_DIR

# Run the evaluation with the lm-evaluation-harness library
accelerate launch -m lm_eval \
  --model hf \
  --model_args $MODEL_ARGS \
  --tasks $TASKS \
  --batch_size auto \
  --log_samples \
  --output_path $OUTPUT_DIR \
  --include tasks/medschool-test/

from pprint import pprint
import functools

import torch
from torch.utils.data import DataLoader
import torch.nn.functional as F
import pytorch_lightning as pl
from transformers import AutoModelForSequenceClassification, CamembertForMaskedLM, AutoTokenizer, AutoConfig
from datasets import load_dataset
from sklearn.metrics import confusion_matrix, f1_score

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from tqdm.notebook import tqdm

camembert = CamembertForMaskedLM.from_pretrained('camembert-base')

batch_sentences = [
    "Vous savez où est la <mask> la plus proche?",
    "La Seine est un <mask>.",
    "Je cherche urgemment un endroit où retirer de l'<mask>.",
]

tokenizer = AutoTokenizer.from_pretrained('camembert-base')

tokenizer_output = tokenizer(
    batch_sentences,
    padding="max_length",
    truncation=True,
    return_tensors="pt"
)

#pprint(tokenizer_output, width=150)
#pprint([tokenizer.convert_ids_to_tokens(input_ids) for input_ids in tokenizer_output['input_ids']], width=150)
#pprint(tokenizer_output, compact=True, width=150)

with torch.no_grad():
    model_output = camembert(**tokenizer_output, output_hidden_states=True)

pprint(model_output, compact=True, width=150)
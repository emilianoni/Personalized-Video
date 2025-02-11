import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification
from torch.utils.data import DataLoader

def load_data(file_path):
    """
    Load the Excel file and return the data as a DataFrame.

    :param file_path: Path to the Excel file containing the data.
    :return: A pandas DataFrame with the loaded data.
    """
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return None

def get_unique_subheaders(data, cif):
    """
    Retrieve unique SUBHEADER values based on the given CIF and specific TRX_TYPE conditions.

    :param data: The pandas DataFrame containing the data.
    :param cif: The CIF value to filter the data.
    :return: A list of unique SUBHEADER values that match the criteria.
    """
    try:
        # Filter the data based on CIF and TRX_TYPE conditions
        filtered_data = data[
            (data['CIF'] == cif) &
            ((data['TRX_TYPE'] == 'Pembayaran') | (data['TRX_TYPE'] == 'Pembayaran Qris'))
        ]

        # Load Model & Tokenizer (Replace with your model)
        model_name = "./model_NER/model/NER_merchant"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForTokenClassification.from_pretrained(model_name)
        model.eval()

        class PredictionDataset(torch.utils.data.Dataset):
            def __init__(self, sentences):
                self.inputs = tokenizer(
                    sentences, 
                    padding=True,
                    truncation=True,
                    return_tensors="pt"
                )

            def __len__(self):
                return len(self.inputs["input_ids"])

            def __getitem__(self, idx):
                return {key: val[idx] for key, val in self.inputs.items()}


        sentences = filtered_data['SUBHEADER'].tolist()
        dataset = PredictionDataset(sentences)
        dataloader = DataLoader(dataset, batch_size=1)

        merchant_names = []

        with torch.no_grad():
            for batch in dataloader:
                inputs = {k: v.to(model.device) for k, v in batch.items()}
                outputs = model(**inputs)
                logits = outputs.logits
                predictions = torch.argmax(logits, dim=-1).cpu().numpy()[0]

                tokens = tokenizer.convert_ids_to_tokens(batch["input_ids"][0])
                merchant_words = []

                for token, label in zip(tokens, predictions):
                    entity = model.config.id2label[label]  # Convert label ID to entity name

                    if entity == "ORG" and token not in ["[CLS]", "[SEP]", "[PAD]"]:
                        token = token.replace("▁", "")  # Remove BPE markers
                        
                        # Handle subword merging safely
                        if token.startswith("##") and merchant_words:
                            merchant_words[-1] += token[2:]  # Merge subwords
                        else:
                            merchant_words.append(token)

                merchant_names.append(" ".join(merchant_words).strip())  # Clean up spaces

        filtered_data["merchant_name"] = merchant_names

        # Return unique SUBHEADER values
        return filtered_data['merchant_name'].unique().tolist()
    except Exception as e:
        print(f"An error occurred during data filtering: {e}")
        return []

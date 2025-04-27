from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Use a fine-tuned BERT model for fact checking
tokenizer = AutoTokenizer.from_pretrained("mrm8488/bert-tiny-finetuned-fake-news-detection")
model = AutoModelForSequenceClassification.from_pretrained("mrm8488/bert-tiny-finetuned-fake-news-detection")

def bert_fact_check(claim, articles):
    if not articles:
        return [{"evidence": "No evidence found.", "label": "❌ Likely False", "score": 0.0}]
    
    inputs = tokenizer([claim] * len(articles), articles, return_tensors='pt', padding=True, truncation=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=1)
    
    results = []
    for i, prediction in enumerate(predictions):
        evidence = articles[i]
        label = "✅ Likely True" if prediction[1] > prediction[0] else "❌ Likely False"
        score = round(torch.max(prediction).item(), 2)
        
        results.append({
            "evidence": evidence,
            "label": label,
            "score": score
        })
    
    return results

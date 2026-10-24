
_lm = None


def _get_lm():
    global _lm
    if _lm is None:
        from transformers import AutoModelForCausalLM, AutoTokenizer

        tok = AutoTokenizer.from_pretrained("distilgpt2")
        model = AutoModelForCausalLM.from_pretrained("distilgpt2")
        model.eval()
        _lm = (tok, model)
    return _lm


def sentence_score(text):
    import torch
    """Higher = the sentence sounds more natural (log-probability)."""
    tok, model = _get_lm()
    ids = tok(tok.bos_token + text, return_tensors="pt").input_ids
    with torch.no_grad():
        loss = model(ids, labels=ids).loss.item()
    return -loss * (ids.shape[1] - 1)
from bson import ObjectId

def to_str_id(doc):
    if not doc: return doc
    out = {}
    for k, v in doc.items():
        if isinstance(v, ObjectId): out[k] = str(v)
        else: out[k] = v
    return out

def to_str_list(docs):
    return [to_str_id(d) for d in docs]

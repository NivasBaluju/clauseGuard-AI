import urllib.request
import mimetypes
import uuid
import json
import time

def upload_and_audit(filepath, doc_type):
    url = "http://127.0.0.1:5000/api/documents"
    boundary = uuid.uuid4().hex
    body = []
    
    # document_type field
    body.append(f"--{boundary}".encode())
    body.append(b'Content-Disposition: form-data; name="document_type"')
    body.append(b"")
    body.append(doc_type.encode())

    # file field
    body.append(f"--{boundary}".encode())
    body.append(f'Content-Disposition: form-data; name="file"; filename="{filepath.split("/")[-1]}"'.encode())
    body.append(b"Content-Type: text/plain")
    body.append(b"")
    with open(filepath, "rb") as f:
        body.append(f.read())
        
    body.append(f"--{boundary}--".encode())
    body.append(b"")

    payload = b"\r\n".join(body)
    req = urllib.request.Request(url, data=payload)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    print(f"Uploading {filepath} as {doc_type}...")
    resp = urllib.request.urlopen(req)
    res_data = json.loads(resp.read().decode())
    print("Upload initiated:", res_data)
    doc_id = res_data.get("document_id") or res_data.get("id")

    # Poll status
    while True:
        time.sleep(2)
        status_resp = urllib.request.urlopen(f"http://127.0.0.1:5000/api/documents/{doc_id}/status")
        s_data = json.loads(status_resp.read().decode())
        print(f"  Stage: {s_data.get('processing_stage')} | Status: {s_data.get('status')}")
        if s_data["status"] in ("analyzed", "failed"):
            break

    if s_data["status"] == "failed":
        print("ERROR:", s_data.get("error_message"))
        return None

    doc_detail = json.loads(urllib.request.urlopen(f"http://127.0.0.1:5000/api/documents/{doc_id}").read().decode())
    print("\n=== AUDIT RESULTS ===")
    print(f"Overall Risk Score: {doc_detail['overall_risk_score']} | Band: {doc_detail['risk_band']}")
    print(f"Model Version: {doc_detail['model_version']}")

    clauses = json.loads(urllib.request.urlopen(f"http://127.0.0.1:5000/api/documents/{doc_id}/clauses").read().decode())
    print(f"Total Segmented Clauses: {len(clauses)}")
    for c in clauses[:6]:
        print(f"  [#{c['clause_index']+1}] {c['clause_type']} | Fav: {c['favorability_label']} ({c['favorability_confidence']:.2f}) | Risk: {c['risk_score']}")

    missing = json.loads(urllib.request.urlopen(f"http://127.0.0.1:5000/api/documents/{doc_id}/missing-clauses").read().decode())
    print(f"Missing Clauses: {len(missing)}")
    for m in missing:
        print(f"  Missing: {m['clause_type']} ({m['severity']})")

    deadlines = json.loads(urllib.request.urlopen(f"http://127.0.0.1:5000/api/documents/{doc_id}/deadlines").read().decode())
    print(f"Deadlines: {len(deadlines)}")
    for d in deadlines[:5]:
        print(f"  Deadline: {d['raw_text']} | Days: {d['relative_days']} | Conf: {d['confidence']}")

    pii = json.loads(urllib.request.urlopen(f"http://127.0.0.1:5000/api/documents/{doc_id}/pii-summary").read().decode())
    print(f"PII Redactions: {pii['total_findings']} entities -> {pii['entity_counts']}")

    # Test Grounded RAG Chat
    print("\n=== TESTING GROUNDED RAG CHAT ===")
    chat_url = f"http://127.0.0.1:5000/api/documents/{doc_id}/chat"
    chat_payload = json.dumps({"question": "How much advance notice is required before the landlord enters?"}).encode()
    chat_req = urllib.request.Request(chat_url, data=chat_payload, headers={"Content-Type": "application/json"})
    chat_resp = json.loads(urllib.request.urlopen(chat_req).read().decode())
    print("User Question: How much advance notice is required before the landlord enters?")
    print(f"AI Grounded Response:\n{chat_resp['answer']}")
    print(f"Grounded: {chat_resp['grounded']} | Cited Clauses: {chat_resp['cited_clause_ids']}")

    # Test PDF Report generation
    print("\n=== TESTING PDF REPORT GENERATION ===")
    pdf_resp = urllib.request.urlopen(f"http://127.0.0.1:5000/api/documents/{doc_id}/report.pdf")
    pdf_bytes = pdf_resp.read()
    print(f"PDF Report generated successfully! Size: {len(pdf_bytes)} bytes.")

    return doc_id

if __name__ == "__main__":
    upload_and_audit("sample_documents/sample_residential_lease.txt", "rental_agreement")

# 🚀 AWS IP Tracker

A tiny, serverless service that lets clients on **changing IPs** report their current address via HTTPS and lets you fetch each client’s **last 10 IPs**.

The advantages are very low operating costs and unlimited amount of clients.

---

## ✨ Main Features

- 🌐 **HTTPS** via Amazon API Gateway (HTTP API)
- 🐍 **AWS Lambda (Python)** for request handling
- 🗄️ **DynamoDB** stores the **last 10** IPs per client hash
- 🔐 **No auth** required (access controlled by unguessable hashes)
- 🧩 **Hard‑coded 8‑char uppercase hex** client hashes
- 🛠️ **Management endpoint** to retrieve recent IPs

---

## ⚙️ Prerequisites

- Ubuntu Linux
- **AWS CDK v2** and **Node.js LTS (≥ 18)** installed:  
  ```bash
  node -v
  cdk --version
  ```
- **Python 3.10+** and an AWS profile with deploy permissions.

---

## 🧰 Setup & Deployment

### 1) Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip wheel setuptools
pip install -r requirements.txt
```

### 2) Configure hashes (recommended)
Edit `ip_tracker_stack/ip_tracker_stack.py` and set:
- `HASH_LIST` — comma‑separated **8‑char uppercase hex** client hashes
- `MANAGE_HASH` — **management token** (8‑char uppercase hex recommended)

It is advisable, for security reasons, to modify the hashes at the lines starting with "HASH_LIST" and "MANAGE LIST":

Quick helpers to generate values:
 
- Run: `./gen_random_urls`
 - At the file `ip_tracker_stack/ip_tracker_stack.py' replace the two lines (near line 30) with the generated lines.


### 3) Deploy to AWS
```bash
cdk bootstrap
cdk deploy
```

After deploy, note the output:
```
Outputs:
IpTrackerStack.ApiUrl = https://<api-id>.execute-api.<region>.amazonaws.com
```
We’ll call this **API_URL** below.

Save this URL. You will use it in the next step.

---

### Create the `info.yaml` file

  - Rename `example_info.yaml to `info.yaml`
  - Replace the "base_url" and "manag_url" by the output of the previous step
  - Replace the hash (8 Hex digits) at the end of the management URL with the value generated earlier

### Sanity check

  Run './get_ips'. You should not get any errors

  There is no actual output yet, as we did not add any clients yet

## 🖥️ Client Setup

### Manually report the current IP 
Each client calls:
```bash
wget -qO- https://<API_URL>/<CLIENT_HASH>
```
The above can be used manually to verify operations.

Use `crontab -e` to enter something like the following to crontab:

Example cron entry (Will report IP every 4 hours):
```bash
0 */4 * * * wget https://abc123.execute-api.us-west-2.amazonaws.com/AB12CD34
```

Add the hash and the name of the client (E.g., host name) to the `info.yaml` file.

(This entry will enable the `get_ips` utility to show which client is associated with the hash)

## 📊 Management: View recent IPs

Simply run `./get_ips`

Example output:

```
paris           200.65.123.106  03Aug 16:00
brazil          61.132.222.24   03Aug 15:21
```

### Troubleshooting

To retrieve the last 10 logs per client hash:

```bash
curl https://<API_URL>/manage/<management hash>
```

You will receive a JSON list of records, each containing:
- `hash`
- `timestamp`
- `ip`

Example response (JSON array):
```json
[
  { "hash": "AB12CD34", "timestamp": "2025-08-03T15:21:00.123456", "ip": "61.132.222.24" },
  { "hash": "AB12CD34", "timestamp": "2025-08-03T12:05:48.554321", "ip": "61.132.222.24" }
]
```


## License

This project is licensed under the [MIT License](LICENSE).

---

**Author:** Shalom Mitz  
**Credits:** Generated with help from ChatGPT (OpenAI)

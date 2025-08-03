# AWS IP Tracker

This project provides an AWS-based service that allows clients with changing IP addresses to report their IP to a centralized location. It also enables retrieval of the last 10 IPs per client via a management endpoint.

## Features

- HTTPS via API Gateway
- Lambda (Python) to log IP changes
- DynamoDB to store latest 10 IPs per client hash
- No authentication
- Hard-coded list of allowed 8-digit uppercase hex hashes
- Management endpoint for viewing the full log

## Deployment Instructions

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip wheel setuptools
pip install -r requirements.txt
cdk bootstrap
cdk deploy
```
It is advisable, for security reasons, to modify the hashes at the lines starting with "HASH_LIST" and "MANAGE LIST":

 - Run: `./gen_random_urls`
 - Replace the two generated lines with the generated lines


After deploying, CDK will output a URL like:

```
Outputs:
IpTrackerStack.ApiUrl = https://<api-id>.execute-api.<region>.amazonaws.com
```

Save this URL. You will use it in the next step.

## Usage

### Client Reporting (e.g. via cronjob)
Each client sends a request using its assigned hash (e.g. `AB12CD34`):

```bash
wget https://<API_URL>/<HASH>
```

Example:

```bash
wget https://abc123.execute-api.us-west-2.amazonaws.com/AB12CD34
```

### Management Access

To retrieve the last 10 logs per client hash:

```bash
curl https://<API_URL>/manage/ADMIN123
```

You will receive a JSON list of records, each containing:
- `hash`
- `timestamp`
- `ip`

## License

This project is licensed under the [MIT License](LICENSE).

---

**Author:** Shalom Mitz  
**Credits:** Generated with help from ChatGPT (OpenAI)

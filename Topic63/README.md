---
title: "Google Cloud Pentesting"
topic: "google-cloud-pentesting"
tags: [gcp, google-cloud, pentesting, storage, gsutil, iam, cloud-security]
difficulty: advanced
day: 63
layout: default
parent: Topics
nav_order: 63
---

# Google Cloud Pentesting

## What You Will Learn
- How Google Cloud Storage (GCS) works and common misconfigurations
- How to enumerate GCP resources with the `gsutil` and `gcloud` tools
- How to check for publicly accessible buckets
- Common GCP attack paths

## What Is It?

**Google Cloud Platform (GCP)** is Google's cloud infrastructure. GCP includes compute (GCE), storage (GCS), serverless (Cloud Functions, Cloud Run), and many other services.

GCP pentesting focuses on misconfigured IAM permissions, public storage buckets, exposed service account keys, and metadata endpoint abuse.

## Why It Matters

GCP misconfigurations are regularly found in bug bounty programs. Publicly accessible Cloud Storage buckets have exposed sensitive data from many major organizations.

## Google Cloud Storage

### List Bucket Contents

```bash
# List all files in a bucket
gsutil ls gs://<storage_name>

# List recursively
gsutil ls -r gs://<storage_name>

# Verify a specific file
gsutil stat gs://<storage_name>/<file>

# Download a file
gsutil cp gs://<storage_name>/<file> ./local_copy

# Download everything
gsutil cp -r gs://<storage_name> ./local_copy
```

### Check Bucket ACL

```bash
# Check if bucket is publicly readable
gsutil acl get gs://<bucket_name>

# Try to access an anonymous bucket
gsutil ls gs://target-bucket --no-auth
curl "https://storage.googleapis.com/<bucket_name>/<file>"
```

### Finding Public Buckets

```bash
# Google Dork
site:storage.googleapis.com target

# Try common bucket names
for name in backup data assets files config; do
  gsutil ls gs://target-$name 2>/dev/null && echo "Found: target-$name"
done

# GCPBucketBrute
python3 GCPBucketBrute.py --keyword targetname
```

## GCP Enumeration with Credentials

```bash
# Authenticate
gcloud auth login
gcloud auth activate-service-account --key-file=service_account.json

# List projects
gcloud projects list

# Set default project
gcloud config set project <project-id>

# List compute instances
gcloud compute instances list

# List Cloud Functions
gcloud functions list

# List Cloud Run services
gcloud run services list

# List storage buckets
gcloud storage ls

# List service accounts
gcloud iam service-accounts list
```

## IAM Enumeration

```bash
# Get IAM policy for a project
gcloud projects get-iam-policy <project-id>

# Get IAM policy for a specific resource
gcloud storage buckets get-iam-policy gs://<bucket>

# List roles
gcloud iam roles list --project <project-id>

# Check your own permissions
gcloud auth list
```

## Metadata Endpoint

The GCE metadata endpoint is only accessible from inside a GCP instance. It can reveal service account tokens:

```bash
# Access metadata from inside a GCE instance
curl "http://metadata.google.internal/computeMetadata/v1/instance/" \
  -H "Metadata-Flavor: Google"

# Get service account token
curl "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token" \
  -H "Metadata-Flavor: Google"
```

## Common GCP Attack Paths

1. **Public GCS bucket** → download sensitive files
2. **Overprivileged service account key in source code** → full project access
3. **SSRF to metadata endpoint** → steal service account token
4. **Cloud Function with SSRF** → access internal services
5. **Misconfigured Cloud Run service** → access internal APIs without auth

## Resources

- [HackTricks — GCP Pentesting](https://cloud.hacktricks.xyz/pentesting-cloud/gcp-security)
- [GCPBucketBrute — Bucket Discovery](https://github.com/RhinoSecurityLabs/GCPBucketBrute)
- [GCP Metadata Documentation](https://cloud.google.com/compute/docs/metadata/overview)
- [TryHackMe — Cloud Security](https://tryhackme.com/)
- [Google Cloud Security Command Center](https://cloud.google.com/security-command-center)

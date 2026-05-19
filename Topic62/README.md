---
title: "Azure Cloud Pentesting"
topic: "azure-pentesting"
tags: [azure, cloud, pentesting, blob-storage, microsoft, enumeration, credentials]
difficulty: advanced
day: 62
layout: default
parent: Topics
nav_order: 62
---

# Azure Cloud Pentesting

## What You Will Learn
- How Azure Blob Storage works and common misconfigurations
- How to enumerate Azure resources with leaked credentials
- How to check for publicly accessible Azure storage
- Common Azure attack paths

## What Is It?

**Microsoft Azure** is one of the major cloud providers alongside AWS and Google Cloud. Azure has its own set of services, authentication mechanisms, and common misconfigurations.

Azure pentesting follows a similar methodology to AWS: start with enumeration, look for overprivileged roles, and explore storage services for exposed data.

## Why It Matters

Organizations increasingly store sensitive data in Azure. Misconfigurations in Blob Storage, Azure Active Directory, and resource groups are regularly found in bug bounty programs and red team engagements.

## Azure Blob Storage

**Azure Blob Storage** is Microsoft's object storage service. Blobs are stored in **containers** inside **storage accounts**.

Default URL format:

```
https://<storageaccount>.blob.core.windows.net/<container>/<blob>
```

### Enumerate Public Blobs

Some containers are configured for anonymous public access:

```bash
# List contents of a public container
curl "https://<storageaccount>.blob.core.windows.net/<container>?restype=container&comp=list"

# List with deleted versions included
curl "https://<storageaccount>.blob.core.windows.net/<container>?restype=container&comp=list&include=deletedwithversions"

# Required header for some operations
curl -H "x-ms-version: 2020-10-02" \
  "https://<storageaccount>.blob.core.windows.net/<container>?restype=container&comp=list"
```

### Download a Blob

```bash
# Download a publicly accessible blob
curl "https://<storageaccount>.blob.core.windows.net/<container>/<blob>" -o output

# With Azure CLI
az storage blob download \
  --account-name <storageaccount> \
  --container-name <container> \
  --name <blob> \
  --file output
```

### Find Azure Storage Accounts

```bash
# Shodan search
org:target ssl.cert.subject.cn:"*.blob.core.windows.net"

# Subdomain brute force
for name in common names; do
  curl -s -o /dev/null -w "$name: %{http_code}\n" \
    "https://$name.blob.core.windows.net/?comp=list"
done
```

## Azure Enumeration with Credentials

```bash
# Install Azure CLI
az login

# List all subscriptions
az account list

# List resource groups
az group list

# List storage accounts
az storage account list

# List VMs
az vm list

# List users in Azure AD
az ad user list

# List service principals
az ad sp list
```

## Azure Active Directory

```bash
# Check current identity
az ad signed-in-user show

# List role assignments
az role assignment list --all

# List app registrations (may have secrets)
az ad app list

# Get app credentials
az ad app credential list --id <app-id>
```

## Common Azure Attack Paths

1. **Leaked SAS token** → access Blob Storage directly
2. **Overprivileged Managed Identity** → access other Azure resources from a VM
3. **Azure AD misconfiguration** → add yourself to privileged groups
4. **Public Blob Storage** → download sensitive files (backups, config files)
5. **Function App environment variables** → leaked connection strings and API keys

```bash
# Check for SAS token exposure in URLs or code
# SAS token format: ?sv=2020-08-04&ss=b&srt=...&sp=...&sig=...

# Use an Azure function's managed identity to query metadata
curl -H "Metadata: true" \
  "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
```

## Resources

- [HackTricks — Azure Pentesting](https://cloud.hacktricks.xyz/pentesting-cloud/azure-security)
- [MicroBurst — Azure Security Assessment](https://github.com/NetSPI/MicroBurst)
- [TryHackMe — Azure Fundamentals](https://tryhackme.com/)
- [Stormspotter — Azure Red Team Visualization](https://github.com/Azure/Stormspotter)

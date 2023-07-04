
# ynab-integrations

The missing link between your banking notifications and You Need A Budget's (YNAB) API.

This project uses AWS CDK to deploy an AWS Lambda function that fetches emails periodically via IMAP, parses them into transactions, and writes them to your YNAB Budget.

## Prerequisites

- YNAB Account and [YNAB Personal Access Token](https://api.ynab.com/#personal-access-tokens)
- Email notifications from your bank
  - If your bank is worth it's salt, you should be able to configure notifications with value thresholds such that you get email notifications for any and all transactions.
- Email account with IMAP access
- Python 3.10
- AWS Account
- [AWS CDK v2](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_install)
- Docker
- Accounts configured

## Getting Started

1. Install AWS CDK
```bash
npm install -g aws-cdk
```
2. Install poetry
```bash
pip install poetry
```
3. Install dependencies
```bash
poetry install
```
4. Activate poetry shell
```bash
poetry shell
```
5. Configure your YNAB, Email and Account information in the config files
   - Refer to the [config README](./src/config/README.md) for tips and best practices
6. [Optional] If you haven't already done so, create resources needed for CDK to work.
```bash
cdk bootstrap
```
7. Test that a Cloudformation template can be created.
```bash
cdk synth
```
8. Deploy the stack.
```bash
cdk deploy
```

## Supported banks/transaction types

### United Overseas Bank (UOB)

- [Paynow transfers](./src/config/README.md#uob_paynow_email_accounts)

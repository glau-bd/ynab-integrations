# Configuration

## Example config

Refer to [example_ynab_config.ini](example_ynab_config.ini) and [example_connector_config.ini](example_connector_config.ini) for an example of how to set up the configuration files.

## YNAB Configuration

`ynab_config.ini` is used for YNAB specific configurations.

There is the `default` section for connecting to YNAB, and 1 section each for the various message parsers.

### config

This section handles connection to your YNAB Budget to write transactions.

| Key               | Type   | Description                                                                                                                                                               |
|-------------------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| YNAB_API_BASE_URL | string | Base URL for the YNAB API. Should not need to change this.                                                                                                                |
| YNAB_ACCESS_TOKEN | string | Your Personal Access Token. Obtain one from [here]( https://api.ynab.com/#personal-access-tokens ).                                                                       |
| YNAB_BUDGET_ID    | string | The ID your of YNAB Budget. You can obtain the budget ID by heading to the [YNAB API Playground](https://api.ynab.com/v1), authorising with your Access Token and calling the GET /budgets endpoint. |


### uob_paynow_email_accounts

This section handles configuration for [UobPaynowEmailParser](../message_parsers/uob_paynow_email.py).

| Key      | Type   | Description                                                                                                                                                                                                             |
|----------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| default  | string | Account that is used for your Paynow transactions. You can obtain the account ID by heading to the  [YNAB API Playground](https://api.ynab.com/v1) , authorising with your Access Token and calling the GET /budgets/{budget_id}/accounts endpoint. |
| timezone | string | Timezone that you expect the transaction time to be in. If left blank, defaults to `Asia/Singapore`|

## Connector Configuration

`connector_config.ini` is used for configuring the various connectors to fetch transaction messages.

Since each connector type can be used for multiple isntances (eg ImapConnector can be used to access multiple email accounts), each section represents an instance of a connector.

### ImapConnector

| Key                       | Type    | Description                                                        |
|---------------------------|---------|--------------------------------------------------------------------|
| connector_type            | string  | Used to identify the connector type, in this case, `ImapConnector` |
| active                    | bool    | `true` if you want it to be active, `false` otherwise              |
| user                      | string  | IMAP Username                                                      |
| password                  | string  | IMAP Password                                                      |
| host                      | string  | IMAP Host                                                          |
| port                      | integer | IMAP Port                                                          |
| ssl                       | boolean | IMAP SSL                                                           |

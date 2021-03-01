# tap-adyen

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from [Adyen Reports](https://docs.adyen.com/reporting)
- Extracts the following resources:
  - [Settlement details report](https://docs.adyen.com/reporting/settlement-detail-report) 
  - [Payment accounting report](https://docs.adyen.com/reporting/payment-accounting-report)
  - [Dispute transaction details report](https://docs.adyen.com/reporting/dispute-report)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

### Step 1: Retrieve the report user credentials
- Visit: Customer Area > Account > API credentials
- In the reporting area, enable `automatic reporting` for any of the following reports you want to use:
  - Dispute transaction details
  - Payment accounting
  - Settlement_details

### Step 2: Configure

Create a file called `adyen_config.json` in your working directory, following [sample_config.json](sample_config.json). The required parameters are the `report_user`, `company_account`, `user_password` and `merchant_account`. The `test` parameter determines whether to use the test or live environment.

This requires a `state.json` file to let the tap know from when to retrieve data. For example:
```
{
  "bookmarks": {
    "dispute_transaction_details": {
      "start_date": "2021-01-01"
    },
    "payment_accounting": {
      "start_date": "2021-01-01"
    },
    "settlement_details": {
      "batch_number": 1
    }
  }
}
```
Will replicate dispute transaction details and payment_accounting data from 2021-01-01. Settlement details will be started from batch 1.

### Step 3: Install and Run

Create a virtual Python environment for this tap. This tap has been tested with Python 3.7, 3.8 and 3.9 and might run on future versions without problems.
```
python -m venv singer-adyen
singer-adyen/bin/python -m pip install --upgrade pip
singer-adyen/bin/pip install git+https://github.com/Yoast/singer-tap-adyen.git
```

This tap can be tested by piping the data to a local JSON target. For example:

Create a virtual Python environment with `singer-json`
```
python -m venv singer-json
singer-json/bin/python -m pip install --upgrade pip
singer-json/bin/pip install target-json
```

Test the tap:

```
singer-adyen/bin/tap-adyen --state state.json -c adyen_config.json | singer-json/bin/target-json >> state_result.json
```

Copyright &copy; 2021 Yoast
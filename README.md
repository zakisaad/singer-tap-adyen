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


Copyright &copy; 2021 Yoast

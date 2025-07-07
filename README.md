# Generative AI for Observability
Exploring different usecases of AI in Observability

## Usage
1. Install depencies
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
2. Run examples in `main.py`
```
python3 main.py
```

## Examples
Experimental prompt/output results can be found in the `/examples/` folder.
- `alert_summariser.txt` - Summarise alert details.
- `clickhouse_query_generator.txt` - Generates a suitable Clickhouse Query from Natural Language.
- `grafana_dashboard_generator.txt` - Generates a scaffold of a dashboard JSON object, which can be imported on Grafana.
- `log_filter.txt` - Extract key metadata from logs.
- `prometheus_config_generator.txt` - Generates a suitable Prometheus custom job definition from Natural Language.
- `onboarding_guide.txt` - Generates an onboarding checklist with the list of fulfilled and unfulfilled items.
- `review_infra_code.txt` - Review infra-as-a-code and suggest any errors or refinements.
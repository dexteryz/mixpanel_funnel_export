# Mixpanel funnel export scripts

This library contains two scripts that help you easily export your Mixpanel funnels to a CSV file or SQL DB to run your analyses.

### Preparing your funnel export

Make sure you update the files with your specific variables, i.e. API key/secret, output file name, funnel parameters and output table labels.

### Running your funnel export

Getting SQL output

```
python funnels_sql.py
```

Getting CSV output

```
python funnels_csv.py
```

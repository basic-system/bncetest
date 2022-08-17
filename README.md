### Build container

```
docker build -t bnce .
```

### Run container

```
docker run -d -p 8000:8000 bnce
```

### How to test results

```
curl 'http://localhost:8000/metrics'
```

Output:

```
...
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06
# HELP symblol_spread Change in symbols, spread
# TYPE symblol_spread gauge
symblol_spread{symbol="BTCUSDT"} 0.819999999999709
symblol_spread{symbol="ETHUSDT"} 0.009999999999990905
symblol_spread{symbol="DOGEUSDT"} 9.999999999996123e-06
symblol_spread{symbol="SHIBUSDT"} 1.0000000000001598e-08
symblol_spread{symbol="EOSUSDT"} 0.0009999999999998899
# HELP symblol_price_change Change in symbols, price
# TYPE symblol_price_change gauge
symblol_price_change{symbol="BTCUSDT"} -17.840000000000146
symblol_price_change{symbol="ETHUSDT"} 0.6999999999998181
symblol_price_change{symbol="DOGEUSDT"} 6.0000000000004494e-05
symblol_price_change{symbol="SHIBUSDT"} 1.0000000000001598e-08
symblol_price_change{symbol="EOSUSDT"} 0.0
dnslookup: 0.007265 | connect: 0.007481 | app
```
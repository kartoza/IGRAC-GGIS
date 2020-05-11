# IGRAC-GGIS

## QUICK INSTALLATION GUIDE
```
git clone https://github.com/kartoza/IGRAC-GGIS.git
cd IGRAC-GGIS/deployment
make build
make up
```

For first time usage, add this command:
```
make db-restore
```

The mapstore frontend will be available at `http://localhost/`

To stop containers:
```
make kill
```

To stop and delete containers:
```
make rm
```

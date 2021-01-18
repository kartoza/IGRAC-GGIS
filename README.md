# IGRAC-GGIS

## QUICK INSTALLATION GUIDE
```
git clone https://github.com/kartoza/IGRAC-GGIS.git
cd IGRAC-GGIS/deployment
make build
make up
make collectstatic
```

The web will be available at `http://localhost/`

To stop containers:
```
make kill
```

To stop and delete containers:
```
make rm
```

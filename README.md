# PETL Exercise

Small app integrating with https://swapi.dev/ and using petl (https://petl.readthedocs.io/en/stable/) for data manipulation

## Startup
- Create new `.env` based on `.example.env`
- Run `docker-compose up` or `invoke compose`

### Tasks
Common tasks are simplified using pyinvoke (http://www.pyinvoke.org/)
- `invoke compose` - run full stack
- `invoke lint` - lint code using isort (https://pycqa.github.io/isort/) and black (https://black.readthedocs.io/en/stable/)
- `invoke shell $SERVICE` - run bash shell inside given service
- `invoke managepy $COMMAND` - run django manage.py command inside backend service

from invoke import task

USE_BUILDKIT_ENV = {
    "COMPOSE_DOCKER_CLI_BUILD": "1",
    "DOCKER_BUILDKIT": "1",
}


@task
def shell(c, service):
    c.run("docker-compose exec {} bash".format(service), pty=True)


@task
def managepy(c, command):
    c.run("docker-compose exec backend python backend/manage.py {}".format(command), pty=True)


@task
def compose(c):
    c.run("docker-compose stop && docker-compose up --build --abort-on-container-exit", env=USE_BUILDKIT_ENV)


@task
def lint(c):
    c.run("isort . && black .")

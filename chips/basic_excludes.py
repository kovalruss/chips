_EXCLUDES = ['chips', 'venv', '.env']
DOCKER_EXCLUDES = ['Dockerfile*', 'docker-*']
DJANGO_EXCLUDES = ['manage.py']
GIT_EXCLUDES = ['.git*']
TESTING_EXCLUDES = ['pytest.ini', 'tests', '.tox', '.coverage']
PYTHON_EXCLUDES = ['*.pyc', '.mypy_cache', '*.py[co]', '*.DS_*', ]
PACKAGES_EXCLUDES = ['*.egg', '*.egg-info', 'dist', 'build', 'eggs', 'parts', 'bin', 'var',
                     'sdist', 'develop-eggs', '.installed.cfg']
PIP_EXCLUDES = ['Pipfile', 'Pipfile.lock', 'requirements.txt', 'pip-*']
FRONTEND_EXCLUDES = ['node_modules', ]
OTHER_EXCLUDES = ['Makefile', 'README.md', '.pre-commit-*', '.flake8', '.idea', '*.vscode',
                  '*.mo', 'db.sqlite3', '.cache', '/.bash_history', ]

BASIC_EXCLUDES = _EXCLUDES + DOCKER_EXCLUDES + DJANGO_EXCLUDES + GIT_EXCLUDES \
                 + TESTING_EXCLUDES + PYTHON_EXCLUDES + PACKAGES_EXCLUDES + \
                 PIP_EXCLUDES + FRONTEND_EXCLUDES + OTHER_EXCLUDES

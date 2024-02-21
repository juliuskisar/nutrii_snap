# nutrii_snap

## Virtual Environment Mode

First, create your virtual environment:

```bash
$ python3 -m venv venv

```

Then, activate your virtual environment:

```bash
$ source venv/bin/activate
```

Then, install dependencies:

```bash
$ pip install -r requirements.txt
```

Create `.env` file:

```bash
$ cp .env.EXAMPLE .env
```

Then, run the application:

```bash
$ uvicorn main:app --reload
```

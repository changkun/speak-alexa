# MagicLingua SprachApp

An Alexa Skill App to practice language such as English/German/Spanish etc. Development based on `flask-ask`

## Running the skill locally

To run the skill, do the following:

1. install virtualenv, **mongodb**, and all dependencies:

```shell
# install `virtualenv` and `mongodb` before the following setups
# setup python environment
virtualenv -p python3 .env
source .env/bin/activate
pip install -r req.txt
```

2. init your local mongodb database:

```python
python src/init_db.py
```

3. Start the flask-ask app on your localhost:

```python   
python src/main.py
```

4. Tunnel your localhost to a https server. In a new shell:

```shell
# linux
tools/ngrok-linux http 5005
# macos
tools/ngrok-mac http 5005
```

5. Go to amazon.developer and fill in your https server adress (ngrok gives you a new server every time it is startet). Look at the output of ngrok and find the server name. It should look similar to this: https://9ee1890b.ngrok.io. Log in to amazon.developer, click on the skill, click on configuration, and fill in the server name, suffixed by "/alexa". In my case: https://9ee1890b.ngrok.io/alexa
6. Click on "Next", chose "**My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority**", click on next again.
7. Got to https://echosim.io/, log in with your amazon developer account. You can now test the skill! Say "Open MagicLingua" into you microphone! Or you can interact with Alexa by say "Alexa, open MagicLingua"

## Deployment

### Redeploy the skills

**step 1:** locally test your development, make sure the code will **not** crash the entire server, and commit your code to our Github repository.

**step 2:** login to the server, in your console, input:

```shell
ssh ubuntu@34.249.7.223 # you need configure ssh pubkey to the server
```

​	now you are logged on the server.

**step 3**: go to `~/team-voice`, input:

```bash
git pull
```

​	since this repository is a private repository, you will need input your github `username` and `passcode`. Then the whole deployment is finished.

### First deployment

If you are deploying the skill for the first time, you need read the following:

**Step 1**: the first three step is as same as before: make sure your code runs correct login to the server, go to the folder `~/team-voice`, `git pull` .

**Step 2**: create a new `tmux` session for `ngrok`:

```shell
tmux new -s ngrok-service-5005
```

​	You will see a green bar on the console bottom if you are correct.

**Step 3**: now you are in a `tmux` session, run the ngrok:

```shell
./ngrok http 5005
```

​	Write down the https ngrok address, you will need this address for your new skill on `developer.amazon.com`.

**Step 4**: detach the tmux session: press `ctrl+b` first, release all keys, then press `d`. You will back to the normal shell session without the green bar.

**Step 5**: create a new tmux session for the skill:

```shell
tmux new -s magiclingua-skill
```

​	You will see a green bar on the console bottom if you are correct.

**Step 6**: now you are in **another** `tmux` session, before you run, you need trigger the virtual environment for python and init the mongodb database:

```shell
virtualenv -p python3 .env
source .env/bin/activate
pip install -r req.txt
python src/init_db.py
```

​	you will see a `venv` mark in the shell prompt, and the `init_db.py` script should output `done`.

**Step 7**: Run the skill:

```shell
python src/main.py
```

​	You can use `pip` install the requirements if the running failed.

**Step 8**: detach the tmux session: press `ctrl+b`, release all keys, then press `d`, you will back to the normal shell session without the green bar. Then fill the entire URL to `developer.amazon.com` you are finished.

## Q&A

- How can I attach to the tmux sessions what I detached?

> You can use: `tmux list-sessions` to check what are the names of running tmux sessions, for example, the name is: `ngrok-service`
>
> Then you can use: `tmux attach -d -t ngrok-service-5005` to attach to your former sessions.
>

- How can I get a summary over running processes on localhost and see their ports?
  `netstat -ntlp | grep LISTEN`

## License

MIT
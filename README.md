# emailapi

## Instructions of deployment with gmail

### Gmail Setup
In https://mail.google.com/mail/u/0/#settings/fwdandpop:

- Enable IMAP

In https://myaccount.google.com/ -> Security:

- Enable 2FA in account

- Generate app password


Set in .env:

USERNAME=youremail@gmail.com \
PASSWORD="Put here the app password" \
IMAP_URL=imap.gmail.com \
SMTP_URL=smtp.gmail.com 


### Local setup

#### Install dependencies

On Windows:

Install Python 3.10 from the official website / Microsoft Store.

On Ubuntu

```shell
sudo apt install python3.10
```


#### Install packages

Run in terminal: 

```shell
pip install -r requirements.txt
```

#### Run loop

```shell
python email_loop.py
```
or
```shell
python3 email_loop.py
```
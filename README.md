# leboncrevard

This is a simple Python scrapper for the french ad website leboncoin.fr that mails you the latest ads you are interested in.

## Synopsis & Motivation

I developed this small tool for two reasons:
- laziness: I don't want to go to the website and manually search for stuff every days,
- speed: I want to receive some ads quickly to be contact the sellers ASAP.

## Usage

- Install the project:

```shell
$ pip install leboncrevard
```

- You can set the configuration with the following environment variables (an SMTP server that supports STARTTLS is mandatory, Gmail is fine):

```shell
$ export LBC_SMTP_USER="user"
$ export LBC_SMTP_PASS="pass"
$ export LBC_SMTP_SERVER="smtp.gmail.com:587"
$ export LBC_JOB_FILE="jobs.csv"
$ export LBC_DELETE_FILE="delete.csv"
```

- Fill the "job file" defined by `LBC_JOB_FILE` (see syntax below), default is `jobs.csv`
- Run the application:

```shell
$ leboncrevard &>> leboncrevard.log
```

The entries in both of these files should look like this:

```
"Title","http://www.leboncoin.fr/voitures/offres/pays_de_la_loire/occasions/?f=a&th=1&q=fuego",60,your.mail@yourprovider.com
```

The numeric field is the time interval (in minutes) you want between scraping sessions.
You can add new entries, the script parses the file regularly and will add them.
You can also delete jobs by moving then from the "job file" to the "delete file" (interval and recipients are ignored when deleting a job, all instances are removed).

The script will create csv files using job names in order to store an history of already mailed ads.

## Limitations and bugs

Seems to run quite well for me, but there may be bugs that I did not foresee or triggered through usage. Feel free to open issues and pull requests.

## Disclaimer

Usual stuff, I am not a professional Python developer and made this for my personal use. Feel free to use it at your own risks.

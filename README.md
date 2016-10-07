# Github Contribution Graph Maximizer
The purpose of this project is to manipulate the user's contribution graph in a way that illustrates consistent effort being pushed to Github throughout the year. Often, strong contributors are prone to squashing their commits or contributing to projects outside Github. As a result, they may have what looks like a poor contribution graphs and in turn this leads to unfair prejudices by peers and a lack of self-worth after reflecting on one's lack of contributions. This project intends to address the deficiencies of summary representations of one’s efforts such as the Github contribution graph.

### Before
![Before](https://raw.githubusercontent.com/geedo0/github_maximizer/master/img/before.png)
### After
![After](https://raw.githubusercontent.com/geedo0/github_maximizer/master/img/after.png)

## Prerequisites
* Python 3
* Pip
* Git

## Quick Start
These commands will install github_maximizer and its prerequisites. Then when you run the script it will create the repository specified by -n and contribute a year's worth of commits to the Github account specified by the config file.
```
git clone https://github.com/geedo0/github_maximizer.git
cd github_maximizer
pip install -r requirements.txt
./github_maximizer.py -n 'stateless_info_client' -c sample_config.ini
```

## Cron Mode
After generating a year's worth of contributions, it may be worthwhile to run the script as a daily cron job with '-d 1'. That way, the script will randomly generate a series of commits and push them up for you each day. The result is an unbroken chain of contributions for your profile.
```
# crontab
# m h  dom mon dow   command
0 0 * * * * /scripts/github_maximizer/github_maximizer.py -n stateless_info_client -c /scripts/github_maximizer/sample_config.ini -d 1
```

## Notes
* This uses a Poisson distribution for determining how many commits to make on any given day. In general, it will look like you commit more often on weekdays than on weekends.
* Your password is stored in plain text and is used without much concern for security by this script. Make sure you read the code and understand your risks.
* The commits generated are obviously fake, so if you care about that mark the repository as private and set Github to count private contributions.
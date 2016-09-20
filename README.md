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
These commands will install github_maximizer and its prerequisites. Then when you run the script it will create the repository specified by -n and contribute a year's worth of commits to the Github account specified by the -u parameter.
```
git clone https://github.com/geedo0/github_maximizer.git
cd github_maximizer
pip install -r requirements.txt
./github_maximizer.py -n 'stateless_info_client' -u geedo0 -p Password1!
```

## Notes
* This uses a Poisson distribution for determining how many commits to make on any given day. In general, it will look like you commit more often on weekdays than on weekends.
* Your password is passed as a command line parameter. That means it will be stored in plaintext to your bash history, make sure to wipe it after.
* The commits generated are obviously fake, so if you care about that mark the repository as private and set Github to count private contributions.
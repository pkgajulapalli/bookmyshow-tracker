### BookMyShow ticket tracker
Developed using python 3.9.9. We use [sendinblue](https://www.sendinblue.com/) api to send emails.

### Installation
```shell
python --version
pip install -r requirements.txt

## Following setup can be ignored if sending emails is not required.
# Setup sendinblue account for sending emails.
# If below command doesn't work, refer https://developers.sendinblue.com/recipes/send-transactional-emails-in-python
pip install git+https://github.com/sendinblue/APIv3-python-library.git
export SENDINBLUE_API_KEY="API_KEY_FROM_SENDINBLUE"
```

### Usage
```shell
python bookmyshow_tracker.py -m MOVIE_NAME -u BOOK_MY_SHOW_LINK
# sample book my show link - https://in.bookmyshow.com/buytickets/pvr-soul-spirit-central-mall-bellandur/cinema-bang-CXBL-MT/20220603
```

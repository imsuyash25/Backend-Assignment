from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MAX_RETRY_FOR_SESSION = 5
BACK_OFF_FACTOR = 0.3
ERROR_CODES = (500, 502, 503, 504)


def make_retry(retries=MAX_RETRY_FOR_SESSION,
                back_off_factor=BACK_OFF_FACTOR,
                status_force_list=ERROR_CODES,
                session=None):
    session = session

    retry = Retry(total=retries,
                  connect=retries,
                  backoff_factor=back_off_factor,
                  status_forcelist=status_force_list)

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

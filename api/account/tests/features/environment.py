from behave import fixture, use_fixture

from account_api.api import acct
from selene.testing.account import add_account, remove_account
from selene.testing.account_geography import add_account_geography
from selene.testing.agreement import add_agreements, remove_agreements
from selene.util.cache import SeleneCache
from selene.util.db import connect_to_db


@fixture
def acct_api_client(context):
    acct.testing = True
    context.client_config = acct.config
    context.client = acct.test_client()

    yield context.client


def before_all(context):
    use_fixture(acct_api_client, context)
    context.db = connect_to_db(context.client_config['DB_CONNECTION_CONFIG'])
    agreements = add_agreements(context.db)
    context.terms_of_use = agreements[0]
    context.privacy_policy = agreements[1]
    context.open_dataset = agreements[2]


def after_all(context):
    remove_agreements(
        context.db,
        [context.privacy_policy, context.terms_of_use, context.open_dataset]
    )


def before_scenario(context, _):
    account = add_account(context.db)
    context.accounts = dict(foo=account)
    context.geography_id = add_account_geography(context.db, account)


def after_scenario(context, _):
    """Scenario-level cleanup.

    The database is setup with cascading deletes that take care of cleaning up[
    referential integrity for us.  All we have to do here is delete the account
    and all rows on all tables related to that account will also be deleted.
    """

    for account in context.accounts.values():
        remove_account(context.db, account)
    _clean_cache()


def _clean_cache():
    cache = SeleneCache()
    cache.delete('pairing.token:this is a token')

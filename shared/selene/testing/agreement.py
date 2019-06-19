from datetime import date, timedelta
from typing import Tuple, List

from selene.data.account import (
    Agreement,
    AgreementRepository,
    OPEN_DATASET,
    PRIVACY_POLICY,
    TERMS_OF_USE
)


def _build_test_terms_of_use():
    return Agreement(
        type=TERMS_OF_USE,
        version='Holy Grail',
        content='I agree that all the tests I write for this application will '
                'be in the theme of Monty Python and the Holy Grail.  If you '
                'do not agree with these terms, I will be forced to say "Ni!" '
                'until such time as you agree',
        effective_date=date.today() - timedelta(days=1)
)


def _build_test_privacy_policy():
    return Agreement(
        type=PRIVACY_POLICY,
        version='Holy Grail',
        content='First, shalt thou take out the Holy Pin.  Then shalt thou '
                'count to three.  No more.  No less.  Three shalt be the '
                'number thou shalt count and the number of the counting shall '
                'be three.  Four shalt thou not count, nor either count thou '
                'two, excepting that thou then proceed to three.  Five is '
                'right out.  Once the number three, being the third number, '
                'be reached, then lobbest thou Holy Hand Grenade of Antioch '
                'towards thy foe, who, being naughty in My sight, '
                'shall snuff it.',
        effective_date=date.today() - timedelta(days=1)
    )


def _build_open_dataset():
    return Agreement(
        type=OPEN_DATASET,
        version='Holy Grail',
        effective_date=date.today() - timedelta(days=1)
    )


def add_agreements(db) -> Tuple[Agreement, Agreement, Agreement]:
    terms_of_use = _build_test_terms_of_use()
    privacy_policy = _build_test_privacy_policy()
    open_dataset = _build_open_dataset()
    agreement_repository = AgreementRepository(db)
    terms_of_use.id = agreement_repository.add(terms_of_use)
    privacy_policy.id = agreement_repository.add(privacy_policy)
    open_dataset.id = agreement_repository.add(open_dataset)

    return terms_of_use, privacy_policy, open_dataset


def remove_agreements(db, agreements: List[Agreement]):
    for agreement in agreements:
        agreement_repository = AgreementRepository(db)
        agreement_repository.remove(agreement, testing=True)

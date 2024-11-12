from typing import Union

from app.models import CharityProject, Donation


def process_investment(
    target: Union[CharityProject, Donation],
    sources: list[Union[CharityProject, Donation]]
):
    update_sources = sources

    for obj in update_sources:
        amoun_to_invest = min(
            target.available_funds, obj.available_funds
        )
        target.invested_amount += amoun_to_invest
        obj.invested_amount += amoun_to_invest

        if obj.invested_amount == obj.full_amount:
            obj.to_close()

        if target.invested_amount == target.full_amount:
            target.to_close()
            break

    update_sources.append(target)

    return update_sources

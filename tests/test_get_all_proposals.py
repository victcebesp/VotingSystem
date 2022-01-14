from brownie import network, VotingSystem, exceptions, accounts, config
import pytest
from scripts.helpful_scripts import FORKED_LOCAL_ENVIRONMENTS, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

def test_get_all_proposals_returns_zero_proposals_when_none_propsal_was_added():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"], 
        {"from": account}
    )
    proposals = voting_system_contract.getAllProposals()
    assert len(proposals) == 0

def test_get_all_proposals_returns_one_proposal_when_only_one_propsal_was_added():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"], 
        {"from": account}
    )
    expected_is_open = True
    expected_description = "Description"
    options = ["2", "3"]
    expected_options = [(o, 0) for o in options]
    expected_id = 0
    add_tx = voting_system_contract.addProposal(
        expected_is_open, 
        expected_description, 
        options, 
        {"from": account}
    )
    add_tx.wait(1)
    proposals = voting_system_contract.getAllProposals()
    assert len(proposals) == 1
    assert proposals[0][0] == expected_id
    assert proposals[0][1] == expected_is_open
    assert proposals[0][2] == expected_description
    assert proposals[0][3] == expected_options


def test_get_all_proposals_returns_two_proposals_when_two_propsals_were_added():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"], 
        {"from": account}
    )
    first_proposal_expected_is_open = True
    first_proposal_expected_description = "Description"
    first_proposal_options = ["2", "3"]
    first_proposal_expected_options = [(o, 0) for o in first_proposal_options]
    first_proposal_expected_id = 0
    add_tx = voting_system_contract.addProposal(
        first_proposal_expected_is_open, 
        first_proposal_expected_description, 
        first_proposal_options, 
        {"from": account}
    )
    add_tx.wait(1)
    second_proposal_expected_is_open = True
    second_proposal_expected_description = "Description of proposal 2"
    second_proposal_options = ["3", "4"]
    second_proposal_expected_options = [(o, 0) for o in second_proposal_options]
    second_proposal_expected_id = 1
    add_tx = voting_system_contract.addProposal(
        second_proposal_expected_is_open, 
        second_proposal_expected_description, 
        second_proposal_options, 
        {"from": account}
    )
    add_tx.wait(1)
    proposals = voting_system_contract.getAllProposals()
    print(proposals)
    assert len(proposals) == 2

    assert proposals[0][0] == first_proposal_expected_id
    assert proposals[0][1] == first_proposal_expected_is_open
    assert proposals[0][2] == first_proposal_expected_description
    assert proposals[0][3] == first_proposal_expected_options

    assert proposals[1][0] == second_proposal_expected_id
    assert proposals[1][1] == second_proposal_expected_is_open
    assert proposals[1][2] == second_proposal_expected_description
    assert proposals[1][3] == second_proposal_expected_options
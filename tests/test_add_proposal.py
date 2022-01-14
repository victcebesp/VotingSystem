from scripts.helpful_scripts import FORKED_LOCAL_ENVIRONMENTS, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import VotingSystem, exceptions, network, accounts, config
import pytest

def test_can_add_proposal():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"],
        {"from": account}
    )
    assert voting_system_contract.proposalsAmount() == 0
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
    assert voting_system_contract.proposalsAmount() == 1
    created_proposal = voting_system_contract.getProposal(expected_id)
    assert created_proposal[0] == expected_id
    assert created_proposal[1] == expected_is_open
    assert created_proposal[2] == expected_description
    assert created_proposal[3] == expected_options

def test_account_not_owner_cannot_add_proposal():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"], 
        {"from": account}
    )
    with pytest.raises(exceptions.VirtualMachineError):
        voting_system_contract.addProposal(True, "Description", ["2", "3"], {"from": accounts[1]})

def test_owner_can_add_multiple_proposals():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"],
        {"from": account}
    )

    expected_first_proposal_is_open = True
    expected_first_proposal_description = "Description"
    first_proposal_options = ["2", "3"]
    expected_first_proposal_options = [(o, 0) for o in first_proposal_options]
    expected_first_proposal_id = 0
    add_tx = voting_system_contract.addProposal(
        expected_first_proposal_is_open, 
        expected_first_proposal_description, 
        first_proposal_options, 
        {"from": account}
    )
    add_tx.wait(1)
    assert voting_system_contract.proposalsAmount() == 1
    createdProposal = voting_system_contract.getProposal(expected_first_proposal_id)
    print(createdProposal)
    assert createdProposal[0] == expected_first_proposal_id
    assert createdProposal[1] == expected_first_proposal_is_open
    assert createdProposal[2] == expected_first_proposal_description
    assert createdProposal[3] == expected_first_proposal_options

    expected_second_proposal_is_open = True
    expected_second_proposal_description = "Description for proposal nº2"
    second_proposal_options = ["Yes", "No"]
    expected_second_proposal_options = [(o, 0) for o in second_proposal_options]
    expected_second_proposal_id = 1
    add_tx = voting_system_contract.addProposal(
        expected_second_proposal_is_open, 
        expected_second_proposal_description, 
        second_proposal_options, 
        {"from": account}
    )
    add_tx.wait(1)
    assert voting_system_contract.proposalsAmount() == 2
    createdProposal = voting_system_contract.getProposal(expected_second_proposal_id)
    assert createdProposal[0] == expected_second_proposal_id
    assert createdProposal[1] == expected_second_proposal_is_open
    assert createdProposal[2] == expected_second_proposal_description
    assert createdProposal[3] == expected_second_proposal_options

def test_cannot_add_proposal_without_options():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"], 
        {"from": account}
    )
    assert voting_system_contract.proposalsAmount() == 0
    with pytest.raises(exceptions.VirtualMachineError):
        voting_system_contract.addProposal(True, "Description", [], {"from": account})

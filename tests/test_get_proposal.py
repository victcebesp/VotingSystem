from brownie import network, VotingSystem, exceptions, config
import pytest
from scripts.helpful_scripts import FORKED_LOCAL_ENVIRONMENTS, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

def test_can_get_proposal_by_id():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(config["networks"][network.show_active()]["collection_contract"], {"from": account})
    expected_id = 0
    expected_is_open = True
    expected_description = "Should create Solidity course?"
    options = ["Yes", "No"]
    expected_options = [(o, 0) for o in options]
    add_tx = voting_system_contract.addProposal(
        expected_is_open, 
        expected_description, 
        options, 
        {"from": account}
    )
    add_tx.wait(1)
    proposal = voting_system_contract.getProposal(0)
    print(proposal)
    assert proposal[0] == expected_id
    assert proposal[1] == expected_is_open
    assert proposal[2] == expected_description
    assert proposal[3] == expected_options

def test_cannot_get_nonexistent_proposal():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(config["networks"][network.show_active()]["collection_contract"], {"from": account})
    with pytest.raises(exceptions.VirtualMachineError):
        voting_system_contract.getProposal(0)
    
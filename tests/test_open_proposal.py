from brownie import network, VotingSystem, exceptions, accounts, config
import pytest
from scripts.helpful_scripts import FORKED_LOCAL_ENVIRONMENTS, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

def test_owner_can_open_proposal():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"], 
        {"from": account}
    )
    add_tx = voting_system_contract.addProposal(
        False, 
        "Should create Solidity course?", 
        ["Yes", "No"], 
        {"from": account}
    )
    add_tx.wait(1)
    open_proposal_tx = voting_system_contract.openProposal(0, {"from": account})
    open_proposal_tx.wait(1)
    proposal = voting_system_contract.getProposal(0)
    assert proposal[1] == True

def test_non_owner_cannot_open_proposal():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"], 
        {"from": account}
    )
    add_tx = voting_system_contract.addProposal(
        False, 
        "Should create Solidity course?", 
        ["Yes", "No"], 
        {"from": account}
    )
    add_tx.wait(1)
    with pytest.raises(exceptions.VirtualMachineError):
        voting_system_contract.openProposal(0, {"from": accounts[1]})

def test_cannot_open_nonexistent_proposal():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"], 
        {"from": account}
    )
    with pytest.raises(exceptions.VirtualMachineError):
        voting_system_contract.openProposal(3, {"from": account})
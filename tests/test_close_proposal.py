from brownie import network, VotingSystem, exceptions, accounts, config
import pytest
from scripts.helpful_scripts import FORKED_LOCAL_ENVIRONMENTS, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

def test_owner_can_close_proposal():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"], 
        {"from": account}
    )
    add_tx = voting_system_contract.addProposal(
        True, 
        "Should create Solidity course?", 
        ["Yes", "No"], 
        {"from": account}
    )
    add_tx.wait(1)
    open_proposal_tx = voting_system_contract.closeProposal(0, {"from": account})
    open_proposal_tx.wait(1)
    proposal = voting_system_contract.getProposal(0)
    assert proposal[1] == False

def test_non_owner_cannot_close_proposal():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"], 
        {"from": account}
    )
    add_tx = voting_system_contract.addProposal(
        True, 
        "Should create Solidity course?", 
        ["Yes", "No"], 
        {"from": account}
    )
    add_tx.wait(1)
    with pytest.raises(exceptions.VirtualMachineError):
        voting_system_contract.closeProposal(0, {"from": accounts[1]})

def test_cannot_close_nonexistent_proposal():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"], 
        {"from": account}
    )
    with pytest.raises(exceptions.VirtualMachineError):
        voting_system_contract.closeProposal(3, {"from": account})
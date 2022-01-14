from brownie import network, VotingSystem, exceptions, config
import pytest
from scripts.helpful_scripts import FORKED_LOCAL_ENVIRONMENTS, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from dotenv import load_dotenv
import os

load_dotenv()

ID = 0
IS_OPEN = 1
DESCRIPTION = 2
OPTIONS = 3
OPTION_TEXT = 0
OPTION_VOTES = 1

def test_collector_can_vote():
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
    expected_voted_option = 1
    vote_tx = voting_system_contract.vote(0, expected_voted_option, os.getenv("TOKEN_ID"), {"from": account})
    vote_tx.wait(1)
    voted_option = voting_system_contract.getUserAnswerForProposal(0, os.getenv("TOKEN_ID"))
    assert voted_option == expected_voted_option
    proposal = voting_system_contract.getProposal(0)
    assert proposal[OPTIONS][expected_voted_option - 1][OPTION_VOTES] == 1
    
def test_collector_cannot_vote_twice():
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
    expected_voted_option = 1
    vote_tx = voting_system_contract.vote(0, expected_voted_option, os.getenv("TOKEN_ID"), {"from": account})
    vote_tx.wait(1)
    expected_voted_option = 2
    with pytest.raises(exceptions.VirtualMachineError):
        vote_tx = voting_system_contract.vote(0, expected_voted_option, os.getenv("TOKEN_ID"), {"from": account})

def test_collector_cannot_vote_if_proposal_is_not_open():
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
        voting_system_contract.vote(0, 1, os.getenv("TOKEN_ID"), {"from": account})

def test_collector_can_vote_after_owner_opened_proposal():
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
        voting_system_contract.vote(0, 1, os.getenv("TOKEN_ID"), {"from": account})

    open_tx = voting_system_contract.openProposal(0, {"from": account})
    open_tx.wait(1)
    expected_voted_option = 1
    vote_tx = voting_system_contract.vote(0, expected_voted_option, os.getenv("TOKEN_ID"), {"from": account})
    vote_tx.wait(1)
    voted_option = voting_system_contract.getUserAnswerForProposal(0, os.getenv("TOKEN_ID"))
    assert voted_option == expected_voted_option
    proposal = voting_system_contract.getProposal(0)
    assert proposal[OPTIONS][expected_voted_option - 1][OPTION_VOTES] == 1

def test_voted_option_cannot_be_zero():
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
        voting_system_contract.vote(0, 0, os.getenv("TOKEN_ID"), {"from": account})

def test_voted_option_cannot_be_out_of_bound():
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
        voting_system_contract.vote(0, 3, os.getenv("TOKEN_ID"), {"from": account})

def test_cannot_vote_nonexistent_proposal():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"], 
        {"from": account}
    )
    with pytest.raises(exceptions.VirtualMachineError):
        voting_system_contract.vote(0, 0, os.getenv("TOKEN_ID"), {"from": account})

def test_collector_can_vote_multiple_proposals():
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
    add_tx = voting_system_contract.addProposal(
        True, 
        "Should publish new video?", 
        ["Yes", "No"], 
        {"from": account}
    )
    add_tx.wait(1)
    expected_voted_option_for_first_proposal = 1
    vote_tx = voting_system_contract.vote(0, expected_voted_option_for_first_proposal, os.getenv("TOKEN_ID"), {"from": account})
    vote_tx.wait(1)
    voted_option = voting_system_contract.getUserAnswerForProposal(0, os.getenv("TOKEN_ID"))
    assert voted_option == expected_voted_option_for_first_proposal
    proposal = voting_system_contract.getProposal(0)
    assert proposal[OPTIONS][expected_voted_option_for_first_proposal - 1][OPTION_VOTES] == 1

    expected_voted_option_for_second_proposal = 2
    vote_tx = voting_system_contract.vote(1, expected_voted_option_for_second_proposal, os.getenv("TOKEN_ID"), {"from": account})
    vote_tx.wait(1)
    voted_option = voting_system_contract.getUserAnswerForProposal(1, os.getenv("TOKEN_ID"))
    assert voted_option == expected_voted_option_for_second_proposal
    proposal = voting_system_contract.getProposal(1)
    assert proposal[OPTIONS][expected_voted_option_for_second_proposal - 1][OPTION_VOTES] == 1

def test_non_collector_cannot_vote():
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
        voting_system_contract.vote(0, 1, os.getenv("TOKEN_ID"), {"from": get_account(index=1)})
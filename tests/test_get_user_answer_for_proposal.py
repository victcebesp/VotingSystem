from brownie import network, VotingSystem, exceptions, config
import pytest
from scripts.helpful_scripts import FORKED_LOCAL_ENVIRONMENTS, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from dotenv import load_dotenv
import os 

load_dotenv()

def test_cannot_get_user_answer_from_nonexistent_proposal():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and
        network.show_active() not in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for local testing")

    account = get_account()
    voting_system_contract = VotingSystem.deploy(
        config["networks"][network.show_active()]["collection_contract"], 
        {"from": account}
    )
    with pytest.raises(exceptions.VirtualMachineError):
        voting_system_contract.getUserAnswerForProposal(3, os.getenv("TOKEN_ID"), {"from": account})
from scripts.helpful_scripts import get_account
from brownie import VotingSystem
from dotenv import load_dotenv
import os

load_dotenv()

def deploy():
    account = get_account()
    voting_system_contract = VotingSystem.deploy({"from": account})
    add_tx = voting_system_contract.addProposal(True, "Description", ["2", "3"], {"from": account})
    add_tx.wait(1)
    print("Proposal added!")
    print(voting_system_contract.getProposal(0))
    answer = voting_system_contract.getUserAnswerForProposal(0, os.getenv("TOKEN_ID"))
    print(answer)
    voting_tx = voting_system_contract.vote(0, 1, os.getenv("TOKEN_ID"), {"from": account})
    voting_tx.wait(1)
    answer = voting_system_contract.getUserAnswerForProposal(0, os.getenv("TOKEN_ID"))
    print(answer)

def main():
    deploy()